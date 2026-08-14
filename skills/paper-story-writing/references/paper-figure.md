# 论文插图规范

当设计、修改、检查或规划论文 figure 时，使用本规范。

论文图不是结果容器。

**论文图是视觉论证。**

它的目标不是把所有结果都塞进去，而是让论文中一个重要结论变得一眼可见。

## 1. 先确定这张图要让读者记住什么

在决定：

- layout；
- panel；
- 颜色；
- marker；
- annotation；
- legend；

之前，先用一句话写出：

> 读者看到这张图几秒钟后，最应该理解什么？

整张图围绕这个 takeaway 设计。

每一个 panel、comparison、annotation 和视觉强调，都应该服务于这个结论。

不能强化主信息的内容应删除、弱化或移到别处。

如果某一个结果是核心结果，就不要平均分配视觉权重。

**让最强结果成为视觉中心。**

## 2. 一切以论文中的最终渲染尺寸为准

论文图真正存在的尺寸，是它在最终 PDF 中被读者看到的尺寸。

不要根据以下状态判断可读性：

- 巨大的 Matplotlib 窗口；
- SVG 编辑器里的放大视图；
- standalone PNG；
- presentation slide；
- 比论文实际尺寸更大的浏览器预览。

在推荐尺寸前，尽可能先确定：

- page size；
- 单栏还是双栏模板；
- 正文 body-text 字号；
- 实际 `\columnwidth`；
- 实际 `\textwidth`；
- 这张图最终是单栏还是跨双栏。

如果已有 LaTeX template 或编译后的论文，应读取实际版式，而不是凭经验猜。

具体 venue 或模板明确规定的 figure 要求优先于本文档的默认建议。

## 3. 给出最终物理尺寸，而不是随便给像素

单栏 figure：

> 目标宽度应接近论文实际 `\columnwidth`。

双栏 figure：

> 目标宽度应接近论文实际 `\textwidth`。

如果已经知道模板尺寸，应明确给出：

- cm；
- mm；
- inch；

等最终物理尺寸。

不要只推荐 width。

还应根据内容给出：

- 推荐 height；或
- 推荐 aspect ratio。

高度和比例应根据：

- panel 数量；
- 主要比较方向；
- axis label 密度；
- annotation 数量；
- caption 和页面空间；
- 视觉主次关系；

共同决定。

不要先做一张很大的图，再依赖 LaTeX 大幅缩小。

缩小 figure 会同时缩小：

- 文字；
- marker；
- line width；
- annotation；
- panel 间距。

## 4. Matplotlib 等绘图库尽量直接按最终尺寸设计

如果使用 Matplotlib 等绘图库，尽可能让 `figsize` 接近论文中预期的最终物理尺寸。

这样以 point 为单位设置的字号，才更接近论文最终实际看到的字号。

例如目标 figure 最终约为：

> 3.4 inch × 2.4 inch

则应优先直接围绕这一尺寸设计，而不是先画成 12 inch 宽再缩到 3.4 inch。

如果必须在 LaTeX 中进一步缩放，应把缩放比例计入最终字号判断。

## 5. 图中文字应接近正文大小

figure 里的文字在最终 PDF 中必须舒适可读。

基本原则：

> 图中文字应该像论文正文的一部分，而不是嵌进去的一个微型软件界面。

以正文 body text 为基准。

推荐最终字号范围：

- 关键 label / annotation：约正文的 `0.9–1.0×`；
- axis label：约 `0.85–1.0×`；
- tick label：约 `0.8–0.95×`；
- legend：约 `0.8–0.95×`；
- panel label `(a) (b) ...`：应明显可见，不应比普通 tick 更弱。

如果正文约为 10 pt，可从以下最终字号开始：

- 关键 label：9–10 pt；
- axis label：约 9 pt；
- tick / legend：约 8–9 pt。

如果正文是 9 pt，应相对正文同步调整，而不是机械沿用 10 pt 模板。

这里所有字号都指：

> **论文最终渲染后的字号。**

不是绘图库中未经缩放的原始参数。

不要通过把所有文字缩到很小来解决拥挤。

优先：

- 简化 figure；
- 删除次要信息；
- 拆 panel；
- 缩短 label；
- 改成双栏图。

## 6. 单栏还是双栏必须主动决定

如果单栏下仍然：

- 字足够大；
- comparison 清晰；
- panel 不拥挤；

优先使用单栏。

出现以下情况时，应主动考虑跨双栏：

- 方法或 category 很多；
- 多个 panel 需要直接横向比较；
- axis label 或 legend 太长；
- 单栏会迫使文字缩得过小；
- figure 本身承担核心论证；
- 核心结果值得获得更大的视觉面积。

不要为了节省版面，强行把复杂或重要的 figure 塞进单栏。

## 7. 让论文故事的层级直接体现在视觉层级中

读者应该能够迅速看出：

- 第一眼应该看哪里；
- 哪个 comparison 最重要；
- 哪个是本文方法；
- 哪个趋势或差异承担核心结论。

主动使用：

- layout；
- ordering；
- whitespace；
- annotation；
- visual emphasis；

建立层级。

如果论证本身不是平均分布的，就不要让所有：

- line；
- bar；
- point；
- panel；

获得完全相同的视觉权重。

关键结果可以更突出。

次要比较应视觉降级。

图的视觉结构应该服务论文的故事结构。

## 8. 多 panel figure

对于 `(a) (b) (c) ...`：

- 字体大小保持一致；
- 相关 panel 尽量使用可直接比较的 axis；
- 相同语义使用一致的视觉编码；
- 能共享 legend 时避免每个 panel 重复；
- panel label 必须容易定位；
- panel 顺序按照论证逻辑，而不是实验执行顺序；
- 空间按照重要性分配，不要机械平均。

每个 panel 都必须能说明自己为什么存在。

不能强化 figure 主结论的 panel，应删除、弱化或移到其他位置。

## 9. 字体、符号和正文保持一致

不仅字号要一致，还应尽量统一：

- font family；
- 数学符号；
- variable name；
- capitalization；
- abbreviation；
- method name；
- notation。

如果正文写：

`K_{\mathrm{PIC}}`

figure 中不要随意变成：

`K_pic`

图和正文应该像同一篇论文，而不是来自两个不同系统。

## 10. 不要只依赖颜色传递关键信息

重要 distinction 应尽量在以下情况下仍然成立：

- grayscale；
- 黑白打印；
- 常见色觉差异；
- 缩小到论文最终尺寸。

必要时组合：

- color；
- line style；
- marker；
- hatch；
- direct label；
- shape；
- annotation。

颜色用于强化视觉层级，不应该成为唯一的信息通道。

## 11. 控制视觉密度

最终渲染尺寸下：

- line 必须仍然容易区分；
- marker 必须仍然可辨认；
- error bar 必须仍然可读；
- annotation 不应互相碰撞；
- legend 不应压过主体；
- grid 不应抢走数据注意力；
- 装饰元素不能浪费核心论证需要的空间。

优先删除视觉噪声，而不是把所有东西一起缩小。

## 12. 导出格式

plot、diagram、line art 在 venue 和论文 pipeline 支持时，优先使用 vector：

- PDF；
- SVG 可用于编辑，再按论文流程转换。

照片、rendered image 等天然 raster 内容再使用 raster 格式。

raster 图的 resolution 应根据：

> 最终物理尺寸

决定，而不是根据原始 canvas 尺寸决定。

避免把文字和本可保持 vector 的图形无必要 rasterize。

## 13. 必须在最终 PDF 中检查

standalone figure 看起来很好，不代表论文里的 figure 已经完成。

只有在 compiled paper 中检查过，figure 才算完成。

至少检查：

- 最终 placement；
- 正常阅读倍率；
- 与正文并排时的视觉大小；
- 实际 caption；
- LaTeX 缩放后的结果；
- 单栏 / 双栏最终版式。

确认：

- 所有文字无需 zoom 即可阅读；
- 图中文字不会明显小于正文；
- visual hierarchy 在缩放后仍然成立；
- label 不碰撞；
- 核心结果仍然一眼可见；
- figure 占用版面与其重要性匹配。

如果最终 PDF 中不可读，应重新设计 figure，而不是接受小字。

## 尺寸建议的输出格式

当用户询问 figure 应该多大时，不要只给泛泛建议。

至少回答：

1. **placement**：单栏还是双栏；
2. **target width**：实际 `\columnwidth` / `\textwidth` 及物理尺寸；
3. **target height / aspect ratio**；
4. **正文 body-text size**；
5. **figure 最终推荐字号**；
6. **为了保持可读性需要做的 layout 调整**；
7. **哪部分应该成为视觉中心**。

例如：

> 当前是双栏论文，正文约 10 pt。建议该图先按单栏 `\columnwidth`
> （约 X cm）设计，aspect ratio 约 Y:Z。最终 axis label 约 9 pt，
> tick / legend 约 8–9 pt。如果现有 panel 在这个宽度下必须进一步缩小字体，
> 应改成跨双栏，而不是继续压缩字号。

如果已有实际论文版式，不要脱离真实 layout 独立推荐 figure 尺寸。

## 最终原则

**按照审稿人最终真正看到的尺寸设计 figure。**

**让论文最核心的视觉结论不可能被错过。**
