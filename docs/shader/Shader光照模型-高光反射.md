---
title: "Shader光照模型-高光反射"
date: "2026-03-21"
tags:
  - Shader
  - 图形学
  - 网络
  - 项目记录
categories:
  - shader
comments: true
---
# Shader光照模型-高光反射

> ###### 参考 《unity shader 入门精要》
> 之前学过了，这几天回顾发现忘了一干二净，现在整理出来

 高光反射光照模型分为**Phong模型**和**Blinn-Phong模型**，而光照实现方式又分为逐像素光照和逐顶点光照

Phong和Blinn-Phong是计算镜面反射光的两种光照模型，两者仅仅有很小的不同之处。
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181014094604428.png)  

 

###  0X01 Phong光照模型(高光反射)	
#### Phong模型公式：
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181014094619163.png)  

Phone模型计算中的一个关键步骤就是反射向量R的计算：
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181014094630562.png)  

 
上图中的位于表面“下面”的向量 ‘I’ 是原始 ‘I’ 向量的拷贝，并且二者是一样的，现在我们的目标计算出向量 ‘R’ 。根据向量相加原则，向量 ‘R’ 等于 'I' + 'V'，‘I’ 是已知的，所以我们需要做的就是找出向量 ‘V’。注意法向量 ‘N’ 的负方向就是 ‘-N’，我们可以在 ‘I’ 和 ‘-N’ 之间使用一个点乘运算就能得到 ‘I’ 在 ‘-N’ 上面的投影的模。这个模正好是 ‘V’ 的模的一半，由于 ‘V’ 与 ‘N’ 有相同的方向，我们可以将这个模乘上 ‘N’ （其模为 1 ）再乘上 2 即可得到 ‘V’。总结一下就是下面的公式：
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181014094715453.png)  

根据公式实现自己的myReflect函数，和unity shader自带的reflect一样
```c
			//反射
			float3 myReflect(float3 I,float3 normal)
			{
				//return  I - 2*normal*dot(normal,I);			
				return  I - 2*normal*mul(I,float3x1( normal.x,normal.y,normal.z));
			}
```
关键代码：
```c
				fixed3 reflectDir = normalize(myReflect(-worldLightDir, worldNormal));

				// Get the view direction in world space
				fixed3 viewDir = normalize(_WorldSpaceCameraPos.xyz - mul(unity_ObjectToWorld, v.vertex).xyz);
				
				// Compute specular term
				fixed3 specular = _LightColor0.rgb * _Specular.rgb * pow(max(0,dot(reflectDir, viewDir)), _Gloss);
```

unity shader实现：
#### 逐顶点光照(Phong高光模型)
```c
//Phong 高光光照模型  逐顶点

Shader "Book/06.SpecularPhongVert" {
	Properties {
		_Diffuse ("Diffuse", Color) = (1, 1, 1, 1)
		_Specular ("Specular", Color) = (1, 1, 1, 1)
		_Gloss ("Gloss", Range(8.0, 256)) = 20
	}
	SubShader {
		Pass { 
			Tags { "LightMode"="ForwardBase" }
			
			CGPROGRAM
			
			#pragma vertex vert
			#pragma fragment frag
			
			#include "Lighting.cginc"
			
			fixed4 _Diffuse;
			fixed4 _Specular;
			float _Gloss;
			
			struct a2v {
				float4 vertex : POSITION;
				float3 normal : NORMAL;
			};
			
			struct v2f {
				float4 pos : SV_POSITION;
				fixed3 color : COLOR;
			};

			//反射
			float3 myReflect(float3 I,float3 normal)
			{
				//return  I - 2*normal*dot(normal,I);			
				return  I - 2*normal*mul(I,float3x1( normal.x,normal.y,normal.z));
			}
			
			v2f vert(a2v v) {
				v2f o;
				// Transform the vertex from object space to projection space
				o.pos = UnityObjectToClipPos(v.vertex);
				
				// Get ambient term
				fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT.xyz;
				
				// Transform the normal from object space to world space
				fixed3 worldNormal = normalize(mul(v.normal, (float3x3)unity_WorldToObject));
				// Get the light direction in world space
				fixed3 worldLightDir = normalize(_WorldSpaceLightPos0.xyz);
				
				// Compute diffuse term
				fixed3 diffuse = _LightColor0.rgb * _Diffuse.rgb * max(0,dot(worldNormal, worldLightDir));
				
				// Get the reflect direction in world space
				//fixed3 reflectDir = normalize(reflect(-worldLightDir, worldNormal));
				fixed3 reflectDir = normalize(myReflect(-worldLightDir, worldNormal));

				// Get the view direction in world space
				fixed3 viewDir = normalize(_WorldSpaceCameraPos.xyz - mul(unity_ObjectToWorld, v.vertex).xyz);
				
				// Compute specular term
				fixed3 specular = _LightColor0.rgb * _Specular.rgb * pow(max(0,dot(reflectDir, viewDir)), _Gloss);
				
				o.color = ambient + diffuse + specular;
							 	
				return o;
			}
			
			fixed4 frag(v2f i) : SV_Target {
				return fixed4(i.color, 1.0);
			}
			
			ENDCG
		}
	} 
	FallBack "Specular"
}

```
#### 逐像素光照(Phong高光模型)
```c
//Phong 高光光照模型  逐像素

Shader "Book/06.SpecularPhongPixel" {
	Properties {
		_Diffuse ("Diffuse", Color) = (1, 1, 1, 1)
		_Specular ("Specular", Color) = (1, 1, 1, 1)
		_Gloss ("Gloss", Range(8.0, 256)) = 20
	}
	SubShader {
		Pass { 
			Tags { "LightMode"="ForwardBase" }
		
			CGPROGRAM
			
			#pragma vertex vert
			#pragma fragment frag

			#include "Lighting.cginc"
			
			fixed4 _Diffuse;
			fixed4 _Specular;
			float _Gloss;
			
			struct a2v {
				float4 vertex : POSITION;
				float3 normal : NORMAL;
			};
			
			struct v2f {
				float4 pos : SV_POSITION;
				float3 worldNormal : TEXCOORD0;
				float3 worldPos : TEXCOORD1;
			};
			
			//反射
			float3 myReflect(float3 I,float3 normal)
			{
				//return  I - 2*normal*dot(normal,I);			
				return  I - 2*normal*mul(I,float3x1( normal.x,normal.y,normal.z));
			}

			v2f vert(a2v v) {
				v2f o;
				// Transform the vertex from object space to projection space
				o.pos = UnityObjectToClipPos(v.vertex);
				
				// Transform the normal from object space to world space
				o.worldNormal = mul(v.normal, (float3x3)unity_WorldToObject);
				// Transform the vertex from object spacet to world space
				o.worldPos = mul(unity_ObjectToWorld, v.vertex).xyz;
				
				return o;
			}
			
			fixed4 frag(v2f i) : SV_Target {
				// Get ambient term
				fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT.xyz;
				
				fixed3 worldNormal = normalize(i.worldNormal);
				fixed3 worldLightDir = normalize(_WorldSpaceLightPos0.xyz);
				
				// Compute diffuse term
				fixed3 diffuse = _LightColor0.rgb * _Diffuse.rgb * max(0,dot(worldNormal, worldLightDir));
				
				// Get the reflect direction in world space
				//fixed3 reflectDir = normalize(reflect(-worldLightDir, worldNormal));
				fixed3 reflectDir = normalize(myReflect(-worldLightDir, worldNormal));

				// Get the view direction in world space
				fixed3 viewDir = normalize(_WorldSpaceCameraPos.xyz - i.worldPos.xyz);
				// Compute specular term
				fixed3 specular = _LightColor0.rgb * _Specular.rgb * pow(max(0,dot(reflectDir, viewDir)), _Gloss);
				
				return fixed4(ambient + diffuse + specular, 1.0);
			}
			
			ENDCG
		}
	} 
	FallBack "Specular"
}

```


###  0X02 Blinn-Phong光照模型(高光反射)	
#### Blinn-Phong模型公式：
 Phong模型中计算反射光线的向量是一件相对比较耗时的任务，因此Blinn-Phong对这一点进行了改进。
  

![Blinn-Phong](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181014094443466.png)  


Ks：物体对于反射光线的衰减系数

N：表面法向量

H：光入射方向L和视点方向V的中间向量

Shininess：高光系数

 

可见，通过该式计算镜面反射光是符合基本规律的，当视点方向和反射光线方向一致时，计算得到的H与N平行，dot(N,H)取得最大；当视点方向V偏离反射方向时，H也偏离N。

同时H的计算比起反射向量R的计算简单的多，R向量的计算需要若干次的向量乘法与加法，而H的计算仅仅需要一次加法。
关键代码：
```c
				fixed3 halfDir = normalize(worldLightDir + viewDir);
				// Compute specular term
				fixed3 specular = _LightColor0.rgb * _Specular.rgb * pow(max(0, dot(worldNormal, halfDir)), _Gloss);
```

unity shader基本实现：
```c
//Blinn-Phong 高光光照模型

Shader "Book/06.SpecularBlinnPhong" {
	Properties {
		_Diffuse ("Diffuse", Color) = (1, 1, 1, 1)
		_Specular ("Specular", Color) = (1, 1, 1, 1)
		_Gloss ("Gloss", Range(8.0, 256)) = 20
	}
	SubShader {
		Pass { 
			Tags { "LightMode"="ForwardBase" }
		
			CGPROGRAM
			
			#pragma vertex vert
			#pragma fragment frag
			
			#include "Lighting.cginc"
			
			fixed4 _Diffuse;
			fixed4 _Specular;
			float _Gloss;
			
			struct a2v {
				float4 vertex : POSITION;
				float3 normal : NORMAL;
			};
			
			struct v2f {
				float4 pos : SV_POSITION;
				float3 worldNormal : TEXCOORD0;
				float3 worldPos : TEXCOORD1;
			};
			
			v2f vert(a2v v) {
				v2f o;
				// Transform the vertex from object space to projection space
				o.pos = UnityObjectToClipPos(v.vertex);
				
				// Transform the normal from object space to world space
				o.worldNormal = mul(v.normal, (float3x3)unity_WorldToObject);
				
				// Transform the vertex from object spacet to world space
				o.worldPos = mul(unity_ObjectToWorld, v.vertex).xyz;
				
				return o;
			}
			
			fixed4 frag(v2f i) : SV_Target {
				// Get ambient term
				fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT.xyz;
				
				fixed3 worldNormal = normalize(i.worldNormal);
				fixed3 worldLightDir = normalize(_WorldSpaceLightPos0.xyz);
				
				// Compute diffuse term
				fixed3 diffuse = _LightColor0.rgb * _Diffuse.rgb * max(0, dot(worldNormal, worldLightDir));
				
				// Get the view direction in world space
				fixed3 viewDir = normalize(_WorldSpaceCameraPos.xyz - i.worldPos.xyz);
				// Get the half direction in world space
				fixed3 halfDir = normalize(worldLightDir + viewDir);
				// Compute specular term
				fixed3 specular = _LightColor0.rgb * _Specular.rgb * pow(max(0, dot(worldNormal, halfDir)), _Gloss);
				
				return fixed4(ambient + diffuse + specular, 1.0);
			}
			
			ENDCG
		}
	} 
	FallBack "Specular"
}

```
所有效果：左边Phong逐顶点光照，中间Phong逐像素光照，右边Blinn-Phong光照
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181014095329302.png)  



*关于法线从模型空间转换到世界空间o.worldNormal = mul(v.normal, (float3x3)unity_WorldToObject);后面补充为什么这么计算*

>参考文章：
>[Phong和Blinn-Phong光照模型](https://www.cnblogs.com/bluebean/p/5299358.html)