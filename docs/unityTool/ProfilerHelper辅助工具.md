---
title: "ProfilerHelper辅助工具"
subtitle: "ProfilerHelper辅助工具"
date: 2020-09-17T21:46:14+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
draft: true
tags: ["Unity Tool"]
categories: ["Unity Tool"]
---

<!--more-->

>Unity Profiler分析辅助类

`ProfilerHelper.cs`代码 ：

```csharp
using UnityEngine.Profiling;

public static class ProfilerHelper
{

    public static bool UseProfiler = false;    public static bool UseStringFormatProfiler = true;

    public static void BeginSample(string name)
    {
        if (!UseProfiler)
            return;

        Profiler.BeginSample(name);
    }
    public static void BeginSample(string name,params object[] param)
    {
        if (!UseProfiler)
            return;
        if (!UseStringFormatProfiler)
            return;

        name = string.Format(name, param);
        Profiler.BeginSample(name);
    }



    public static void EndSample()
    {
        if (!UseProfiler)
            return;
        Profiler.EndSample();
    }

}


```