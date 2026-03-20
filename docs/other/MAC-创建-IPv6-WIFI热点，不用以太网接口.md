
---
title: "MAC-创建-IPv6-WIFI热点，不用以太网接口"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["IOS","Ipv6"]
categories: ["随笔"]
---

<!--more-->


1.需要两个ios手机（一个测试机，一个提供网络热点的）
2.需要mac一台，可以没有以太网，可以不联网

**共享热点:使mac可以上网**
1.使用usb连接mac电脑
2.打开ios设置-->个人热点-->打开，会提示**仅蓝牙和USB**上网（没有提示则把wifi关闭再试，选择后也可以把wifi打开使用wifi给mac上网）
3.测试mac 上网，打开浏览器随便打开个网站，确认网络可用

**创建IPV6 wifi热点**
点击桌面左上角小苹果--->系统偏好设置---->共享（要按住option键）


![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-6d923750c7d3d08b.png)  





![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-a844a61e7155848b.png)  


**共享一下来源的连接：**这里使用USB(如果有以太网就选择以太网)
**共享给电脑：**选择Wi-Fi
**创建NAT64网络选项：**一定要勾上，就靠它来共享NAT64网络
wifi选项---频段 ---- 我这里选择的11
勾上互联网共享就可以了


![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-2d8ebfda4a1d6952.png)  


**打开共享如果不按住option，则打开的共享面板没有【创建NAT64网络选项】**


手机的dns就是ipv6的地址，就ok了
