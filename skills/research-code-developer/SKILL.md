---
name: research-code-developer
description: 面向实验研究的代码开发规范。用于设计、实现、修改和维护科研代码，优先保证研究语义清晰、便于调试与分析、实验可扩展、日志与结果可追溯，同时避免把科研原型机械地写成生产系统。
---

# Research Code Developer

## 目标

为实验研究设计、实现、修改和维护代码，使代码：

- 忠实表达研究意图与实验语义；
- 便于运行、检查、调试、分析、可视化和干预；
- 能自然支持实际存在和可预见的实验扩展；
- 保留足够的日志、配置和结果信息，以解释和复现实验；
- 在满足研究需求的前提下保持简练、清楚、易修改。

本 Skill 约束的是**科研代码开发方式**，不是默认要求完成从研究问题到论文的端到端科研流程。端到端实验开发仅在任务需要时参考 `refs/experiment-workflow.md`。

## 核心优先级

默认按以下顺序权衡设计：

1. 研究实现的正确性，以及实验语义与研究意图的一致性；
2. 研究概念和关键执行路径是否清楚、可检查；
3. 调试、观察中间状态、干预和修改是否方便；
4. 实验日志、配置、结果和重要 artifact 是否可追溯；
5. 多模型、多数据集、多方法、多配置等实验结构是否组织一致；
6. 代码是否简练、易懂、易维护。

生产级 robustness、backward compatibility、复杂输入防御、全面 regression testing 等不是默认优先目标。只有实际运行环境、用户要求或项目性质确实需要时，才为这些目标增加复杂度。

## 1. 保持研究语义清楚

代码结构应尽量对应研究问题中的真实概念和计算步骤。

- 研究中的 method、model、dataset、metric、loss、selection、compression、evaluation 等概念，应能在代码中直接找到对应实现。
- 不要为了统一工程接口，把关键算法逻辑隐藏在过深的 adapter、wrapper、factory 或 inheritance 层级中。
- 重构时首先检查实验语义是否保持一致，而不是只检查接口和输出类型是否保持一致。
- 不要在没有明确要求时，顺手改变 loss、normalization、sampling、aggregation、data filtering、evaluation protocol 等会影响实验含义的行为。
- 当研究实现需要偏离论文、已有实现或用户原始说明时，应明确说明影响研究语义的偏离。

尽量保持从研究概念到实际实现代码的路径短而清楚。

## 2. 抽象与 framework

framework 本身不是问题。多模型、多数据集、多方法、多任务或其他系统化实验需求出现时，应从整体实验结构出发设计统一接口，避免脚本和逻辑重复。

逐层生长不等于边写边补、等脚本堆积后再考虑架构。开始实现前，先为当前已知需求和实验维度完成足够完整的架构设计，明确最小可工作的端到端切片、各部分职责以及后续能力如何局部加入。实现时先完成这个最小切片并保持它可运行，再在既有结构上逐层增加能力；不要无设计地堆组合脚本，也不要借“完整设计”之名提前实现尚未需要的层。

围绕真实研究概念、当前实验维度、变化点和观察点组织抽象，使新增已知能力尽量局部，同时保留 one-off experiment、debug 和临时分析所需的直接路径。不要复制实验组合，也不要为假设中的需求增加层级。具体设计方法见 `refs/research-architecture.md`。

## 3. 面向调试、观察和实验干预设计

科研代码不仅要能运行，还要便于回答“为什么得到这个结果”。

让影响研究结论的关键执行步骤和中间状态能够按实际需要被观察、记录或干预。不要把关键研究逻辑封闭在难以拆分的接口中，也不要预先暴露和保存所有内部状态。

具体设计见 `refs/debugging-and-observability.md`。

## 4. 日志、配置和 artifact 是实验代码的一部分

实验结果如果缺少足够上下文，无法判断它由什么条件产生，就不是完整的实验输出。

记录足以解释、比较和复现实验的 resolved configuration、输入、实现版本、运行状态、结果与关键 artifact；需要程序化分析的结果使用机器可读格式。不要记录与这些目标无关的信息，也不要把科研代码变成 production telemetry system。

具体见 `refs/logging-and-artifacts.md`。

## 5. 不要默认引入生产系统需求

针对实际实验环境设计代码，不要针对想象中的 production environment 增加复杂度。

除非确实存在需求，否则不要主动引入：

- 多用户或敌对输入 threat model；
- 复杂并发写入协议；
- transaction 或多阶段 publish；
- legacy format compatibility；
- schema migration；
- 复杂 retry / recovery；
- 针对极低概率 filesystem 行为的防御；
- 为所有错误路径设计专门 exception hierarchy。

对于受控研究环境，清楚、局部、容易发现的失败通常优于复杂的防御性处理。

这不意味着忽略真实风险。会静默污染实验结果、破坏昂贵 artifact、导致错误复用 cache、错误 resume 或难以察觉的数据混淆的问题，应直接处理。

## 6. 不要因为修改代码就默认增加 test

Test 是验证手段，不是代码修改后的固定交付物。不新增长期维护的 test 可以是正确结论；很多科研修改只需运行已有 test、实际代码路径或一次性验证。

只有当 test 能保护真实、重要且可能逃逸的 failure，并且 behavior 预计长期稳定、存在可信 oracle、现有覆盖不足且维护成本合理时，才增加长期 test。Public、documented、当前被调用或可以描述为 contract，都不能单独证明它值得长期保护；快速演进的 behavior 默认使用开发期验证。

确实需要长期 test 时，选择能够完整暴露目标 failure 的最轻层级，只覆盖与 failure mechanism 相关的代表场景，并只断言必要的 observable result。不要在多个层级重复保护同一 behavior，也不要在低价值或实现耦合的已有 test 上继续堆 case。

涉及测试设计、增删测试或验证策略时，读取 `refs/testing.md`。

## 7. 修改范围

不要机械追求最小 diff，也不要无理由扩大修改范围。

应在**最小但结构完整的范围**内修改代码：

- 小改动能保持结构清楚时，不做额外重构；
- 局部补丁会继续制造重复或破坏实验结构时，可以进行必要的整体设计；
- 重构范围应能由当前研究需求、已有重复或明确扩展需求解释；
- 不顺手清理与任务无关的代码，不为了“更工程化”改写整个项目。

## 8. 开发流程

先理解需要保持的实验语义并阅读真实执行路径，再识别实验维度、变化点和观察点，完成最小但结构完整的设计。实现后运行与修改直接相关的真实路径，检查任务所需的中间状态与结果，并如实汇报已实现、已验证和未验证的内容。

不要把“代码已写完”“路径已运行”“实验结果已证明方法有效”混为一谈。

## 9. Reference 路由

任务涉及下列内容时，读取相应 reference：

- tests、validation strategy、regression、mock：`refs/testing.md`
- 多 model / dataset / method、framework、接口和扩展设计：`refs/research-architecture.md`
- debug、hook、中间状态、可视化观察点、profiling：`refs/debugging-and-observability.md`
- training/evaluation logs、config、checkpoint、cache、artifact：`refs/logging-and-artifacts.md`
- 完整实验开发、批量运行和结果分析流程：`refs/experiment-workflow.md`
- 根据论文实现或复现方法：`refs/paper-to-code.md`
- GPU、memory、throughput、kernel、distributed、系统性能：`refs/performance-and-systems.md`
- 结果聚合、表格、plot、paper figure：`refs/plotting-and-analysis.md`

只读取当前任务需要的 reference，不要为了形式完整加载全部文件。

## 10. 交付

完成代码修改后，简洁说明：

- 改了什么；
- 为什么采用当前结构；
- 实际运行或检查了什么；
- 哪些内容尚未运行或验证；
- 关键运行命令、配置或 artifact 在哪里。

不要用大量防御性说明代替实际实现和验证结果。
