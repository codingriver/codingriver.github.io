---
title: "C# async与await的使用说明"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["CSharp"]
categories: ["CSharp"]
---

<!--more-->

>C# 异步编程提供了两个关键字，async 和await，这里说明下怎么用
>C# 5 引入了一种简便方法，即异步编程。==此方法利用了 .NET Framework 4.5 及更高版本==、.NET Core 和 Windows 运行时中的异步支持。 编译器可执行开发人员曾进行的高难度工作，且应用程序保留了一个类似于同步代码的逻辑结构。 因此，你只需做一小部分工作就可以获得异步编程的所有好处。


本主题概述了何时以及如何使用异步编程，并包括指向包含详细信息和示例的支持主题的链接。
测试环境：vs2017，.Net Framework4.6.1。

**用法**
async 用在方法定义前面，await只能写在带有async标记的方法中。
==注意await异步等待的地方，await后面的代码和前面的代码执行的线程可能不一样==
==async关键字创建了一个状态机，类似yield return 语句；await会解除当前线程的阻塞，完成其他任务==

####  0X01 简单用法
**测试代码**
```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace AsyncAndAwait_Test
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("主线程ManagedThreadId:" + Thread.CurrentThread.ManagedThreadId);
            AsyncTest();
        }

        static async void AsyncTest()
        {
            Console.WriteLine("*******Start************ManagedThreadId:" + Thread.CurrentThread.ManagedThreadId);
            Task<int> taskA=  Print();
            Console.WriteLine("*********Middle**********ManagedThreadId:" + Thread.CurrentThread.ManagedThreadId);
            int a = await taskA;
            Console.WriteLine("*********End**********ManagedThreadId:" + Thread.CurrentThread.ManagedThreadId);
        }


        static Task<int> Print()
        {
            var tcs = new TaskCompletionSource<int>();
            var thrd = new Thread(() =>
            {
                Console.WriteLine("子线程ManagedThreadId:" + Thread.CurrentThread.ManagedThreadId);
                for (int i = 0; i < 3; i++)
                {
                    Console.WriteLine("===========等待==========" + i);
                    System.Threading.Thread.Sleep(1000);
                }
                tcs.SetResult(99);

            });
            thrd.Start();
            return tcs.Task;
        }
    }
}

```

结果

  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181024123829263.png)  


这里的结果红框这个地方线程id变了，按照我的理解是异步调用await前面代码的线程和await后面代码的线程可能不一样

再看一个测试例子
```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace AsyncAndAwait_Test
{
    class Program
    {
        /// <summary>
        /// async 和await 实践测试
        /// </summary>
        /// <param name="args"></param>
        static void Main(string[] args)
        {
            
            var tcs1 = new TaskCompletionSource<int>();
            var tcs2 = new TaskCompletionSource<int>();
            Console.WriteLine("主线程ManagedThreadId:" + Thread.CurrentThread.ManagedThreadId);
            AsyncTest(tcs1,tcs2);

            Thread.Sleep(1000);
            tcs1.SetResult(100);

            Thread.Sleep(5000);
            tcs2.SetResult(100);
            Console.WriteLine("主线程结束ManagedThreadId:" + Thread.CurrentThread.ManagedThreadId);
        }
        static async void AsyncTest(TaskCompletionSource<int> tcs1, TaskCompletionSource<int> tcs2)
        {
            Console.WriteLine("AsyncTest方法执行的线程id:" + Thread.CurrentThread.ManagedThreadId);
            //await后线程出现变化，异步执行（线程id不一样）
            int a = await Print();
            Console.WriteLine("11****await tcs3后的线程id:" + Thread.CurrentThread.ManagedThreadId);
            //await后的线程没有变化，是因为SetResult比较早，这里可以直接同步执行（我认为的）
            int b = await tcs1.Task;
            Console.WriteLine("22****await tcs1后的线程id:" + Thread.CurrentThread.ManagedThreadId);
            //await后线程出现变化，异步执行（线程id不一样）
            int c= await tcs2.Task;
            Console.WriteLine("33****await tcs2后的线程id：" + Thread.CurrentThread.ManagedThreadId);
        }


        static Task<int> Print()
        {
            var tcs3 = new TaskCompletionSource<int>();
            var thrd = new Thread(() =>
            {
                Console.WriteLine("子线程ManagedThreadId:" + Thread.CurrentThread.ManagedThreadId);
                for (int i = 0; i < 3; i++)
                {
                    Console.WriteLine("===========等待==========" + i);
                    System.Threading.Thread.Sleep(1000);
                }
                tcs3.SetResult(99);

            });
            thrd.Start();
            return tcs3.Task;
        }
    }
}

```
结果：

  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181024130744619.png)  

*代码里面await用法，这里异步返回的是一个`Task<int>`类型，通过await等待Task执行完成后返回的是int，或者返回的是T模板*

根据结果总结结论如下：
**如果执行到await时TaskCompletionSource没有设置SetResult、SetCanceled、SetException中的一个则await后面的线程可能出现变化（异步操作）**
**如果执行到await时TaskCompletionSource有设置SetResult、SetCanceled、SetException中的一个则await后面的线程不变化（同步操作）**

####  0X02 深入用法
```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace AsyncAwaitTest
{
    class Program
    {
        static void Main(string[] args)
        {

            Main1();
            Main2();
        }


        static void Main1()
        {
            AsyncMethod1();
            Console.WriteLine("Main finished!!!");
            //这里是为了处理Task启动一个后台线程的问题，主线程结束时，后台线程自动关闭
            Thread.Sleep(5000);
        }
        static async void AsyncMethod1()
        {
            Console.WriteLine("主线程id:" + Thread.CurrentThread.ManagedThreadId);


            //切换线程等待完成
            string res = await Task.Run<string>( () =>{
                Thread.Sleep(1000);
                Console.WriteLine("func thread id:" + Thread.CurrentThread.ManagedThreadId);
                return "hello";
            });

            Console.WriteLine("AsyncMethod finished!!!");

        }

        /// <summary>
        /// 
        /// </summary>
        static void Main2()
        {
            Console.WriteLine("===============================================");
            AsyncMethod2();
            Console.WriteLine("Main2 finished!!!");
            //这里是为了处理Task启动一个后台线程的问题，主线程结束时，后台线程自动关闭
            Thread.Sleep(5000);
        }
        /// <summary>
        /// 两个task同时执行
        /// </summary>
        static async void AsyncMethod2()
        {
            Task<string> t1 = GreetingAsync("Wang",500);
            Task<string> t2 = GreetingAsync("Codingriver");
            //两个异步task同时执行，直到所有task执行完 await才返回
            await Task.WhenAll(t1, t2);
            Console.WriteLine("result:::" + t1.Result + "    " + t2.Result);
        }




        static Task<string>GreetingAsync(string name,int time=1000)
        {
            return Task.Run<string>(()=>{
                Thread.Sleep(time);
                return Greeting(name);
            });
        }

        static string Greeting(string name)
        {
            return "Hello " + name;
        }
    }
}

```
结果：

  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181026233027235.png)  


**异步的异常捕获需要注意的是要将异步await放在try catch块中，且返回Task泛型，大概是这个意思**
捕获多个异步的异常例子：
```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace AsyncAwaitTest
{
    class Program
    {
        static void Main(string[] args)
        {
            TestMoreTaskException();
        }




        static async void TestMoreTaskException()
        {

            Task results=null;
            try
            {

                Task<string> t1 = GreetingAsync(null, 500);
                Task<string> t2 = GreetingAsync("Codingriver");
                //两个异步task同时执行，直到所有task执行完 await才返回
                await(results= Task.WhenAll(t1, t2));
                Console.WriteLine("TestMoreTaskException");


            }
            catch (Exception ex)
            {
                //AggregateException
                Console.WriteLine("Exception:::::::::" + ex.ToString());
                foreach (var item in results.Exception.InnerExceptions)
                {
                    Console.WriteLine("InnerException:::::::::" + item.ToString());
                }
            }

        }
        static Task<string> GreetingAsync(string name, int time = 1000)
        {
            return Task.Run<string>(() =>
            {
                Thread.CurrentThread.IsBackground = false;
                Thread.Sleep(time);
                throw new Exception("codingriver test");
                return string.Empty;
            });
        }
    }
}

```
结果：

  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181026234605830.png)  


>参考文章
>[使用 Async 和 Await 的异步编程 (C#)](https://www.cnblogs.com/cncc/articles/7998956.html)

