---
title: "C# 特性详解（Attribute）"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["CSharp"]
categories: ["CSharp"]
---

<!--more-->

>今天整理关于特性的资料，之前都忘了，今天整理一下
>参考《C#高级编程》第10版 


####  0X01 特性（Attribute）

### 特性定义
*特性不会影响编译过程，因为编译器不能识别它们，但这些特性在应用于程序元素时，可以在编译好的程序集中用作元数据*
上面这句话是书上说的，但不太认可，如果通过反射来使用特性呢

这里假设某个类上使用了特性如下：
```csharp
    [Test]
    class BBB
    {    }
```
当编译器发现这个类`BBB`应用了Test特性时，首先会把字符串Attribute追加到这个名称后面，形成一个组合名称
`TestAttribute`，然后在其搜索路径的所有名称空间 （即using使用的命名空间）中搜索有指定名称的类，如果特性本身已Attribute结尾，编译器就不会再追加Attritude了，而是不修改该特性名。如下
```csharp
    [TestAttritude]
    class BBB
    {    }
```
编译器会找到含有该名称的类（`TestAttribute`），且这个类直接或者间接派生自System.Attribute。编译器还人为这个类包含控制特性用法的信息。
现在来看这个类的定义
```csharp
    public enum Flag
    {
        None,
        Input,
        Output
    }
    [AttributeUsage(AttributeTargets.Class | AttributeTargets.Method | AttributeTargets.Constructor | AttributeTargets.ReturnValue | AttributeTargets.Assembly,AllowMultiple=true,Inherited=false)]
    class TestAttribute:Attribute
    {

        public TestAttribute(Flag flag = Flag.None)
        {

        }

    }

```
### 指定AttributeUsage特性
**引申：**
特性（Attribute）本身用特性（`System.AttributeUsage`）来标记，C#编译器为它提供了特殊支持，其实`AttributeUsage`不能认为是一个特性了，应该理解为==元特性==，它只能用来标记特性类，不能标记其它的类。
**使用：**
`AttributeUsage`主要用于标识自定义特性可以应用到哪些类型的程序元素上。这些信息由它的第一个参数给出（`AttributeTargets`），像上面使用的一样。

`AttributeTargets`的定义
```csharp
    public sealed class AttributeUsageAttribute : Attribute
    {
        // 摘要: 
        //     用指定的 System.AttributeTargets、System.AttributeUsageAttribute.AllowMultiple
        //     值和 System.AttributeUsageAttribute.Inherited 值列表初始化 System.AttributeUsageAttribute
        //     类的新实例。
        //
        // 参数: 
        //   validOn:
        //     使用按位"或"运算符组合的一组值，用于指示哪些程序元素是有效的。
        public AttributeUsageAttribute(AttributeTargets validOn);

        // 摘要: 
        //     获取或设置一个布尔值，该值指示能否为一个程序元素指定多个指示属性实例。
        //
        // 返回结果: 
        //     如果允许指定多个实例，则为 true；否则为 false。 默认值为 false。
        public bool AllowMultiple { get; set; }
        //
        // 摘要: 
        //     获取或设置一个布尔值，该值指示指示的属性能否由派生类和重写成员继承。
        //
        // 返回结果: 
        //     如果该属性可由派生类和重写成员继承，则为 true，否则为 false。 默认值为 true。
        public bool Inherited { get; set; }
        //
        // 摘要: 
        //     获取一组值，这组值标识指示的属性可应用到的程序元素。
        //
        // 返回结果: 
        //     一个或多个 System.AttributeTargets 值。 默认值为 All。
        public AttributeTargets ValidOn { get; }
    }
```
AttributeTargets的定义
```csharp
    // 摘要: 
    //     指定可以对它们应用特性的应用程序元素。
    [Serializable]
    [ComVisible(true)]
    [Flags]
    public enum AttributeTargets
    {
        // 摘要: 
        //     可以对程序集应用属性。
        Assembly = 1,
        //
        // 摘要: 
        //     可以对模块应用属性。
        Module = 2,
        //
        // 摘要: 
        //     可以对类应用属性。
        Class = 4,
        //
        // 摘要: 
        //     可以对结构应用属性，即值类型。
        Struct = 8,
        //
        // 摘要: 
        //     可以对枚举应用属性。
        Enum = 16,
        //
        // 摘要: 
        //     可以对构造函数应用属性。
        Constructor = 32,
        //
        // 摘要: 
        //     可以对方法应用属性。
        Method = 64,
        //
        // 摘要: 
        //     可以对属性 (Property) 应用属性 (Attribute)。
        Property = 128,
        //
        // 摘要: 
        //     可以对字段应用属性。
        Field = 256,
        //
        // 摘要: 
        //     可以对事件应用属性。
        Event = 512,
        //
        // 摘要: 
        //     可以对接口应用属性。
        Interface = 1024,
        //
        // 摘要: 
        //     可以对参数应用属性。
        Parameter = 2048,
        //
        // 摘要: 
        //     可以对委托应用属性。
        Delegate = 4096,
        //
        // 摘要: 
        //     可以对返回值应用属性。
        ReturnValue = 8192,
        //
        // 摘要: 
        //     可以对泛型参数应用属性。
        GenericParameter = 16384,
        //
        // 摘要: 
        //     可以对任何应用程序元素应用属性。
        All = 32767,
    }
```

特性应用于Assembly或者Module时，要这样写：
[assembly: someAssemblyAttribute(Parameters)]
[module: someAssemblyAttribute(Parameters)]
在指定自定义特性的有效目标元素时可以用为操作 `|`或运算符来组合 ，例如
```csharp
    [AttributeUsage(AttributeTargets.Class | AttributeTargets.Method | AttributeTargets.Constructor | AttributeTargets.ReturnValue | AttributeTargets.Assembly,AllowMultiple=true,Inherited=false)]
    class TestAttribute:Attribute
```

该类有两个可选参数`AllowMultiple `和`Inherited `：
`AllowMultiple `  参数表示一个特性是否能够多次应用在同一项上。
`Inherited ` 参数如果为true，表示应用到类或者接口上的特性也自动应用到所有派生类或者接口上。如果应用到方法或者属性上，就可以自动应用到该方法或属性等重写的版本上
```csharp
using AttributeTest;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

[assembly: TestAttribute]
[module: TestAttribute]
namespace AttributeTest
{
    
    /// <summary>
    /// AllowMultiple=true 表示同一个元素可以被应用多次该特性
    /// Inherited=true 表示特性可以被继承
    /// </summary>
    [AttributeUsage(AttributeTargets.All,AllowMultiple=true,Inherited=true)]
    class TestAttribute:Attribute
    {
        /// <summary>
        /// 可选参数
        /// </summary>
        public int flag;
        /// <summary>
        /// 可选参数
        /// </summary>
        public bool isInner;
        /// <summary>
        /// 构造函数的参数是和正常构造函数传参一样的
        /// </summary>
        /// <param name="arg"></param>
        public TestAttribute(string arg=null){  }
    }

    [Test("class",flag=3,isInner=true)]
    class AAA
    {
        [Test("constructor",flag=2)]
        public AAA(){       }
        [Test]
        [Test]
        [Test("hello method")]
        public void SSS(){        }
    }

    /// <summary>
    /// 这里特性的构造函数默认参数就是arg=null，可选参数没有传，按照正常默认值处理
    /// </summary>
    [Test]
    class BBB{   }
    class Program
    {
        static void Main(string[] args)
        {


        }
    }
}

```
### 指定特性参数
特性参数就是特性构造函数的参数，参考上面例子arg传参

### 指定特性可选参数
如上面例子的flag和isInner用法


####  0X02 特性例子
直接上代码
```csharp
using AttributeTest;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

[assembly: TestAttribute]
[module: TestAttribute]
namespace AttributeTest
{
    
    /// <summary>
    /// AllowMultiple=true 表示同一个元素可以被应用多次该特性
    /// Inherited=true 表示特性可以被继承
    /// </summary>
    [AttributeUsage(AttributeTargets.All,AllowMultiple=true,Inherited=true)]
    class TestAttribute:Attribute
    {
        /// <summary>
        /// 可选参数
        /// </summary>
        public int flag;
        /// <summary>
        /// 可选参数
        /// </summary>
        public bool isInner;
        /// <summary>
        /// 构造函数的参数是和正常构造函数传参一样的
        /// </summary>
        /// <param name="arg"></param>
        public TestAttribute(string arg=null){  }
    }

    [Test("class",flag=3,isInner=true)]
    class AAA
    {
        [Test("constructor",flag=2)]
        public AAA(){       }
        [Test]
        [Test(flag=10)]
        [Test("hello method",flag=9)]
        public void SSS(){        }
    }

    /// <summary>
    /// 这里特性的构造函数默认参数就是arg=null，可选参数没有传，按照正常默认值处理
    /// </summary>
    [Test]
    class BBB{   }
    class Program
    {
        static void Main(string[] args)
        {
            Type t1 = typeof(AAA);
             object[] objs= t1.GetCustomAttributes(typeof(TestAttribute),false);
             foreach (var item in objs)
             {
                 Console.WriteLine("AAA:::::::" + ((TestAttribute)item).flag);
             }
             foreach (var item in t1.GetMethod("SSS").GetCustomAttributes(typeof(TestAttribute), false))
            {
                Console.WriteLine("AAA::Method:::::" + ((TestAttribute)item).flag);
            }


            foreach (var item in typeof(BBB).GetCustomAttributes(typeof(TestAttribute), false))
            {
                Console.WriteLine("BBB:::::::" + ((TestAttribute)item).flag);
            }


        }
    }
}

```
结果：


  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181026224717896.png)  



