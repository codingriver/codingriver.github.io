
---
title: "Unity-GameObject-销毁（Destroy）后的几种状态"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Unity"]
categories: ["Unity"]
---

<!--more-->


>直接上测试结果，方便后面使用:
>>#####GameObject被销毁时当前帧可以继续使用属性（gameObject,parent,transform等等）。
>>#####GameObject被销毁的下一帧判定null是相等的但是物体类型还是GameObject。
>>#####特别注意GameObject被销毁时当前帧 根据它的Parent获取childCount时是包含销毁的GameObject，所以这里计数不是想象的那样，如果使用childCount则在Destory前将父子关系解除

场景内未运行截图


![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-a00bbae7f1473952.png)  

Test.cs代码
```cs
//=====================================================
// - FileName:    	Test 
// - Description:
// - Author:		wangguoqing
// - Email:			wangguoqing@hehemj.com
// - Created:		2017/12/13 17:12:17
// - CLR version: 	4.0.30319.42000
// - UserName:		Wang
// -  (C) Copyright 2008 - 2015, hehehuyu,Inc.
// -  All Rights Reserved.
//======================================================
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.Text;
using UnityEngine.Events;
using UnityEngine.EventSystems;
public class Test : MonoBehaviour {
    public GameObject obj;
    void Start()
    {
        StartCoroutine(DestroyObj(obj));
    }
    IEnumerator DestroyObj(GameObject go)
    {
        Debug.Log("StartCoroutine");
        Destroy(go);
        Debug.Log("go:::" + go);
        Debug.Log("go transform::1:::" + go.transform);
        Debug.Log("type::1::"+ go.GetType().FullName);
        //go = null;
        yield return new WaitForEndOfFrame();
        if (go == null)
        {
            Debug.Log("null===1");
        }
        if(go is GameObject)
        {
            Debug.Log("type::2::" + go.GetType().FullName);
        }
        Destroy(go);
        if (go == null)
        {
            Debug.Log("null===2");
        }
        Debug.Log("go transform::2:::" + go.transform);//这里是77行
        Destroy(go);
        yield break;
    }
}
```

运行结果



![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-d32dc1f6884f558e.png)  



将go=null这行代码注释放开后的运行结果：


![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-f0dbd41b641893c3.png)  



根据结果说明：
**1. gameObject在第一次Destroy后名没有立即被删除，当前帧可以继续使用；相关属性例如transform还可以用；在获取它Parent的所有物体时是能读到该gameObject属性的，并且Parent读取childCount是包含该gameObject计数的.**
**2. gameObject在第一次Destroy后的下一帧再使用时属性读取失败，应为Destroy的那一帧最终gameObject被销毁，然后go变量为null(这里的null并不是C#真正的null，因为go.transform报错信息有说明)，但是Destroy(go)是不报错的,**
