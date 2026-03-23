#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查 docs/ 下 Markdown 文档的基础可读性与 front matter 格式。

能力：
1. 检查 UTF-8 读取是否成功
2. 检查 YAML front matter 是否闭合
3. 检查 YAML front matter 是否可解析，并输出文件/行/列
4. 检查 mkdocs.yml nav 中引用的文档是否存在

用法：
  python scripts/check_docs.py            # 只输出错误/警告，退出码 0
  python scripts/check_docs.py --strict   # 有错误时退出码 1
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


def gha_escape(message: str) -> str:
    return (
        message.replace('%', '%25')
        .replace('\r', '%0D')
        .replace('\n', '%0A')
        .replace(':', '%3A')
        .replace(',', '%2C')
    )


def gha_error(file: str, message: str, line: int | None = None, col: int | None = None) -> None:
    location = f"file={file}"
    if line is not None:
        location += f",line={line}"
    if col is not None:
        location += f",col={col}"
    print(f"::error {location}::{gha_escape(message)}")


def gha_warning(file: str, message: str, line: int | None = None, col: int | None = None) -> None:
    location = f"file={file}"
    if line is not None:
        location += f",line={line}"
    if col is not None:
        location += f",col={col}"
    print(f"::warning {location}::{gha_escape(message)}")


def load_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding='utf-8')
    except UnicodeDecodeError as e:
        gha_error(str(path).replace('\\', '/'), f'文件不是有效 UTF-8 编码: {e}', getattr(e, 'start', None), None)
        return None
    except Exception as e:
        gha_error(str(path).replace('\\', '/'), f'读取文件失败: {e}')
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


def validate_front_matter(path: Path, text: str) -> int:
    errors = 0
    fm_text, end_line = extract_front_matter(text)
    normalized = str(path).replace('\\', '/')

    if fm_text is None:
        return errors

    if end_line == 1 and fm_text == '':
        gha_error(normalized, 'front matter 已开始但没有结束分隔符 ---', 1, 1)
        return 1

    try:
        data = yaml.safe_load(fm_text) if fm_text.strip() else {}
        if data is not None and not isinstance(data, dict):
            gha_error(normalized, 'front matter 顶层必须是键值对象', 2, 1)
            errors += 1
    except yaml.MarkedYAMLError as e:
        line = None
        col = None
        if getattr(e, 'problem_mark', None) is not None:
            line = e.problem_mark.line + 2
            col = e.problem_mark.column + 1
        message = getattr(e, 'problem', None) or str(e)
        gha_error(normalized, f'front matter YAML 解析失败: {message}', line, col)
        errors += 1
    except Exception as e:
        gha_error(normalized, f'front matter 解析失败: {e}', 2, 1)
        errors += 1

    return errors


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


def validate_mkdocs_nav(mkdocs_path: Path, docs_dir: Path) -> int:
    errors = 0
    try:
        config = yaml.safe_load(mkdocs_path.read_text(encoding='utf-8')) or {}
    except Exception as e:
        gha_error(str(mkdocs_path).replace('\\', '/'), f'mkdocs.yml 解析失败: {e}')
        return 1

    nav_files: set[str] = set()
    collect_nav_files(config.get('nav', []), nav_files)

    for rel in sorted(nav_files):
        target = docs_dir / rel
        if not target.exists():
            gha_error(str(mkdocs_path).replace('\\', '/'), f'nav 引用了不存在的文档: {rel}')
            errors += 1

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--strict', action='store_true', help='发现错误时返回非 0 退出码')
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    docs_dir = repo_root / 'docs'
    mkdocs_path = repo_root / 'mkdocs.yml'

    total_errors = 0
    total_files = 0

    if mkdocs_path.exists():
        total_errors += validate_mkdocs_nav(mkdocs_path, docs_dir)

    for md_file in sorted(docs_dir.rglob('*.md')):
        total_files += 1
        text = load_text(md_file)
        if text is None:
            total_errors += 1
            continue
        total_errors += validate_front_matter(md_file, text)

    print(f'checked {total_files} markdown files, found {total_errors} error(s)')

    if args.strict and total_errors > 0:
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
