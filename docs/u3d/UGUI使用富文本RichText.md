---
title: "UGUI使用富文本RichText"
date: "2026-03-21"
tags:
  - Unity
  - UI
  - 网络
categories:
  - u3d
comments: true
---
# UGUI使用富文本RichText

参考文章：

- <https://www.cnblogs.com/slysky/p/4301676.html>
- <https://docs.unity3d.com/Manual/StyledText.html>
- [Unity Text 插入超链接](https://blog.csdn.net/akof1314/article/details/49077983)
- [Unity Text 插入图片](https://blog.csdn.net/akof1314/article/details/49028279)

| 名字 | 标签 | 例子 |
|:-:|:-:|:-:|
| 加粗 | `b` | `<b>TestTest</b>` |
| 倾斜 | `i` | `<i>TestTest</i>` |
| 大小 | `size` | `<size=40>TestTest</size>` |
| 颜色 | `color` | `<color=#00ffffff>TestTest</color>` |
| 材质 | `material` | `<material=1>TestTest</material>` |

## material

这只是使用 text meshes 呈现一段文本，这个材料通过所指定的参数设定。值是索引在 text meshes 数组中的材料。

```text
We are <material=2>texturally</material> amused
```

## quad

这只是使用文本网格并呈现图像与内联文本。它采用参数，指定 material、使用的图像、图像的高度和矩形区域。

```text
<quadmaterial=1 size=20 x=0.1 y=0.1 width=0.5 height=0.5 />
```

## 相关文章

UGUI Text 换行问题可以参考：

- `UGUI-Text换行问题`
