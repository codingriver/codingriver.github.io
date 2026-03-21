---
title: "Xlua-线程问题"
date: "2026-03-21"
tags:
  - 工具链
  - 异步编程
  - 网络
  - Lua
categories:
  - other
comments: true
---
# Xlua-线程问题

网络socket接收数据的异步回调不可以直接调入lua，在数据非常大的情况下如6321字节，在lua中解包，会出现线程同步的bug，
所以必须在unity的Update中转入主线程调用lua
