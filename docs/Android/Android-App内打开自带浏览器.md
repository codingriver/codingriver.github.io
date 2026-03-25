---
title: "Android-App内打开自带浏览器"
date: "2020-12-13"
tags:
  - Android
  - 网络
categories:
  - Android
comments: true
---
# Android-App内打开自带浏览器

﻿

```
import android.net.NetworkInfo;
import android.net.Uri;

    public void OpenWebView(String url)
    {
    	Log.i("pay",url);
        Intent intent = new Intent();
        intent.setAction("android.intent.action.VIEW");
        Uri content_url = Uri.parse(url);
        intent.setData(content_url);
        intent.setClassName("com.android.browser","com.android.browser.BrowserActivity");
        startActivity(intent);
    }
```
