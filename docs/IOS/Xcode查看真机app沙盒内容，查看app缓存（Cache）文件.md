---
title: "Xcode查看真机app沙盒内容，查看app缓存（Cache）文件"
date: "2026-03-21"
tags:
  - iOS
  - 网络
  - 工具链
categories:
  - IOS
comments: true
---
# Xcode查看真机app沙盒内容，查看app缓存（Cache）文件

﻿

1.连接你的设备，在Xcode下点击 Window —> Device（cmd + shift + 2） 弹出窗口，选择你的设备，找到你已安装的APP，选中你想要查看沙盒的APP。

2.点击底部有个类似设置的按钮，出现几个选项，选择Download Container ，下载文件到本地，将会看到一个后缀为xcappdata的文件，选择这个文件并显示包内容查看对应的沙盒文件。

  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/Xcode查看真机app沙盒内容，查看app缓存（Cache）文件/20200921113309.png)  




***下载失败或者Show Container没有内容 解决方案：  卸载app，重启手机设备，安装app就好了**

  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/Xcode查看真机app沙盒内容，查看app缓存（Cache）文件/20200921113343.png)  



