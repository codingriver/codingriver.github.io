
---
title: "unity--android获取电量和wifi信号强度"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Android","Unity"]
categories: ["Unity"]
---

<!--more-->


```
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.os.BatteryManager;
//*******************************部分代码********************************************
	TelephonyManager phoneManager=null;
	WifiManager wifiManager=null;
	WifiInfo wifiInfo = null;       //获得的Wifi信息 
	@Override
	  protected void onCreate(Bundle savedInstanceState)
	  {
		  super.onCreate(savedInstanceState);
		  phoneManager = (TelephonyManager) this.getSystemService(TELEPHONY_SERVICE);
	       // 获得WifiManager  
	        wifiManager = (WifiManager) getSystemService(WIFI_SERVICE);	 
      }
  //********************************Battery 电量*************************************************
    private IntentFilter ifilter = new IntentFilter(Intent.ACTION_BATTERY_CHANGED);
    public float GetBatterySignal()
    {
    	Intent batteryStatus = this.registerReceiver(null, ifilter);
    	//当前剩余电量
    	int level = batteryStatus.getIntExtra(BatteryManager.EXTRA_LEVEL, -1);
    	//电量最大值
    	int scale = batteryStatus.getIntExtra(BatteryManager.EXTRA_SCALE, -1);
    	//电量百分比
    	float batteryPct = level / (float)scale;
    	Log.i("unity", "GetBatterySignal:::"+batteryPct);
             	
        return batteryPct;
    }  

    //********************************wifi 网络信号 *************************************************
    
    public int GetWifiSignal()
    {
        wifiInfo = wifiManager.getConnectionInfo();  
        //获得信号强度值  
        int level = wifiInfo.getRssi();
        int signal=0;
        //根据获得的信号强度发送信息  
        if (level <= 0 && level >= -50) {  
            signal=5;  
        } else if (level < -50 && level >= -70) {  
        	signal=4;  
        } else if (level < -70 && level >= -80) {  
        	signal=3;  
        } else if (level < -80 && level >= -100) {  
        	signal=2;  
        } else {  
        	signal=1;  
        }     	
        Log.i("unity", "GetWifiSignal:::"+signal);
        return signal;
    }
```
