#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查并可选自动修复 Markdown 图片路径规范。

规则：
1. draft: true 文章跳过
2. 单文章图片目标目录：docs/<栏目>/image/<文章slug>/文件名
3. 多文章共享同一图片时，移动到 docs/assets/shared/<hash8>-<文件名>
4. 输出 JSON 报告和 Markdown 汇总

用法：
  python scripts/normalize_images.py --check
  python scripts/normalize_images.py --fix --report-json artifacts/image-fix-report.json --summary-md artifacts/image-fix-summary.md
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

IMAGE_PATTERN = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')
HTML_IMAGE_PATTERN = re.compile(r'<img\s+[^>]*src=["\']([^"\']+)["\']', re.IGNORECASE)
SKIP_PREFIXES = ('http://', 'https://', 'data:', 'mailto:', '#', '/')


@dataclass
class ImageRef:
    raw_path: str
    full_match: str
    start: int
    end: int
    kind: str


@dataclass
class Failure:
    article: str
    image: str
    reason: str

    def to_dict(self) -> dict[str, str]:
        return {'article': self.article, 'image': self.image, 'reason': self.reason}


class Context:
    def __init__(self, mode: str) -> None:
        self.mode = mode
        self.scanned_articles = 0
        self.skipped_draft_articles: list[str] = []
        self.total_image_refs = 0
        self.invalid_path_refs = 0
        self.moved_images_success = 0
        self.moved_images_failed = 0
        self.updated_articles_success = 0
        self.updated_articles_failed = 0
        self.shared_images_detected = 0
        self.failures: list[Failure] = []



def extract_front_matter(text: str) -> str | None:
    if not text.startswith('---'):
        return None
    lines = text.splitlines()
    if not lines or lines[0].strip() != '---':
        return None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == '---':
            return '\n'.join(lines[1:idx])
    return ''



def is_draft_markdown(path: Path) -> bool:
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        return False

    front_matter = extract_front_matter(text)
    if front_matter in (None, ''):
        return False

    try:
        data = yaml.safe_load(front_matter) if front_matter.strip() else {}
    except Exception:
        return False

    return isinstance(data, dict) and data.get('draft') is True



def slugify_post_name(name: str) -> str:
    slug = re.sub(r'\s+', '-', name.strip())
    slug = slug.replace('/', '-').replace('\\', '-')
    return slug or 'post'



def parse_image_refs(content: str) -> list[ImageRef]:
    refs: list[ImageRef] = []
    for match in IMAGE_PATTERN.finditer(content):
        refs.append(ImageRef(raw_path=match.group(1).strip(), full_match=match.group(0), start=match.start(1), end=match.end(1), kind='markdown'))
    for match in HTML_IMAGE_PATTERN.finditer(content):
        refs.append(ImageRef(raw_path=match.group(1).strip(), full_match=match.group(0), start=match.start(1), end=match.end(1), kind='html'))
    refs.sort(key=lambda item: item.start)
    return refs



def should_skip_path(raw_path: str) -> bool:
    lower = raw_path.lower()
    return lower.startswith(SKIP_PREFIXES)



def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            digest.update(chunk)
    return digest.hexdigest()



def relative_posix(path: Path, base: Path) -> str:
    import os
    return Path(os.path.relpath(path, base)).as_posix()



def build_target_path(repo_root: Path, article_path: Path, source_file: Path, shared: bool, file_hash: str) -> Path:
    docs_dir = repo_root / 'docs'
    if shared:
        safe_name = f'{file_hash[:8]}-{source_file.name}'
        return docs_dir / 'assets' / 'shared' / safe_name

    article_rel = article_path.relative_to(docs_dir)
    category = article_rel.parts[0]
    slug = slugify_post_name(article_path.stem)
    return docs_dir / category / 'image' / slug / source_file.name



def first_pass_usage(repo_root: Path) -> tuple[dict[str, list[tuple[Path, ImageRef]]], Context]:
    ctx = Context(mode='scan')
    usage: dict[str, list[tuple[Path, ImageRef]]] = {}
    docs_dir = repo_root / 'docs'

    for article_path in sorted(docs_dir.rglob('*.md')):
        if is_draft_markdown(article_path):
            ctx.skipped_draft_articles.append(relative_posix(article_path, repo_root))
            continue

        ctx.scanned_articles += 1
        try:
            content = article_path.read_text(encoding='utf-8')
        except Exception as exc:
            ctx.updated_articles_failed += 1
            ctx.failures.append(Failure(relative_posix(article_path, repo_root), '', f'读取文章失败: {exc}'))
            continue

        refs = parse_image_refs(content)
        for ref in refs:
            if should_skip_path(ref.raw_path):
                continue
            ctx.total_image_refs += 1
            usage.setdefault(ref.raw_path, []).append((article_path, ref))

    return usage, ctx



def normalize_images(repo_root: Path, fix: bool) -> Context:
    usage, ctx = first_pass_usage(repo_root)
    path_counts = {key: len(value) for key, value in usage.items()}

    docs_dir = repo_root / 'docs'
    hash_target_cache: dict[str, Path] = {}

    article_replacements: dict[Path, list[tuple[str, str]]] = {}

    for raw_path, refs in usage.items():
        shared = path_counts[raw_path] > 1
        if shared:
            ctx.shared_images_detected += 1

        for article_path, ref in refs:
            source_path = (article_path.parent / raw_path).resolve()
            article_key = relative_posix(article_path, repo_root)

            if not source_path.exists() or not source_path.is_file():
                ctx.invalid_path_refs += 1
                ctx.moved_images_failed += 1
                ctx.failures.append(Failure(article_key, raw_path, '图片文件不存在'))
                continue

            file_hash = sha256_file(source_path)
            target_path = hash_target_cache.get(file_hash)
            if target_path is None:
                target_path = build_target_path(repo_root, article_path, source_path, shared, file_hash)
                hash_target_cache[file_hash] = target_path

            expected_rel = relative_posix(target_path, article_path.parent)
            expected_rel = expected_rel.replace('\\', '/')
            is_already_normalized = raw_path == expected_rel
            if is_already_normalized:
                continue

            ctx.invalid_path_refs += 1

            if fix:
                try:
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    if source_path.resolve() != target_path.resolve():
                        if target_path.exists():
                            target_hash = sha256_file(target_path)
                            if target_hash != file_hash:
                                target_path = build_target_path(repo_root, article_path, source_path, shared, file_hash)
                                target_path.parent.mkdir(parents=True, exist_ok=True)
                                if not target_path.exists():
                                    shutil.copy2(source_path, target_path)
                            # 若存在且相同则复用
                        else:
                            shutil.move(str(source_path), str(target_path))
                            ctx.moved_images_success += 1
                    article_replacements.setdefault(article_path, []).append((raw_path, expected_rel))
                except Exception as exc:
                    ctx.moved_images_failed += 1
                    ctx.failures.append(Failure(article_key, raw_path, f'移动或准备目标失败: {exc}'))
            else:
                article_replacements.setdefault(article_path, []).append((raw_path, expected_rel))

    for article_path, replacements in article_replacements.items():
        article_key = relative_posix(article_path, repo_root)
        try:
            content = article_path.read_text(encoding='utf-8')
            for old, new in replacements:
                content = content.replace(f'({old})', f'({new})')
                content = content.replace(f'src="{old}"', f'src="{new}"')
                content = content.replace(f"src='{old}'", f"src='{new}'")
            if fix:
                article_path.write_text(content, encoding='utf-8')
            ctx.updated_articles_success += 1
        except Exception as exc:
            ctx.updated_articles_failed += 1
            ctx.failures.append(Failure(article_key, '', f'回写文章失败: {exc}'))

    return ctx



def build_summary(ctx: Context) -> str:
    lines = [
        '# 图片路径检查报告',
        '',
        f'- 模式：{ctx.mode}',
        f'- 扫描文章数：{ctx.scanned_articles}',
        f'- 跳过 Draft 文章数：{len(ctx.skipped_draft_articles)}',
        f'- 图片引用数：{ctx.total_image_refs}',
        f'- 不规范引用数：{ctx.invalid_path_refs}',
        f'- 图片移动成功数：{ctx.moved_images_success}',
        f'- 图片移动失败数：{ctx.moved_images_failed}',
        f'- 文章更新成功数：{ctx.updated_articles_success}',
        f'- 文章更新失败数：{ctx.updated_articles_failed}',
        f'- 共享图片检测数：{ctx.shared_images_detected}',
        '',
    ]

    if ctx.skipped_draft_articles:
        lines.extend(['## 跳过的 Draft 文章', ''])
        for item in ctx.skipped_draft_articles:
            lines.append(f'- `{item}`')
        lines.append('')

    if ctx.failures:
        lines.extend(['## 失败明细', ''])
        for failure in ctx.failures:
            lines.append(f'- 文章 `{failure.article}` / 图片 `{failure.image}` / 原因：{failure.reason}')
        lines.append('')
    else:
        lines.extend(['## 失败明细', '', '- 无', ''])

    return '\n'.join(lines)



def write_outputs(ctx: Context, report_json: Path | None, summary_md: Path | None) -> None:
    if report_json:
        report_json.parent.mkdir(parents=True, exist_ok=True)
        report_json.write_text(json.dumps({
            'mode': ctx.mode,
            'scanned_articles': ctx.scanned_articles,
            'skipped_draft_articles': ctx.skipped_draft_articles,
            'total_image_refs': ctx.total_image_refs,
            'invalid_path_refs': ctx.invalid_path_refs,
            'moved_images_success': ctx.moved_images_success,
            'moved_images_failed': ctx.moved_images_failed,
            'updated_articles_success': ctx.updated_articles_success,
            'updated_articles_failed': ctx.updated_articles_failed,
            'shared_images_detected': ctx.shared_images_detected,
            'failures': [failure.to_dict() for failure in ctx.failures],
        }, ensure_ascii=False, indent=2), encoding='utf-8')

    if summary_md:
        summary_md.parent.mkdir(parents=True, exist_ok=True)
        summary_md.write_text(build_summary(ctx), encoding='utf-8')



def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--fix', action='store_true')
    parser.add_argument('--report-json', type=Path)
    parser.add_argument('--summary-md', type=Path)
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    ctx = normalize_images(repo_root, fix=args.fix)
    ctx.mode = 'fix' if args.fix else 'check'
    write_outputs(ctx, args.report_json, args.summary_md)

    print(build_summary(ctx))

    if args.check and ctx.invalid_path_refs > 0:
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
