---
title: "Unity和IOS交互char-作为方法返回值到CSharp中bug"
date: "2020-12-13"
tags:
  - Unity
  - UI
  - CSharp
  - iOS
categories:
  - u3d
comments: true
---
# Unity和IOS交互char-作为方法返回值到CSharp中bug

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
