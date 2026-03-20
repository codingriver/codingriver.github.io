
---
title: "Unity和IOS交互char-作为方法返回值到C#中bug"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Unity","IOS"]
categories: ["Unity"]
---

<!--more-->


修复方法
id不能直接返回，必须分配内存
```

#import "IosTools.h"

#if defined (__cplusplus)
extern "C" {
#endif
    //char*分配内存
    char* StringCopy (const char* string)
    {
        
        if (string == NULL)
            return NULL;
        
        char* res = (char*)malloc(strlen(string) + 1);
        
        strcpy(res, string);
        
        return res;
        
    }
//获取imei，id不能直接返回，必须分配内存
char* GetImei ()
{
    NSLog(@"GetImei");
	NSString *uuid = [[[UIDevice currentDevice] identifierForVendor] UUIDString];
    char* id=[uuid UTF8String];
    NSLog(@"GetImei1111");
    return StringCopy(id);
}

#if defined (__cplusplus)
}
#endif

```
