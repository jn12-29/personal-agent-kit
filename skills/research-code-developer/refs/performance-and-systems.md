# Performance and Systems Work in Research Code

## 目标

在不混淆研究语义的前提下进行 GPU、memory、throughput、latency、kernel、distributed 和系统级优化。

## 1. 先明确优化目标

区分：

- latency；
- throughput；
- peak memory；
- total memory；
- GPU utilization；
- communication；
- data loading；
- preprocessing；
- kernel time；
- end-to-end runtime。

不要只因为代码“看起来慢”就开始大规模优化。

## 2. 测量真实瓶颈

优先使用 profiler 或代表性 workload。

检查：

```text
compute
memory bandwidth
CPU-GPU transfer
synchronization
kernel launch
data loading
communication
serialization
```

不要通过复杂架构推断替代实际 profiling。

## 3. 保持研究语义

优化时重点确认是否改变：

- numerical behavior；
- precision；
- reduction order；
- mask；
- sampling；
- batching semantics；
- gradient；
- cache behavior；
- evaluation output。

性能更快不等于研究实现仍然相同。

## 4. Reference path

当 optimized path 复杂、容易出现 silent numerical error 时，保留简单 reference path 往往有价值。

典型：

```text
PyTorch reference vs custom kernel
full attention vs sparse/partial path
eager vs compiled
single-GPU reference vs distributed path
```

必要时做 output / gradient parity。

是否长期保留 test 由 `testing.md` 判断。

## 5. Memory optimization

处理：

- activation；
- KV cache；
- optimizer state；
- temporary buffer；
- batch size；
- checkpointing；
- offload；

时，应区分：

- 只是减少 memory；
- 是否改变计算；
- 是否改变 gradient；
- 是否改变 sequence / batch composition。

记录会影响实验比较的设置。

## 6. Mixed precision

使用 FP16、BF16、FP8 或其他低精度时：

- 明确哪些部分使用低精度；
- 关注 loss / gradient stability；
- 对数值敏感路径必要时保留更高精度；
- 比较方法时保持 precision policy 一致，除非 precision 本身就是实验变量。

## 7. Compilation 和 fused path

使用：

- `torch.compile`；
- Triton；
- custom CUDA；
- fused kernel；

时，优先保留一个能够独立验证语义的直接实现，至少在开发阶段如此。

不要把所有逻辑一开始就融合到难以观察的 kernel 中。

## 8. Distributed

只有实际实验需要时才增加 distributed complexity。

系统化设计：

- data / tensor / pipeline parallel；
- process launch；
- seed；
- logging；
- checkpoint；
- aggregation。

不要为了未来可能使用多机而提前实现完整 distributed abstraction。

## 9. Benchmark

性能 benchmark 需要说明：

- hardware；
- model；
- dtype；
- batch / sequence；
- warmup；
- measurement window；
- synchronization；
- memory measurement definition。

不要比较不一致 workload。

## 10. 优化后的研究可调试性

性能优化不应完全消灭 debug path。

需要时保留：

- disable optimized path 的开关；
- reference implementation；
- intermediate check；
- profiling entry point。

这样可以在性能和研究分析之间切换，而不是把系统变成只能跑 benchmark 的黑盒。
