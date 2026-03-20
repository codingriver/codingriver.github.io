---
title: "C# SynchronizationContext线程上下文简单说明"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["CSharp"]
categories: ["CSharp"]
---

<!--more-->



> SynchronizationContext线程上下文说明
> SynchronizationContext在通讯中充当传输者的角色，实现功能就是一个线程和另外一个线程的通讯
> 　那么SynchronizationContext的Send()和Post()
>　　Send() 是简单的在当前线程上去调用委托来实现（同步调用）。也就是在子线程上直接调用UI线程执行，等UI线程执行完成后子线程才继续执行。
>　Post() 是在线程池上去调用委托来实现（异步调用）。这是子线程会从线程池中找一个线程去调UI线程，子线程不等待UI线程的完成而直接执行自己下面的代码。

```
　	SynchronizationContext.Send(SendOrPostCallback d,object state);
　　SynchronizationContext.Post(SendOrPostCallback d,object state);
```

测试代码：
```csharp
using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace ContextTest
{
    class Program
    {

        static SynchronizationContext context;

        // 线程同步队列,发送接收socket回调都放到该队列,由poll线程统一执行
        //private  ConcurrentQueue<Action> queue = new ConcurrentQueue<Action>();
        /// <summary>
        /// 测试上下文同步
        /// SynchronizationContext
        /// </summary>
        /// <param name="args"></param>
        static void Main(string[] args)
        {

            context = new SynchronizationContext();
            Console.WriteLine("主线程id："+Thread.CurrentThread.ManagedThreadId);
            TestThread();
            Thread.Sleep(6000);
            Console.WriteLine("主线程执行");
            context.Send(EventMethod, "Send");
            context.Post(EventMethod, "Post");
            Console.WriteLine("主线程结束");
        }


        static void TestThread()
        {
            var thrd= new Thread(Start);
            thrd.Start();

        }

        static void Start()
        {
             
            Console.WriteLine("子线程id：" + Thread.CurrentThread.ManagedThreadId);
            context.Send(EventMethod, "子线程Send");
            context.Post(EventMethod, "子线程Post");
            Console.WriteLine("子线程结束");
        }


        static void EventMethod(object arg)
        {

            Console.WriteLine("CallBack::当前线程id：" + Thread.CurrentThread.ManagedThreadId+"     arg:"+(string)arg);


        }
    }
}

```

结果：

  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181025130928980.png)  


根据结果分下得出：
**Send是在当前线程执行的（同步）**
**Post是在新的线程执行的（异步）**
*其它的不同后面再补充*


>参考文章
>[梦琪小生
【C#】【Thread】SynchronizationContext线程间同步](https://www.cnblogs.com/mqxs/p/4288644.html)
