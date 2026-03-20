
---
title: "unity创建新脚本自动添加版权声明，文件名，作者，创建时间等"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Unity"]
categories: ["Unity"]
---

<!--more-->


- ####1.修改81-C# Script-NewBehaviourScript.cs.txt文件
打开unity安装目录对应.\Unity\Editor\Data\Resources\ScriptTemplates\81-C# Script-NewBehaviourScript.cs.txt文件
我的目录：C:\Program Files\Unity\Editor\Data\Resources\ScriptTemplates\81-C# Script-NewBehaviourScript.cs.txt
我的文件修改如下：
```
//=====================================================
// - FileName:    	#SCRIPTNAME#.cs
// - Created:		#AuthorName#
// - UserName:		#CreateTime#
// - Email:			#AuthorEmail#
// - Description:	
// -  (C) Copyright 2008 - 2015, hehehuyu,Inc.
// -  All Rights Reserved.
//======================================================
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class #SCRIPTNAME# : MonoBehaviour {

	// Use this for initialization
	void Start () {
		#NOTRIM#
	}
	
	// Update is called once per frame
	void Update () {
		#NOTRIM#
	}
}

```
- ####2.添加脚本Copyright.cs


![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-a2e70c2103fe460d.png)  


在工程中的Editor目录下添加脚本Copyright.cs
```
//=====================================================
// - FileName:    	#SCRIPTNAME#.cs
// - Created:		#AuthorName#
// - UserName:		#CreateTime#
// - Email:			#AuthorEmail#
// - Description:	
// -  (C) Copyright 2008 - 2015, hehehuyu,Inc.
// -  All Rights Reserved.
//======================================================
using UnityEngine;
using System.Collections;
using System.IO;

public class Copyright: UnityEditor.AssetModificationProcessor
{
    private const string AuthorName="wangguoqing";
    private const string AuthorEmail = "wangguoqing@hehegames.cn";

    private const string DateFormat = "yyyy/MM/dd HH:mm:ss";
    private static void OnWillCreateAsset(string path)
    {
        path = path.Replace(".meta", "");
        if (path.EndsWith(".cs"))
        {
            string allText = File.ReadAllText(path);
            allText = allText.Replace("#AuthorName#", AuthorName);
            allText = allText.Replace("#AuthorEmail#", AuthorEmail);
            allText = allText.Replace("#CreateTime#", System.DateTime.Now.ToString(DateFormat));            
            File.WriteAllText(path, allText);
            UnityEditor.AssetDatabase.Refresh();
        }

    }
}
```
**效果如下**


![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-5ebb622277023064.png)  


>参考文章：<http://blog.csdn.net/u013108312/article/details/54174757>
