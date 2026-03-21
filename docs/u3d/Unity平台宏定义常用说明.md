---
title: "Unity平台宏定义常用说明"
date: "2026-03-21"
tags:
  - Unity
  - UI
  - CSharp
  - Android
  - iOS
categories:
  - u3d
comments: true
---
# Unity平台宏定义常用说明

## 平台 #define 指令

| 属性 | 功能 |
|:------:| -----------:|
| UNITY_EDITOR | 用于从游戏代码中调用 Unity Editor 脚本的 #define 指令。 |
| UNITY_EDITOR_WIN | 用于 Windows 上的 Editor 代码的 #define 指令。 |
| UNITY_EDITOR_OSX | 用于 Mac OS X 上的 Editor 代码的 #define 指令。 |
| UNITY_STANDALONE_OSX | 用于专门为 Mac OS X（包括 Universal、PPC 和 Intel 架构）编译/执行代码的 #define 指令。 |
| UNITY_STANDALONE_WIN | 用于专门为 Windows 独立平台应用程序编译/执行代码的 #define 指令。 |
| UNITY_STANDALONE_LINUX | 用于专门为 Linux 独立平台应用程序编译/执行代码的 #define 指令。 |
| UNITY_STANDALONE | 用于为任何独立平台（Mac OS X、Windows 或 Linux）编译/执行代码的 #define 指令。 |
| UNITY_WII | 用于为 Wii 游戏主机编译/执行代码的 #define 指令。 |
| UNITY_IOS | 用于为 iOS 平台编译/执行代码的 #define 指令。 |
| UNITY_IPHONE | 已弃用。改用 UNITY_IOS。 |
| UNITY_ANDROID | 用于 Android 平台的 #define 指令。 |
| UNITY_PS4 | 用于运行 PlayStation 4 代码的 #define 指令。 |
| UNITY_XBOXONE | 用于执行 Xbox One 代码的 #define 指令。 |
| UNITY_TIZEN | 用于 Tizen 平台的 #define 指令。 |
| UNITY_TVOS | 用于 Apple TV 平台的 #define 指令。 |
| UNITY_WSA | 用于通用 Windows 平台的 #define 指令。此外，根据 .NET Core 和使用 .NET 脚本后端来编译 C# 文件时会定义 NETFX_CORE。 |
| UNITY_WSA_10_0 | 用于通用 Windows 平台的 #define 指令。此外，根据 .NET Core 来编译 C# 文件时会定义 WINDOWS_UWP。 |
| UNITY_WINRT | 与 UNITY_WSA 相同。 |
| UNITY_WINRT_10_0 | 等效于 UNITY_WSA_10_0 |
| UNITY_WEBGL | 用于 WebGL 的 #define 指令。 |
| UNITY_FACEBOOK | 用于 Facebook 平台（WebGL 或 Windows 独立平台）的 #define 指令。 |
| UNITY_ADS | 用于从游戏代码中调用 Unity Ads 方法的 #define 指令。5.2 及更高版本。 |
| UNITY_ANALYTICS | 用于从游戏代码中调用 Unity Analytics 方法的 #define 指令。5.2 及更高版本。 |
| UNITY_ASSERTIONS | 用于断言控制过程的 #define 指令。 |
| DEVELOPMENT_BUILD | Development模式|

测试预编译宏定义：
```csharp
    #if UNITY_EDITOR
      Debug.Log("Unity Editor");
    #endif
```

完整测试案例：
``` csharp
using UnityEngine;
using System.Collections;

public class PlatformDefines : MonoBehaviour {
  void Start () {

    #if UNITY_EDITOR
      Debug.Log("Unity Editor");
    #endif
    #if UNITY_EDITOR_WIN
      Debug.Log("UNITY_EDITOR_WIN");
    #endif
    #if UNITY_EDITOR_OSX
      Debug.Log("UNITY_EDITOR_OSX");
    #endif    

    #if UNITY_IOS
      Debug.Log("Iphone");
    #endif

    #if UNITY_ANDROID
      Debug.Log("UNITY_ANDROID");
    #endif

    #if UNITY_STANDALONE_OSX
    Debug.Log("Stand Alone OSX");
    #endif

    #if UNITY_STANDALONE_WIN
      Debug.Log("Stand Alone Windows");
    #endif


  }          
}
```
## 平台自定义 #define 指令
您也可以向内置的 #define 指令集合中添加您自己的指令。打开 Player Settings 的 Other Settings 面板，并导航到 Scripting Define Symbols 文本框。    
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/Unity平台宏定义常用说明/20200914125524.png)  

输入要为该特定平台定义的符号名称，以分号分隔。随后可以将这些符号用作 #if 指令中的条件，就像内置条件一样。

## 全局自定义 #define 指令

您可以定义自己的预处理器指令来控制在编译时包含的代码。为此，必须将包含额外指令的文本文件添加到 Assets 文件夹。文件名取决于您使用的语言。扩展名为 __.rsp__：


| C#（播放器和 Editor 脚本） | <项目路径>/Assets/mcs.rsp |
|:------:| -----------:|
	
举例来说，如果在 mcs.rsp 文件中包含单行 -define:UNITY_DEBUG，则 #define 指令 UNITY_DEBUG 将作为 C# 脚本的全局 #define 指令存在，但 Editor 脚本除外。

每次对 .rsp 文件进行更改时，都需要重新编译才能使更改生效。可通过更新或重新导入单个脚本（.js 或 .cs）文件来完成此操作。

**注意**

如果只想修改全局 #define 指令，请使用 Player 设置中的 Scripting Define Symbols__，因为此选项涵盖了所有编译器。如果选择 .rsp__ 文件，则需要为 Unity 使用的每个编译器提供一个文件。

包含在 Editor 安装文件夹中的 mcs 应用程序的“Help”部分中描述了 .rsp 文件的使用方法。可通过运行 mcs -help 获取更多信息。

请注意，.rsp 文件需要与正在调用的编译器匹配。例如：

- 当针对 .NET 3.5 Equivalent（已弃用）脚本运行时版本时，__mcs__ 与 mcs.rsp 一起使用，
- 当针对 .NET 4.x Eqivalent 脚本运行时版本编译器时，__csc__ 与 csc.rsp 一起使用。


> 引用自：[Unity官方说明](https://docs.unity.cn/cn/current/Manual/PlatformDependentCompilation.html)
