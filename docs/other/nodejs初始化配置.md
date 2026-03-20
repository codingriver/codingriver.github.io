---
title: "Nodejs初始化配置"
subtitle: "Nodejs初始化配置"
date: 2024-03-14T17:54:47+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
draft: true
tags: []
categories: []
---

<!--more-->
>转载：[windows安装npm教程](https://www.cnblogs.com/liluxiang/p/9592003.html)

[windows下npm安装vue](https://www.cnblogs.com/liluxiang/p/9592003.html)
====================================================================

一、使用之前，我们先来掌握3个东西是用来干什么的。
-------------------------

npm: Nodejs下的包管理器。
------------------

webpack: 它主要的用途是通过CommonJS的语法把所有浏览器端需要发布的静态资源做相应的准备，比如资源的合并和打包。
---------------------------------------------------------------

vue-cli: 用户生成Vue工程模板。（帮你快速开始一个vue的项目，也就是给你一套vue的结构，包含基础的依赖库，只需要 npm install就可以安装）
---------------------------------------------------------------------------------

开始：
---

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212145017816-1078102167.png)

### 如图，下载8.9.3 LTS （推荐给绝大部分用户使用）

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212145228394-1659342805.png)

### 双击安装

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212145307316-1352109111.png)

### 可以使用默认路径，本例子中自行修改为d:\\nodejs

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212145332816-1106051339.png)

### 一路点Next

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212145443082-1633079415.png)

### 点Finish完成

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212145526363-1294346495.png)

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212145534144-1685678132.png)

### 打开CMD，检查是否正常

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212145657082-1826714804.png)

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212145723801-1548672252.png)

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212145740222-1613793922.png)

### 再看看另外2个目录，npm的本地仓库跑在系统盘c盘的用户目录了(没见到npm-cache是因为没有用过，一使用缓存目录就生成了)，我们试图把这2个目录移动回到D:\\nodejs

### 先如下图建立2个目录

###  ![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212145811019-407092018.png)

### 然后运行以下2条命令

### npm config set prefix "D:\\nodejs\\node\_global"

### npm config set cache "D:\\nodejs\\node\_cache"

### ![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212145854347-808420142.png)

### 如上图，我们再来关注一下npm的本地仓库，输入命令npm list -global

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212145924051-372279137.png)

### 输入命令npm config set registry=http://registry.npm.taobao.org 配置镜像站

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212145956347-1443850138.png)

### 输入命令npm config list 显示所有配置信息，我们关注一个配置文件

### C:\\Users\\Administrator\\.npmrc

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212150036551-2051372473.png)

### 使用文本编辑器编辑它，可以看到刚才的配置信息

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212150059472-912062155.png)

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212150115488-275634578.png)

### 检查一下镜像站行不行命令1

### npm config get registry

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212150211879-638610714.png)

### 检查一下镜像站行不行命令2

### Npm info vue 看看能否获得vue的信息

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212150233535-577937828.png)

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212150246691-739368557.png)

### 注意，此时，默认的模块D:\\nodejs\\node\_modules 目录

### 将会改变为D:\\nodejs\\node\_global\\node\_modules 目录，

### 如果直接运行npm install等命令会报错的。

### 我们需要做1件事情：

### 1、增加环境变量NODE\_PATH 内容是：D:\\nodejs\\node\_global\\node\_modules

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212150402894-2086448836.png)

### （注意，一下操作需要重新打开CMD让上面的环境变量生效）

### 一、测试NPM安装vue.js

### 命令：npm install vue -g

### 这里的-g是指安装到global全局目录去

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212150420488-1331978539.png)

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212150458519-2132301252.png)

### 二、测试NPM安装vue-router

### 命令：npm install vue-router -g

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212150538707-640998672.png)

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212150544879-938347487.png)

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212150744051-1058132537.png)

### 运行npm install vue-cli -g安装vue脚手架

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212150805238-349743368.png)

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212150836707-1925918113.png)

### 编辑环境编辑path

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212150853863-1117215657.png)

### 对path环境变量添加D:\\nodejs\\node\_global

### win10以下版本的，横向显示PATH的，注意添加到最后时，不要有分号【;】

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212150928332-1178968243.png)

### 重新打开CMD，并且测试vue是否使用正常

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212150949097-1600189468.png)

### 注意，vue-cli工具是内置了模板包括 webpack 和 webpack-simple,前者是比较复杂专业的项目，

### 他的配置并不全放在根目录下的 webpack.config.js 中。

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212151033847-2077318030.png)

### 初始化，安装依赖

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212151121910-1710109810.png)

### 运行npm install安装依赖

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212151139176-1075396617.png)

### npm run dev

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212151206519-436420011.png)

### 成功界面，提示打开地址http://localhost:8080

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212151256129-333658407.png)

### 自动打开浏览器http://localhost:8080/#/

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212151314504-1422396943.png)

### npm run build

### 生成静态文件，打开dist文件夹下新生成的index.html文件

### nmp下新建出来的vue01的目录描述：

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212151528301-530076803.png)

懂的越多，不会的也就越多，知识之路是不断进取的


---
<!---
>转载：[windows安装npm教程](https://blog.csdn.net/zhouyan8603/article/details/109039732)


#### 在使用之前，先类掌握3个东西，明白它们是用来干什么的：

**npm:  nodejs 下的包管理器。**

**webpack: 它主要用途是通过CommonJS 的语法把所有浏览器端需要发布的静态资源作相应的准备，比如资源的合并和打包。**

**vue-cli: 用户生成Vue工程模板。（帮你快速开始一个vue的项目，也就是给你一套vue的结构，包含基础的依赖库，只需要npm install 就可以安装。**

#### 2、nodejs下载网址：[https://nodejs.org/en/](https://nodejs.org/en/)     【如果嫌下载的慢，可以下载其他网站上的，别人有现成的，下载的比较快】

![](https://img-blog.csdnimg.cn/img_convert/2122db339ad4c282c01e0a4c9b842b84.png)

####  3、下载好后，双击安装：

![](https://img-blog.csdnimg.cn/img_convert/787070181d4eb6354442b627b349d00a.png)

####  4、默认，下一步：

![](https://img-blog.csdnimg.cn/img_convert/b40ce42d6a962b73376ade7d717ea3d0.png)

####  5、接受协议：

![](https://img-blog.csdnimg.cn/img_convert/12461a83230969a4b8664295fa610716.png)

####  6、选择安装路径：

![](https://img-blog.csdnimg.cn/img_convert/180628a64010aee2bc96647596a79d83.png)

####  7、会默认自己添加环境变量：

![](https://img-blog.csdnimg.cn/img_convert/3ee3761f8088d44e72a9d8f6c46ae143.png)

####  8、接下去一路“next”，最后点击finish

![](https://img-blog.csdnimg.cn/img_convert/48ab1caa2f04c9ac15eaf8ffb33b1b38.png)

####  9、安装好后，对应的各个文件的作用：

![](https://img-blog.csdnimg.cn/img_convert/775ce05db690c99c6b8b213227b0cd89.png)

####  10、cmd打开终端：

![](https://img-blog.csdnimg.cn/img_convert/b0ea3721f682845f92536af72810213e.png)

####  11、检查是否正常

![](https://img-blog.csdnimg.cn/img_convert/23a6f91b01a20c3626bff643920570ce.png)

![](https://img-blog.csdnimg.cn/img_convert/afdbfef7b39d19c767eb66f5dbcf95db.png)

####  12、再看看另外2个目录，npm的本地仓库跑在系统盘c盘的用户目录了(没见到npm-cache是因为没有用过，

#### 一使用缓存目录就生成了)，我们试图把这2个目录移动回到D:\\nodejs

![](https://img-blog.csdnimg.cn/img_convert/9dc6663392f9d03b969bff2175468600.png)

#### 先如下图建立2个目录：

![](https://img-blog.csdnimg.cn/img_convert/bea0426031debd0f385132b017526465.png)

####  13、然后运行以下2条命令

#### npm config set prefix "D:\\nodejs\\node\_global"

#### npm config set cache "D:\\nodejs\\node\_cache"

 ![](https://img-blog.csdnimg.cn/img_convert/c8e9d031ccdb2314e8adc3b0098bfad5.png)

如上图，我们再来关注一下npm的本地仓库，输入命令npm list -global

#### 14、配置一个镜像站，为了提升速度，

#### 输入命令npm config set registry=http://registry.npm.taobao.org 配置镜像站

![](https://img-blog.csdnimg.cn/img_convert/2e6d19ebf5be093e10ebd45a436aa901.png)

**输入命令npm config list 显示所有配置信息，我们关注一个配置文件**

**C:\\Users\\Administrator\\.npmrc**

 ![](https://img-blog.csdnimg.cn/img_convert/6fb55bc990e0eb811ce9303640921486.png)

 ![](https://img-blog.csdnimg.cn/img_convert/ab8a6434f4515c16775435472a873221.png)

#### 使用文本编辑器编辑它，可以看到刚才的配置信息

![](https://img-blog.csdnimg.cn/img_convert/ccc3a17aeb5823553d75e6081cd5c63c.png)

 ![](https://img-blog.csdnimg.cn/img_convert/3df9daea6c48dade192158131df21074.png)

 **检查一下镜像站行不行命令1**

**npm config get registry**

![](https://img-blog.csdnimg.cn/img_convert/087562dead6f199f218f8032263d2067.png)

 ![](https://img-blog.csdnimg.cn/img_convert/1277205d6cca776b88f7fb23ec113750.png)

 **检查一下镜像站行不行命令2**

**Npm info vue 看看能否获得vue的信息**

![](https://img-blog.csdnimg.cn/img_convert/224014342e122552603196676f5f8e4c.png)

 ![](https://img-blog.csdnimg.cn/img_convert/580f43b3443c751115604db3b12a8c49.png)

#### 注意，此时，默认的模块D:\\nodejs\\node\_modules 目录

#### 将会改变为D:\\nodejs\\node\_global\\node\_modules 目录，

#### 如果直接运行npm install等命令会报错的。

#### 我们需要做1件事情：

#### 1、增加环境变量NODE\_PATH 内容是：D:\\nodejs\\node\_global\\node\_modules

![](https://img-blog.csdnimg.cn/img_convert/3f79255792c728601fd0fb7195684d33.png)

#### （注意，一下操作需要重新打开CMD让上面的环境变量生效）

#### 一、测试NPM安装vue.js

#### 命令：npm install vue -g

#### 这里的-g是指安装到global全局目录去

![](https://img-blog.csdnimg.cn/img_convert/5889d49f18335ce543450ebbf85fd8dd.png)

 ![](https://img-blog.csdnimg.cn/img_convert/ffe5c8d602ad058d4dbfdad556a1c9ed.png)

#### 二、测试NPM安装vue-router

#### 命令：npm install vue-router -g

![](https://img-blog.csdnimg.cn/img_convert/4024d8446e874a004be0151c8bca4bb8.png)

 ![](https://img-blog.csdnimg.cn/img_convert/38b6522c3e39ad77733d8f3f3ee8c0ba.png)

#### 运行npm install vue-cli -g安装vue脚手架

![](https://img-blog.csdnimg.cn/img_convert/2d23ea4ad2f33b3d571c3b1a7b28e11d.png)

![](https://img-blog.csdnimg.cn/img_convert/3e88d7433a401baf57c2498ced109591.png)

#### 编辑环境编辑path

![](https://img-blog.csdnimg.cn/img_convert/0f5351a8141de34b61fa5e1f4d4863dd.png)

#### 对path环境变量添加D:\\nodejs\\node\_global

#### win10以下版本的，横向显示PATH的，注意添加到最后时，不要有分号【;】

![](https://img-blog.csdnimg.cn/img_convert/48d5e84d132ba017e2dbf5915c62ca05.png)

#### 重新打开CMD，并且测试vue是否使用正常

![](https://img-blog.csdnimg.cn/img_convert/3c91448efcf967bc63f972324c26ecf9.png)

#### 注意，vue-cli工具是内置了模板包括 webpack 和 webpack-simple,前者是比较复杂专业的项目，

#### 他的配置并不全放在根目录下的 webpack.config.js 中

![](https://img-blog.csdnimg.cn/img_convert/f11c8646992878549289624c0ccd0330.png)

#### 初始化，安装依赖

![](https://img-blog.csdnimg.cn/img_convert/7de5fa3a2449afcad87128c61c107301.png)

#### 运行npm install安装依赖

![](https://img-blog.csdnimg.cn/img_convert/e3dfc9979ed19fba2a568a46fa373474.png)

 ![](https://img-blog.csdnimg.cn/img_convert/cabc86eb7771b4b01e659fa8885d4148.png)

#### 成功界面，提示打开地址http://localhost:8080

![](https://img-blog.csdnimg.cn/img_convert/f2d3b88e533e6f346f01c7c291a8b405.png)

#### 自动打开浏览器http://localhost:8080/#/

#### npm run build

#### 生成静态文件，打开dist文件夹下新生成的index.html文件

#### nmp下新建出来的vue01的目录描述：

![](https://img-blog.csdnimg.cn/img_convert/0afcef4fe0a45f12be2651652dbd3949.png)

大部分借鉴的下面这个大神的：

[https://www.cnblogs.com/liluxiang/p/9592003.html](https://www.cnblogs.com/liluxiang/p/9592003.html)

按着大神的步骤操作了一遍，没什么大问题。在此表示感谢，同时声明下，该篇文章只用来自己学习用。
-->