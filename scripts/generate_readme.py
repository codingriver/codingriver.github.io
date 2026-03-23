#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动生成 README.md 和 docs/all-articles.md
扫描 docs/ 目录，按分类组织文章链接，包含创建日期
"""

import os
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def get_article_info(filepath):
    """从 Markdown 文件提取 title 和 date"""
    title = None
    date = None

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            title_match = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', content)
            if title_match:
                title = title_match.group(1).strip()
            date_match = re.search(r'date:\s*["\']?([^"\'\n]+)["\']?', content)
            if date_match:
                date = date_match.group(1).strip()
    except Exception as e:
        print(f"warning: cannot read {filepath}: {e}")

    if not title:
        title = Path(filepath).stem
    if not date:
        timestamp = os.path.getmtime(filepath)
        date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

    return title, date

def scan_docs():
    """扫描 docs 目录，按分类组织文章"""
    # 使用 resolve() 确保为绝对路径，避免 relative_to 在 CI 环境报错
    docs_dir = Path('docs').resolve()
    repo_root = docs_dir.parent
    articles = defaultdict(list)

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
        return articles

    for category_dir in sorted(docs_dir.iterdir()):
        if not category_dir.is_dir() or category_dir.name.startswith('.'):
            continue
        category_name = category_names.get(category_dir.name, category_dir.name)
        for md_file in sorted(category_dir.glob('*.md')):
            if md_file.name == 'index.md':
                continue
            title, date = get_article_info(md_file)
            # relative_to(repo_root) 确保两边都是绝对路径，CI 和本地均可正常工作
            rel_path = str(md_file.relative_to(repo_root)).replace('\\', '/')
            articles[category_name].append((title, date, rel_path))

    return articles

def generate_readme_section(articles):
    """生成 README 的文章索引部分（含日期，按日期倒序）"""
    lines = ['## \U0001f4da 完整文章索引\n']

    for category in sorted(articles.keys()):
        items = articles[category]
        lines.append('\n### ' + category + '\n')
        sorted_items = sorted(items, key=lambda x: x[1], reverse=True)
        for title, date, path in sorted_items:
            lines.append('- **' + date + '** - [' + title + '](' + path + ')')

    lines.append('\n### 项目记录与随笔\n')
    lines.append('详见 [ANote 栏目](docs/ANote/index.md)\n')

    return '\n'.join(lines)

def generate_all_articles_page(articles):
    """生成 docs/all-articles.md 页面（含日期，按日期倒序）"""
    lines = [
        '---',
        'title: "全部文档"',
        'date: "2026-03-23"',
        'comments: false',
        '---',
        '',
        '# 全部文档',
        '',
        '这里列出博客中的全部文章，按分类组织，包含创建日期。',
        '',
    ]

    for category in sorted(articles.keys()):
        items = articles[category]
        lines.append('## ' + category + '\n')
        sorted_items = sorted(items, key=lambda x: x[1], reverse=True)
        for title, date, path in sorted_items:
            lines.append('- **' + date + '** - [' + title + '](' + path + ')')
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
        print("error: cannot find article index section in README.md")
        return False

    new_content = content[:start_idx] + new_section + '\n\n' + content[end_idx:]

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("README.md updated")
    return True

def create_all_articles_page(content):
    """创建或更新 docs/all-articles.md"""
    all_articles_path = Path('docs/all-articles.md')
    with open(all_articles_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("docs/all-articles.md updated")
    return True

if __name__ == '__main__':
    print("scanning docs/...")
    articles = scan_docs()

    if not articles:
        print("warning: no articles found")
    else:
        total = sum(len(items) for items in articles.values())
        print(f"found {total} articles in {len(articles)} categories")

    print("generating README section...")
    readme_section = generate_readme_section(articles)

    print("updating README.md...")
    if not update_readme(readme_section):
        print("error: failed to update README.md")
        exit(1)

    print("generating all-articles page...")
    all_articles_content = generate_all_articles_page(articles)

    print("writing docs/all-articles.md...")
    if not create_all_articles_page(all_articles_content):
        print("error: failed to write docs/all-articles.md")
        exit(1)

    print("done")
