---
title: "UGUI Image 图片置灰"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Unity"]
categories: ["Unity"]
---

<!--more-->


置灰的关键代码：
```c
				//gray
				color.rgb = dot(color.rgb, fixed3(0.222, 0.707, 0.071));  //0.299, 0.587, 0.114

				//half gray = dot(color.rgb, fixed3(0.299, 0.0587, 0.114));
				//color.rgb = half3(gray, gray, gray);


```
这里是从官网下载对应内置shader，然后修改UI-Default


上完整的shader代码：
```c
// Unity built-in shader source. Copyright (c) 2016 Unity Technologies. MIT license (see license.txt)

Shader "Custom/UI-Gray"
{
    Properties
    {
        [PerRendererData] _MainTex ("Sprite Texture", 2D) = "white" {}
        _Color ("Tint", Color) = (1,1,1,1)

        _StencilComp ("Stencil Comparison", Float) = 8
        _Stencil ("Stencil ID", Float) = 0
        _StencilOp ("Stencil Operation", Float) = 0
        _StencilWriteMask ("Stencil Write Mask", Float) = 255
        _StencilReadMask ("Stencil Read Mask", Float) = 255

        _ColorMask ("Color Mask", Float) = 15

        [Toggle(UNITY_UI_ALPHACLIP)] _UseUIAlphaClip ("Use Alpha Clip", Float) = 0
    }

    SubShader
    {
        Tags
        {
            "Queue"="Transparent"
            "IgnoreProjector"="True"
            "RenderType"="Transparent"
            "PreviewType"="Plane"
            "CanUseSpriteAtlas"="True"
        }

        Stencil
        {
            Ref [_Stencil]
            Comp [_StencilComp]
            Pass [_StencilOp]
            ReadMask [_StencilReadMask]
            WriteMask [_StencilWriteMask]
        }

        Cull Off
        Lighting Off
        ZWrite Off
        ZTest [unity_GUIZTestMode]
        Blend SrcAlpha OneMinusSrcAlpha
        ColorMask [_ColorMask]

        Pass
        {
            Name "Default"
        CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma target 2.0

            #include "UnityCG.cginc"
            #include "UnityUI.cginc"

            #pragma multi_compile __ UNITY_UI_CLIP_RECT
            #pragma multi_compile __ UNITY_UI_ALPHACLIP

            struct appdata_t
            {
                float4 vertex   : POSITION;
                float4 color    : COLOR;
                float2 texcoord : TEXCOORD0;
                UNITY_VERTEX_INPUT_INSTANCE_ID
            };

            struct v2f
            {
                float4 vertex   : SV_POSITION;
                fixed4 color    : COLOR;
                float2 texcoord  : TEXCOORD0;
                float4 worldPosition : TEXCOORD1;
                UNITY_VERTEX_OUTPUT_STEREO
            };

            sampler2D _MainTex;
            fixed4 _Color;
            fixed4 _TextureSampleAdd;
            float4 _ClipRect;
            float4 _MainTex_ST;

            v2f vert(appdata_t v)
            {
                v2f OUT;
                UNITY_SETUP_INSTANCE_ID(v);
                UNITY_INITIALIZE_VERTEX_OUTPUT_STEREO(OUT);
                OUT.worldPosition = v.vertex;
                OUT.vertex = UnityObjectToClipPos(OUT.worldPosition);

                OUT.texcoord = TRANSFORM_TEX(v.texcoord, _MainTex);

                OUT.color = v.color * _Color;
                return OUT;
            }

            fixed4 frag(v2f IN) : SV_Target
            {
                half4 color = (tex2D(_MainTex, IN.texcoord) + _TextureSampleAdd) * IN.color;

                #ifdef UNITY_UI_CLIP_RECT
                color.a *= UnityGet2DClipping(IN.worldPosition.xy, _ClipRect);
                #endif

                #ifdef UNITY_UI_ALPHACLIP
                clip (color.a - 0.001);
                #endif

				//gray
				color.rgb = dot(color.rgb, fixed3(0.222, 0.707, 0.071));  //0.299, 0.587, 0.114

				//half gray = dot(color.rgb, fixed3(0.299, 0.0587, 0.114));
				//color.rgb = half3(gray, gray, gray);

                return color;
            }
        ENDCG
        }
    }
}

```

使用代码
```csharp
//=====================================================
// - FileName:      UIGray.cs
// - Created:       codingriver
//======================================================

using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// 图片置灰
/// </summary>
public static class UIGray {
    private static Material grayMat;

    /// <summary>
    /// 创建置灰材质球
    /// </summary>
    /// <returns></returns>
    private static Material GetGrayMat()
    {
        if(grayMat==null)
        {
            Shader shader = Shader.Find("Custom/UI-Gray");
            if(shader==null)
            {
                Debug.Log("null");
                return null;
            }
            Material mat = new Material(shader);
            grayMat = mat;
        }

        return grayMat;
    }

    /// <summary>
    /// 图片置灰
    /// </summary>
    /// <param name="img"></param>
    public static void SetUIGray(Image img)
    {
        img.material = GetGrayMat();
        img.SetMaterialDirty();
    }

    /// <summary>
    /// 图片回复
    /// </summary>
    /// <param name="img"></param>
    public static void Recovery(Image img)
    {
        img.material = null;
    }

}

```

效果：
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181123125022542.png)  
