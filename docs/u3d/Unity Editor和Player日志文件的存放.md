---
title: "Unity Editor和Player日志文件的存放"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Unity"]
categories: ["Unity"]
---

<!--more-->



### Editor 编辑器日志
>编辑器日志，可以通过Unity的控制台窗口中Open Editor Log 按钮打开。

|Mac OS X|	~/Library/Logs/Unity/Editor.log|
|-|-|
|Windows XP *	|C:\Documents and Settings\username\Local Settings\Application Data\Unity\Editor\Editor.log|
|Windows Vista/7 *|	C:\Users\username\AppData\Local\Unity\Editor\Editor.log|




### Player 运行日志

|macOS|	~/Library/Logs/Unity/Player.log|
|-|-|
|Windows	|C:\Users\username\AppData\LocalLow\CompanyName\ProductName\output_log.txt|
|Linux	|~/.config/unity3d/CompanyName/ProductName/Player.log|


[官方说明](https://docs.unity3d.com/Manual/LogFiles.html)