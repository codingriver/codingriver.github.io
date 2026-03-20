# 博客使用指南

> 基于 MkDocs Material 主题，托管于 GitHub Pages
> 博客地址：https://blog.wgqing.com

---

## 目录

1. [环境搭建](#1-环境搭建)
2. [本地预览](#2-本地预览)
3. [新建文章](#3-新建文章)
4. [图片使用](#4-图片使用)
5. [发布到线上](#5-发布到线上)
6. [更换主题风格](#6-更换主题风格)
7. [常用配置说明](#7-常用配置说明)
8. [目录结构说明](#8-目录结构说明)

---

## 1. 环境搭建

### 前置要求

- Python 3.8 及以上（推荐 3.11）
- Git

### 一次性安装（首次使用）

```bash
# 安装 MkDocs Material 及插件
pip install mkdocs-material mkdocs-git-revision-date-localized-plugin gitpython jieba
```

### 验证安装

```bash
python -m mkdocs --version
# 输出类似：python -m mkdocs, version 1.6.1
```

### 克隆仓库（换电脑时）

```bash
git clone git@github.com:codingriver/codingriver.github.io.git
cd codingriver.github.io
```

---

## 2. 本地预览

### 启动预览服务

```bash
# 在项目根目录执行
python -m mkdocs serve
```

然后浏览器打开：**http://127.0.0.1:8000**

> 支持热更新：修改 `docs/` 下的 md 文件后，浏览器会自动刷新，无需重启。

### 构建静态文件（可选）

```bash
python -m mkdocs build
```

生成的静态文件在 `site/` 目录下，可直接部署到任意静态托管服务。

### 停止预览

在终端按 `Ctrl + C` 即可。

---

## 3. 新建文章

### 选择分类

| 目录 | 分类 | 适用内容 |
|------|------|----------|
| `docs/u3d/` | Unity3D | Unity 相关技术文章 |
| `docs/shader/` | Shader | Shader / 渲染技术 |
| `docs/csharp/` | CSharp | C# 语言特性 |
| `docs/math/` | 数学 | 图形学数学推导 |
| `docs/ANote/` | 日常笔记 | 随笔、技术记录 |
| `docs/other/` | 其他 | 工具、杂项 |
| `docs/basesystem/` | 操作系统 | 底层系统知识 |
| `docs/datastruct/` | 数据结构算法 | 算法分析 |
| `docs/IOS/` | iOS | iOS 开发 |
| `docs/Android/` | Android | Android 开发 |
| `docs/unityTool/` | Unity工具 | 工具类封装 |
| `docs/unity编辑器/` | Unity编辑器 | Editor 扩展 |
| `docs/Graphics/` | 图形学 | DirectX / 图形学 |
| `docs/lua/` | Lua | Lua 语言 |
| `docs/hugo/` | Hugo | Hugo 博客相关 |

### 新建随笔（以日常笔记为例）

1. 在 `docs/ANote/` 目录下新建 `.md` 文件：

```bash
# 文件名建议用简洁的中文或英文，不要有特殊符号
# 例如：docs/ANote/我的随笔.md
```

2. 文件内容格式：

```markdown
# 文章标题

> 可选的摘要描述

正文内容...

## 小节标题

更多内容...
```

> **注意**：MkDocs 不需要 Hugo 的 front matter（`---` 头部元数据），直接写 Markdown 即可。文章标题用 `# 一级标题`。

3. 更新分类索引页（可选，推荐）：

打开 `docs/ANote/index.md`，在文章列表末尾加上新文章的链接：

```markdown
- [我的随笔](我的随笔.md)
```

4. 保存后，本地预览会自动刷新。

### 新建分类（如果需要全新分类）

1. 在 `docs/` 下新建目录，如 `docs/新分类/`
2. 在目录下创建 `index.md` 作为分类首页
3. 在 `mkdocs.yml` 的 `nav` 中添加入口（如果使用手动 nav）

---

## 4. 图片使用

### 集中图片（推荐）

将图片放到 `docs/images/` 目录下，在文章中引用：

```markdown
<!-- 文章在 docs/ANote/ 下，图片在 docs/images/ 下 -->
![图片说明](../images/图片文件名.png)
```

### 文章本地图片

也可以在文章同级目录下建 `image/文章名/` 子目录存放图片：

```
docs/u3d/image/我的文章/
    截图1.png
    截图2.png
```

引用方式：

```markdown
![说明](image/我的文章/截图1.png)
```

### 支持的格式

`png` / `jpg` / `gif` / `webp` / `svg` / `mp4`（视频用 `<video>` 标签）

### 视频引用

```html
<video src="../images/demo.mp4" controls width="560" height="330"></video>
```

---

## 5. 发布到线上

### 日常写作发布流程

```bash
# 1. 写好文章，本地预览确认无误
python -m mkdocs serve

# 2. 提交并推送
git add docs/
git commit -m "新增文章：文章标题"
git push origin master
```

推送后 GitHub Actions 自动触发，约 **2~3 分钟** 后 `blog.wgqing.com` 更新。

### 查看部署状态

打开：https://github.com/codingriver/codingriver.github.io/actions

绿色勾 = 部署成功，红色叉 = 部署失败（点击查看日志）。

### 手动触发部署（可选）

在 GitHub Actions 页面点击 `Run workflow` 可手动触发。

---

## 6. 更换主题风格

### 修改配色

编辑 `mkdocs.yml` 中的 `theme.palette`：

```yaml
theme:
  name: material
  palette:
    # 亮色模式
    - scheme: default
      primary: indigo      # 主色：indigo / blue / teal / green / red / pink 等
      accent: indigo       # 强调色
      toggle:
        icon: material/brightness-7
        name: 切换暗色模式
    # 暗色模式
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: 切换亮色模式
```

可用颜色：`red` `pink` `purple` `indigo` `blue` `cyan` `teal` `green` `lime` `yellow` `orange` `deep-orange` `brown` `grey` `blue-grey`

### 修改字体

```yaml
theme:
  font:
    text: Roboto        # 正文字体（Google Fonts）
    code: Roboto Mono   # 代码字体
```

### 更换为纯暗色（不切换）

```yaml
theme:
  palette:
    scheme: slate
    primary: blue grey
    accent: cyan
```

### 修改 Logo 和 Favicon

```yaml
theme:
  logo: images/logo.png      # 放到 docs/images/logo.png
  favicon: images/favicon.ico
```

### 关闭/开启导航功能

```yaml
theme:
  features:
    - navigation.tabs         # 顶部标签栏
    - navigation.sections     # 左侧分组展开
    - navigation.top          # 返回顶部按钮
    - navigation.indexes      # 分类目录页
    - search.highlight        # 搜索结果高亮
    - search.suggest          # 搜索建议
    - content.code.copy       # 代码一键复制
```

---

## 7. 常用配置说明

`mkdocs.yml` 关键配置项说明：

```yaml
site_name: codingriver          # 网站标题（显示在浏览器标签和顶栏）
site_url: https://blog.wgqing.com/  # 网站地址（用于 sitemap 和 canonical URL）
site_author: codingriver        # 作者名
site_description: ...           # 网站描述（SEO 用）

repo_url: https://github.com/...  # 右上角 GitHub 图标链接
edit_uri: edit/master/docs/       # 页面右上角「编辑」按钮链接到源文件

docs_dir: docs                  # 内容目录（不要改）
```

### 添加自定义 CSS

1. 新建 `docs/stylesheets/extra.css`
2. 在 `mkdocs.yml` 中添加：

```yaml
extra_css:
  - stylesheets/extra.css
```

### 添加自定义 JS

```yaml
extra_javascript:
  - javascripts/extra.js
```

---

## 8. 目录结构说明

```
hugo-project/                   # 项目根目录
├── docs/                       # 所有博客内容（核心目录）
│   ├── index.md                # 博客首页
│   ├── about.md                # 关于页
│   ├── images/                 # 集中存放图片（442张+）
│   ├── u3d/                    # Unity3D 分类（57篇）
│   │   ├── index.md            # 分类首页（文章列表）
│   │   ├── unity性能优化总结.md
│   │   └── image/              # 该分类文章的本地图片
│   ├── shader/                 # Shader 分类（19篇）
│   ├── csharp/                 # CSharp 分类（15篇）
│   ├── math/                   # 数学分类（12篇）
│   ├── ANote/                  # 日常笔记（43篇）
│   └── ...                     # 其他分类
├── mkdocs.yml                  # MkDocs 主配置文件
├── .github/
│   └── workflows/
│       └── deploy-mkdocs.yml   # GitHub Actions 自动部署配置
├── BLOG_GUIDE.md               # 本文档
├── content/                    # Hugo 旧内容（保留备用，不影响 MkDocs）
├── themes/                     # Hugo 旧主题（保留备用）
└── site/                       # MkDocs 构建产物（自动生成，不要提交）
```

---

## 快速参考卡

```bash
# 本地预览
python -m mkdocs serve

# 构建静态文件
python -m mkdocs build

# 发布文章
git add docs/
git commit -m "新增：文章标题"
git push origin master

# 重新安装依赖（换电脑时）
pip install mkdocs-material mkdocs-git-revision-date-localized-plugin gitpython jieba
```
