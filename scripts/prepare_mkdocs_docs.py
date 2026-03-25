#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
构建前预处理 docs/ 目录：跳过 draft: true 的文章，并同步更新 mkdocs 配置中的 docs_dir。

用法：
  python scripts/prepare_mkdocs_docs.py --source docs --output build_docs --mkdocs mkdocs.yml
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import yaml


class _IgnoreUnknownTags(yaml.SafeLoader):
    pass



def _ignore_tag_constructor(loader, tag_suffix, node):
    return loader.construct_scalar(node)


_IgnoreUnknownTags.add_multi_constructor('', _ignore_tag_constructor)



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



def is_draft_file(path: Path) -> bool:
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



def copy_docs_tree(source: Path, output: Path) -> tuple[int, list[str]]:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)

    skipped: list[str] = []
    copied = 0

    for item in source.rglob('*'):
        relative = item.relative_to(source)
        target = output / relative

        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue

        if item.suffix.lower() == '.md' and is_draft_file(item):
            skipped.append(str(relative).replace('\\', '/'))
            continue

        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target)
        copied += 1

    return copied, skipped



def update_mkdocs_docs_dir(mkdocs_path: Path, output_docs_dir: str) -> None:
    content = mkdocs_path.read_text(encoding='utf-8')
    lines = content.splitlines()
    replaced = False
    new_lines: list[str] = []

    for line in lines:
        if line.startswith('docs_dir:'):
            new_lines.append(f'docs_dir: {output_docs_dir}')
            replaced = True
        else:
            new_lines.append(line)

    if not replaced:
        insert_at = 0
        for idx, line in enumerate(new_lines):
            if line.startswith('site_url:'):
                insert_at = idx + 1
                break
        new_lines.insert(insert_at, f'docs_dir: {output_docs_dir}')

    mkdocs_path.write_text('\n'.join(new_lines) + '\n', encoding='utf-8')



def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=Path('docs'))
    parser.add_argument('--output', type=Path, default=Path('build_docs'))
    parser.add_argument('--mkdocs', type=Path, default=Path('mkdocs.yml'))
    args = parser.parse_args()

    copied, skipped = copy_docs_tree(args.source, args.output)
    update_mkdocs_docs_dir(args.mkdocs, args.output.as_posix())

    print(f'copied {copied} file(s) into {args.output.as_posix()}')
    print(f'skipped {len(skipped)} draft markdown file(s)')
    for rel in skipped:
        print(f'skipped draft: {rel}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
