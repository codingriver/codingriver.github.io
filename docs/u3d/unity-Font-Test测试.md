
---
title: "unity-Font-Test测试"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Unity"]
categories: ["Unity"]
---

<!--more-->


>#####font贴图纹理中，同一个字符的两个size会在纹理中绘制两份，在font纹理中使用的字符数量很少后，纹理大小会释放，最小的font纹理256*256


```
//=====================================================
// - FileName:    	FontTest.cs
// - Created:		wangguoqing
// - UserName:		2018/03/10 14:13:08
// - Email:			wangguoqing@hehegames.cn
// - Description:	
// -  (C) Copyright 2008 - 2015, hehehuyu,Inc.
// -  All Rights Reserved.
//======================================================
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.IO;

public class FontTest : MonoBehaviour {

	// Use this for initialization
    public Text text;
    public RawImage img;
    public MeshRenderer renderer;

	void Awake () {
        
        Font.textureRebuilt += FontTextureRebuild;
        text.font.material = renderer.sharedMaterial;
        
        
	}



    void Start()
    {
        FontInfo(text.font);
        img.material.mainTexture = text.font.material.mainTexture;
        //StartCoroutine(CreateCharacters());
    }
	// Update is called once per frame
	void Update () {
		
	}
    /// <summary>
    /// 文字生成器
    /// </summary>
    /// <returns></returns>
    IEnumerator CreateCharacters()
    {
        if(text==null)
        {
            yield break;
        }

        int unicodeMin = 0X4E00;
        int unicodeMax = 0X9FA5;
        int count = 0;
        for (int i = unicodeMin; i < 0X8FA5; i++)
        {
            text.text += System.Convert.ToChar(i);
            count++;
            if(count>=100)
            {
                count = 0;
               yield return new WaitForSeconds(0.1f);
            }
        }
        
         yield  break;
    }

    void FontInfo(Font font)
    {
        Texture tex = font.material.mainTexture;

        Dg.LogFormat("font name({0}),fontSize({1}),textureId({2}),tex width({3}),tex height({4})",font.name,font.fontSize,tex.GetInstanceID(),tex.width,tex.height);
        
        //Texture2D tex2d = tex as Texture2D;
        //byte[] data = tex2d.EncodeToPNG();
        //System.IO.File.WriteAllBytes("./+" + font.name + "_font.png", data);

    }
     void FontTextureRebuild(Font font)
    {
        Dg.Log("FontTextureRebuild:::" + font.name);
        FontInfo(font);
    }
}

```
