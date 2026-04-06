# Step 3d: User Supplement — 用户补充 + 二次搜索

> **Previous**: Step 3c cross_validator.md | **Next**: Step 3e company_synthesizer.md

> 本模板在 Research Engine Layer 1-3 完成后执行。
> 将自动调研结果展示给用户，标注置信度，收集额外情报，必要时做二次搜索。

---

## 输入

- `cross_validation_result`: Layer 3 交叉验证输出（含置信度标签和信息缺口）
- `company`: 目标公司名
- `role`: 目标职位

## 执行逻辑

### 1. 展示调研结果摘要

```
以上是自动调研结果。请检查：

[HIGH] 高置信度信息（多源印证）
[LOW] 低置信度信息（仅少量来源）
[GAP] 信息缺口（未搜集到）

你有没有额外情报？比如：
- 朋友/recruiter告诉你的内部信息
- 你在论坛看到的面经
- 任何你知道但我没搜到的

直接粘贴或描述，我来整合。也可以说"没有，继续"。
```
### 2. 处理用户输入

**如果用户说"没有，继续"：**
- 直接进入 company_synthesizer 步骤

**如果用户提供了新信息：**

1. **分类**：判断新信息属于哪个维度（公司基本面/面试流程/面经真题/公司文化/近期动态）
2. **定向验证搜索**：针对用户说的关键信息构造1-2个验证query
   - 例：用户说"听说Google最近改了面试流程" → 搜索 "Google interview process change 2026"
3. **合并**：将验证过的新信息合并到 cross_validation_result
4. **更新置信度**：用户直接经验 = 高权重来源，可提升相关条目的置信度
5. **再次展示更新后的摘要**，确认后进入下一步

### 3. 信息缺口处理

对于标记为 [GAP] 的信息缺口：
- 如果用户也无法补充 → 在 company_brief 中标注 "信息不足，建议面试时直接询问"
- 如果缺口涉及面试流程 → 建议用户联系 recruiter 确认

## 输出

- 更新后的研究数据（含用户补充）
- 每条用户补充标注来源为 "user_provided"
- 准备传入 company_synthesizer.md