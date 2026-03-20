---
title: "Unity Profiler 使用 Android 真机连接测试"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Unity","Android"]
categories: ["Unity"]
---

<!--more-->

> 官方说明：https://docs.unity3d.com/2018.4/Documentation/Manual/profiler-profiling-applications.html



# 使用usb连接
>官网说明：
> - Attach your device to your computer via cable and make sure that it shows in the **adb**
 devices list.
> - Go to the **Build Settings** (menu: **File > Build Settings**), enable the **Development Build**checkbox, and then select **Build & Run**
> - When the application launches on the device, open the Profiler window in the Unity Editor (menu: **Window > Analysis > Profiler**).
> - From the **Attach to Player** drop-down menu, select **AndroidProfiler(ADB@127.0.0.1:34999)**. The entry in the drop-down menu is only visible when the selected target is Android.

翻译后：
- 打开手机调试模式
-  打开 **Build Settings** (menu: **File > Build Settings**)，勾选 **Development Build**
-  打开Profiler (menu: **Window > Analysis > Profiler**).
- 点击**Attach to Player** ，选择**AndroidProfiler(ADB@127.0.0.1:34999)**
- 勾选**Enable Internal Profiler** (menu: **File > Build Settings>Player Settings >Other Settings**).
  
win系统打开cmd命令行，执行命令  `adb forward tcp:34999 localabstract:Unity-{在此处插入 Bundle ID}`    
例如  `adb forward tcp:34999 localabstract:Unity-com.test.aoc` （将`com.test.aoc`替换成自己的`Bundle ID`，**不是将冒号后面的替换**）

*执行该命令时必须打开unity且电脑连接android手机，手机处于调试模式*
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20200817213544990.png#pic_center)  

  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20200817214702727.png)  

  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/2020081721473018.png)  


# 使用wifi连接
> - Disable mobile data on your Android device.
> - Connect your Android device to your WiFi network. The Profiler uses a local WiFi network to send profiling data from your device to the Unity Editor.
> - Attach your device to your computer via cable. Go to the Build Settings (menu: File > Build Settings), enable the Development Build and Autoconnect Profiler checkboxes, then select Build & Run.
> - When the application launches on the device, open the Profiler window in the Unity Editor (menu: Window > Analysis > Profiler).
Build Settings 里，将 Development Build、Autoconnect Profiler、Script Debugging 打开。

# 查看端口占用
-   `netstat -ano|findstr 5037`   去查找5037对应的端口号的进程id 也就是pid。
-   `tasklist |findstr 20120`  查看进程名字。
- 用任务管理器 查看进程pid对应的进程，然后结束进程（打开任务管理器后右键勾选PID显示pid）

  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20200817213907858.png)  


  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20200817214356745.png)  



> *如果进程有守护进程，干不掉，则参考文章 https://blog.csdn.net/aLLLiyyy/article/details/86555228，最后面会说怎么结束掉*

