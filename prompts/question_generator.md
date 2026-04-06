# Step 4: Question Generator — 面试题生成

> 基于公司简报、JD解析、面试轮次和简历匹配结果，生成定制化面试题库。
> 每道题标注频率、考察点和参考思路，不是泛泛的通用题。

---

## 输入

- `company_brief`: Step 3 生成的公司简报
- `jd_parsed`: JD解析结果（技能要求、技术栈）
- `interview_round`: 用户选择的面试轮次（Q4）
- `resume_match`: 简历匹配结果（如有，针对gap出题）
- `references/question_bank.md`: 通用高频题库
- `references/interview_formats.md`: 该轮次的题目类型分布
- `references/company_culture_tags.md`: 公司文化标签

## 生成规则

### 题目来源优先级
1. **真实面经题**（company_brief中标注[REAL]的题目）→ 直接收录
2. **高频考点定制题**（基于交叉验证HIGH频考点）→ 针对性生成
3. **JD技能匹配题**（基于JD要求的具体技术栈）→ 技术题
4. **简历Gap题**（如果有resume_match，针对弱项出题）→ 查漏补缺
5. **通用高频题**（从question_bank.md中选取适配该公司的）→ 补充
### 题目数量（按轮次调整）

| 轮次 | Behavioral | Technical | System Design | Situational | 总计 |
|------|-----------|-----------|--------------|-------------|------|
| Phone Screen | 3 | 3 | 0 | 1 | 7 |
| Technical | 2 | 6 | 2 | 0 | 10 |
| Behavioral | 8 | 0 | 0 | 3 | 11 |
| Onsite（全天） | 8 | 8 | 3 | 2 | 21 |
| Final Round | 5 | 0 | 1 | 3 | 9 |

### 每题输出格式

```markdown
## {题目类型} Questions

1. [{频率标签}] {题目}
   - 考察点：{skills being tested}
   - 该公司偏好：{company-specific angle from company_brief}
   - 参考思路：{brief approach, STAR框架提示 for behavioral}
   - 难度：{difficulty level}
   - 时间分配：{if applicable, e.g. system design}
```

### 简历Gap专项题（如果有resume_match）

针对 `resume_match.gap_skills` 中的每个gap，生成1-2道题：
- 目的：让用户提前准备如何回答"你没有XX经验"
- 策略：将gap转化为学习意愿和迁移能力的展示机会

## 预览确认 Checkpoint #2

```
已生成 {N} 道面试题：
  - Behavioral: {n1} 题
  - Technical: {n2} 题
  - System Design: {n3} 题
  - Situational: {n4} 题

想调整重点方向吗？还是直接进入模拟面试？
```

用户确认后进入 Step 5 mock_interviewer。