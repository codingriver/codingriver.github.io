---
title: "泛光（Bloom）实现"
date: 2021-08-09T20:28:47+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
draft: false
tags: []
categories: []
---

<!--more-->

Bloom实现分为4步：
- 提取亮度阈值
- 降采样
- 升采样
- 合并

`Bloom.shader`
```c
Shader "Hidden/Bloom"
{
	Properties
	{
		_MainTex("Texture", 2D) = "white" {}
		_BlurOffset("BlurOffset",Float) = 1
	}

	CGINCLUDE
	#include "UnityCG.cginc"

	sampler2D _MainTex;
	sampler2D _BloomTex;
	float4 _MainTex_TexelSize;
	float _Threshold;
	float _Intensity;
	float _BlurRadius;

	//阈值
	half4 frag_PreFilter(v2f_img i) : SV_Target
	{
		//提取阈值
		half4 d = _MainTex_TexelSize.xyxy * half4(-1,-1,1,1)* _BlurRadius;
		half4 color = 0;
		color += tex2D(_MainTex, i.uv);
		float br = max(max(color.r, color.g), color.b);
		br = max(0.0f, (br - _Threshold)) / max(br,0.00001f);

		//降采样
		color = 0;
		color += tex2D(_MainTex, i.uv + d.xy);
		color += tex2D(_MainTex, i.uv + d.zy);
		color += tex2D(_MainTex, i.uv + d.xw);
		color += tex2D(_MainTex, i.uv + d.zw);
		color *= 0.25;
		color.rgb *= br;
		return color;
	}
	//降采样模糊,BoxBlur
	half4 frag_DownsampleBox(v2f_img i) : SV_Target
	{
		half4 d = _MainTex_TexelSize.xyxy * half4(-1,-1,1,1)* _BlurRadius;
		half4 s = 0;
		s += tex2D(_MainTex, i.uv + d.xy);
		s += tex2D(_MainTex, i.uv + d.zy);
		s += tex2D(_MainTex, i.uv + d.xw);
		s += tex2D(_MainTex, i.uv + d.zw);
		s *= 0.25;
		return s;
	}

	//升采样模糊,BoxBlur
	half4 frag_UpsampleBox(v2f_img i) : SV_Target
	{
		half4 d = _MainTex_TexelSize.xyxy * half4(-1,-1,1,1)* _BlurRadius;
		half4 color = 0;
		color += tex2D(_MainTex, i.uv + d.xy);
		color += tex2D(_MainTex, i.uv + d.zy);
		color += tex2D(_MainTex, i.uv + d.xw);
		color += tex2D(_MainTex, i.uv + d.zw);
		color *= 0.25;

		half4 color2 = tex2D(_BloomTex, i.uv);
		return color + color2;
	}



	//合并
	half4 frag_Combine(v2f_img i) : SV_Target
	{
		half4 base_color = tex2D(_MainTex, i.uv);
		half4 bloom_color = tex2D(_BloomTex, i.uv);

		half3 final_color = base_color.rgb + bloom_color.rgb * _Intensity;
		return half4(final_color,1.0);
	}

	ENDCG


	SubShader
	{
		Cull Off ZWrite Off ZTest Always
		//0 阈值
		Pass
		{
			CGPROGRAM
			#pragma vertex vert_img
			#pragma fragment frag_PreFilter
			ENDCG
		}
		//1 降采样模糊
		Pass
		{
			CGPROGRAM
			#pragma vertex vert_img
			#pragma fragment frag_DownsampleBox
			ENDCG
		}
		//2 升采样模糊
		Pass
		{
			CGPROGRAM
			#pragma vertex vert_img
			#pragma fragment frag_UpsampleBox
			ENDCG
		}
		//3 合并
		Pass
		{
			CGPROGRAM
			#pragma vertex vert_img
			#pragma fragment frag_Combine
			ENDCG
		}
	}
}

```

`Bloom.cs`

```c
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[ExecuteInEditMode()]
[RequireComponent(typeof(Camera))]
public class Bloom : MonoBehaviour
{
    public Shader shader;
    private Material material;
    [Range(0, 10)]
    public float _Intensity = 1;
    [Range(0, 10)]
    public float _Threshold = 1;
    [Range(0, 5)]
    public float _BlurRadius = 1.0f;
    [Range(0, 9)]
    public int _Iteration = 4;

    private List<RenderTexture> ls;
    private void Awake()
    {
        if (shader == null)
        {
            shader = Shader.Find("Hidden/Bloom");
        }
    }
    void OnEnable()
    {
        if (shader == null || shader.isSupported == false)
        {
            enabled = false;
            return;
        }
        if (material == null)
        {
            material = new Material(shader);
        }
        if (ls == null)
        {
            ls = new List<RenderTexture>(_Iteration);
        }

    }
   const RenderTextureFormat format= RenderTextureFormat.DefaultHDR;
    void OnRenderImage(RenderTexture source, RenderTexture destination)
    {
        float intensity = Mathf.Exp(_Intensity / 10.0f * 0.693f) - 1.0f;
        material.SetFloat("_Intensity", intensity);
        material.SetFloat("_Threshold", _Threshold);
        material.SetFloat("_BlurRadius", _BlurRadius);

        if (_Iteration == 0 || intensity == 0 || _BlurRadius == 0)
        {
            Graphics.Blit(source, destination);
            return;
        }

        int width = (int)(source.width / 2);
        int height = (int)(source.height / 2);
        RenderTexture RT1, RT2;
        
        RT1 = RenderTexture.GetTemporary(width, height, 0, format);

        //提取亮度阈值
        Graphics.Blit(source, RT1, material, 0); //这里提取阈值且进行一次降采样
        ls.Add(RT1);

        //降采样
        for (int i = 0; i < _Iteration - 1; i++)
        {
            width /= 2; height /= 2;
            RT2 = RenderTexture.GetTemporary(width, height, 0, format);
            Graphics.Blit(RT1, RT2, material, 1);
            ls.Add(RT1 = RT2);
        }

        //升采样
        for (int i = _Iteration - 1; i >= 1; i--)
        {
            width *= 2; height *= 2;
            material.SetTexture("_BloomTex", ls[i - 1]);
            RT2 = RenderTexture.GetTemporary(width, height, 0, format);
            Graphics.Blit(RT1, RT2, material, 2);
            ls.Add(RT1 = RT2);
        }

        //合并
        material.SetTexture("_BloomTex", RT1);
        Graphics.Blit(source, destination, material, 3);

        // Release
        for (int i = 0; i < ls.Count; i++)
        {
            RenderTexture.ReleaseTemporary(ls[i]);
        }
        ls.Clear();
    }
}

```

开启Bloom的效果：  
![](../images/ZfxJF5EeY8nGhMs.png)  

没有开Bloom的效果：  
![20210809203405](../images/IVftH8ix1aA4guh.png)