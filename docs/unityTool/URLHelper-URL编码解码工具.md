---
title: "URLHelper URL编码解码工具"
subtitle: "escape,encodeURI和encodeURIComponent实现对URL编码解码"
date: 2020-09-17T20:47:11+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Unity Tool","Unicode编码","URL编码解码","encodeURI"]
categories: ["Unity Tool"]
toc: false
---

<!--more-->
>C#实现URL编码解码
> URL编码解码原理参考 [URL编码与解码原理]({{<ref "URL编码与解码原理.md" >}})

`URLHelper`实现URL编码和URL解码 ( *这些解码编码不支持`空格`和字符`+`转换* ) ：
- `Escape` 和 `Unescape`
- `EncodeURI` 和 `DecodeURI`
- `EncodeURIComponent` 和 `DecodeURIComponent`
  
还有 `UrlEncode`和`UrlDecode`方法支持支持`空格`和字符`+`转换


###### `URLHelper.cs`代码:point_down::point_down::point_down:

```csharp
using System;
using System.Collections.Generic;
using System.Net;
using System.Text;
using System.Web;

namespace Codingriver
{
    public static class URLHelper
    {

        /// <summary>
        /// URL编码（不支持空格和字符+转换）
        /// 使用UTF-16
        /// </summary>
        /// <param name="url"></param>
        /// <param name="encoding"></param>
        /// <returns></returns>
        public static string Escape(string url)
        {
            StringBuilder builder = new StringBuilder(url.Length * 2);
            for (int i = 0; i < url.Length; i++)
            {
                char c = url[i];
                ushort value = url[i];
                if (c >= '0' && c <= '9' || c >= 'A' && c <= 'Z' || c >= 'a' && c <= 'z')
                {
                    builder.Append(c);
                    continue;
                }
                switch (c)
                {
                    case '*':
                    case '/':
                    case '@':
                    case '+':
                    case '-':
                    case '.':
                    case '_':
                        builder.Append(c);
                        continue;
                    default:
                        break;
                }
                if(value<= 255)
                {
                    builder.AppendFormat("%{0:X2}",value);
                }
                else
                {
                    builder.AppendFormat("%u{0:X2}{1:X2}", (value & 0xFF00)>>8, value & 0xFF);
                }
            }

            return builder.ToString();
        }
        /// <summary>
        /// URL解码（不支持空格和字符+转换）
        /// 使用UTF-16
        /// </summary>
        /// <param name="escapeUrl"></param>
        /// <returns></returns>
        public static string Unescape(string escapeUrl)
        {
            StringBuilder builder = new StringBuilder(escapeUrl.Length);
            int index = 0;
            int len = escapeUrl.Length;

            while (index < len)
            {
                if (escapeUrl[index] != '%')
                {
                    builder.Append(escapeUrl[index]);
                    index++;
                    continue;
                }
                else if (escapeUrl[index+1] == 'u')
                {
                    // unicode
                    if (index + 5 >= len)
                    {
                        throw new Exception("error url not match");
                    }
                    ushort value = 0;
                    int high = ByteHelper.Parse(escapeUrl[index + 2]);
                    int low = ByteHelper.Parse(escapeUrl[index + 3]);
                    value = (byte)((high << 4) | low);
                    high = ByteHelper.Parse(escapeUrl[index + 4]);
                    low = ByteHelper.Parse(escapeUrl[index + 5]);
                    value = (ushort)((value<<8) |((high << 4) | low));
                    builder.Append((char)value);
                    index = index + 6;
                }
                else
                {
                    // ascii
                    if (index + 2 >= len)
                    {
                        throw new Exception("error url not match");
                    }
                    ushort value = 0;
                    int high = ByteHelper.Parse(escapeUrl[index + 1]);
                    int low = ByteHelper.Parse(escapeUrl[index + 2]);
                    value = (byte)((high << 4) | low);
                    builder.Append((char)value);
                    index = index + 3;
                }

            }

            return builder.ToString();
        }

        /// <summary>
        /// URL编码（支持空格和字符+转换）
        /// 使用UTF-16
        /// </summary>
        /// <param name="str"></param>
        /// <param name="encoding"></param>
        /// <returns></returns>
        public static string UrlEncode(string str, Encoding encoding = null)
        {
            if (encoding == null)
                return HttpUtility.UrlEncode(str);
            else
                return HttpUtility.UrlEncode(str, encoding);
        }
        /// <summary>
        /// URL解码（支持空格和字符+转换）
        /// 使用UTF-16
        /// </summary>
        /// <param name="str"></param>
        /// <param name="encoding"></param>
        /// <returns></returns>
        public static string UrlDecode(string str, Encoding encoding = null)
        {
            if (encoding == null)
                return HttpUtility.UrlDecode(str);
            else
                return HttpUtility.UrlDecode(str, encoding);
        }

        /// <summary>
        /// URL编码（不支持空格和字符+转换）
        /// </summary>
        /// <param name="url"></param>
        /// <param name="encoding">默认使用UTF-8</param>
        /// <returns></returns>
        public static string EncodeURI(string url, Encoding encoding = null)
        {
            if (encoding == null)
            {
                encoding = Encoding.UTF8;
            }
            StringBuilder builder = new StringBuilder(url.Length * 2);
            char[] cArr = new char[1];
            for (int i = 0; i < url.Length; i++)
            {
                char c = url[i];
                ushort value = url[i];
                if (c >= '0' && c <= '9' || c >= 'A' && c <= 'Z' || c >= 'a' && c <= 'z')
                {
                    builder.Append(c);
                    continue;
                }
                switch (c)
                {
                    case '!':
                    case '#':
                    case '$':
                    case '&':
                    case '\'':
                    case '(':
                    case ')':
                    case '*':
                    case '+':
                    case ',':
                    case '/':
                    case ':':
                    case ';':
                    case '=':
                    case '?':
                    case '@':
                    case '-':
                    case '.':
                    case '_':
                    case '~':
                    case '"':
                        builder.Append(c);
                        continue;
                    default:
                        break;
                }
                cArr[0] = c;
                byte[] bts = encoding.GetBytes(cArr);
                for (int j = 0; j < bts.Length; j++)
                {
                    builder.AppendFormat("%{0:X2}", bts[j]);
                }
            }

            return builder.ToString();
        }

        /// <summary>
        /// URL解码（不支持空格和字符+转换）
        /// 
        /// </summary>
        /// <param name="encodeUrl"></param>
        /// <param name="encoding">默认使用UTF-8</param>
        /// <returns></returns>
        public static string DecodeURI(string encodeUrl, Encoding encoding = null)
        {
            if (encoding == null)
            {
                encoding = Encoding.UTF8;
            }
            StringBuilder builder = new StringBuilder(encodeUrl.Length);
            int index = 0;
            int len = encodeUrl.Length;
            List<byte> bytes = new List<byte>(128);

            while (index < len)
            {
                if (encodeUrl[index] == '%')
                {
                    if (index + 2 >= len)
                    {
                        throw new Exception("error url not match");
                    }
                    int high = ByteHelper.Parse(encodeUrl[index + 1]);
                    int low = ByteHelper.Parse(encodeUrl[index + 2]);
                    byte value = (byte)((high << 4) | low);
                    bytes.Add(value);
                    index = index + 3;
                }
                else
                {
                    if (bytes.Count > 0)
                    {
                        builder.Append(encoding.GetString(bytes.ToArray()));
                        bytes.Clear();
                    }
                    builder.Append(encodeUrl[index]);
                    index++;
                    continue;
                }

            }
            if (bytes.Count > 0)
            {
                builder.Append(encoding.GetString(bytes.ToArray()));
                bytes.Clear();
            }

            return builder.ToString();
        }


        /// <summary>
        /// URL编码（不支持空格和字符+转换）
        /// </summary>
        /// <param name="url"></param>
        /// <param name="encoding">默认使用UTF-8</param>
        /// <returns></returns>
        public static string EncodeURIComponent(string url, Encoding encoding = null)
        {
            if (encoding == null)
            {
                encoding = Encoding.UTF8;
            }
            StringBuilder builder = new StringBuilder(url.Length * 2);
            char[] cArr = new char[1];
            for (int i = 0; i < url.Length; i++)
            {
                char c = url[i];
                ushort value = url[i];
                if (c >= '0' && c <= '9' || c >= 'A' && c <= 'Z' || c >= 'a' && c <= 'z')
                {
                    builder.Append(c);
                    continue;
                }
                switch (c)
                {
                    case '!':
                    case '\'':
                    case '(':
                    case ')':
                    case '*':
                    case '-':
                    case '.':
                    case '_':
                    case '~':
                        builder.Append(c);
                        continue;
                    default:
                        break;
                }
                cArr[0] = c;
                byte[] bts = encoding.GetBytes(cArr);
                for (int j = 0; j < bts.Length; j++)
                {
                    builder.AppendFormat("%{0:X2}", bts[j]);
                }
            }

            return builder.ToString();
        }

        /// <summary>
        /// URL解码（不支持空格和字符+转换）
        /// </summary>
        /// <param name="encodeUrl"></param>
        /// <param name="encoding">默认使用UTF-8</param>
        /// <returns></returns>
        public static string DecodeURIComponent(string encodeUrl, Encoding encoding = null)
        {
            return DecodeURI(encodeUrl, encoding);
        }
    }
}

```

测试代码：
```
using System;
using UnityEngine;
using Codingriver;
using System.Text;

public class URLHelperTest : MonoBehaviour
{
    private void OnEnable()
    {
        string url = "h://+w.b+b d. m:9 0 0/o/t/i.a? key=你好吗？#&好鸭好鸭 ！! ，#，$，&，'，(，)，*，+，,，-，.，/，:，;，=，?，@，_，~，#";
        //string url = "http://www.baidu.com/ s?ie=utf-8&f=8&tn=baidu&wd=临时邮箱";


        Debug.Log(url);
        Debug.Log("UrlEncode:" + URLHelper.UrlEncode(url, encoding: Encoding.UTF8));
        Debug.Log("UrlDecode:"+URLHelper.UrlDecode(URLHelper.EncodeURI(url), Encoding.UTF8));
        Debug.Log("EncodeURI:"+URLHelper.EncodeURI(url));
        Debug.Log("DecodeURI:"+URLHelper.DecodeURI("h://+w.b+b%20d.%20m:9%200%200/o/t/i.a?%20key=%E4%BD%A0%E5%A5%BD%E5%90%97%EF%BC%9F#&%E5%A5%BD%E9%B8%AD%E5%A5%BD%E9%B8%AD%20%EF%BC%81!%20%EF%BC%8C#%EF%BC%8C$%EF%BC%8C&%EF%BC%8C'%EF%BC%8C(%EF%BC%8C)%EF%BC%8C*%EF%BC%8C+%EF%BC%8C,%EF%BC%8C-%EF%BC%8C.%EF%BC%8C/%EF%BC%8C:%EF%BC%8C;%EF%BC%8C=%EF%BC%8C?%EF%BC%8C@%EF%BC%8C_%EF%BC%8C~%EF%BC%8C#"));
        Debug.Log("EncodeURIComponent:" + URLHelper.EncodeURIComponent(url));
        Debug.Log("DecodeURIComponent:" + URLHelper.DecodeURIComponent(URLHelper.EncodeURIComponent(url)));
        Debug.Log("Escape:"+URLHelper.Escape(url));
        Debug.Log("Unescape:" + URLHelper.Unescape("h%3A//+w.b+b%20d.%20m%3A9%200%200/o/t/i.a%3F%20key%3D%u4F60%u597D%u5417%uFF1F%23%26%u597D%u9E2D%u597D%u9E2D%20%uFF01%21%20%uFF0C%23%uFF0C%24%uFF0C%26%uFF0C%27%uFF0C%28%uFF0C%29%uFF0C*%uFF0C+%uFF0C%2C%uFF0C-%uFF0C.%uFF0C/%uFF0C%3A%uFF0C%3B%uFF0C%3D%uFF0C%3F%uFF0C@%uFF0C_%uFF0C%7E%uFF0C%23"));
        Debug.Log("Unescape:"+URLHelper.Unescape(URLHelper.Escape(url)));


    }

}


```

测试结果：

![20200917205639](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/URLHelper-URL编码解码工具/20200917205639.png)