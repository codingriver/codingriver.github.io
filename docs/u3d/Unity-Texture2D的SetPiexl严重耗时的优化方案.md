---
title: "Unity-Texture2D的SetPiexl严重耗时的优化方案"
date: "2021-12-20"
tags:
  - Unity
  - 性能优化
  - 网络
  - 图形学
  - CSharp
categories:
  - u3d
comments: true
---
# Unity-Texture2D的SetPiexl严重耗时的优化方案

*Unity中使用Texture2D的SetPixel大量调用的时候耗时非常严重。*
>在使用战争迷雾时需要不断的更新迷雾数据，当进入场景时需要先初始化迷雾数据，将数据转换成纹理（`Texture2D`），一张图片，使用`public void SetPixel(int x, int y, Color color);`时耗时非常严重。这里提供使用纹理原始数据直接修改的办法`public NativeArray<T> GetRawTextureData<T>() where T : struct;`，耗时优化明显提升。

使用`GetRawTextureData<T>()`该方法时遇到了一个问题：
- 当使用`texture.GetRawTextureData<Color32>()`时获取数据的长度是正常的。
- 当使用`texture.GetRawTextureData<Color>()`时获取数据的长度是原始长度的四分之一。
  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/Unity-Texture2D的SetPiexl严重耗时的优化方案/20201010180832.png)  

[unity官方测试例子](https://docs.unity.cn/cn/current/ScriptReference/Texture2D.GetRawTextureData.html)：
```csharp
using UnityEngine;

public class ExampleScript : MonoBehaviour
{
    void Start()
    {
        var texture = new Texture2D(128, 128, TextureFormat.RGBA32, false);
        GetComponent<Renderer>().material.mainTexture = texture;

        // RGBA32 texture format data layout exactly matches Color32 struct
        var data = texture.GetRawTextureData<Color32>();

        // fill texture data with a simple pattern
        Color32 orange = new Color32(255, 165, 0, 255);
        Color32 teal = new Color32(0, 128, 128, 255);
        int index = 0;
        for (int y = 0; y < texture.height; y++)
        {
            for (int x = 0; x < texture.width; x++)
            {
                data[index++] = ((x &amp; y) == 0 ? orange : teal);
            }
        }
        // upload to the GPU
        texture.Apply();
    }
}
```

测试代码：
```csharp
        public void Awake()
        {
            MapComponent.Instance.fogComponent = this;
            jiesuoQueue.Clear();
            if (DCFog.InstanceFog.Data == null)
            {
                Log.Error("FogComponent::DCFog.InstanceFog.Data=null");
                return;
            }

            if (!CheckFog)
            {
                GameObject warFogObj = GameObject.Find("WarFog");//TODO TEMP
                if (warFogObj != null)
                {
                    warFogObj.SetActive(false);
                }
                return;
            }
            Debug.Log($"FOG LOADType::{LoadType}");
            long starttime = DateTime.UtcNow.Ticks;
            ProfilerHelper.BeginSample("FogComponent::Awake:UpdateLogicCell");
            int cell = SN01GameConstCategory.FogSide;
            int size = (int)(MapFactory.MAP_SIZE / cell);
            //texture = new Texture2D(size, size, TextureFormat.R8,false);
            texture = new Texture2D(MapFactory.MAP_SIZE, MapFactory.MAP_SIZE, TextureFormat.ARGB32, false);
            //Debug.Log("FogComponent::texture size:"+MapFactory.MAP_SIZE+"  texture:"+texture+"  data len:"+ DCFog.InstanceFog.Data.Length);
            texture.filterMode = FilterMode.Point;
            texture.wrapMode = TextureWrapMode.Clamp;
            texture.name = "fogtexture";
            texture.anisoLevel = 0;
            
            
            if(LoadType==0)
            {
                for (int i = 0; i < size; i++)
                {
                    for (int j = 0; j < size; j++)
                    {
                        byte v = 0;
                        if (DCFog.InstanceFog.Data.Length == 0)
                        {
                            v = 1;
                        }
                        else
                        {
                            v = DCFog.InstanceFog.Data[i * size + j];
                        }

                        //if(v==1)
                        //{
                        //ProfilerHelper.BeginSample("UpdateCell");
                        UpdateLogicCell(i, j, v);
                        //ProfilerHelper.EndSample();
                        //}


                    }
                }
            }
            else
            {
                var array = texture.GetRawTextureData<Color32>();
                //Debug.Log($"fog::::===>>array:{array.Length},texture:({texture.width},{texture.height}),mipmap:{texture.mipmapCount},curlevel:{texture.loadedMipmapLevel}");
                for (int i = 0; i < size; i++)
                {
                    for (int j = 0; j < size; j++)
                    {
                        byte v = 0;
                        if (DCFog.InstanceFog.Data.Length == 0)
                        {
                            v = 1;
                        }
                        else
                        {
                            v = DCFog.InstanceFog.Data[i * size + j];
                        }

                        for (int m = 0; m < cell; m++)
                        {
                            for (int n = 0; n < cell; n++)
                            {
                                array[(i * cell + m)  + (j * cell + n) * MapFactory.MAP_SIZE] = v !=0  ? closeCol : openCol;
                            }
                        }


                    }
                }


            }

            //ProfilerHelper.EndSample();
            //ProfilerHelper.BeginSample("Apply");
            texture.Apply();
            ProfilerHelper.EndSample();
            Debug.LogError((DateTime.UtcNow.Ticks - starttime)/10000);
#if UNITY_EDITOR
            float time = Time.realtimeSinceStartup;
            ProfilerHelper.BeginSample("FogComponent::Awake:WritePNG");
            Debug.LogError(System.IO.Path.Combine(Environment.CurrentDirectory, "fog.png"));
            System.IO.File.WriteAllBytes(System.IO.Path.Combine(Environment.CurrentDirectory, "fog.png"), texture.EncodeToPNG());
            ProfilerHelper.EndSample();
            Log.Error("EDITOR  FogComponent::Awake:WritePNG Time: " + (Time.realtimeSinceStartup - time));
#endif
            FogBlur fogBlur = Camera.main.GetComponent<FogBlur>();
            if(fogBlur!=null)
            {
                //ProfilerHelper.BeginSample("FogComponent::ComputeShaderBlur");
                fogBlur.Source = texture;
                fogBlur.ComputeShaderBlurTextureOfFog(texture, Camera.main.GetComponent<FogBlur>().PrintTexture);
                //ProfilerHelper.EndSample();
            }
            else
            {
                Debug.LogWarning("have no fogBlur");
            }

            //List<int> ls = new List<int>();
            //ls.Add(1024*4+500);
            //ls.Add(1024 * 9 + 500);
            //ls.Add(1024 * 9 + 501);
            //ls.Add(1024 * 10 + 500);
            //ls.Add(1024 * 10 + 501);
            //UnlockFog(ls, 0);
            //List<int> ls = new List<int> { 270, 150, 30};

            //TimerEventComponent.Instance.CreateEvent(() => UnLockItemFogArea(ls), 1000 * 5);

        }


        private void UpdateLogicCell(int i,int j,int v)
        {
        //    ProfilerHelper.BeginSample("UpdateLogicCell Inner");
        //    ProfilerHelper.BeginSample("UpdateLogicCell new color");
            int cell = SN01GameConstCategory.FogSide;
            Color color = new Color();
            //ProfilerHelper.EndSample();
            //Debug.Log($"FogComponent:::UpdateLogicCell:{i }-{j } cell:{cell} value:{1-v}");
            //ProfilerHelper.BeginSample("UpdateLogicCell loop");
            for (int m = 0; m < cell; m++)
            {
                for (int n = 0; n < cell; n++)
                {
                    
                    //if(v==1||v==0)
                    {
                        //ProfilerHelper.BeginSample("UpdateLogicCell color set");
                        //v = 1-v; //TODO HardReset
                        color.r = v;
                        color.g = v;
                        color.b = 0;
                        color.a = 1;
                        //ProfilerHelper.EndSample();
                        //Debug.Log($"FogComponent:::UpdateLogicCell:{i * cell + m}-{j * cell + n} value:{v}");
                        //ProfilerHelper.BeginSample("SetPixel");
                        texture.SetPixel(i * cell + m, j * cell + n, color);
                        //ProfilerHelper.EndSample();
                    }

                }
            }
            //ProfilerHelper.EndSample();
            //ProfilerHelper.EndSample();

        }

```