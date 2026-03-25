---
title: "Unity截屏"
date: "2020-12-13"
tags:
  - Unity
categories:
  - u3d
comments: true
---
# Unity截屏

```
    IEnumerator CoroutineScreenShot(System.Action action)
    {

        //ReadPixels was called to read pixels from system frame buffer, while not inside drawing frame.
        yield return new WaitForEndOfFrame();
        byte[] data = CaptureScreenshot();
        CacheUtil.WriteSync(ScreenshotPath,data);
        if(action!=null)
            action();
        yield break;
    }
    /// <summary>
    /// 截图
    /// </summary>
    public void SahreCaptureScreenshot()
    {
        Dg.Log("SaveCaptureScreenshot:", ScreenshotPath);

        StartCoroutine(CoroutineScreenShot(() => {
        
        }));
    }
```
**屏幕截图时需要在协程中执行，且必须有yield return new WaitForEndOfFrame();，否则报错:ReadPixels was called to read pixels from system frame buffer, while not inside drawing frame.**
