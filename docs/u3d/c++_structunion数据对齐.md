---
title: "C++ struct union数据对齐"
date: 2019-12-01T21:57:40+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["c++"]
categories: ["c++"]
---

<!--more-->

> 数据对齐几年前看过，都忘了，看`深入理解计算机系统`又看到了，今天回顾下做下记录  
> 参考文章:  [ struct union数据对齐和sizeof大小](https://blog.csdn.net/zhengjihao/article/details/77816708)  
>**这篇文章只说明struct结构体和union联合体的对齐**  

1. 基本数据类型的数据对齐 
基本类型的数据对齐值是其本身的大小。

2. struct/class的自身对齐值。**对于结构体和类的自身对齐值是所有成员中最大的自身对齐值。** 

	**结构体和类的对齐规则：先将数据成员对齐，在将结构体和类自身对齐，最终大小与数据成员顺序 有关。**  

	**这里的数据对齐是指数据的地址是对齐**

3. union的自身对齐值。**union的自身对齐值是所有成员中最大的对齐值。union的对齐规则，只需要union自身对齐，不需要数据成员对齐,最终大小与数据成员顺序无关。**

4. 指定对齐值。使用#pragma pack(n)指定对齐值为n,使用#pragma pack() 回复默认对齐值。

5. 有效对齐值。
   
   对于指定了对齐值的代码， 有效对齐值=min(类/结构体/成员的自身对齐值， 指定对齐值)  

	未指定对齐值时，默认的对齐值一般为4。   

	有效对齐值决定了数据存放的方式，sizeof运算符是根据有效对齐值计算大小的。

## struct结构体的数据对齐

上测试代码：
```c
#include <stdio.h>
#include <stdlib.h>

struct A
{
	char a[7];
	short b;
	int c;
};

struct B
{
	short a;
	int b;
	char c[9];

};

struct C
{
	int a;
	char b[7];
	short c;
};

void main()
{

	printf("A:%d\n", sizeof(A));
	printf("B:%d\n", sizeof(B));
	printf("C:%d\n", sizeof(C));
	A a;
	printf("a:%0x,a.a:%0x,a.b:%0x,a.c:%0x\n", &a, &a.a, &a.b, &a.c);
	B b;
	printf("b:%0x,b.a:%0x,b.b:%0x,b.c:%0x\n", &b, &b.a, &b.b, &b.c);
	C c;
	printf("c:%0x,c.a:%0x,c.b:%0x,c.c:%0x\n", &c, &c.a, &c.b, &c.c);
	
	system("pause");
}
```
结果：
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181013114611972.png)  


**A**

A的大小如果不考虑数据对齐的话为13，假设a变量起始位0X00,a.a是第一个变量，所以a.a的地址位0X00，a.a的地址对齐值是1，共分配7个字节；a.b的地址对齐值是2 ，所以a.b起始地址必须满足被2整除，所以a.b的地址是0X08（(7+1)%2=0），分配2个字节；a.c的地址对齐值是4，前面占用10个字节了，所以地址是0X0C（(10+2)%4=0）,分配4个字节，当前A的大小是16个字节，A的对齐值是4，16%4=0，所以A的大小是16字节

**B**

假设b变量起始位0X00,b.a是第一个变量，所以b.a的地址位0X00，b.a的地址对齐值是2，分配2个字节；b.b的地址对齐值是4 ，所以b.b起始地址必须满足被4整除，所以b.b的地址是0X04（(2+2)%4=0），分配4个字节；b.c的地址对齐值是1个字节，前面占用8个字节了，所以地址是0X08（(8+0)%1=0）,分配9字节，当前B的大小是17个字节，B的对齐值是4，(17+3)%4=0，所以B的大小是20字节

**C**

假设c变量起始位0X00,c.a是第一个变量，所以b.a的地址位0X00，c.a的地址对齐值是4，分配4个字节；c.b的地址对齐值是1 ，所以c.b起始地址必须满足被1整除，所以c.b的地址是0X04（(4+0)%4=0），分配7个字节；c.c的地址对齐值是2，前面占用11个字节了，所以地址是0X0C（(11+1)%2=0）,分配2字节，当前B的大小是14个字节，B的对齐值是4，(14+2)%4=0，所以B的大小是16字节

A,B,C结构体的数据对齐值是所有基础变量的最大值，这里是int，对齐值4，

*根据打印结果验证通过* 

## union联合体数据对齐

上测试代码：
```c
#include <stdio.h>
#include <stdlib.h>

union A
{
	char a[7];
	short b;
	int c;
};

union B
{
	short a;
	long long b;
	char c[9];

};


void main()
{

	printf("A:%d\n", sizeof(A));
	printf("B:%d\n", sizeof(B));
	printf("long long size:%d\n", sizeof(long long));
	A a;
	printf("a:%0x,a.a:%0x,a.b:%0x,a.c:%0x\n", &a, &a.a, &a.b, &a.c);
	B b;
	printf("b:%0x,b.a:%0x,b.b:%0x,b.c:%0x\n", &b, &b.a, &b.b, &b.c);
	system("pause");
}
```
结果：
  
  

![在这里插入图片描述](https://cdn.jsdelivr.net/gh/codingriver/cdn/20181013121547845.png)  

**A**

A 三个变量占用字节最大的值是a,7个字节，A的对齐值是4，所以A的大小是7+1=8（（7+1）%4=0）

**B**

B 三个变量占用字节最大的值是c,9个字节，B的对齐值是8，所以B的大小是9+7=16 （（9+7）%8=0）

结构体和联合体嵌套混合也是这么分析，这里不再做说明了