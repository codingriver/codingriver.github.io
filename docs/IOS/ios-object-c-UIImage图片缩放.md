
---
title: "ios-object-c-UIImage图片缩放"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["IOS"]
categories: ["IOS"]
---

<!--more-->


```
1.等比缩放


- (UIImage *) scaleImage:(UIImage *)image toScale:(float)scaleSize {
UIGraphicsBeginImageContext(CGSizeMake(image.size.width * scaleSize, image.size.height * scaleSize);
[image drawInRect:CGRectMake(0, 0, image.size.width * scaleSize, image.size.height * scaleSize)];
UIImage *scaledImage = UIGraphicsGetImageFromCurrentImageContext();
UIGraphicsEndImageContext();
return scaledImage;
}

2.自定义大小
- (UIImage *) reSizeImage:(UIImage *)image toSize:(CGSize)reSize {
UIGraphicsBeginImageContext(CGSizeMake(reSize.width, reSize.height));
[image drawInRect:CGRectMake(0, 0, reSize.width, reSize.height)];
UIImage *reSizeImage = UIGraphicsGetImageFromCurrentImageContext();
UIGraphicsEndImageContext();
return reSizeImage;
}
```
