
---
title: "C#-Unicode编码和中文互转"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Unicode编码"]
categories: ["计算机基础"]
---

<!--more-->


**直接上代码**
```
//=====================================================
// - FileName:    	UnicodeTools 
// - Description:
// - Author:		wangguoqing
// - Email:			wangguoqing@hehemj.com
// - Created:		2018/3/2 17:17:50
// - CLR version: 	4.0.30319.42000
// - UserName:		Wang
// -  (C) Copyright 2008 - 2015, hehehuyu,Inc.
// -  All Rights Reserved.
//======================================================

using System;
using System.Text;
/// <summary>
/// Unicode编码和中文互转
/// 这里的Unicode编码是Unicode Big Endian (UCS-2 Big Endian)
/// </summary>
class UnicodeTools
{

    /// <summary>
    /// 标准unicode编码
    /// </summary>
    /// <param name="text"></param>
    /// <returns></returns>
    public static string EncodeString(string text)
    {
        if (string.IsNullOrEmpty(text))
        {
            return string.Empty;
        }
        int len = text.Length;
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < len; i++)
        {
            builder.Append("\\u");
            builder.Append(UShortToHex((ushort)text[i]));
        }
        return builder.ToString();
    }
    /// <summary>
    /// 编码Unicode
    /// </summary>
    /// <param name="text">原字符串</param>
    /// <returns>unicode编码</returns>
    public static string EncodeString1(string text)
    {
        if (string.IsNullOrEmpty(text))
        {
            return string.Empty;
        }
        var bytes = Encoding.Unicode.GetBytes(text);
        int len = bytes.Length;
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < len; i += 2)
        {
            builder.Append("\\u");
            builder.Append(bytes[i + 1].ToString("x2"));
            builder.Append(bytes[i].ToString("x2"));
        }
        return builder.ToString();
    }

    public static string EncodeString2(string text)
    {
        if (string.IsNullOrEmpty(text))
        {
            return string.Empty;
        }
        int len = text.Length;
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < len; i++)
        {
            builder.Append("\\u");
            builder.Append(((ushort)text[i]).ToString("x4"));
        }
        return builder.ToString();
    }


    private static char[] UShortToHex(ushort n)
    {
        int num;
        char[] hex = new char[4];
        for (int i = 0; i < 4; i++)
        {
            num = n % 16;

            if (num < 10)
                hex[3 - i] = (char)('0' + num);
            else
                hex[3 - i] = (char)('A' + (num - 10));

            n >>= 4;
        }
        return hex;
    }
    private static char[] UShortToHexE(ushort n)
    {
        var hex = n.ToString("x").ToCharArray();
        return hex;
    }

    public static string DecodeString(string unicode)
    {
        if (string.IsNullOrEmpty(unicode))
        {
            return string.Empty;
        }
        //string[] ls = unicode.Replace("\\", "").Split(new char[]{'u'},StringSplitOptions.RemoveEmptyEntries);
        string[] ls = unicode.Split(new string[] { "\\u" }, StringSplitOptions.RemoveEmptyEntries);
        StringBuilder builder = new StringBuilder();
        int len = ls.Length;
        for (int i = 0; i < len; i++)
        {
            //builder.Append((Char)ushort.Parse(ls[i], System.Globalization.NumberStyles.HexNumber));
            builder.Append(Convert.ToChar(ushort.Parse(ls[i], System.Globalization.NumberStyles.HexNumber)));

        }
        return builder.ToString();
    }

    
    /// <summary>
    /// 这种只能解出标准unicode编码
    /// </summary>
    /// <param name="unicode"></param>
    /// <returns></returns>
    public static string DecodeString1(string unicode)
    {
        if (string.IsNullOrEmpty(unicode))
        {
            return string.Empty;
        }
        return System.Text.RegularExpressions.Regex.Unescape(unicode);
    }
    
}



```
**测试**
```c++
            string s = "天空测试s";
            Console.WriteLine(UnicodeTools.EncodeString(s));
            Console.WriteLine(UnicodeTools.EncodeString1(s));
            Console.WriteLine(UnicodeTools.EncodeString2(s));
            Console.WriteLine(UnicodeTools.DecodeString(UnicodeTools.EncodeString(s)));
            Console.WriteLine(UnicodeTools.DecodeString(UnicodeTools.EncodeString1(s)));
            Console.WriteLine(UnicodeTools.DecodeString(UnicodeTools.EncodeString2(s)));
            Console.WriteLine(UnicodeTools.DecodeString1(UnicodeTools.EncodeString(s)));
            Console.WriteLine(UnicodeTools.DecodeString1(UnicodeTools.EncodeString1(s)));
            Console.WriteLine(UnicodeTools.DecodeString1(UnicodeTools.EncodeString2(s)));
```
**结果**


![结果.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-0b66f358f0fa5f41.png)  


