---
title: "【Unity编辑器】MeshRenderer和SkinnedMeshRenderer在Inspector增加sortingLayer选项"
date: 2020-09-14T20:55:09+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
toc: false
tags: ["Unity编辑器"]
categories: ["Unity编辑器"]
---

<!--more-->

>MeshRenderer和SkinnedMeshRenderer在Inspector增加sortingLayerName和sortingOrder选项。  
> Unity的SortingLayer在MeshRenderer和SkinnedMeshRendererEditor中的Inspector面板不可以配置，而想要调整SortingLayer或者sortingOrder则需要在脚本中设置比如脚本的Awake或者Start，这样非常不灵活。  
> 通过Hooker钩子修改Inspector的MeshRendererEditor和SkinnedMeshRendererEditor而达到SortingLayer参数暴露在编辑器中，这样可以直接修改了在物体的MeshRenderer和SkinnedMeshRenderer组件上，修改后的值自动存储在序列化数据里。  
> 这里使用了一个Githubh的插件 [MonoHook](https://github.com/Misaka-Mikoto-Tech/MonoHook)，请自行下载，然后导入到工程中。


- 首先需要下载MonoHook插件，导入到工程中，这里的代码需要依赖这个插件。  
- 然后将文件`RendererLayerEditor.cs`和`InitializeOnLoadTool.cs`放入Editor目录下，这个是编辑器代码文件。  


`RendererLayerEditor.cs`文件：  
```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;
using System;
using System.Reflection;
using UnityEditorInternal;


public class RendererLayerEditor
{
    public static void Register()
    {

        // MeshRendererEditor
        Type type = typeof(AssetDatabase).Assembly.GetType("UnityEditor.MeshRendererEditor");
        MethodInfo method = type.GetMethod("OnInspectorGUI", BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic);
        type = typeof(RendererLayerEditor);
        MethodInfo methodReplacement = type.GetMethod("SubRendererOnInspectorGUI", BindingFlags.Static | BindingFlags.NonPublic);
        MethodInfo methodProxy = type.GetMethod("SubRendererOnInspectorGUIProxy", BindingFlags.Static | BindingFlags.NonPublic);
        MethodHook hooker = new MethodHook(method, methodReplacement, methodProxy);
        hooker.Install();

        // SkinnedMeshRendererEditor
        type = typeof(AssetDatabase).Assembly.GetType("UnityEditor.SkinnedMeshRendererEditor");
        method = type.GetMethod("OnInspectorGUI", BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic);
        type = typeof(RendererLayerEditor);
        methodReplacement = type.GetMethod("SubRendererOnInspectorGUI", BindingFlags.Static | BindingFlags.NonPublic);
        methodProxy = type.GetMethod("SubRendererOnInspectorGUIProxyE", BindingFlags.Static | BindingFlags.NonPublic);
        hooker = new MethodHook(method, methodReplacement, methodProxy);
        hooker.Install();
    }

    static void SubRendererOnInspectorGUI(Editor editor)
    {
        //Debug.Log(editor.target);
        if (editor.target != null)
        {

            var renderer = editor.target as Renderer;

            var options = GetSortingLayerNames();
            var picks = new int[options.Length];
            //Debug.Log($"renderer.sortingLayerName:{renderer.sortingLayerName},options.len:{options.Length}");
            var name = renderer.sortingLayerName;
            var choice = -1;
            for (int i = 0; i < options.Length; i++)
            {
                picks[i] = i;
                if (name == options[i]) choice = i;
            }

            choice = EditorGUILayout.IntPopup("Sorting Layer", choice, options, picks);


            string oldLayerName = renderer.sortingLayerName;
            renderer.sortingLayerName = options[choice];

            int order = renderer.sortingOrder;
            renderer.sortingOrder = EditorGUILayout.IntField("Sorting Order", renderer.sortingOrder);

            if(renderer.sortingOrder!=order||renderer.sortingLayerName!= oldLayerName)
            {
                EditorUtility.SetDirty(renderer);
            }
            if(editor.target is MeshRenderer)
            {
                SubRendererOnInspectorGUIProxy(editor);
            }
            else 
            {
                SubRendererOnInspectorGUIProxyE(editor);
            }
            
        }
        

    }

    static void SubRendererOnInspectorGUIProxy(Editor editor)
    {

    }
    static void SubRendererOnInspectorGUIProxyE(Editor editor)
    {

    }
    public static string[] GetSortingLayerNames()
    {
        //SortingLayer.layers
        Type internalEditorUtilityType = typeof(InternalEditorUtility);
        PropertyInfo sortingLayersProperty = internalEditorUtilityType.GetProperty("sortingLayerNames", BindingFlags.Static | BindingFlags.NonPublic);
        return (string[])sortingLayersProperty.GetValue(null, new object[0]);
    }
}

```
**MonoHook插件需要打开unsafe宏定义，`Build Setting`-->`Player Setting`--> 勾选 `Allow unsafe Code` 如图：**
  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/MeshRenderer在Inspector设置SorttingLayerName和SorttingOrder/20200914222927.png)  

 
`InitializeOnLoadTool.cs`文件：
```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;
using System;
using System.Reflection;
using UnityEditorInternal;

[InitializeOnLoad] // 最好Editor启动及重新编译完毕就执行
public class InitializeOnLoadTool
{
    static bool register = false;
    
    static InitializeOnLoadTool()
    {
        if (!register)
        {
            RendererLayerEditor.Register();
            register =true;
        }

    }

}

```

效果：
`MeshRenderer`    
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/MeshRenderer在Inspector设置SorttingLayerName和SorttingOrder/20200914210918.png)  
  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/MeshRenderer在Inspector设置SorttingLayerName和SorttingOrder/20200914210942.png)  

`SkinnedMeshRenderer`    
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/MeshRenderer在Inspector设置SorttingLayerName和SorttingOrder/20200914211053.png)  

> [Githuh工程](https://github.com/codingriver/Project/tree/master/UnityEditorProject/Assets/Editor/Tools)