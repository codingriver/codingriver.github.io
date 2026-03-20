---
title: "iOS-11-升级后无法真机调试（could-not-locate-device-support-files）"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["IOS","Xcode"]
categories: ["IOS"]
---

<!--more-->


  

![image.png](https://imgconvert.csdnimg.cn/aHR0cDovL3VwbG9hZC1pbWFnZXMuamlhbnNodS5pby91cGxvYWRfaW1hZ2VzLzEwOTU2NDMtYmI4ZGFlOWUzMjZkN2ZlMi5wbmc?x-oss-process=image/format,png)  


**这个错误是因为Xcode缺少对应ios版本的supoort文件**

>iOS 升级到11之后，你会发现无法进行真机测试了。这种情况我在iOS 10.0更新的时候也遇到过。原因是Xcode 的DeviceSupport里面缺少了对应iOS系统版本的SDK。所以你可以选择将Xcode更新到最新版本。

或者从新版的Xcode目录支持文件复制到自己的Xcode目录中
文件路径：/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/DeviceSupport
打开这个路径，然后看到ios 系统列表
  

![image.png](https://imgconvert.csdnimg.cn/aHR0cDovL3VwbG9hZC1pbWFnZXMuamlhbnNodS5pby91cGxvYWRfaW1hZ2VzLzEwOTU2NDMtZThjNTk0NjY1ZGUzYzA5Yi5wbmc?x-oss-process=image/format,png)  


找到自己需要的版本（我用的是11.1）将整个文件夹拷贝到自己的Xcode目录中
