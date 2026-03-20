---
title: "【Shader】 消融特效"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["shader"]
categories: ["shader"]
---

<!--more-->

>角色死亡消融，尸体消融，地图烧毁特效
>不带阴影
>参考 《unity shader 入门精要》


```hlsl
// Upgrade NOTE: replaced 'mul(UNITY_MATRIX_MVP,*)' with 'UnityObjectToClipPos(*)'

Shader "Book/15.Dissolve" {
    Properties {
        _BurnAmount("Burn Amount",Range(0.0,1.0)) = 0.0
		_LineWidth("Burn Line Width",Range(0.0,0.2))=0.1
        _MainTex ("Albedo (RGB)", 2D) = "white" {}
		_BumpMap("Bump Map",2D)= "white" {}
		_BurnFirstColor("Burn First Color",Color)= (1,0,0,1)
		_BurnSecondColor("Burn Second Color",Color)= (1,0,0,1)
		_BurnMap("Burn Map",2D)= "white" {}
    }
    SubShader {
        Tags {"RenderType"="Opaque" "Queue"="Geometry"}
        

	Pass {
		Tags {"LightMode"="ForwardBase" }
		Cull Off


        CGPROGRAM
        #include "UnityCG.cginc"
		#include "Lighting.cginc"
		#include "AutoLight.cginc"

		#pragma multi_compile_fwdbase
        #pragma vertex vert
        #pragma fragment frag



			sampler2D _MainTex;
            sampler2D _BurnMap;
            sampler2D _BumpMap;
            float4 _BurnFirstColor;
            float4 _BurnSecondColor;
            float4 _MainTex_ST;
            float4 _BumpMap_ST;
            float4 _BurnMap_ST;
            float _BurnAmount,_LineWidth;

            struct a2v {
                float4 vertex : POSITION;
                float3 normal : NORMAL;
                float4 tangent : TANGENT;
                float4 texcoord : TEXCOORD0;
            };

            struct v2f {
                float4 pos : SV_POSITION;
                float2 uvMainTex : TEXCOORD0;
                float2 uvBumpMap : TEXCOORD1;
                float2 uvBurnMap : TEXCOORD2;
                float3 lightDir  : TEXCOORD3;
                float3 worldPos  : TEXCOORD4;
                SHADOW_COORDS(5)
			};

            v2f vert( a2v v ) {
				v2f o;
				o.pos = UnityObjectToClipPos(v.vertex);
				//o.uvMainTex = v.texcoord*_MainTex_ST.xy + _MainTex_ST.zw;
				o.uvMainTex = TRANSFORM_TEX( v.texcoord,_MainTex);
				 o.uvBumpMap = TRANSFORM_TEX( v.texcoord,_BumpMap);
				 o.uvBurnMap = TRANSFORM_TEX( v.texcoord,_BurnMap);
				 //副切线
				float3 binormal = cross(v.normal,v.tangent.xyz)*v.tangent.w;
				//从模型空间到切线空间的转换矩阵
				float3x3 rotation = float3x3(v.tangent.xyz,binormal,v.normal);
				//将光源位置减去顶点位置，这样就得到光照方向了 — 但是我们应该首先将顶点位置乘上光源的w分量，如果是平行光，w分量为0，得到的结果为0，说明顶点位置全变为(0.0, 0.0, 0.0)了，这样光照方向就是源   本的位置   （return objSpaceLightPos.xyz）。对于点光源，w为1，所以乘上顶点位置后，顶点位置无变化，这样计算的光照方向就是（return objSpaceLightPos.xyz – v.xyz）。
				float3 lightDir = mul(unity_WorldToObject,_WorldSpaceLightPos0).xyz - v.vertex*_WorldSpaceLightPos0.w;
				o.lightDir = mul(rotation,lightDir);
				o.worldPos = mul(unity_ObjectToWorld,v.vertex).xyz;
				//o.worldNormal = normalize( mul(v.normal,(float3x3)unity_WorldToObject));
				TRANSFER_SHADOW(o);
                return o;
            }
 
        /*
        将上面的函数拷贝进来
        */

        half4 frag(v2f i) : SV_Target {
                fixed3 burn = tex2D(_BurnMap,i.uvBurnMap).rgb;
                clip(burn.r - _BurnAmount);
                float3 tangentLightDir = normalize(i.lightDir);
                //uppack  normal
				fixed3 tangentNormal;
                fixed4 packedNormal  = tex2D(_BumpMap,i.uvBumpMap);
                #if defined(UNITY_NO_DXT5nm)
				tangentNormal.xyz = packedNormal.xyz*2 -1;
                #else
				// --rgba  -- xyzw 
				//DXTnm 格式中a通道（即w分量）对应发现x分量,g通道（即y分量）对应发现y分量,
				//tangentNormal.xy = packedNormal.ag*2 -1;
				tangentNormal.xy = packedNormal.wy*2 -1;
                //tangentNormal=tangentNormal* _BumpScale;
				tangentNormal.z = sqrt(1.0-max(0,dot(tangentNormal.xy,tangentNormal.xy)));
                #endif

				fixed3 albedo = tex2D(_MainTex,i.uvMainTex).rgb;
                fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT.xyz*albedo;
                fixed3 diffuse = _LightColor0.rgb*albedo*max(0,dot(tangentNormal,tangentLightDir));
                fixed t  = 1 - smoothstep(0.0,_LineWidth,burn.r - _BurnAmount);
                fixed3 burnColor = lerp(_BurnFirstColor,_BurnSecondColor,t);
                burnColor = pow(burnColor,5);
                UNITY_LIGHT_ATTENUATION(atten,i,i.worldPos);
                fixed3 finalColor = lerp(ambient+diffuse*atten,burnColor, t* step(0.0001,_BurnAmount));
                return fixed4(finalColor,1);
            }


        ENDCG
        }
    }
    FallBack "Diffuse"
}
```

效果图：
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20180926184200202.png)  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20180926184142862.png)  
