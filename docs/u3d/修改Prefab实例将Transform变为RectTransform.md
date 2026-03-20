---
title: "Unity 修改Prefab实例将Transform变为RectTransform"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Unity","Unity编辑器"]
categories: ["Unity"]
---

<!--more-->

> 引用：[Is there a way to destroy/replace a GameObject that is inside or part of a Prefab instance?](https://stackoverflow.com/questions/55525960/is-there-a-way-to-destroy-replace-a-gameobject-that-is-inside-or-part-of-a-prefa)
> *Changing Transform on a Prefab instance (jiantou) is not allowed.*
>这里用到的需求是做ui特效时将3Dmesh 渲染到ui层，用的ugui，ugui依赖于RectTransform，所以就有这个问题
## 将Prefab应用的Model对象的Transform修改为RectTransform

默认Model对象导入Transform组件，但是在ui中有些组件需要RectTransform组件，所以就需要强制将Transform变为RectTransform，这里通过调整Hierarchy面板内的prefab实例并且应用到prefab中，来完成修改，当然还有一个简单方法就是直接修改prefab

```csharp

        /// <summary>
        /// 把Prefab中的Transform替换为RectTransform
        /// 有个不足的地方是prefab的继承关系会丢失（Variant关系丢失）
        /// 如果一个prefab中引用另一个prefab，这种关系也会丢失
        /// </summary>
        /// <typeparam name="T">RectTransform</typeparam>
        /// <param name="obj"></param>
        private void AddComponentFromPrefab<T>(GameObject obj)  where T :UnityEngine.Component
        {
            PrefabAssetType prefabType = PrefabUtility.GetPrefabAssetType(obj);
            //Debug.Log($"AddComponentFromPrefab,name:{obj.name},PrefabAssetType:{prefabType}");
            switch (prefabType)
            {
                
                case PrefabAssetType.Regular:
                case PrefabAssetType.Variant:
                    //获取prefab实例的根节点
                    GameObject prefabRoot = PrefabUtility.GetOutermostPrefabInstanceRoot(obj);
                    //获取prefab资源，在project中的
                    GameObject prefabAsset = PrefabUtility.GetCorrespondingObjectFromSource(obj);
                    //Object prefabAsset = PrefabUtility.GetCorrespondingObjectFromOriginalSource(obj);
                    //获取资源的路径名字
                    string assetPath = AssetDatabase.GetAssetPath(prefabAsset);
                    //Debug.Log(assetPath);

                    //断开Model的联系，如果是Model是禁止修改RectTransform的
                    PrefabUtility.UnpackPrefabInstance(prefabRoot, PrefabUnpackMode.Completely, InteractionMode.AutomatedAction); //有个不足的地方是prefab的继承关系会丢失,这里是完全断开连接，非完全的方式没有测试
                    PrefabUtility.SaveAsPrefabAssetAndConnect(prefabRoot, assetPath, InteractionMode.AutomatedAction);

                    //修改prefab的RectTransform，如果修改实例的RectTransfom是失败的（Model虽然断开连接，但是还是禁止直接修改prefab实例的RectTransfom）
                    GameObject pobj = PrefabUtility.LoadPrefabContents(assetPath);
                    var ts=pobj.GetComponentsInChildren<Transform>();
                    foreach (var t in ts)
                        if (!(t is RectTransform))
                            t.gameObject.AddComponent<T>();
                    PrefabUtility.SaveAsPrefabAsset(pobj, assetPath);
                    PrefabUtility.UnloadPrefabContents(pobj);
                    break;
                case PrefabAssetType.Model:
                    PrefabUtility.UnpackPrefabInstanceAndReturnNewOutermostRoots(obj, PrefabUnpackMode.Completely);
                    if (!(obj.transform is T))
                        obj.AddComponent<T>();
                    break;
                default:
                    break;
            }
            

        }
```

测试
```csharp
AddComponentFromPrefab<RectTransform>(gameObject);
```
将测试代码写到Start方法中，且脚本设置`[ExecuteInEditMode]`标签，挂载prefab跟节点，
测试结果：
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20200729203806952.png)  

  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20200729204241328.png)  



结果：
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20200729203912335.png)  


  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20200729204139969.png)  


  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20200729204118121.png)  


**执行代码后Model引用变为prefab内的普通物体，切换修改成功RectTransform，并且prefab也已经修改成功**

## Prefab和GameObject的正向和逆向查找引用
> 转自 [Unity研究院之Prefab和GameObject的正向和逆向查找引用](http://www.xuanyusong.com/archives/2576)
```csharp

	[MenuItem("Assets/Check Prefab Use ?")]
	private static void OnSearchForReferences()
	{
	  //确保鼠标右键选择的是一个Prefab
		if(Selection.gameObjects.Length != 1)
		{
			return;
		}
 
		//遍历所有游戏场景
		foreach(EditorBuildSettingsScene scene in EditorBuildSettings.scenes)
		{
			if(scene.enabled)
			{
			  //打开场景
				EditorApplication.OpenScene(scene.path);
				//获取场景中的所有游戏对象
				GameObject []gos = (GameObject[])FindObjectsOfType(typeof(GameObject));
				foreach(GameObject go  in gos)
				{
				  //判断GameObject是否为一个Prefab的引用
					if(PrefabUtility.GetPrefabType(go)  == PrefabType.PrefabInstance)
					{
						UnityEngine.Object parentObject = EditorUtility.GetPrefabParent(go); 
						string path = AssetDatabase.GetAssetPath(parentObject);
						//判断GameObject的Prefab是否和右键选择的Prefab是同一路径。
						if(path == AssetDatabase.GetAssetPath(Selection.activeGameObject))
						{
							//输出场景名，以及Prefab引用的路径
							Debug.Log(scene.path  + "  " + GetGameObjectPath(go));
						}
					}
				}
			}
		}
	}
	public static string GetGameObjectPath(GameObject obj)
	{
		string path = "/" + obj.name;
		while (obj.transform.parent != null)
		{
			obj = obj.transform.parent.gameObject;
			path = "/" + obj.name + path;
		}
		return path;
	}
```
## Unity2018.4的Prefab Variant(Prefab变种)功能
> 转自[[Unity]Unity2018.4的Prefab Variant(Prefab变种)功能](http://blog.coolcoding.cn/?p=205)
> 
Unity 2018.4中送了一个新的功能: Prefab Variant

思路是, Prefab Variant 继承于一个父Prefab, 父Prefab属性修改后:

- (1)如果子Prefab的某些属性不动, 则父Prefab的属性影响子Prefab的属性, 此为 [属性继承]

- (2)如果对子Prefab的某些属性进行修改/覆盖, 则父Prefab的属性无法影响, 此为 [属性定制]

创建Prefab Variant的方法为: 把Prefab从Hierarchy再次拉到Project中,选择 Prefab Variant
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20200729205632565.png)  

  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20200729210005580.png)  



用处举例:

比如做一个UGUI窗体模板, 上面有标题文字和关闭按钮

邮件窗体继承于此窗体模板,制作成为一个PrefabVariant, 但是标题文字定制修改为”邮件”

这时,可以通过修改窗体模板中的关闭按钮,对所有派生的窗体按钮进行修改

附:以下为官方对PrefabAssetType的解释:
```
    public enum PrefabAssetType
    {
 
        //
        // 摘要:
        //     The object being queried is not part of a Prefab at all.
        NotAPrefab = 0, // 不是Prefab
 
        //
        // 摘要:
        //     The object being queried is part of a regular Prefab.
        Regular = 1, // 常规的Prefab
 
        //
        // 摘要:
        //     The object being queried is part of a Model Prefab.
        Model = 2, // 模型(例如:FBX)
 
        //
        // 摘要:
        // The object being queried is part of a Prefab Variant.
        // A Variant Prefab is a Prefab that is derived from another Prefab, 
        // that be could be a Regular, Model or even Variant Prefab.
        Variant = 3, // Prefab变种
 
        //
        // 摘要:
        //     The object being queried is part of a Prefab instance, but because the asset
        //     it missing the actual type of Prefab can’t be determined.
        MissingAsset = 4 // Prefab实例化出来的对象,但是Prefab被删了(红色)
    }
```