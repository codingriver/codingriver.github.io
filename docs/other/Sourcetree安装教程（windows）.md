---
title: "Sourcetree安装教程（windows）"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: [""]
categories: ["随笔"]
---

<!--more-->

>给美术同学和策划同学提供安装git管理软件教程

###  0X01 安装Git	
****
这里安装的git版本是2.15.0
****
**1.双击git**
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120113208417.png)  

**2.点击运行**
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120113255325.png)  


**3.点击Next**

  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120113314436.png)  


**4.点击Next，其他选项是默认就行**
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120113330903.png)  

**5.点击Next，其他选项是默认就行**
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120113404854.png)  

**6.点击Next，其他选项是默认就行**
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120113415146.png)  

**7.点击Next，其他选项是默认就行**
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120113427980.png)  

**8.点击Next，其他选项是默认就行**
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120113441432.png)  

**9.点击Next，其他选项是默认就行**
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120113500909.png)  

**10.点击Next，其他选项是默认就行**
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120113510982.png)  

**11.点击Next，其他选项是默认就行**
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120113532762.png)  

**12.点击Finish，其他选项是默认就行**
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120113547862.png)  


到这里git软件安装完成。
*这一步是为了防止sourcetree安装后要下载git软件*
###  0X02 安装Sourcetree	
==这里安装的版本是2.5.5，不需要翻墙，不需要登陆账户==
**1.双击sourceTree**
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120113719121.png)  


**2.点击运行**
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120113830948.png)  


**3.勾选我同意，点击下一步**  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120113851327.png)  


**4.点击关闭**
这里不点击下一步，下一步需要登陆账户，这里绕过账户登陆
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120113920758.png)  

**5.破解账户登陆**
==复制accounts.json文件到`%LocalAppData%\Atlassian\SourceTree\` 目录下,没有则新建==
在文件管理器中打开目录`%LocalAppData%\Atlassian\SourceTree\` 点击回车
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120114346673.png)  


  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120114025954.png)  


将accounts.json文件拷贝到该目录下
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/2018112011410246.png)  


在文章结尾附上acccounts.json文件

**6.双击Sourcetree启动**
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120114709754.png)  


**7.选择我不想使用**

  

![Sourcet](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120114737411.png)  

8.安装Sourcetree完成
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120114804270.png)  

后面补充使用教程


这里附上`accounts.json`文件
```c
[
  {
    "$id": "1",
    "$type": "SourceTree.Api.Host.Identity.Model.IdentityAccount, SourceTree.Api.Host.Identity",
    "Authenticate": true,
    "HostInstance": {
      "$id": "2",
      "$type": "SourceTree.Host.Atlassianaccount.AtlassianAccountInstance, SourceTree.Host.AtlassianAccount",
      "Host": {
        "$id": "3",
        "$type": "SourceTree.Host.Atlassianaccount.AtlassianAccountHost, SourceTree.Host.AtlassianAccount",
        "Id": "atlassian account"
      },
      "BaseUrl": "https://id.atlassian.com/"
    },
    "Credentials": {
      "$id": "4",
      "$type": "SourceTree.Model.BasicAuthCredentials, SourceTree.Api.Account",
      "Username": "",
      "Email": null
    },
    "IsDefault": false
  }
]
```

>参考文章
>[SourceTree 破解登录](https://blog.csdn.net/suwei791488323/article/details/79572221)

