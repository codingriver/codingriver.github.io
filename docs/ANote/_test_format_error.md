---
title "[TEST] 格式错误文章"
date: "2026-03-25"
categories:
  - ANote
tags:
  - test
---
# 格式错误测试文章

这篇文章的 front matter 故意有 YAML 语法错误（title 缺少冒号后面的空格与引号）。
用于验证 check_docs.py 能正确报告错误文件。
