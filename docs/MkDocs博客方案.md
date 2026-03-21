# MkDocs 博客方案

本文档用于说明当前博客从 Hugo 迁移到 MkDocs 之后的标准使用方式，包括本地环境部署、日常写作、主题选择、GitHub Pages 部署、`gh-pages` 分支使用方式，以及搜索、评论、Git 更新时间等增强能力方案。

---

## 1. 当前博客架构说明

当前仓库采用如下结构：

- `master` 分支：保存源码
  - `docs/`：文章与图片资源
  - `mkdocs.yml`：MkDocs 配置
  - `.github/workflows/`：自动部署流程
- `gh-pages` 分支：保存构建产物
  - 只放静态站点文件，不放源码

推荐原则：

- 平时只在 `master` 分支维护内容
- 不要把 `site/` 构建产物提交到 `master`
- 使用 GitHub Actions 自动将构建结果发布到 `gh-pages`

---

## 2. 本地环境部署

### 2.1 Python 环境

建议使用 Python 3.10 及以上版本。

检查版本：

```bash
python --version
```

### 2.2 安装 MkDocs 和主题

当前站点使用 Material for MkDocs 主题。

安装命令：

```bash
pip install mkdocs mkdocs-material
```

### 2.3 安装推荐插件

如果要支持 Git 更新时间、作者信息等功能，建议同时安装以下插件：

```bash
pip install mkdocs-git-revision-date-localized-plugin mkdocs-git-authors-plugin gitpython jieba
```

说明：

- `mkdocs-git-revision-date-localized-plugin`：显示页面最后更新时间、创建时间
- `mkdocs-git-authors-plugin`：显示页面作者信息
- `gitpython`：部分 Git 相关插件依赖
- `jieba`：增强中文搜索分词

### 2.4 本地启动预览

在项目根目录执行：

```bash
mkdocs serve
```

默认访问地址：

```text
http://127.0.0.1:8000
```

### 2.5 本地构建静态站点

```bash
mkdocs build
```

构建产物默认输出到：

```text
site/
```

---

## 3. 日常使用方式

### 3.1 新建一篇普通文章

例如在 `docs/u3d/` 下新增文章：

```text
docs/u3d/Unity新文章示例.md
```

正文格式示例：

```markdown
# Unity 新文章示例

这里写正文。
```

如果文章里有图片，建议与文章放在同分类目录下的 `image/` 子目录中，例如：

```text
docs/u3d/image/Unity新文章示例/demo.png
```

文章内引用：

```markdown
![示意图](image/Unity新文章示例/demo.png)
```

### 3.2 如何创建一份随笔

当前博客最适合把“随笔”放到 `ANote` 分类中。

例如新建：

```text
docs/ANote/2026-03-21-我的随笔.md
```

推荐内容模板：

```markdown
---
title: 我的随笔
date: 2026-03-21
categories:
  - ANote
tags:
  - 随笔
  - 记录
status: published
---

# 我的随笔

## 背景

记录一下今天的想法。

## 正文

正文内容。

## 总结

一句话总结。
```

说明：

- 文件名尽量简洁，必要时可带日期
- `ANote` 比较适合杂记、随笔、草稿整理、阶段记录
- 如果后续启用标签插件，上述 front matter 可以直接复用

### 3.3 如何添加分类

MkDocs 没有 Hugo 那种内建 taxonomy 分类体系，当前项目推荐使用：

## 目录即分类

例如：

- `docs/ANote/`
- `docs/u3d/`
- `docs/shader/`
- `docs/other/`

分类的标准做法：

1. 在 `docs/` 下创建目录
2. 在目录中放一个 `index.md` 作为栏目首页
3. 在 `mkdocs.yml` 的 `nav` 中加入该目录
4. 将该类文章都放在此目录下

例如新增一个 `essay` 分类：

```text
docs/essay/
docs/essay/index.md
```

`index.md` 示例：

```markdown
# essay

这里收录个人随笔、阶段总结与非技术长文。
```

然后在 `mkdocs.yml` 中添加：

```yaml
- essay:
  - 栏目首页: essay/index.md
```

### 3.4 如何添加标签

当前项目可以先采用“文档中写标签 + 后续逐步增强”的方式。

推荐在文章头部添加 front matter：

```markdown
---
title: Shader 学习记录
tags:
  - Shader
  - Unity
  - 图形学
categories:
  - shader
---
```

当前阶段标签主要有两个用途：

1. 作为文章元数据保留
2. 为后续接入标签插件或博客插件做准备

如果后续要把标签真正展示成可点击页面，有两种方案：

#### 方案 A：接入博客/标签插件

优点：自动化程度高。  
缺点：配置复杂度更高。

#### 方案 B：手工维护标签索引页

例如建立：

```text
docs/tags/index.md
```

手动按标签整理文章链接。

优点：简单稳定。  
缺点：需要人工维护。

对于你当前项目，建议先采用：

## 先写 front matter 标签，展示层后续再增强

---

## 4. 主题如何使用

当前站点已经使用：

- `Material for MkDocs`

在 `mkdocs.yml` 中基本配置形式如下：

```yaml
theme:
  name: material
  language: zh
```

### 4.1 常用能力

Material 主题常用能力包括：

- 全文搜索
- 左侧导航树
- 深色/浅色模式
- 代码高亮
- 提示块（admonition）
- 页内目录
- 顶部导航增强
- 页脚与社交链接

### 4.2 常见扩展配置示例

```yaml
theme:
  name: material
  language: zh
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.top
    - search.suggest
    - search.highlight
    - content.code.copy
```

### 4.3 推荐开启的 Markdown 扩展

```yaml
markdown_extensions:
  - admonition
  - tables
  - toc:
      permalink: true
  - pymdownx.highlight
  - pymdownx.superfences
  - pymdownx.inlinehilite
  - pymdownx.tabbed:
      alternate_style: true
```

---

## 5. 推荐哪些主题

### 5.1 第一推荐：Material for MkDocs

适用场景：

- 技术博客
- 知识库
- 文档站
- 带导航分组的大型文章集合

优点：

- 功能最全
- 社区成熟
- 搜索体验好
- 主题美观
- 插件与生态完善

### 5.2 次选：MkDocs 默认主题

适用场景：

- 极简站点
- 个人内部笔记
- 对美观要求不高，只追求最小依赖

优点：

- 轻量
- 配置最简单

缺点：

- 展示能力弱
- 不适合你当前这种多分类博客

### 5.3 其他主题建议

如果后续想尝试更博客化的风格，可以考虑：

- Material + blog 插件
- Material + 自定义首页

对于当前项目，不建议频繁换主题，建议继续以 Material 为主。

---

## 6. 如何部署到 GitHub

### 6.1 部署目标说明

推荐方式：

- `master`：源码分支
- `gh-pages`：静态站点发布分支

GitHub Pages 读取 `gh-pages` 分支内容进行站点发布。

### 6.2 `gh-pages` 分支如何使用

`gh-pages` 是专门用来放静态网站产物的分支。

它的特点：

- 不保存 MkDocs 源码
- 只保存构建好的 HTML、CSS、JS、图片等文件
- 每次部署时会被新的构建产物覆盖

因此：

- 日常开发不要在 `gh-pages` 上改文章
- 日常开发永远在 `master` 上进行
- `gh-pages` 只作为发布分支使用

### 6.3 当前在 `master` 分支，如何手工将产物推送到 `gh-pages`

最简单方式：

```bash
mkdocs gh-deploy --clean
```

这个命令会自动：

1. 构建站点
2. 切换发布逻辑
3. 将产物推送到 `gh-pages`

如果要强制覆盖远端：

```bash
mkdocs gh-deploy --clean --force
```

### 6.4 手工发布的底层逻辑说明

如果不使用 `mkdocs gh-deploy`，理论上也可以手工发布：

1. 在 `master` 执行 `mkdocs build`
2. 得到 `site/` 目录
3. 切换到 `gh-pages`
4. 清空旧内容
5. 将 `site/` 内容复制到分支根目录
6. 提交并推送

这种方式可行，但不推荐长期使用，因为容易出错。

### 6.5 GitHub Pages 仓库设置

在 GitHub 仓库页面中：

1. 打开 `Settings`
2. 打开 `Pages`
3. 如果使用 Actions 自动化：选择 `GitHub Actions`
4. 如果使用分支发布：选择 `Deploy from a branch`
5. 分支选择 `gh-pages`

推荐优先使用：

## GitHub Actions 自动部署

---

## 7. 是否使用 GitHub Actions 自动化

### 7.1 当前仓库已有自动化部署

当前仓库已经存在工作流：

```text
.github/workflows/deploy-mkdocs.yml
```

当前逻辑是：

- 当 `master` 分支有新的 push 时触发
- 自动安装 MkDocs 依赖
- 执行 `mkdocs gh-deploy --force --clean`
- 自动推送到 `gh-pages`

### 7.2 当前工作流的意义

这意味着：

- 你平时只需要提交 `master`
- 不需要手工切换 `gh-pages`
- 不需要把 `site/` 提交到源码分支

### 7.3 当前工作流示意

```yaml
name: Deploy MkDocs to GitHub Pages

on:
  push:
    branches:
      - master

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      - name: Install dependencies
        run: |
          pip install mkdocs-material mkdocs-git-revision-date-localized-plugin gitpython jieba

      - name: Deploy
        run: mkdocs gh-deploy --force --clean
```

### 7.4 自动化部署推荐结论

对于当前项目，推荐：

## 保持 `master` 维护源码，使用 GitHub Actions 自动发布到 `gh-pages`

这是最省心、最稳定的方式。

---

## 8. master 分支如何忽略 MkDocs 产物

MkDocs 默认构建输出目录为：

```text
site/
```

这个目录不应该提交到 `master` 分支。

因此必须在 `.gitignore` 中加入：

```gitignore
site/
```

这样可以避免：

- 构建产物污染源码分支
- 出现大量无意义 diff
- 误把静态 HTML 提交到 `master`

推荐原则：

- `master` 只放源码
- `gh-pages` 只放构建产物

---

## 9. 博客增强能力方案

### 9.1 搜索（保留 `jieba` 依赖）

当前站点继续使用 Material 主题自带搜索能力，推荐在 `mkdocs.yml` 中显式保留：

```yaml
plugins:
  - search
```

如果中文内容较多，建议继续保留 `jieba` 依赖，用于增强中文分词搜索效果。

安装示例：

```bash
pip install jieba
```

如果使用 GitHub Actions 自动部署，也应在工作流安装依赖时保留 `jieba`：

```bash
pip install mkdocs-material mkdocs-git-revision-date-localized-plugin mkdocs-git-authors-plugin gitpython jieba
```

推荐结论：

- 搜索功能保留
- `jieba` 依赖保留
- 继续使用 Material 内置搜索，不额外引入第三方搜索服务

### 9.2 显示 Git 最后更新时间

推荐使用插件：

```bash
pip install mkdocs-git-revision-date-localized-plugin
```

推荐配置：

```yaml
plugins:
  - search
  - git-revision-date-localized:
      enable_creation_date: true
      type: datetime
      timezone: Asia/Shanghai
      locale: zh
```

这个插件可以提供：

- 页面最后更新时间
- 页面创建时间（首次提交时间）

适合技术博客和知识库，因为读者可以快速判断文档是否过时。

### 9.3 显示 Git 作者信息

推荐使用插件：

```bash
pip install mkdocs-git-authors-plugin
```

推荐配置：

```yaml
plugins:
  - search
  - git-revision-date-localized:
      enable_creation_date: true
      type: datetime
      timezone: Asia/Shanghai
      locale: zh
  - git-authors
```

作用：

- 显示页面作者信息
- 多人协作时可追踪主要维护者

对于单人博客，它的价值主要体现在：

- 为后续多人协作留好扩展位
- 与 Git 更新时间一起构成完整的文档元信息

### 9.4 支持评论系统：采用 Giscus 方案

评论系统建议统一采用：

## Giscus

原因：

- 基于 GitHub Discussions
- 不需要自建评论后端
- 与 GitHub Pages 兼容性好
- 适合技术博客
- 评论数据跟随仓库生态，不依赖额外数据库

接入步骤：

1. 在 GitHub 仓库中开启 `Discussions`
2. 访问 `https://giscus.app/zh-CN`
3. 选择仓库、Discussion 分类、映射方式
4. 生成脚本配置
5. 通过 Material 自定义模板或额外 HTML 注入到文章页

建议映射方式：

- 使用页面路径或页面标题作为 discussions 映射键

推荐结论：

- 评论系统统一使用 Giscus
- 不再推荐新增 Disqus 之类的重型第三方方案
- `Utterances` 作为备选，但优先级低于 Giscus

### 9.5 支持标签系统

当前项目已经建议在文章 front matter 中保留标签字段，例如：

```markdown
---
title: Shader 学习记录
tags:
  - Shader
  - Unity
  - 图形学
categories:
  - shader
---
```

推荐的标签系统落地分两步：

#### 第一步：先统一写标签元数据

所有新文章都尽量补充 `tags` 字段，先把标签数据沉淀下来。

优点：

- 成本低
- 不影响当前文档结构
- 为后续自动化标签页做准备

#### 第二步：再决定标签展示方式

推荐两种可选方案：

##### 方案 A：手工维护标签索引页

例如建立：

```text
docs/tags/index.md
```

再按标签整理文章入口。

优点：

- 最稳定
- 不依赖额外插件
- 易于控制展示质量

缺点：

- 需要人工维护

##### 方案 B：后续接入博客/标签插件

适合未来更博客化的展示需求，例如：

- 自动生成标签归档页
- 标签聚合浏览
- 更像博客站点而非纯文档站

优点：

- 自动化程度高

缺点：

- 配置复杂度更高
- 需要额外适配当前目录结构

当前项目推荐结论：

## 先统一写 `tags` 元数据，展示层先采用手工标签页，后续再评估是否插件化

### 9.6 显示 Git 提交更新日志

MkDocs 默认不直接展示每篇文章的完整 Git 提交历史。

推荐分两档：

#### 最低成本方案

- 显示最后更新时间
- 显示作者信息
- 增加“编辑此页”入口
- 通过 GitHub 页面查看历史提交

优点：

- 实现简单
- 维护成本低
- 对当前博客最合适

#### 增强方案

在 CI 中通过脚本执行 `git log`，自动生成一份全站或每篇文章的 changelog 页面，例如：

```text
docs/changelog/index.md
```

优点：

- 可在站内直接看更新历史

缺点：

- 维护复杂度高
- 需要定制脚本

当前推荐先采用：

## 最低成本方案

---

## 10. 推荐的后续配置增强

后续建议逐步增强 `mkdocs.yml`：

```yaml
theme:
  name: material
  language: zh
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.top
    - search.suggest
    - search.highlight
    - content.code.copy

plugins:
  - search
  - git-revision-date-localized:
      enable_creation_date: true
      type: datetime
      timezone: Asia/Shanghai
      locale: zh
  - git-authors
```

如果要支持“编辑此页”：

```yaml
repo_url: <你的 GitHub 仓库地址>
edit_uri: edit/master/docs/
```

这样每篇文章都能直接跳转到 GitHub 编辑页面。

---

## 11. 推荐维护规范

### 11.1 文件命名

建议：

- 文件名直接用文章标题即可
- 图片放在对应分类目录下的 `image/文章名/` 中
- 不要把大量公共图片散落在根目录

### 11.2 分类原则

建议分类保持稳定，不要频繁改目录名。

### 11.3 标签原则

建议标签数量控制在 3 到 5 个以内，避免标签泛滥。

### 11.4 部署原则

- 平时只改 `master`
- 构建产物不提交到 `master`
- 通过 GitHub Actions 自动发到 `gh-pages`

---

## 12. 当前项目推荐的最终落地方案

对于当前博客，最推荐的组合是：

- 主题：Material for MkDocs
- 内容组织：目录即分类
- 标签：先写 front matter，后续按需展示
- 搜索：启用 `search`
- 更新时间：启用 `mkdocs-git-revision-date-localized-plugin`
- 提交历史：先使用 GitHub 页面查看，后续再决定是否生成 changelog 页面
- 评论：使用 Giscus
- 部署：`master` 保存源码，GitHub Actions 自动部署到 `gh-pages`
- 忽略：`master` 分支忽略 `site/`

这套方案最适合当前仓库的结构，也最容易长期维护。
