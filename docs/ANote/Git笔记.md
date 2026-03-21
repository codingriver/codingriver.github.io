---
title: "Git笔记"
date: "2026-03-21"
tags:
  - 随笔
  - 笔记
  - 工具链
  - Git
categories:
  - ANote
comments: true
---
# Git笔记

## Git LFS的使用
> <https://git-lfs.github.com/>  
> <https://www.jianshu.com/p/493b81544f80>  
> <https://zzz.buzz/zh/2016/04/19/the-guide-to-git-lfs/>  

```sh
# 查看安装的git lfs 环境信息
git lfs env 
git lfs env | head -2

# 查看当前使用 Git LFS 管理的匹配列表
git lfs track

# 使用 Git LFS 管理指定的文件
git lfs track "*.psd"

# 不再使用 Git LFS 管理指定的文件
git lfs untrack "*.psd"

# 类似 `git status`，查看当前 Git LFS 对象的状态
git lfs status

# 枚举目前所有被 Git LFS 管理的具体文件
git lfs ls-files

# 检查当前所用 Git LFS 的版本
git lfs version

# 针对使用了 LFS 的仓库进行了特别优化的 clone 命令，显著提升获取
# LFS 对象的速度，接受和 `git clone` 一样的参数。 [1] [2]
git lfs clone https://github.com/user/repo.git
```

1. `git lfs install`开启lfs功能
1. `git lfs track "*.png"` 添加大文件追踪，所有的png文件
    - 指定文件后缀名 `git lfs track "*.filetype"`
    - 指定某个目录下的所有文件 `git lfs track "directory/*"`
    - 具体指定某个文件 `git lfs track "path/to/file"`

1. `git lfs track ` 查看所有的lfs文件追踪模式
1. `git lfs ls-files` 可以显示当前跟踪的文件列表


### 迁移已有的 git 仓库使用 git lfs 管理
```sh
# 重写 master 分支，将历史提交中的 *.zip 都用 git lfs 进行管理
git lfs migrate import --include-ref=master --include="*.png"

# 重写所有分支及标签，将历史提交中的 *.rar,*.zip 都用 git lfs 进行管理
git lfs migrate import --everything --include="*.bin,*.lib,*.so,*.dll,*.a,*.param,*.zip,*.gz,*.png,*.jpg,*.unitypackage,*.hdr,*.HDR" 
```
**注意：** 重写历史后的提交需执行：   
```sh
git push --force --all
```  
*注意： 如有迁移至 git lfs 前的仓库的多份拷贝，其他拷贝可能需要执行 git reset --hard origin/master 来重置其本地的分支，注意执行 git reset --hard 命令将会丢失本地的改动。*  

如果需要对本地仓库进行清理(非安全的)  
```sh
git reflog expire --expire-unreachable=now --all
git gc --prune=now
```
## `git clone`命令
`git clone -b ${branch} --depth=1` 可以拉对应分支

## `git clone --depth=1`后只有一个分支的解决办法
> `git clone --depth=1`克隆项目后，使用`git branch -r`查看远程仓库只显示一个分支，实际远程仓库有多个分支。
>
>这种方法克隆的项目只包含最近的一次commit的一个分支，体积很小，即可解决文章开头提到的项目过大导致Timeout的问题，但会产生另外一个问题，他只会把默认分支clone下来，其他远程分支并不在本地，也看不到其他远程分支。

### `checkout` 一个新的分支
```c
$ git clone --depth 1 https://github.com/dogescript/xxxxxxx.git
$ git remote set-branches origin 'remote_branch_name'
$ git fetch --depth 1 origin remote_branch_name
$ git checkout remote_branch_name
```
>参考：[https://blog.csdn.net/qq_29094161/article/details/120649473](https://blog.csdn.net/qq_29094161/article/details/120649473)

### 获取全部分支
修改.git/config文件中的  
`fetch = +refs/heads/master:refs/remotes/origin/master`  
为
`fetch = +refs/heads/*:refs/remotes/origin/*`  
然后执行

`git fetch --all`

> 参考[https://blog.csdn.net/a924068818/article/details/115725982](https://blog.csdn.net/a924068818/article/details/115725982)


## Git更新远程分支列表
```
git remote update origin --prune
```
> 这个命令没有测试
## Git 强制推送
```
git push -f origin master
git push --force origin master:master
```

## Git Pull

### git pull origin master:mm

 在repository中找到名字为master的branch，使用它去更新local repository中找到名字为mm的branch，，如果local repository下不存在名字是mm的branch，那么新建一个。(如果mm不是当前激活的分支，git pull执行完也不是)

## Git Push

### git push origin master:master

```
git push origin master:master
```
 在local repository中找到名字为master的branch，使用它去更新remote repository下名字为master的branch，如果remote repository下不存在名字是master的branch，那么新建一个

## Git Clean
> git clean命令用来从你的工作目录中删除所有没有tracked过的文件
>
>**git clean经常和`git reset --hard`一起结合使用**. 记住reset只影响被track过的文件, 所以需要clean来删除没有track过的文件. 结合使用这两个命令能让你的工作目录完全回到一个指定的<commit>的状态

- `git clean -n`
    是一次clean的演习, 告诉你哪些文件会被删除. 记住他不会真正的删除文件, 只是一个提醒

- `git clean -f`
    删除当前目录下所有没有track过的文件. 他不会删除.gitignore文件里面指定的文件夹和文件, 不管这些文件有没有被track过

- `git clean -f <path>`
    删除指定路径下的没有被track过的文件

- `git clean -df`
    删除当前目录下没有被track过的文件和文件夹

- `git clean -xf`
    删除当前目录下所有没有track过的文件. 不管他是否是.gitignore文件里面指定的文件夹和文件


下面的例子要删除所有工作目录下面的修改, 包括新添加的文件. 假设你已经提交了一些快照了, 而且做了一些新的开发
```sh
git reset --hard

git clean -df
```

运行后, 工作目录和缓存区回到最近一次commit时候一摸一样的状态.  
`git status`会告诉你这是一个干净的工作目录, 又是一个新的开始了！



> <https://www.jianshu.com/p/0b05ef199749>
 ## Git Config

用git config命令查看配置文件：  
- 查看仓库级的config，即`.git/.config`，命令：`git config –local -l`  
- 查看全局级的config，即`~\.gitconfig`，命令：`git config –global -l`  
- 查看系统级的config，即`C:\Program Files\Git\etc\gitconfig`，命令：`git config –system -l`  
*查看当前生效的配置，命令：`git config -l`，这个时候会显示最终三个配置文件计算后的配置信息*


查看当前生效的配置，命令：git config -l，这个时候会显示最终三个配置文件计算后的配置信息，如下图：

git有几个配置文件呢？ 是的，聪明的你，稍微查查资料就知道咯，git里面一共有3个配置文件
- 仓库级配置文件：`.git/config` (该文件位于当前仓库下)

```sh
[core]
	repositoryformatversion = 0
	filemode = true
	bare = false
	logallrefupdates = true
	ignorecase = true
	precomposeunicode = true
[remote "origin"]
	url = git@github.com:codingriver/codingriver.github.io.git
	fetch = +refs/heads/*:refs/remotes/origin/*
[branch "master"]
	remote = origin
	merge = refs/heads/master
[lfs]
	repositoryformatversion = 0
```

- 全局配置文件 `~/.gitconfig`

```sh
[user]
	name = codingriver
	email = codingriver@163.com
[filter "lfs"]
	clean = git-lfs clean -- %f
	smudge = git-lfs smudge -- %f
	process = git-lfs filter-process
	required = true


```
- 系统级配置文件 `C:\Program Files\Git\etc\gitconfig` (git安装目录)
```sh
[diff "astextplain"]
	textconv = astextplain
[filter "lfs"]
	clean = git-lfs clean -- %f
	smudge = git-lfs smudge -- %f
	process = git-lfs filter-process
	required = true
[http]
	sslBackend = openssl
	sslCAInfo = C:/Program Files/Git/mingw64/ssl/certs/ca-bundle.crt
[core]
	autocrlf = false
	fscache = true
	symlinks = false
[pull]
	rebase = false
[credential]
	helper = manager-core
[credential "https://dev.azure.com"]
	useHttpPath = true
[init]
	defaultBranch = master

```



 ```sh
 git config --global user.name “yourname”
 git config --global user.email “email@email.com ”
 ```
 案例:
 ```sh
 git config --global user.name "codingriver"
 git config --global user.email "codingriver@163.com"
 ```

 ## Git 提交空文件夹

 git设计时是不支持空文件夹提交的，这里是在文件夹里面新建.gitignore文件或者.gitkeep空文件来处理的
>unity也支持忽略以.开头的文件的

**新建.gitignore文件**
在空文件夹下新建.gitignore文件，文件内容：
```c
## Ignore everything in this directory
*
## Except this file
!.gitignore
```
这样就能提交git仓库了
*我这是在windows上操作的，不能直接创建以.开头的文件，参考这篇文章[Windows创建.开头的文件或者.开头的文件夹](https://blog.csdn.net/codingriver/article/details/83414019)*

**新建.gitkeep文件**
在空文件夹下新建.gitkeep文件，是空文件，这样就能提交git仓库了


## shell判断git remote是否存在

假如，要判断的 remote 的名字为 faraway。
- 第一种方案
```sh
if git config remote.faraway.url > /dev/null; then 
 …
fi
```
- 第二种方案
```sh
if git remote | grep faraway > /dev/null; then 
 …
fi
```

判断 remote 是否已存在，如果已存在，直接进行 git fetch faraway 等操作，如果不存在，git add remote faraway http://xxxxx 后，再进行操作。

>参考：   
> <https://www.jianshu.com/p/e4b9c6c6bab7>  
> <https://www.cnblogs.com/ibingshan/p/11126345.html>  
> <https://blog.csdn.net/longerzone/article/details/12948925>  


## shell 判断 git branch 分支是否存在

举例：判断当前分支是否为master，本地分支master是否存在，远端分支master是否存在
```sh
if git branch --list master | grep "*"; then 
    ## 分支名字完全匹配，不是模糊匹配！只能匹配master，不能匹配mastertest等
    echo "当前分支是master"
    git reset --hard
    git clean -df > /dev/null    
elif git branch --list | grep -w master > /dev/null; then
    ## 分支名字完全匹配，不是模糊匹配！只能匹配master，不能匹配mastertest等
    echo "master不是当前分支，但本地分支master存在"
    git reset --hard
    git clean -df > /dev/null
    git checkout  master
elif git branch -r | grep -w master; then
    ## 分支名字完全匹配，不是模糊匹配，只能匹配origin/master,不能匹配origin/mastertest等
    echo "本地分支master不存在,远端master分支存在"
    git reset --hard
    git clean -df > /dev/null
    git checkout -b  master origin/master
else
    echo "本地分支master不存在,远端master分支也不存在"
fi

```


## shell 判断 git本地工作文件夹是否干净(clean)

```sh
if [[ -z $(git status -s) ]]; then
  ## 没有修改的文件和未纳入版本控制的文件(untracked)的文件
  echo "没有可提交内容"
  exit 2
fi
```

> <https://blog.csdn.net/10km/article/details/100689481>
## git文件内容没变但status显示不同的解决方案
![](image/Git笔记/2022-01-17-21-47-17.png)

这里提示的不同，是文件的权限改变了。

SO，解决方案奏是：不让git检测文件权限的区别

```sh
git config core.filemode false
```
>参考: <https://blog.csdn.net/u012109105/article/details/51252242>


## The file will have its original line endings in your working directory
git 报错：
```
warning: LF will be replaced by CRLF in basic-markdown-syntax/index.html.
The file will have its original line endings in your working directory
warning: LF will be replaced by CRLF in hugo-loveit-problems/index.html.
The file will have its original line endings in your working directory
```



解决方案：
```sh
    git rm -r --cached .
    git config core.autocrlf false

    git add .
```
> <https://blog.csdn.net/namechenfl/article/details/81257973>
## Git处理换行符问题

对仓库使用 `.gitattributes`文件进行配置

```sh
# Set the default behavior, in case people don't have core.autocrlf set.
* text=auto #让git自行处理左边匹配的文件使用何种换行符格式，这是默认选项。
# text eol=lf

# Explicitly declare text files you want to always be normalized and converted
# to native line endings on checkout.
*.c text
*.h text

# Declare files that will always have CRLF line endings on checkout.
*.sln text eol=crlf

# Denote all files that are truly binary and should not be modified.
*.png binary
*.jpg binary
```
>参考: <https://blog.csdn.net/github_30605157/article/details/56680990>

项目在用的`.gitattributes`文件
```sh
* text=auto

*.cs diff=csharp text
*.cginc text
*.shader text
*.spriteatlas text eol=lf
# Unity YAML
*.anim -text merge=unityyamlmerge diff
*.asset -text merge=unityyamlmerge diff
*.controller -text merge=unityyamlmerge diff
*.mat -text merge=unityyamlmerge diff
*.meta -text merge=unityyamlmerge diff
*.physicMaterial -text merge=unityyamlmerge diff
*.physicsMaterial2D -text merge=unityyamlmerge diff
*.prefab -text merge=unityyamlmerge diff
*.unity -text merge=unityyamlmerge diff

# Unity LFS
*.cubemap filter=lfs diff=lfs merge=lfs -text
*.unitypackage filter=lfs diff=lfs merge=lfs -text

# 2D formats
*.[aA][iI] filter=lfs diff=lfs merge=lfs -text
*.[bB][mM][pP] filter=lfs diff=lfs merge=lfs -text
*.[dD][dD][sS] filter=lfs diff=lfs merge=lfs -text
*.[eE][xX][rR] filter=lfs diff=lfs merge=lfs -text
*.[gG][iI][fF] filter=lfs diff=lfs merge=lfs -text
*.[hH][dD][rR] filter=lfs diff=lfs merge=lfs -text
*.[iI][fF][fF] filter=lfs diff=lfs merge=lfs -text
*.[jJ][pP][eE][gG] filter=lfs diff=lfs merge=lfs -text
*.[jJ][pP][gG] filter=lfs diff=lfs merge=lfs -text
*.[pP][iI][cC][tT] filter=lfs diff=lfs merge=lfs -text
*.[pP][nN][gG] filter=lfs diff=lfs merge=lfs -text
*.[pP][sS][dD] filter=lfs diff=lfs merge=lfs -text
*.[tT][gG][aA] filter=lfs diff=lfs merge=lfs -text
*.[tT][iI][fF] filter=lfs diff=lfs merge=lfs -text
*.[tT][iI][fF][fF] filter=lfs diff=lfs merge=lfs -text

# 3D formats
*.3[dD][mM] filter=lfs diff=lfs merge=lfs -text
*.3[dD][sS] filter=lfs diff=lfs merge=lfs -text
*.[aA][bB][cC] filter=lfs diff=lfs merge=lfs -text
*.[bB][lL][eE][nN][dD] filter=lfs diff=lfs merge=lfs -text
*.[cC]4[dD] filter=lfs diff=lfs merge=lfs -text
*.[cC][oO][lL][lL][aA][dD][aA] filter=lfs diff=lfs merge=lfs -text
*.[dD][aA][eE] filter=lfs diff=lfs merge=lfs -text
*.[dD][xX][fF] filter=lfs diff=lfs merge=lfs -text
*.[fF][bB][xX] filter=lfs diff=lfs merge=lfs -text
*.[jJ][aA][sS] filter=lfs diff=lfs merge=lfs -text
*.[lL][wW][oO] filter=lfs diff=lfs merge=lfs -text
*.[lL][wW][oO]2 filter=lfs diff=lfs merge=lfs -text
*.[lL][wW][sS] filter=lfs diff=lfs merge=lfs -text
*.[lL][xX][oO] filter=lfs diff=lfs merge=lfs -text
*.[mM][aA] filter=lfs diff=lfs merge=lfs -text
*.[mM][aA][xX] filter=lfs diff=lfs merge=lfs -text
*.[mM][bB] filter=lfs diff=lfs merge=lfs -text
*.[oO][bB][jJ] filter=lfs diff=lfs merge=lfs -text
*.[pP][lL][yY] filter=lfs diff=lfs merge=lfs -text
*.[sS][kK][pP] filter=lfs diff=lfs merge=lfs -text
*.[sS][tT][lL] filter=lfs diff=lfs merge=lfs -text
*.[zZ][tT][lL] filter=lfs diff=lfs merge=lfs -text

# Audio formats
*.[aA][iI][fF] filter=lfs diff=lfs merge=lfs -text
*.[aA][iI][fF][fF] filter=lfs diff=lfs merge=lfs -text
*.[bB][aA][nN][kK] filter=lfs diff=lfs merge=lfs -text
*.[iI][tT] filter=lfs diff=lfs merge=lfs -text
*.[mM][oO][dD] filter=lfs diff=lfs merge=lfs -text
*.[mM][pP]3 filter=lfs diff=lfs merge=lfs -text
*.[oO][gG][gG] filter=lfs diff=lfs merge=lfs -text
*.[sS]3[mM] filter=lfs diff=lfs merge=lfs -text
*.[wW][aA][vV] filter=lfs diff=lfs merge=lfs -text
*.[xX][mM] filter=lfs diff=lfs merge=lfs -text

# Video formats
*.[aA][sS][fF] filter=lfs diff=lfs merge=lfs -text
*.[aA][vV][iI] filter=lfs diff=lfs merge=lfs -text
*.[fF][lL][vV] filter=lfs diff=lfs merge=lfs -text
*.[mM][oO][vV] filter=lfs diff=lfs merge=lfs -text
*.[mM][pP]4 filter=lfs diff=lfs merge=lfs -text
*.[mM][pP][eE][gG] filter=lfs diff=lfs merge=lfs -text
*.[mM][pP][gG] filter=lfs diff=lfs merge=lfs -text
*.[oO][gG][vV] filter=lfs diff=lfs merge=lfs -text
*.[wW][mM][vV] filter=lfs diff=lfs merge=lfs -text

# Build
*.[dD][lL][lL] filter=lfs diff=lfs merge=lfs -text
*.[mM][dD][bB] filter=lfs diff=lfs merge=lfs -text
*.[pP][dD][bB] filter=lfs diff=lfs merge=lfs -text
*.[sS][oO] filter=lfs diff=lfs merge=lfs -text

# Packaging
*.7[zZ] filter=lfs diff=lfs merge=lfs -text
*.[bB][zZ]2 filter=lfs diff=lfs merge=lfs -text
*.[gG][zZ] filter=lfs diff=lfs merge=lfs -text
*.[rR][aA][rR] filter=lfs diff=lfs merge=lfs -text
*.[tT][aA][rR] filter=lfs diff=lfs merge=lfs -text
*.[tT][aA][rR].[gG][zZ] filter=lfs diff=lfs merge=lfs -text
*.[zZ][iI][pP] filter=lfs diff=lfs merge=lfs -text

# Fonts
*.[oO][tT][fF] filter=lfs diff=lfs merge=lfs -text
*.[tT][tT][fF] filter=lfs diff=lfs merge=lfs -text

# Documents
*.[pP][dD][fF] filter=lfs diff=lfs merge=lfs -text

# Collapse Unity-generated files on GitHub
*.asset             linguist-generated
*.mat               linguist-generated
*.meta              linguist-generated
*.prefab            linguist-generated
*.unity             linguist-generated

```