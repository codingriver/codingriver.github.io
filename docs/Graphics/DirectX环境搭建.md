---
title: "DirectX环境搭建"
date: "2026-03-21"
tags:
  - 图形学
  - 网络
  - 项目记录
categories:
  - Graphics
comments: true
---
# DirectX环境搭建

>IDE支持 `DirectX11` 和 `DirectX12`

vs2019自带了DirectX，所以不要很复杂且繁琐的配置。但是如果安装的时候，没有勾选正确的包，后面就无法找到自带的DirectX。

- 启动Visual Studio Installer
- 勾选下图所示的两个安装包
    ![20210724162525](image/DirectX环境搭建/c7nYgPNMuvztEUW.png)
    *第二个安装包，如果不够选也是无法看到DirectX的。*

 - 在通用Windows平台开发中，需要勾选如下所示包
    ![20210724162607](image/DirectX环境搭建/cmoCpS2hnw7PDkU.png)
- 这样在创建项目的时候，就可以看见DirectX11了  
![](image/DirectX环境搭建/G7gmvNHyjq6S419.png)  
- 开发者模式也需要打开  
![](image/DirectX环境搭建/pd7mfIhNjDC5zVr.png)  
- 然后，运行一下模板  
![](image/DirectX环境搭建/9RNZmfIWlC2Lsoj.png)  

> ref: [https://juejin.cn/post/6916331857856430088](https://juejin.cn/post/6916331857856430088)