---
title: "ProfilerHelper辅助工具"
date: "2020-12-13"
tags:
  - Unity
  - 工具链
  - 性能优化
  - CSharp
categories:
  - unityTool
comments: true
---
# ProfilerHelper辅助工具

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