---
title: "lua 闭包 和and/or 操作符及其它的说明"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["lua"]
categories: ["lua"]
---

<!--more-->

>今天发现学过的知识不常用的都忘了差不多了，这里重新整理下，做下记录吧

####  0X01 闭包

>在Lua中，闭包（closure）是由一个函数和该函数会访问到的非局部变量（或者是upvalue）组成的，其中非局部变量（non-local variable）是指不是在局部作用范围内定义的一个变量，但同时又不是一个全局变量，主要应用在嵌套函数和匿名函数里，因此若一个闭包没有会访问的非局部变量，那么它就是通常说的函数。也就是说，在Lua中，函数是闭包一种特殊情况。简而言之，闭包就是一个函数加一个upvalue。那么接下来看下upvalue是啥。
>
>Lua使用结构体upvalue来实现闭包。外面的局部变量可以直接通过upvalue进行访问。upvalue最开始的时候指向栈中的一个变量，此时这个变量还在它的生存周期内。当变量离开作用域（译者注：就是函数返回后，变量的生存周期结束时），这个变量就从栈转移到了upvalue中。虽然这个变量存储在upvalue中，但是访问这个变量还是间接通过upvalue中的一个指针进行的（译者注：和在栈中时候的访问方式一样）。因此，变量位置的转移对任何试图读写这个变量的代码都是透明的。有别于这个变量在一个函数内部时候的行为，函数声明、访问这个变量，就是直接对栈的操作。
>来自[lua闭包全面解析](https://blog.csdn.net/peter_teng/article/details/52750022) 这篇有详细说明


lua的闭包之前自己也研究过这里做下记录吧，直接上代码
```c
function test()
	local i=0;
	local f=function()
				i=i+1;
				return i
			end
	return f
end
--这里生成一个闭包f1，同时变量i也是闭包的一部分
local f1 = test()
local a = f1()
local b = f1()
--这里再生成一个闭包f2，同时变量i也重新创建也是闭包的一部分，是和前面没有任何关系的
local f2=test()
local c=f2()
local e=f1()
local d=f2()

print("a:"..a.." b:"..b.." c:"..c.." d:"..d.." e:"..e)


```

结果：
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181011195056786.png)  


~~关于闭包的应用场景，这里没有过多的去注意，很尴尬，至今为止可能用过没有注意，~~ 
这里有个例子：
方法参数button，clickHandler，caller，data，isNotSound对于evtHandler方法是upvalue数据，属于 evtHandler闭包相关的，之前没注意
```c
--isSound:true:没有声音。false：有声音
function UIComponent:RegisterButtonClickHandler(button, clickHandler, caller,data,isNotSound)  
    --local obj = self:GetChildObj(childName);
    --if nil == obj then return end;

    if nil == button then return end;

    local evtHandler = function()
        if(isNotSound ~= true)then
            local musicstr = "click"
            audio.AudioMgr.GetInstance():PlayEffect(musicstr) --音效
        end
        
        if nil == caller then
            clickHandler();
        else
            if data then
                clickHandler(caller,button,data);
            else
                clickHandler(caller,button);
            end
             
        end
--        audios.AudioManager.GetInstance():PlayEffectSound(11);
    end

    --button.onClick:AddListener(evtHandler);
    --button.colors.pressedColor = UnityEngine.Color.black
 
    self.m_Behaviour:AddClick(button,evtHandler, caller);
    return obj;
end
```
再来一个例子
方法参数obj,params对于cb方法是upvalue数据，属于 cb闭包相关的，其实用的蛮多的
```c
function utils.HttpUtil.FileUploadAsync(url,path,fileName,callback,obj,params)
    local maxRetryCount=2;
    local cb=function(content,errcode)
        if obj then
            callback(obj,content,errcode,params)
        else
            callback(content,errcode,params)
        end
    end    

    CSHttpUtil.FileUploadAsync(url,path,fileName,cb,maxRetryCount)
end
```
> 参考文章
~~[深入理解Lua的闭包一：概念、应用和实现原理](https://blog.csdn.net/maximuszhou/article/details/44280109)，关于应用还是不要参考这篇文章了，感觉不对，文章说的table.sort方法我觉得不是闭包~~ 
> [lua闭包全面解析](https://blog.csdn.net/peter_teng/article/details/52750022) 这篇有详细说明

####  0X02 and/or操作符

*操作符这里有坑，之前以为和c语言类似，但今天发现不对*
Lua中的逻辑运算符：与(and)、或(or)和非(not)，与其他语言的逻辑运算符功能一致，这里不做赘述。只说一点，==所有的逻辑运算符将false和nil视为假，其他任何东西视为真，0也视为真。==
直接上代码：
```c
--and 操作符 如果前面的参数为假则直接输出前面的值
local a = 0 and 3
local b = nil and 3
local m = false and 3
--nil和false不能直接拼接字符串，所以需要先tostring
print( "a:"..a.."  b:"..tostring( b).." m:"..tostring( m))

--or 操作符 如果前面的参数为假则直接输出后面的值
local c = 0 or 5
local d = nil or 5
local e = false or 5
local f = nil or false
print( "c:"..c.."  d:"..d.." e:"..e.." f:"..tostring(f))

if 0 then
	print("0 is true !")
else
	print("0 is false")
end
if nil then
	print("nil is true !")
else
	print("nil is false")
end

if false then
	print("false is true !")
else
	print("false is false")
end


```
结果：
  

![结果](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181011202238228.png)  

>参考文章：
>[Lua中and、or的一些特殊用法](https://blog.csdn.net/gzy252050968/article/details/50513100/)

####  0X03 多行字符串

一个字符串带换行的怎么处理这里说明下,使用`[[   ]]`来处理
```c
local text=[[
abc
def
hello
world
]]
print(text)
```
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181011203321427.png)  


####  0X04 lua递归函数

c语言允许函数内部调用函数本身，==但lua不允许函数内部调用函数本身==
**递归调用需要先定义一个函数变量，这样在函数内部调用本身的时候后能访问到定义的函数变量地址**
```c
--一个阶乘的例子
--递归调用需要先定义一个函数变量，这样在函数内部调用本身的时候后能访问到定义的变量地址
local fact
fact = function (n)
    if n == 0 then
          return 1 
     else
       return n*fact(n-1)
    end
end

--120
print(fact(5))

--错误的用法
local fact1 = function (n)
    if n == 0 then
          return 1 
     else
       return n*fact1(n-1)
    end
end
print(fact1(5))
```
结果：
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181011203830657.png)  


