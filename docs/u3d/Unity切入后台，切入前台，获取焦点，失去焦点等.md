
---
title: "Unity切入后台，切入前台，获取焦点，失去焦点等"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Unity"]
categories: ["Unity"]
---

<!--more-->


正常进:

OnApplicationFocus, isFocus=True

正常退:

OnApplicationQuit


Home出：

OnApplicationPause, isPause=True

OnApplicationFocus, isFocus=False



Home进：

OnApplicationPause, isPause=False
OnApplicationFocus, _isFocus=True



Kill进程：

当前应用双击Home，然后Kill：

OnApplicationQuit  (IOS 有回调，android 没回调)



跳出当前应用，然后Kill：

OnApplicationQuit  (IOS和Android都没回调)

```cs
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class GameApp : MonoBehaviour {

    void Awake()
    {
        //Debug.Log("awake:::::::::");
    }
	// Use this for initialization
	void Start () {
	}
	
	// Update is called once per frame
	void Update () {
        if (Input.GetKeyDown(KeyCode.Escape))
        {
            Dg.Log("Input.GetKeyDown:::KeyCode.Escape");
            //Application.Quit();  
            //ProviderService.Instance.OnBackPressedE("KeyCode.Escape");
        }
            
	}

    void LateUpdate()
    {
        //Debug.Log("LateUpdate^^^^^^^^^^^^^");
    }

    void FixedUpdate()
    {
        //Debug.Log("FixedUpdate^^^^^^^^^^^^^");
    }
    void OnDestroy()
    {

    }


    void OnApplicationFocus(bool hasFocus)
    {
        //Dg.Log("OnApplicationFocus,hasFocus:", hasFocus);
    }


    void OnApplicationPause(bool pauseStatus)
    {
        Dg.Log("OnApplicationPause,pauseStatus:", pauseStatus);
    }


    void OnApplicationQuit()
    {
        Dg.Log("OnApplicationQuit");

    }
}

```
