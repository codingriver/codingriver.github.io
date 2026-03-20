---
title: "StringHelper编码辅助工具"
date: 2020-09-16T21:38:31+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Unity Tool","Unicode编码"]
categories: ["Unity Tool"]
---

<!--more-->

>StringHelper编码辅助工具 (C#)  
>
>Unicode编码介绍参考文章：  [ASCII，Unicode，UTF-16 和 UTF-8编码等字符编码]({{< ref "ASCII，Unicode和UTF-8.md" >}})
>
>[URL编码与解码原理]({{<ref "URL编码与解码原理.md" >}})
>
>这里处理了Unicode编码相关操作，以及增加String类辅助方法。


**String转Unicode编码（中文转Unicode编码）**

```csharp
        /// <summary>
        /// 字符串转Unicode编码
        /// </summary>
        /// <param name="str"></param>
        /// <returns>UTF-16 BE，大头方式</returns>
        public static string ToUnicode(this string str)
        {
            StringBuilder builder = new StringBuilder(str.Length * 6);
            for (int i = 0; i < str.Length; i++)
            {
                builder.AppendFormat("\\u{0:X4}",(ushort)str[i]);
            }
            return builder.ToString();
        }
```

**Unicode编码转String（Unicode编码转中文）**


```csharp
        /// <summary>
        /// Unicode编码转字符串
        /// </summary>
        /// <param name="unicodeStr">UTF-16 BE，大头方式</param>
        /// <returns></returns>
        public static string FromUnicode(this string unicodeStr)
        {
            if (unicodeStr.Length % 6 != 0)
            {
                throw new ArgumentException(String.Format(CultureInfo.InvariantCulture, "The unicode string cannot have an odd number of digits: {0}", unicodeStr));
            }
            StringBuilder builder = new StringBuilder(unicodeStr.Length/6);

            for (int i = 0; i < unicodeStr.Length; i+=6)
            {
                if(unicodeStr[i]=='\\'&&(unicodeStr[i+1]=='u'|| unicodeStr[i + 1] == 'U'))
                {
                    byte high = (byte)((Parse(unicodeStr[i+2])<<4)| Parse(unicodeStr[i + 3]));
                    byte low= (byte)((Parse(unicodeStr[i + 4]) << 4) | Parse(unicodeStr[i + 5]));
                    ushort value = (ushort)((high << 8) | low);
                    builder.Append((char)value);
                }
            }
            return builder.ToString();
        }
        private static int Parse(char c)
        {
            if (c >= 'a')
                return (c - 'a' + 10) & 0x0f;
            if (c >= 'A')
                return (c - 'A' + 10) & 0x0f;
            return (c - '0') & 0x0f;
        }
```

**十六进制字符串转字节数组**

```csharp
        public static byte[] HexToBytes(this string hexString)
        {
            if (hexString.Length % 2 != 0)
            {
                throw new ArgumentException(String.Format(CultureInfo.InvariantCulture, "The binary key cannot have an odd number of digits: {0}", hexString));
            }
            var hexAsBytes = new byte[hexString.Length / 2];
            for (int index = 0; index < hexAsBytes.Length; index++)
                hexAsBytes[index] = (byte)((Parse(hexString[index*2]) << 4) | Parse(hexString[index * 2+1]));
            
            return hexAsBytes;
        }
```

**字节数组转十六进制字符串**

```csharp
        public static string ToHex(this byte[] bytes)
        {
            StringBuilder stringBuilder = new StringBuilder(bytes.Length*2);
            for (int i = 0; i < bytes.Length; i++)
            {
                stringBuilder.Append(bytes[i].ToString("X2"));
            }
            return stringBuilder.ToString();
        }
        public static string ToHex(this byte[] bytes,int index,int count)
        {
            StringBuilder stringBuilder = new StringBuilder(count * 2);
            for (int i = 0; i < count; i++)
            {
                stringBuilder.Append(bytes[index+i].ToString("X2"));
            }
            return stringBuilder.ToString();
        }
```

**字节数组转字符串（UTF-16 BE）**

```csharp
            if(bytes.Length%2!=0)
            {
                throw new ArgumentException(String.Format(CultureInfo.InvariantCulture, "The binary key cannot have an odd number of digits: {0}", bytes.ToHex()));
            }

            StringBuilder builder = new StringBuilder(bytes.Length / 2);
            for (int i = 0; i < bytes.Length; i+=2)
            {
                ushort value = (ushort)((bytes[i + 1] << 8) | bytes[i]);
                builder.Append((char)value);
            }
            return builder.ToString();

```

**字符串（UTF-16 BE）转字节数组**

```csharp
        /// <summary>
        /// 
        /// </summary>
        /// <param name="str"></param>
        /// <returns>UTF-16 BE，大头方式</returns>
		public static byte[] ToBytes(this string str)
		{
            byte[] bytes = new byte[str.Length * 2];
            for (int i = 0; i < str.Length; i++)
            {
                bytes[i * 2] = (byte)(((ushort)str[i]) & 0xFF);
                bytes[i * 2+1] = (byte)(((ushort)str[i]>>8) & 0xFF);
            }
			return bytes;
		}

```

`StringHelper.cs`代码：

```csharp
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Text;

namespace Codingriver
{
	public static class StringHelper
	{

        /// <summary>
        /// 
        /// </summary>
        /// <param name="str"></param>
        /// <returns>UTF-16 BE，大头方式</returns>
		public static byte[] ToBytes(this string str)
		{
            byte[] bytes = new byte[str.Length * 2];
            for (int i = 0; i < str.Length; i++)
            {
                bytes[i * 2] = (byte)(((ushort)str[i]) & 0xFF);
                bytes[i * 2+1] = (byte)(((ushort)str[i]>>8) & 0xFF);
            }
			return bytes;
		}
        //public static byte[] ToBytes(this string str)
        //{
        //    byte[] byteArray = Encoding.Default.GetBytes(str);
        //    return byteArray;
        //}
        public static IEnumerable<byte> ToBytesItor(this string str)
        {
            byte[] byteArray = Encoding.Default.GetBytes(str);
            return byteArray;
        }

        public static byte[] ToUtf8(this string str)
	    {
            byte[] byteArray = Encoding.UTF8.GetBytes(str);
            return byteArray;
        }

        /// <summary>
        /// 字符串转Unicode编码
        /// </summary>
        /// <param name="str"></param>
        /// <returns>UTF-16 BE，大头方式</returns>
        public static string ToUnicode(this string str)
        {
            StringBuilder builder = new StringBuilder(str.Length * 6);
            for (int i = 0; i < str.Length; i++)
            {
                builder.AppendFormat("\\u{0:X4}",(ushort)str[i]);
            }
            return builder.ToString();
        }

        /// <summary>
        /// Unicode编码转字符串
        /// </summary>
        /// <param name="unicodeStr">UTF-16 BE，大头方式</param>
        /// <returns></returns>
        public static string FromUnicode(this string unicodeStr)
        {
            if (unicodeStr.Length % 6 != 0)
            {
                throw new ArgumentException(String.Format(CultureInfo.InvariantCulture, "The unicode string cannot have an odd number of digits: {0}", unicodeStr));
            }
            StringBuilder builder = new StringBuilder(unicodeStr.Length/6);

            for (int i = 0; i < unicodeStr.Length; i+=6)
            {
                if(unicodeStr[i]=='\\'&&(unicodeStr[i+1]=='u'|| unicodeStr[i + 1] == 'U'))
                {
                    byte high = (byte)((Parse(unicodeStr[i+2])<<4)| Parse(unicodeStr[i + 3]));
                    byte low= (byte)((Parse(unicodeStr[i + 4]) << 4) | Parse(unicodeStr[i + 5]));
                    ushort value = (ushort)((high << 8) | low);
                    builder.Append((char)value);
                }
            }
            return builder.ToString();
        }
        private static int Parse(char c)
        {
            if (c >= 'a')
                return (c - 'a' + 10) & 0x0f;
            if (c >= 'A')
                return (c - 'A' + 10) & 0x0f;
            return (c - '0') & 0x0f;
        }


        public static byte[] HexToBytes(this string hexString)
        {
            if (hexString.Length % 2 != 0)
            {
                throw new ArgumentException(String.Format(CultureInfo.InvariantCulture, "The binary key cannot have an odd number of digits: {0}", hexString));
            }
            var hexAsBytes = new byte[hexString.Length / 2];
            for (int index = 0; index < hexAsBytes.Length; index++)
                hexAsBytes[index] = (byte)((Parse(hexString[index*2]) << 4) | Parse(hexString[index * 2+1]));
            
            return hexAsBytes;
        }

        //public static byte[] HexToBytes(this string hexString)
        //{
        //	if (hexString.Length % 2 != 0)
        //	{
        //		throw new ArgumentException(String.Format(CultureInfo.InvariantCulture, "The binary key cannot have an odd number of digits: {0}", hexString));
        //	}

        //	var hexAsBytes = new byte[hexString.Length / 2];
        //	for (int index = 0; index < hexAsBytes.Length; index++)
        //	{
        //		string byteValue = "";
        //		byteValue += hexString[index * 2];
        //		byteValue += hexString[index * 2 + 1];
        //		hexAsBytes[index] = byte.Parse(byteValue, NumberStyles.HexNumber, CultureInfo.InvariantCulture);
        //	}
        //	return hexAsBytes;
        //}

        public static string Fmt(this string text, params object[] args)
		{
			return string.Format(text, args);
		}

		public static string ListToString<T>(this List<T> list)
		{
			StringBuilder sb = new StringBuilder();
			foreach (T t in list)
			{
				sb.Append(t);
				sb.Append(",");
			}
			return sb.ToString();
		}

        public static bool IsEmpty(string str)
        {
            return string.IsNullOrEmpty(str);
        }

		public static string MessageToStr(object message)
		{
			return Dumper.DumpAsString(message);
		}
	}
}
```

测试代码：
```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Codingriver;

public class StringHelperTest : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        string str = "哈哈哈哈你们好吗！ hello";
        Debug.Log(str.ToUnicode());
        Debug.Log(str.ToUnicode().FromUnicode());

        Debug.Log(str.ToBytes().ToHex());
        Debug.Log(str.ToUtf8().ToHex());
        Debug.Log(str.ToBytes().ToStr());

    }

}

```

测试结果：
  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/StringHelper编码辅助工具/20200916214430.png)  

>附：  
>
>中文转Unicode在线工具：<http://tool.chinaz.com/tools/unicode.aspx>  
>
>二进制与十六进制在线转换工具：<http://tool.oschina.net/hexconvert>  
>