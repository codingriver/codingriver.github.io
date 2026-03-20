---
title: "【Shader】 常用函数（UnityShader内置函数、CG和GLSL内置函数等）和内置变量"
date: 2020-09-14T13:15:46+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["shader"]
categories: ["shader"]
---

<!--more-->

## 一、CG和GLSL常用函数
### CG语言中的变量修饰符

| 修饰符 | 解析 |
|:-:|:-:|
| const | 变量被定义成常量的话，在程序中，就不能再对该变量赋值，除非const和uniform，varying一起使用。const修饰的变量，需要在声明时给予一个初始值 |
| extern | extern表明声明仅仅是声明，而非定义。在程序中一定有一个地方存在一个非extern的对应的声明 |
| in | 只在声明参数，或是使用varying修饰符时使用。将参数，或是varying作为函数或是程序的输入值。函数参数如果没有in，out，或者inout的话，隐式的默认为in |
| inline | 只在函数定义时有用，告诉编译器始终对该函数采取内联调用 |
| inout | 只在声明为参数和varying时使用，将参数或是varying声明为函数或是程序的输入输出值 |
| static | 只在声明全局变量时使用，static将使变量对程序而言成为私有的，外部不可见，不能和uniform，varying一起使用 |
| out | 只在声明参数和varying时使用，将变量或varying定义为函数或是程序的输出值 |
| uniform | 用于全局变量和程序的入口函数的参数，用来定义constant buffers(常量缓存)。如果用于一个非入口函数的参数，它将被忽略。这样做的目的是为了使一个函数既能作为入口函数，又能作为非入口函数。uniform的变量可以像非uniform的变量那样读写。uniform修饰符通过向外部语言提供一个机制，来提供变量的初始值是如何指定和保存的信息。 |

### 1、数学函数
|CG语言|GLSL语言|	功能描述|
|:-:|:-:|:-:|
| ceil(x) | ceil(x) | 对输入参数向上取整。例如： ceil(float(1.3)) ，其返回值为2.0 |
| floor(x) | floor(x) | 对输入参数向下取整。例如floor(float(1.3))返回的值为1.0；但是floor(float(-1.3))返回的值为-2.0。该函数与ceil(x)函数相对应。 |
| fmod(x,y) | mod(x, y) | 返回x/y的余数。如果y为0，结果不可预料。 |
| frac(x) | fract(x) | 返回标量或矢量的小数 |
| frexp(x, out i) |  | 将浮点数 x 分解为尾数和指数，即 x = m* 2^exp，返回 m，并将指数存入 exp 中；如果 x 为 0，则尾数和指数都返回 0 |
| modf(x, out ip) |  | 把x分解成整数和分数两部分，每部分都和x有着相同的符号，整数部分被保存在ip中，分数部分由函数返回 |
| round(x) |  | 返回四舍五入值。 |
| exp(x) | exp(x) |   计算e <sup>x</sup>  的值，e=2.71828182845904523536 |
| exp2(x) | exp2(x) |  计 算 2 <sup>x</sup> 的 值 |
| log(x) | log(x) |  计 算 ln ⁡ ( x ) 的 值 ， x 必 须 大 于 0 |
| log2(x) | log2(x) | 计 算 log ⁡ 2 ( x ) 的 值 ， x 必 须 大 于 0 |
| log10(x) |  | 计 算 lg ⁡ ( x ) 的 值 ， x 必 须 大 于 0 |
| max(a, b) | max(a, b) | 比较两个标量或等长向量元素，返回最大值。 |
| min(a,b) | min(a,b) | 比较两个标量或等长向量元素，返回最小值。 |
| pow(x, y) | pow(x, y) |  计 算 x <sup>y</sup> 的 值 |
| sqrt(x) | sqrt(x) | 求x的平方根，，x必须大于0 |
| rsqrt(x) | inversesqrt(x) | x的平方根的倒数，x必须大于0 |
| abs(x) | abs(x) | 返回输入参数的绝对值 |
| ldexp(x, n) |  |  计 算 x ∗ 2 <sup>n</sup> 的 值 |
| mul(M, N) | M*N | 矩阵M和矩阵N的积 |
| mul(M, v) | M*v | 矩阵M和列向量v的积 |
| mul(v, M) | v* M | 行向量v和矩阵M的积 |
| determinant(m) |  | 计算矩阵的行列式因子。 |
| transpose(M) |  | 矩阵M的转置矩阵 如果M是一个AxB矩阵，M的转置是一个BxA矩阵，它第一列是M的第一行，第二列是M的第二行，第三列是M的第三行，等等|
| asin(x) | asin(x) | 反正弦函数,输入参数取值区间为，返回角度值范围为[−π/2,π/2] |
| acos(x) | acos(x) | 反余切函数，输入参数范围为[-1,1]， 返回[0,π]区间的角度值 |
| atan(x) | atan(x) | 反正切函数，返回角度值范围为[−π/2,π/2] |
| atan2(y,x) | atan2(y,x) | 计算y/x的反正切值。实际上和atan(x)函数功能完全一样，至少输入参数不同。atan(x) = atan2(x, float(1))。 |
| sin(x) | sin(x) | 输入参数为弧度，计算正弦值，返回值范围 为[-1,1] |
| cos(x) | cos(x) | 返回弧度x的余弦值。返回值范围为 |
| tan(x) | tan(x) | 计算x正切值 |
| sincos(float x, out s, out c) |  | 该函数是同时计算x的sin值和cos值，其中s=sin(x)，c=cos(x)。该函数用于“同时需要计算sin值和cos值的情况”，比分别运算要快很多! |
| sinh(x) |  | 计算x的双曲正弦 |
| cosh(x) |  | 双曲余弦（hyperbolic cosine）函数，计算x的双曲余弦值。 |
| tanh(x) |  | 计算x的双曲线切线 |
| radians(x) | radians(x) | 函数将角度值转换为弧度值 |
| degrees(x) | degrees(x) | 输入参数为弧度值(radians)，函数将其转换为角度值(degrees) |
| cross(A,B) | cross(A,B) | 返回两个三元向量的叉积(cross product)。注意，输入参数必须是三元向量！ |
| lit(NdotL, NdotH, m) |  | 函数计算环境光、散射光、镜面光的贡献，返回的4元向量。<br>N表示法向量；<br>L表示入射光向量；<br>H表示半角向量；<br>m表示高光系数。<br>X位表示环境光的贡献，总是1.0;<br>Y位代表散射光的贡献，如果 N∙L<0，则为0；否则为N∙L<br>Z位代表镜面光的贡献，如果N∙L<0 或者N∙H \< 0，则位0；否则为(N∙L)m; <br>W位始终位1.0|
| all(x) | all(x) | 如果输入参数均不为0，则返回ture； 否则返回flase。&&运算 |
| any(x) | any(x) | 输入参数只要有其中一个不为0，则返回true。 |
| isfinite(x) |  | 判断标量或者向量中的每个数据是否是有限数，如果是返回true；否则返回false; |
| isinf(x) |  | 判断标量或者向量中的每个数据是否是无限，如果是返回true；否则返回false; |
| isnan(x) |  | 判断标量或者向量中的每个数据是否是非数据(not-a-number NaN)，如果是返回true；否则返回false; |
| step(a, x) | step(a, x) | 如果x<a, 返回0；否则返回1 |
| sign(x) | sign(x) | 如果x>0则返回1；如果x=0返回0；如果x<0则返回-1 |
| dot(A,B) | dot(A,B) | 返回A和B的点积(dot product)。参数A和B可以是标量，也可以是向量（输入参数方面，点积和叉积函数有很大不同）。 |
| noise(x) |  | 根据它的参数类型，这个函数可以是一元、二元或三元噪音函数。返回的值在0和1之间，并且通常与给定的输入值一样 |
| clamp(x,a,b) | clamp(x,a,b) | 如果x值小于a，则返回a； <br>如果x值大于b，返回b；<br>否则，返回x。|
| lerp(a, b, f) | mix(a, b, f) | 计算或者的值。即在下限a和上限b之间进行插值，f表示权值。注意，如果a和b是向量，则权值f必须是标量或者等长的向量。 |
| saturate(x) |  | 把x限制到[0,1]之间 |
| smoothstep(min, max, x) | smoothstep(min, max, x) | 值x位于min、max区间中。 <br>如果x=min，返回0；如果x=max，返回1；<br>如果x在两者之间，按照下列公式返回数据：<br>**– 2 ∗ ( ( x – m i n ) / ( m a x – m i n ) ) <sup>3</sup> + 3 ∗ ( ( x – m i n ) / ( m a x – m i n ) ) <sup>2</sup>**|

smoothstep(min, max, x)对于参数全是float的重载

```glsl
float smoothstep(float a, float b, float x)
{
    float t = saturate((x - a)/(b - a));
    return t*t*(3.0 - (2.0*t));
}

```

### 2、几何函数

| CG语言 | GLSL语言 | 功能描述 |
|:-:|:-:|:-:|
| distance(pt1, pt2) | distance(pt1, pt2) | 两点之间的欧几里德距离（Euclidean distance） |
| faceforward(N,I,Ng) | faceforward(N,I,Ng) | 根据 矢量 N 与Nref 调整法向量,如果Ng•I < 0 ，返回 N；否则返回-N。 |
| length(v) | length(v) | 返回一个向量的模，即sqrt(dot(v,v)) |
| normalize(v) | normalize(v) | 返回v向量的单位向量 |
| reflect(I, N) | reflect(I, N) | 根据入射光方向向量 I，和顶点法向量 N，计算反射光方向向量。 <br>其中 I 和 N 必须被归一化，需要非常注意的是，这个 I 是指向顶点的；<br>函数只对三元向量有效|
| refract(I,N,eta) | refract(I,N,eta) | 计算折射向量，I 为入射光线，N 为法向量，eta 为折射系数； <br>其中 I 和 N 必须被归一化，如果 I 和 N 之间的夹角太大，则返回（0，0，0），也就是没有折射光线；I 是指向顶点的；函数只对三元向量有效|

### 3、纹理映射函数

| CG语言 | 功能描述 |
|:-:|:-:|
| tex1D(sampler1D tex, float s) | 一维纹理查询 |
| tex1D(sampler1D tex, float s, float dsdx, float dsdy) | 使用导数值（derivatives）查询一维纹理 |
| Tex1D(sampler1D tex, float2 sz) | 一维纹理查询，并进行深度值比较 |
| Tex1D(sampler1D tex, float2 sz, float dsdx,float dsdy) | 使用导数值（derivatives）查询一维纹理， 并进行深度值比较 |
| Tex1Dproj(sampler1D tex, float2 sq) | 一维投影纹理查询 |
| Tex1Dproj(sampler1D tex, float3 szq) | 一维投影纹理查询，并比较深度值 |
| Tex2D(sampler2D tex, float2 s) | 二维纹理查询 |
| Tex2D(sampler2D tex, float2 s, float2 dsdx, float2 dsdy) | 使用导数值（derivatives）查询二维纹理 |
| Tex2D(sampler2D tex, float3 sz) | 二维纹理查询，并进行深度值比较 |
| Tex2D(sampler2D tex, float3 sz, float2 dsdx,float2 dsdy) | 使用导数值（derivatives）查询二维纹理，并进行深度值比较 |
| Tex2Dproj(sampler2D tex, float3 sq) | 二维投影纹理查询 |
| Tex2Dproj(sampler2D tex, float4 szq) | 二维投影纹理查询，并进行深度值比较 |
| texRECT(samplerRECT tex, float2 s) | 二维非投影矩形纹理查询（OpenGL独有） |
| texRECT (samplerRECT tex, float3 sz, float2 dsdx,float2 dsdy) | 二维非投影使用导数的矩形纹理查询（OpenGL独有） |
| texRECT (samplerRECT tex, float3 sz) | 二维非投影深度比较矩形纹理查询（OpenGL独有） |
| texRECT (samplerRECT tex, float3 sz, float2 dsdx,float2 dsdy) | 二维非投影深度比较并使用导数的矩形纹理查询（OpenGL独有） |
| texRECT proj(samplerRECT tex, float3 sq) | 二维投影矩形纹理查询（OpenGL独有） |
| texRECT proj(samplerRECT tex, float3 szq) | 二维投影矩形纹理深度比较查询（OpenGL独有） |
| Tex3D(sampler3D tex, float s) | 三维纹理查询 |
| Tex3D(sampler3D tex, float3 s, float3 dsdx, float3 dsdy) | 结合导数值（derivatives）查询三维纹理 |
| Tex3Dproj(sampler3D tex, float4 szq) | 查询三维投影纹理，并进行深度值比较 |
| texCUBE(samplerCUBE tex, float3 s) | 查询立方体纹理 |
| texCUBE (samplerCUBE tex, float3 s, float3 dsdx, float3 dsdy) | 结合导数值（derivatives）查询立方体纹理 |
| texCUBEproj (samplerCUBE tex, float4 sq) | 查询投影立方体纹理 |

### 4、偏导函数

| 函数 | 功能描述 |
|:-:|:-:|
| ddx(a) | 近似a关于屏幕空间x轴的偏导数 |
| ddy(a) | 近似a关于屏幕空间y轴的偏导数 |

## 二、Unity常用的内置函数，变量
### 1、Unity常用的结构体
#### 1.1、顶点着色器输入

| 名称 | 描述 | 包含的变量 |
|:-:|:-:|:-:|
| appdata_base | 用于顶点着色器输入 | 顶点位置、顶点法线、第一组纹理坐标 |
| appdata_tan | 用于顶点着色器输入 | 顶点位置、顶点切线、顶点法线、第一组纹理坐标 |
| appdata_full | 用于顶点着色器输入 | 顶点位置、顶点切线、顶点法线、四组（或更多）纹理坐标 |
| appdata_img | 用于顶点着色器输入 | 顶点位置、第一组纹理坐标 |

```glsl
struct appdata_base {
    float4 vertex : POSITION;
    float3 normal : NORMAL;
    float4 texcoord : TEXCOORD0;
    UNITY_VERTEX_INPUT_INSTANCE_ID
};

struct appdata_tan {
    float4 vertex : POSITION;
    float4 tangent : TANGENT;
    float3 normal : NORMAL;
    float4 texcoord : TEXCOORD0;
    UNITY_VERTEX_INPUT_INSTANCE_ID
};

struct appdata_full {
    float4 vertex : POSITION;
    float4 tangent : TANGENT;
    float3 normal : NORMAL;
    float4 texcoord : TEXCOORD0;
    float4 texcoord1 : TEXCOORD1;
    float4 texcoord2 : TEXCOORD2;
    float4 texcoord3 : TEXCOORD3;
    fixed4 color : COLOR;
    UNITY_VERTEX_INPUT_INSTANCE_ID
};
struct appdata_img
{
    float4 vertex : POSITION;
    half2 texcoord : TEXCOORD0;
    UNITY_VERTEX_INPUT_INSTANCE_ID
};

```

#### 1.2、顶点着色器输出

| 名称 | 描述 | 包含的变量 |
|:-:|:-:|:-:|
| v2f_img | 用于顶点着色器输出 | 裁剪空间中的位置、纹理坐标 |

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
#### A、空间变换函数

| 函数名 | 描述 |
|:-:|:-:|
| float4 UnityWorldToClipPos(float3 pos ) | 把世界坐标空间中某一点pos变换到齐次裁剪空间 |
| float4 UnityViewToClipPos(float3 pos ) | 把观察坐标空间中某一点pos变换到齐次裁剪空间 |
| float3 UnityObjectToViewPos(float3 pos或float4 pos) | 模型局部空间坐标系中某一个点pos变换到观察空间坐标系 |
| float3 UnityWorldToViewPos(float3 pos ) | 把世界坐标系下的一个点pos变换到观察空间坐标系 |
| float3 UnityObjectToWorldDir(float3 dir ) | 把方向矢量从模型空间转换到世界空间（方向已单位化） |
| float3 UnityWorldToObjectDir(float3 dir ) | 把方向矢量从世界空间转换到模型空间（方向已单位化） |
| float3 UnityObjectToWorldNormal(float3 norm ) | 将法线从模型空间转换到世界空间（方向已单位化） |
| float3 UnityWorldSpaceLightDir(float3 worldPos ) | 输入参数worldPos是一个世界坐标系下的坐标，得到世界空间中从该点到光源（_WorldSpaceLightPos0）的光照方向。（方向没单位化） |
| float3 WorldSpaceLightDir(float4 localPos ) | 输入一个模型顶点坐标，得到世界空间中从该点到光源（_WorldSpaceLightPos0）的光照方向。（方向没单位化） |
| float3 ObjSpaceLightDir(float4 v ) | 输入一个模型顶点坐标，得到模型空间中从该点到光源（_WorldSpaceLightPos0）的光照方向。（方向没单位化） |
| float3 UnityWorldSpaceViewDir(float3 worldPos ) | 输入参数worldPos是一个世界坐标系下的坐标，得到世界空间中从该点到摄像机的观察方向。（方向没单位化） |
| float3 WorldSpaceViewDir(float4 localPos ) | 输入一个模型顶点坐标，得到世界空间中从该点到摄像机的观察方向。（方向没单位化） |
| float3 ObjSpaceViewDir(float4 v ) | 输入一个模型顶点坐标，得到模型空间中从该点到摄像机的观察方向。（方向没单位化） |

#### B、屏幕空间相关函数
以下函数可计算用于采样屏幕空间纹理的坐标。它们返回 float4，其中用于纹理采样的最终坐标可以通过透视除法（例如 xy/w）计算得出。

| 函数名 | 描述 |
|:-:|:-:|
| float4 ComputeScreenPos (float4 clipPos) | 计算用于执行屏幕空间贴图纹理采样的纹理坐标。输入是裁剪空间位置。 |
| float4 ComputeGrabScreenPos (float4 clipPos) | 计算用于 GrabPass 纹理采样的纹理坐标。输入是裁剪空间位置。 |

#### C、内置变量矩阵
|变量名	|描述|
|:-:|:-:|
| UNITY_MATRIX_MVP | 当前的模型观察投影矩阵，用于将顶点/方向矢量从模型空间转换到裁剪空间 |
| UNITY_MATRIX_MV | 当前的模型*观察矩阵，用于将顶点/方向矢量从模型空间转换到观察空间 |
| UNITY_MATRIX_V | 当前的观察矩阵，用于将顶点/方向矢量从世界空间转换到观察空间 |
| UNITY_MATRIX_I_V | 当前的观察矩阵的逆矩阵，用于从观察空间转换到世界空间|
| UNITY_MATRIX_P | 当前的投影矩阵，用于将顶点/方向矢量从观察空间转换到裁剪空间 |
| UNITY_MATRIX_VP | 当前的观察*投影矩阵，用于将顶点/方向矢量从世界空间转换到裁剪空间 |
| UNITY_MATRIX_T_MV | UNITY_MATRIX_MV的转置矩阵 |
| UNITY_MATRIX_IT_MV | UNITY_MATRIX_MV的逆转置矩阵，用于将发现从模型空间转换到观察空间，也可以用于得到UNITY_MATRIX_MV的逆矩阵 |
| unity_MatrixInvV | UNITY_MATRIX_V的逆矩阵 |

---

#### D、摄像机和屏幕参数


| 参数名 | 描述 |
|:-:|:-:|
| float3 _WorldSpaceCameraPos | 该摄像机在世界空间中的位置 |
| float4 _ProjectionParams | x=1.0(或-1.0，如果正在使用一个翻转的投影矩阵进行渲染)，y=Near,z=Far,w=1.0+1.0/Far,其中Near和Far分别是近裁剪平面和远裁剪平面到摄像机的距离 |
| float4 _ScreenParams | x=width,y=height,z=1.0+1.0/width,w=1.0+1.0/height,其中width和height分别是该摄像机的渲染目标（render target）的像素宽度和高度 |
| float4 _ZBufferParams | x=1-Far/Near,y=Far/Near,z=x/Far,w=y/Far,该变量用于线性化Z缓存中的深度值 |
| float4 unity_OrthoParams | x=width,y=height,z没有定义,w=1.0(该摄像机是正交摄像机)或w=0.0（该摄像机是透视摄像机），其中width和height是正交投影摄像机的宽度和高度 |
| float4x4 unity_CameraProjection | 该摄像机的投影矩阵 |
| float4x4 unity_CameraInvProjection | 该摄像机的投影矩阵的逆矩阵 |
| float4 unity_CameraWorldClipPlanes[6] | 该摄像机的6个裁剪平面在世界空间下的等式，按左、右、下、上、近、远裁剪平面 |


#### E、时间变量

---
|名称	|类型	|值|
|:-:|:-:|:-:|
_Time|	float4|	自关卡加载以来的时间 (t/20, t, t*2, t*3)，用于将着色器中的内容动画化。
_SinTime|	float4|	时间正弦：(t/8, t/4, t/2, t)。
_CosTime|	float4|	时间余弦：(t/8, t/4, t/2, t)。
unity_DeltaTime|	float4|	增量时间：(dt, 1/dt, smoothDt, 1/smoothDt)。
---
#### F、光照变量
---
>参考unity官方文档：[内置着色器变量](https://docs.unity.cn/cn/current/Manual/SL-UnityShaderVariables.html)

#### G、雾效和环境光
---
名称|	类型|	值
|:-:|:-:|:-:|
unity_AmbientSky|	fixed4|	梯度环境光照情况下的天空环境光照颜色。
unity_AmbientEquator|	fixed4	|梯度环境光照情况下的赤道环境光照颜色。
unity_AmbientGround	|fixed4	|梯度环境光照情况下的地面环境光照颜色。
UNITY_LIGHTMODEL_AMBIENT|	fixed4|	环境光照颜色（梯度环境情况下的天空颜色）。旧版变量。
unity_FogColor|	fixed4|	雾效颜色。
unity_FogParams	|float4	|用于雾效计算的参数：`(density / sqrt(ln(2))、density / ln(2)、–1/(end-start) `和 `end/(end-start))`。x 对于 Exp2 雾模式很有用；_y_ 对于 Exp 模式很有用，_z_ 和 w 对于 Linear 模式很有用。


#### H、其他
---
名称|	类型|	值
|-|-|-|
unity_LODFade|	float4|	使用 LODGroup 时的细节级别淡入淡出。x 为淡入淡出（0 到 1），_y_ 为量化为 16 级的淡入淡出，_z_ 和 w 未使用。
_TextureSampleAdd|	float4	|根据所使用的纹理是 Alpha8 格式（值设置为 (1,1,1,0)）还是不是该格式（值设置为 (0,0,0,0)）由 Unity 仅针对 UI 自动设置。

### 3、数学常数

``` glsl
#ifndef UNITY_CG_INCLUDED
#define UNITY_CG_INCLUDED
 
#define UNITY_PI            3.14159265359f       //圆周率
#define UNITY_TWO_PI        6.28318530718f       //2倍圆周率
#define UNITY_FOUR_PI       12.56637061436f      //4倍圆周率
#define UNITY_INV_PI        0.31830988618f       //圆周率的倒数
#define UNITY_INV_TWO_PI    0.15915494309f       //2倍圆周率的倒数
#define UNITY_INV_FOUR_PI   0.07957747155f       //4倍圆周率的倒数
#define UNITY_HALF_PI       1.57079632679f       //半圆周率
#define UNITY_INV_HALF_PI   0.636619772367f      //半圆周率的倒数


```

### 4、与颜色空间相关

| 函数名 | 描述 |
|:-:|:-:|
| bool IsGammaSpace() | 根据宏UNITY_COLORSPACE_GAMMA是否被启用了，判断当前是否启用了伽马颜色空间。 |
| float GammaToLinearSpaceExact (float value) | 把一个颜色值精确地从伽马颜色空间(sRGB颜色空间)变化到线性空间(CIE-XYZ颜色空间)。 |
| half3 GammaToLinearSpace (half3 sRGB) | 用一个近似模拟的函数把颜色值近似地从伽马空间变换到线性空间。 |
| float LinearToGammaSpaceExact (float value) | 把一个颜色值精确地从线性空间变换到伽马颜色空间。 |
| half3 LinearToGammaSpace (half3 linRGB) | 用一个近似模拟的函数把颜色值近似地从线性空间变换到伽马颜色空间。 |

>引用：[UnityShader常用函数（UnityShader内置函数、CG和GLSL内置函数等）](https://blog.csdn.net/u012722551/article/details/103926660)  
>unity官方文档：[内置着色器变量](https://docs.unity.cn/cn/current/Manual/SL-UnityShaderVariables.html)