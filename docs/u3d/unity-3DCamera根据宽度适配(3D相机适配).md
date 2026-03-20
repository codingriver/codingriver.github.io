
---
title: "unity-3DCamera根据宽度适配(3D相机适配)"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Unity"]
categories: ["Unity"]
---

<!--more-->


>unity的3D相机默认是根据高度适配的（保持3D相机的高度视野范围不变），这里调整成根据宽度适配（就是保持3D相机宽度的视野范围不变）。

直接上脚本，将脚本挂在Camera的物体上
```cs
//=====================================================
// - FileName:    	CameraAdjust.cs
// - Description:
// - Author:		wangguoqing
// - Email:			wangguoqing@hehemj.com
// - Created:		#CreateTime#
// - UserName:		#AuthorName#
// -  (C) Copyright 2008 - 2015, hehehuyu,Inc.
// -  All Rights Reserved.
//======================================================
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// 3D相机根据宽度适配，默认的相机是根据高度适配的
/// 将该脚本挂在Camera的物体上
/// </summary>
public class CameraAdjust : MonoBehaviour {

    void Start () 
    {
        int ManualWidth = 1280;   //首先记录下你想要的屏幕分辨率的宽
        int ManualHeight = 720;   //记录下你想要的屏幕分辨率的高        //普通安卓的都是 1280*720的分辨率
        int manualHeight;

        //然后得到当前屏幕的高宽比 和 你自定义需求的高宽比。通过判断他们的大小，来不同赋值
        //*其中Convert.ToSingle（）和 Convert.ToFloat() 来取得一个int类型的单精度浮点数（C#中没有 Convert.ToFloat() ）；
        if (Convert.ToSingle(Screen.height) / Screen.width > Convert.ToSingle(ManualHeight) / ManualWidth)
        {
            //如果屏幕的高宽比大于自定义的高宽比 。则通过公式  ManualWidth * manualHeight = Screen.width * Screen.height；
            //来求得适应的  manualHeight ，用它待求出 实际高度与理想高度的比率 scale
            manualHeight = Mathf.RoundToInt(Convert.ToSingle(ManualWidth) / Screen.width * Screen.height);
        }
        else
        {   //否则 直接给manualHeight 自定义的 ManualHeight的值，那么相机的fieldOfView就会原封不动
            manualHeight = ManualHeight;
        }
            
        Camera camera = GetComponent<Camera>();       
        float scale = Convert.ToSingle(manualHeight*1.0f / ManualHeight);   
        camera.fieldOfView *= scale;                      //Camera.fieldOfView 视野:  这是垂直视野：水平FOV取决于视口的宽高比，当相机是正交时fieldofView被忽略
        //把实际高度与理想高度的比率 scale乘加给Camera.fieldOfView。
        //这样就能达到，屏幕自动调节分辨率的效果
    }
    
}

```
