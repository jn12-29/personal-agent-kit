# End-to-End Experiment Workflow

## 适用范围

仅当任务要求从研究需求一路完成到实验运行、结果检查或分析时使用。

普通局部代码修改不需要执行完整流程。

## 1. 明确研究问题

先确认：

- 要验证什么 hypothesis 或 claim；
- baseline 是什么；
- 哪些量是变化因素；
- 哪些条件应保持一致；
- 使用什么 metric；
- 什么结果能够回答当前问题。

不要自行把“实现一个方法”扩展成新的研究方向。

## 2. 阅读现有代码

先找到实际执行路径：

```text
entry point
config
data loading
model construction
method implementation
training / inference loop
evaluation
logging
artifact output
```

优先复用已有运行方式和抽象，不要先写一套平行 pipeline。

## 3. 设计实验结构

如果存在多个：

```text
models × datasets × methods × seeds
```

先整体规划接口、config 和结果格式。

先设计不等于一次实现全部实验基础设施。应先确定能够贯通真实输入、方法执行、评估和结果输出的最小可工作切片以及后续扩展位置，实现并验证这个切片后，再在保持可运行的前提下逐层加入其他组合。

明确：

- baseline；
- new method；
- ablation；
- shared settings；
- run matrix；
- artifact location。

需要时读取 `research-architecture.md`。

## 4. 实现

保持研究概念和代码路径清楚。

如果实现需要影响多个公共组件，可以在当前实验需求范围内做必要重构，不机械追求最小 diff。

如果需要根据论文实现，读取 `paper-to-code.md`。

## 5. 代码级验证

先使用低成本验证：

- import / syntax；
- tiny input；
- one batch；
- one forward；
- few training steps；
- small dataset subset；
- direct output inspection；
- relevant runtime assertions。

只有存在明确长期价值时才新增长期维护的 test。

## 6. 建立 baseline

如果任务涉及比较，确保 baseline 能以当前代码和当前环境正常运行，并留下：

- config；
- metric；
- output；
- 必要日志。

不要在 new method 和 baseline 使用不同 evaluation semantics，除非研究设计明确要求。

## 7. 运行实验

根据资源和任务范围选择合理规模。

正式运行前确认：

- run config 已保存；
- output path 明确；
- checkpoint / cache 行为符合当前任务；
- training/evaluation log 足以发现明显异常。

不要因为有 GPU 就自动扩大 sweep。

## 8. 监控

运行中主要检查：

- loss / metric 是否合理；
- NaN / Inf；
- gradient 是否异常；
- throughput / memory 是否异常；
- output 是否写到正确位置；
- config / checkpoint 是否正确。

不要把一次随机波动自动解释成实现 bug。

## 9. 分析结果

结果分析时区分：

- implementation behavior；
- experimental observation；
- scientific interpretation。

例如：

```text
code path executes correctly
```

不等于：

```text
method is effective
```

一次运行结果也不自动说明稳定趋势。

## 10. 迭代

如果实验用于比较具体改动，尽量让对比条件清楚。

适合时采用：

```text
baseline
→ one controlled change
→ run
→ inspect
→ record
```

但如果研究问题本身要求多个联动变化，不要机械坚持“一次只能改一个变量”。

## 11. 结果交付

至少说明：

- 实现了什么；
- 运行了什么；
- 使用了什么主要配置；
- 得到了什么结果；
- 哪些结果只是初步观察；
- 哪些部分尚未验证；
- 结果和 artifact 在哪里。

不要把代码实现完成、实验运行完成和研究结论成立混为一个状态。
