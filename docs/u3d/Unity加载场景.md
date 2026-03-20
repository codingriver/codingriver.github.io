
---
title: "Unity加载场景"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Unity"]
categories: ["Unity"]
---

<!--more-->


>加载场景需要引入UnityEngine.SceneManagement这个命名空间，使用类SceneManager.
>这里说明下基本的代码加载机制，正常是要在场景加载完成后的Awake或者Start等方法去执行场景业务初始化。
```
//异步加载场景
public static AsyncOperation LoadSceneAsync(string sceneName, LoadSceneMode mode);
```
**异步加载后执行后面代码时，是在执行完场景中所有Awake方法且没有执行Start的时候**
```
//同步加载场景
public static void LoadScene(string sceneName, LoadSceneMode mode);
```
**同步加载后执行后面代码时，是在场景中所有Awake方法没有执行的时候调用的，且使用GameObject.Find("Game")方法是找不到场景中该物体的，但是场景中本身有该物体**

脚本：
```
using UnityEngine;
using System.Collections;
using System.Collections.Generic;
#if UNITY_EDITOR
using UnityEditor;
#endif
using System;
using System.IO;
using System.Text;
using Object = UnityEngine.Object;
using UnityEngine.SceneManagement;
public class AssetLoader : MonoBehaviour
{
public static AssetLoader Instance { get; private set; }
void Awake()
{
    Instance=this;
}
    /// <summary>
    /// 同步加载场景
    /// 说明：执行该方法后在后面直接使用GameObject.Find("Game"),是找不到对应物体的，需要加载完场景后场景的Awake执行后才能Find到物体
    /// </summary>
    /// <param name="sceneName">场景名</param>
    /// <param name="isAdditive">是否叠加场景</param>
    public static void LoadSceneSync(string sceneName,bool isAdditive=false)
    {
        SceneManager.LoadScene(sceneName);
    }

    /// <summary>
    /// 异步加载场景
    /// action调用的时候是在场景加载完成且场景所有的Awake执行完后调用（Start还没有执行的时候）
    /// </summary>
    /// <param name="sceneName">场景名</param>
    /// <param name="action">加载完成回调</param>
    /// <param name="isAdditive">是否叠加场景</param>
    public static void LoadSceneAsync(string sceneName,Action action,bool isAdditive=false)
    {
        Instance.InnerLoadSceneAsync(sceneName, action, isAdditive);
    }
    private void InnerLoadSceneAsync(string sceneName, Action action, bool isAdditive)
    {
        StartCoroutine(LoadLeveAsync(sceneName, action, isAdditive));
    }

    private IEnumerator LoadLeveAsync(string sceneName, Action action, bool isAdditive)
    {
        LoadSceneMode mode = isAdditive ? LoadSceneMode.Additive : LoadSceneMode.Single;
        yield return SceneManager.LoadSceneAsync(sceneName, mode);
        if (!isAdditive) GC.Collect();
        action();
    }

}
```
