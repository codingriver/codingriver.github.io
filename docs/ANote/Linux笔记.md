# Linux笔记

### 常用命令
- 路由表
在 Windows 系统中，你可以使用以下命令来查看路由表：
```
route print

或者

netstat -r

#  tracert显示路由耗时
tracert www.example.com
或者
tracert 192.168.1.1
```
在 Unix/Linux 系统中，你可以使用以下命令来查看路由表：
```
netstat -rn
或者

ip route
```
这些命令会列出当前系统的路由表，包括目的网络、子网掩码、网关、接口等信息，这对于网络故障排查和理解数据包如何在网络中传输非常有用。



### zerotier配置及moon服务器搭建
><https://www.itblogcn.com/article/1815.html>
>
><https://www.cnblogs.com/cx850116/p/17805450.html>

#### Moon是什么，为什么需要Moon？
ZeroTier通过自己的多个根服务器帮助我们建立虚拟的局域网，让虚拟局域网内的各台设备可以打洞直连。这些根服务器的功能有些类似于通过域名查询找到服务器地址的DNS服务器，它们被称为Planet。然而这里存在一个非常严重的问题，就是Zerotier的官方行星服务器都部署在国外，从国内访问的时候延迟很大，甚至在网络高峰期的时候都没法访问，这也会导致我们的虚拟局域网变得极不稳定，经常掉链子。

为了应对网络链接的延迟和不稳定，提高虚拟局域网的速度和可靠性，Zerotier允许我们建立自己的moon卫星中转服务器。

作为Moon服务器不需要具备太强大的CPU性能/内存空间和存储空间，虚拟机、VPS、或者云服务器甚至一个树莓派都行，当然，这台服务器需要长时间可靠在线并且具有静态IP地址（ZeroTier官网上说公网IP或者内网IP都可以，只是如果用的是内网IP的话，在外网的设备就只能依靠Planet而不能使用moon了）。

#### Moon服务器配置过程
以Linux系统为例配置Moon服务器

##### TIPS：

由于ZeroTier本身使用UDP协议，因此如果存在防火墙的话，需要开放UDP，否则无法连接。
本篇内容仅介绍ZeroTier-Moon服务器的配置。

##### 安装

下载并安装ZeroTier:
```
curl -s https://install.zerotier.com/ | sudo bash
```
安装完成后得到一个ID：
```
*** Success! You are ZeroTier address [ 1c110b9ac2 ]
```
加入网络（只作为Moon服务的话不用加入网络）：
```
sudo zerotier-cli join 3efa5cb78a961967
200 join OK
```
进入ZeroTier的默认安装目录，生成Moon配置文件：
```
cd /var/lib/zerotier-one
sudo zerotier-idtool initmoon identity.public > moon.json
vim moon.json
```
其内容包括id、objtype、roots、signingKey等等。

生成的文件样式如下：
```
 "id": "1c110b9ac2",
 "objtype": "world",
 "roots": [
  {
   "identity": "9c960b9ac2:0:daca38dfc5f3",
   "stableEndpoints": []
  }
 ],
 "signingKey": "676f0c29eb8d6f2f00ce22ee2082b3ec",
 "signingKey_SECRET": "39de9f7ab16d0adb035276b7281f73344",
 "updatesMustBeSignedBy": "676f0c29eb8d6f2f00ce22ee",
 "worldType": "moon"
}
```
这里我们需要根据自己服务器的公网静态IP，修改stableEndpoints那一行格式如下，其中11.22.33.44为你的公网IP，9993是默认的端口号：
```
"stableEndpoints": [ "11.22.33.44/9993" ]
```
根据moon.json文件生成真正需要的签名文件.moon：
```
sudo zerotier-idtool genmoon moon.json
```
输出：
```
wrote 0000009c960b9ac2.moon (signed world with timestamp 1280398410930)
```
执行该命令以后会在软件目录下生成一个类似000000xxxxxxxxx.moon的文件，妥善保存该文件，因为要使用moon服务器，必须在所有客户端上面都发送一个这个文件。

移动.moon签名文件到moons.d目录下并且重启服务
```
cd /var/lib/zerotier-one
mkdir moons.d
mv 000000*.moon moons.d
service zerotier-one restart
```
#### 其他客户端使用
其他机器如果要使用Moon服务器，必须要在本地加入之前生成的.moon签名文件并重启服务才能生效。有两种方法。

一、在本机的Zerotier安装目录创建moons.d文件夹，然后下载该签名文件放在创建的moons.d目录里,重启服务。
```
#For linux
# 一般是 /var/lib/zerotier-one 目录下
cd /var/lib/zerotier-one
mkdir moons.d
# 将 .moon 文件移动到 moons.d 目录下

```
二、直接使用命令zerotier-cli orbit

```
Windows和Linux通用
# zerotier-cli orbit
sudo zerotier-cli orbit 9c960b9ac2 9c960b9ac2
200 orbit OK
# zerotier-one restart
sudo service zerotier-one restart
zerotier-one stop/waiting
zerotier-one start/running, process 18347
```
客户端添加.moon文件后需要重启ZeroTier One！Windows要在服务中重启ZeroTier One

##### 检查连接是否成功
```
#for linux and windows(windows需要用管理员模式启动cmd输入)
zerotier-cli listpeers
```
如果输出中出现一条最后为MOON的记录，说明已经成功连接Moon服务器
```
zerotier-cli listpeers
200 listpeers <ztaddr> <path> <latency> <version> <role>
200 listpeers id myip/9993;6012;1706 -1 1.8.4 MOON
200 listpeers 62f865ae71 50.7.252.138/9993;6012;1070 -294 - PLANET
```

### centos更改docker镜像默认存储位置

1、需求背景
docker镜像默认存放在根目录下，而有时候根目录往往比较小或者有时候需要重装系统，将docker镜像放在根目录下有被删除或者根目录被撑爆的风险，因此需要将docker镜像默认存储位置更改为其他数据盘的位置。

2、解决办法

2.1、修改/etc/docker/daemon.json文件
在终端执行以下命令：
```
vim /etc/docker/daemon.json
```
然后添加以下内容：
```
{
  "data-root": "/data/docker" #将docker的默认存储位置在该目录下
}
```
2.2、重启docker
```
systemctl restart docker
```
2.3、检测是否生效
```
docker info | grep "Docker Root Dir"
```
如果输出为 Docker Root Dir: /data/docker，则说明更改生效

如果感觉对你有用，麻烦点击一下小红心，谢谢！

### CentOS8.5安装docker
><https://blog.csdn.net/Monster_WangXiaotu/article/details/122590389>
>
><https://www.cnblogs.com/jolyonyue/p/16963568.html>

### Centos安装docker和docker-compose
CentOS9以上
1. yum安装docker服务
```
yum install -y docker
```
2. 启动docker服务
```
systemctl start docker  
systemctl enable docker
systemctl status docker
```
3. 安装docker-compose
```
curl -L https://github.com/docker/compose/releases/download/v2.14.1/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
或者: curl -L http://mirror.azure.cn/docker-toolbox/linux/compose/v2.14.1/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose

chmod +x /usr/local/bin/docker-compose
```
4. 开启你的docker之旅吧！
```
docker run ...
```

### Emulate Docker CLI using podman. Create /etc/containers/nodocker to quiet msg. Error: open /proc/sel

问题描述：在Centos8系统中，使用docker run时，出现如下报错：
Emulate Docker CLI using podman. Create /etc/containers/nodocker to quiet msg.
Error: open /proc/self/uid_map: no such file or directory

解决办法：
1，卸载podman软件（可以使用rpm -qa|grep docker）
yum remove docker
2,下载docker-ce源
curl https://download.docker.com/linux/centos/docker-ce.repo -o /etc/yum.repos.d/docker-ce.repo
3，安装docker-ce
yum install docker-ce -y

问题原因分析：
Centos 8使用yum install docker -y时，默认安装的是podman-docker软件

### 问题解决：Failed to download metadata for repo ‘appstream‘: Cannot prepare internal mirrorlist:...

大家都知道Centos8于2021年年底停止了服务，大家再在使用yum源安装时候，出现下面错误“错误：Failed to download metadata for repo ‘AppStream’: Cannot prepare internal mirrorlist: No URLs in mirrorlist”

1、进入yum的repos目录
```
cd /etc/yum.repos.d/
```

2、修改所有的CentOS文件内容
```
sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*

sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*
```
3、更新yum源为阿里镜像
```
wget -O /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-vault-8.5.2111.repo

yum clean all

yum makecache
```
4、yum安装测试是否可以yum安装
```
yum install wget –y
```

