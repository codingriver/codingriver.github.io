---
title: "【Shader】 法线贴图（世界空间）"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["shader"]
categories: ["shader"]
---

<!--more-->

>法线贴图，世界空间下计算
>参考 《unity shader 入门精要》


```c++
// Upgrade NOTE: replaced 'mul(UNITY_MATRIX_MVP,*)' with 'UnityObjectToClipPos(*)'

Shader "Book/07.WorldNormal"
{
//法线贴图
	Properties
	{
		_Color ("Color Tint",Color)=(1,1,1,1)
		_MainTex ("Main Tex", 2D) = "white" {}
		_BumpMap("Normal Map",2D) = "white" {}
		_BumpScale("Bump Scale",Float) = 1.0
		_Specular("Specular",Color) = (1,1,1,1)
		_Gloss("Gloss",Range(8.0,256)) = 20
	}
	SubShader
	{

		Pass
		{
			Tags { "LightMode"="ForwardBase" }

			CGPROGRAM
			#pragma vertex vert
			#pragma fragment frag
			// make fog work
			//#pragma multi_compile_fog
			
			#include "UnityCG.cginc"
			#include "Lighting.cginc"
			#include "AutoLight.cginc"

			float4 _Color,_Specular;
			sampler2D _MainTex;
			sampler2D _BumpMap;
			float _BumpScale,_Gloss;

			float4 _MainTex_ST;
			float4 _BumpMap_ST;



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
				float3 worldPos: TEXCOORD1;
				float3 mat1: TEXCOORD2;
				float3 mat2: TEXCOORD3;
				float3 mat3: TEXCOORD4;
			};

			
			v2f vert (a2v v)
			{
				v2f o;
				o.pos = UnityObjectToClipPos(v.vertex);
				o.worldPos= mul(unity_ObjectToWorld,v.vertex);
				o.uv.xy = v.texcoord.xy*_MainTex_ST.xy + _MainTex_ST.zw;
				o.uv.zw = v.texcoord.xy*_BumpMap_ST.xy + _BumpMap_ST.zw;
				//float3 worldNormal = mul((float3x3)unity_ObjectToWorld,v.normal);
				float3 worldNormal = mul(v.normal,(float3x3)unity_WorldToObject);
				float3 worldTangent= mul((float3x3)unity_ObjectToWorld,v.tangent.xyz).xyz;
				float3 worldBinormal = cross(worldNormal,worldTangent.xyz)*v.tangent.w;
				o.mat1=worldTangent.xyz;
				o.mat2 = worldBinormal;
				o.mat3 = worldNormal;
				return o;
			}
			
			fixed4 frag (v2f i) : SV_Target
			{
				float3 lightDir = _WorldSpaceLightPos0.xyz - i.worldPos*_WorldSpaceLightPos0.w;
				lightDir = normalize(lightDir);
				float3 viewDir = _WorldSpaceCameraPos.xyz - i.worldPos;
				viewDir = normalize(viewDir);
				float3x3 rotation = float3x3(i.mat1,i.mat2,i.mat3);

				//uppack  normal
				fixed3 tangentNormal; 
				fixed4 packedNormal  = tex2D(_BumpMap,i.uv.zw);
				#if defined(UNITY_NO_DXT5nm)
					tangentNormal.xyz = packedNormal.xyz*2 -1;
				#else
					// --rgba  -- xyzw 
					//DXTnm 格式中a通道（即w分量）对应发现x分量,g通道（即y分量）对应发现y分量,
					//tangentNormal.xy = packedNormal.ag*2 -1;
					tangentNormal.xy = packedNormal.wy*2 -1;
					tangentNormal=tangentNormal* _BumpScale;
					tangentNormal.z = sqrt(1.0-max(0,dot(tangentNormal.xy,tangentNormal.xy)));
				#endif

				tangentNormal = mul(rotation,tangentNormal);
				

				fixed3 albedo = tex2D(_MainTex,i.uv).rgb*_Color.rgb;
				fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT.xyz*albedo;
				fixed3 diffuse = _LightColor0.rgb*albedo*max(0,dot(tangentNormal,lightDir));
				fixed3 halfDir = normalize(lightDir+viewDir);
				fixed3 specular = _LightColor0.rgb*_Specular.rgb*pow(max(0,dot(tangentNormal,halfDir)),_Gloss);
				

				return fixed4(ambient+diffuse+specular,1.0);
			}
			ENDCG
		}
	}
}

```
