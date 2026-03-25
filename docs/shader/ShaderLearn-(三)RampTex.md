---
title: "ShaderLearn-(三)RampTex"
date: "2021-12-22"
tags:
  - Shader
  - 图形学
  - 网络
  - CSharp
categories:
  - shader
comments: true
---
# ShaderLearn-(三)RampTex

## TampTex
  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/ShaderLearn-(三)RampTex/20210419183653.png)  

> 构建uv坐标 `uv=float2(dot(N,L)*0.5+0.5,0.5)`，half lambert 构建uv的u坐标


```shader
/// Ramp Tex
Shader "SL/RampTex"
{
    Properties
    {
        _MainTex("Ramp Tex",2D)="white"{}
        _Color("Color",Color) = (1,1,1,1)
    }
        SubShader
    {
        Tags { "RenderType" = "Opaque" }
        LOD 100

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "AutoLight.cginc"

            struct appdata
            {
                float4 vertex : POSITION;
                float2 texcoord : TEXCOORD0;
                float3 normal:NORMAL;
            };

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 pos : SV_POSITION;
                float3 normal_dir : TEXCOORD1;
            };

            half4 _Color;
            sampler2D _MainTex;

            v2f vert(appdata v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv = v.texcoord;
                o.normal_dir = normalize(mul(v.normal, (float3x3)unity_WorldToObject));
                return o;
            }

            fixed4 frag(v2f i) : SV_Target
            {
                half3 normal_dir = normalize(i.normal_dir);
                half3 light_dir = normalize(_WorldSpaceLightPos0.xyz);

                half ndotl = dot(normal_dir, light_dir);

                half half_lambert = ndotl*0.5+0.5;

                half uv =half2(half_lambert,0.5);
                half3 col=tex2D(_MainTex,uv).rgb;

                fixed3 diffuse = col * _Color.rgb;
                return fixed4(diffuse,1.0);
            }
            ENDCG
        }
    }
}

```

> 参考及资源来源：[庄懂-BoyanTata](https://space.bilibili.com/6373917)  
> [庄懂公开课资源](https://github.com/BoyanTata/AP01)