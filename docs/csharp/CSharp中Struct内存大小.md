---
title: "CSharp中Struct内存大小"
date: "2026-03-21"
tags:
  - CSharp
  - 网络
  - 项目记录
categories:
  - csharp
comments: true
---
# CSharp中Struct内存大小

> `sizeof` 只适用于值类型，并且需要在unsafe上下文环境中使用  
> 也可以使用 `System.Runtime.InteropServices.Marshal.SizeOf() `

- 新建C#控制台项目，项目设置 `unsafe`  允许不安全代码  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/CSharp中Struct内存大小/20210716163908.png)  


`Program.cs`
```
using System;

namespace test
{
    class Program
    {
        public struct A //size 8=a(4)+b(4)
        {
            public char a;
            public int b;
        }
        public unsafe struct B  //size 12=a(4)+b(4)+c(4)
        {
            public char a;
            public int b;
            public byte c;
        }

        public struct C //size 8=a(2)+c(2)+b(4)
        {
            public char a;

            public byte c;
            public int b;
        }

        public struct D //size 2=a(2)
        {
            public char a;
        }

        static void Main(string[] args)
        {
            TestSize();
        }
        static unsafe void TestSize()
        {
            //A :8,B :12,C :8,D :2
            Console.WriteLine($"A :{sizeof(A)},B :{sizeof(B)},C :{sizeof(C)},D :{sizeof(D)}");
            
        }

    }
}

```



> ref: [C#中sizeof的用法](https://www.cnblogs.com/darrenji/p/3976029.html)  
> ref: [C#sizeof用法](https://blog.csdn.net/qq_36724994/article/details/81254709)  
> 详细参考:[C++ struct union数据对齐](../u3d/c++_structunion数据对齐.md)