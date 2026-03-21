---
title: "CSharp语言6-字符串插值"
date: "2026-03-21"
tags:
  - CSharp
  - 网络
categories:
  - csharp
comments: true
---
# CSharp语言6-字符串插值

string s = "hello";

string y = $"{s} world";

等同于使用Format方法：

string y = string.Format("{0} world",s);

并且我们可以调用值的方法，如：

string y = $"{s.ToLower()} world";

使用新的字符串格式代码可读性要好一些如：




```csharp
            int a = 1;
            int b = 2;
            string c = $"{a} + {b} = {a + b}";//使用$
            string d = string.Format("{0} + {1} = {2}", a, b, a + b);//使用Format
```

>
>参考文章
>https://blog.csdn.net/xc917563264/article/details/79348233 