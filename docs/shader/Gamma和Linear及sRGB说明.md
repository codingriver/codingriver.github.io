---
title: "Gamma和Linear及sRGB说明"
subtitle: "Unity Linear Gamma色彩空间矫正测试"
date: 2022-03-09T10:44:08+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
# draft: true
tags: ["shader"]
categories: ["shader"]
---

<!--more-->
>**Gamma校正**: 
>所谓Gamma校正就是对颜色进行指数运算。对图像进行Gamma校正（gamma = 1/2.2 = 0.4545454…）是为了在存储空间有限的情况下，提高符合人眼特性的可辨识精度。由于硬盘存储的图像是经过Gamma校正的，因此显示器显示图片时，需要做一次逆Gamma校正（gamma = 2.2）——也就是说，所有显示器都期待软件输出的图片是经过Gamma校正的。至于为什么这个值是2.2，由于历史惯用，Gamma值=2.2已成为业界标准。
>
> Unity中sRGB(Color Texture)选项说明：  
>sRGB (Color Texture)        启用此属性可指定将纹理存储在伽马空间中。对于非 HDR 颜色纹理（例如反照率和镜面反射颜色），应始终选中此复选框。如果纹理存储了有特定含义的信息，并且您需要着色器中的确切值（例如，平滑度或金属度），请禁用此属性。默认情况下会启用此属性。
### unity中测试结果：

1. Gamma space，开不开sRGB都没有影响
2. Linear space，gamma texture 勾选sRGB
3. Linear space，linear texture 不勾sRGB （这个是没有测试的，推断的）

### unity中测试过程：

外部导入一张gamma texture贴图：  
![](../images/gammatest.jpg)
*ps导出的gamma空间的图片*  

外部导入一张linear texture贴图：  
![](../images/lineartest.jpg)
*ps导出的linear空间的图片*  
1. unity 使用 Gamma Space 勾不勾sRGB都没有影响
2. unity 使用 Linear Space
    1. 使用 gamma texture 勾选sRGB
    ![](../images/2022-03-09-16-29-13.png)  
        > 在Linear Space下，如果勾了sRGB 之后，Unity是做了Remove Gamma Correction
    1. 使用 gamma texture 不勾选sRGB
    ![](../images/2022-03-09-16-29-43.png)  
    1. 使用 linear texture 勾选sRGB
    ![](../images/2022-03-09-17-28-49.png)  
    *这个是错误的，不能勾选sRGB,这个效果和ps中显示是一样的*
    1. 使用 linear texture 不勾选sRGB    
    ![](../images/2022-03-09-17-29-09.png)

**对于测试纹理勾选sRGB后再内存中的格式是RGB8_sRGB,对于这种_SRGB后缀的格式，GPU在进行纹理采样的时候，会自动将其移除GamaCorrection，即将数值做2.2次幂操作，但是不会对原始数据做修改。在Gamma空间中，不论勾选还是不勾选sRGB，格式都是RGB8_UNORM。**

>注意 `public Color GetPixel(int x, int y` 方法获取纹理中间的颜色时，linear space下，不管勾不勾sRGB都是返回固定值，中间的红色位置始终返回0.996，没有定论

### Gamma工作流说明：
![](../images/2022-03-09-16-40-31.png)

gamma texture 在存储时 预先做gamma校正（0.454）,然后储存到文件（这时候纹理是被整体提亮的），文件加载读取后直接输出到屏幕时，显示器内置自动做逆gamma校正（2.2），所以看到是正常的图片。  
unity中gamma空间也是这样工作的，这时sRGB没有任何作用，如果做pbr等光照计算，需要在计算前进行逆gamma校正（2.2）回归到线性空间，然后进行光照计算，计算后的颜色需要做gamma校正（0.454）（从线性空间返回到gamma空间），输出后的颜色从显示器显示（内置逆gamma校正（2.2）） ，看到正常图片。*参与光照计算的光滑度/金属度贴图，这类存储数值信息的贴图，是线性贴图，在渲染时，它不提供色彩信息给显示器，而是提供光滑度/金属度这样的数据用以光照计算，因此0.5就是0.5，不需要sRGB解码*



>参考：  
> <https://segmentfault.com/a/1190000040181885>  
> <https://blog.51cto.com/u_15054050/4550752>  
> <https://ciel1012.github.io/2019/06/12/ColorSpace/>  
> <https://answer.uwa4d.com/question/5f8129c29424416784ef25a1>





