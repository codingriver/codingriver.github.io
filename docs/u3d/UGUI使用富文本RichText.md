
---
title: "UGUI使用富文本RichText"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
toc: false
tags: ["UGUI"]
categories: ["Unity"]
---

<!--more-->


>  参考文章：<https://www.cnblogs.com/slysky/p/4301676.html>  
>  参考文章：<https://docs.unity3d.com/Manual/StyledText.html>  
>    [Unity Text 插入超链接](https://blog.csdn.net/akof1314/article/details/49077983)  
>    [Unity Text 插入图片](https://blog.csdn.net/akof1314/article/details/49028279)  



|名字|标签|例子|
|:-:|:-:|:-:|
|加粗|**b**|\<b>TestTest\</b>|
|倾斜|**i**|\<i>TestTest\</i>|
|大小|**size**|<size=40>TestTest</size>|
|颜色|**color**| <color=#00ffffff>TestTest</color>|
|材质|**material**| <material=1>TestTest</material>|

**material**

这只是使用textmeshes呈现一段文本，这个材料通过所指定的参数设定。值是索引在text meshes数组中的材料，检查器inspector中的。

        We are <material=2>texturally</material> amused

**quad**

这只是使用文本网格并呈现图像与内联文本。它采用参数，指定material，使用的图像，图像的高度（以像素为单位）和表示要显示的图像的一个矩形区域。不同于其他标签tags，quad不会围绕着一段文字，所以没有结束标记-斜杠字符放在结尾，以指示它是"自闭"。

```
<quadmaterial=1 size=20 x=0.1 y=0.1 width=0.5 height=0.5 />
```

这选择材料在renderer’s material数组中的位置，并将图像的高度设置为 20 像素。矩形区域的图像开始得到的 x、 y、宽度和高度值，都被赋予了作为未缩放宽度的一小部分和纹理的高度。

> UGUI Text换行问题可以参考 [UGUI Text换行问题]({{<ref "UGUI-Text换行问题.md">}})