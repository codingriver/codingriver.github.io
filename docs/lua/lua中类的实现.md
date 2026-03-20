---
title: "lua中类的实现"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["lua"]
categories: ["lua"]
---

<!--more-->

> 这里说明下unity中一般用C# 加lua的方式来支持代码的热更新，而在lua中一般封装类来实现业务
> 这里两年前研究过，没有做记录，今天提到了，发现忘干净了，今天借此机会复习下做下记录吧!
> 第二节的代码已经找不到出处了
 
##  0X01 lua元表和元方法
元表设置：`    setmetatable(table, metatable)`
元表读取：`    getmetatable(table)`
元方法操作：
```
    metatable.元方法 = function (可接受参数)
		(函数体)
    end
 ```
#### table访问的元方法

**元方法：**
    算数运算符：`__add`(加法)[+]、`__mul`(乘法)[*]、`__sub`(减法)[-]、`__div`(除法)[/]、`__unm`(相反数)[-]、`__mod`(取模)[%]、`__pow`(乘幂)[^]。
    逻辑运算符：`__eq`(等于)[=]、`__lt`(小于)[<]、`__le`(小于等于)[<=]。
    其他运算符：`__concat`(连接)[..]、`__len`(取长度)[#]。
    其他元方法： 
    `__tostring`：返回值(可接受参数：table)
   ` __call`：函数调用(可接受参数：table, key)
    `__metatable`：保护元方法(字符串)
    `__index`：查找表索引(可接受参数：table, key)
    `__newindex`：添加新索引(可接受参数：table, key, value) 
**说明：**
**`__add`**
 如果任何不是数字的值（包括不能转换为数字的字符串）做加法， Lua 就会尝试调用元方法。 首先、Lua 检查第一个操作数（即使它是合法的）， 如果这个操作数没有为 "__add" 事件定义元方法， Lua 就会接着检查第二个操作数。 一旦 Lua 找到了元方法， 它将把两个操作数作为参数传入元方法， 元方法的结果（调整为单个值）作为这个操作的结果。 如果找不到元方法，将抛出一个错误。(其它 算数运算符和逻辑运算符及其它运算符跟这个类似)

**`__index`**

当我们访问一个表的不存在的域，返回结果为nil，这是正确的，但并不一定正确。实际上，这种访问触发lua解释器去查找__index元方法：如果不存在，返回结果为nil；如果存在则由__index 元方法返回结果。当我们想不通过调用__index 元方法来访问一个表，我们可以使用rawget函数。Rawget(t,i)的调用以raw access方式访问表。这种访问方式不会使你的代码变快（the overhead of a function call kills any gain you could have），但有些时候我们需要他，在后面我们将会看到。

**`__newindex`**

__newindex元方法用来对表更新，__index则用来对表访问。当你给表的一个缺少的域赋值，解释器就会查找__newindex元方法：如果存在则调用这个函数而不进行赋值操作。像__index一样，如果元方法是一个表，解释器对指定的那个表，而不是原始的表进行赋值操作。另外，有一个raw函数可以绕过元方法：调用rawset(t,k,v)不掉用任何元方法对表t的k域赋值为v。__index和__newindex 元方法的混合使用提供了强大的结构：从只读表到面向对象编程的带有继承默认值的表。


>参考文章 
>[Lua 元表与元方法](https://blog.csdn.net/jingangxin666/article/details/80382748 )
>[lua元表以及元方法](https://www.cnblogs.com/Dong-Forward/p/6063365.html)

##  0X02 lua类的实现
lua类的实现直接上类的实现的代码,注释加好了,文件名 `class.lua`
```js
--class.lua
local _class = { }

function class(super)
    -- 一个类的构建，这里构建的是类本身，ctor是构造函数，super是父类，这里继承只允许一个父类
    local class_type = { ctor = false, super = super }
    --vtbl是当前类中所有域存放的地方
    local vtbl = { }
    _class[class_type] = vtbl
    --_class[super]这里返回的是super 本身作为class_type 对应的vtbl
    --父类的vtbl
    vtbl.super = _class[super]  
    class_type.superclass = _class[super]

    --设置class_type类本身的元方法，这里操作的是vtbl，并没有修改class_type本身（查找域和添加域都是操作的vtbl，class_type只是简单的原型）
    setmetatable(class_type, {
        __newindex = function(t, k, v) vtbl[k] = v end,
        __index = function(t, k) return vtbl[k] end,
    } )

    if super then
        --关联父类子类的关系的查找域，vtbl关联父类的btbl查找域
        setmetatable(vtbl, {
            __index =
            function(t, k)
                if k and _class[super] then
                    local ret = _class[super][k]
                    vtbl[k] = ret
                    return ret
                else
                    return nil
                end
            end
        } )
    end

    class_type.New = function(...)
        -- 一个类实例的构建
        local obj = { class = class_type }
        -- 设置实例关联类的查找域vtbl
        setmetatable(obj, {
            __index =
            function(t, k)
                return _class[class_type][k]
            end
        } )

        --类和所有父类的ctor构造函数收集，第一个当前类的ctor，第二个父类的ctor，第三个父类的父类的ctor，....
        local inherit_list = { }
        local class_ptr = class_type
        while class_ptr do
            if class_ptr.ctor then table.insert(inherit_list, class_ptr) end
            class_ptr = class_ptr.super
        end
        local inherit_length = #inherit_list
        --调用所有构造函数，从最上层的父类ctor开始知道当前类的ctor
        if inherit_length > 0 then
            for i = inherit_length, 1, -1 do 
                inherit_list[i].ctor(obj, ...)
            end
        end
        obj.super = inherit_list[2];

        if detectMemoryLeak then
            registerToWeakTable(obj, debug.traceback("obj lua stack:"));
        end

        obj.class = class_type

        return obj
    end

    class_type.is = function(self_ptr, compare_class)
        if not compare_class or not self_ptr then return false end
        local raw_class = self_ptr.class
        while raw_class do
            if raw_class == compare_class then return true end
            raw_class = raw_class.super
        end
        return false
    end

    return class_type
end

--测试代码
function printclass(class_type)
	local s="{"
	for k,v in pairs(class_type)do
		s=s..tostring(k)..":"..tostring(v)..","
	end
	s=s.."}"..tostring(class_type)
    print("class_type::"..s);

	s="{"
    local vtbl=_class[class_type]
	for k,v in pairs(vtbl)do
		s=s..tostring(k)..":"..tostring(v)..","
	end
	s=s.."}"..tostring(vtbl)
    print("vtbl::"..s);
end
```
**这里说下，类的实现由两种，一种是纯copy所有的域，还有一种是元表访问，只有修改时才会在当前类真的添加父类的键，而不是修改父类的，这里用的是元表访问**

下面来做测试代码，文件名字`test.lua`，需要把`class.lua`和`test.lua`放在同一个目录下，require文件需要

```js
require"class"

--转table成为字符串
log=function(t)
	local s="{"
	for k,v in pairs(t)do
		s=s..tostring(k)..":"..tostring(v)..","
	end
	s=s.."}"
	return s;
end



--定义一个类A
A=class()
--定义一个静态变量
A.static=10

function A:ctor()
	self.a=3;
	print("---A:ctor----")
end
function A:test()
	print("---A:test----a:"..self.a)
end

--定义一个类B,继承A
B=class(A)
function B:ctor()
	self.b=5;
	print("---B:ctor----")
end
function B:test()
	print("---B:test----a:"..self.a)
end

--构建实例
local a= A.New()
a:test();
local b=B.New()
b:test();

--打印
printclass(A)
print("a::"..log(a))
print("------------------------------------------------------------")
printclass(B)
print("b::"..log(b))
print("--------------------------modify static of B----------------------------------")
B.static  =20;
printclass(B)
print("b::"..log(b))
print("--------------------------modify static of b----------------------------------")
b.static  =30;
printclass(B)
print("b::"..log(b))

```
结果：注意标红的a，是因为B实例化时执行了父类的ctor构造函数产生的，static:20和static:30,是因为  B.static=20,b.static=30代码通过__newindex实现的
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181011230250419.png)  



##  0X03 lua简单的类的实现
lua类的实现，==简单版本==
```js

--简单的类的实现
function class(super)
	local class_type={ctor=false,super=super}
	if super then
		setmetatable(class_type,{
			__index = function(t,k)
				if k then
					return super[k];
				else
					return nil
				end
			end
		})
	end
	
	class_type.New = function(...)
		local obj={class = class_type}
		setmetatable(obj,{
			__index = function(t,k)
				if k then
					return class_type[k];
				else
					return nil
				end
			end
		})
		
		local ctor_list={}
        local class_ptr = class_type
        while class_ptr do
            if class_ptr.ctor then table.insert(ctor_list, class_ptr) end
            class_ptr = class_ptr.super
        end		
		for i=#ctor_list,1,-1 do
			ctor_list[i].ctor(obj,...)
		end
		return obj;
	end

	return class_type
end


--测试代码
function printclass(class_type)
	local s="{"
	for k,v in pairs(class_type)do
		s=s..tostring(k)..":"..tostring(v)..","
	end
	s=s.."}"..tostring(class_type)
    print("class_type::"..s);
end
```
根据第二节的测试代码`test.lua`执行的结果：
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181011231837306.png)  
