---
title: "unity-响应Android返回键"
date: "2020-12-13"
tags:
  - Unity
  - Android
  - Lua
categories:
  - u3d
comments: true
---
# unity-响应Android返回键

>  android 通过java层重载返回键事件onBackPressed有bug，有时候不响应！！！
```
    @Override 
    public void onBackPressed(){
    	Log.v("life","onBackPressed");  
        super.onBackPressed();  
        UnityPlayer.UnitySendMessage(GameObjectName, OnBackMethodName,"back");
        
    } 
```
**解决方案：在unity中获取KeyCode.Escape点击事件，android返回键就是KeyCode.Escape点击事件,这个没有问题**

```
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
public class GameApp : MonoBehaviour {
	void Update () {
        //Debug.Log("Update^^^^^^^^^^^^^");
        _luaMgr.Update();
        if (Input.GetKeyDown(KeyCode.Escape))
        {
            Dg.Log("Input.GetKeyDown:::KeyCode.Escape");
        }
            
	}
}
```

