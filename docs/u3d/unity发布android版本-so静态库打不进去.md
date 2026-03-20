
---
title: "unity发布android版本-so静态库打不进去"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Unity","Android"]
categories: ["Unity"]
---

<!--more-->


发布android包时 armeabi文件夹下的so静态库打包不进去（unity版本：unity5.6.0f3）


![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-9bf9d1be22a42b47.png)  


检查so文件对应的meta文件
```
fileFormatVersion: 2
guid: 4df0d61d0843d4914a5dcd11225fdd84
timeCreated: 1513074069
licenseType: Pro
PluginImporter:
  serializedVersion: 2
  iconMap: {}
  executionOrder: {}
  isPreloaded: 0
  isOverridable: 0
  platformData:
    data:
      first:
        Android: Android
      second:
        enabled: 0
        settings: {}
    data:
      first:
        Any: 
      second:
        enabled: 0
        settings: {}
    data:
      first:
        Editor: Editor
      second:
        enabled: 0
        settings:
          DefaultValueInitialized: true
  userData: 
  assetBundleName: 
  assetBundleVariant: 


```
能打包so静态库到包里面的meta文件配置
```
fileFormatVersion: 2
guid: d942bd3bc664af74a902489cf22548ed
timeCreated: 1513426642
licenseType: Pro
PluginImporter:
  serializedVersion: 2
  iconMap: {}
  executionOrder: {}
  isPreloaded: 0
  isOverridable: 0
  platformData:
    data:
      first:
        Android: Android
      second:
        enabled: 1
        settings:
          CPU: ARMv7
    data:
      first:
        Any: 
      second:
        enabled: 0
        settings: {}
    data:
      first:
        Editor: Editor
      second:
        enabled: 0
        settings:
          DefaultValueInitialized: true
  userData: 
  assetBundleName: 
  assetBundleVariant: 

```
在CPU选项选择ARMv7后我的meta文件的CPU对应数据是空的(上面的数据是对的，可以和自己的对比下)，但是界面显示


![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-c4f7b9db6f1c7ca4.png)  

所以有时候unity 的meta文件和unity工程打开的显示不一样，打包的时候以meta信息为主。
应该是unity的bug
