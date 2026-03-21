# Unity渲染顺序

Unity中的渲染顺序有三层：
+ **第一层：Camera的depth，值越大渲染越在前面**
+ **第二层：Sorting Layer，配置SortingLayer面板（越在下面的layer渲染越在前面），然后在Canvas上设置或者在Renderer组件上设置**
+ **第三层:SortingOrder,值越大越在前面渲染，然后在Canvas上设置或者在Renderer组件上设置**
*决定渲染顺序:第一层>第二层和第三层*


[render1.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-798cee6f38385334.png)
![render2.png](https://cdn.jsdelivr.net/gh/codingriver/cdn/texs/1095643-3da8b646958023e6.png)


## 相机渲染顺序

　　相机的渲染顺序，由Camera的Depth参数控制

##  RenderQueue

　　Queue分为五个队列：

　　　　Background，天空盒，天生用来被覆盖的（1000）

　　　　Geometry，不透明物渲染队列（2000）

　　　　AlphaTest，通道测试的几何体使用这个队列，这些物体的渲染有点介于Opaue与Transparent之间（2450）

　　　　Geometrylast，特殊的点，定义了透明与不透明的分界点（2500），属于不透明队列

　　　　Transparent，不写深度的物体，一般是透明物或粒子效果（3000）

　　　　Overlay，最后渲染的内容，天生覆盖别人的，如UI（4000）

##  RenderQueue与SortingLayer与Order之间的关系

1. `Queue > 2500` 的物体绝对会在 `Queue <= 2500` 之后渲染，这时`Layer`、`Order`将完全不起作用
2. `Queue` 位于1中的同一侧时，`Layer`低的先渲染，无视`Queue`与`Order`值

3. `Queue` 位于1中的同一侧时，`Layer` 相同，`Order` 低的先渲染，无视 `Queue`

4. `Layer`与`Order`都一样时，`Queue` 低的先渲染

## Opaque调整SortingLayer，SortingOrder为什么没作用？

　　因为不透明物体是打开ZWrite的，即使改了SortingLayer与Order，让一个本来在后边（Z值大）的物体先渲染了，但是另一个物体渲染时

　　　　由于Z值小，写深度以后，立马把前边的物体覆盖了，结果总是一样的；透明物渲染时，关闭了ZWrite，渲染的结果不是替换的，是

　　　　混合的，所以先渲染后渲染，结果就可能会不同（与混合的方式有关）

## 总结
> `Geometry`不透明队列是`RenderQueue<=2500`的  
> `Transparent`透明队列是`RenderQueue>2500`的  
1. 如果两个物体分别属于 `Geometry`不透明队列 和 `Transparent`透明队列，则`Sorting Layer` 和 `Order in Layer` 怎么设置都是不起作用的 (Z值是最后决定前后关系的)
2. 如果两个物体都在`Geometry`不透明队列 或者都属于 `Transparent`透明队列，则
在`Sorting Layer`高的绝对会在`Sorting Layer`前面，无视`RenderQueue`跟`Order in Layer`，只有在`Sorting Layer`相同的前提下，`Order in Layer`高的会在`Order in Layer`低的前面，无视`RenderQueue`。当`Sorting Layer`跟`Order in Layer`相同时，才看`RenderQueue`的高低，高的在前面。（假设ZWrite和ZTest关闭）  
*简要概括：物体属于同一队列则`Layer`比`Queue`优先*

>如果要测试，则使用`Transparent`透明队列测试，且把shader的深度写入和深度测试关闭
>参考：  
> <https://www.cnblogs.com/hiker-online/p/12489252.html>  
