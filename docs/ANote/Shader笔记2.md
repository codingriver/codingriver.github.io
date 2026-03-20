---
title: "Shader笔记2"
subtitle: "Shader笔记2"
date: 2021-04-11T09:22:48+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
draft: true
tags: ["shader","笔记"]
categories: ["shader","笔记"]
---

<!--more-->



## 渲染相关问题（Problem）
- [x] BRDF
- [x] GPU Instancing
- [x] SRPBatcher
- [ ] Shadow,联级阴影

## tex2Dproj和tex2D的区别
> ref [tex2Dproj和tex2D的区别](https://zhuanlan.zhihu.com/p/107627483)
tex2Dproj和tex2D这两个功能几乎相同。

唯一的区别是，在对纹理进行采样之前，tex2Dproj将输入的UV xy坐标除以其w坐标。这是将坐标从正交投影转换为透视投影。

例如 以下段代码的返回值是相同的.

`float existingDepth01 = tex2Dproj(_CameraDepthTexture, UNITY_PROJ_COORD(i.screenPosition)).r;`


`float existingDepth01 = tex2D(_CameraDepthTexture, UNITY_PROJ_COORD(i.screenPosition.xy / i.screenPosition.w)).r;`


>具体什么情况下使用tex2Dproj呢?  
>我们知道,裁剪空间的坐标经过缩放和偏移后就变成了(0,ｗ),而当分量除以分量W以后,就变成了(0,1),这样在计算需要返回(0,1)值的时候,就可以直接使用tex2Dproj了.

## 深度图基础及应用
> ref [Unity Shader - 深度图基础及应用](https://www.jianshu.com/p/80a932d1f11e)  
> ref [神奇的深度图：复杂的效果，不复杂的原理](https://zhuanlan.zhihu.com/p/27547127?refer=chenjiadong)  
>  章节：*ShaderLearn-CS61*


- [x] 渲染深度图
- [x] 相交高亮  
- 能量场
- [x] 全局雾效
- [x] 扫描线
- 水淹
- [x] 垂直雾效
- 边缘检测
- 运动模糊
- 景深
- [x] 透过墙壁绘制背后的“人影”



## Depth实现特效实现概览

### DepthTextureMode.Depth
 深度会被保存在 `_CameraDepthTexture` 中，可以通过screenpos坐标来获取贴图中的值，然后使用 `UNITY_SAMPLE_DEPTH` 宏来提取深度（经常指向r通道）。

需要注意的是，深度纹理使用了与阴影投射（shadow caster）相同的Shader pass，所以如果一个对象不支持阴影投射，那么它将不会出现在深度纹理当中，并且只有RenderQueue小于等于2500的对象才能被渲染到深度纹理当中去。

```c
    float2 uv = i.uv;
    float depth = UNITY_SAMPLE_DEPTH(tex2D(_CameraDepthTexture, uv));
```

### DepthTextureMode.DepthNormals

带有`Normals`和`depth` 的的32位贴图，`Normals`根据`Stereographic projection`编码到`R&G`通道，`Depth`通过映射编码到 `B&A` 通道。Unity ShaderLab也提供`DecodeDepthNormal` 方法进行解码，其中深度是0~1范围。

`Normals & Depth Texture` 是通过 `Camera Shader replacement` 实现，可以将`RenderType`为：Opaque、TransparentCutout、TreeBark、TreeLeaf、TreeOpaque、TreeTransparentCutout、TreeBillboard、GrassBillboard、Grass类型才会进行深度渲染，对于`Transparent\AlphaTest`是不会渲染到这个纹理中。详情可参考：[浅析Unity shader中RenderType的作用及_CameraDepthNormalsTexture](https://blog.csdn.net/mobilebbki399/article/details/50512059)

在使用中，需提前定义 `_CameraDepthNormalsTexture` ，使用`DecodeDepthNormal`解码，需要注意的是：深度是0~1范围，和`_CameraDepthTexture` 有区别。

```c
	float2 uv = i.uv;
    half depth;
    half3 norm;
    DecodeDepthNormal(tex2D(_CameraDepthNormalTexture, uv), depth, norm);

```

### 入门版水面实现
- 使用相机做一张反射图，使用屏幕坐标作为UV进行采样
- 使用水的法线做出双层法线然后相加得出世界空间法线
  
- 用计算出的法线除以投影空间下的w（z值），做出近大远小的法线扰动（z值越远越大，作为被除数使得法线近大远小）然后和采样UV相加进行UV扰动
- 增加水底使用视差贴图
- 增加阳光照到水面BlinBlin闪闪的效果（将HDR部分扣除使用Bloom）
  
### 升级版海边
> CS18
1. 水体颜色(Water color)
3. 镜面反射（高光）
3. 折射/水底(Refrection)
4. 焦散
4. 海浪（Wave）
5. 岸边泡沫(Foam)
6. 水体运动（顶点动画）

## 第十五章 天空和水面
- [x] 采样纹理颜色后进行减法操作，减2，然后取大于0的值， 