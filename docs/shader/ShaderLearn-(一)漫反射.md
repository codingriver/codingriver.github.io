---
title: "ShaderLearn-(一)漫反射"
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
# ShaderLearn-(一)漫反射

### 兰伯特（Lambert）
`max(0,dot(N,L))`  
或者`saturate(dot(N,L))`
  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/ShaderLearn-漫反射(一)/20210419183005.png)  
```shader
Shader "SL/Lambert"
{
    Properties
    {
        _Color("Color",Color)=(1,1,1,1)
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
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

            v2f vert (appdata v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv = v.texcoord;
                o.normal_dir = normalize( mul(v.normal, (float3x3)unity_WorldToObject));
                return o;
            }

            fixed4 frag(v2f i) : SV_Target
            {
                half3 normal_dir = normalize(i.normal_dir);
                half3 light_dir = normalize(_WorldSpaceLightPos0.xyz);

                half ndotl = dot(normal_dir, light_dir);

                half lambert = max(0, ndotl);

                fixed3 diffuse = lambert * _Color.rgb;

                return fixed4(diffuse,1.0);
            }
            ENDCG
        }
    }
}

```

### 半兰伯特（Half Lambert）
`dot(n,l)*0.5+0.5`  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/ShaderLearn-漫反射(一)/20210419183039.png)  
```shader
// Half-Lambert
Shader "SL/Lambert-Half"
{
    Properties
    {
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

                fixed3 diffuse = half_lambert * _Color.rgb;

                return fixed4(diffuse,1.0);
            }
            ENDCG
        }
    }
}


```

>详细可参考[【Shader】 光照模型-漫反射](Shader光照模型-漫反射.md)  
> 参考及资源来源：[庄懂-BoyanTata](https://space.bilibili.com/6373917)  
> [庄懂公开课资源](https://github.com/BoyanTata/AP01)