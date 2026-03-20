---
title: "Unity Assert断言工具"
subtitle: "Unity Assert断言工具"
date: 2021-04-16T19:57:20+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: []
categories: []
---

<!--more-->
> 断言工具   
> 特性 ` [Conditional("UNITY_ASSERTIONS")]`

**Asserts 有手动检查的一些优势:**  
- 简单易读的代码  
- 错误消息是 干净和 可读性强的 assert 错误消息  
- 默认情况下断言在 non-development模式 (你不需要使用预处理器), building 游戏时就扒掉。  

**断言在development下执行，非development 则代码自动删除**
**非development下如果要用则增加编译符号 `UNITY_ASSERTIONS`(Edit -> Project Settings -> Player的 Script Define Symbolsxx下增加),断言不中断执行,资产将只打印错误和会继续执行**
**如果你想要它只是作为exceptions(中断执行)，请确保从您的代码将 Assert.raiseExceptions 设置为 true.**

`Assert.cs`
```
using System;
using UnityEngine;
using UnityEngine.Assertions;
//using UnityEngine.Assertions.Must;
//using UnityEngine.Assertions.Comparers;


/// <summary>
///  Unity 断言
/// </summary>
public class Assert
{
    /// <summary>
    ///  Whether Unity should throw an exception on a failure.
    ///  是否抛出异常
    /// </summary>
    public static bool raiseExceptions
    {
        get
        {
            return UnityEngine.Assertions.Assert.raiseExceptions;
        }
        set
        {
            UnityEngine.Assertions.Assert.raiseExceptions = value;
        }
    }

    /// <summary>
    /// 期待的值为True
    ///  如果是condition是false 则抛出异常 msg
    /// </summary>
    /// <param name="condition">false 则抛出异常 msg</param>
    /// <param name="msg"></param>
    public static void IsTrue(bool condition,string msg=null)
    {
        UnityEngine.Assertions.Assert.IsTrue(condition, msg);
    }
    public static void IsTrue(bool condition, String format, params object[] args)
    {
        UnityEngine.Assertions.Assert.IsTrue(condition, string.Format(format, args));
    }
    public static void IsFalse(bool condition, string msg = null)
    {
        UnityEngine.Assertions.Assert.IsFalse(condition, msg);
    }
    public static void IsFalse(bool condition, String format, params object[] args)
    {
        UnityEngine.Assertions.Assert.IsFalse(condition, string.Format(format, args));
    }
    public static void IsNull<T>(T value, string message=null) where T : class
    {
        UnityEngine.Assertions.Assert.IsNull<T>(value, message);
    }
    public static void IsNull(UnityEngine.Object value, string message = null)
    {
        UnityEngine.Assertions.Assert.IsNull(value, message);
    }
    public static void IsNotNull<T>(T value, string message = null) where T : class
    {
        UnityEngine.Assertions.Assert.IsNotNull<T>(value, message);
    }
    public static void IsNotNull(UnityEngine.Object value, string message = null)
    {
        UnityEngine.Assertions.Assert.IsNotNull(value, message);
    }
}

```

>参考文章：[https://blog.csdn.net/u010019717/article/details/50375226](https://blog.csdn.net/u010019717/article/details/50375226)