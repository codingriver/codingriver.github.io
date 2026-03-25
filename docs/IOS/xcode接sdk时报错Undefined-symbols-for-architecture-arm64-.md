---
title: "xcode接sdk时报错Undefined-symbols-for-architecture-arm64-"
date: "2021-12-20"
tags:
  - iOS
  - UI
  - 网络
  - CSharp
  - 工具链
categories:
  - IOS
comments: true
---
# xcode接sdk时报错Undefined-symbols-for-architecture-arm64-

﻿

unity 导出xcode后接环信libHyphenateSDK时build报错Undefined symbols for architecture armv7:
也有Undefined symbols for architecture arm64:
```
Undefined symbols for architecture armv7:
  "_CGImageDestinationCreateWithURL", referenced from:
      -[EMVideoMessageBody initWithLocalPath:displayName:] in libHyphenateSDK.a(EMVideoMessageBody.o)
  "_CGImageDestinationAddImage", referenced from:
      -[EMVideoMessageBody initWithLocalPath:displayName:] in libHyphenateSDK.a(EMVideoMessageBody.o)
  "_CGImageDestinationFinalize", referenced from:
      -[EMVideoMessageBody initWithLocalPath:displayName:] in libHyphenateSDK.a(EMVideoMessageBody.o)
ld: symbol(s) not found for architecture armv7
clang: error: linker command failed with exit code 1 (use -v to see invocation)
```

  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/xcode接sdk时报错Undefined-symbols-for-architecture-arm64-/20200921113551.png)  


这个错误以为sdk或者framework不支持armv7或者arm64，我这实际上是缺少framework
这个错误是工程里面没有引用 ImageIO.framework造成的，
  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/xcode接sdk时报错Undefined-symbols-for-architecture-arm64-/20200921113618.png)  



环信的libHyphenateSDK.a库依赖ImageIO.framework，结果报错让人无语



