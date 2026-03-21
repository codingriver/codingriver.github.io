# 泛光（Bloom）实现

Bloom 实现分为 4 步：

- 提取亮度阈值
- 降采样
- 升采样
- 合并

## `Bloom.shader`

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

    half4 frag_PreFilter(v2f_img i) : SV_Target
    {
        half4 d = _MainTex_TexelSize.xyxy * half4(-1,-1,1,1) * _BlurRadius;
        half4 color = 0;
        color += tex2D(_MainTex, i.uv);
        float br = max(max(color.r, color.g), color.b);
        br = max(0.0f, (br - _Threshold)) / max(br, 0.00001f);

        color = 0;
        color += tex2D(_MainTex, i.uv + d.xy);
        color += tex2D(_MainTex, i.uv + d.zy);
        color += tex2D(_MainTex, i.uv + d.xw);
        color += tex2D(_MainTex, i.uv + d.zw);
        color *= 0.25;
        color.rgb *= br;
        return color;
    }

    half4 frag_DownsampleBox(v2f_img i) : SV_Target
    {
        half4 d = _MainTex_TexelSize.xyxy * half4(-1,-1,1,1) * _BlurRadius;
        half4 s = 0;
        s += tex2D(_MainTex, i.uv + d.xy);
        s += tex2D(_MainTex, i.uv + d.zy);
        s += tex2D(_MainTex, i.uv + d.xw);
        s += tex2D(_MainTex, i.uv + d.zw);
        s *= 0.25;
        return s;
    }

    half4 frag_UpsampleBox(v2f_img i) : SV_Target
    {
        half4 d = _MainTex_TexelSize.xyxy * half4(-1,-1,1,1) * _BlurRadius;
        half4 color = 0;
        color += tex2D(_MainTex, i.uv + d.xy);
        color += tex2D(_MainTex, i.uv + d.zy);
        color += tex2D(_MainTex, i.uv + d.xw);
        color += tex2D(_MainTex, i.uv + d.zw);
        color *= 0.25;

        half4 color2 = tex2D(_BloomTex, i.uv);
        return color + color2;
    }

    half4 frag_Combine(v2f_img i) : SV_Target
    {
        half4 base_color = tex2D(_MainTex, i.uv);
        half4 bloom_color = tex2D(_BloomTex, i.uv);
        half3 final_color = base_color.rgb + bloom_color.rgb * _Intensity;
        return half4(final_color, 1.0);
    }
    ENDCG
}
```

## `Bloom.cs`

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[ExecuteInEditMode()]
[RequireComponent(typeof(Camera))]
public class Bloom : MonoBehaviour
{
    public Shader shader;
    private Material material;
    [Range(0, 10)] public float _Intensity = 1;
    [Range(0, 10)] public float _Threshold = 1;
    [Range(0, 5)] public float _BlurRadius = 1.0f;
    [Range(0, 9)] public int _Iteration = 4;

    private List<RenderTexture> ls;

    private void Awake()
    {
        if (shader == null)
        {
            shader = Shader.Find("Hidden/Bloom");
        }
    }
}
```

## 实现要点

- 先做阈值提取，保留高亮区域
- 通过降采样降低开销，并顺便模糊
- 通过升采样逐层合并结果
- 最后与原图叠加，形成 Bloom 效果
