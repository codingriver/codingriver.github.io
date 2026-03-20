---
title: "【Shader】 纹理动画"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["shader"]
categories: ["shader"]
---

<!--more-->

> ###### 参考 《unity shader 入门精要》


###  0X01 序列帧动画	
### 爆炸的动画
```c
// Upgrade NOTE: replaced 'mul(UNITY_MATRIX_MVP,*)' with 'UnityObjectToClipPos(*)'
Shader "Book/11.ImageSequenceAnimation"
{
//折射
	Properties
	{
		_Color ("Color Tint",Color)=(1,1,1,1)
		_MainTex("Main Tex",2D)="white"{}
		_HorizontalAmount("Horizontal Amount",Float)=4.0
		_VerticalAmount("Vertical Amount",Float)=4.0
		_Speed("Speed",Range(1,100))=30.0
		
	}
	SubShader
	{
		Tags { "Queue"="Transparent" "IgnoreProjector"="True" "RenderType"="Transparent"}
		Pass
		{
			Tags { "LightMode"="ForwardBase" }
			ZWrite  Off
			Blend srcAlpha OneMinusSrcAlpha

			CGPROGRAM
			#pragma vertex vert
			#pragma fragment frag
			// make fog work
			//#pragma multi_compile_fog
			
			#include "UnityCG.cginc"


			float4 _Color;
			 sampler2D _MainTex;
			 float _HorizontalAmount,_VerticalAmount,_Speed;
			 float4 _MainTex_ST;



			struct a2v
			{
				float4 vertex : POSITION;
				float3 normal: NORMAL;
				float4 tangent:TANGENT;
				float2 texcoord : TEXCOORD0;
			};

			struct v2f
			{
				float4 pos : SV_POSITION;
				float2 uv : TEXCOORD0;
				float3 lightDir:TEXCOORD1;
				float3 viewDir:TEXCOORD2;
				float3 worldNormal:TEXCOORD3;
				float3 worldPos:TEXCOORD4;
				float3 worldRefr:TEXCOORD5;
			};

			v2f vert (a2v v)
			{
				v2f o;
				o.pos = UnityObjectToClipPos(v.vertex);
				o.uv = TRANSFORM_TEX(v.texcoord,_MainTex);
				float time = floor(_Time.y*_Speed);
				float y = floor(time/_HorizontalAmount);
				float x = time - y*_HorizontalAmount;
				o.uv= o.uv +float2(x,-y);
				o.uv.x /= _HorizontalAmount;
				o.uv.y /= _VerticalAmount;
				return o;
			}
			

			fixed4 frag (v2f i) : SV_Target
			{

				float4 col = tex2D(_MainTex,i.uv);
				col.rgb*=_Color.rgb;
				return col;
			}
			fixed4 frag1 (v2f i) : SV_Target
			{
				float time = floor(_Time.y*_Speed);
				/*
				float offset = time%(_HorizontalAmount*_VerticalAmount);
				float offsetY=floor(offset/_HorizontalAmount);
				float offsetX = offset - offsetY*_HorizontalAmount;
				float2 uv = float2(i.uv.x/_HorizontalAmount,i.uv.y/_VerticalAmount) +float2(offsetX*1/_HorizontalAmount,-offsetY*1/_VerticalAmount);
				*/
				//想象成动画一直竖着往下滚动，向下无限远且循环，time是当前要播放第几帧的编号，这个编号一直无限增加
				float y = floor(time/_HorizontalAmount);
				float x = time - y*_HorizontalAmount;
				float2 uv = i.uv +float2(x,-y);
				uv.x /= _HorizontalAmount;
				uv.y /= _VerticalAmount;

				float4 col = tex2D(_MainTex,uv);
				col.rgb*=_Color.rgb;
				return col;
			}
			ENDCG
		}
	}
	FallBack "Diffuse"
}

```
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181014110354872.png)  


  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/201810141104025.png)  


### 滚动背景
```c
// Upgrade NOTE: replaced 'mul(UNITY_MATRIX_MVP,*)' with 'UnityObjectToClipPos(*)'
Shader "Book/11.ScrollingBackground"
{
//折射
	Properties
	{
		_MainTex("Base Layer",2D)="white"{}
		_DetailTex("2nd Layer",2D)="white"{}
		_ScrollX("Base Layer Scroll Speed",Float)=4.0
		_Scroll2X("2nd Layer Scroll Speed",Float)=4.0
		_Multiplier("Layer Multiplier",Float)=1.0
		
	}
	SubShader
	{
		Tags { "RenderType"="Opaque" "Queue"="Geometry"}
		Pass
		{
			Tags { "LightMode"="ForwardBase" }
			ZWrite  Off
			Blend srcAlpha OneMinusSrcAlpha

			CGPROGRAM
			#pragma vertex vert
			#pragma fragment frag
			// make fog work
			//#pragma multi_compile_fog
			
			#include "UnityCG.cginc"


			 sampler2D _MainTex,_DetailTex;
			 float _ScrollX,_Scroll2X,_Multiplier;
			 float4 _MainTex_ST,_DetailTex_ST;



			struct a2v
			{
				float4 vertex : POSITION;
				float3 normal: NORMAL;
				float4 tangent:TANGENT;
				float2 texcoord : TEXCOORD0;
			};

			struct v2f
			{
				float4 pos : SV_POSITION;
				float4 uv : TEXCOORD0;
				float3 lightDir:TEXCOORD1;
				float3 viewDir:TEXCOORD2;
				float3 worldNormal:TEXCOORD3;
				float3 worldPos:TEXCOORD4;
				float3 worldRefr:TEXCOORD5;
			};

			v2f vert (a2v v)
			{
				v2f o;
				o.pos = UnityObjectToClipPos(v.vertex);
				o.uv.xy = TRANSFORM_TEX(v.texcoord,_MainTex)+frac(float2(_ScrollX*_Time.y,0));
				o.uv.zw = TRANSFORM_TEX(v.texcoord,_DetailTex)+frac(float2(_Scroll2X*_Time.y,0));
				
				return o;
			}
			


			fixed4 frag (v2f i) : SV_Target
			{
				float4 baseColor = tex2D(_MainTex,i.uv.xy);
				float4 secondColor = tex2D(_DetailTex,i.uv.zw);
				fixed4 c = lerp(baseColor,secondColor,secondColor.a);
				c.rgb *= _Multiplier;
				return c;
			}
			ENDCG
		}
	}
	FallBack "Diffuse"
}

```
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181014110847634.png)  

  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181014110918886.png)  

  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181014110538846.png)  


###  0X02 顶点动画	

### 流动的河流
```c
// Upgrade NOTE: replaced 'mul(UNITY_MATRIX_MVP,*)' with 'UnityObjectToClipPos(*)'
Shader "Book/11.Water"
{
//折射
	Properties
	{
		_MainTex("Main Tex",2D)="white"{}
		_Color("Color Tint",Color)=(1,1,1,1)
		_Magnitude("Distortion Magnitude",float)=1
		_Frequency("Distortion Frequency",float)=1
		_InvWaveLength("Distortion Inverse Wave Length",float)=10
		_Speed("Speed",float)=0.5
	}
	SubShader
	{
		Tags { "RenderType"="Transparent" "Queue"="Transparent" "IgnoreProjector"="True" "DisableBatching"="True"}

		Pass
		{
			Tags { "LightMode"="ForwardBase" }
			ZWrite  Off
			Blend SrcAlpha OneMinusSrcAlpha
			Cull Off
			//Cull Front

			CGPROGRAM
			#pragma vertex vert
			#pragma fragment frag
			// make fog work
			//#pragma multi_compile_fog
			
			#include "UnityCG.cginc"

			float4 _Color;
			 sampler2D _MainTex;
			 float _Magnitude,_Frequency,_InvWaveLength,_Speed;
			 float4 _MainTex_ST;



			struct a2v
			{
				float4 vertex : POSITION;
				float3 normal: NORMAL;
				float4 tangent:TANGENT;
				float2 texcoord : TEXCOORD0;
			};

			struct v2f
			{
				float4 pos : SV_POSITION;
				float4 uv : TEXCOORD0;
				float3 lightDir:TEXCOORD1;
				float3 viewDir:TEXCOORD2;
				float3 worldNormal:TEXCOORD3;
				float3 worldPos:TEXCOORD4;
				float3 worldRefr:TEXCOORD5;
			};

			v2f vert (a2v v)
			{
				v2f o;
				float4 offset=float4(0,0,0,0);
				//offset.x = sin(_Time.y*_Frequency+(v.vertex.x+v.vertex.y+v.vertex.z)*_InvWaveLength)*_Magnitude;
				offset.x = sin(_Time.y*_Frequency+(v.vertex.z)*_InvWaveLength)*_Magnitude;
				//offset.x = sin((v.vertex.z)*_InvWaveLength)*_Magnitude;

				o.pos = UnityObjectToClipPos(v.vertex+offset);
				o.uv.xy = TRANSFORM_TEX(v.texcoord,_MainTex)+frac(float2(0,_Speed*_Time.y));
				return o;
			}
			


			fixed4 frag (v2f i) : SV_Target
			{
				fixed4 c = tex2D(_MainTex,i.uv.xy);;
				return c;
			}
			ENDCG
		}
	}
	FallBack "Diffuse"
}

```

### 广告牌（始终面向摄像机）
```c
// Upgrade NOTE: replaced 'mul(UNITY_MATRIX_MVP,*)' with 'UnityObjectToClipPos(*)'
Shader "Book/11.Billboard"
{
//折射
	Properties
	{
		_MainTex("Main Tex",2D)="white"{}
		_Color("Color Tint",Color)=(1,1,1,1)
		_VerticalBillboarding("Vertical Restraints",Range(0,1))=1
	}
	SubShader
	{
		Tags { "RenderType"="Transparent" "Queue"="Transparent" "IgnoreProjector"="True" "DisableBatching"="True"}
		//Tags { "RenderType"="Transparent" "Queue"="Transparent" "IgnoreProjector"="True"}

		Pass
		{
			Tags { "LightMode"="ForwardBase" }
			ZWrite  Off
			Blend SrcAlpha OneMinusSrcAlpha
			//Cull Front
			Cull Off

			CGPROGRAM
			#pragma vertex vert
			#pragma fragment frag
			// make fog work
			//#pragma multi_compile_fog
			
			#include "UnityCG.cginc"

			float4 _Color;
			 sampler2D _MainTex;
			 float _VerticalBillboarding;
			 float4 _MainTex_ST;



			struct a2v
			{
				float4 vertex : POSITION;
				float3 normal: NORMAL;
				float4 tangent:TANGENT;
				float2 texcoord : TEXCOORD0;
			};

			struct v2f
			{
				float4 pos : SV_POSITION;
				float4 uv : TEXCOORD0;
				float3 lightDir:TEXCOORD1;
				float3 viewDir:TEXCOORD2;
				float3 worldNormal:TEXCOORD3;
				float3 worldPos:TEXCOORD4;
				float3 worldRefr:TEXCOORD5;
			};

			v2f vert (a2v v)
			{
				v2f o;
				float3 center = float3(0,0,0);
				float3 viewer = mul(unity_WorldToObject,float4(_WorldSpaceCameraPos,1));
				float3 normalDir =viewer-center;

				normalDir.y=normalDir.y*_VerticalBillboarding;
				normalDir = normalize(normalDir);

				float3 upDir = abs(normalDir.y)>0.999?float3(0,0,1): float3(0,1,0);
				float3 rightDir=normalize(cross(upDir,normalDir));
				upDir = normalize(cross(normalDir,rightDir));

				float3 centerOffs = v.vertex.xyz - center;
				float3 localPos = center+ rightDir*centerOffs.x+upDir*centerOffs.y+normalDir*centerOffs.z;

				//o.pos = mul(UNITY_MATRIX_MVP,float4(localPos,1));
				o.pos = UnityObjectToClipPos(float4(localPos, 1));
				o.uv.xy = TRANSFORM_TEX(v.texcoord,_MainTex);
				return o;
			}

			fixed4 frag (v2f i) : SV_Target
			{
				fixed4 c = tex2D(_MainTex,i.uv.xy);;
				c.rgb*=_Color.rgb;
				return c;
			}
			ENDCG
		}
	}
	FallBack "Transparent/VertexLit"
}

```