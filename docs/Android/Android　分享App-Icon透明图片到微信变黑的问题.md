
---
title: "Android　分享App-Icon透明图片到微信变黑的问题"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Android","Unity"]
categories: ["Unity"]
---

<!--more-->


> 参考文章：https://www.cnblogs.com/jasonkent27/p/5113184.html

```
/**
     * bitmap中的透明色用白色替换
     * 
     * @param bitmap
     * @return
     */
    public static Bitmap changeColor(Bitmap bitmap) {
        if (bitmap == null) {
            return null;
        }
        int w = bitmap.getWidth();
        int h = bitmap.getHeight();
        int[] colorArray = new int[w * h];
        int n = 0;
        for (int i = 0; i < h; i++) {
            for (int j = 0; j < w; j++) {
                int color = getMixtureWhite(bitmap.getPixel(j, i));
                colorArray[n++] = color;
            }
        }
        return Bitmap.createBitmap(colorArray, w, h, Bitmap.Config.ARGB_8888);
    }

    /**
     * 获取和白色混合颜色
     * 
     * @return
     */
    private static int getMixtureWhite(int color) {
        int alpha = Color.alpha(color);
        int red = Color.red(color);
        int green = Color.green(color);
        int blue = Color.blue(color);
        return Color.rgb(getSingleMixtureWhite(red, alpha), getSingleMixtureWhite

(green, alpha),
                getSingleMixtureWhite(blue, alpha));
    }

    /**
     * 获取单色的混合值
     * 
     * @param color
     * @param alpha
     * @return
     */
    private static int getSingleMixtureWhite(int color, int alpha) {
        int newColor = color * alpha / 255 + 255 - alpha;
        return newColor > 255 ? 255 : newColor;
    }
```
