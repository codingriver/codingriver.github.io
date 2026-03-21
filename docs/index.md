---
title: "王国庆的博客"
date: "2026-03-21"
tags:
  - 笔记
categories:
  - 首页
comments: false
---
# 王国庆的博客

当前仓库正在从 Hugo 迁移到 MkDocs。

## 当前状态

- 已开始盘点 Hugo 源内容
- 已删除第一批高置信废弃文件
- 已建立 MkDocs 最小配置骨架
- 下一步将把 `content/` 下的有效文章迁移到 `docs/` 分类目录

## 已确认保留的核心来源

- `content/`：文章正文来源
- `static/`：可能被文章引用的静态资源
- `config.toml`：迁移时用于提取站点信息
- `docs/博客从Hugo迁移到MkDocs执行方案.md`

## 迁移原则

- 先分析，再迁移
- 明确无用的直接删除
- 不能确认的列入待确认清单
- 最终只保留 MkDocs 有效结构
