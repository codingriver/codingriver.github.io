
---
title: "IOS中Xcode-framework无法识别headers目录问题，头文件读不出来"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["IOS","Xcode"]
categories: ["IOS"]
---

<!--more-->


> 引用文章: http://blog.csdn.net/hicui/article/details/51146969

## 问题现象

framework是ios开发中经常使用到的一个组件，但是有些情况下拿到第三方提供的framework，导入自己的项目后会发现，Headers目录无法识别，编译出错的情况，比如这里：[http://tieba.baidu.com/p/4405458569#](http://tieba.baidu.com/p/4405458569#)

## 问题原因

常见IOS framework的目录结构为：

*   sdk.framework目录 

    *   Headers目录
    *   SDK文件

但是有些第三方framework生成时，脚本有问题，生成的目录结构为：

*   sdk.framework目录 

    *   Headers软链接
    *   SDK软链接
    *   Versions目录 
        -current软链接 
        -A目录 

        *   Headers目录
        *   SDK文件

软链接在不同的电脑上移动时可能会出现路径不存在，因此就导致xcode无法识别Headers目录的情况。

## 解决

将sdk.framework/Versions/A/ 下的Headers和SDK文件移动到sdk.framework目录下，将其他文件删除，重新编译即可。
