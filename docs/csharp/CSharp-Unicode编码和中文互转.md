# C#-Unicode编码和中文互转

## 直接上代码

```csharp
using System;
using System.Text;

/// <summary>
/// Unicode 编码和中文互转
/// 这里的 Unicode 编码是 Unicode Big Endian (UCS-2 Big Endian)
/// </summary>
class UnicodeTools
{
    public static string EncodeString(string text)
    {
        if (string.IsNullOrEmpty(text))
        {
            return string.Empty;
        }
        int len = text.Length;
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < len; i++)
        {
            builder.Append("\\u");
            builder.Append(UShortToHex((ushort)text[i]));
        }
        return builder.ToString();
    }

    public static string EncodeString1(string text)
    {
        if (string.IsNullOrEmpty(text))
        {
            return string.Empty;
        }
        var bytes = Encoding.Unicode.GetBytes(text);
        int len = bytes.Length;
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < len; i += 2)
        {
            builder.Append("\\u");
            builder.Append(bytes[i + 1].ToString("x2"));
            builder.Append(bytes[i].ToString("x2"));
        }
        return builder.ToString();
    }

    public static string EncodeString2(string text)
    {
        if (string.IsNullOrEmpty(text))
        {
            return string.Empty;
        }
        int len = text.Length;
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < len; i++)
        {
            builder.Append("\\u");
            builder.Append(((ushort)text[i]).ToString("x4"));
        }
        return builder.ToString();
    }

    private static char[] UShortToHex(ushort n)
    {
        int num;
        char[] hex = new char[4];
        for (int i = 0; i < 4; i++)
        {
            num = n % 16;
            if (num < 10)
                hex[3 - i] = (char)('0' + num);
            else
                hex[3 - i] = (char)('A' + (num - 10));
            n >>= 4;
        }
        return hex;
    }

    public static string DecodeString(string unicode)
    {
        if (string.IsNullOrEmpty(unicode))
        {
            return string.Empty;
        }
        string[] ls = unicode.Split(new string[] { "\\u" }, StringSplitOptions.RemoveEmptyEntries);
        StringBuilder builder = new StringBuilder();
        int len = ls.Length;
        for (int i = 0; i < len; i++)
        {
            builder.Append(Convert.ToChar(ushort.Parse(ls[i], System.Globalization.NumberStyles.HexNumber)));
        }
        return builder.ToString();
    }

    public static string DecodeString1(string unicode)
    {
        if (string.IsNullOrEmpty(unicode))
        {
            return string.Empty;
        }
        return System.Text.RegularExpressions.Regex.Unescape(unicode);
    }
}
```

## 测试

```csharp
string s = "天空测试s";
Console.WriteLine(UnicodeTools.EncodeString(s));
Console.WriteLine(UnicodeTools.EncodeString1(s));
Console.WriteLine(UnicodeTools.EncodeString2(s));
Console.WriteLine(UnicodeTools.DecodeString(UnicodeTools.EncodeString(s)));
Console.WriteLine(UnicodeTools.DecodeString(UnicodeTools.EncodeString1(s)));
Console.WriteLine(UnicodeTools.DecodeString(UnicodeTools.EncodeString2(s)));
Console.WriteLine(UnicodeTools.DecodeString1(UnicodeTools.EncodeString(s)));
Console.WriteLine(UnicodeTools.DecodeString1(UnicodeTools.EncodeString1(s)));
Console.WriteLine(UnicodeTools.DecodeString1(UnicodeTools.EncodeString2(s)));
```

## 结果

![结果.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-0b66f358f0fa5f41.png)
