#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动生成 README.md 和/或 docs/all-articles.md

用法：
  python scripts/generate_readme.py                 # 同时生成两者
  python scripts/generate_readme.py --target readme
  python scripts/generate_readme.py --target all-articles
  python scripts/generate_readme.py --target both
"""

import argparse
import os
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

import yaml


def extract_front_matter(text):
    """提取 front matter 文本，未包含分隔符 ---。无 front matter 返回 None。"""
    if not text.startswith('---'):
        return None

    lines = text.splitlines()
    if not lines or lines[0].strip() != '---':
        return None

    for idx in range(1, len(lines)):
        if lines[idx].strip() == '---':
            return '\n'.join(lines[1:idx])

    return ''


def parse_front_matter(filepath, content):
    """解析 front matter，成功返回 dict；失败抛异常。无 front matter 返回 None。"""
    front_matter = extract_front_matter(content)
    if front_matter is None:
        return None

    if front_matter == '':
        raise ValueError('front matter 已开始但没有结束分隔符 ---')

    try:
        data = yaml.safe_load(front_matter) if front_matter.strip() else {}
    except yaml.MarkedYAMLError as e:
        line = getattr(getattr(e, 'problem_mark', None), 'line', None)
        col = getattr(getattr(e, 'problem_mark', None), 'column', None)
        line_info = ''
        if line is not None and col is not None:
            line_info = f' (line {line + 2}, col {col + 1})'
        message = getattr(e, 'problem', None) or str(e)
        raise ValueError(f'front matter YAML 解析失败{line_info}: {message}') from e

    if data is not None and not isinstance(data, dict):
        raise ValueError('front matter 顶层必须是键值对象')

    return data or {}


def get_article_info(filepath):
    """从 Markdown 文件提取 title 和 date。

    返回：
      - 成功： (title, date)
      - front matter 异常需跳过： None
    """
    title = None
    date = None

    try:
        content = Path(filepath).read_text(encoding='utf-8')
    except Exception as e:
        print(f"warning: cannot read {filepath}: {e}")
        return None

    try:
        front_matter = parse_front_matter(filepath, content)
    except ValueError as e:
        print(f"warning: skip {filepath}: {e}")
        return None

    if front_matter is not None:
        raw_title = front_matter.get('title')
        raw_date = front_matter.get('date')
        if raw_title is not None:
            title = str(raw_title).strip()
        if raw_date is not None:
            date = str(raw_date).strip()

    if not title:
        title_match = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', content)
        if title_match:
            title = title_match.group(1).strip()

    if not date:
        date_match = re.search(r'date:\s*["\']?([^"\'\n]+)["\']?', content)
        if date_match:
            date = date_match.group(1).strip()

    if not title:
        title = Path(filepath).stem
    if not date:
        timestamp = os.path.getmtime(filepath)
        date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

    return title, date


def scan_docs():
    """扫描 docs 目录，按分类组织文章"""
    docs_dir = Path('docs').resolve()
    repo_root = docs_dir.parent
    articles = defaultdict(list)
    skipped_files = []

    category_names = {
        'u3d': 'Unity 开发',
        'shader': 'Shader 与图形学',
        'csharp': 'C# 语言与工程',
        'Android': 'Android 开发',
        'IOS': 'iOS 开发',
        'math': '数学与图形学基础',
        'datastruct': '数据结构与算法',
        'basesystem': '系统基础',
        'unity编辑器': 'Unity 编辑器扩展',
        'unityTool': 'Unity 工具',
        'lua': 'Lua 语言',
        'Graphics': '图形学',
        'datastructbase': '数据结构基础',
        'other': '工具与系统',
        'ANote': '项目记录与随笔',
    }

    if not docs_dir.exists():
        print(f"error: {docs_dir} does not exist")
        return articles, skipped_files

    for category_dir in sorted(docs_dir.iterdir()):
        if not category_dir.is_dir() or category_dir.name.startswith('.'):
            continue
        category_name = category_names.get(category_dir.name, category_dir.name)
        for md_file in sorted(category_dir.glob('*.md')):
            if md_file.name == 'index.md':
                continue
            article_info = get_article_info(md_file)
            if article_info is None:
                skipped_files.append(str(md_file.relative_to(repo_root)).replace('\\', '/'))
                continue
            title, date = article_info
            readme_path = str(md_file.relative_to(repo_root)).replace('\\', '/')
            docs_path = str(md_file.relative_to(docs_dir)).replace('\\', '/')
            articles[category_name].append((title, date, readme_path, docs_path))

    return articles, skipped_files


def generate_readme_section(articles):
    """生成 README 的文章索引部分（含日期，按日期倒序）"""
    lines = ['## \U0001f4da 完整文章索引\n']

    for category in sorted(articles.keys()):
        items = articles[category]
        lines.append('\n### ' + category + '\n')
        sorted_items = sorted(items, key=lambda x: x[1], reverse=True)
        for title, date, readme_path, docs_path in sorted_items:
            lines.append('- **' + date + '** - [' + title + '](' + readme_path + ')')

    lines.append('\n### 项目记录与随笔\n')
    lines.append('详见 [ANote 栏目](docs/ANote/index.md)\n')

    return '\n'.join(lines)


def generate_all_articles_page(articles):
    """生成 docs/all-articles.md 页面（含日期，按日期倒序）"""
    lines = [
        '---',
        'title: "全部文章"',
        'date: "2026-03-23"',
        'comments: false',
        '---',
        '',
        '# 全部文章',
        '',
        '这里列出博客中的全部文章，按分类组织，包含创建日期。',
        '',
    ]

    for category in sorted(articles.keys()):
        items = articles[category]
        lines.append('## ' + category + '\n')
        sorted_items = sorted(items, key=lambda x: x[1], reverse=True)
        for title, date, readme_path, docs_path in sorted_items:
            lines.append('- **' + date + '** - [' + title + '](' + docs_path + ')')
        lines.append('')

    return '\n'.join(lines)


def update_readme(new_section):
    """更新 README.md，替换文章索引部分"""
    readme_path = Path('README.md')

    if not readme_path.exists():
        print(f"error: {readme_path} does not exist")
        return False

    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    start_marker = '## \U0001f4da 完整文章索引'
    end_marker = '## \U0001f3d7\ufe0f 仓库定位'

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print('error: cannot find article index section in README.md')
        return False

    new_content = content[:start_idx] + new_section + '\n\n' + content[end_idx:]

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print('README.md updated')
    return True


def create_all_articles_page(content):
    """创建或更新 docs/all-articles.md"""
    all_articles_path = Path('docs/all-articles.md')
    with open(all_articles_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('docs/all-articles.md updated')
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--target',
        choices=['readme', 'all-articles', 'both'],
        default='both',
        help='选择要生成的目标文件',
    )
    args = parser.parse_args()

    print('scanning docs/...')
    articles, skipped_files = scan_docs()

    if not articles:
        print('warning: no articles found')
    else:
        total = sum(len(items) for items in articles.values())
        print(f'found {total} articles in {len(articles)} categories')

    if skipped_files:
        print(f'warning: skipped {len(skipped_files)} file(s) due to invalid front matter')
        for path in skipped_files:
            print(f'warning: skipped file: {path}')

    if args.target in ('readme', 'both'):
        print('generating README section...')
        readme_section = generate_readme_section(articles)
        print('updating README.md...')
        if not update_readme(readme_section):
            print('error: failed to update README.md')
            raise SystemExit(1)

    if args.target in ('all-articles', 'both'):
        print('generating all-articles page...')
        all_articles_content = generate_all_articles_page(articles)
        print('writing docs/all-articles.md...')
        if not create_all_articles_page(all_articles_content):
            print('error: failed to write docs/all-articles.md')
            raise SystemExit(1)

    print('done')


if __name__ == '__main__':
    main()
