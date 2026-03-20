---
title: "【Shader】 水波纹效果"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["shader"]
categories: ["shader"]
---

<!--more-->

> ###### 使用噪声纹理模拟波纹
> ###### 参考 《unity shader 入门精要》

```c++
// Upgrade NOTE: replaced 'mul(UNITY_MATRIX_MVP,*)' with 'UnityObjectToClipPos(*)'

Shader "Book/15.WaterWave" {
    Properties {
		_Color ("Main Color", Color) = (0, 0.15, 0.115, 1)
		_MainTex ("Base (RGB)", 2D) = "white" {}
		_WaveMap ("Wave Map", 2D) = "bump" {}
		_Cubemap ("Environment Cubemap", Cube) = "_Skybox" {}
		_WaveXSpeed ("Wave Horizontal Speed", Range(-0.1, 0.1)) = 0.01
		_WaveYSpeed ("Wave Vertical Speed", Range(-0.1, 0.1)) = 0.01
		_Distortion ("Distortion", Range(0, 100)) = 10
    }
    SubShader {
        Tags {"RenderType"="Opaque" "Queue"="Transparent"}

		GrabPass{"_RefractionTex"}

	Pass {
		Tags {"LightMode"="ForwardBase" }
		


        CGPROGRAM
		#include "UnityCG.cginc"
		#include "Lighting.cginc"

		#pragma multi_compile_fwdbase
        #pragma vertex vert
        #pragma fragment frag



			fixed4 _Color;
			sampler2D _MainTex;
			float4 _MainTex_ST;
			sampler2D _WaveMap;
			float4 _WaveMap_ST;
			samplerCUBE _Cubemap;
			fixed _WaveXSpeed;
			fixed _WaveYSpeed;
			float _Distortion;	
			sampler2D _RefractionTex;
			//_RefractionTex纹理的像素大小，假设纹理大小为256*512，像素大小为（1/256,1/512）
			float4 _RefractionTex_TexelSize;

            struct a2v {
                float4 vertex : POSITION;
                float3 normal : NORMAL;
                float4 tangent : TANGENT;
                float4 texcoord : TEXCOORD0;
            };

            struct v2f {
				float4 pos : SV_POSITION;
				float4 srcPos : TEXCOORD0;
				float4 uv : TEXCOORD1;
				float3 TtoW0 : TEXCOORD2;  
				float3 TtoW1 : TEXCOORD3;  
				float3 TtoW2 : TEXCOORD4; 
				float3 worldPos:TEXCOORD5; 

			};

            v2f vert( a2v v ) {
				v2f o;
				o.pos = UnityObjectToClipPos(v.vertex);
				o.uv.xy = v.texcoord*_MainTex_ST.xy + _MainTex_ST.zw;
				o.uv.zw = v.texcoord*_WaveMap_ST.xy + _WaveMap_ST.zw;
				
				o.srcPos = ComputeGrabScreenPos(o.pos);

				o.worldPos = mul(unity_ObjectToWorld,v.vertex).xyz;
				float3 worldNormal = mul(v.normal,(float3x3)unity_WorldToObject);
				float3 worldTangent= mul((float3x3)unity_ObjectToWorld,v.tangent.xyz).xyz;
				float3 worldBinormal = cross(worldNormal,worldTangent.xyz)*v.tangent.w;
				
				o.TtoW0 = float3(worldTangent.x, worldBinormal.x, worldNormal.x);  
				o.TtoW1 = float3(worldTangent.y, worldBinormal.y, worldNormal.y);  
				o.TtoW2 = float3(worldTangent.z, worldBinormal.z, worldNormal.z);  

                return o;
            }
 
        
		fixed3 unpackNormal(fixed4 packedNormal)
		{
				fixed3 tangentNormal;
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
				return tangentNormal;
		}

			//反射
			float3 Reflect(float3 I,float3 normal)
			{
				//return  I - 2*normal*dot(normal,I);			
				return  I - 2*normal*mul(I,float3x1( normal.x,normal.y,normal.z));				
			}


        half4 frag(v2f i) : SV_Target {

				float3 viewDir = _WorldSpaceCameraPos.xyz - i.worldPos;
				viewDir = normalize(viewDir);
				float2 speed =_Time.y*float2(_WaveXSpeed,_WaveYSpeed);

				// Get the normal in tangent space
				fixed3 bump1 = unpackNormal(tex2D(_WaveMap,i.uv.zw + speed)).rgb;
				fixed3 bump2 = unpackNormal(tex2D(_WaveMap,i.uv.zw - speed)).rgb;
				fixed3 bump = normalize(bump1 + bump2);

				// Compute the offset in tangent space
				float2 offset = bump.xy*_Distortion*_RefractionTex_TexelSize.xy;
				i.srcPos.xy = offset*i.srcPos.z + i.srcPos.xy;
				fixed3 refrCol = tex2D(_RefractionTex,i.srcPos.xy/i.srcPos.w).rgb;

				// Convert the normal to world space
				float3x3 rotation = float3x3(i.TtoW0,i.TtoW1,i.TtoW2);
				bump = normalize(mul(rotation,bump));
				//bump = normalize(half3(dot(i.TtoW0.xyz, bump), dot(i.TtoW1.xyz, bump), dot(i.TtoW2.xyz, bump)));
				fixed4 texColor = tex2D(_MainTex, i.uv.xy + speed);
				fixed3 reflDir = Reflect(-viewDir, bump);
				fixed3 reflCol = texCUBE(_Cubemap, reflDir).rgb * texColor.rgb * _Color.rgb;
				
				fixed fresnel = pow(1 - saturate(dot(viewDir, bump)), 4);
				fixed3 finalColor = reflCol * fresnel + refrCol * (1 - fresnel);
				
                return fixed4(finalColor,1);
            }


        ENDCG
        }
    }
    FallBack "Diffuse"
}
```

效果：有损压缩了

  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/2018092712014978.png)  
