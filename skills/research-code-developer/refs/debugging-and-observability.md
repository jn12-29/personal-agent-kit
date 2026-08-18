# Debugging and Observability for Research Code

## 目标

科研代码应便于检查实际计算过程、定位结果异常、观察中间表示、做临时干预和支持可视化分析。

这里的重点不是 production monitoring，而是研究开发中的可观察性和可调试性。

## 1. 让关键中间量可访问

对于影响研究问题的重要量，根据需要提供直接访问方式，例如：

- hidden states；
- attention scores / weights；
- KV；
- selected indices；
- routing decisions；
- intermediate logits；
- loss components；
- gradients；
- masks；
- timing / memory measurements。

不要只留下最终 loss 或 final output，使内部研究行为无法检查。

## 2. 选择合适的暴露方式

根据使用频率和性能成本选择：

### 直接返回

适合少量、稳定、经常使用的辅助结果。

```python
output, aux = model(..., return_aux=True)
```

### Structured auxiliary output

当需要多个有明确含义的中间结果时，可以使用 dict 或 dataclass。

```python
aux = {
    "scores": scores,
    "selected_indices": selected_indices,
}
```

### Hook / callback

适合：

- 不希望改变主返回接口；
- 需要观察多个 layer；
- 可视化或 tracing；
- 临时分析；
- profiling。

### Debug script

适合一次性、局部或强实验性的检查。

不要为了一个临时问题把大量 debug 参数永久塞进主 API。

## 3. 支持实验干预

研究代码常需要：

```text
replace
override
disable
freeze
perturb
ablate
```

如果某个组件明显是研究中的变化点，应避免把它硬编码在不可替换的大函数中。

例如将：

```text
score computation
token selection
KV construction
evaluation
```

拆成清楚的阶段，可以直接替换其中一个阶段，而不复制整个 pipeline。

## 4. Tiny-case debugging

出现异常时，优先构造最小但真实的运行路径：

- small tensor；
- tiny model；
- small batch；
- few tokens；
- one sample；
- one layer；
- one training step；
- one evaluation case。

目标是保留真实 tensor shape、dtype、device 和 library behavior，同时降低调试成本。

不要优先用大量 mock 重建一个与真实运行约束不同的世界。

## 5. 检查实际语义

科研 bug 经常不会 crash。调试时不仅看程序是否运行，还要检查：

- shape 是否符合算法定义；
- mask 是否作用在预期位置；
- normalization 维度是否正确；
- selected indices 是否对应预期 token；
- gradient 是否存在、finite 且到达目标参数；
- metric 输入是否是正确 split / sample；
- cache 是否复用了正确条件下的结果；
- aggregation 是否与研究定义一致。

## 6. Failure locality

让错误尽量在靠近根因的位置暴露。

适合使用简单 runtime assertion 的场景包括：

```python
assert scores.ndim == 3
assert selected_indices.shape[0] == batch_size
assert torch.isfinite(loss)
```

前提是这些 invariant 对当前研究路径真实且稳定。

不要为了每个 assertion 再自动建立永久 unit test。

## 7. 日志和 debug 输出分工

常规日志记录长期有意义的信息。

临时 debug 输出用于定位当前问题，例如：

- 一个 batch 的 token；
- 某层最大/最小 attention；
- 某个 sample 的 indices；
- 特定 tensor slice。

临时 debug 信息不要长期污染标准训练日志。问题解决后应删除、关闭或移动到显式 debug path。

## 8. 可视化支持

如果研究问题需要观察：

- attention pattern；
- activation distribution；
- token selection；
- spatial representation；
- training dynamics；
- error cases；

优先让原始中间结果可稳定导出，然后由 analysis/plotting code 消费。

不要把核心 forward path 和复杂 plotting 逻辑绑在一起。

## 9. Profiling

性能相关异常使用实际 profiling 工具和小规模代表性 workload 检查：

- GPU memory；
- kernel time；
- CPU-GPU transfer；
- data loading；
- synchronization；
- throughput。

不要通过大量手写时间戳替代已有 profiler，除非只需要非常局部的粗略测量。

## 10. Determinism

Debug 时可以固定：

- seed；
- sample；
- batch；
- checkpoint；
- config；

以便复现问题。

但不要因为 debug 方便就默认把整个科研项目强制成完全 deterministic；某些 backend 和训练设置会因此显著降低性能或改变实际运行条件。

## 11. 结束调试后

完成问题定位后：

- 保留真正有长期研究价值的观察接口；
- 删除无意义的 print、临时 dump 和只服务单次问题的复杂分支；
- 已发现且可能静默复发的重要 bug，可根据 `testing.md` 判断是否需要 regression test；
- 将影响实验解释的重要发现记录到日志、配置或文档中。
