---
title: "C# async与await的使用说明"
date: "2026-03-21"
tags:
  - CSharp
  - 异步编程
categories:
  - csharp
comments: true
---
# C# async与await的使用说明

> C# 异步编程提供了两个关键字，`async` 和 `await`，这里说明下怎么用。
>
> C# 5 引入了一种简便方法，即异步编程。此方法利用了 .NET Framework 4.5 及更高版本、.NET Core 和 Windows 运行时中的异步支持。编译器可执行开发人员曾进行的高难度工作，且应用程序保留了一个类似于同步代码的逻辑结构。因此，只需做一小部分工作就可以获得异步编程的所有好处。

本主题概述了何时以及如何使用异步编程，并包括指向包含详细信息和示例的支持主题的链接。

测试环境：vs2017，.Net Framework 4.6.1。

## 用法

`async` 用在方法定义前面，`await` 只能写在带有 `async` 标记的方法中。

- 注意 `await` 异步等待的地方，`await` 后面的代码和前面的代码执行的线程可能不一样
- `async` 关键字创建了一个状态机，类似 `yield return` 语句；`await` 会解除当前线程的阻塞，完成其他任务

### 0X01 简单用法

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

这里的结果红框这个地方线程 id 变了，按照我的理解是异步调用 `await` 前面代码的线程和 `await` 后面代码的线程可能不一样。

再看一个测试例子：

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
            int a = await Print();
            Console.WriteLine("11****await tcs3后的线程id:" + Thread.CurrentThread.ManagedThreadId);
            int b = await tcs1.Task;
            Console.WriteLine("22****await tcs1后的线程id:" + Thread.CurrentThread.ManagedThreadId);
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

代码里面 `await` 用法，这里异步返回的是一个 `Task<int>` 类型，通过 `await` 等待 `Task` 执行完成后返回的是 `int`，或者返回的是 `T` 模板。

根据结果总结如下：

- 如果执行到 `await` 时 `TaskCompletionSource` 没有设置 `SetResult`、`SetCanceled`、`SetException` 中的一个，则 `await` 后面的线程可能出现变化（异步操作）
- 如果执行到 `await` 时 `TaskCompletionSource` 有设置 `SetResult`、`SetCanceled`、`SetException` 中的一个，则 `await` 后面的线程不变化（同步操作）
