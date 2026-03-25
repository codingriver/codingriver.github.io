---
title: "ios-object-c-获取App图标使用的图片名字AppIcon"
date: "2020-12-13"
tags:
  - iOS
  - CSharp
categories:
  - IOS
comments: true
---
# ios-object-c-获取App图标使用的图片名字AppIcon

﻿

```
//获取appIconName
-(NSString*)GetAppIconName{
    NSDictionary *infoPlist = [[NSBundle mainBundle] infoDictionary];
    
    NSString *icon = [[infoPlist valueForKeyPath:@"CFBundleIcons.CFBundlePrimaryIcon.CFBundleIconFiles"] lastObject];
    NSLog(@"GetAppIconName,icon:%@",icon);
    return icon;
}
···
