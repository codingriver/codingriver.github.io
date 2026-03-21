# Nodejs初始化配置

> 转载：[windows安装npm教程](https://www.cnblogs.com/liluxiang/p/9592003.html)

## 使用之前，先掌握 3 个概念

- `npm`：Nodejs 下的包管理器
- `webpack`：通过 CommonJS 语法对浏览器端静态资源进行打包与准备
- `vue-cli`：用于生成 Vue 工程模板

## 开始

### 下载 Node.js

如图，下载 8.9.3 LTS（原文推荐）。

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212145017816-1078102167.png)

### 安装

- 双击安装
- 可以使用默认路径，本例中修改为 `d:\nodejs`
- 一路点 Next
- Finish 完成

### 打开 CMD 检查是否正常

![](https://images2017.cnblogs.com/blog/1287619/201712/1287619-20171212145657082-1826714804.png)

### 配置 npm 全局目录和缓存目录

先建立两个目录：

- `D:\nodejs\node_global`
- `D:\nodejs\node_cache`

然后运行：

```bash
npm config set prefix "D:\\nodejs\\node_global"
npm config set cache "D:\\nodejs\\node_cache"
```

### 配置镜像站

```bash
npm config set registry=http://registry.npm.taobao.org
npm config list
npm config get registry
npm info vue
```

### 配置环境变量

增加环境变量 `NODE_PATH`：

```text
D:\nodejs\node_global\node_modules
```

并将下面路径加入 `PATH`：

```text
D:\nodejs\node_global
```

## 测试 npm 安装 vue.js

```bash
npm install vue -g
npm install vue-router -g
npm install vue-cli -g
```

## 初始化项目

```bash
npm install
npm run dev
npm run build
```

## 说明

原文包含大量安装截图，当前已迁移核心步骤和关键命令，后续可继续补充完整图文说明。
