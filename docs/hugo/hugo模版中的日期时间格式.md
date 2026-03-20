---
title: "hugo / go 模版中的日期格式"
date: 2020-09-01T21:08:09+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ['hugo']
categories: ['hugo']
toc: false
---

<!--more-->

>  我们怎么设置日期都和想要的不一样，怎么解决呢?

**这里的时间格式用的时间点是固定的，找到这个规律就好了，也就是： `2006-01-02 15:04:05`**

```toml
dateFormat = "2006-01-02 15:04:05"
```
这样就能解决了

> *日期时间格式可能是每一个 go 程序员都遇到过的问题，但是对于一个 hugo 使用者来说， 未免不太友好，如果你正在为这个问题烦恼，希望本文会对你有所帮助。*
>
> 参考：[hugo / go 模版中的日期格式](https://tricks.one/post/date-format-in-hugo-or-go-templates/)



