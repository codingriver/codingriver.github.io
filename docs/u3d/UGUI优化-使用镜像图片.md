---
title: "【Unity优化】：使用镜像图片"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["UGUI","unity优化"]
categories: ["UGUI优化"]
---

<!--more-->

> ui中使用好多像按钮等对称的图片，如果使用1/2、1/4图片将大量的节省内存，这里详细说下这个解决方案；

unity版本：2018.2.13f1
ugui源码版本2018.2（这里在这个版本基础上修改的）

使用的素材有1/2、1/4图片
**下面1/2图片**
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181211202506494.png)  

**左边1/2图片**
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181211202538148.png)  

**左下1/4图片**
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181211202555451.png)  


**这里新建类`MirrorImage`继承Image，对Image功能进行扩展**
根据ImageType 分为四种扩展：Simple，Sliced，Tiled，Filled；只处理了三种

####  0X01 Simple类型

1.先在MirrorImage中增加变量`mirrorType`来定义当前原始素材是是要用什么镜像类型
```c
    /// <summary>
    /// 镜像类型
    /// </summary>
    public enum MirrorType
    {
        /// <summary>
        /// 水平
        /// 提供左侧一半素材
        /// </summary>
        Horizontal,

        /// <summary>
        /// 垂直
        /// 提供下侧一半素材
        /// </summary>
        Vertical,

        /// <summary>
        /// 四分之一
        /// 相当于水平，然后再垂直
        /// 提供左下侧素材
        /// </summary>
        Quarter
    }
    
    /// <summary>
    /// 镜像类型
    /// </summary>
    [SerializeField]
    private MirrorType _mirrorType = MirrorType.Horizontal;

    public MirrorType mirrorType
    {
        get { return _mirrorType; }
        set
        {
            if (_mirrorType != value)
            {
                _mirrorType = value;
                SetVerticesDirty();
                
            }
        }
    }
```
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/2018121210365169.png)  

这个地方需要修改editor，下面有整个工程，可以看下
2.重写`SetNativeSize`方法，实现自动扩展MirrorImage镜像的大小,根据素材的大小和镜像类型来自动配置image大小
```c
    public override void SetNativeSize()
    {
        if (sprite != null)
        {
            float w = sprite.rect.width / pixelsPerUnit;
            float h = sprite.rect.height / pixelsPerUnit;
            if (mirrorType== MirrorType.Horizontal)
            {
                w *= 2;
            }
            else if (mirrorType == MirrorType.Vertical)
            {
                h *= 2;
            }
            else
            {
                w *= 2;
                h *= 2;
            }

            rectTransform.anchorMax = rectTransform.anchorMin;
            rectTransform.sizeDelta = new Vector2(w, h);
            SetAllDirty();
        }
    }
```
3 重写OnPopulateMesh方法，这个方法会修改mesh信息，然后给Graphic
```c

    protected override void OnPopulateMesh(VertexHelper toFill)
    {
        Sprite _sprite = overrideSprite != null ? overrideSprite : sprite;
        if (_sprite == null)
        {
            base.OnPopulateMesh(toFill);
            return;
        }

        switch (type)
        {
            case Type.Simple:
                GenerateSimpleSprite(toFill, preserveAspect);
                break;
            case Type.Sliced:
                //GenerateSlicedSprite(toFill);
                break;
            case Type.Tiled:
                //GenerateTiledSprite(toFill);
                break;
            case Type.Filled:
                //GenerateFilledSprite(toFill, m_PreserveAspect);
                break;
        }
    }
```


这里先处理Simple类型
4. 修改Mesh信息和uv信息，在Image原来的基础上，将mesh增加两个顶点（1/2图片），如果是Horizontal镜像类型，将右侧两个定点移动到中间，在右侧增加这两个定点，uv信息要和左侧的对称
```c
    /// <summary>
    /// Generate vertices for a simple Image.
    /// </summary>
    void GenerateSimpleSprite(VertexHelper vh, bool lPreserveAspect)
    {
        Vector4 v = GetDrawingDimensions(lPreserveAspect);
        var uv = (sprite != null) ? DataUtility.GetOuterUV(sprite) : Vector4.zero;
        Vector4 v1 = v;
        //Debug.Log("uv::::" + uv + "  v:" + v+ "  center:"+ rectTransform.rect.center+ "  rect:" + rectTransform.rect);

        switch (mirrorType)
        {
            case MirrorType.Horizontal:
                v.z = (v.z + v.x) / 2;
                break;
            case MirrorType.Vertical:
                v.w = (v.w + v.y) / 2;
                break;
            case MirrorType.Quarter:
                v.z = (v.z + v.x) / 2;
                v.w = (v.w + v.y) / 2;
                break;
            default:
                break;
        }
        

        //v.w = (v.w + v.y) / 2;
        //Debug.Log("uv::::" + uv + "  v:" + v + "  center:" + rectTransform.rect.center + "  rect:" + rectTransform.rect);
        var color32 = color;
        vh.Clear();
        vh.AddVert(new Vector3(v.x, v.y), color32, new Vector2(uv.x, uv.y));
        vh.AddVert(new Vector3(v.x, v.w), color32, new Vector2(uv.x, uv.w));
        vh.AddVert(new Vector3(v.z, v.w), color32, new Vector2(uv.z, uv.w));
        vh.AddVert(new Vector3(v.z, v.y), color32, new Vector2(uv.z, uv.y));
        vh.AddTriangle(0, 1, 2);
        vh.AddTriangle(2, 3, 0);

        switch (mirrorType)
        {
            /// 1,2,5
            /// 0,3,4
            case MirrorType.Horizontal:
                vh.AddVert(new Vector3(v1.z, v1.y), color32, new Vector2(uv.x, uv.y));
                vh.AddVert(new Vector3(v1.z, v1.w), color32, new Vector2(uv.x, uv.w));
                vh.AddTriangle(3, 2, 5);
                vh.AddTriangle(5, 4, 3);
                break;
            //4,5
            //1,2
            //0,3
            case MirrorType.Vertical:
                vh.AddVert(new Vector3(v1.x, v1.w), color32, new Vector2(uv.x, uv.y));
                vh.AddVert(new Vector3(v1.z, v1.w), color32, new Vector2(uv.z, uv.y));
                vh.AddTriangle(1, 4, 5);
                vh.AddTriangle(5, 2, 1);
                break;
            /// 8,7,6
            /// 1,2,5
            /// 0,3,4
            case MirrorType.Quarter:
                vh.AddVert(new Vector3(v1.z, v1.y), color32, new Vector2(uv.x, uv.y));
                vh.AddVert(new Vector3(v1.z, v.w), color32, new Vector2(uv.x, uv.w));
                vh.AddTriangle(3, 2, 5);
                vh.AddTriangle(5, 4, 3);
                vh.AddVert(new Vector3(v1.z, v1.w), color32, new Vector2(uv.x, uv.y));
                vh.AddVert(new Vector3(v.z, v1.w), color32, new Vector2(uv.z, uv.y));
                vh.AddVert(new Vector3(v1.x, v1.w), color32, new Vector2(uv.x, uv.y));
                vh.AddTriangle(6, 5, 2);
                vh.AddTriangle(2, 7, 6);
                vh.AddTriangle(7, 2, 1);
                vh.AddTriangle(1, 8, 7);
                break;
            default:
                break;
        }

    }
```
水平镜像后：
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181211210600513.png)  

####  0X02 Sliced类型
修改上面的步骤
3 重写OnPopulateMesh方法，这个方法会修改mesh信息，然后给Graphic；增加Sliced类型
```c

    protected override void OnPopulateMesh(VertexHelper toFill)
    {
        Sprite _sprite = overrideSprite != null ? overrideSprite : sprite;
        if (_sprite == null)
        {
            base.OnPopulateMesh(toFill);
            return;
        }

        switch (type)
        {
            case Type.Simple:
                GenerateSimpleSprite(toFill, preserveAspect);
                break;
            case Type.Sliced:
                GenerateSlicedSprite(toFill);
                break;
            case Type.Tiled:
                //GenerateTiledSprite(toFill);
                break;
            case Type.Filled:
                //GenerateFilledSprite(toFill, m_PreserveAspect);
                break;
        }
    }
```
4.Sliced类型支持九宫图，这里注意九宫图做的时候，水平镜像要注意保留九宫图中间无限拉伸的那部分，456区域会镜像并且和原始456区域组成九宫图中心部分进行拉伸，这里注意右侧border不要拉出来。
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181211210110143.png)  

```c
    private void GenerateSlicedSprite(VertexHelper toFill)
    {
        if (!hasBorder)
        {
            GenerateSimpleSprite(toFill, false);
            return;
        }

        Vector4 outer, inner, padding, border;

        if (sprite != null)
        {
            outer = DataUtility.GetOuterUV(sprite);
            inner = DataUtility.GetInnerUV(sprite);
            padding = DataUtility.GetPadding(sprite);
            border = sprite.border;
        }
        else
        {
            outer = Vector4.zero;
            inner = Vector4.zero;
            padding = Vector4.zero;
            border = Vector4.zero;
        }
        
        Rect rect = GetPixelAdjustedRect();
        
        Vector4 adjustedBorders = GetAdjustedBorders(border / pixelsPerUnit, rect);
        //Debug.Log($"outer:{outer},inner:{inner},padding:{padding},adjustedBorders:{adjustedBorders},border:{border}");
        padding = padding / pixelsPerUnit;
        //Debug.Log($"outer:{outer},inner:{inner},padding:{padding},border:{border}");
        s_VertScratch[0] = new Vector2(padding.x, padding.y);
        s_VertScratch[3] = new Vector2(rect.width - padding.z, rect.height - padding.w);

        s_VertScratch[1].x = adjustedBorders.x;
        s_VertScratch[1].y = adjustedBorders.y;

        s_VertScratch[2].x = rect.width - adjustedBorders.z;
        s_VertScratch[2].y = rect.height - adjustedBorders.w;



        s_UVScratch[0] = new Vector2(outer.x, outer.y);
        s_UVScratch[1] = new Vector2(inner.x, inner.y);
        s_UVScratch[2] = new Vector2(inner.z, inner.w);
        s_UVScratch[3] = new Vector2(outer.z, outer.w);

        //Debug.Log($"vert1:{s_VertScratch[0]},{s_VertScratch[1]},{s_VertScratch[2]},{s_VertScratch[3]},");
        //Debug.Log($"uv1:{s_UVScratch[0]},{s_UVScratch[1]},{s_UVScratch[2]},{s_UVScratch[3]},");
        switch (mirrorType)
        {
            case MirrorType.Horizontal:
                s_VertScratch[2].x = rect.width-(s_VertScratch[1].x-s_VertScratch[0].x);
                s_VertScratch[2].y = rect.height - (s_VertScratch[1].y - s_VertScratch[0].y);
                s_UVScratch[2] = new Vector2(inner.x, inner.w);
                s_UVScratch[3] = new Vector2(outer.x, outer.w);
                break;
            case MirrorType.Vertical:
                s_VertScratch[2].x = rect.width - (s_VertScratch[1].x - s_VertScratch[0].x);
                s_VertScratch[2].y = rect.height - (s_VertScratch[1].y - s_VertScratch[0].y);
                s_UVScratch[2] = new Vector2(inner.z, inner.y);
                s_UVScratch[3] = new Vector2(outer.z, outer.y);
                break;
            case MirrorType.Quarter:
                s_VertScratch[2].x = rect.width - (s_VertScratch[1].x - s_VertScratch[0].x);
                s_VertScratch[2].y = rect.height - (s_VertScratch[1].y - s_VertScratch[0].y);
                s_UVScratch[2] = new Vector2(inner.x, inner.y);
                s_UVScratch[3] = new Vector2(outer.x, outer.y);
                break;
            default:
                break;
        }

        //Debug.Log($"uv2:{s_UVScratch[0]},{s_UVScratch[1]},{s_UVScratch[2]},{s_UVScratch[3]},");
        //Debug.Log($"vert2:{s_VertScratch[0]},{s_VertScratch[1]},{s_VertScratch[2]},{s_VertScratch[3]},");

        for (int i = 0; i < 4; ++i)
        {
            s_VertScratch[i].x += rect.x;
            s_VertScratch[i].y += rect.y;
        }
        toFill.Clear();

        for (int x = 0; x < 3; ++x)
        {
            int x2 = x + 1;

            for (int y = 0; y < 3; ++y)
            {
                if (!fillCenter && x == 1 && y == 1)
                    continue;

                int y2 = y + 1;


                AddQuad(toFill,
                    new Vector2(s_VertScratch[x].x, s_VertScratch[y].y),
                    new Vector2(s_VertScratch[x2].x, s_VertScratch[y2].y),
                    color,
                    new Vector2(s_UVScratch[x].x, s_UVScratch[y].y),
                    new Vector2(s_UVScratch[x2].x, s_UVScratch[y2].y));
            }
        }
    }
```

镜像后的效果：
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181211210349466.png)  


####  0X03 Tiled类型

修改上面的步骤
3 重写OnPopulateMesh方法，这个方法会修改mesh信息，然后给Graphic；增加Tiled类型
```c

    protected override void OnPopulateMesh(VertexHelper toFill)
    {
        Sprite _sprite = overrideSprite != null ? overrideSprite : sprite;
        if (_sprite == null)
        {
            base.OnPopulateMesh(toFill);
            return;
        }

        switch (type)
        {
            case Type.Simple:
                GenerateSimpleSprite(toFill, preserveAspect);
                break;
            case Type.Sliced:
                GenerateSlicedSprite(toFill);
                break;
            case Type.Tiled:
                GenerateTiledSprite(toFill);
                break;
            case Type.Filled:
                //GenerateFilledSprite(toFill, m_PreserveAspect);
                break;
        }
    }
```

4.Tiled类型这里注意，不支持九宫图，注意不要曾加border；
假设是水平镜像类型：tiled平铺时会自动把右侧相邻的镜像补上
**没有九宫的border线，一定要注意，要不然出错**
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/2018121121110096.png)  



```c
    /// <summary>
    /// Generate vertices for a tiled Image.
    /// </summary>

    void GenerateTiledSprite(VertexHelper toFill)
    {
        //Debug.Log("==============================&&&&&");
        Vector4 outer, inner, border;
        Vector2 spriteSize;

        if (sprite != null)
        {
            outer = DataUtility.GetOuterUV(sprite);
            inner = DataUtility.GetInnerUV(sprite);
            border = sprite.border;
            spriteSize = sprite.rect.size;
        }
        else
        {
            outer = Vector4.zero;
            inner = Vector4.zero;
            border = Vector4.zero;
            spriteSize = Vector2.one * 100;
        }

        Rect rect = GetPixelAdjustedRect();
        float tileWidth = (spriteSize.x - border.x - border.z) / pixelsPerUnit;
        float tileHeight = (spriteSize.y - border.y - border.w) / pixelsPerUnit;
        border = GetAdjustedBorders(border / pixelsPerUnit, rect);

        var uvMin = new Vector2(inner.x, inner.y);
        var uvMax = new Vector2(inner.z, inner.w);

        // Min to max max range for tiled region in coordinates relative to lower left corner.
        float xMin = border.x;
        float xMax = rect.width - border.z;
        float yMin = border.y;
        float yMax = rect.height - border.w;

        toFill.Clear();
        var clipped = uvMax;

        // if either width is zero we cant tile so just assume it was the full width.
        if (tileWidth <= 0)
            tileWidth = xMax - xMin;

        if (tileHeight <= 0)
            tileHeight = yMax - yMin;

        if (sprite != null && (hasBorder || sprite.packed || sprite.texture.wrapMode != TextureWrapMode.Repeat))
        {
            // Sprite has border, or is not in repeat mode, or cannot be repeated because of packing.
            // We cannot use texture tiling so we will generate a mesh of quads to tile the texture.

            // Evaluate how many vertices we will generate. Limit this number to something sane,
            // especially since meshes can not have more than 65000 vertices.

            long nTilesW = 0;
            long nTilesH = 0;
            if (fillCenter)
            {
                nTilesW = (long)Mathf.Ceil((xMax - xMin) / tileWidth);
                nTilesH = (long)Mathf.Ceil((yMax - yMin) / tileHeight);

                double nVertices = 0;
                if (hasBorder)
                {
                    nVertices = (nTilesW + 2.0) * (nTilesH + 2.0) * 4.0; // 4 vertices per tile
                }
                else
                {
                    nVertices = nTilesW * nTilesH * 4.0; // 4 vertices per tile
                }

                if (nVertices > 65000.0)
                {
                    //Debug.LogError("Too many sprite tiles on Image \"" + name + "\". The tile size will be increased. To remove the limit on the number of tiles, convert the Sprite to an Advanced texture, remove the borders, clear the Packing tag and set the Wrap mode to Repeat.", this);

                    double maxTiles = 65000.0 / 4.0; // Max number of vertices is 65000; 4 vertices per tile.
                    double imageRatio;
                    if (hasBorder)
                    {
                        imageRatio = (nTilesW + 2.0) / (nTilesH + 2.0);
                    }
                    else
                    {
                        imageRatio = (double)nTilesW / nTilesH;
                    }

                    float targetTilesW = Mathf.Sqrt((float)(maxTiles / imageRatio));
                    float targetTilesH = (float)(targetTilesW * imageRatio);
                    if (hasBorder)
                    {
                        targetTilesW -= 2;
                        targetTilesH -= 2;
                    }

                    nTilesW = (long)Mathf.Floor(targetTilesW);
                    nTilesH = (long)Mathf.Floor(targetTilesH);
                    tileWidth = (xMax - xMin) / nTilesW;
                    tileHeight = (yMax - yMin) / nTilesH;
                }
            }
            else
            {
                if (hasBorder)
                {
                    // Texture on the border is repeated only in one direction.
                    nTilesW = (long)Mathf.Ceil((xMax - xMin) / tileWidth);
                    nTilesH = (long)Mathf.Ceil((yMax - yMin) / tileHeight);
                    double nVertices = (nTilesH + nTilesW + 2.0 /*corners*/) * 2.0 /*sides*/ * 4.0 /*vertices per tile*/;
                    if (nVertices > 65000.0)
                    {
                        //Debug.LogError("Too many sprite tiles on Image \"" + name + "\". The tile size will be increased. To remove the limit on the number of tiles, convert the Sprite to an Advanced texture, remove the borders, clear the Packing tag and set the Wrap mode to Repeat.", this);

                        double maxTiles = 65000.0 / 4.0; // Max number of vertices is 65000; 4 vertices per tile.
                        double imageRatio = (double)nTilesW / nTilesH;
                        float targetTilesW = (float)((maxTiles - 4 /*corners*/) / (2 * (1.0 + imageRatio)));
                        float targetTilesH = (float)(targetTilesW * imageRatio);

                        nTilesW = (long)Mathf.Floor(targetTilesW);
                        nTilesH = (long)Mathf.Floor(targetTilesH);
                        tileWidth = (xMax - xMin) / nTilesW;
                        tileHeight = (yMax - yMin) / nTilesH;
                    }
                }
                else
                {
                    nTilesH = nTilesW = 0;
                }
            }

            if (fillCenter)
            {
                // TODO: we could share vertices between quads. If vertex sharing is implemented. update the computation for the number of vertices accordingly.
                for (long j = 0; j < nTilesH; j++)
                {
                    float y1 = yMin + j * tileHeight;
                    float y2 = yMin + (j + 1) * tileHeight;
                    float y2e = y2;
                    if (y2 > yMax)
                    {
                        clipped.y = uvMin.y + (uvMax.y - uvMin.y) * (yMax - y1) / (y2 - y1);
                        y2 = yMax;
                    }
                    clipped.x = uvMax.x;
                    for (long i = 0; i < nTilesW; i++)
                    {
                        float x1 = xMin + i * tileWidth;
                        float x2 = xMin + (i + 1) * tileWidth;
                        float x2e=x2;
                        if (x2 > xMax)
                        {
                            clipped.x = uvMin.x + (uvMax.x - uvMin.x) * (xMax - x1) / (x2 - x1);
                            x2 = xMax;
                        }

                        var uvMin1 = uvMin;
                        var clipped1 = clipped;
                        //Debug.Log("i::" + i + "  j:::" + j);
                        switch (mirrorType)
                        {
                            case MirrorType.Horizontal:
                                if (i % 2 == 1)
                                {
                                    float offsetX = 0;
                                    if (x2e > xMax)
                                    {
                                        offsetX = uvMax.x - (uvMax.x - uvMin.x) * (xMax - x1) / (x2e - x1);
                                    }
                                    uvMin1 = new Vector2(uvMax.x, uvMin.y);
                                    //clipped1 = new Vector2(uvMin.x, clipped.y);
                                    clipped1 = new Vector2(offsetX, clipped.y);
                                }
                                break;
                            case MirrorType.Vertical:
                                if (j % 2 == 1)
                                {
                                    float offsetY = 0;
                                    if (y2e > yMax)
                                    {
                                        offsetY = uvMax.y - (uvMax.y - uvMin.y) * (yMax - y1) / (y2e - y1);
                                    }
                                    //uvMin1 = new Vector2(uvMin.x, clipped.y);
                                    uvMin1 = new Vector2(uvMin.x, uvMax.y);
                                    //clipped1 = new Vector2(clipped.x, uvMin.y);
                                    clipped1 = new Vector2(clipped.x, offsetY);

                                }
                                break;
                            case MirrorType.Quarter:
                                if(j % 2 == 1&& i % 2 == 1)
                                {

                                    float offsetX = uvMin.x;
                                    if (x2e > xMax)
                                    {
                                        offsetX = uvMax.x - (uvMax.x - uvMin.x) * (xMax - x1) / (x2e - x1);
                                    }

                                    float offsetY = uvMin.y;
                                    if (y2e > yMax)
                                    {
                                        offsetY = uvMax.y - (uvMax.y - uvMin.y) * (yMax - y1) / (y2e - y1);
                                    }

                                    clipped1 = new Vector2(offsetX,offsetY) ;
                                    uvMin1 = uvMax;
                                }
                                else if (j % 2 == 1)
                                {
                                    float offsetY = 0;
                                    if (y2e > yMax)
                                    {
                                        offsetY = uvMax.y - (uvMax.y - uvMin.y) * (yMax - y1) / (y2e - y1);
                                    }
                                    //uvMin1 = new Vector2(uvMin.x, clipped.y);
                                    uvMin1 = new Vector2(uvMin.x, uvMax.y);
                                    //clipped1 = new Vector2(clipped.x, uvMin.y);
                                    clipped1 = new Vector2(clipped.x, offsetY);
                                }
                                else if (i % 2 == 1)
                                {
                                    float offsetX = 0;
                                    if (x2e > xMax)
                                    {
                                        offsetX = uvMax.x - (uvMax.x - uvMin.x) * (xMax - x1) / (x2e - x1);
                                    }
                                    uvMin1 = new Vector2(uvMax.x, uvMin.y);
                                    //clipped1 = new Vector2(uvMin.x, clipped.y);
                                    clipped1 = new Vector2(offsetX, clipped.y);
                                }
                                break;
                            default:
                                break;
                        }

                        
                        AddQuad(toFill, new Vector2(x1, y1) + rect.position, new Vector2(x2, y2) + rect.position, color, uvMin1, clipped1);
                    }
                }
            }
            if (hasBorder)
            {
                clipped = uvMax;
                for (long j = 0; j < nTilesH; j++)
                {
                    float y1 = yMin + j * tileHeight;
                    float y2 = yMin + (j + 1) * tileHeight;
                    if (y2 > yMax)
                    {
                        clipped.y = uvMin.y + (uvMax.y - uvMin.y) * (yMax - y1) / (y2 - y1);
                        y2 = yMax;
                    }
                    AddQuad(toFill,
                        new Vector2(0, y1) + rect.position,
                        new Vector2(xMin, y2) + rect.position,
                        color,
                        new Vector2(outer.x, uvMin.y),
                        new Vector2(uvMin.x, clipped.y));
                    AddQuad(toFill,
                        new Vector2(xMax, y1) + rect.position,
                        new Vector2(rect.width, y2) + rect.position,
                        color,
                        new Vector2(uvMax.x, uvMin.y),
                        new Vector2(outer.z, clipped.y));
                }

                // Bottom and top tiled border
                clipped = uvMax;
                for (long i = 0; i < nTilesW; i++)
                {
                    float x1 = xMin + i * tileWidth;
                    float x2 = xMin + (i + 1) * tileWidth;
                    if (x2 > xMax)
                    {
                        clipped.x = uvMin.x + (uvMax.x - uvMin.x) * (xMax - x1) / (x2 - x1);
                        x2 = xMax;
                    }
                    AddQuad(toFill,
                        new Vector2(x1, 0) + rect.position,
                        new Vector2(x2, yMin) + rect.position,
                        color,
                        new Vector2(uvMin.x, outer.y),
                        new Vector2(clipped.x, uvMin.y));
                    AddQuad(toFill,
                        new Vector2(x1, yMax) + rect.position,
                        new Vector2(x2, rect.height) + rect.position,
                        color,
                        new Vector2(uvMin.x, uvMax.y),
                        new Vector2(clipped.x, outer.w));
                }

                // Corners
                AddQuad(toFill,
                    new Vector2(0, 0) + rect.position,
                    new Vector2(xMin, yMin) + rect.position,
                    color,
                    new Vector2(outer.x, outer.y),
                    new Vector2(uvMin.x, uvMin.y));
                AddQuad(toFill,
                    new Vector2(xMax, 0) + rect.position,
                    new Vector2(rect.width, yMin) + rect.position,
                    color,
                    new Vector2(uvMax.x, outer.y),
                    new Vector2(outer.z, uvMin.y));
                AddQuad(toFill,
                    new Vector2(0, yMax) + rect.position,
                    new Vector2(xMin, rect.height) + rect.position,
                    color,
                    new Vector2(outer.x, uvMax.y),
                    new Vector2(uvMin.x, outer.w));
                AddQuad(toFill,
                    new Vector2(xMax, yMax) + rect.position,
                    new Vector2(rect.width, rect.height) + rect.position,
                    color,
                    new Vector2(uvMax.x, uvMax.y),
                    new Vector2(outer.z, outer.w));
            }
        }
        else
        {
            // Texture has no border, is in repeat mode and not packed. Use texture tiling.
            Vector2 uvScale = new Vector2((xMax - xMin) / tileWidth, (yMax - yMin) / tileHeight);

            if (fillCenter)
            {
                AddQuad(toFill, new Vector2(xMin, yMin) + rect.position, new Vector2(xMax, yMax) + rect.position, color, Vector2.Scale(uvMin, uvScale), Vector2.Scale(uvMax, uvScale));
            }
        }
    }

```

镜像后：
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181211211241904.png)  


如果是左下1/4图片
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181211211319238.png)  

则4个tile组成一个完整的图
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181211211407233.png)  

  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181211211509926.png)  




[github工程](https://github.com/codingriver/UnityProjectTest/tree/master/MirrorImage)

>参考文章
>https://zhuanlan.zhihu.com/p/25995971 