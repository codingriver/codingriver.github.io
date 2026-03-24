---
title: "【Shader】常用函数（UnityShader内置函数、CG 和 GLSL 内置函数等）和内置变量"
date: "2026-03-21"
tags:
  - Shader
  - 图形学
  - CSharp
  - 数学
categories:
  - shader
comments: true
---
# 【Shader】常用函数（UnityShader内置函数、CG 和 GLSL 内置函数等）和内置变量

## 一、CG 和 GLSL 常用函数

### CG 语言中的变量修饰符

| 修饰符 | 解析 |
|:-:|:-:|
| const | 变量定义为常量后，程序中不能再对其赋值 |
| extern | 表明声明仅仅是声明，而非定义 |
| in | 作为函数或程序的输入值 |
| inline | 告诉编译器对该函数采取内联调用 |
| inout | 作为函数或程序的输入输出值 |
| static | 只在声明全局变量时使用 |
| out | 作为函数或程序的输出值 |
| uniform | 定义 constant buffers（常量缓存） |

### 1、数学函数

原文整理了大量 CG / GLSL 数学函数对照，包括：

- `ceil` / `floor`
- `frac` / `fract`
- `exp` / `log` / `pow`
- `sqrt` / `rsqrt`
- `sin` / `cos` / `tan`
- `dot` / `cross`
- `clamp` / `lerp` / `smoothstep`

### smoothstep 示例

```glsl
float smoothstep(float a, float b, float x)
{
    float t = saturate((x - a) / (b - a));
    return t * t * (3.0 - (2.0 * t));
}
```

### 2、几何函数

常见函数包括：

- `distance`
- `faceforward`
- `length`
- `normalize`
- `reflect`
- `refract`

### 3、纹理映射函数

原文整理了常见：

- `tex1D`
- `tex2D`
- `tex3D`
- `texCUBE`
- 各类 `proj`、深度比较、导数版本

### 4、偏导函数

- `ddx(a)`：近似 `a` 关于屏幕空间 x 轴的偏导数
- `ddy(a)`：近似 `a` 关于屏幕空间 y 轴的偏导数

## 二、Unity 常用内置函数、变量

### 1、Unity 常用结构体

#### 顶点着色器输入

- `appdata_base`
- `appdata_tan`
- `appdata_full`
- `appdata_img`

#### 顶点着色器输出

- `v2f_img`

```glsl
struct v2f_img
{
    float4 pos : SV_POSITION;
    half2 uv : TEXCOORD0;
    UNITY_VERTEX_INPUT_INSTANCE_ID
    UNITY_VERTEX_OUTPUT_STEREO
};
```

### 2、空间变换函数及内置变量

常见函数包括：

- `UnityWorldToClipPos`
- `UnityViewToClipPos`
- `UnityObjectToViewPos`
- `UnityWorldToViewPos`
- `UnityObjectToWorldDir`
- `UnityWorldToObjectDir`
- `UnityObjectToWorldNormal`
- `UnityWorldSpaceLightDir`
- `UnityWorldSpaceViewDir`

