# DrawCall优化实战

> 世界地图合批优化实战分享草稿。

# 世界地图合批的优化实战

## 基本概念

参考：

- <https://zhuanlan.zhihu.com/p/356211912>
- <https://zhuanlan.zhihu.com/p/651364842>
- <https://zhuanlan.zhihu.com/p/432223843>
- <https://blog.csdn.net/qq_33726878/article/details/119863710>

### 什么是 Draw Call

在 Unity 中，每次 CPU 准备数据并通知 GPU 的过程就称之为一个 Draw Call。这个过程会指定一个 Mesh 被渲染、绘制材质。

### 为什么 Draw Call 多了会影响帧率

- Draw Call 是 CPU 告诉 GPU 需要绘制什么的命令
- 每次发出一个 Draw Call，CPU 都需要做设置渲染状态、准备数据、调用图形 API 等工作
- 当 Draw Call 数量增加时，CPU 处理量上升，可能成为性能瓶颈
- GPU 端也会因为图形管线执行次数增加而承担更多负载

### Draw Call、Batcher、Set Pass Call

- `Draw Call`：CPU 向 GPU 提交绘制数据的次数
- `Batcher`：经过打包之后的 Draw Call
- `Set Pass Call`：材质或 Pass 切换带来的状态设置成本，往往比单纯的 Draw Call 更能反映 CPU 开销

## 合批优化常见方法

- 合并网格和材质
- 使用共享材质
- 使用 `MaterialPropertyBlock`
- Static Batching 静态批处理
- Dynamic Batching 动态批处理
- GPU Instancing
- SRP Batcher
- 打包图集 / 动态图集
- 使用光照贴图
- 使用 LOD
- 使用 Culling 技术

### Static Batching

适用于不会移动的静态物体。优点是减少状态切换，缺点是会增加包体和内存占用。

### Dynamic Batching

适用于顶点数较低、材质一致的小型动态物体。它会带来一定 CPU 额外开销，因此并不是越多越好。

### GPU Instancing

适用于相同网格和材质的大量实例。允许通过 `MaterialPropertyBlock` 为不同实例设置差异化属性。

### SRP Batcher

- 着色器必须兼容 SRP Batcher
- 不支持用 `MaterialPropertyBlock` 修改导致不兼容的属性
- 适合 URP / HDRP / SRP 环境下的渲染批处理优化

## 迁移说明

原文为超长草稿，当前先迁移了主体结构与关键结论，后续可继续细化：

- OpenGL 渲染状态说明
- Draw Call CPU 开销详细分析
- Static / Dynamic / Instancing 的适用边界
- 遮挡剔除与视锥剔除的实践案例
