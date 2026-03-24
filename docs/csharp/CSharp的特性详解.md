---
title: "C# 特性详解（Attribute）"
date: "2026-03-21"
tags:
  - CSharp
categories:
  - csharp
comments: true
---
# C# 特性详解（Attribute）

> 今天整理关于特性的资料，之前都忘了，今天整理一下。
>
> 参考《C#高级编程》第 10 版。

## 0X01 特性（Attribute）

### 特性定义

特性不会影响编译过程，因为编译器不能识别它们，但这些特性在应用于程序元素时，可以在编译好的程序集中用作元数据。

这里假设某个类上使用了特性如下：

```csharp
[Test]
class BBB
{
}
```

当编译器发现这个类 `BBB` 应用了 `Test` 特性时，首先会把字符串 `Attribute` 追加到这个名称后面，形成组合名称 `TestAttribute`，然后在搜索路径的所有名称空间中搜索有指定名称的类。

### 指定 AttributeUsage 特性

```csharp
public enum Flag
{
    None,
    Input,
    Output
}

[AttributeUsage(AttributeTargets.Class | AttributeTargets.Method | AttributeTargets.Constructor | AttributeTargets.ReturnValue | AttributeTargets.Assembly, AllowMultiple = true, Inherited = false)]
class TestAttribute : Attribute
{
    public TestAttribute(Flag flag = Flag.None)
    {
    }
}
```

### AttributeTargets 的常见说明

- `Assembly`
- `Module`
- `Class`
- `Struct`
- `Enum`
- `Constructor`
- `Method`
- `Property`
- `Field`
- `Event`
- `Interface`
- `Parameter`
- `Delegate`
- `ReturnValue`
- `GenericParameter`
- `All`

特性应用于 `Assembly` 或 `Module` 时，要这样写：

```csharp
[assembly: someAssemblyAttribute(Parameters)]
[module: someAssemblyAttribute(Parameters)]
```

### AllowMultiple 与 Inherited

- `AllowMultiple` 表示一个特性是否能够多次应用在同一项上
- `Inherited` 如果为 `true`，表示应用到类或者接口上的特性也自动应用到所有派生类或者接口上

```csharp
using AttributeTest;
using System;

[assembly: TestAttribute]
[module: TestAttribute]

namespace AttributeTest
{
    [AttributeUsage(AttributeTargets.All, AllowMultiple = true, Inherited = true)]
    class TestAttribute : Attribute
    {
        public int flag;
        public bool isInner;

        public TestAttribute(string arg = null)
        {
        }
    }

    [Test("class", flag = 3, isInner = true)]
    class Example
    {
    }
}
```

