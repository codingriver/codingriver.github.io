---
title: "unity优化-相同模型的多个实例设置各自的颜色优化"
date: "2020-12-13"
tags:
  - Unity
  - 性能优化
  - 网络
  - Shader
  - CSharp
categories:
  - u3d
comments: true
---
# unity优化-相同模型的多个实例设置各自的颜色优化

> 转自：[MaterialPropertyBlock](https://blog.csdn.net/liweizhao/article/details/81937590)

设置多个相同模型的各自颜色一般是设置材质球颜色时如
```csharp
gameObject.GetComponent<MeshRenderer>().material.color=Color.red;
```
这样会产生新的material实例，可以通过profile观察到，drawcall增加；

==优化方案==：
- **设置顶点颜色(需要shader的顶点着色器支持)**
```csharp
gameObject.GetComponent<MeshFilter>().mesh.colors
```
- **通过设置MaterialPropertyBlock来设置多个模型的各自颜色（简单方便）**
```csharp
            MaterialPropertyBlock mpb = new MaterialPropertyBlock();
            gameObject.GetComponent<MeshRenderer>().GetPropertyBlock(mpb);
            mpb.SetColor("_Color", Color.red);
            gameObject.GetComponent<MeshRenderer>().SetPropertyBlock(mpb);
```

==详细内容参考 [MaterialPropertyBlock](https://blog.csdn.net/liweizhao/article/details/81937590)==

