
---
title: "unity接入声网sdk视频bug"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["SDK"]
categories: ["other"]
---

<!--more-->


渲染更新每帧纹理后，unity不重新绘制，暂时用每帧移动物体来屏蔽

```
//=====================================================
// - FileName:    	AgoraDraw 
// - Description:
// - Author:		wangguoqing
// - Email:			wangguoqing@hehemj.com
// - Created:		2018/1/4 11:30:06
// - CLR version: 	4.0.30319.42000
// - UserName:		Wang
// -  (C) Copyright 2008 - 2015, hehehuyu,Inc.
// -  All Rights Reserved.
//======================================================

//using System;
using UnityEngine;
using UnityEngine.UI;
using System.Collections.Generic;
using System.Text;
using agora_gaming_rtc;


public class AgoraDraw : MonoBehaviour 
{

    public delegate void AdjustTransfromDelegate(uint uid, string objName, ref Transform transform);
    public AdjustTransfromDelegate mAdjustTransfrom = null;
    private uint mUid = 0;
    private bool mEnable = false; // if disabled, then no rendering happens

    private Image image;
    private Sprite sprite;
    private IRtcEngineForGaming engine;
    public void SetForUser(uint uid)
    {
        mUid = uid;
        Debug.Log("Set uid " + uid + " for " + gameObject.name);
    }

    public void SetEnable(bool enable)
    {
        mEnable = enable;
    }

    
    // Use this for initialization
    void Start()
    {
        mEnable = true;
        image = GetComponent<Image>();
        engine = agora_gaming_rtc.IRtcEngineForGaming.QueryEngine();
        //Dg.Log("engine:::", engine,"  image:",image,"   sprite:",image.sprite);
        mAdjustTransfrom = AgoraController.onTransformDelegate;
    }

    // Update is called once per frame
    void Update()
    {
        // process engine messages (TODO: put in some other place)
        agora_gaming_rtc.IRtcEngineForGaming engine = agora_gaming_rtc.IRtcEngineForGaming.QueryEngine();
        if (engine == null)
            return;

        while (engine.GetMessageCount() > 0)
            engine.Poll();


#if UNITY_IOS || UNITY_ANDROID
        uint uid = mUid;
        //Dg.Log("uid:::" + uid + "  enable:", mEnable,"  name:",gameObject.name);
        if (mEnable)
        {
            if (image.sprite==null)
            {
                //Debug.Log("Texture2D.CreateExternalTexture:::");
                System.IntPtr texPtr = (System.IntPtr)engine.GenerateNativeTexture();
                Texture2D tex = Texture2D.CreateExternalTexture(640, 360, TextureFormat.ARGB32, false, false, texPtr); // FIXME! texture size is subject to change
                Sprite spt = Sprite.Create(tex, new Rect(0, 0, 640, 360), new Vector2(0.5f, 0.5f));
                this.sprite = spt;
                image.sprite = spt;
                //Debug.Log("Texture2D.CreateExternalTexture:::texPtr:"+texPtr+"  size:"+ tex.texelSize);
            }


            // update texture
            if (sprite != null)
            {

                int texId = (int)sprite.texture.GetNativeTexturePtr();

                // update texture (possible size changing)
                uint texWidth = 0;
                uint texHeight = 0;
                if (engine.UpdateTexture(texId, uid, ref texWidth, ref texHeight) == 0)
                {
                    // TODO: process texture then render
                }
                
                //image.SetAllDirty();
            }
        }
        else if (sprite != null)
        {
           int texId = (int)sprite.texture.GetNativeTexturePtr();
           image.sprite = null;
           engine.DeleteTexture(texId);
        }
#endif

        if (mAdjustTransfrom != null)
        {
            var trans = transform;
            mAdjustTransfrom(mUid, gameObject.name, ref trans);
        }        
    }


}


```

```C#
//=====================================================
// - FileName:    	AgoraController 
// - Description:
// - Author:		wangguoqing
// - Email:			wangguoqing@hehemj.com
// - Created:		2018/1/4 11:48:38
// - CLR version: 	4.0.30319.42000
// - UserName:		Wang
// -  (C) Copyright 2008 - 2015, hehehuyu,Inc.
// -  All Rights Reserved.
//======================================================

using UnityEngine;
using UnityEngine.UI;
using System.Collections.Generic;
using System.Text;
using agora_gaming_rtc;

class AgoraController
{
    public  IRtcEngineForGaming mRtcEngine;
    public static string appId = "657d422025b44a7793ef3a94a59cae0c";

    private XLua.LuaFunction func;
    public static void onTransformDelegate(uint uid, string objName, ref Transform transform)
    {
        var pos = transform.position;
        transform.position = new Vector3(pos.x, pos.y + 0.00000000001f, pos.z);
        //if (uid == 0) {
        //    //transform.position = new Vector3 (0f, 2f, 0f);
        //    //transform.localScale = new Vector3 (2.0f, 2.0f, 1.0f);
        //    //transform.Rotate (0f, 1f, 0f);
        //} else {
        //    //transform.Rotate (0.0f, 1.0f, 0.0f);
        //}
    }
}
```


