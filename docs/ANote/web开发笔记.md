---
title: "web开发笔记"
date: "2026-03-21"
tags:
  - 随笔
  - 笔记
  - 网络
  - iOS
  - 项目记录
categories:
  - ANote
comments: true
---
# web开发笔记.md

### 常用header说明

```
请求网址: http://10.24.0.24:8889/executeCmd
请求方法: POST
状态代码: 200 
远程地址: 10.24.0.24:8889
引荐来源网址政策: strict-origin-when-cross-origin

响应Header(response headers)
Connection: keep-alive
Content-Length: 6
Content-Type: text/html;charset=utf-8
Date: Wed, 30 Mar 2022 08:22:51 GMT
Keep-Alive: timeout=60

请求Header(request header)
Accept: */*
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: keep-alive
Content-Length: 56
Content-Type: application/json
Host: 10.24.0.24:8889
Origin: http://10.24.0.24:8889
Referer: http://10.24.0.24:8889/cmd
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36
X-Requested-With: XMLHttpRequest
```

#### request header


>Accept-Language: 支持的语言类型，类似于一个数组，每种语言对应一个权重(0-1的数字)，一般用来做多语言用

>Content-Type: 请求体的类型  
*设置响应内容的类型和编码, 经常配合mime模块使用*
```c
// 常用几种类型

application/x-www-form-urlencoded  // a=1&b=2
application/json // {"a": "1", "b": "2"}
multipart/form-data //文件类型

application/x-www-form-urlencoded;charset=utf-8
```


>Referer: 资源在哪个网站中被使用，来源。可篡改，重要的东西不可依赖于他

>Accept-Encoding: 浏览器支持的格式

>Origin: 当前网站的来源，只支持post请求

>Cookie: 每次发请求，都会带到服务端

>If-Modified-Since: 缓存相关，详见下文的 Last-Modified

>If-None-Match: 缓存相关，详见下文的 Etag

>Range: Range:bytes=n-m, 请求内容的第n 到m 的字节

```
服务端设置res.setHeader('Content-Range', 'bytes n-m/total'),
并设置状态码res.statusCode = 206
```

#### response header
>Content-Type: 设置响应内容的类型和编码, 经常配合mime模块使用
```
res.setHeader('Content-Type', mime.getType(req.url) + ';charset=utf-8' )
```

>Cache-Control: 强制缓存，设置缓存有效时长(比expires靠谱)
```
res.setHeader('Cache-Control', 'no-cache') //不设置强制缓存
res.setHeader('Cache-Control', 'max-age=3600') //强制缓存1小时, 单位：秒
```
>Expires: 强制缓存 单位：毫秒，设置缓存失效的一个时间点
```
res.setHeader('Expires', new Date( Date.now() + 3600 * 1000 ).toLocaleString()) 
```
>Last-Modified: 上次修改时间

```c
// 通过fs.stat 拿到 statRes, 拿到上次修改的时间
// 设置给Last-Modified, 浏览器下次访问这个文件时候
// 会带上一个头If-Modified-Since, 取出值old
// 再次通过fs.stat获取修改时间，和old进行比较
// 若相同，则设置304，并end，否则重新设置Last-Modified并重新返回文件
res.setHeader('Last-Modified', statRes.ctime.toGMTString())
```
>Etag: 存放根据文件内容计算出的价签字符串

```
// sign的计算可以根据实际情况来定，可以用md5文件内容加签得到一个值，
// 常用的是文件内容的 修改时间的16进制+内容长度的16进制值，
// 也可以通过其他算法， 得到一个不规则字符串，
// 设置到Etag以后，浏览器下次访问这个文件,会带上一个头If-None-Match
// 取到值old以后，重新根据文件内容用相同算法计算一个sign，和old比较，
// 若相同，则设置304，并end，否则重新设置Etag并重新返回文件
res.setHeader('Etag', sign);

```

**3种缓存可以同时使用， Last-Modified和Etag是并且关系，有一个没对上，就重新发送文件**

>Content-Range: 返回部分内容，和响应头Range配合使用

>Content-Length: 响应内容的字节长度

>Access-Control-Allow-Origin: 允许哪个源来访问
```
可以设置成 *(所有网站) ，也可以设置一个白名单，当当前访问的域名在白名单中，
就设置成当前访问的域名
```
>Access-Control-Allow-Methods: 允许哪些方法访问,GET,POST,PUT,DELETE。。。

>Access-Control-Allow-Credentials:是否可携带cookie  
>需要前端ajax也设置xhr.withCredentials = true;

>Content-Encoding: 告诉浏览器，按照那种方式解析文件



