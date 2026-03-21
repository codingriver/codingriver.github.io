---
title: "unity脚本MonoBehaviour默认方法执行顺序测试"
date: "2026-03-21"
tags:
  - Unity
  - 网络
  - CSharp
categories:
  - u3d
comments: true
---
# unity脚本MonoBehaviour默认方法执行顺序测试

>基础的MonoBehaviour默认方法执行顺序参考上篇文章[Unity脚本执行顺序](https://www.jianshu.com/p/b69ef6ace840)
>>测试结果：
>>+ ######1.通过Instantiate加载Prefab时Awake和OnEnable会先后执行，并且在Instantiate执行过程中执行的；
>>+ ######2.通过SceneManager.LoadScene加载场景时是在当前代码块执行完成后并且执行Ondestroy后开始执行所加载场景test1内的代码的，所以在当前代码块调用完LoadScene后用GameObject.Find去获取场景内的物体时是获取不到的
>>+ ######3.在Awake中执行SceneManager.LoadScene，当前的Start方法是不会执行的
>>+ ######4.在执行gameObject.AddComponent<TestPrefab>().Init();时会先执行TestPrefab中的Awake和OnEnable后才执行Init

这里先上工程截图


![场景test2.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-2e4fb7b1860a8626.png)  



![场景test1.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-343d06bf491ff0eb.png)  



![TestPrefab.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-0e2e0397560d1425.png)  

*这里在TestPrefab上只挂TestPrefab一个脚本*


![TestPrefab2.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-c09e6dde3a4864cf.png)  

*这里在TestPrefab2上只挂TestPrefab2一个脚本*
**测试是在test2场景中运行，脚本加载切换到test1场景**

这里放上所有的脚本
```
//=====================================================
// - FileName:    	Test.cs
// - Created:		wangguoqing
// - UserName:		2018/03/02 14:04:52
// - Email:			wangguoqing@hehegames.cn
// - Description:	
// -  (C) Copyright 2008 - 2015, hehehuyu,Inc.
// -  All Rights Reserved.
//======================================================
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TestLoading : MonoBehaviour
{
    #region Method Call Order
    void Awake()
    {
        Debug.LogWarning("TestLoading:::Awake^^^Begin^^^^^^^^^^");
        //LoadPrefab();
        //LoadScene();
        Debug.LogWarning("TestLoading:::Awake^^^End^^^^^^^^^^");
    }

    void OnEnable()
    {
        Debug.LogWarning("TestLoading:::OnEnable^^^^^^^^^^^^^");
    }
    // Use this for initialization
    void Start()
    {
        Debug.LogWarning("TestLoading:::Start^^^^^^^^Begin^^^^^");
        LoadPrefab();
        LoadScene();
        Debug.LogWarning("TestLoading:::Start^^^^^^^^End^^^^^");
    }


    void LoadPrefab()
    {
        GameObject asset = Resources.Load<GameObject>("TestPrefab");
        GameObject obj = GameObject.Instantiate(asset);
    }
    void LoadScene()
    {
        UnityEngine.SceneManagement.SceneManager.LoadScene("test1");
    }

    void FixedUpdate()
    {
        //Debug.LogWarning("TestLoading:::FixedUpdate^^^^^^^^^^^^^");

    }
    // Update is called once per frame
    void Update()
    {
        //Debug.LogWarning("TestLoading:::Update^^^^^^^^^^^^^");

    }

    void LateUpdate()
    {
        //Debug.LogWarning("TestLoading:::LateUpdate^^^^^^^^^^^^^");

    }

    void OnGUI()
    {
        //Debug.LogWarning("TestLoading:::OnGUI^^^^^^^^^^^^^");
    }

    void Reset()
    {
        Debug.LogWarning("TestLoading:::Reset^^^^^^^^^^^^^");
    }

    void OnDisable()
    {
        Debug.LogWarning("TestLoading:::OnDisable^^^^^^^^^^^^^");
    }

    void OnDestroy()
    {
        Debug.LogWarning("TestLoading:::OnDestroy^^^^^^^^^^^^^");
    }
    #endregion
}

```
```
//=====================================================
// - FileName:    	TestScene.cs
// - Created:		wangguoqing
// - UserName:		2018/03/02 14:08:53
// - Email:			wangguoqing@hehegames.cn
// - Description:	
// -  (C) Copyright 2008 - 2015, hehehuyu,Inc.
// -  All Rights Reserved.
//======================================================
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TestScene : MonoBehaviour {

    #region Method Call Order
    void Awake()
    {
        Debug.Log("TestScene:::Awake^^^Begin^^^^^^^^^^");
        LoadPrefab();
        Debug.Log("TestScene:::Awake^^^End^^^^^^^^^^");
    }

    void OnEnable()
    {
        Debug.Log("TestScene:::OnEnable^^^^^^^^^^^^^");
    }
    // Use this for initialization
    void Start()
    {
        Debug.Log("TestScene:::Start^^^^^^^^^^^^^");
    }
    void LoadPrefab()
    {
        GameObject asset = Resources.Load<GameObject>("TestPrefab2");
        GameObject obj = GameObject.Instantiate(asset);
    }

    void FixedUpdate()
    {
        //Debug.Log("TestScene:::FixedUpdate^^^^^^^^^^^^^");

    }
    // Update is called once per frame
    void Update()
    {
        //Debug.Log("TestScene:::Update^^^^^^^^^^^^^");

    }

    void LateUpdate()
    {
        //Debug.Log("TestScene:::LateUpdate^^^^^^^^^^^^^");

    }

    void OnGUI()
    {
        //Debug.Log("TestScene:::OnGUI^^^^^^^^^^^^^");
    }

    void Reset()
    {
        Debug.Log("TestScene:::Reset^^^^^^^^^^^^^");
    }

    void OnDisable()
    {
        Debug.Log("TestScene:::OnDisable^^^^^^^^^^^^^");
    }

    void OnDestroy()
    {
        Debug.Log("TestScene:::OnDestroy^^^^^^^^^^^^^");
    }
    #endregion
}

```
```
//=====================================================
// - FileName:    	TestScene1.cs
// - Created:		wangguoqing
// - UserName:		2018/03/02 14:08:53
// - Email:			wangguoqing@hehegames.cn
// - Description:	
// -  (C) Copyright 2008 - 2015, hehehuyu,Inc.
// -  All Rights Reserved.
//======================================================
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TestScene1 : MonoBehaviour {

    #region Method Call Order
    void Awake()
    {
        Debug.Log("TestScene1:::Awake^^^^^^^^^^^^^");
    }

    void OnEnable()
    {
        Debug.Log("TestScene1:::OnEnable^^^^^^^^^^^^^");
    }
    // Use this for initialization
    void Start()
    {
        Debug.Log("TestScene1:::Start^^^^^^^^^^^^^");
    }


    void FixedUpdate()
    {
        //Debug.Log("TestScene1:::FixedUpdate^^^^^^^^^^^^^");

    }
    // Update is called once per frame
    void Update()
    {
        //Debug.Log("TestScene1:::Update^^^^^^^^^^^^^");

    }

    void LateUpdate()
    {
        //Debug.Log("TestScene1:::LateUpdate^^^^^^^^^^^^^");

    }

    void OnGUI()
    {
        //Debug.Log("TestScene1:::OnGUI^^^^^^^^^^^^^");
    }

    void Reset()
    {
        Debug.Log("TestScene1:::Reset^^^^^^^^^^^^^");
    }

    void OnDisable()
    {
        Debug.Log("TestScene1:::OnDisable^^^^^^^^^^^^^");
    }

    void OnDestroy()
    {
        Debug.Log("TestScene1:::OnDestroy^^^^^^^^^^^^^");
    }
    #endregion
}

```
```
//=====================================================
// - FileName:    	TestPrefab.cs
// - Created:		wangguoqing
// - UserName:		2018/03/02 14:04:52
// - Email:			wangguoqing@hehegames.cn
// - Description:	
// -  (C) Copyright 2008 - 2015, hehehuyu,Inc.
// -  All Rights Reserved.
//======================================================
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// Unity脚本执行顺序 测试
/// </summary>
public class TestPrefab : MonoBehaviour
{

    void Awake()
    {
        Debug.Log("TestPrefab:::Awake^^^^^^^^^^^^^");
    }

    void OnEnable()
    {
        Debug.Log("TestPrefab:::OnEnable^^^^^^^^^^^^^");
    }
    // Use this for initialization
    void Start()
    {
        Debug.Log("TestPrefab:::Start^^^^^^^^^^^^^");
    }

    public void Init()
    {
        Debug.Log("TestPrefab:::Init^^^^^^^^^^^^^");
    }
    void FixedUpdate()
    {
        //Debug.Log("TestPrefab:::FixedUpdate^^^^^^^^^^^^^");

    }
    // Update is called once per frame
    void Update()
    {
        //Debug.Log("TestPrefab:::Update^^^^^^^^^^^^^");

    }

    void LateUpdate()
    {
        //Debug.Log("TestPrefab:::LateUpdate^^^^^^^^^^^^^");

    }

    void OnGUI()
    {
        //Debug.Log("TestPrefab:::OnGUI^^^^^^^^^^^^^");
    }

    void Reset()
    {
        Debug.Log("TestPrefab:::Reset^^^^^^^^^^^^^");
    }

    void OnDisable()
    {
        Debug.Log("TestPrefab:::OnDisable^^^^^^^^^^^^^");
    }

    void OnDestroy()
    {
        Debug.Log("TestPrefab:::OnDestroy^^^^^^^^^^^^^");
    }
}

```
```
//=====================================================
// - FileName:    	TestPrefab2.cs
// - Created:		wangguoqing
// - UserName:		2018/03/02 14:04:52
// - Email:			wangguoqing@hehegames.cn
// - Description:	
// -  (C) Copyright 2008 - 2015, hehehuyu,Inc.
// -  All Rights Reserved.
//======================================================
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// Unity脚本执行顺序 测试
/// </summary>
public class TestPrefab2 : MonoBehaviour
{

    void Awake()
    {
        Debug.Log("TestPrefab2:::Awake^^^^^^^^^^^^^");
    }

    void OnEnable()
    {
        Debug.Log("TestPrefab2:::OnEnable^^^^^^^^^^^^^");
    }
    // Use this for initialization
    void Start()
    {
        Debug.Log("TestPrefab2:::Start^^^^^^^^^^^^^");
    }


    void FixedUpdate()
    {
        //Debug.Log("TestPrefab2:::FixedUpdate^^^^^^^^^^^^^");

    }
    // Update is called once per frame
    void Update()
    {
        //Debug.Log("TestPrefab2:::Update^^^^^^^^^^^^^");

    }

    void LateUpdate()
    {
        //Debug.Log("TestPrefab2:::LateUpdate^^^^^^^^^^^^^");

    }

    void OnGUI()
    {
        //Debug.Log("TestPrefab2:::OnGUI^^^^^^^^^^^^^");
    }

    void Reset()
    {
        Debug.Log("TestPrefab2:::Reset^^^^^^^^^^^^^");
    }

    void OnDisable()
    {
        Debug.Log("TestPrefab2:::OnDisable^^^^^^^^^^^^^");
    }

    void OnDestroy()
    {
        Debug.Log("TestPrefab2:::OnDestroy^^^^^^^^^^^^^");
    }
}

```
**在test2场景中直接运行后的结果**


![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-ba534b3ea7ecffcb.png)  


**将TestLoading在Awake方法和Start方法修改成如下**


![修改代码.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-6db091ad42a9701e.png)  

**在test2场景中直接运行上面修改后的结果**


![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-6a9805fec957e746.png)  


**结果表明：**
+ ######1. 通过Instantiate加载Prefab时Awake和OnEnable会先后执行，并且在Instantiate执行过程中执行的；
+ ######2.通过SceneManager.LoadScene加载场景时是在当前代码块执行完成后并且执行Ondestroy后开始执行所加载场景test1内的代码的，所以在当前代码块调用完LoadScene后用GameObject.Find去获取场景内的物体时是获取不到的
+ ######3.在Awake中执行SceneManager.LoadScene，当前的Start方法是不会执行的

***
***
**当添加脚本组件时如下代码**


![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-b68e47ea9010a6ef.png)  

执行结果为


![image.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-98ae4ead391bbc13.png)  

+ ######4.在执行gameObject.AddComponent<TestPrefab>().Init();时会先执行TestPrefab中的Awake和OnEnable后才执行Init
