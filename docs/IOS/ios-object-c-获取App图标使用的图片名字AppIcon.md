
---
title: "ios-object-c-获取App图标使用的图片名字AppIcon"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["IOS"]
categories: ["IOS"]
---

<!--more-->



```
//获取appIconName
-(NSString*)GetAppIconName{
    NSDictionary *infoPlist = [[NSBundle mainBundle] infoDictionary];
    
    NSString *icon = [[infoPlist valueForKeyPath:@"CFBundleIcons.CFBundlePrimaryIcon.CFBundleIconFiles"] lastObject];
    NSLog(@"GetAppIconName,icon:%@",icon);
    return icon;
}
···
