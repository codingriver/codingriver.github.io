#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 docs/ 下所有中文图片目录名改为对应的英文（拼音/英文映射），
并同步更新所有 md 文件中的图片引用路径。

只重命名 image/ 子目录，不改动图片文件名本身。
"""

import os
import re
import shutil
from pathlib import Path

# 中文目录名 -> 英文目录名映射
DIR_MAP = {
    'Unity-URP笔记': 'Unity-URP-Note',
    'CSharp笔记': 'CSharp-Note',
    'DOTS笔记': 'DOTS-Note',
    'DrawCall优化实战演讲稿': 'DrawCall-Optimization',
    'EOC项目分析笔记1': 'EOC-Project-Analysis1',
    'EOC项目笔记': 'EOC-Project-Note',
    'Git笔记': 'Git-Note',
    'IGG开发笔记': 'IGG-Dev-Note',
    'IGG性能分析笔记': 'IGG-Perf-Note',
    'PBR笔记': 'PBR-Note',
    'ParticleEffectForUGUI使用教程': 'ParticleEffectForUGUI-Tutorial',
    'SSH笔记': 'SSH-Note',
    'Shader案例': 'Shader-Cases',
    'Shader笔记': 'Shader-Note',
    'Shell笔记': 'Shell-Note',
    'UI笔记': 'UI-Note',
    '包体大小优化笔记': 'Package-Size-Note',
    '操作系统笔记': 'OS-Note',
    '日常笔记': 'Daily-Note',
}

docs_dir = Path('docs')

# Step 1: 收集所有 image 目录下需要重命名的子目录
rename_pairs = []  # (old_path, new_path, old_rel, new_rel)
for image_dir in docs_dir.rglob('image'):
    if not image_dir.is_dir():
        continue
    for sub in image_dir.iterdir():
        if sub.is_dir() and sub.name in DIR_MAP:
            new_name = DIR_MAP[sub.name]
            new_path = sub.parent / new_name
            rename_pairs.append((sub, new_path, sub.name, new_name))

print(f'Found {len(rename_pairs)} directories to rename:')
for old, new, _, _ in rename_pairs:
    print(f'  {old} -> {new}')

# Step 2: 重命名目录
for old_path, new_path, old_name, new_name in rename_pairs:
    if old_path.exists():
        if new_path.exists():
            print(f'SKIP (already exists): {new_path}')
        else:
            old_path.rename(new_path)
            print(f'Renamed: {old_name} -> {new_name}')

# Step 3: 更新所有 md 文件中的引用
md_files = list(docs_dir.rglob('*.md'))
print(f'\nUpdating {len(md_files)} markdown files...')
updated_files = 0
for md_file in md_files:
    content = md_file.read_text(encoding='utf-8')
    new_content = content
    for _, _, old_name, new_name in rename_pairs:
        new_content = new_content.replace(
            f'image/{old_name}/', f'image/{new_name}/'
        )
    if new_content != content:
        md_file.write_text(new_content, encoding='utf-8')
        print(f'  Updated: {md_file}')
        updated_files += 1

print(f'\nDone: renamed {len(rename_pairs)} dirs, updated {updated_files} md files')
