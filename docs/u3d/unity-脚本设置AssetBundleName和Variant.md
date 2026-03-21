---
title: "unity-脚本设置AssetBundleName和Variant"
date: "2026-03-21"
tags:
  - Unity
  - UI
  - 网络
  - CSharp
categories:
  - u3d
comments: true
---
# unity-脚本设置AssetBundleName和Variant

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
