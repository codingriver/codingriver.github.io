---
title: "golang笔记"
date: "2022-03-06"
tags:
  - 随笔
  - 笔记
  - UI
  - 网络
  - 工具链
categories:
  - ANote
comments: true
---
# golang笔记

## 安装
mac 安装
```sh
brew update
brew install go
```
>参考: [centos 7 安装golang1.17](https://www.cnblogs.com/nickchou/p/13252545.html)


## 设置代理环境变量
设置代理环境变量，再拉去golang.org的时候就不需要墙了。注意GO1.13及之后支持direct的写法
```
go env -w GOPROXY=https://goproxy.cn,direct
```

## 问题

#### [GO在Visual Studio Code初次运行时提示go: go.mod file not found in current directory or any parent directory; see 'go help modules'](https://www.cnblogs.com/cela/p/go_go_1_S1.html)

 新建项目后需要在项目根目录执行
 ```sh
 go mod init {项目名}
 ```

 #### [[Go] 解决missing go.sum entry for module providing package <package_name>](https://blog.csdn.net/taoshihan/article/details/116514102)

 当在代码中使用了第三方库 ，但是go.mod中并没有跟着更新的时候

如果直接run或者build就会报这个错误

missing go.sum entry for module providing package <package_name>

可以使用go mod tidy 来整理依赖

这个命令会：

删除不需要的依赖包

下载新的依赖包

更新go.sum
