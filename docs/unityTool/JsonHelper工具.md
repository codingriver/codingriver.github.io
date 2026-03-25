---
title: "JsonHelper工具"
date: "2021-12-20"
tags:
  - Unity
  - 工具链
  - Git
  - 网络
  - CSharp
categories:
  - unityTool
comments: true
---
# JsonHelper工具

>Json序列化和反序列化工具
>这里的Json工具使用的是Unity自带的JsonUtility，也可以使用[LitJson](https://github.com/codingriver/tools/tree/master/thirdPlugins/LitJson.zip)或者MiniJson等工具
>这里对比下JsonUtility和LitJson

`JsonHelper.cs`代码：
```csharp
using System;
using System.ComponentModel;
using System.Runtime.Serialization;
using UnityEngine;

namespace Codingriver
{
	public static class JsonHelper
	{
		public static string ToJson(object obj)
		{

			return JsonUtility.ToJson(obj);
		}

		public static T FromJson<T>(string str)
		{
			T t = JsonUtility.FromJson<T>(str);
			ISupportInitialize iSupportInitialize = t as ISupportInitialize;
			if (iSupportInitialize != null)
			{
                iSupportInitialize.EndInit();
            }
			

            IDeserializationCallback deserializationCallback = t as IDeserializationCallback;
            if(deserializationCallback!=null)
            {
                deserializationCallback.OnDeserialization(t);
            }
            return t;
		}

		public static object FromJson(Type type, string str)
		{
			object t = JsonUtility.FromJson(str,type);
			ISupportInitialize iSupportInitialize = t as ISupportInitialize;
            if (iSupportInitialize != null)
            {
                iSupportInitialize.EndInit();
            }

            IDeserializationCallback deserializationCallback = t as IDeserializationCallback;
            if (deserializationCallback != null)
            {
                deserializationCallback.OnDeserialization(t);
            }
            return t;
		}

		public static T Clone<T>(T t)
		{
			return FromJson<T>(ToJson(t));
		}
	}
}
```

JsonUtility和LitJson对比测试代码：
```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Codingriver;
using System.IO;
using System;
using LitJson;
using System.Runtime.Serialization;

public class JsonHelperTest : MonoBehaviour
{

    [Serializable]
    public class InnerTest
    {
        public class InnerA
        {
           public string innerStr = "严";
            int key = 99;
        }
        public int a = 1;
        public string b = "hello";
        int[] arr = new int[] { 5, 76, 12 };
        public InnerA innerA = new InnerA();
    }

    
    public class TestData: IDeserializationCallback
    {
        public string[] Sitekeys = new string[] { "river", "coding" };
        public string name = "codingriver";
        
        public int a = 1000;
        public int d = 3;
        public string b = "哈哈哈哈";
        [NonSerialized]
        public int c;
        protected string protect = "11111";
        
        int m_Main = 1024;

        [NonSerialized]
        public InnerTest obj = new InnerTest();

        public int Main
        {
            get
            {
                return m_Main;
            }
            set
            {
                m_Main = value;
            }
        }

        public void OnDeserialization(object sender)
        {
            c = a * d;
        }
    }


    // Start is called before the first frame update
    void Start()
    {
        TestData data = new TestData();
        data.Main = 2048;
        data.name = "你们好吗！";
        data.obj.a = 9;
        data.a = 7;
        data.d = 2;
        
        Debug.Log("origin:"+Dumper.DumpAsString(data));
        string json= JsonHelper.ToJson(data);
        Debug.Log("json:"+json);
        File.WriteAllText("./test.json", json);
        TestData data1 = JsonHelper.FromJson<TestData>(json);
        Debug.Log("data1:"+ Dumper.DumpAsString(data1));

        string litJson = JsonMapper.ToJson(data);
        Debug.Log($"litJson:{litJson}");
        TestData data2 = JsonMapper.ToObject<TestData>(litJson);
        Debug.Log($"data2:{Dumper.DumpAsString(data2)}");
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}


```

测试结果：
  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/JsonHelper工具/20200916173137.png)  
  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/JsonHelper工具/20200916175857.png)  

JsonUtility和LitJson对比说明：

- JsonUtility和LitJson默认都是序列化公有变量；保护变量和私有变量不能序列化。
- JsonUtility和LitJson都是支持序列化字段变量，不支持序列化属性变量（带set、get访问器的）。
- LitJson序列化的字符串如果是中文则结果是进行十六进制编码，而JsonUtility序列化后的字符串是字符串本身
- LitJson对于`NonSerialized`和`Serializable`特性配置是无效的。
- JsonUtility是支持`NonSerialized`和`Serializable`特性的，定义的类如果要被序列化需要标记`Serializable`特性，字段不想被序列化则标记`NonSerialized`特性。



* `Serializable` 仅对“类, 结构, 枚举, 委托”声明有效*