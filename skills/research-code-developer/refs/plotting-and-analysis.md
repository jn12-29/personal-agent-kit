# Plotting and Result Analysis

## 目标

让实验结果的聚合、统计、表格和可视化清楚表达真实数据与研究定义，同时避免把 presentation 细节永久化成无价值的代码 contract。

## 1. 分离原始结果与展示

优先流程：

```text
raw / structured experiment results
→ aggregation / analysis
→ table / figure
```

不要让 plotting script 自己重新运行实验、重新定义 metric 或从不透明日志中猜数据。

## 2. 结构化结果

多 model / dataset / method 实验使用统一字段，例如：

```text
model
dataset
method
seed
metric
value
checkpoint
config identity
```

这样 aggregation 和 plotting 不需要为每个组合写独立逻辑。

## 3. 明确 metric 语义

分析代码必须清楚处理数据和评估流程中实际可能出现、且会影响 metric 语义的情况，例如：

- denominator；
- averaging；
- weighting；
- missing values；
- failed runs；
- duplicate runs；
- seed aggregation；
- confidence interval / error bar；
- dataset split。

这些情况存在时，相关处理会影响研究结论，应比颜色、marker 和 legend 位置更受重视；不存在时，不要为了形式完整增加无关逻辑。

## 4. 不要在 plot 中隐藏数据处理

避免：

```text
load
→ silently filter
→ silently drop NaN
→ silently average
→ plot
```

重要过滤和 aggregation 应使用明确函数或中间 table，使研究者可以检查。

## 5. 多模型、多方法、多数据集

当 figure 需要系统展示多个实验维度时，统一：

- result schema；
- display-name mapping；
- ordering；
- grouping；
- aggregation。

不要为每个 figure 复制一套数据读取和 metric 计算。

但也不要为了几张简单图建立庞大的 visualization framework。

## 6. Figure code

Paper figure 通常值得：

- 可重复生成；
- 固定输入；
- 清楚保存输出；
- 记录生成命令；
- 使用统一 style helper，如果确实有多图共享需求。

不需要永久 test：

- exact color；
- marker；
- legend order；
- output filename；
- glyph 数量；
- layout 常量；

除非这些内容本身是稳定的外部 contract。

## 7. Visual review

Figure 的很多问题最适合人工检查：

- label 是否遮挡；
- 字号是否可读；
- legend 是否合理；
- 数据是否明显错位；
- 颜色和线型是否容易区分。

生成最终 figure 后应实际查看，而不是试图用大量 unit tests 替代视觉检查。

## 8. 分析脚本可调试性

保留中间 dataframe / table 或允许导出，使研究者能检查：

```text
raw rows
filtered rows
grouped values
final plotted values
```

不要让一个超长 plotting function 同时负责 loading、filtering、statistics 和 rendering。

## 9. 可视化中间研究量

对于 attention、activation、token selection、error cases 等研究性图形：

- 原始中间量由模型或 debug interface 提供；
- analysis code 负责转换和绘图；
- 不要把 plotting 逻辑硬编码进核心 forward path。

需要观察接口时参考 `debugging-and-observability.md`。

## 10. 保存最终结果

正式 table / figure 应能追踪到：

- 输入 result files；
- aggregation config；
- code revision；
- 生成命令或 script。

不必建立复杂 artifact management system，但最终论文结果不应依赖无法定位的手工步骤。
