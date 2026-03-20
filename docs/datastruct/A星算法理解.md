---
title: "【数据结构】 A* 算法理解(C#)"
date: 2020-09-03T21:09:12+08:00
author: "codingriver"
authorLink: "https://codingriver.github.io"
tags: ["算法"]
categories: ["数据结构"]
---

<!--more-->


> 最近发现A\*算法忘的一干二净啊，记忆是个好东西，可惜吾没有啊，只能整理一篇文章以备日后翻看
> *这里只谈A\*算法的实现，不谈A*算法的优化*
> 这里的工程是unity版本的，当然理解A\*算法是通用的

这里先放上A*算法的unity工程(unity2017.3.1) **[unity工程](https://github.com/codingriver/UnityProjectTest/tree/master/AStarTest)**（github）

### 0X01 A*算法基本概念

**启发式搜索：** 启发式搜索就是在状态空间中的搜索对每一个搜索的位置进行评估，得到最好的位置，再从这个位置进行搜索直到目标。这样可以省略大量无畏的搜索路径，提到了效率。在启发式搜索中，对位置的估价是十分重要的。采用了不同的估价可以有不同的效果。
**IDA*算法：** 这种算法被称为迭代加深A*算法，可以有效的解决A*空间增长带来的问题，甚至可以不用到优先级队列。如果要知道详细：google一下。
**搜索区域（The Search Area）：** 图中的搜索区域被划分为了简单的二维数组，数组每个元素对应一个小方格，当然我们也可以将区域等分成是五角星，矩形等，通常将一个单位的中心点称之为搜索区域节点（Node）。　　
**开放列表(Open List)：** 我们将路径规划过程中待检测的节点存放于Open List中，而已检测过的格子则存放于Close List中。
**关闭列表(Close List)：** 我们将路径规划过程中已经检查过的节点放在Close List。
**启发函数（Heuristics Function）（估价函数）：** H为启发函数，也被认为是一种试探，由于在找到唯一路径前，我们不确定在前面会出现什么障碍物，因此用了一种计算H的算法，具体根据实际场景决定。在我们简化的模型中，H采用的是传统的曼哈顿距离（Manhattan Distance）估价函数，也就是横纵向走的距离之和。
==F(n) = G + H。F代表当前检查点的总花费，G代表起点到当前检查点的花费，H代表当前检查点到终点的预估花费。==
**父节点（parent）：** 在路径规划中用于回溯的节点。
*A\*算法的特点：* A*算法在理论上是时间最优的，但是也有缺点：它的空间增长是指数级别的。

### 0X02 A*算法寻路过程
1. 将起点A添加到open列表中（A没有计算花费F是因为当前open列表只有这一个节点）。
2. 检查open列表，选取花费F最小的节点M（检查M如果为终点是则结束寻路，如果open列表没有则寻路失败，直接结束）。
3.  对于与M相邻的每一节点N：（下面本来没有序号的，csdn markdown的bug）
	- 如果N是阻挡障碍，那么不管它。
    - 如果N在closed列表中，那么不管它。
	- 如果N不在open列表中：添加它然后计算出它的花费F(n)=G+H。
	- 如果N已在open列表中：当我们使用当前生成的路径时，检查F花费是否更小。如果是，更新它的花费F和它的父节点。
5. 重复2，3步。



### 0X03 A*算法寻路详细描述
寻路关键代码：
```csharp
    /// <summary>
    /// 使用A*算法寻路
    /// </summary>
    /// <param name="start"></param>
    /// <param name="end"></param>
    void FindPath(Vector2 start,Vector2 end)
    {
        //和A*算法无关，只是为了显示使用
        int showFindNum=1;

        //开启列表
        List<Cell> openLs = new List<Cell>();
        //关闭列表
        List<Cell> closeLs = new List<Cell>();

        //起点
        Cell startCell = grid.GetCell(start);
        //终点
        Cell endCell = grid.GetCell(end);
        Debug.LogFormat("寻路开始,start({0}),end({1})!",start,end);

        //将起点作为待处理的点放入开启列表，
        openLs.Add(startCell);

        //如果开启列表没有待处理点表示寻路失败，此路不通
        while(openLs.Count>0)
        {
            //遍历开启列表，找到消费最小的点作为检查点
            Cell cur = openLs[0];
            for (int i = 0; i < openLs.Count; i++)
            {
                if(openLs[i].fCost<cur.fCost&&openLs[i].hCost<cur.hCost)
                {
                    cur = openLs[i];
                }
            }
            Debug.Log("当前检查点：" + cur.ToString()+" 编号："+showFindNum+"  open列表节点数量："+openLs.Count);
            //显示在界面，和A*算法无关
            cur.obj.transform.Find("Num").GetComponent<Text>().text=showFindNum.ToString();
            showFindNum++;

            //从开启列表中删除检查点，把它加入到一个“关闭列表”，列表中保存所有不需要再次检查的方格。
            openLs.Remove(cur);
            closeLs.Add(cur);

            //检查是否找到终点
            if(cur==endCell)
            {
                Debug.Log("寻路结束!");
                grid.CreatePath(cur);
                return;
            }

            //根据检查点来找到周围可行走的点
            //1.如果是墙或者在关闭列表中则跳过
            //2.如果点不在开启列表中则添加
            //3.如果点在开启列表中且当前的总花费比之前的总花费小，则更新该点信息
            List<Cell> aroundCells = GetAllAroundCells(cur);
            foreach (var cell in aroundCells)
            {
                
                if (cell.isWall || closeLs.Contains(cell))
                    continue;

                int cost= cur.gCost+ GetDistanceCost(cell, cur);

                if(cost<cell.gCost||!openLs.Contains(cell))
                {
                    cell.gCost = cost;
                    cell.hCost = GetDistanceCost(cell,endCell);
                    cell.parent = cur;
                    Debug.Log("cell:" + cell.ToString() + "  parent:" + cur.ToString() + "  " + cell.PrintCost());
                    if(!openLs.Contains(cell))
                    {
                        openLs.Add(cell);
                    }

                    //显示在界面，和A*算法无关
                    cell.obj.transform.Find("Cost").GetComponent<Text>().text = cell.fCost.ToString();
                }


            }

        }

        Debug.Log("寻路失败!");
    }
```
根据上面的工程得到这个图：
  
{{< image src ="https://cdn.jsdelivr.net/gh/codingriver/cdn/20181019163900234.png" >}}

  
圆点说明：黑色是障碍物体，红色是起点，绿色是终点，浅紫色是寻路路径
红色数字：总花费F
蓝色数字：寻路的过程描述

过程描述：
+ 将起点（3，6）放到open列表中。
+ 选择open列表中花费最小的点M（3，6）,将M从open中移除，添加到closed列表中，后面检查时不再检查该点。
+ 计算（3，6）相邻的点，一共8个点，并且分别计算花费F（红色数字），都添加到open中
  
 {{< image src ="https://cdn.jsdelivr.net/gh/codingriver/cdn/20181019172657745.png" >}}  
+ 选择open列表中花费最小的点M（4，6）,将M从open中移除，添加到closed列表中，后面检查时不再检查该点。
+ 计算（4，6）相邻的点，一共8个点，右侧是障碍物，其它5个点都在open中，分别计算当前路径花费和原来对比，都大，所以没有更新花费和父节点
+ 选择open列表中花费最小的点M（4，5）,将M从open中移除，添加到closed列表中，后面检查时不再检查该点。
+ 计算M相邻的点，在下面有三个新节点添加open中，其它五个点要么是障碍要么是已经在open中且花费比原来大，
  
 {{< image src ="https://cdn.jsdelivr.net/gh/codingriver/cdn/20181019173445990.png" >}}  

+ 选择open列表中花费最小的点M（4，7）,将M从open中移除，添加到closed列表中，后面检查时不再检查该点。
+ 计算M相邻的点，在上面有三个新节点添加open中，其它五个点要么是障碍要么是已经在open中且花费比原来大，
  
 {{< image src ="https://cdn.jsdelivr.net/gh/codingriver/cdn/20181019173546409.png" >}}  
+ 选择open列表中花费最小的点M（3，5）,将M从open中移除，添加到closed列表中，后面检查时不再检查该点。
+ 计算M相邻的点，在左下有一个新节点添加open中，在正下面有一个点（3，4）的花费比原来小，更新该节点信息，其它的点已经在open中且花费比原来大，
  
 {{< image src ="https://cdn.jsdelivr.net/gh/codingriver/cdn/20181019173902618.png" >}}  
+ 选择open列表中花费最小的点M（3，7）,将M从open中移除，添加到closed列表中，后面检查时不再检查该点。
+ 计算M相邻的点，在左下有一个新节点添加open中，在正下面有一个点（3，8）的花费比原来小，更新该节点信息，其它的点已经在open中且花费比原来大，
  
 {{< image src ="https://cdn.jsdelivr.net/gh/codingriver/cdn/20181019174002852.png" >}}  

+ 选择open列表中花费最小的点M（5，4）,将M从open中移除，添加到closed列表中，后面检查时不再检查该点。
+ 计算M相邻的点，有五个新节点添加open中，其它三个点要么是障碍要么是已经在open中且花费比原来大，
  
 {{< image src ="https://cdn.jsdelivr.net/gh/codingriver/cdn/20181019174210851.png" >}}  
+ 选择open列表中花费最小的点M（5，8）,将M从open中移除，添加到closed列表中，后面检查时不再检查该点。
+ 计算M相邻的点，有五个新节点添加open中，其它三个点要么是障碍要么是已经在open中且花费比原来大，
  
 {{< image src ="https://cdn.jsdelivr.net/gh/codingriver/cdn/2018101917430594.png" >}}  
+ 选择open列表中花费最小的点M（6，5）,将M从open中移除，添加到closed列表中，后面检查时不再检查该点。
+ 计算M相邻的点，有四个新节点添加open中，其它四个点要么是障碍要么是已经在open中且花费比原来大或者相等，
  
 {{< image src ="https://cdn.jsdelivr.net/gh/codingriver/cdn/20181019174416470.png" >}}  
+ 选择open列表中花费最小的点M（6，7）,将M从open中移除，添加到closed列表中，后面检查时不再检查该点。
+ 计算M相邻的点，有两个新节点添加open中，其它六个点要么是障碍要么是已经在open中且花费比原来大或者相等，
  
 {{< image src ="https://cdn.jsdelivr.net/gh/codingriver/cdn/20181019174606521.png" >}}  

+ 选择open列表中花费最小的点M（7，6）,将M从open中移除，添加到closed列表中，和终点对比相等，寻路结束。
  
 {{< image src ="https://cdn.jsdelivr.net/gh/codingriver/cdn/20181019174750658.png" >}}  

**根据当前代码寻路有个情况就是寻路到终点前临近终点时，可以提前一步结束，这里没有结束，是为了方便演示**

> 参考文章：
> [A*算法完全理解](https://www.cnblogs.com/chxer/p/4542068.html)
> [堪称最好最全的A*算法详解（译文）](https://blog.csdn.net/denghecsdn/article/details/78778769)
> [A星寻路算法介绍](https://www.cnblogs.com/zhoug2020/p/3468167.html)
> 这里的unity工程是参考一篇文章的，是两年前的文章，没有找到，就不放参考链接了