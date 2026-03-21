---
title: "cloudflare反向代理工具"
date: "2026-03-21"
tags:
  - 随笔
  - 笔记
  - UI
  - Git
  - 网络
categories:
  - ANote
comments: true
---
# cloudflare反向代理工具

😀

当我们建立Cloudflare团队账户后，就打通了外网访问路径，实现了免费科学上网，但您是不是发现仍然不能正常访问ChatGPT，一会能访问一会又不能了，而且网速还很慢。今天通过对workers脚本的部署，手把手带您创建一个能无障碍访问油管、奈菲，chatgpt的科学上网环境。如果您还缺一个免费科学上网的备选方案，并且想了解worker脚本的部署方法，一定不要错过。

![Video preview](https://i.ytimg.com/vi/1Jvo9I37yAU/hqdefault.jpg)

## 📝 通过Workers脚本部署设置，手把手带您实现免费高速科学上网，无障碍访问奈菲，ChatGPT

### 脚本部署工具连接

v2rayN客户端及workers代码都托管在GitHub上，访问时需要科学上网。

#### 1、v2rayN下载

#### 2、登陆Cloudflare：

Cloudflare账户注册小布出过一期Zero Trust团队账户设置视频，其中演示了怎么注册Cloudflare账户，不会注册的朋友可以参考那期视频。

#### 3、部署workers脚本：

Wordkers脚本：

部署中修改两个地方：替换UUID，CF反代IP，反代IP可以使用下面大佬提供的，也可以自己去筛选。如果使用的是\[ 3K大佬的 \]worker脚本，替换下伪装域名。

**http** \= \[80, 8080, 8880, 2052, 2086, 2095, 2082\] **https** \= \[443, 8443, 2053, 2096, 2087, 2083\]

**大佬提供的CF反代IP：**

```

```

**优选域名：**

```
```

#### 4、**套Tls**设置v2rayN（建议套上Tls）

套Tls需要将域名托管到Cloudflare，所以配置之前要想将域名托管设置好

4.1、添加自定义域

4.2、获取vless订阅地址

4.3、v2rayN中添加vless订阅地址

4.4、修改端口为443，传输层安全（Tls）开启

## Workers脚本设置步骤

#### 1、创建workers应用

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2F53074612-390f-4252-a146-71de27292848%2FUntitled.webp?table=block&id=6348310b-22f0-4936-ae5b-3635d6e6166b&t=6348310b-22f0-4936-ae5b-3635d6e6166b&width=1879&cache=v2)

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2F18e69067-7f52-449b-9d84-1c49c4260b8c%2FUntitled.webp?table=block&id=b8d9000a-e7b5-408d-bef3-58d7ccd3fb79&t=b8d9000a-e7b5-408d-bef3-58d7ccd3fb79&width=1877&cache=v2)

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2Ff38eca09-a25a-41a6-bae5-ecb8ca91cd5b%2FUntitled.webp?table=block&id=dde5a4c6-cb36-4416-8e14-827724ac9a0c&t=dde5a4c6-cb36-4416-8e14-827724ac9a0c&width=1877&cache=v2)

#### 2、添加workers脚本

2.1、复制github上的workers脚本

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2F01cd8894-8287-4d68-b204-42763882ed90%2FUntitled.webp?table=block&id=c98cefc4-0f06-48e3-a883-b3cc1e27b26c&t=c98cefc4-0f06-48e3-a883-b3cc1e27b26c&width=1881&cache=v2)

2.2、删除默认脚本并粘贴workers脚本

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2F3fa613d4-00b3-4141-8a71-427ce366b6d9%2FUntitled.webp?table=block&id=9777808d-683f-4017-b4c2-5cc4e7026037&t=9777808d-683f-4017-b4c2-5cc4e7026037&width=1878&cache=v2)

#### 3、修改UserID和proxyIP

UserID可以通过在线生成UUID得到，也可通过v2rayN创建Vless连接中的生成用户ID得到。

proxyIP可以复制上面大佬提供的反代域名，也可以自己筛选得到

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2Fa0f02faa-6f08-487d-8905-95faa945184a%2FUntitled.webp?table=block&id=8771cf5f-1962-442f-8615-e9e688c05031&t=8771cf5f-1962-442f-8615-e9e688c05031&width=1873&cache=v2)

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2F777971a4-4c2d-470d-9a12-0ccacd2d77a4%2FUntitled.webp?table=block&id=58a59feb-9805-469e-91ae-a74e3ecae558&t=58a59feb-9805-469e-91ae-a74e3ecae558&width=1880&cache=v2)

#### 4、生成应用

4.1、保存并部署部署

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2Fe99c7a9a-c626-4cc1-9dba-d69a545666d0%2FUntitled.webp?table=block&id=2763218d-2ae6-4c3d-873d-59376bf30c74&t=2763218d-2ae6-4c3d-873d-59376bf30c74&width=1883&cache=v2)

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2F57adbf49-d732-4864-a990-56e57777c7e4%2FUntitled.webp?table=block&id=bf751c31-2c3a-4894-bedf-add3f40fb9ec&t=bf751c31-2c3a-4894-bedf-add3f40fb9ec&width=1876&cache=v2)

### 获取未加密的Vless订阅连接

#### 1、 打开连接

1.1、点workers.dev (点击此链接前需要科学上网)

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2F5392b333-e998-431c-a589-78b803d488dc%2FUntitled.webp?table=block&id=441c54a9-8fa2-4c77-9bb5-6263e3a03d4d&t=441c54a9-8fa2-4c77-9bb5-6263e3a03d4d&width=1907&cache=v2)

1.2、如果看到下面的代码说明部署成功

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2F07345770-0546-4eda-9bbe-d6ac0fce56b3%2FUntitled.webp?table=block&id=ef8deedb-08cc-4d57-8825-67bdecefff05&t=ef8deedb-08cc-4d57-8825-67bdecefff05&width=1876&cache=v2)

#### 2、添加UserID

在连接后面添加UserID（就是workers代码中UserID），注意添加反斜线 “ **/** ”，然后回车

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2Fbdb28598-03ee-4546-bd72-0eb5953f8dae%2FUntitled.webp?table=block&id=6598d48d-7b73-402b-8147-42807f4d844f&t=6598d48d-7b73-402b-8147-42807f4d844f&width=1050&cache=v2)

#### 3、生成Vless订阅连接

得到未套Tls的Vless订阅连接

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2F59de94ff-aa30-443f-909c-58a0295a9b27%2FUntitled.webp?table=block&id=5d8846a8-4278-457c-89c7-19949560653b&t=5d8846a8-4278-457c-89c7-19949560653b&width=1876&cache=v2)

### 获取Tls加密的Vless订阅连接

操作前需确定域名已经成功托管到Cloudflare上

#### 1、添加自定义域

1.1、点击刚刚添加的edge应用

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2F282ed8be-ed9d-4701-9e4a-42e9133ea48c%2FUntitled.webp?table=block&id=e7454faf-3005-4f94-adb0-f5d1ed1e04f2&t=e7454faf-3005-4f94-adb0-f5d1ed1e04f2&width=1882&cache=v2)

1.2、点击【查看】，或者点击【触发器】

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2Fd356e56e-84b0-4195-b91b-d0602302f3e8%2FUntitled.webp?table=block&id=4998ea65-dd9b-4c8d-9314-584c72151ecf&t=4998ea65-dd9b-4c8d-9314-584c72151ecf&width=1874&cache=v2)

1.3、点击【添加自定义域】

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2F43472afd-7373-4c49-b6b0-b95e59f32b4c%2FUntitled.webp?table=block&id=014e07f6-257e-4f1b-9a52-493a09aaa7c4&t=014e07f6-257e-4f1b-9a52-493a09aaa7c4&width=1872&cache=v2)

1.4、输入一个二级域名，名称随便起。二级域名要填写完整（**二级域名**.temptemps.top）

然后点击下面的添加自定义域按钮

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2F0c79e97a-63a7-4682-ad40-f9e71936328d%2FUntitled.webp?table=block&id=c7a37bc4-ef32-4a41-80d5-dbb1112dcff9&t=c7a37bc4-ef32-4a41-80d5-dbb1112dcff9&width=1867&cache=v2)

1.5、添加自定义域后续等待证书申请完成

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2Fc7e10238-884b-484b-a4fa-dad5d99658c9%2FUntitled.webp?table=block&id=001bf4e0-c8d5-49d4-8b7d-55e85c88a2bd&t=001bf4e0-c8d5-49d4-8b7d-55e85c88a2bd&width=1876&cache=v2)

看到有效即证书申请完成

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2Ff4d21491-8d3a-4b73-a94e-05fceb2aac96%2FUntitled.webp?table=block&id=7fa8ec6c-882b-4e5a-9b76-10e83c32625b&t=7fa8ec6c-882b-4e5a-9b76-10e83c32625b&width=1862&cache=v2)

#### 2、 打开连接

2.1、点击刚刚生成的二级域名

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2F5c114970-5f5d-4ac7-89a7-c9bb25c7dfa3%2FUntitled.webp?table=block&id=4899ff62-4b72-438e-b4ac-f542f68782bc&t=4899ff62-4b72-438e-b4ac-f542f68782bc&width=1898&cache=v2)

2.2、看到下面代码说明部署成功

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2F226af9b9-1976-4212-ad3e-6aeab5fb6c9e%2FUntitled.webp?table=block&id=6dc44bfb-0026-4064-9ddb-dd5121863dc8&t=6dc44bfb-0026-4064-9ddb-dd5121863dc8&width=1914&cache=v2)

#### 3、生成Vless订阅连接

3.1、在域名后添加UserID回车，得到以套Tls的vless订阅连接

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2F8b2d8fae-74c5-4f27-a0ae-6bbd17c0a858%2FUntitled.webp?table=block&id=4ba8c042-ca62-4312-a4fb-a3475b10c1c2&t=4ba8c042-ca62-4312-a4fb-a3475b10c1c2&width=1686&cache=v2)

### v2rayN客户端设置

#### 1、添加未套Tls的vless连接

1.1、复制未加密vless订阅连接，粘贴到v2rayN客户端

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2F59de94ff-aa30-443f-909c-58a0295a9b27%2FUntitled.webp?table=block&id=5f91ef69-b62c-42ed-bf45-cf519c99b8f3&t=5f91ef69-b62c-42ed-bf45-cf519c99b8f3&width=1876&cache=v2)

1.2、打开v3rayN客户端，从剪贴板导入批量URL或者直接按Ctrl+V

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2F991fbdcb-11e7-4d75-bed3-9da4564b6cd2%2FUntitled.webp?table=block&id=c66e2d74-fb9c-4e2c-a503-c15a4c3cb570&t=c66e2d74-fb9c-4e2c-a503-c15a4c3cb570&width=840&cache=v2)

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2F545b9af0-cd34-4c10-949f-0b064bddfb1f%2FUntitled.webp?table=block&id=45f6e54e-d757-45ef-9018-cfa99cb6b2fd&t=45f6e54e-d757-45ef-9018-cfa99cb6b2fd&width=1218&cache=v2)

1.3、双击连接打开配置页面,因为是为加密的vless订阅，不能使用443端口，将443端口改为80,传输层安全（Tls）：设置为空

总共有7个端口可选，可以任选其中一个： \[80, 8080, 8880, 2052, 2086, 2095, 2082\]

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2F368a5508-f56a-40e6-8faf-cccf9e93c5eb%2FUntitled.webp?table=block&id=ffb17f3f-bd26-48cb-822b-af69dbd1969c&t=ffb17f3f-bd26-48cb-822b-af69dbd1969c&width=1233&cache=v2)

#### 2、添加已套Tls的vless连接

2.1、复制生成的Vless订阅连接

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2F8b2d8fae-74c5-4f27-a0ae-6bbd17c0a858%2FUntitled.webp?table=block&id=98b81228-ed74-4bcb-a596-a58d4260a3a3&t=98b81228-ed74-4bcb-a596-a58d4260a3a3&width=1686&cache=v2)

2.2、粘贴到v2rayN中

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2F86e7dc5a-4ef1-4a7f-b580-8bb749058504%2FUntitled.webp?table=block&id=fd4e8aaa-38ed-45e2-854f-073e06da2669&t=fd4e8aaa-38ed-45e2-854f-073e06da2669&width=1282&cache=v2)

Vless添加后不用修改设置，如果出现不能访问的情况，可将地址修改为优选ip或优选域名

Tls端口总共有6个端口可选，可以任选其中一个： \[443, 8443, 2053, 2096, 2087, 2083\]

![notion image](https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fee629410-c1e7-477c-acf8-9cf2619b7702%2Fda1b6b38-08f6-44de-b963-bc2c9f1e3c5a%2FUntitled.webp?table=block&id=bdd08b80-161b-4135-ba3d-8ad0c52084f4&t=bdd08b80-161b-4135-ba3d-8ad0c52084f4&width=1796&cache=v2)

## CloudFlare在线优选IP网站:
本地IP优选网址: <http://ip.flares.cloud/>  
在线IP优选网址： <https://stock.hostmonit.com/CloudFlareYes>  
在线IP优选网址： <https://monitor.gacjie.cn/page/cloudflare/ipv4.html>  
在线IP优选网址： <https://monitor.gacjie.cn/page/cloudflare/cname.html>  
在线IP优选网址： <https://api.uouin.com/cloudflare.html>  

## cloudflare 优选域名
```
*.cloudflare.182682.xyz
115155.xyz
cdn.2020111.xyz
cf.0sm.com
cf.090227.xyz
f3058171cad.002404.xyz
cf.zhetengsha.eu.org
8.889288.xyz
cf.zerone-cdn.pp.ua
cf.cdn.bingbook.cn
achk.cloudflarest.link
cfip.1323123.xyz
cf.877771.xyz
cnamefuckxxs.yuchen.icu
```