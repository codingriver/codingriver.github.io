
---
title: "SVN-trunk(主线)-branch(分支)-创建和合并教程"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["SVN"]
categories: ["随笔"]
---

<!--more-->


>文章：[SVN trunk(主线) branch(分支) tag(标记) 用法详解和详细操作步骤](http://blog.csdn.net/vbirdbest/article/details/51122637)

这里做一些补充:
#####1.从trunk创建一个branch分支
在svn上创建branchs目录


![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-54041b4316358c6a.png)  

在trunk上的Majiang上右键


![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-db5f9008e1c6dea7.png)  

**To path填写分支的名字在branchs下**


![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-04c551778ab30a74.png)  

点击ok就创建分支完成，Tag版本也是这么操作，把branchs换成Tag就可以了
#####2.从trunk合并到branch
**从分支Cache上右键**


![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-a9781a60f3b4bfb1.png)  




![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-268788118fb4c7df.png)  




![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-ed796045925cc388.png)  

*这里选择all revisions 是将从分支建立的时候到主干现在所有的修改都合并到分支上*
*这里选择specific range 是将选择指定的Revision号的提交合并到分支上*


![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-a3d6d96e628c2f28.png)  

***Test Merge** 选项表示测试Merge合并，可以提前测试检查合并中是否有冲突*
****
**合并完成后所有的修改都在本地了，解决冲突然后提交就可以了，如果合并要放弃则执行 ***Clean Up*** 操作**
****
#####3.从branch合并到trunk
同上，这里略过了
