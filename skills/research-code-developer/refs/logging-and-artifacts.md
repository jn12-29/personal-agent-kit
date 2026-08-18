# Logging and Artifacts for Research Code

## 目标

让实验结果能够回答：

> 这个结果是由什么模型、数据、方法、配置和代码条件产生的？

Logging、config、checkpoint、cache 和结果 artifact 是科研代码的一部分，但不需要复制 production observability system。

## 1. Run identity

一个正式实验通常应能追踪以下信息中的相关部分：

```text
experiment / run name
timestamp
git revision
command
resolved config
model
dataset / split
method
seed
checkpoint
backend / dtype
output directory
```

不是所有实验都必须记录所有字段。只记录影响解释、比较和复现的条件。

## 2. Resolved config

优先保存**实际生效的 config**，而不是只保存用户输入的部分参数。

原因：

- defaults 可能影响结果；
- inheritance / override 后的值才是真实条件；
- 之后分析需要知道最终使用了什么。

对于正式实验，建议将 resolved config 与结果放在同一 run directory 或建立明确关联。

## 3. Training logs

根据任务记录真正有研究价值的训练状态，例如：

```text
step / epoch
train loss
validation metric
learning rate
gradient norm
throughput
memory
```

不要为了“日志完整”无脑记录所有 optimizer state、每层统计或大量 tensor。

关键问题是：

> 之后是否能够判断训练是否正常，以及不同 run 为什么不同？

## 4. Evaluation logs

评估结果至少要能对应：

- dataset / split；
- model / checkpoint；
- method；
- metric；
- sample count；
- 影响 metric 的关键配置。

如果存在多 dataset / model / method，使用统一字段，方便后续 aggregation。

不要只打印：

```text
accuracy = 0.783
```

而没有任何运行上下文。

## 5. Human-readable 与 machine-readable

终端输出适合：

- progress；
- 当前 loss；
- 当前 metric；
- warning；
- run path。

长期结果适合保存为：

- JSON；
- JSONL；
- CSV；
- Parquet；
- structured YAML；
- experiment tracker 的结构化记录。

后续需要程序化比较和画图的值，不要只保存在日志文本中。

## 6. Checkpoint

Checkpoint 策略由训练成本和研究需求决定。

常见需求：

- latest；
- best by metric；
- fixed interval；
- milestone；
- final。

不要默认高频保存所有 checkpoint。

Checkpoint 应能关联到：

- run/config；
- training step；
- model state；
- 必要时 optimizer / scheduler state；
- 与 resume 相关的其他 state。

如果 checkpoint 只用于 inference，可以只保存真正需要的内容。

## 7. Resume

Resume 功能只需要支持实际训练流程。

重点检查：

- 是否恢复了正确 run；
- step / epoch 是否一致；
- optimizer / scheduler 是否按需要恢复；
- config 是否发生影响语义的变化；
- 新日志是否与旧 run 正确衔接。

不要默认实现复杂 migration 或跨多个历史格式兼容。

## 8. Artifact

常见 artifact：

- generated outputs；
- embeddings；
- KV；
- predictions；
- metrics；
- checkpoints；
- intermediate statistics；
- figures；
- tables。

正式结果应有明确来源，不要让最终 figure 依赖无法定位的临时文件。

如果 artifact 生成昂贵或不可重建，应提高：

- provenance；
- integrity check；
- cache identity；
- metadata；

的要求。

## 9. Cache

Cache key 必须表达所有会改变 cache 语义的输入。

例如 generation cache 可能需要考虑：

```text
model / checkpoint
prompt / document
query
method
generation config
seed
tokenization-relevant config
```

具体字段取决于实际语义。

最危险的问题不是 cache miss，而是**合法读取了错误条件下生成的结果**。

对于昂贵且跨实验复用的 cache，应优先保护 semantic identity 和 provenance，而不是为所有 filesystem corner case 建立复杂协议。

## 10. Directory layout

目录结构应让人可以快速找到：

```text
config
logs
metrics
checkpoints
artifacts
figures
```

可以采用类似：

```text
runs/
  <run>/
    config.yaml
    metrics.jsonl
    checkpoints/
    artifacts/
    figures/
```

但不强制统一模板。项目已有清楚结构时继续使用。

不要为了目录“规范”引入大量 manager、schema 和 migration code。

## 11. Naming

命名优先满足：

- 人能看懂；
- 程序能稳定解析需要的字段；
- 不与真实 experimental axis 冲突。

不要把所有实验信息塞进一个超长文件名。更复杂的 metadata 应进入 config/result file。

## 12. Logging library

可以使用：

- Python logging；
- TensorBoard；
- Weights & Biases；
- MLflow；
- 项目已有 logger；
- 简单 JSONL writer。

优先复用项目已有方案。除非任务确实需要，不要为了日志单独引入大型依赖。

## 13. 避免两种极端

不要：

- 只有终端 print，实验结束后无法追踪；
- 把每个 tensor、每个函数调用、每个系统事件都永久记录。

原则：

> 保存解释和复现实验所需的信息，同时保持日志可读、artifact 可管理。
