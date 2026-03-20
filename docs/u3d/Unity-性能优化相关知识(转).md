---
title: "Unity 性能优化相关知识(转)"
subtitle: "Unity 性能优化相关知识(转)"
date: 2020-09-23T20:54:44+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Unity"]
categories: ["Unity"]
draft: true
---

<!--more-->

## 一、综合优化

1、降低屏幕分辨率尤其是在android平台对性能提升很大。可以有效缓解gpu的压力。

　　我们在android上分辨率是实际的0.85左右。

2、做好资源异步加载，实现一个实例化队列，可以很大程度上减少卡顿。

3、做好超量的模型和特效屏蔽，可以有效减轻cpu压力。

4、善用工具。比如Unity Profiler、Snapdragon Profiler等，针对性的对性能瓶颈进行优化。

5、玩家头顶血条的HUD要使用3D的，而不是UGUI。否则同屏玩家数量很多的时候Mesh合并开销很大。

6、UI上使用TextMeshPro。可以很大程度上缓解UI打开卡顿的问题。描边、阴影开销很低。

7、控制帧率。现在高刷新率的手机非常多。不要直接使用VSyncCount控制帧率了。否则在120hz刷新率的手机上vSyncCount=1会有120fps的帧率。直接使用targetFrameRate=30来设置帧率。



## 二、优化的经验

### (一) UI的性能优化

1、写一个UICollider而不是透明的Image，可以减少overdraw

2、小地图用shader实现指定位置的图片渲染，而不是RectMask2D，可以减少overdraw。因为RectMask2D是使用alpha=0来实现裁剪的。

3、小地图的玩家标识，聊天界面，都添加Canvas，目的是动静分离。

4、使用TextMeshPro。减少GC，减少字体生成的开销。字体放大缩小依然保持锐利清晰。

5、玩家头顶的HUD，比如血条和名字，使用3D的TextMeshPro和SpriteRenderer，目的是避免UGUI的mesh计算开销。MMO中的头顶血条可能会有同屏几百个人。

　　血条的减少动画之前是Image和DOTween来实现的。后面修改为shader实现。(坐标计算)

6、战斗飘字，原先是DOTween来实现的，后面修改为直接在Update里面计算坐标。目的是减少DOTween动画初始化的GC开销。自己实现简化版的动画，性能也更好一些。

　　战斗飘字还是用UGUI来实现。主要是因为这里还是美术给的艺术字。而且飘字只有玩家自己才会显示，数量不会很多。

7、实现一个高效率的 FindChlid 函数。因为在写UI的时候查询控件对象是非常常见的操作。如果不做优化，使用 gameObject.name == "xxx" 来做比对的话，可能会产生很多的GCAlloc。

8、使用SimpleAnimationComponent 来做UI动画，而不直接使用Animator。因为Animator在动画播放完毕之后，依然会Update。这会导致两个问题，一个是性能隐患，另外一个是被动画控制的控件无法再通过代码设置位置。在动画播放完毕之后再禁用动画组件，实现起来比较复杂。相比而言，直接使用SimpleAnimationComponent就要简单干净很多，也更加高效。

9、禁用不必要的raycastTarget。

10、实现一个UICircleImage来替代用Mask实现的圆形遮罩裁剪。一般64个点就可以形成圆形。外部再罩一个边框图，就可以消除边缘锯齿。



### (二) 场景的性能优化

1、要勾选StaticBatch，但是不能滥用。有color、uv3的，顶点超过4000个以上的，数量超多，但是同屏显示不多的模型。这些都不应该勾选StaticBatch。否则会导致包体积明显增大。因为StaticBatch会把模型都build到场景的ab包内。

2、注意压缩纹理的使用。法线应该用etc2，ios下用astc6x6，法线需要更高的精度，要避免压缩纹理导致的失真。

3、避免模型和贴图勾选 readable选项。这个可以在模型和纹理导入的时候做设置。

4、光照贴图和shadowmask图的压缩纹理选项。ios下可以统一使用astc6x6。android下shadowmask图使用rgb16，否则阴影会有明显的模糊或者锯齿。lightmap图倒是没有太大限制，尽量使用压缩纹理即可。

### (三) 战斗的性能优化

1、设计一套完善的屏蔽规则。保证玩家自己的模型和特效显示。

2、异步加载资源，模型、特效和声音。缓存池的使用。

3、同屏玩家数量很多的时候，屏蔽超额的模型、特效和技能流程。只保留技能数值逻辑即可。

　　注意，屏蔽特效要以玩家为单位进行屏蔽。我们之前以特效为单位屏蔽会出现坐骑身上左翅膀有特效，右翅膀没有特效的情况。

4、更多的细节优化。比如lua到C#的调用。一些频繁调用的接口，能用简单类型做参数，就不要弄一个结构体出来。xlua有针对这里做NoGC的性能优化。

5、缓存，预加载特效。两个预加载时机，游戏初始化的时候，或者技能模板初始化的时候。

### (四) 内存的性能优化

1、压缩纹理的使用。

2、合理的释放不必要的资源。引用计数。定期UnloadUnusedAssets

3、粒子系统缓存占用的内存。一个ParticleSystem占用8k内存。特效缓存的多了，可能会占用几十兆内存。

4、Shader Lab内存。变体多了，加载的shader多了。这块儿的内存占用可能会比较大。三四十兆都是有可能的。

5、Lua配置的内存优化

5.1、我们业务逻辑都是lua写的，所以配置直接导出为lua文件，而不再需要有额外的解析过程。

5.2、lua中（luajit）没有整型，所有类型都是double。所以与C++相比配置文件超级占内存。我们现在lua占用内存启动游戏后会有40兆左右。其中30兆都是配置文件所占用的内存。

5.3、导出的配置的格式是数组结构，不是key value结构。通过给每个条目设置metatable，业务层同样可以用key来访问对应的数据。这样可以节省一半以上的内存。

5.4、客户端不用的列不用导出。避免浪费。

5.5、超大的配置，可以导出为sqlite。这样只有需要的时候才会加载对应的数据，而不会把整个表格都加载进来。

5.6、C#用到的配置，直接导出为json。不要导出为lua又再设置给C#。

### (五) 卡顿的性能优化

1、GCAlloc。可能发生GCAlloc的情景。比如实例化资源，new对象。以及gameObject.SetActive、闭包调用、gameObject.name读写等等。

2、通过Profiler查找热点是什么，针对性的进行优化。

3、不要频繁调用activeSelf=true。要先做好判断，只在需要以及必要的时候调用。

4、特效不用的时候，停掉ParticleSystem，然后把特效丢到很远的地方，而不是active。同样是减少开销大的接口调用。

5、像图片不显示可以把alpha=0，或者文字不显示可以直接设置一个空的字符串。而不是直接active禁用。这样也可以提升效率。

6、lua调用C#的时候尽可能减少字符串的传递。字符串在lua和C#的交互过程中不可避免的会产生多份内存开销，且有可能还会有编码转换的开销。比如lua中获取一个组件，可以用组件Type作为参数传递，而不是组件名。

7、注意字符串比较时的参数传递。一般都是Ordinal。使用Culture的参数会考虑国际化因素，性能较低。同理，可以实现一个 StartWithFast，简单进行字符比对。它会比C#默认的StartWith快很多。

8、使用同一的CoroutineManager而不是直接用MonoBehaviour的StartCoroutine，可以提高性能。

9、尽可能的减少MonoBehaviour的Update的调用。比如我们的Actor，都是通过ObjectManager来驱动Update。

10、Unity的Profiler不会跟踪主线程之外的GCAlloc分配。如果在子线程需要进行分析，可以考虑把子线程切换的主线程进行调试，或者使用功能BeginThreadProfiling API。

11、在每帧执行的代码中，尽可能避免闭包。减少匿名方法。这些可能会产生GCAlloc。

12、避免使用枚举作为字典的key。会有装箱操作。原因是enum为值类型，Dictionary实现会调用Object.getHashCode获取key的哈希代码，这里期望的是引用类型。

　　可以考虑强制转换为int即可。或者实现一个 IEqualityComparer。

13、foreach 虽然在5.5的版本以上不再有因为装箱产生的GCalloc的开销。但是与for相比还是有性能差距。所以在调用不频繁的地方，可以使用foreach以提高可读性。频繁调用的地方还是推荐直接用for进行遍历。

14、慎用 mesh.vertices 等接口。它每次调用都会生成一个新的内存副本。同理 Input.touches类似。

15、Physics的接口中也会有对应的NonAlloc版本。

16、C#的string是不可变的，任何SubSting等操作都会产生新的副本。

### (六) 一般优化

1、按ID寻址属性。比如 Animator、Shader都有对应的接口。Animator.StringToHash。Shader.PropertyToID。

2、使用非分配物理API。替换Physics.RaycastAll为Physics.RaycastNonAlloc等。

3、UnityEngine.Object == null 比纯C#对象判定成本要高很多。因为它要判定对象（可能是资源）是否存在，是否有被Destroy掉。

4、减少矢量和四元数的数学计算。控制运算顺序。

5、隐形颜色字符串转换的时候 （#RRGGBBAA），使用一个 ColorUtility 的API会更加高效，且可以避免GCAlloc。

6、尽可能避免使用 Find 或者 FindObjectOfType

7、尽可能减少 Camera.,main 的调用。它内部会调用 Object.FindObjectWithTag。在Start中进行缓存。

8、调试代码可以增加 [Conditional("DEBUG")] 这样的标签。防止开发版本的代码或者日志发布出去。频繁打Log会对性能有严重影响。

9、不要用 type[x, y] 这样的多维数组。性能很低。

10、Update统一放到管理器里面进行更新。而不要每个对象一个Update。

11、合理使用C#的委托。每次添加或者删除回调的时候，C#的委托都会执行回调列表的完整拷贝。所以不要在Update中进行委托的添加或者删除回调的操作。如果有频繁添加的需求，可以考虑使用List维护回调数组而不是委托。

12、手工编码的 String.StartsWithFast 会比内置方法快 10~100倍。

13、Vector3.zero 会返回一个新的Vector3对象。虽然因为其是值类型，远比引用类型性能要高。但是频繁调用的地方还是应该维护一个const的对象用来进行比对或者赋值。

14、更新材质属性的时候，使用MaterialPropertyBlock。性能更好。且可以避免实例化一份新的材质对象。

15、AlphaBlend会比AlphaTest性能要好一些。因为移动平台的GPU会有EarlyZ的优化，而AlphaTest会使EarlyZ无效。

16、低版本的Unity上使用的是PhysicX 2的版本，移动没有刚体的静态碰撞体会导致整个物理世界重建，会有较大的开销。在新版本的Unity里面已经升级到 PhysicX 3，解决了这个问题。

17、使用SimpleAnimationComponent来替代Unity的Animator来做UI动画。主要是Animator会一直更新，即便动画已经播放完毕了。这个一方面会有性能问题，另外一方面被动画驱动的控件无法再通过脚本移动。

18、统一封装 Time.deltaTime和 Time.realTimeSinceStartup。因为这个调用是有一定开销的，至少存在C#到C++的调用。统一在入口Update处调用并缓存。在大量业务逻辑调用，直接取缓存的值。



### (七) Lua的性能优化

1、扩展Unity的API，简化.localPosition等调用的交互次数。

　　尽可能的减少lua和C#的参数传递。比如通过扩展Unity接口，实现SetPosition直接给gameObject或者Component设置坐标，而不用 go.transform.position = xxx 这样设置坐标。

2、减少使用 os.date 函数。会有明显的内存分配。

3、在Update中频繁执行的代码，避免各种临时表的分配。

4、配表的内存优化。

5、使用 table.concat 组合字符串，而不是 .. 连接。因为字符串每次 .. 都会产生一份新的字符串内存。

6、尽可能避免数组、字典或者自定义类型的交互参数，这会产生大量的GCAlloc。如果是数组，可以考虑使用一个循环遍历调用。

7、尽可能避免lua到C#传递字符串参数。传递字符串操作不可避免的会有多份内存开销，C#需要把lua的字符串内存拷贝到托管堆中，这是性能低下且有GCAlloc的。

　　比如我们GetComponent获取类型，就统一使用type(http://CS.XXX)这样的类型做参数，而没有使用字符串获取组件。无论从交互的角度考虑，还是在C#内部获取组件的效率考虑，都会获得更好的性能。



### (八) Shader的性能优化经验

1、使用Mobile版本的shader。比如Particle/Additive中有ColorMask，这个在移动平台比较耗。

2、避免使用昂贵的数学函数。比如 pow exp log cos sin tan 等。

3、尽可能减少纹理采样数目。

4、如果有一些计算比较复杂，可以使用查找纹理（lut）

5、优先使用低精度的数字格式。优先使用half。在现代gpu上fixed等同于half。 部分对精度有特殊需求的情况下才使用float。个别情况下，尤其是与法线相关的时候，使用half容易因为精度不足导致渲染结果错误，这个时候还是应该使用float。

### (九) 资源规格

1、模型角色高模 6000+面，低模 3000面。顶点数不定，因为顶点存在共用的情况，所以顶点数量可能是面数的两倍，也可能比面数低。纹理使用1024大小的贴图。低模纹理大小减半。主角因为有高低模，所以不开mipmap。个别精度比较高的npc（有UI显示需求）需要开mipmap，否则场景中会有明显的闪烁。

2、场景的drawcall控制在200以下。个别场景因为美术需求，drawcall可能会更高一些，但是SetPassCall也要尽可能保证比较小（材质尽可能共用，可以有效减少SetPassCall）

3、场景的面数在100k~300k之间都是合理的数值。

4、UI的drawcall100以下，一般就是三四十常驻UI Drawcall。

### (十) 性能优化的常用工具

1、Unity Profiler。 deep profile。

2、Miku-LuaProfiler

3、Frame debugger

4、Snapdragon Profiler或者RenderDoc

5、Xcode的instrument

6、Intel GPA

>转自：[性能优化相关知识](https://zhuanlan.zhihu.com/p/157877557)