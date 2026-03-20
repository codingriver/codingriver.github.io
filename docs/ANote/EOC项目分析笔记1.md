---
title: "EOC项目分析笔记1"
subtitle: "EOC项目分析笔记1"
date: 2022-03-29T11:08:00+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
draft: true
tags: []
categories: []
---

<!--more-->

## 项目优化列表
- [ ] UI生成的view文件，这里执行比较浪费效率，有可能无用的节点也会Find transform 节点
![](../images/2022-04-14-16-11-38.png)
    **方案：使用C#属性的方式去处理，只有使用的时候才get，能有效的减少无用节点的使用**

- [ ] 字符串拼接问题，使用公用 `StringBuilder` 进行处理
```csharp
using System.Text;
using Sproto;

namespace Skyunion
{
    public static class StringBuilderCache
    {
        private const int MAX_Size = 512;
        private static StringBuilder s_Cache = new StringBuilder(MAX_Size, MAX_Size);

        public static StringBuilder Get(int capacity = 0)
        {
            if (s_Cache.Capacity < capacity)
                return new StringBuilder(capacity);
            s_Cache.Length = 0;
            return s_Cache;
        }
    }
}
```

- [ ] 所有new 数组的地方建议使用公共方法去管理，或者组成一个共有池


- [ ] 所有使用 `Physics.RaycastAll`和`Physics.Raycast`的地方修改成无GC的方法

```csharp
public static int RaycastNonAlloc(Ray ray, RaycastHit[] results, float maxDistance, int layerMask)
```
![](../images/2022-04-15-16-35-28.png)

- [x] 对比字符串查找业务对象和id查找业务对象耗时及HashCode获取业务对象
> 方式1：  
> 点击gameObject 根据GameObject的name字符串查找对应的业务对象  
> 方式2:  
> 初始化gameObject时添加一个组件，组件内有id字段，点击gameObject时根据gameObject上的组件找到id，然后根据id找到对应业务对象  
> 方式3:  
> 点击gameObject，根据gameObject的HashCode找到对应业务对象

对比耗时：  
*使用800000个gameObject测试：*  
![](../images/2022-04-20-15-26-15.png)

方式1的耗时：重命名gameObject+通过字符串查找业务对象; 耗时 **503+316** 毫秒
方式2的耗时：给gameObject添加组件+通过id查找业务对象； 耗时 **3883+191** 毫秒
方式3的耗时：gameObject获取HashCode+通过HashCode查找业务对象；耗时 **34+12** 毫秒

结论：  
**gameObject的HashCode查找效率最高，其次是字符串查找，添加组件绑定id的方式最慢**

- [ ] UGUI 优先使用RectMask2D，最后使用Mask

### 登录流程

设置登录信息，并且派发登录事件（开发模式）
![](../images/2022-03-29-11-10-55.png)
设置登录信息，并且派发登录事件（线上模式）
![](../images/2022-03-29-11-11-38.png)
链接服务器
![](../images/2022-03-29-11-09-55.png)
连接服务器后进行重定向，再次连接服务器，并且验证；重定向且验证后表示登录成功

登录成功后获取角色列表
![](../images/2022-03-29-11-23-25.png)

获取角色回调后后使用第一个角色
![](../images/2022-03-29-11-34-28.png)
![](../images/2022-03-29-11-37-20.png)

使用第一个角色进行登录，登录角色服  
`发送: SprotoType.Role_RoleLogin`
![](../images/2022-03-29-11-38-52.png)

收到登录角色服的回调，返回角色信息
![](../images/2022-03-29-12-00-56.png)

![](../images/2022-03-29-12-03-44.png)

![](../images/2022-03-29-12-08-10.png)


### 内城初始化

### 地图初始化

![](../images/2022-03-29-14-40-41.png)

#### 相机位置初始化

相机参数初始化
![](../images/2022-03-29-14-43-09.png)

![](../images/2022-03-29-14-05-26.png)

![](../images/2022-03-29-14-02-22.png)
![](../images/2022-03-29-14-09-10.png)



#### 相机视野变化和同步视野到服务器

> 监听 `WorldCamera.Instance().AddViewChange(OnWorldViewChange);`
>![](../images/2022-03-29-14-08-18.png)  
>![](../images/2022-03-29-14-07-12.png)  
>![](../images/2022-03-29-14-10-28.png)  
> *发送给服务器相机移动的消息 `public void SendMapMove(long x, long y)` *
```
FogSystemMediator.cs(300):WorldCamera.Instance().AddViewChange(OnMapViewChange);
GlobalViewLevelMediator.cs(553):WorldCamera.Instance().AddViewChange(OnWorldViewChange);
MapUIiconMyCityMediator.cs(175):WorldCamera.Instance().AddViewChange(OnWorldViewChange);
PVPGlobalMediator.cs(468):WorldCamera.Instance().AddViewChange(OnWorldViewChange);
WorldMgrMediator.cs(312):WorldCamera.Instance().AddViewChange(OnWorldViewChange);
MainInterfaceMediator.cs(724):WorldCamera.Instance().AddViewChange(OnWorldViewChange);
WorldPanelMediator.cs(96):WorldCamera.Instance().AddViewChange(OnWorldViewChange);
```

#### 地图单位初始化
初始化添加单位及更新单位数据
![](../images/2022-03-29-14-58-41.png)
![](../images/2022-03-29-15-11-14.png)
相机视野改变，调整单位
![](../images/2022-03-29-15-12-38.png)


单位资源加载
```csharp
public static void WorldMapViewObjFactory.SysLoadWorldObj(MapObjectInfoEntity data, string prefabname, Action<GameObject, MapObjectInfoEntity> callback)

public void WorldMgrMediator.OnLoadMapObj(GameObject go,MapObjectInfoEntity data)
```

#### 地图地表及装饰物初始化

```c
public void ReadMapBriefDataFromFile2(string map_data_path, int server_x, int server_y, Action action = null)
```
![](../images/2022-03-29-16-49-32.png)
![](../images/2022-03-29-16-49-51.png)

#### LOD管理

#### 联盟区域数据及显示






