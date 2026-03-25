---
title: "[TEST] Draft 功能测试文章"
date: "2026-03-25"
draft: true
categories:
  - ANote
tags:
  - test
---
# Draft 测试文章

这是一篇 draft: true 的测试文章。

- 不应出现在 README 索引
- 不应出现在 all-articles.md
- 不应出现在 all-categories.md
- 不应出现在 mkdocs.yml nav
- check_docs.py 应跳过检查
- normalize_images.py 应跳过图片检查
