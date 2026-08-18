# Research Code Architecture

## 目标

为真实实验结构设计清楚、可扩展、易修改的代码组织。framework 可以简单，也可以复杂；关键是其复杂度能够由研究需求解释，并且不会遮蔽研究逻辑。

## 1. 先识别实验结构

当任务涉及系统化实验时，先列出真实变化维度，例如：

```text
model
dataset
method
task
seed
metric
loss
backend
checkpoint
hyperparameter
```

再判断：

- 哪些维度会组合；
- 哪些维度共享执行流程；
- 哪些差异只是参数；
- 哪些差异需要不同实现；
- 哪些结果需要统一比较；
- 哪些中间状态需要共同观察。

开始实现前，先基于当前已知需求完成足够完整的架构构思：明确实验维度、职责边界、共享路径、变化点，以及能够贯通真实输入、核心计算和结果输出的最小可工作端到端切片。

实现从这个最小切片开始，并始终保持它可运行；后续 model、dataset、method、metric 或 backend 在既有结构上逐层加入。逐层生长不是先无设计地写一批组合脚本、等形成重复后再事后抽象，也不是一次性实现所有未来能力。设计应覆盖当前已知结构和明确扩展方向，代码只实现当前需要的最小完整层。

## 2. 抽象应表达研究概念

优先围绕研究中的真实概念建立接口，例如：

```python
result = evaluate(
    model=model,
    dataset=dataset,
    method=method,
    config=config,
)
```

这比围绕偶然的实现重复建立抽象更有价值。

如果两段代码只是暂时共享几行 tensor 操作，不必立即抽成公共接口。只有当共同逻辑具有稳定含义、会持续复用，或单独抽出后明显降低理解成本时再抽象。

## 3. framework 何时合理

以下情况通常适合建立统一 framework：

- 多个 model / dataset / method 会系统组合；
- 需要统一训练、评估、日志和 artifact 管理；
- 新 baseline、ablation 或 metric 会持续加入；
- 多个执行路径共享大量真实逻辑；
- 需要批量运行、比较和聚合实验；
- 需要为不同实现暴露一致的观察点或干预点。

framework 不是为了“更工程化”，而是为了使实验结构显式、减少结构性重复并降低扩展成本。

## 4. framework 复杂度

允许使用：

- registry；
- interface；
- adapter；
- runner；
- evaluator；
- config system；
- callback / hook；
- plugin-like extension；
- class hierarchy。

但每一层都应有明确用途。

避免：

- 只为两个简单分支建立多层 factory；
- base class 只提供名字，没有共享 contract；
- wrapper 层层转发同一组参数；
- 为尚不存在的 backend、remote execution、distributed mode 预先设计大量接口；
- 为了消除少量重复，把直接可读的算法流程拆得难以追踪。

判断标准：

> 抽象后，研究者是否更容易理解实验结构、增加实验和定位实现？

如果答案是否定的，应简化。

## 5. 保持研究逻辑直接可读

如果研究方法描述的是：

```text
score
→ select
→ compress
→ decode
```

代码最好也保留类似结构：

```python
scores = compute_scores(...)
selected = select_tokens(scores, ...)
kv = build_compressed_kv(..., selected)
output = decode(..., kv)
```

可以在外围使用 framework，但关键算法路径不要被无意义的 orchestration 层遮蔽。

## 6. Extensibility

面向未来扩展时，优先处理已经存在或明确可预见的变化。

目标是让常见扩展变得局部，例如：

```text
add a method
add a model
add a dataset
add a metric
add an ablation
add a backend
```

新增一个维度时，不应需要复制整条 pipeline 或修改大量无关文件。

但不要为“未来可能有”却没有现实依据的需求提前实现接口。

## 7. Registry、函数与 class 的选择

### 简单映射足够时

优先：

```python
METHODS = {
    "full": full_method,
    "method_a": method_a,
    "method_b": method_b,
}
```

适合：

- method 生命周期简单；
- 主要差异是一个纯函数或局部计算；
- 不需要复杂 state。

### 需要 class 时

当实现具有：

- 持久 state；
- prepare / run / finalize 生命周期；
- 多个相关方法；
- checkpoint 或 resource ownership；
- 需要统一 hook 或 callback；

可以使用 class/interface。

### 需要 adapter 时

只有在不同 model、dataset 或 backend 之间存在稳定的接口差异，并且这些差异会反复出现时使用 adapter。

不要为了形式统一给每个对象都增加 adapter。

## 8. Config

Config 应表达实验选择，而不是隐藏执行逻辑。

推荐：

- model / dataset / method 等实验维度显式；
- 使用 resolved config 记录最终值；
- 公共默认值集中管理；
- 影响实验语义的参数不要散落在脚本常量中。

避免：

- 一个巨大 config 控制大量相互无关的内部细节；
- 用 config flag 代替清楚的代码结构；
- 同一个概念在 CLI、YAML、Python defaults 中各有不同含义。

## 9. Common infrastructure

多个实验共享的基础设施可以统一，例如：

- config loading；
- run directory；
- logging；
- checkpoint；
- result serialization；
- evaluator；
- dataset loading；
- model loading；
- distributed launch。

统一的目标是减少真实重复和实验差异，而不是建立一个通用平台。

## 10. 保留直接路径

framework 应允许：

- 单独运行某一个 stage；
- 构造 tiny case；
- 单独调用一个 method；
- 临时替换某个组件；
- 写 one-off debug / analysis script；
- 绕开批量 runner 做局部验证。

不要要求每个临时研究想法都先注册完整 plugin、schema 或 experiment class。

## 11. 修改现有项目

改已有 research code 时：

1. 先理解当前执行路径和已有抽象；
2. 判断问题是局部实现问题，还是已有结构无法支持新实验；
3. 小改能保持清楚时局部修改；
4. 如果继续打补丁会制造组合爆炸或重复，则在当前需求范围内重构；
5. 重构后检查研究语义和已有实验入口是否仍然清楚。

不要机械追求最小 diff；也不要把一次新实验变成全项目重写的理由。
