---
title: "socket测试结果"
date: 2019-12-01T21:57:40+08:00
draft: true
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: [""]
categories: [""]
---

<!--more-->

socket测试结果(基于发送和接收缓冲区没有缓存的情况下测试，有缓存也一样)
SocketOptionName.Linger=false 且没有异步或同步监听接受接口，close 后发送Fin包(close没有延时)（LingerState参数无影响）
SocketOptionName.Linger=false 且有异步或同步监听接受接口，close 后发送Rst包(close没有延时)（LingerState参数无影响）（socket的都关闭了还接收数据肯定错误）

SocketOptionName.Linger=false 且没有异步或同步监听接受接口，close 后发送Fin包(close延时1秒)
SocketOptionName.Linger=false 且有异步或同步监听接受接口，close 后发送Fin包(close延时1秒)

SocketOptionName.Linger=true 且没有异步或同步监听接受接口，close 后发送Rst包(close没有延时)
SocketOptionName.Linger=true 且有异步或同步监听接受接口，close 后发送Rst包(close没有延时)

SocketOptionName.Linger=true 且没有异步或同步监听接受接口，close 后发送Fin包(close延时1秒)
SocketOptionName.Linger=true 且有异步或同步监听接受接口，close 后发送Fin包(close延时1秒)


Socket.Shutdown(SocketShutdown.Receive); 只是通知内核缓冲区接收消息的流，我不收数据了，不给对端任何消息。
直到对端发消息过来后才给对端发送Rst包告诉他网络重置（出错了）。 （自己这个时候在发送数据提示shutdown错误）
Socket.Shutdown(SocketShutdown.Send)只是关闭了内核缓冲区发送消息的流 给对端发送Fin包 受到ack包后会受到0字节长度的消息。
（对端收到0长度消息后如果继续Receive消息：内核自己会给用户态返回0长度消息）
shutdown 只是关闭网络连接 并没有关闭socket文件描述符，所以还得用close（）关闭文件描述符



大端小端
如果自己设置RecvBuffSize=0 网卡接收数据会另外开辟一块缓冲区存放数据直到用户态调用Receive返回给用户

jit(动态编译)和aot（静态编译）