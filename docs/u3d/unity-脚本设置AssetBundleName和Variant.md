---
title: "unity3d 脚本设置AssetBundle Name和Variant"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Unity"]
categories: ["Unity"]
---

<!--more-->



unity现在的版本所有资源可以手动配置AssetBundle 的Name和Variant，这里用脚本设置下
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181112122730679.png)  

```csharp

    [MenuItem("Tools/Test1")]
    public static void SetBundleName()
    {
        AssetImporter importer = AssetImporter.GetAtPath("assets/test.prefab");
        Debug.Log("assetPath:" + importer.assetPath);
        Debug.Log("name:" + importer.name);
        string bundleName = importer.assetPath.Split('.')[0].Replace("assets/",string.Empty);
        Debug.Log("bundleName:" + bundleName);
        importer.assetBundleName = bundleName + ".unity3d";
        importer.assetBundleVariant = "v1";
        AssetDatabase.SaveAssets();
        AssetDatabase.Refresh();
    }
```


  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181112122805789.png)  

  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/2018111212281621.png)  
