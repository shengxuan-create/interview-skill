# Step 6: Answer Evaluator — STAR框架评分

> 对模拟面试中用户的每个回答进行结构化评分。
> 使用 STAR 框架分析 behavioral 题，使用技术评分标准分析 technical 题。
> 参考 `references/star_framework.md`。

---

## 输入

- `mock_transcript`: Step 5 模拟面试的完整对话记录
- `questions_asked`: 实际提问的题目列表
- `references/star_framework.md`: STAR框架详细说明

## Behavioral 题评分（STAR框架）

对每道 behavioral 题的回答，按4个维度评分（1-5）：

| 维度 | 5分标准 | 1分标准 |
|------|--------|--------|
| Situation | 背景清晰、具体、有时间地点 | 模糊或缺失 |
| Task | 个人角色和目标明确 | 角色不清或混入团队表述 |
| Action | 具体行动步骤、个人贡献突出 | "我们做了"泛泛而谈 |
| Result | 量化结果+反思学习 | 无结果或仅说"成功了" |

**综合评分 = (S + T + A×2 + R×2) / 6**（Action和Result双倍权重）
## Technical 题评分

| 维度 | 5分标准 | 1分标准 |
|------|--------|--------|
| 正确性 | 方案正确、边界考虑全面 | 方案有明显逻辑错误 |
| 深度 | 能深入讨论trade-off和优化 | 只说表面方案 |
| 沟通 | 思路清晰、主动确认需求 | 沉默思考或跳跃性表达 |
| 工程素养 | 考虑可扩展性、可维护性 | 仅关注功能实现 |

## 每题评分输出格式

```markdown
## 题目 {N}：{question text}

你的回答评分：{score}/5

### STAR分析（Behavioral题）/ 技术分析（Technical题）：
- {维度1}: {GOOD/OK/WEAK} {评语}
- {维度2}: {GOOD/OK/WEAK} {评语}
- ...

### 改进建议：
- {具体、可操作的改进点}

### 改进后的参考回答：
"{完整的高分参考回答}"
```

## 总评输出

```markdown
## 整体评估

总体表现：{average_score}/5
强项：{列出表现好的方面}
需要重点提升：{列出薄弱方面}
建议下次重点练习：题目 {numbers}

### 分类表现
- Behavioral: {avg}/5
- Technical: {avg}/5
- System Design: {avg}/5（如有）

### 下一步建议
{根据评分结果给出1-3条具体行动建议}
```

评分完成后自动进入 Step 7 prep_builder。