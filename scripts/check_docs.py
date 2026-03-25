#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查 docs/ 下 Markdown 文档的基础可读性与 front matter 格式，并输出可汇总报告。

能力：
1. 检查 UTF-8 读取是否成功
2. 检查 YAML front matter 是否闭合
3. 检查 YAML front matter 是否可解析，并输出文件/行/列
4. 检查 mkdocs.yml nav 中引用的文档是否存在
5. 支持 draft: true 文档跳过检查
6. 支持输出 JSON 报告和 Markdown Summary

用法：
  python scripts/check_docs.py
  python scripts/check_docs.py --strict
  python scripts/check_docs.py --strict --report-json artifacts/check-report.json --summary-md artifacts/check-summary.md
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass
class CheckIssue:
    level: str
    file: str
    message: str
    line: int | None = None
    col: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            'level': self.level,
            'file': self.file,
            'message': self.message,
            'line': self.line,
            'col': self.col,
        }


class CheckContext:
    def __init__(self) -> None:
        self.issues: list[CheckIssue] = []
        self.checked_files = 0
        self.skipped_draft_files: list[str] = []
        self.nav_checked = False

    @property
    def error_count(self) -> int:
        return sum(1 for issue in self.issues if issue.level == 'error')

    @property
    def warning_count(self) -> int:
        return sum(1 for issue in self.issues if issue.level == 'warning')

    @property
    def error_files(self) -> list[str]:
        return sorted({issue.file for issue in self.issues if issue.level == 'error'})


ctx = CheckContext()


def gha_escape(message: str) -> str:
    return (
        message.replace('%', '%25')
        .replace('\r', '%0D')
        .replace('\n', '%0A')
        .replace(':', '%3A')
        .replace(',', '%2C')
    )


def record_issue(level: str, file: str, message: str, line: int | None = None, col: int | None = None) -> None:
    issue = CheckIssue(level=level, file=file, message=message, line=line, col=col)
    ctx.issues.append(issue)

    location = f'file={file}'
    if line is not None:
        location += f',line={line}'
    if col is not None:
        location += f',col={col}'

    if level == 'error':
        print(f'::error {location}::{gha_escape(message)}')
    else:
        print(f'::warning {location}::{gha_escape(message)}')



def gha_error(file: str, message: str, line: int | None = None, col: int | None = None) -> None:
    record_issue('error', file, message, line, col)



def gha_warning(file: str, message: str, line: int | None = None, col: int | None = None) -> None:
    record_issue('warning', file, message, line, col)



def normalize_path(path: Path) -> str:
    return str(path).replace('\\', '/')



def load_text(path: Path) -> str | None:
    normalized = normalize_path(path)
    try:
        return path.read_text(encoding='utf-8')
    except UnicodeDecodeError as e:
        gha_error(normalized, f'文件不是有效 UTF-8 编码: {e}', getattr(e, 'start', None), None)
        return None
    except Exception as e:
        gha_error(normalized, f'读取文件失败: {e}')
        return None



def extract_front_matter(text: str) -> tuple[str | None, int | None]:
    if not text.startswith('---'):
        return None, None

    lines = text.splitlines()
    if not lines or lines[0].strip() != '---':
        return None, None

    for idx in range(1, len(lines)):
        if lines[idx].strip() == '---':
            return '\n'.join(lines[1:idx]), idx + 1

    return '', 1



def parse_front_matter(path: Path, text: str) -> tuple[dict[str, Any] | None, int]:
    normalized = normalize_path(path)
    fm_text, end_line = extract_front_matter(text)

    if fm_text is None:
        return None, 0

    if end_line == 1 and fm_text == '':
        gha_error(normalized, 'front matter 已开始但没有结束分隔符 ---', 1, 1)
        return None, 1

    try:
        data = yaml.safe_load(fm_text) if fm_text.strip() else {}
        if data is not None and not isinstance(data, dict):
            gha_error(normalized, 'front matter 顶层必须是键值对象', 2, 1)
            return None, 1
        return data or {}, 0
    except yaml.MarkedYAMLError as e:
        line = None
        col = None
        if getattr(e, 'problem_mark', None) is not None:
            line = e.problem_mark.line + 2
            col = e.problem_mark.column + 1
        message = getattr(e, 'problem', None) or str(e)
        gha_error(normalized, f'front matter YAML 解析失败: {message}', line, col)
        return None, 1
    except Exception as e:
        gha_error(normalized, f'front matter 解析失败: {e}', 2, 1)
        return None, 1



def is_draft_front_matter(data: dict[str, Any] | None) -> bool:
    if not data:
        return False
    return data.get('draft') is True



def collect_nav_files(node: Any, result: set[str]) -> None:
    if isinstance(node, list):
        for item in node:
            collect_nav_files(item, result)
        return

    if isinstance(node, dict):
        for _, value in node.items():
            collect_nav_files(value, result)
        return

    if isinstance(node, str) and node.endswith('.md'):
        result.add(node)


class _IgnoreUnknownTags(yaml.SafeLoader):
    """SafeLoader 扩展：遇到 !!python/name: 等自定义标签时忽略而非报错。"""



def _ignore_tag_constructor(loader, tag_suffix, node):
    return loader.construct_scalar(node)


_IgnoreUnknownTags.add_multi_constructor('', _ignore_tag_constructor)



def validate_mkdocs_nav(mkdocs_path: Path, docs_dir: Path) -> int:
    errors = 0
    ctx.nav_checked = True
    try:
        config = yaml.load(mkdocs_path.read_text(encoding='utf-8'), Loader=_IgnoreUnknownTags) or {}
    except Exception as e:
        gha_error(normalize_path(mkdocs_path), f'mkdocs.yml 解析失败: {e}')
        return 1

    nav_files: set[str] = set()
    collect_nav_files(config.get('nav', []), nav_files)

    for rel in sorted(nav_files):
        target = docs_dir / rel
        if not target.exists():
            gha_error(normalize_path(mkdocs_path), f'nav 引用了不存在的文档: {rel}')
            errors += 1

    return errors



def write_report_json(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    report = {
        'checked_files': ctx.checked_files,
        'error_count': ctx.error_count,
        'warning_count': ctx.warning_count,
        'error_files': ctx.error_files,
        'skipped_draft_files': ctx.skipped_draft_files,
        'nav_checked': ctx.nav_checked,
        'issues': [issue.to_dict() for issue in ctx.issues],
    }
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')



def build_summary_markdown() -> str:
    lines = [
        '# 文档检查报告',
        '',
        f'- 已检查文件数：{ctx.checked_files}',
        f'- Draft 跳过文件数：{len(ctx.skipped_draft_files)}',
        f'- 错误数：{ctx.error_count}',
        f'- 警告数：{ctx.warning_count}',
        '',
    ]

    if ctx.error_files:
        lines.extend([
            '## 格式有问题的文章',
            '',
        ])
        for file in ctx.error_files:
            lines.append(f'- `{file}`')
        lines.append('')
    else:
        lines.extend([
            '## 格式有问题的文章',
            '',
            '- 无',
            '',
        ])

    if ctx.skipped_draft_files:
        lines.extend([
            '## 跳过的 Draft 文章',
            '',
        ])
        for file in ctx.skipped_draft_files:
            lines.append(f'- `{file}`')
        lines.append('')

    if ctx.issues:
        lines.extend([
            '## 详细问题',
            '',
        ])
        for issue in ctx.issues:
            location = issue.file
            if issue.line is not None:
                location += f':{issue.line}'
            if issue.col is not None:
                location += f':{issue.col}'
            lines.append(f'- **{issue.level.upper()}** `{location}` - {issue.message}')
        lines.append('')

    return '\n'.join(lines)



def write_summary_markdown(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(build_summary_markdown(), encoding='utf-8')



def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--strict', action='store_true', help='发现错误时返回非 0 退出码')
    parser.add_argument('--report-json', type=Path, help='输出 JSON 报告路径')
    parser.add_argument('--summary-md', type=Path, help='输出 Markdown 汇总路径')
    parser.add_argument('--skip-draft', action='store_true', default=True, help='跳过 front matter 中 draft: true 的文档')
    parser.add_argument('--include-draft', action='store_true', help='包含 draft 文档并进行检查')
    args = parser.parse_args()

    skip_draft = args.skip_draft and not args.include_draft

    repo_root = Path(__file__).resolve().parent.parent
    docs_dir = repo_root / 'docs'
    mkdocs_path = repo_root / 'mkdocs.yml'

    total_errors = 0

    if mkdocs_path.exists():
        total_errors += validate_mkdocs_nav(mkdocs_path, docs_dir)

    for md_file in sorted(docs_dir.rglob('*.md')):
        text = load_text(md_file)
        if text is None:
            total_errors += 1
            continue

        fm_data, fm_errors = parse_front_matter(md_file, text)
        total_errors += fm_errors
        if fm_errors > 0:
            continue

        if skip_draft and is_draft_front_matter(fm_data):
            ctx.skipped_draft_files.append(normalize_path(md_file))
            continue

        ctx.checked_files += 1

    print(
        f'checked {ctx.checked_files} markdown files, '
        f'skipped {len(ctx.skipped_draft_files)} draft file(s), '
        f'found {ctx.error_count} error(s) and {ctx.warning_count} warning(s)'
    )

    if args.report_json:
        write_report_json(args.report_json)
    if args.summary_md:
        write_summary_markdown(args.summary_md)

    if args.strict and total_errors > 0:
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
