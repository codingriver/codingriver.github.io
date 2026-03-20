---
title: "客户端开发C#命名规范手册"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["CSharp"]
categories: ["CSharp"]
---

<!--more-->



#### 命名规范
1.	使用驼峰法命名
2.	类名使用首字母大写的驼峰法命名，例如：PlayerObject
3.	方法名使用首写字母大写命名方式，例如：Init()
4.	成员变量、局部变量都统一使用首字母小写的命名方式，例如：localValue；属性首字母大写，字段统一小写；（属性是指带get，set访问器的）
5.	常量和enum的命名都使用大写+下划线的方式，例如：MAX_PLAYER_NUMBER
6.	抽象类名使用Abstract开头，例如：AbstractCharacter，接口使用I开头，例如：ITask
7.	避免在类和变量的命名中使用缩写
8.	对于接口和抽象类，需要在类前加注释，在每个方法上也尽量多写注释，用来说明类或者函数的作用
9.	枚举类名也使用首字母大写的驼峰法命名，且以Enum结尾，例如：ServerStatusEnum
10.	所有的语句块必须使用大括号包裹，禁止出现if(condition) do();这种使用方式，这种写法不利于调试


####  驼峰式（补充）
驼峰式命名法就是当变量名或函式名是由一个或多个单词连结在一起，而构成的唯一识别字时，第一个单词以小写字母开始；第二个单词的首字母大写或每一个单词的首字母都采用大写字母，例如：myFirstName、myLastName，这样的变量名看上去就像驼峰峰一样此起彼伏，故得名。 
驼峰式命名法（Camel-Case）一词来自 Perl 语言中普遍使用的大小写混合格式，而 Larry Wall 等人所著的畅销书《Programming Perl》（O’Reilly 出版）的封面图片正是一匹骆驼。 
驼峰式命名法的命名规则可视为一种惯例，并无绝对与强制，为的是增加识别和可读性。 
**小驼峰法**
变量一般用小驼峰法标识。驼峰法的意思是：除第一个单词之外，其他单词首字母大写。譬如 
int myStudentCount; 
变量myStudentCount第一个单词是全部小写，后面的单词首字母大写。 
**大驼峰法***
相比小驼峰法，大驼峰法把第一个单词的首字母也大写了。常用于类名，函数名，属性，命名空间。譬如 
public class DataBaseUser; 

