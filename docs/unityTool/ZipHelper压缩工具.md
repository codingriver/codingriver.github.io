---
title: "ZipHelper压缩工具"
subtitle: "ZipHelper压缩工具"
date: 2020-09-19T18:44:48+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["Unity Tool","Zip压缩工具"]
categories: ["Unity Tool"]
---

<!--more-->

>用C#实现压缩和解压缩的方法，支持Zip压缩解压缩和Gzip压缩解压缩（后缀gz）  

{{< admonition info >}}
使用`ICSharpCode.SharpZipLib.dll`来压缩/解压（压缩效率比GZip要高一点）  
`ICSharpCode.SharpZipLib.dll`下载： <https://github.com/codingriver/tools/tree/master/thirdPlugins>
{{< /admonition >}}


`ZipHelper.cs`文件：

```csharp
using System.IO;
using System.IO.Compression;
using ICSharpCode.SharpZipLib.Zip.Compression;


namespace Codingriver
{
	public static class ZipHelper
	{


        //压缩字节
        //1.创建压缩的数据流 
        //2.设定compressStream为存放被压缩的文件流,并设定为压缩模式
        //3.将需要压缩的字节写到被压缩的文件流
        public static byte[] GZipCompress(byte[] bytes)
        {
            using (MemoryStream compressStream = new MemoryStream())
            {
                using (var zipStream = new GZipStream(compressStream, CompressionMode.Compress))
                    zipStream.Write(bytes, 0, bytes.Length);
                byte[] data= compressStream.ToArray();
                compressStream.Dispose();
                return data;
            }
        }

        //解压缩字节
        //1.创建被压缩的数据流
        //2.创建zipStream对象，并传入解压的文件流
        //3.创建目标流
        //4.zipStream拷贝到目标流
        //5.返回目标流输出字节
        public static byte[] GZipDecompress(byte[] bytes)
        {
            using (var compressStream = new MemoryStream(bytes))
            {
                using (var zipStream = new GZipStream(compressStream, CompressionMode.Decompress))
                {
                    using (var resultStream = new MemoryStream())
                    {
                        zipStream.CopyTo(resultStream);
                        UnityEngine.Debug.Log(resultStream.Capacity);
                        return resultStream.ToArray();
                    }
                }
            }
        }


        /// <summary>
        /// Zip
        /// </summary>
        /// <param name="content"></param>
        /// <returns></returns>
        public static byte[] Compress(byte[] content)
		{
            
            //return content;
            Deflater compressor = new Deflater();
			compressor.SetLevel(Deflater.BEST_COMPRESSION);

			compressor.SetInput(content);
			compressor.Finish();

			using (MemoryStream bos = new MemoryStream(content.Length))
			{
				var buf = new byte[1024];
				while (!compressor.IsFinished)
				{
					int n = compressor.Deflate(buf);
					bos.Write(buf, 0, n);
				}
				return bos.ToArray();
			}
		}

        /// <summary>
        /// Unzip
        /// </summary>
        /// <param name="content"></param>
        /// <returns></returns>
		public static byte[] Decompress(byte[] content)
		{
			return Decompress(content, 0, content.Length);
		}

		public static byte[] Decompress(byte[] content, int offset, int count)
		{
			//return content;
			Inflater decompressor = new Inflater();
			decompressor.SetInput(content, offset, count);

			using (MemoryStream bos = new MemoryStream(content.Length))
			{
				var buf = new byte[1024];
				while (!decompressor.IsFinished)
				{
					int n = decompressor.Inflate(buf);
					bos.Write(buf, 0, n);
				}
				return bos.ToArray();
			}
		}
	}
}

/*
using System.IO;
using System.IO.Compression;

namespace Codingriver
{
	public static class ZipHelper
	{
		public static byte[] Compress(byte[] content)
		{
			using (MemoryStream ms = new MemoryStream())
			using (DeflateStream stream = new DeflateStream(ms, CompressionMode.Compress, true))
			{
				stream.Write(content, 0, content.Length);
				return ms.ToArray();
			}
		}

		public static byte[] Decompress(byte[] content)
		{
			return Decompress(content, 0, content.Length);
		}

		public static byte[] Decompress(byte[] content, int offset, int count)
		{
			using (MemoryStream ms = new MemoryStream())
			using (DeflateStream stream = new DeflateStream(new MemoryStream(content, offset, count), CompressionMode.Decompress, true))
			{
				byte[] buffer = new byte[1024];
				while (true)
				{
					int bytesRead = stream.Read(buffer, 0, 1024);
					if (bytesRead == 0)
					{
						break;
					}
					ms.Write(buffer, 0, bytesRead);
				}
				return ms.ToArray();
			}
		}
	}
}
*/
```