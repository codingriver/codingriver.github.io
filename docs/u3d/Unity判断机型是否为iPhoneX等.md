---
title: "Unity判断机型是否为iPhoneX，iPhoneXS，iPhoneXR，以及iPhoneXS Max"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Unity"]
categories: ["Unity"]
---

<!--more-->

## 原生iOS常用的判断方法
iOS中判断机型的方式通常是利用屏幕分辨率，导航栏尺寸，是否支持某些功能特性等进行判断。

例如获取屏幕宽高：
```oc
CGFloat screenWidth = [UIScreen mainScreen].bounds.size.width;
CGFloat screenHeight = [UIScreen mainScreen].bounds.size.height;
```

## Unity中通过device model判断
unity中通常获取iPhone设备的device model来进行机型判断，iPhoneX以后的设备判断方法如下：
```csharp
bool IsIphoneXDevice = false;
	string modelStr = SystemInfo.deviceModel;
#if UNITY_IOS
    // iPhoneX:"iPhone10,3","iPhone10,6"  iPhoneXR:"iPhone11,8"  iPhoneXS:"iPhone11,2"  iPhoneXS Max:"iPhone11,6"
    IsIphoneXDevice = modelStr.Equals("iPhone10,3") || modelStr.Equals("iPhone10,6") || modelStr.Equals("iPhone11,8") || modelStr.Equals("iPhone11,2") || modelStr.Equals("iPhone11,6");
#endif
```
### 不同机型对应的model如下：

iPhoneX: “iPhone10,3”, “iPhone10,6”
iPhoneXR: “iPhone11,8”
iPhoneXS: “iPhone11,2”
iPhoneXS Max: “iPhone11,6”
维基百科中有最新的iPhone设备model表可查看：
https://www.theiphonewiki.com/wiki/Models

--------------------- 
>参考文章：
>原文：https://blog.csdn.net/cordova/article/details/82945154 
>