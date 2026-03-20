---
title: "C# 闭包Closure"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["CSharp"]
categories: ["CSharp"]
---

<!--more-->


>考虑了下，还是记录下吧 ，要不然以后又忘了
>参考文章：
>[C#与闭包](https://www.cnblogs.com/jujusharp/archive/2011/08/04/2127999.html)

```csharp

public class TCloser{
public Func<int> T1()
    {
        var n = 999;
        Func<int> result = () =>
        {
            return n;
        };
 
        n = 10;
        return result;
    }
 
    public dynamic T2()
    {
        var n = 999;
        dynamic result =new { A = n };
        n = 10;
        return result;
    }
    static void Main(){
        var a = new TCloser();
        var b = a.T1();
        var c = a.T2();
        Console.WriteLine(b());
        Console.WriteLine(c.A);
    }
} 
```
返回结果：

  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181011234652734.png)  

**因为闭包的特性，这里匿名函数中所使用的变量就是实际T1中的变量，与之相反的是，匿名对象result里面的A只是初始化时被赋予了变量n的值，它并不是n，所以后面n改变之后A并未随之而改变。这正是闭包的魔力所在。**
还有就是像T1方法带upvalue的返回函数其实IL中返回的是一个类，将变量n作为类的一个属性去处理的




