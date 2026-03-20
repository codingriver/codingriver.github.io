---
title: "Sourcetree基本使用教程"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: [""]
categories: ["随笔"]
---

<!--more-->

>sourcetree使用，给策划同学和美术同学准备的文档，只有基础功能介绍
>版本：2.5.5.0（windows）


###  0X01 Clone项目	
打开sourcetree后是这样的，如果有项目了先点击+号
**1.点击Clone**  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120134715905.png)  


**2.配置克隆项目的信息**
位置1处添加远程项目git路径。
程序：`http://10.113.4.228:10010/r/Client.git`
美术：`http://10.113.4.228:10010/r/Art.git`
策划：`http://10.113.4.228:10010/r/Document.git`
位置2处添加需要将项目保存的本地文件夹。

  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120134833835.png)  



点击高级选项
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/2018112013500386.png)  

检出分支处，根据项目情况选择
*我们这里策划和美术项目不需要修改，用默认的master分支；程序项目选择develop分支*
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120135038867.png)  

然后点击克隆
**3.下载项目中**

  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120135244470.png)  

**4.提示框配置邮件信息**
这里邮件只是为了显示日志用，不会真的给你发邮件
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120135259583.png)  

**5.完成**

###  0X02 提交和更新项目	
**1.更新项目，选择拉取**
*这里更新是整个项目更新，和svn不一样，不区分目录更新，用svn习惯的同学需要注意下*
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120135727283.png)  


**2.提交修改**
第一步先暂存要提交的内容
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120135917141.png)  


第二步提交暂存的内容，备注提交日志，需要先勾选推送，然后点击提交，就完成了
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120140006727.png)  

==注意每次提交前尽量先更新下==
###  0X03 解决冲突	

冲突的原因是有同学修改一个文件并且提交了，你没有更新的情况下也修改了这个文件，这时候更新时提示冲突
#### 第一种情况，提交后推送失败，更新后合并冲突
**1.更新失败，提示有冲突文件**
*这里是cs文件*
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120141517606.png)  


**2.将冲突的文件先提交上去，会提示推送失败，不管它**
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120144831429.png)  


**3.再次拉取**

  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120144859667.png)  


**4.拉取后有冲突**
感叹号图标表示冲突
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120144922880.png)  

**5.解决冲突**
根据自己情况选择解决方案，选中冲突文件右键
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120145013854.png)  

  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120145040867.png)  


解决冲突后，感叹号没有了
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120145049813.png)  


然后提交，不要做其他操作，先提交，日志是默认冲突日志，不用管（如果有其它文件需要提交，也不要管，先把冲突文件提交上去，再重新提交需要提交的文件）

解决冲突后有可能出现orig后缀文件，直接删除就行，冲突备份用的
如果还提示推送，点击推送按钮就好了
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181120150515699.png)  



#### 第二种情况，本地修改没提交，更新提示冲突
**1.更新失败提示**
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181121142304428.png)  

**2.解决方案**
将自己修改的文件备份，然后黄色或者灰色图标的丢弃修改，问号图标的移除
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/2018112114250917.png)  

  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181121142533218.png)  

更新完成后再覆盖，然后提交



>这里注意下，文件冲突不管是不是同一行都会提示冲突，没有自动合并，应该和冲突比对工具有关，这里不做说明了，svn如果修改不是同一行自动合并
>git不会去管理文件夹，unity的meta文件让这个问题很蛋疼

###  0X04 基本知识	

**1.当前项目所在文件夹目录**
点击浏览器会打开项目所在的文件夹
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181121120056273.png)  


**2.文件图标说明**
新添加文件
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181121120704641.png)  

如果删除这个文件选移除
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181121120731434.png)  


修改的文件
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181121120902108.png)  

放弃本地修改选择丢弃
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181121120931941.png)  

删除的文件
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181121124036453.png)  


  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181121124054319.png)  

放弃删除，选择丢弃，就恢复了
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181121124120719.png)  


还有一种图标是更换目录
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181121130121168.png)  



>如果还不明白或者想要更详细的资料，这里推荐几篇文章
>[iOS-SourceTree的使用](https://www.jianshu.com/p/70d8dafd4b55) (解决冲突参考)
>[SourceTree图文示例教程（Win版）](https://zhuanlan.zhihu.com/p/37253726)
>[SourceTree使用方法](https://blog.csdn.net/u012230055/article/details/64125268/)