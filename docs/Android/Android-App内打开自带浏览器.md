
---
title: "Android-App内打开自带浏览器"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Android","Unity"]
categories: ["Unity"]
---

<!--more-->


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
