
---
title: "unity读取StreamingAssets文本文件"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Unity"]
categories: ["Unity"]
---

<!--more-->


因为StreamingAssets目录对于Android来说是在apk里面的，所以File读取不到里面的内容信息，必须通过Android的api读取加载。
C#代码
```cs
//=====================================================
// - FileName:    	ProviderService 
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
using System.Runtime.InteropServices;
using UnityEngine;
/// <summary>
/// 和平台层交互必须通过unity主线程调用
/// </summary>
public class ProviderService :MonoBehaviour {
    public static ProviderService Instance;

#if UNITY_ANDROID
    private AndroidJavaClass jc;
    private AndroidJavaObject jo;
#endif
    void Awake()
    {
        Instance = this;
    }
	void Start()
    {
#if UNITY_ANDROID &&!UNITY_EDITOR
        jc = new AndroidJavaClass("com.test.game.AppActivity");
        jo = jc.CallStatic<AndroidJavaObject>("GetActivity");
#endif
    }


    /// <summary>
    /// 读取StreamingAsset 下的文件
    /// 必须在unity主线程调用，否则JNI调用不过去
    /// </summary>
    /// <returns></returns>
    public byte[] ReadBytes(string fileName)
    {
		byte[] data = null;
		#if UNITY_ANDROID &&!UNITY_EDITOR
        	data = jo.Call<byte[]>("ReadBytes", fileName);
		#endif
        	return data;
    }
}

```

Android代码
```java
package com.test.game;

import com.unity3d.player.UnityPlayerActivity;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import com.unity3d.player.UnityPlayer;

import android.app.AlertDialog;
import android.content.BroadcastReceiver;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.res.AssetManager;
import android.content.res.Resources;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.Uri;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.os.BatteryManager;
import android.os.Bundle;
import android.os.Environment;
import android.telephony.TelephonyManager;
import android.util.Log;
import android.widget.ImageView;
import android.widget.Toast;


public class AppActivity extends UnityPlayerActivity {
	
	public static final String GameObjectName="Service";
	public static final String ApplinkMethodName="BroadcastApplinkUrl";
	public static final String BatteryChangedMethodName="BroadcastBatteryChanged";
	public static final String AppPackName = "com.hehegames.majiangone";
	
	public static AppActivity activity=null;
	TelephonyManager phoneManager=null;
	WifiManager wifiManager=null;
	WifiInfo wifiInfo = null;       //获得的Wifi信息 
	@Override
	  protected void onCreate(Bundle savedInstanceState)
	  {
		Log.v("life","onCreate");  
		  super.onCreate(savedInstanceState);
		  activity=this;
		  //显示splash
		  ShowSplash();
		  phoneManager = (TelephonyManager) this.getSystemService(TELEPHONY_SERVICE);
	       // 获得WifiManager  
	        wifiManager = (WifiManager) getSystemService(WIFI_SERVICE);
	        assetManager = getAssets();
	       //applink 
		  Uri uri = getIntent().getData();
		  if(uri!=null)
		  {
			  ApplinkUrl=uri.toString();
		  }
		  else
		  {
			  ApplinkUrl=null;
		  }
		  
	  }
	public static AppActivity GetActivity()
	{
		
		return activity;
	}
    
    //********************************read StreamingAsset file*************************************************
    protected AssetManager assetManager;
	private byte[] ReadBytesByStream(InputStream inputStream) 
	{
 
	  ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
//长度这里暂时先写成1024
	  byte buf[] = new byte [2048];
 
	  int len;
 
	  try {
 
	   while ((len = inputStream.read(buf)) != -1) {
 
	    outputStream.write(buf, 0, len);
 
	   }
 
	   outputStream.close();
 
	   inputStream.close();
 
	  } catch (IOException e) {
		  return null;
	  }
	  return outputStream.toByteArray();
	}    

	
	//load StreamingAsset file by byte array
	public byte[] ReadBytes(String path)
	{
	
		 InputStream inputStream = null ;
		 
		  try {
 
			   inputStream = assetManager.open(path);
 
			  } catch (IOException e) {
 
			   Log.v ("unity", "ReadBytes:::"+e.getMessage());
			   return null;
			  }
 
		  return ReadBytesByStream(inputStream);
	}	 
} 
```

**这里注意下AppActivity 的方法ReadBytes必须在unity主线程调用，否则调用失败，unity没有日志，这里被坑了**
