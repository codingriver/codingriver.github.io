---
title: "【Unity编辑器】 扩展菜单项及右键菜单"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Unity编辑器"]
categories: ["Unity编辑器"]
---

<!--more-->

>今天用到了在Hierarchy中扩展右键的功能，这里整理下菜单扩展资料
>这里只是简单整理，如果需要详细的直接看参考文章

### API说明：

```
    [AttributeUsage(AttributeTargets.Method, AllowMultiple = true)]
    [RequiredByNativeCode]
    public sealed class MenuItem : Attribute
    {
        public string menuItem;
        public bool validate;
        public int priority;
        public MenuItem(string itemName);
        public MenuItem(string itemName, bool isValidateFunction);
        public MenuItem(string itemName, bool isValidateFunction, int priority);
    }
```
可知MenuItem最多有三个参数： 
- 参数一表示MenuItem所处的路径 
- 参数二表示是否有验证方法 
- 参数三表示MenuItem在整个Menu中所处的优先级 

### 普通用法
需要将脚本放到Editor目录中；Editor目录可以在其他普通目录的子目录中
需要UnityEditor命名空间
```c
    [MenuItem("Tools/Test", false, 2200)]
    public static void Create(MenuCommand menuCommand)
    {
	    GameObject parent = menuCommand.context as GameObject;
    }
```
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181203185654802.png)  

### 特殊用法
**在project右键使用**
```c
    [MenuItem("Assets/Tes2", false)]
    public static void Create2()
    {
    }
```
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181203185621295.png)  

**在Hierarchy右键使用**
```c
    /*
     * 这里注意 priority参数，值要控制在-10到49之间
     */
    [MenuItem("GameObject/Tes1", false, 0)]
    public static void Create1()
    {

    }
```
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181203185637406.png)  

**在Scene右键使用**

```c
    [InitializeOnLoadMethod]
    static void Init()
    {
        SceneView.onSceneGUIDelegate += OnSceneGUI;
    }
    static void OnSceneGUI(SceneView sceneView)
    {
        Event e = Event.current;
        if (e != null && e.button == 1 && e.type == EventType.MouseUp)
        {
            //右键单击啦，在这里显示菜单
            GenericMenu menu = new GenericMenu();
            menu.AddItem(new GUIContent("菜单项1"), false, OnMenuClick, "menu_1");
            menu.AddItem(new GUIContent("菜单项2"), false, OnMenuClick, "menu_2");
            menu.AddItem(new GUIContent("菜单项3"), false, OnMenuClick, "menu_3");
            menu.ShowAsContext();
        }
    }
    static void OnMenuClick(object userData)
    {
        EditorUtility.DisplayDialog("Tip", "OnMenuClick" + userData.ToString(), "Ok");
    }
```
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181203185725973.png)  


>参考文章：
>[Unity编辑器扩展-在Scene视图添加右键菜单](https://blog.csdn.net/yudianxia/article/details/79793978)
>https://blog.csdn.net/zw514159799/article/details/50775502
>http://m.manew.com/thread-90330-1-1.html
>https://blog.csdn.net/WPAPA/article/details/51066397
