---
title: "unity 中的LayerMask用法"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Unity"]
categories: ["Unity"]
---

<!--more-->

>突然发现自己忘了，尴尬

layerMask参数：

`Raycast (ray : Ray, out hitInfo : RaycastHit, distance : float = Mathf.Infinity, layerMask : int = kDefaultRaycastLayers)`

```c
            RaycastHit hit;
            Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
            if (Physics.Raycast(ray, out hit, 1000, 1<<LayerMask.NameToLayer("Ground")))
            {
                Log.Debug(" hit :" + hit.point );
            }
            else
            {
                Log.Debug("ray cast null!");
            }
```

int layer = LayerMask.NameToLayer("Ground"); //假设=10

LayerMask.GetMask(("Ground"); //相当于 1 << 10

其实很简单：

>1 << 10 打开第10的层。 等价于【1 << LayerMask.NameToLayer("Ground");】  也等价于【 LayerMask.GetMask(("Ground");】

>~(1 << 10) 打开除了第10之外的层。

>~(1 << 0) 打开所有的层。

>(1 << 10) | (1 << 8) 打开第10和第8的层。等价于【 LayerMask.GetMask(("Ground", "Wall");】


在代码中使用时如何开启某个Layers？
LayerMask mask = 1 << 你需要开启的Layers层。
LayerMask mask = 0 << 你需要关闭的Layers层。
举几个个栗子：

>LayerMask mask = 1 << 2; 表示开启Layer2。


>LayerMask mask = 0 << 5;表示关闭Layer5。


>LayerMask mask = 1<<2|1<<8;表示开启Layer2和Layer8。


>LayerMask mask = 0<<3|0<<7;表示关闭Layer3和Layer7。

上面也可以写成：

>LayerMask mask = ~（1<<3|1<<7）;表示关闭Layer3和Layer7。


>LayerMask mask = 1<<2|0<<4;表示开启Layer2并且同时关闭Layer4.


>参考文章：
>[LayerMask小结](https://www.cnblogs.com/dabiaoge/p/8980224.html)
>[Unity3D中Layers和LayerMask解析](https://www.jianshu.com/p/89d5252a8b74)