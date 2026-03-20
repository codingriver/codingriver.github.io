---
title: "Shader学习 1"
subtitle: "Shader学习 1"
date: 2021-02-09T07:55:48+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
draft: true
tags: [“Shader学习”]
categories: [“Shader”]
---

<!--more-->
### Unity 渲染管线
  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/Shader学习-1.1基础概要/20210209075913.png)  
  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/Shader学习记录/20210208172515.png)  
  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/Shader学习记录/20210208174407.png)  
  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/Shader学习记录/20210208192111.png)  
  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/Shader学习记录/20210208192548.png)  

  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/Shader学习-1.1基础概要/20210209080530.png)  
![20210208200542](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/Shader学习记录/20210208200542.png)


> 增加一个pass提取深度值，怎么确定哪个pass先执行？
>  uv动画，模型的阴影不能跟随变化

>Unity Shader说明链接：  
>[Unity Shader基础示例](https://docs.unity3d.com/cn/current/Manual/SL-VertexFragmentShaderExamples.html)  
>[unity Shader属性（材质球属性）](https://docs.unity3d.com/cn/current/Manual/SL-Properties.html)  
>[unity Shader自定义属性（材质球自定义属性）](https://docs.unity3d.com/cn/current/ScriptReference/MaterialPropertyDrawer.html)  
>[Shader面板上常用的一些内置Enum](https://zhuanlan.zhihu.com/p/93194054)  
>[Unity Shader内置变量](https://docs.unity3d.com/cn/current/Manual/SL-UnityShaderVariables.html)  
>[Unity Shader内置函数](https://docs.unity3d.com/cn/current/Manual/SL-BuiltinFunctions.html)  
>[Unity Shader内置 include 文件](https://docs.unity3d.com/cn/current/Manual/SL-BuiltinIncludes.html)  
>[Unity Shader子着色器标签](https://docs.unity3d.com/cn/current/Manual/SL-SubShaderTags.html)  
>[Unity Shader通道标签](https://docs.unity3d.com/cn/current/Manual/SL-PassTags.html)  