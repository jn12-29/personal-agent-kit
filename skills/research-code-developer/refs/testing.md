# Testing Research Code

## 目标

Test 的作用是保护真实、重要且可能逃逸的错误，不是为每次代码修改增加一个形式上的 regression contract。

科研代码中，**不新增 test 可以是正确结论**。

## 1. 先决定是否需要 test

在新增长期维护的 test 前，先回答：

1. 要保护的 behavior 或 invariant 是什么？
2. 具体什么 failure 可能在没有 test 时逃逸？
3. 这个 failure 会怎样影响研究结果、复用接口或重要 artifact？
4. 正确结果是否有可信的 oracle？
5. 被保护行为预计会存在多久？
6. 直接运行、runtime assertion、manual inspection 或 smoke test 为什么不够？
7. test 的运行与维护成本是否合理？

如果无法指出具体 failure，默认不要新增长期维护的 test。

可以用下面的近似关系帮助判断，而不是机械计算：

```text
test value
≈ failure probability
× failure impact
× behavior lifetime
× difficulty of detecting the failure otherwise
× oracle confidence
− implementation and maintenance cost
− execution cost
```

## 2. 验证方式不只有长期维护的 test

根据任务选择最便宜且足够的验证方式：

- no test；
- code inspection；
- type checking / static analysis；
- runtime assertion；
- one-time manual verification；
- smoke test；
- unit test；
- differential / property test；
- integration / E2E test；
- scheduled / nightly test。

一次性验证代码不必自动进入长期 test suite。

如果已经确定需要长期 test，再选择能够完整暴露目标 failure 的最轻层级。Kernel/op 或 component 的输出本身就是被保护的 behavior 时，可以直接测试；只有 failure 来自跨组件交互时，才扩大到 model、service 或 workflow。不要在多个层级重复保护同一 behavior。

## 3. 优先保护科研中难以察觉的错误

高价值 test 通常保护以下问题：

- optimized implementation 与 trusted reference 不一致；
- full / eager path 与 partial / chunked / streaming path 不一致；
- CPU 与 CUDA 或不同 backend 的数值行为异常；
- output parity；
- gradient parity；
- trainable parameter 意外断开计算图；
- semantic cache key collision；
- aggregation、denominator 或 missing-data semantics 错误；
- expensive artifact 的 corruption 或 provenance mismatch；
- 已实际发生过且容易复发的 bug；
- 关键状态转换违反 invariant。

这些错误常常不会 crash，却会静默污染实验结论。

## 4. Oracle 优先级

优先使用：

1. 独立且可信的实现；
2. 更慢但直接、简单的 reference path；
3. 数学或领域 invariant；
4. 已知 bug 的可复现 failure state；
5. 稳定的外部行为 contract；
6. 必要时使用经过审查的 golden output。

避免：

- 把 production implementation 复制一遍来计算 expected value；
- mock 整个核心逻辑后只断言 mock call；
- snapshot 整个内部对象只为了提高 coverage；
- 断言 private call sequence，除非顺序本身就是需要保护的行为。

每个 test 只断言足以暴露目标 failure 的 observable result。除非本身就是明确 contract，不要顺带固定完整 error message、artifact filename、directory layout、ordering 或 serialization details。

## 5. Config test

不要测试显而易见的字段存储和当前实验配置 literal，例如：

```python
assert Config(x=1).x == 1
```

也不要把快速变化的实验 JSON/YAML 原样复制到 test expected values 中。

值得测试的是有真实运行语义的行为，例如：

- parsing；
- inheritance；
- precedence；
- normalization；
- cross-field conflict；
- invalid boundary；
- runtime consequence；
- 会导致 kernel、model 或 evaluator 错误的值域。

对快速变化的实验 config，更适合保存 resolved config、schema 和必要的 cross-field validation。

## 6. Mock

Mock 的主要用途是隔离与被测行为无关、但昂贵或难启动的 infrastructure。

使用 mock 前检查：

- 被 mock 的部分是否与要保护的 behavior 无关？
- mock 是否隐藏真实 model、tokenizer、tensor shape、dtype、device 或 lifecycle 约束？
- 是否能使用 tiny real object 替代？
- test 是否只在复述预先配置的 mock call sequence？

原则：

> Mock away irrelevant infrastructure; do not mock away the behavior being validated.

对于模型和系统研究，tiny real model、small tensor 和 real core object 往往比复杂 fake 更可靠。

## 7. 一次性实验和快速原型

快速变化的 research prototype 不应被旧 tests 锁死。

以下内容通常不值得建立长期 regression contract：

- 一次性实验脚本；
- 临时 analysis pipeline；
- paper figure 的颜色、marker、legend 布局；
- display name；
- 默认输出文件名；
- 正在频繁改变的内部 JSON schema；
- 用户从未要求的 backward compatibility；
- 仅供当前实验使用的中间格式。

这类内容更适合：

- manual verification；
- smoke run；
- resolved config；
- reproducibility command；
- artifact metadata；
- 最终 figure 的 visual review。

## 8. Production-style edge cases

不要因为能够想到一个低概率 failure，就自动：

```text
add defensive implementation
→ add detailed tests
→ turn it into a permanent requirement
```

例如 concurrency protocol、hostile symlink、short write recovery、legacy migration 等，只有在实际运行环境中真实存在时才值得维护。

但会静默污染研究结果或不可重建 artifact 的问题例外，例如：

- cache identity 错误；
- incomplete checkpoint 被当成有效结果；
- provenance mismatch；
- 昂贵 artifact corruption；
- resume 到错误 run。

## 9. Test 生命周期

新增 test 时明确它属于哪一类：

- permanent behavior contract；
- known-bug regression；
- temporary migration test；
- experiment-only verification；
- manual reproducibility check。

当被保护的旧行为已经删除，应同步删除对应 tests。不要为了让旧 tests 继续通过而默认增加 compatibility layer。

## 10. 参数化和实验矩阵

同一种验证逻辑需要覆盖多个 model、dtype、backend 或 boundary 时，优先参数化或复用共同 runner，不要复制整个 test body。

但不要机械做 Cartesian product。只覆盖与 failure mechanism 相关的代表性组合。

GPU、model loading、server 和 distributed tests 应使用能够暴露问题的最小资源规模。

## 11. 明确拒绝的低价值模式

通常不要写：

- `Config(x=1).x == 1`；
- exact color / marker / style dictionary；
- 当前 experiment config 的完整 literal snapshot；
- 一次性 plot 的固定 glyph 数量；
- 默认文件名或 display label 的机械断言；
- 用户未要求的 legacy compatibility tests；
- mock 整个系统后断言 mock calls；
- 为 coverage 测试 Python / framework 自己保证的行为；
- 与 production implementation 逐行同构的 expected implementation。

## 12. 推荐模式

优先考虑：

```text
optimized vs reference
CPU vs CUDA/backend
streaming/chunked vs eager/full
checkpointed vs direct forward
output parity
gradient parity
semantic identity / cache collision
known bug minimal reproduction
meaningful state invariant
artifact provenance/corruption
```

验证完成后，只报告实际运行过的 test 或 check。不要把“代码看起来正确”表述为“已验证”。
