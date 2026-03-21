---
title: "shader记录"
date: "2026-03-21"
tags:
  - 随笔
  - 笔记
  - Git
  - 网络
  - Shader
categories:
  - ANote
comments: true
---
# shader记录

[如何开始用 C++ 写一个光栅化渲染器？](https://www.zhihu.com/question/24786878/answer/1483055155)

bilibili的 [GAMES101-现代计算机图形学入门-闫令琪](https://www.bilibili.com/video/BV1X7411F744?from=search&seid=13728008737010812958)

[庄懂-BoyanTata](https://space.bilibili.com/6373917) 
- [ ]    第二节没有完成 （屏幕空间使用，及素描风格）


[庄懂公开课资源](https://github.com/BoyanTata/AP01)

### 学习课程中的问题

- [ ] z缓冲消隐算法 (投影矩阵提到)


- [ ] Mapcap昆虫最后的颜色为啥是相乘和相加？（第一章第四节）

- [ ] 视差贴图，视差映射 ，视差偏移没有仔细学习（第二章第二节）。
- [ ]  绕y轴旋转的旋转矩阵怎么写是对的，需要和unity Transform旋转一致（第三章第一节 Cubemap旋转）
    ><https://wgqing.com/unity%E7%9F%A9%E9%98%B5%E5%8F%98%E6%8D%A2%E4%BB%8E%E6%A8%A1%E5%9E%8B%E7%A9%BA%E9%97%B4%E5%88%B0%E5%B1%8F%E5%B9%95%E7%A9%BA%E9%97%B4%E7%9A%84%E8%BD%AC%E6%8D%A2/>

- [ ] 次表面散射，Skin_LUT （第四章第二节），皮肤阴影区域的SSS效果调整不理想
- [ ] 屏幕后处理，添加玻璃破碎效果，屏幕适配失败，不同分辨率时破碎效果不能保持居中（第五章第一节第二课题，BrokenGlass）
- [ ] 火焰形状扰动后输出异常 （第六章第一节）
- [ ] 动画纹理（VAT）,（第六章第三节），*(需要Hodini)*
- [ ] FlowMap的意义，案例中使用FlowMap没有看出效果在哪,（第六章第三节）
- [ ] 宝石自发光，光晕效果（第八章）


### 水体渲染

1. 水体颜色
    - 根据水底的深度计算（获取深度图）区分浅水区和深水区得到颜色
1. 反射
    - 根据PlanarReflection获取 _ReflectionTex纹理，然后使用屏幕空间作为UV进行采样（使用水的法线贴图进行扰动uv），得到反射颜色；增加菲涅尔效果
1. 折射/水底
    - 使用grabPass获取屏幕颜色，然后使用屏幕空间作为UV进行采样（使用水的法线贴图进行扰动UV），得到折射的颜色
1. 焦散
    - 使用深度还原的世界坐标作为UV采样焦散纹理，采样两次取两次的最小值 （应该可以使用默认UV进行采样）
1. 岸边泡沫
    - 使用根据time使用sin波向岸边推送波浪模拟的泡沫，使用一个noise进行扰动，需要处理遮罩 保证只在岸边有泡沫
1. 波浪（Wave）（顶点动画）
    - 正弦/余弦
    - 格斯特纳波（Gerstner）