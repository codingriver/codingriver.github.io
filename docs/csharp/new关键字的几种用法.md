---
title: "C#的new关键字的几种用法"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["CSharp"]
categories: ["CSharp"]
---

<!--more-->



一共有三种用法：
**在 C# 中，new 关键字可用作运算符、修饰符或约束。**
==1）new 运算符：用于创建对象和调用构造函数。这种大家都比较熟悉，没什么好说的了。==
==2）new 修饰符：在用作修饰符时，new 关键字可以显式隐藏从基类继承的成员。==
==3）new 约束：用于在泛型声明中约束可能用作类型参数的参数的类型。==

直接上代码：
```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace NewTest
{
    /*
     * a)     作为运算符用来创建一个对象和调用构造函数。
     * b)     作为修饰符。
     * c)      用于在泛型声明中约束可能用作类型参数的参数的类型。
     * 
     */

    class A
    {
        public A() { }
        public int data;
        public int Data { get { return data; } set { data = value; } }
        public int Data1 { get; set; }
        public virtual void Get()
        {
            Console.WriteLine("AAAAAAA");
        }
    }

    class B : A
    {
        public B():base() { }
        new public int data;
        new public int Data { get; set; }
        new public int Data1 { get; set; }
        new public void Get()
        {
            Console.WriteLine("BBBBBBB");
        }
    }
    class C<T> where T:new()
    {
    }
    class Program
    {
        static void Main(string[] args)
        {
            B b = new B();
            b.data = 10;
            b.Data = 12;
            b.Data1 = 13;
            Console.WriteLine($"B:::data:{b.data},Data:{b.Data},Data1:{b.Data1}");
            b.Get();
            A a = b ;
            Console.WriteLine($"A:::data:{a.data},Data:{a.Data},Data1:{a.Data1}");
            a.data = 100;
            a.Data = 120;
            a.Data1 = 130;
            Console.WriteLine($"A:::data:{a.data},Data:{a.Data},Data1:{a.Data1}");
            a.Get();
            Console.WriteLine($"B:::data:{b.data},Data:{b.Data},Data1:{b.Data1}");
            b.Get();
            C<B> c = new C<B>();
        }
    }
}

```
结果：

  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181102170340640.png)  


b断点调试结果：

  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181102170532964.png)  


这里说明下，重写父类的变量其实是重新定义了一个新的变量，变量名相同是把父类的变量隐藏了，会增加内存

>参考文章：
>[C#的new关键字的几种用法](https://www.cnblogs.com/lzxboke/p/8414776.html)