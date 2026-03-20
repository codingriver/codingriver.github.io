
---
title: "Xlua-线程问题"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: []
categories: ["other"]
---

<!--more-->


网络socket接收数据的异步回调不可以直接调入lua，在数据非常大的情况下如6321字节，在lua中解包，会出现线程同步的bug，
所以必须在unity的Update中转入主线程调用lua
