---
title: "【Unity Tool】 ByteHelper字节数组辅助工具"
date: 2020-09-15T18:21:07+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Unity Tool"]
categories: ["Unity Tool"]
---

<!--more-->

>  C# ByteHelper字节数组辅助工具 ,用来处理字节数组序列化及反序列化数据，比如处理网络通信数据，自定义的
> 

`ByteHelper.cs`

```csharp
using System;
using System.Text;
using UnityEngine;

namespace Codingriver
{
    /// <summary>
    /// 字节辅助工具，System.BitConverter;
    ///   这里是大端模式读写的（BitConverter.IsLittleEndian检查大小端）
    ///   特别注意： C# char类型是双字节的！！！
    /// </summary>
	public static class ByteHelper
    {
        public static string ToHex(this byte b)
        {
            return b.ToString("X2");
        }

        public static string ToHex(this byte[] bytes)
        {
            StringBuilder stringBuilder = new StringBuilder();
            foreach (byte b in bytes)
            {
                stringBuilder.Append(b.ToString("X2"));
            }
            return stringBuilder.ToString();
        }

        public static string ToHex(this byte[] bytes, string format)
        {
            StringBuilder stringBuilder = new StringBuilder();
            foreach (byte b in bytes)
            {
                stringBuilder.Append(b.ToString(format));
            }
            return stringBuilder.ToString();
        }

        public static string ToHex(this byte[] bytes, int offset, int count)
        {
            StringBuilder stringBuilder = new StringBuilder();
            for (int i = offset; i < offset + count; ++i)
            {
                stringBuilder.Append(bytes[i].ToString("X2"));
            }
            return stringBuilder.ToString();
        }

        public static string ToStr(this byte[] bytes)
        {
            return Encoding.Default.GetString(bytes);
        }

        public static string ToStr(this byte[] bytes, int index, int count)
        {
            return Encoding.Default.GetString(bytes, index, count);
        }

        public static string Utf8ToStr(this byte[] bytes)
        {
            return Encoding.UTF8.GetString(bytes);
        }

        public static string Utf8ToStr(this byte[] bytes, int index, int count)
        {
            return Encoding.UTF8.GetString(bytes, index, count);
        }
        public static void WriteTo(this byte[] bytes, int offset, ulong num)
        {
            for (int i = 0; i < sizeof(ulong); i++)
                bytes[offset + i] = (byte)(num >> (i * 8) & 0xff);
        }
        public static void ReadTo(this byte[] bytes, int offset, out ulong num)
        {
            num = 0;
            for (int i = sizeof(ulong) - 1; i >= 0; i--)
                num = (num << 8) | bytes[offset + i];
        }

        public static void WriteTo(this byte[] bytes, int offset, long num)
        {
            for (int i = 0; i < sizeof(long); i++)
                bytes[offset + i] = (byte)(num >> (i * 8) & 0xff);
        }
        public static void ReadTo(this byte[] bytes, int offset, out long num)
        {
            num = 0;
            for (int i = sizeof(long) - 1; i >= 0; i--)
                num = (num << 8) | bytes[offset + i];
        }


        public static void WriteTo(this byte[] bytes, int offset, uint num)
        {
            bytes[offset] = (byte)(num & 0xff);
            bytes[offset + 1] = (byte)((num & 0xff00) >> 8);
            bytes[offset + 2] = (byte)((num & 0xff0000) >> 16);
            bytes[offset + 3] = (byte)((num & 0xff000000) >> 24);
        }

        public static void ReadTo(this byte[] bytes, int offset, out uint num)
        {
            num = 0;
            num = bytes[offset + 3];
            num = (uint)((num << 8) | bytes[offset + 2]);
            num = (uint)((num << 8) | bytes[offset + 1]);
            num = (uint)((num << 8) | bytes[offset]);
        }

        public static void WriteTo(this byte[] bytes, int offset, int num)
        {
            bytes[offset] = (byte)(num & 0xff);
            bytes[offset + 1] = (byte)((num & 0xff00) >> 8);
            bytes[offset + 2] = (byte)((num & 0xff0000) >> 16);
            bytes[offset + 3] = (byte)((num & 0xff000000) >> 24);
        }
        public static void ReadTo(this byte[] bytes, int offset, out int num)
        {
            num = 0;
            num = bytes[offset + 3];
            num = (int)((num << 8) | bytes[offset + 2]);
            num = (int)((num << 8) | bytes[offset + 1]);
            num = (int)((num << 8) | bytes[offset]);
        }

        public static void WriteTo(this byte[] bytes, int offset, byte num)
        {
            bytes[offset] = num;
        }

        public static void WriteTo(this byte[] bytes, int offset, short num)
        {
            bytes[offset] = (byte)(num & 0xff);
            bytes[offset + 1] = (byte)((num & 0xff00) >> 8);
        }
        public static void ReadTo(this byte[] bytes, int offset, out short num)
        {
            num = 0;
            num = bytes[offset + 1];
            num = (short)((num << 8) | bytes[offset]);
        }

        public static void WriteTo(this byte[] bytes, int offset, ushort num)
        {
            bytes[offset] = (byte)(num & 0xff);
            bytes[offset + 1] = (byte)((num & 0xff00) >> 8);
        }
        public static void ReadTo(this byte[] bytes, int offset, out ushort num)
        {
            num = 0;
            num = bytes[offset + 1];
            num = (ushort)((num << 8) | bytes[offset]);
        }

        

        public unsafe static void WriteTo(this byte[] bytes, int offset, float num)
        {
            byte* ptr = (byte*)&num;
            for (int i = 0; i < sizeof(float); i++)
                bytes[offset + i] = (byte)(*(ptr + i));
        }
        public unsafe static void ReadTo(this byte[] bytes, int offset, out  float num)
        {
            float tmp = 0;
            byte* ptr = (byte*)&tmp;
            for (int i = sizeof(float) - 1; i >= 0; i--)
                *(ptr + i) = (byte)bytes[offset + i];
            num = tmp;
        }
        public unsafe static void WriteTo(this byte[] bytes, int offset, double num)
        {
            byte* ptr = (byte*)&num;
            for (int i = 0; i < sizeof(double); i++)
                bytes[offset + i] = (byte)(*(ptr + i));
        }
        public unsafe static void ReadTo(this byte[] bytes, int offset, out double num)
        {
            double tmp = 0;
            byte* ptr = (byte*)&tmp;
            for (int i = sizeof(double) - 1; i >= 0; i--)
                *(ptr + i) = (byte)bytes[offset + i];
            num = tmp;
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
using System.IO;
using System;

public class ByteHelperTest : MonoBehaviour
{

    // Start is called before the first frame update
    void Start()
    {
        short a= 32767;
        short aa = -32767;
        ushort b = 65534;
        int c = 2147483647;
        int cc = -2147483648;
        uint d = 4294967295;
        long e = 9223372036854775806;
        long ee = -9223372036854775807;
        ulong f = 18446744073709551613;
        float g = 3.40282347E+38F;
        float gg = -66.98978f;
        double h = 1.7976931348623157E+308;
        double hh = 89898989.34567891d;
        Debug.Log($"{g.ToString("F8")}  , {h.ToString("F8")} , {hh.ToString("F8")}");
        byte[] bts = new byte[1024];

        bts.WriteTo(0, a);
        bts.WriteTo(2, aa);
        bts.WriteTo(4, b);
        bts.WriteTo(6, c);
        bts.WriteTo(10, cc);
        bts.WriteTo(14, d);
        bts.WriteTo(18, e);
        bts.WriteTo(26, ee);
        bts.WriteTo(34, f);
        bts.WriteTo(42, g);
        bts.WriteTo(46, gg);
        bts.WriteTo(50, h);
        bts.WriteTo(58, hh);

        short ta;
        short taa;
        ushort tb;
        int tc;
        int tcc;
        uint td;
        long te;
        long tee;
        ulong tf;
        float tg;
        float tgg;
        double th;
        double thh;
        
        bts.ReadTo(0, out ta);
        bts.ReadTo(2, out taa);
        bts.ReadTo(4, out tb);
        bts.ReadTo(6, out tc);
        bts.ReadTo(10, out tcc);
        bts.ReadTo(14, out td);
        bts.ReadTo(18, out te);
        bts.ReadTo(26, out tee);
        bts.ReadTo(34, out tf);
        bts.ReadTo(42, out tg);
        bts.ReadTo(46, out tgg);
        bts.ReadTo(50, out th);
        bts.ReadTo(58, out thh);

        Debug.Log($"ReadTo---------------->>>>{ta} , {taa} , {tb} , {tc} , {tcc} , {td} , {te} , {tee} , {tf} , {tg.ToString("F8")} , {tgg.ToString("F8")} , {th.ToString("F8")} , {thh.ToString("F8")} ");

        ta = BitConverter.ToInt16(bts, 0);
        taa = BitConverter.ToInt16(bts, 2);
        tb = BitConverter.ToUInt16(bts, 4);
        tc = BitConverter.ToInt32(bts, 6);
        tcc = BitConverter.ToInt32(bts, 10);
        td = BitConverter.ToUInt32(bts, 14);
        te = BitConverter.ToInt64(bts, 18);
        tee = BitConverter.ToInt64(bts, 26);
        tf= BitConverter.ToUInt64(bts, 34);
        tg = BitConverter.ToSingle(bts, 42);
        tgg = BitConverter.ToSingle(bts, 46);
        th = BitConverter.ToDouble(bts, 50);
        thh = BitConverter.ToDouble(bts, 58);



        Debug.Log($"BitConverter ToValue>>>>{ta} , {taa} , {tb} , {tc} , {tcc} , {td} , {te} , {tee} , {tf} , {tg} , {tgg} , {th} , {thh}  ");

        BitConverter.GetBytes(a).ReadTo(0, out ta);
        BitConverter.GetBytes(aa).ReadTo(0, out taa);
        BitConverter.GetBytes(b).ReadTo(0, out tb);
        BitConverter.GetBytes(c).ReadTo(0, out tc);
        BitConverter.GetBytes(cc).ReadTo(0, out tcc);
        BitConverter.GetBytes(d).ReadTo(0, out td);
        BitConverter.GetBytes(e).ReadTo(0, out te);
        BitConverter.GetBytes(ee).ReadTo(0, out tee);
        BitConverter.GetBytes(f).ReadTo(0, out tf);
        BitConverter.GetBytes(g).ReadTo(0, out tg);
        BitConverter.GetBytes(gg).ReadTo(0, out tgg);
        BitConverter.GetBytes(h).ReadTo(0, out th);
        BitConverter.GetBytes(hh).ReadTo(0, out thh);

        Debug.Log($"BitConverter ToBytes>>>>  {ta} , {taa} , {tb} , {tc} , {tcc} , {td} , {te} , {tee} , {tf} , {tg} , {tgg} , {th} , {thh}  ");

    }
}

```


测试结果：
  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/ByteHelper字节数组辅助工具/20200915182212.png)  
  
![](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/ByteHelper字节数组辅助工具/20200915182231.png)  

![20200915194718](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/ByteHelper字节数组辅助工具/20200915194718.png)