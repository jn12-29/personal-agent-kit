# Implementing Research Code from Papers

## 目标

把论文、appendix、supplement 或官方实现中的方法准确映射到代码，同时明确真正影响实验语义的不确定项。

## 1. 先确定任务来源

实现要求可能来自：

- 用户明确说明；
- paper main text；
- appendix / supplement；
- official code；
- existing codebase；
- author-provided material。

用户明确要求做 ablation、变体或偏离原论文时，以用户要求的实验为目标，不要因为论文不同而自行改回原方法。

## 2. 对照已有代码

如果项目已经有：

- model wrapper；
- dataset pipeline；
- evaluator；
- config；
- baseline；
- shared utilities；

优先把论文方法映射到现有结构。

不要默认重新实现完整训练或评估框架。

## 3. 逐步映射方法

从论文中明确：

```text
inputs
intermediate variables
equations / operations
normalization
indexing
masking
aggregation
loss
training procedure
inference procedure
evaluation
```

把这些概念对应到实际 tensor 和代码阶段。

特别检查：

- tensor shape；
- batch / sequence / head / feature dimension；
- softmax / normalization dimension；
- reduction dimension；
- padding；
- causal mask；
- indexing convention；
- detach / gradient flow；
- train/eval mode；
- dtype；
- numerical tolerance。

## 4. 保留论文术语

如果论文有稳定术语，代码中的函数、变量和注释尽量沿用这些术语。

这样研究者能从 paper 概念直接定位到 implementation。

不要为了通用工程命名，把 method-specific 概念全部改成抽象的 `processor`、`handler`、`strategy`。

## 5. 处理论文没有写清楚的细节

论文经常不会完整说明 implementation detail。

区分：

- 文中明确规定；
- official code 明确体现；
- 可从当前 codebase 直接确定；
- 需要合理推断；
- 会改变研究语义的重要假设。

普通实现细节可以按项目惯例合理处理。

真正会影响实验定义或结果解释的不确定项，应明确记录，而不是静默选择。

例如：

```text
normalization before or after aggregation
which tokens are included in the denominator
whether gradients pass through selection
how ties are resolved
```

## 6. 不要过度记录无关 ambiguity

不要把每个变量名、默认 dtype、目录名都升级成“论文假设”。

只有可能影响：

- algorithm semantics；
- training objective；
- evaluation；
- result comparison；

的不确定项才需要显式说明。

## 7. Official code

存在 official code 时，它通常是重要参考，但不能机械认为所有实现细节都是论文定义本身。

检查：

- code revision；
- config；
- default parameters；
- evaluation script；
- issue / branch 是否与论文版本对应。

当 paper 与 official code 不一致时，不要静默混合两者。按当前任务目标选择，并说明影响实验语义的差异。

## 8. 实现 reference path

对于复杂优化或系统实现，如果存在简单直接版本，保留或先实现 reference path 往往有价值。

例如：

```text
full recompute
vs
optimized partial recompute
```

reference path 可以用于：

- correctness comparison；
- debugging；
- ablation；
- backend parity。

但不要为了形式完整保留永远不会使用的双实现。

## 9. 验证

论文实现最有价值的验证通常是：

- equation-level sanity check；
- tiny tensor 手工可解释 case；
- reference implementation parity；
- official implementation parity；
- full vs optimized path；
- output / gradient parity；
- paper-reported small example；
- real-model smoke run。

是否建立长期维护的 test 参考 `testing.md`。

## 10. 交付

说明：

- 实现对应论文哪一部分；
- 使用了哪些现有项目接口；
- 哪些行为是论文明确规定的；
- 是否存在会影响实验语义的推断或偏离；
- 实际运行了哪些验证；
- 如何运行该方法或实验。
