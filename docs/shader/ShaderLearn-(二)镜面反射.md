---
title: "ShaderLearn (二)镜面反射"
subtitle: "镜面反射 Phong和Blinn Phong"
date: 2021-04-16T20:42:28+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: []
categories: []
draft: true
---

<!--more-->

### Phong高光反射
`pow(max(dot(v,r),0),_Gloss)`
```shader
Shader "SL/Phong"
{
    Properties
    {
        _Gloss("Gloss",range(3,256))=5
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
                float4 pos : SV_POSITION;
                float2 uv : TEXCOORD0;
                float3 pos_world : TEXCOORD1;
                float3 normal_dir : TEXCOORD2;
            };

            half _Gloss;

            v2f vert(appdata v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv = v.texcoord;
                o.pos_world = mul(unity_ObjectToWorld, v.vertex).xyz;
                o.normal_dir = normalize(mul(v.normal, (float3x3)unity_WorldToObject));

                return o;
            }

            fixed4 frag(v2f i) : SV_Target
            {
                half3 normal_dir = normalize(i.normal_dir);
                half3 view_dir = normalize(_WorldSpaceCameraPos.xyz - i.pos_world); // view的反方向
                half3 light_dir = normalize(_WorldSpaceLightPos0.xyz);
                half3 reflect_dir = reflect(light_dir, normal_dir);
               
                half rdotv = dot(reflect_dir, -view_dir);
                
                half phong = pow(max(0, rdotv), _Gloss);

                fixed specular = phong;

                return fixed4(specular.xxx,1.0);
            }
            ENDCG
        }
    }
}

```

### Blinn-Phong 高光反射
`pow(max(dot(n,h),0),_Gloss)`
```shader
/// Blinn Phong
Shader "SL/Phong-Blinn"
{
    Properties
    {
        _Gloss("Gloss",range(3,256)) = 5
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
                float4 pos : SV_POSITION;
                float2 uv : TEXCOORD0;
                float3 pos_world : TEXCOORD1;
                float3 normal_dir : TEXCOORD2;
            };

            half _Gloss;

            v2f vert(appdata v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv = v.texcoord;
                o.pos_world = mul(unity_ObjectToWorld, v.vertex).xyz;
                o.normal_dir = normalize(mul(v.normal, (float3x3)unity_WorldToObject));

                return o;
            }

            fixed4 frag(v2f i) : SV_Target
            {
                half3 normal_dir = normalize(i.normal_dir);
                half3 view_dir = normalize(_WorldSpaceCameraPos.xyz-i.pos_world); // view的反方向
                half3 light_dir = normalize(_WorldSpaceLightPos0.xyz);
                half3 half_dir = normalize(light_dir+ view_dir);

                half ndoth = dot(normal_dir, half_dir);

                half blinnphong = pow(max(0, ndoth), _Gloss);

                fixed specular = blinnphong;

                return fixed4(specular.xxx, 1.0);
                //return fixed4(ndoth,1.0);
            }
            ENDCG
        }
    }
}

```

>详细参考[Shader光照模型-高光反射](Shader光照模型-高光反射.md)  
> 参考及资源来源：[庄懂-BoyanTata](https://space.bilibili.com/6373917)  
> [庄懂公开课资源](https://github.com/BoyanTata/AP01)