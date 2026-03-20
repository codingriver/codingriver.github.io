---
title: "MD5计算工具"
subtitle: "C#实现md5计算工具"
date: 2020-09-19T18:45:30+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Unity Tool","md5工具"]
categories: ["Unity Tool"]
---

<!--more-->

>用C#实现md5计算，获取十六进制md5

`MD5Helper.cs`文件：

```csharp
using System.IO;
using System.Security.Cryptography;

namespace Codingriver
{
	public static class MD5Helper
	{
        /// <summary>
        /// 计算文件的md5
        /// </summary>
        /// <param name="fileName"></param>
        /// <returns></returns>
        public static string CalculateMD5File(string fileName)
        {
            string md5Str = null;
            if (File.Exists(fileName))
            {

                using (FileStream fs = new FileStream(fileName, FileMode.Open, FileAccess.Read))
                {
                    MD5 md5 = new MD5CryptoServiceProvider();
                    byte[] bts = md5.ComputeHash(fs);
                    md5Str = bts.ToHex();
                }
            }

            return md5Str;
        }
        /// <summary>
        /// 计算字符串的md5
        /// </summary>
        /// <param name="text"></param>
        /// <returns></returns>
        public static string CalculateMD5(string text)
        {

            MemoryStream stream = new MemoryStream();
            StreamWriter sw = new StreamWriter(stream);
            sw.Write(text);
            sw.Flush();
            return CalculateMD5(stream);
        }

        public static string CalculateMD5(Stream stream)
        {
            string md5Str = null;
            if (stream != null)
            {
                stream.Position = 0;
                MD5 md5 = new MD5CryptoServiceProvider();
                byte[] bts = md5.ComputeHash(stream);
                md5Str = bts.ToHex();

            }
            return md5Str;
        }
        public static string CalculateMD5(byte[] data)
        {
            string md5Str = null;
            if (data != null)
            {
                MD5 md5 = new MD5CryptoServiceProvider();
                byte[] bts = md5.ComputeHash(data);
                md5Str = bts.ToHex();

            }
            return md5Str;
        }
        public static string CalculateMD5(byte[] data, int offset, int count)
        {
            string md5Str = null;
            if (data != null)
            {
                MD5 md5 = new MD5CryptoServiceProvider();
                byte[] bts = md5.ComputeHash(data, offset, count);
                md5Str = bts.ToHex();

            }
            return md5Str;
        }

    }
}

```