
---
title: "ios配置开发者证书及添加AppID"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["IOS"]
categories: ["IOS"]
---

<!--more-->
>原文： [**ios配置开发者证书及添加AppID**](https://www.jianshu.com/p/ee83dc090b20)

**一. 有两种配置开发者证书的方法**
## 第一种，通用的并且复杂的一种
##  0X01 创建请求证书的请求文件
  1.打开钥匙串


![开发者证书请求文件1.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-3c1099f5a8c6b7f0.png)  



2

![开发者证书请求文件2.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-87d16259a7fd86ad.png)  




![开发者证书请求文件3.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-9162cd518a4824f4.png)  

2.创建请求文件



![开发者证书请求文件4.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-a179cd60b065d1ae.png)  

打开：*钥匙串访问===>证书助理===>从证书颁发机构请求证书...*



![开发者证书请求文件5.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-28c509ebed45a12f.png)  

请求是：*存储到磁盘*
*设置电邮地址*
点击继续


![开发者证书请求文件6.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-4f7c1d6eb8791e83.png)  

存储请求文件
##  0X02 创建开发证书
1.打开https://developer.apple.com 点击Account 登录

![[图片上传中...(创建开发者证书2.png-c69c56-1517639491122-0)]
](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-f017dfd4c9ea901a.png)



![创建开发者证书2.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-2b64c98e0c19c5e4.png)  




![创建开发者证书3.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-425ddfe1e5281860.png)  


点击：*Certificates, Identifiers & Profiles*


![创建开发者证书4.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-1b4524e663b64ebf.png)  

点击Certificates 的+号，准备创建开发者证书


![创建开发者证书5.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-9f3d59546a22ffd0.png)  

这里根据自己的需求选择开发证书还是生产证书（如果是自己测试可以选择Development开发证书，如果发布appstore提审，则需要Production生产证书）



![创建开发者证书6.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-400d94cbef0fc850.png)  

*拖到屏幕最下面，选择继续*



![创建开发者证书7.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-53c8dfc36a1285e3.png)  

*选择继续*


![创建开发者证书8.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-8ed297c64eb13a77.png)  

*这里选择刚才生成的创建开发者证书的请求文件*


![创建开发者证书9.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-d36cf6cbfbb2fd74.png)  



![创建开发者证书10.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-1cfff855cb956cf8.png)  

*选择继续*


![创建开发者证书11.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-c2ed8e152fc833bb.png)  

*这里选择下载，证书已经配置完成，下载到本地,然后点击Done*

**证书下载完成后双击自动导入证书，检查证书是否成功导入!**
[创建开发者证书12.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-90bf059efbd967be.png)

**我之前在创建证书请求文件时配置的常用名称wang_develop 这里看到表示成功了**

## 第二种，通过Xcode配置，（我这里是Xcode9.2，Xcode8.0及以上都可以）
1.打开Xcode，这里就不说怎么打开了
2.点击左上角Xcode按钮===>Preferences...


![创建开发者证书21.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-47911c2aa385a337.png)  

3. 点击 *Accounts* 选择自己apple账户，然后点击 * Manage Certificates*


![创建开发者证书22.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-e60370cfb454a271.png)  


4.点击+号


![创建开发者证书23.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-766b45adcc0bc4eb.png)  


*这里点击+号后展开菜单有Development和App Store*（这里根据自己的需求选择开发证书还是生产证书（如果是自己测试可以选择Development开发证书，如果发布appstore提审，则需要App Store生产证书））
*等待证书添加完成*


![创建开发者证书24.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-0dc121553d666943.png)  

这里证书添加完成，然后重启Xcode，防止出现未知bug

#二.  添加AppId
打开开发者账户网站（上面网页中配置证书的地方）
1.App IDs==>+号
选择左侧的appIds


![配置开发者AppID-1.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-6fa59263807032c8.png)  

2.


![配置开发者AppID-2.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-3b6dded1164aac38.png)  

添加AppId的名字和BundleID
点击继续，（在屏幕最下面）
3.选择选项点击继续


![配置开发者AppID-3.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-d0ce20fcc5961fa9.png)  


4.点击*Register*完成


![配置开发者AppID-4.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-f7b559b6ce9b9753.png)  






