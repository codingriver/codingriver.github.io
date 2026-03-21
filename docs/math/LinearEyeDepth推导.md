---
title: "LinearEyeDepth推导"
date: "2026-03-21"
tags:
  - 数学
  - 图形学
  - 网络
  - Shader
  - CSharp
categories:
  - math
comments: true
---
# LinearEyeDepth推导

>转自 冯乐乐 《unity shader 入门精要》 :<https://blog.csdn.net/linuxheik/article/details/79446780/>


Unity 从`相机空间` 通过透视投影变换（裁剪矩阵）后到`裁剪空间`，然后通过透视除法变换到归一化的设备坐标（Normalized Device Coordinates, `NDC`）,然后转换到视口坐标 。

z 分量从ndc [-1,1]到屏幕坐标[0,1]的映射方法：  
    ![20210424154055](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/LinearEyeDepth推导/20210424154055.png)

*其中，d对应了深度纹理中的像素值，Z<sub>ndc</sub>对应了NDC坐标中的z分量的值。*



透视变换
  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/透视投影变换推导/20210424144836.png)  

正交变换
  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/LinearEyeDepth推导/20210424151036.png)  


## 推导

> 参考:[透视投影变换推导](透视投影变换推导.md) , [屏幕空间变换](屏幕空间变换.md) 


根据前面**透视投影变换推导**和**屏幕空间变换**，我们使用透视投影的裁剪矩阵P<sub>clip</sub>对相机空间下的一个顶点进行变换，裁剪空间下顶点的z分量和w分量分别为：
  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/LinearEyeDepth推导/20210424154025.png)  

其中，Far 和 Near 分别是远近裁剪平面的距离。然后，我们通过齐次除法就可以得到NDC下的z分量：
  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/LinearEyeDepth推导/20210424154041.png)  

之前我们知道，深度纹理中的深度值是 通过下面的公式由NDC计算而得的：
  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/LinearEyeDepth推导/20210424154055.png)  

由上面的这些式子，我们可以推导出用d表示而得的Z<sub>visw</sub>的表达式：

> d=0.5((f+n)/(f-n) +2nf/((f-n)z))+0.5
> 
> d-0.5=0.5((f+n)/(f-n) +2nf/((f-n)z))
> 
> 2d-1=((f+n)/(f-n) +2nf/((f-n)z))
> 
> 2d-1=(((f+n)z +2nf)/((f-n)z))
> 
> (f+n)z+2nf=(2d-1)(f-n)z
> 
> (2d-1)(f-n)z-(f+n)z=2nf
> 
> ((2d-1)(f-n)-(f+n))z=2nf
> 
> z=2nf/((2d-1)(f-n)-(f+n))
> 
> z=2nf/(2d(f-n)-(f-n)-(f+n))
> 
> z=2nf/(2d(f-n)-2f)
> 
> z=nf/(d(f-n)-f)
> 
> z=1/((f-n)d/(nf)-1/n)
  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/LinearEyeDepth推导/20210424155107.png)  

由于在Unity使用的视角空间中，摄像机正向对应的z值均为负值，因此为了得到深度值的正数表示，我们需要对上面的结果取反，最后得到的结果如下：
  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/LinearEyeDepth推导/20210424155739.png)  

它的取值范围就是视锥体深度范围，即[Near,Far]。如果我们想要得到范围在[0, 1]之间的深度值，只需要把上面得到的结果除以Far即可。这样，0就表示该点与摄像机位于同一位置，1表示该点位于视锥体的远裁剪平面上。结果如下：
  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/LinearEyeDepth推导/20210424155757.png)  

运的是，Unity提供了两个辅助函数来为我们进行上述的计算过程 `LinearEyeDepth` 和 `Linear01Depth`:
- `LinearEyeDepth` 负责把深度纹理的采样结果转换到视角空间下的深度值，也 就是我们上面得到的Z<sub>visw</sub>。
-  `Linear01Depth` 则会返回一个范围在[0, 1]的线性深度值，也就是我们上面得到的Z<sub>01</sub>，这两个函数内部使用了内置的 `_ZBufferParams` 变量来得到远近裁剪平面的距离。

`LinearEyeDepth` 方法和 `Linear01Depth` 方法：
```shader

// Z buffer to linear depth
inline float LinearEyeDepth( float z )
{
return 1.0 / (_ZBufferParams.z * z + _ZBufferParams.w);
}


// Z buffer to linear 0..1 depth (0 at eye, 1 at far plane)
inline float Linear01Depth( float z )
{
return 1.0 / (_ZBufferParams.x * z + _ZBufferParams.y);
}


//其中_ZBufferParams的定义如下：
//double zc0, zc1;
// OpenGL would be this:
// zc0 = (1.0 - m_FarClip / m_NearClip) / 2.0;
// zc1 = (1.0 + m_FarClip / m_NearClip) / 2.0;
// D3D is this:
//zc0 = 1.0 - m_FarClip / m_NearClip;
//zc1 = m_FarClip / m_NearClip;
// now set _ZBufferParams with (zc0, zc1, zc0/m_FarClip, zc1/m_FarClip);

```
- `_ZBufferParams` 参数：`(1-Far/Near, Far/Near, x/Far, y/Far)`

## 使用

```
```