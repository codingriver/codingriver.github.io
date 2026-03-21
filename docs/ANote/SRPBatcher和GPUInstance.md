# SRPBatcher和GPUInstance

## GPU Instancing（unity内置渲染管线）
>`GPU Instancing` 是对相同mesh的多份实例进行处理，例如树和草等  
> `instanceID`:语义 `SV_InstanceID`，类型 `uint`,实例对应的数组索引。当启用实例化时，我们现在可以访问顶点程序中的实例 ID。有了它，我们可以在变换顶点位置时使用正确的矩阵。但是，UnityObjectToClipPos没有矩阵参数。它总是使用unity_ObjectToWorld. 为了解决这个问题，UnityInstancing包含unity_ObjectToWorld使用矩阵数组的宏覆盖文件。这可以被认为是一个肮脏的宏黑客，但它无需更改现有着色器代码即可工作，从而确保向后兼容性。（在使用实例化渲染调用时，gl_InstanceID会从0开始，在每个实例被渲染时递增1。比如说，我们正在渲染第43个实例，那么顶点着色器中它的gl_InstanceID将会是42。因为每个实例都有唯一的ID，我们可以建立一个数组，将ID与位置值对应起来，将每个实例放置在世界的不同位置。）  
> 教程：[(Jasper Flick) GPU Instancing](https://catlikecoding.com/unity/tutorials/rendering/part-19/)  
> `Jasper Flick`详细说明了原理及 `lod_fade`对GPU Instancing的支持

简要概括：**cpu将相同mesh的物体相且相同材质球每次次最大化数量提交到GPU,额外增加untiy_ObjectToWorld[]数组，及不同的颜色数组（如果有），顶点属性（instanceID）等等信息，减少了SetPassCall，实际GPU的DrawCall没有减少**。

条件：
- 相同mesh的物体
- 相同材质球  (可以使用共享材质球)

*支持使用`MaterialPropertyBlock`修改*

## SRP Batcher（SRP 自定义渲染管线）

>教程：[(Jasper Flick)SRP Batcher](https://catlikecoding.com/unity/tutorials/custom-srp/draw-calls/)  
>这里教程说明了SRP Batcher在2.1节，GPU Instancing（SRP渲染管线） 在2.3节

将属性写在 UnityPerMaterial 和 UnityPerDraw 中

条件：
- 相同Shader（允许不同材质球，不同mesh）
- 相同Shader的Keywords(变体)
- 对象不可以是粒子或蒙皮网格
- 位置不相邻且中间夹杂不同的Shader或不同的变体的其他物体，不会同批处理（可以调整Queue来避免该情况）

*不支持使用 ~~MaterialPropertyBlock~~ 修改，使用 MaterialPropertyBlock 对属性进行更改之后，不再合并,然后转到GPUIn stancing，如果支持的话。*  

## SRP Batcher & GPU instancing的不同点和相同点
>优先级顺序： SRP Batcher > Static Batching > GPU Instancing > Dynamic Batching

|-|Static Batching|Dynamic Batching|GPU Instancing| SRP Batcher|
|-|-|-|-|-|
|优点|限制少|自动无需处理|性能极好|多材质加速|
|缺点|增加包体大小<br>增加运行时内存|增加运行时CPU消耗<br>限制多|限制多|只能用于SRP中|
|适用场景|静态场景<br>`不适合`大量重复物体|小物体、特效等|大量重复物体|较为广泛|

> 参考：[https://www.jianshu.com/p/f2a7e9ed9b89](https://www.jianshu.com/p/f2a7e9ed9b89)  
>[(Unity Doc) GPU Instancing](https://docs.unity3d.com/Manual/GPUInstancing.html)
> [(Unity Doc) SRP Batcher](https://docs.unity3d.com/cn/2019.4/Manual/SRPBatcher.html)  


