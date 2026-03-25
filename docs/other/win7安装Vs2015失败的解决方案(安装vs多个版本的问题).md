---
title: "win7安装Vs2015失败的解决方案(安装vs多个版本的问题)"
date: "2020-12-13"
tags:
  - 工具链
  - 网络
  - CSharp
categories:
  - other
comments: true
---
# win7安装Vs2015失败的解决方案(安装vs多个版本的问题)

一开始安装vs2017时失败了，然后安装vs2015和vs2013的时候各种错误，安装不上；
是因为安装缓存（C:\ProgramData\Package Cache）的存在，指向之前的版本了，我这是一开始的vs2017的缓存，我安装vs2015时，目录存在则直接使用了，没有重新创建，所以缓存错了，
vs安装完成后 C:\ProgramData\Package Cache 下的缓存不会清理，在安装vs前先删除这个目录就好了



>参考文章
>[分享一个安装Vs2015失败的解决方案，报错为系统找不到指定路径](https://blog.csdn.net/a827443469/article/details/78619561)