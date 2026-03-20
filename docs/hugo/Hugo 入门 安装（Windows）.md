---
title: "Hugo 入门 安装（Windows）"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: [""]
categories: ["随笔"]
---

<!--more-->

>参考 [Hugo 入门 安装和使用](https://blog.csdn.net/weixin_30952535/article/details/97155453)

### 1. 下载Hugo
[Hugo官网]()
[github](https://github.com/gohugoio/hugo)
下载：[下载Hugo](https://github.com/gohugoio/hugo/releases)
这里下载的是`hugo_0.74.3_Windows-64bit.zip`
解压后就一个exe文件
放在文件夹`F:\Hugo\bin\`中，然后添加到环境变量中
执行 `hugo -version`
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20200731180653107.png)  

出现版本号，配置完成
### 2. 创建站点项目
假设要创建站点存放在`F:\Hugo\Sites\`目录中
在命令行切换到该目录下执行`hugo new site codingriver` 创建codingriver站点项目

  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20200731181020763.png)  

创建完成
### 3.添加主题
命令行切换到新创建站点项目codingriver内
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/2020073118165314.png)  


 添加主题 [maupassant](https://github.com/flysnow-org/maupassant-hugo)执行`git clone https://github.com/JokerQyou/maupassant-hugo.git themes/maupassant`
   
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20200731181707703.png)  

 这样主题下载完成然后，在当前项目目录内打开`config.toml`配置文件，在最后添加一行`theme = "maupassant"`
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20200731181855310.png)  


  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20200731181842321.png)  

这样主题配置完成
### 4. 运行站点项目
在站点项目内执行命令`hugo server -D`
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20200731181955198.png)  

这里表示执行成功，打开网页`http://localhost:1313/`
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20200731182103643.png)  

安装配置完成


### 5. 使用
使用教程`https://www.flysnow.org/2018/07/29/from-hexo-to-hugo.html`
使用教程 `https://blog.csdn.net/weixin_30952535/article/details/97155453`
主題説明 `https://github.com/JokerQyou/maupassant-hugo/blob/master/README_zh.md`
主題説明 `https://github.com/flysnow-org/maupassant-hugo`
參考文章 `https://www.cnblogs.com/kika/p/10851605.html`

### 6. 常见问题
#### Unable to locate Config file
启动 hugo 内置服务器时，会在当前目录执行的目录中寻找项目的配置文件。所以，需要在项目根目录中执行这个命令，否则报错如下：
```
C:\Users\kika\kikakika\themes>hugo server --theme=hugo-bootstrap --buildDrafts --watch
Error: Unable to locate Config file. Perhaps you need to create a new site.
       Run `hugo help new` for details. (Config File "config" Not Found in "[C:\\Users\\kika\\kikakika\\themes]")
```

#### Unable to find theme Directory
hugo 默认在项目中的 themes 目录中寻找指定的主题。所有下载的主题都要放在这个目录中才能使用，否则报错如下：
```
C:\Users\kika\kikakika>hugo server --theme=hugo-bootstrap --buildDrafts --watch
Error: Unable to find theme Directory: C:\Users\kika\kikakika\themes\hugo-bootstrap
```
#### 生成的网站没有文章
生成静态网站时，hugo 会忽略所有通过 draft: true 标记为草稿的文件。必须改为 draft: false 才会编译进 HTML 文件。


