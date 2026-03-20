
---
title: "Unity中获取依赖信息出现其他未引用字体问题"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Unity"]
categories: ["Unity"]
---

<!--more-->


>参考文章: [Unity中字体名对依赖关系的影响](https://blog.uwa4d.com/archives/2249.html)



**第一种方法是修改fontName,这种可以,亲测（导出要选择【版本重新生成】否则无效）且必须重启unity**
方法一：用FontCreator修改FontName
使用了FontCreator（9.1）修改FontName，步骤如下：
1）用FontCreator打开PKCommonFont.ttf文件后，通过【字体】【属性】打开属性面板。
2）切换到【扩展】页签，修改【字体族】为“PKCommonFont（【识别】的【字体族】也可以）”。
3）导出：【文件】【导出字体为】选择TrueType字体，字体名称选择【版本重新生成】，导出
PKCommonFont2.ttf。


![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-8d60cf8e526de178.png)  




![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-e8f7de0f54de6df9.png)  



![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-3dfabd7b44ec4465.png)  


**如果是替换字体文件则需要将meta文件中的【fontName】和【fontNames】都修改掉**



![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-a072f97d708eea39.png)  



![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-25eb612e71192edd.png)  



![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-62e35b49fa558e56.png)  



**这里是将字体文件对应的meta文件中的  fallbackFontReferences对应的数据改为空（这种方法有时候无效）**


![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-0f980b43130df74c.png)  



![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-99812059bd3a1e84.png)  

