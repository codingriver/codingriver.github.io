#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动生成 README.md、docs/all-articles.md、docs/all-categories.md、mkdocs.yml nav

用法：
  python scripts/generate_readme.py                    # 同时生成 readme + all-articles
  python scripts/generate_readme.py --target readme
  python scripts/generate_readme.py --target all-articles
  python scripts/generate_readme.py --target all-categories
  python scripts/generate_readme.py --target mkdocs-nav
  python scripts/generate_readme.py --target both      # readme + all-articles
  python scripts/generate_readme.py --target all       # readme + all-articles + all-categories + mkdocs-nav
"""

import argparse
import os
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

import yaml

# ──────────────────────────────────────────────
# 固定 nav 头部：这些入口不由脚本扫描生成，保持不变
# ──────────────────────────────────────────────
FIXED_NAV_HEADER = [
    {'首页': 'index.md'},
    {'关于': 'about.md'},
    {'全部栏目': 'all-articles.md'},
    {'全部分类': 'all-categories.md'},
    {'MkDocs 博客方案': 'MkDocs博客方案.md'},
    {'标签': 'tags/index.md'},
]

# 栏目目录名 -> 栏目显示名（决定 nav 中分组标题）
CATEGORY_NAMES = {
    'u3d': 'Unity 开发',
    'shader': 'Shader 与图形学',
    'csharp': 'C# 语言与工程',
    'Android': 'Android 开发',
    'IOS': 'iOS 开发',
    'math': '数学与图形学基础',
    'datastruct': '数据结构与算法',
    'basesystem': '系统基础',
    'unity-editor': 'Unity 编辑器扩展',
    'unityTool': 'Unity 工具',
    'lua': 'Lua 语言',
    'Graphics': '图形学',
    'datastructbase': '数据结构基础',
    'other': '工具与系统',
    'ANote': '项目记录与随笔',
}


# ──────────────────────────────────────────────
# front matter 解析
# ──────────────────────────────────────────────

def extract_front_matter(text):
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
        line_info = f' (line {line + 2}, col {col + 1})' if line is not None and col is not None else ''
        message = getattr(e, 'problem', None) or str(e)
        raise ValueError(f'front matter YAML 解析失败{line_info}: {message}') from e
    if data is not None and not isinstance(data, dict):
        raise ValueError('front matter 顶层必须是键值对象')
    return data or {}


# ──────────────────────────────────────────────
# 文章信息提取
# ──────────────────────────────────────────────

def get_article_info(filepath):
    """返回文章信息 dict 或 None（需跳过）"""
    try:
        content = Path(filepath).read_text(encoding='utf-8')
    except Exception as e:
        print(f'warning: cannot read {filepath}: {e}')
        return None

    try:
        fm = parse_front_matter(filepath, content)
    except ValueError as e:
        print(f'warning: skip {filepath}: {e}')
        return None

    title = None
    date = None
    categories = []

    if fm is not None:
        raw_title = fm.get('title')
        raw_date = fm.get('date')
        raw_categories = fm.get('categories')

        if raw_title is not None:
            title = str(raw_title).strip()
        if raw_date is not None:
            date = str(raw_date).strip()

        if isinstance(raw_categories, list):
            categories = [str(x).strip() for x in raw_categories if str(x).strip()]
        elif raw_categories is not None:
            c = str(raw_categories).strip()
            if c:
                categories = [c]

    if not title:
        m = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', content)
        if m:
            title = m.group(1).strip()
    if not date:
        m = re.search(r'date:\s*["\']?([^"\'\n]+)["\']?', content)
        if m:
            date = m.group(1).strip()
    if not title:
        title = Path(filepath).stem
    if not date:
        date = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d')

    return {
        'title': title,
        'date': date,
        'categories': categories,
    }


# ──────────────────────────────────────────────
# 扫描 docs/
# ──────────────────────────────────────────────

def scan_docs():
    """返回 (articles, category_articles, skipped_files, dir_order)"""
    docs_dir = Path('docs').resolve()
    repo_root = docs_dir.parent
    articles = defaultdict(list)
    category_articles = defaultdict(list)
    skipped_files = []
    dir_order = []   # 保留扫描到的目录名顺序

    if not docs_dir.exists():
        print(f'error: {docs_dir} does not exist')
        return articles, category_articles, skipped_files, dir_order

    for category_dir in sorted(docs_dir.iterdir()):
        if not category_dir.is_dir() or category_dir.name.startswith('.'):
            continue
        dir_name = category_dir.name
        category_name = CATEGORY_NAMES.get(dir_name, dir_name)
        has_article = False
        for md_file in sorted(category_dir.glob('*.md')):
            if md_file.name == 'index.md':
                continue
            info = get_article_info(md_file)
            if info is None:
                skipped_files.append(str(md_file.relative_to(repo_root)).replace('\\', '/'))
                continue

            title = info['title']
            date = info['date']
            fm_categories = info['categories']

            readme_path = str(md_file.relative_to(repo_root)).replace('\\', '/')
            docs_path = str(md_file.relative_to(docs_dir)).replace('\\', '/')

            entry = (title, date, readme_path, docs_path, dir_name)
            articles[category_name].append(entry)
            has_article = True

            article_categories = fm_categories if fm_categories else ['未分类']
            for c in article_categories:
                category_articles[c].append(entry)

        if has_article or (category_dir / 'index.md').exists():
            dir_order.append(dir_name)

    return articles, category_articles, skipped_files, dir_order


# ──────────────────────────────────────────────
# README
# ──────────────────────────────────────────────

def generate_readme_section(articles):
    lines = ['## \U0001f4da 完整文章索引\n']
    for category in sorted(articles.keys()):
        items = articles[category]
        lines.append('\n### ' + category + '\n')
        sorted_items = sorted(items, key=lambda x: x[1], reverse=True)
        for title, date, readme_path, docs_path, dir_name in sorted_items:
            lines.append('- **' + date + '** - [' + title + '](' + readme_path + ')')
    lines.append('\n### 项目记录与随笔\n')
    lines.append('详见 [ANote 栏目](docs/ANote/index.md)\n')
    return '\n'.join(lines)


def update_readme(new_section):
    readme_path = Path('README.md')
    if not readme_path.exists():
        print(f'error: {readme_path} does not exist')
        return False
    content = readme_path.read_text(encoding='utf-8')
    start_marker = '## \U0001f4da 完整文章索引'
    end_marker = '## \U0001f3d7\ufe0f 仓库定位'
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    if start_idx == -1:
        print('error: cannot find article index section in README.md')
        return False

    if end_idx == -1 or end_idx < start_idx:
        # 如果 README 里没有后续“仓库定位”分节，则替换到文件末尾
        readme_path.write_text(content[:start_idx] + new_section + '\n', encoding='utf-8')
    else:
        readme_path.write_text(content[:start_idx] + new_section + '\n\n' + content[end_idx:], encoding='utf-8')

    print('README.md updated')
    return True


# ──────────────────────────────────────────────
# all-articles.md
# ──────────────────────────────────────────────

def generate_all_articles_page(articles):
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
        for title, date, readme_path, docs_path, dir_name in sorted_items:
            lines.append('- **' + date + '** - [' + title + '](' + docs_path + ')')
        lines.append('')
    return '\n'.join(lines)


def create_all_articles_page(content):
    Path('docs/all-articles.md').write_text(content, encoding='utf-8')
    print('docs/all-articles.md updated')
    return True


def generate_all_categories_page(category_articles):
    lines = [
        '---',
        'title: "全部分类"',
        'date: "2026-03-25"',
        'comments: false',
        '---',
        '',
        '# 全部分类',
        '',
        '这里列出博客中的全部文章，按文章 front matter 中定义的 `categories` 分组。',
        '',
    ]

    for category in sorted(category_articles.keys()):
        items = category_articles[category]
        sorted_items = sorted(items, key=lambda x: x[1], reverse=True)
        lines.append(f'## {category}（{len(sorted_items)}）\n')
        for title, date, readme_path, docs_path, dir_name in sorted_items:
            lines.append('- **' + date + '** - [' + title + '](' + docs_path + ')')
        lines.append('')

    return '\n'.join(lines)


def create_all_categories_page(content):
    Path('docs/all-categories.md').write_text(content, encoding='utf-8')
    print('docs/all-categories.md updated')
    return True


# ──────────────────────────────────────────────
# mkdocs.yml nav
# ──────────────────────────────────────────────

def generate_mkdocs_nav(articles, dir_order):
    """生成完整 nav 列表（Python 对象，供 yaml.dump 使用）"""
    nav = list(FIXED_NAV_HEADER)

    for dir_name in dir_order:
        category_name = CATEGORY_NAMES.get(dir_name, dir_name)
        items = articles.get(category_name, [])
        # 栏目首页永远排第一
        category_nav = [{'栏目首页': f'{dir_name}/index.md'}]
        # 文章按文件名排序（和扫描一致），标题作为 nav key
        for title, date, readme_path, docs_path, _ in items:
            category_nav.append({title: docs_path})
        nav.append({category_name: category_nav})

    return nav


def update_mkdocs_nav(nav):
    """把 nav 写回 mkdocs.yml，保留 nav 以外的所有配置。

    策略：用正则定位 nav: 块的起止位置做字符串替换，
    避免 yaml.dump 破坏 !!python/name: 等自定义标签。
    """
    import re as _re
    mkdocs_path = Path('mkdocs.yml')
    if not mkdocs_path.exists():
        print('error: mkdocs.yml does not exist')
        return False

    # 生成新的 nav YAML 片段
    nav_yaml = yaml.dump(
        {'nav': nav},
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
        width=4096,
    )

    content = mkdocs_path.read_text(encoding='utf-8')

    # 用正则找到 nav: 块：从 ^nav: 开始，到下一个顶层 key 或文件末尾
    nav_pattern = _re.compile(
        r'^nav:.*?(?=^[a-z_]|\Z)',
        _re.MULTILINE | _re.DOTALL,
    )
    if nav_pattern.search(content):
        new_content = nav_pattern.sub(nav_yaml, content, count=1)
    else:
        new_content = content.rstrip('\n') + '\n\n' + nav_yaml

    mkdocs_path.write_text(new_content, encoding='utf-8')
    print('mkdocs.yml nav updated')
    return True


# ──────────────────────────────────────────────
# main
# ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--target',
        choices=['readme', 'all-articles', 'all-categories', 'mkdocs-nav', 'both', 'all'],
        default='both',
        help='选择要生成的目标（both=readme+all-articles，all=readme+all-articles+all-categories+mkdocs-nav）',
    )
    args = parser.parse_args()

    print('scanning docs/...')
    articles, category_articles, skipped_files, dir_order = scan_docs()

    if not articles:
        print('warning: no articles found')
    else:
        total = sum(len(items) for items in articles.values())
        print(f'found {total} articles in {len(articles)} directory categories and {len(category_articles)} front-matter categories')

    if skipped_files:
        print(f'warning: skipped {len(skipped_files)} file(s) due to invalid front matter')
        for path in skipped_files:
            print(f'warning: skipped file: {path}')

    do_readme = args.target in ('readme', 'both', 'all')
    do_all_articles = args.target in ('all-articles', 'both', 'all')
    do_all_categories = args.target in ('all-categories', 'all')
    do_nav = args.target in ('mkdocs-nav', 'all')

    if do_readme:
        print('generating README section...')
        readme_section = generate_readme_section(articles)
        print('updating README.md...')
        if not update_readme(readme_section):
            print('error: failed to update README.md')
            raise SystemExit(1)

    if do_all_articles:
        print('generating all-articles page...')
        all_articles_content = generate_all_articles_page(articles)
        print('writing docs/all-articles.md...')
        if not create_all_articles_page(all_articles_content):
            print('error: failed to write docs/all-articles.md')
            raise SystemExit(1)

    if do_all_categories:
        print('generating all-categories page...')
        all_categories_content = generate_all_categories_page(category_articles)
        print('writing docs/all-categories.md...')
        if not create_all_categories_page(all_categories_content):
            print('error: failed to write docs/all-categories.md')
            raise SystemExit(1)

    if do_nav:
        print('generating mkdocs.yml nav...')
        nav = generate_mkdocs_nav(articles, dir_order)
        print('updating mkdocs.yml...')
        if not update_mkdocs_nav(nav):
            print('error: failed to update mkdocs.yml')
            raise SystemExit(1)

    print('done')


if __name__ == '__main__':
    main()
