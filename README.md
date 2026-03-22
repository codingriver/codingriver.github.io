# 王国庆的博客

这是个人技术博客的源码仓库，同时也可以作为博客的基础阅读版使用。

- 高级版在线阅读：`https://codingriver.github.io/`
- 基础版仓库入口：当前仓库首页与 `docs/` 目录

## 主要内容

- [Unity](docs/u3d/index.md) ：开发实践、性能优化、UI、平台适配
- [Shader](docs/shader/index.md) ：基础概念、光照模型、特效实现
- [CSharp](docs/csharp/index.md) ：语法机制、异步编程、工程经验
- [ANote](docs/ANote/index.md) ：项目记录、随笔、开发笔记
- [Android](docs/Android/index.md) ：平台接入、浏览器跳转、系统交互
- [iOS](docs/IOS/index.md) ：Xcode、证书、审核、原生交互
- [数学](docs/math/index.md) ：图形学相关数学基础
- [工具与系统](docs/other/index.md) ：Git、Sourcetree、Node.js、系统工具等
- [标签索引](docs/tags/index.md)
- [关于](docs/about.md)

## 这个仓库的定位

这个仓库承担两层职责：

### 1. 基础版博客

直接通过 GitHub 仓库阅读内容：

- 浏览 `docs/` 目录查看文章原文
- 通过各分类 `index.md` 查看栏目导览
- 查看提交记录、差异、历史版本

### 2. 高级版博客

通过 GitHub Pages 提供更适合阅读的站点体验：

- 更完整的导航结构
- 标签索引
- 搜索与主题样式
- 后续可继续接入评论、自定义域名等能力

## 内容组织规则

当前项目采用下面这套规则：

- 分类以文件夹为主，例如 `docs/u3d/`、`docs/shader/`
- 每个分类目录下都有一个 `index.md` 作为栏目页
- 文章使用 front matter 维护 `title`、`date`、`tags`、`categories`
- `categories` 作为元数据补充，通常与所在目录保持一致
- `tags` 用于更细粒度的主题聚合

## 新增文章的基本流程

1. 选择所属分类目录，例如 `docs/u3d/`
2. 新建文章 Markdown 文件
3. 写入 front matter
4. 完成正文内容
5. 更新对应分类下的 `index.md`
6. 如有必要，再更新 `docs/tags/index.md`
7. 提交并推送，等待站点自动部署

## 文章模板

```md
---
title: "文章标题"
date: "2026-03-22"
tags:
  - 标签1
  - 标签2
categories:
  - u3d
comments: true
---

# 文章标题

正文内容。
```

## 本地预览

安装依赖后可以本地预览：

```bash
pip install mkdocs-material mkdocs-git-revision-date-localized-plugin mkdocs-git-authors-plugin gitpython jieba
mkdocs serve
```

默认访问：`http://127.0.0.1:8000/`

## 部署方式

仓库推送后通过 GitHub Pages 自动部署高级版站点。

如果后续接入自定义域名、评论系统或进一步调整首页/栏目页，也都以这个仓库为统一内容源。
