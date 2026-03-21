---
title: "unity和android交互bug"
date: "2026-03-21"
tags:
  - Unity
  - Android
  - 项目记录
categories:
  - u3d
comments: true
---
# unity和android交互bug

``` java
    public String ApplinkUrl=null;
    public void BroadcastApplinkUrl(String linkUrl)
    {
    	Log.i(AppPackName,"BroadcastApplinkUrl::linkUrl:"+linkUrl);
        //linkUrl 不能传null，否则崩溃
    	UnityPlayer.UnitySendMessage(GameObjectName, ApplinkMethodName, linkUrl);
    }
    @Override
    protected void onNewIntent(Intent intent) {
    	super.onNewIntent(intent);
    	setIntent(intent);
    	Uri uri = getIntent().getData();
    	if(uri!=null)
    	{
    		BroadcastApplinkUrl(uri.toString());
    	}
    	else
    	{
    		BroadcastApplinkUrl("");
    	}
    }    
```




    	UnityPlayer.UnitySendMessage(GameObjectName, ApplinkMethodName, linkUrl);
  在linkUrl这个参数传null的情况下，直接崩溃,这里做下记录

