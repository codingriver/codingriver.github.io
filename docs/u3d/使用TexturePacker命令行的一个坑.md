---
title: "使用TexturePacker命令行的一个坑"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Unity"]
categories: ["Unity"]
---

<!--more-->

>使用命令行发现没办法处理九宫图呀还得在工程里面配置九宫图，太麻烦了，不知道怎么破这个问题
```c
REM @echo off 
REM :: # cmd TextruePacker 
REM :: # --sheet path 输出图片名字
REM :: # --data path 输出描述文件，plist tpsheet
REM :: # --format  format 输出格式
REM :: # --max-width 1024 --max-height 1024 当前图集的尺寸 （前面两个等价于后面 --max-size 1024）
REM :: # –shape-padding <int> 图块之间缝隙的宽度,默认值是2
REM :: # –border-padding <int> 可以理解为边框的宽度,默认值为2
REM :: # –enable-rotation/diable-rotation 开启/关闭旋转,默认值和输出的格式有关系,cococ2d格式默认enable
REM :: # –trim/no-trim 剪裁图片,即移除图片周围的透明像素,保留原始尺寸,默认开启
set atlas=common
echo %atlas%
set assetDir=../%atlas%
set project=../%atlas%.tps
set outputPath=./../../Unity/Assets/OriginalRes/UIImage/
set texPath=%outputPath%%atlas%.png
set sheetPath=%outputPath%%atlas%.tpsheet
echo %assetDir%
echo %outputPath%
echo %texPath%
echo %sheetPath%
TexturePacker %project% --format unity-texture2d --sheet %texPath% --data %sheetPath% --max-width 1024 --max-height 1024 --shape-padding 2 --border-padding 2 --enable-rotation --no-trim --opt RGBA8888 --texture-format png --scale 1
REM TexturePacker %project% --format unity-texture2d --sheet %texPath% --data %sheetPath% 
REM TexturePacker %project% 
pause & exit 
```