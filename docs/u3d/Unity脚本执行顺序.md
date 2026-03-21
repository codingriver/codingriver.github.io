# Unity脚本执行顺序

> 进阶测试参考[[unity脚本MonoBehaviour默认方法执行顺序测试](http://www.jianshu.com/p/574910aa3f52)
](http://www.jianshu.com/p/574910aa3f52)

将脚本挂到空物体上执行
```
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// Unity脚本执行顺序 测试
/// </summary>
public class TestCallSequence : MonoBehaviour
{

    void Awake()
    {
        Debug.Log("Awake^^^^^^^^^^^^^");
    }

    void OnEnable()
    {
        Debug.Log("OnEnable^^^^^^^^^^^^^");
    }    
    // Use this for initialization
    void Start()
   {
       Debug.Log("Start^^^^^^^^^^^^^");
    }


    void FixedUpdate()
    {
        Debug.Log("FixedUpdate^^^^^^^^^^^^^");

    }
    // Update is called once per frame
    void Update()
    {
        Debug.Log("Update^^^^^^^^^^^^^");
        
    }

    void LateUpdate()
    {
        Debug.Log("LateUpdate^^^^^^^^^^^^^");
        
    }

    void OnGUI()
    {
        Debug.Log("OnGUI^^^^^^^^^^^^^");
    }

    void Reset()
    {
        Debug.Log("Reset^^^^^^^^^^^^^");
    }

    void OnDisable()
    {
        Debug.Log("OnDisable^^^^^^^^^^^^^");
    }   

    void OnDestroy()
    {
        Debug.Log("OnDestroy^^^^^^^^^^^^^");
    }
}

```
执行结果




![执行结果](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-fedff950d9562364.png)  

*先运行脚本然后将将脚本组件改为非激活状态（active=false），然后停止运行。*
**上面的执行结果说明方法的调用顺序一部分是不固定的（FixedUpdate）。**

>　　Unity脚本从唤醒到销毁都有着一套比较完善的生命周期，添加任何脚本都要遵守生命周期法则！　　接下来介绍几种系统自调用的重要方法。首先要我们先来说明一下它们的执行顺序：　
Awake --> Start --> Update --> FixedUpdate --> LateUpdate -->OnGUI -->Reset --> OnDisable -->OnDestroy　　
下面我们针对每一个方法进行详细的说明：　　
1.Awake：用于在游戏开始之前初始化变量或游戏状态。在脚本整个生命周期内它仅被调用一次.Awake在所有对象被初始化之后调用，所以你可以安全的与其他对象对话或用诸如GameObject.FindWithTag()这样的函数搜索它们。每个游戏物体上的Awake以随机的顺序被调用。因此，你应该用Awake来设置脚本间的引用，并用Start来传递信息Awake总是在Start之前被调用。它不能用来执行协同程序。　　
2.Start：仅在Update函数第一次被调用前调用。Start在behaviour的生命周期中只被调用一次。它和Awake的不同是Start只在脚本实例被启用时调用。你可以按需调整延迟初始化代码。Awake总是在Start之前执行。这允许你协调初始化顺序。在所有脚本实例中，Start函数总是在Awake函数之后调用。　　
3.Update：正常帧更新，用于更新逻辑。每一帧都执行，处理Rigidbody时，需要用FixedUpdate代替Update。例如:给刚体加一个作用力时，你必须应用作用力在FixedUpdate里的固定帧，而不是Update中的帧。(两者帧长不同)FixedUpdate，每固定帧绘制时执行一次，和update不同的是FixedUpdate是渲染帧执行，如果你的渲染效率低下的时候FixedUpdate调用次数就会跟着下降。FixedUpdate比较适用于物理引擎的计算，因为是跟每帧渲染有关。Update就比较适合做控制。　　
4.FixedUpdate：固定帧更新，在Unity导航菜单栏中，点击“Edit”-->“Project Setting”-->“Time”菜单项后，右侧的Inspector视图将弹出时间管理器，其中“Fixed Timestep”选项用于设置FixedUpdate()的更新频率，更新频率默认为0.02s。　　
5.LateUpdate：在所有Update函数调用后被调用，和fixedupdate一样都是每一帧都被调用执行，这可用于调整脚本执行顺序。例如:当物体在Update里移动时，跟随物体的相机可以在LateUpdate里实现。LateUpdate,在每帧Update执行完毕调用，他是在所有update结束后才调用，比较适合用于命令脚本的执行。官网上例子是摄像机的跟随，都是在所有update操作完才跟进摄像机，不然就有可能出现摄像机已经推进了，但是视角里还未有角色的空帧出现。　　
6.OnGUI：在渲染和处理GUI事件时调用。比如：你画一个button或label时常常用到它。这意味着OnGUI也是每帧执行一次。　　
7.Reset：在用户点击检视面板的Reset按钮或者首次添加该组件时被调用。此函数只在编辑模式下被调用。Reset最常用于在检视面板中给定一个默认值。　　
8.OnDisable：当物体被销毁时 OnDisable将被调用，并且可用于任意清理代码。脚本被卸载时，OnDisable将被调用，OnEnable在脚本被载入后调用。注意： OnDisable不能用于协同程序。　　
9.OnDestroy：当MonoBehaviour将被销毁时，这个函数被调用。OnDestroy只会在预先已经被激活的游戏物体上被调用。注意：OnDestroy也不能用于协同程序。　　
备注：　　协同程序，即在主程序运行时同时开启另一段逻辑处理，来协同当前程序的执行。换句话说，开启协同程序就是开启一个线程。
协同程序，即在主程序运行时同时开启另一段逻辑处理，来协同当前程序的执行。换句话说，开启协同程序就是开启一个线程。在中，使用MonoBehaviour.StartCoroutine方法即可开启一个协同程序，也就是说该方法必须在MonoBehaviour或继承于MonoBehaviour的类中调用。
unity的生命周期;unity中画线;[unity3d](http://www.manew.com/)使用ondestroy;unity生命周期函数;unity onenable start;unity awake onenable;unity 生命周期;在unity画线;unity画线;unity3d ondestroy;unity 函数生命周期;unity start onenable;unity onenable awake
>引用文章:
> http://www.manew.com/thread-14461-1-1.html

![脚本的生命周期流程图](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/85844-f30df6032371595b.png);
>引用文章: http://www.jianshu.com/p/1d93ece664e2

#####如果在其他脚本里面实例化物体，且物体上挂有该脚本：
脚本会在实例化时（Instantiate）Awake直接同步执行，执行完后才执行Instantiate后面的代码
