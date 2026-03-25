---
title: "Unity-使用Android-Splash"
date: "2020-12-13"
tags:
  - Unity
  - UI
  - 网络
  - Android
categories:
  - u3d
comments: true
---
# Unity-使用Android-Splash

java代码
``` java
	ImageView bgView=null;
	//显示启动图 
	void ShowSplash() {
	   try {
              //对应unity目录：
	      InputStream is = getAssets().open("bin/Data/splash.png");
	      Bitmap splashBitmap = null;
	      BitmapFactory.Options options = new BitmapFactory.Options();
	      options.inPreferredConfig = Bitmap.Config.ARGB_8888;
	      splashBitmap = BitmapFactory.decodeStream(is, null, options);
	      is.close();
	      bgView = new ImageView(this);
	      bgView.setImageBitmap(splashBitmap);
	      bgView.setScaleType(ImageView.ScaleType.CENTER_CROP);
//	      Resources r = mUnityPlayer.currentActivity.getResources();
	      mUnityPlayer.addView(bgView);	      
//	      mUnityPlayer.addView(bgView, r.getDisplayMetrics().widthPixels, r.getDisplayMetrics().heightPixels);
	  } catch (Exception e) {
	      Log.v("unity", "Exception while load splash:" + e.toString());
	  }
	}

	//关闭启动图 
	void HideSplash() {
	   this.runOnUiThread(new Runnable() {
		   @Override
	      public void run() {
	    	  mUnityPlayer.removeView(bgView);
	          bgView = null;
	      }
	   });
	}
```
splash.png文件放在unity工程中的目录为：

![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-786f1cf1a75de54d.png)  

该文件不用放到android的插件工程中，直接放在unity中就可以了

**这里有个bug:splash在加载第0个场景时会被隐藏或者销毁掉没有仔细测试，然后加载场景过程中是黑屏**
