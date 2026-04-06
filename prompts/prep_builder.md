# Step 7: Prep Builder — 输出面试准备文档包

> 将所有前序步骤的输出汇总为一套完整的面试准备文档。
> 创建目录结构，写入所有文件，生成独立可运行的skill。

---

## 输入

- `company_brief`: Step 3 公司简报
- `questions`: Step 4 题库
- `mock_script`: Step 5 模拟面试记录
- `evaluation`: Step 6 评分结果
- `meta_data`: 元信息（公司/职位/轮次/语言/时间）

## 执行步骤

### 7a. 创建目录结构

```bash
mkdir -p preps/{slug}/knowledge
```

### 7b. 写入文件

1. **`preps/{slug}/company_brief.md`** — 公司简报（含置信度标签+来源）
2. **`preps/{slug}/questions.md`** — 题库+参考思路
3. **`preps/{slug}/mock_script.md`** — 模拟面试记录+评分
4. **`preps/{slug}/prep_plan.md`** — 时间线准备计划
**prep_plan.md 格式：**

```markdown
# {company} {role} 面试准备计划

## 面试日期：{如果知道}
## 剩余准备时间：{天数}

### 第1天（今天）
- [ ] 复习company brief，熟悉公司文化和价值观
- [ ] 准备3个最重要的STAR故事

### 第2-3天
- [ ] 刷高频LeetCode题：{题号列表}
- [ ] 练习system design: {具体题目}

### 第4-5天
- [ ] 再做一次mock interview
- [ ] 准备"为什么选我们"的回答
- [ ] 准备提问面试官的问题

### 面试当天
- [ ] 复习company brief关键数据
- [ ] 回顾STAR故事要点
- [ ] 提前10分钟准备好环境
```

5. **`preps/{slug}/meta.json`** — 元数据（结构见架构文档§四）
6. **`preps/{slug}/SKILL.md`** — 独立可运行的skill文件
### 7c. 生成独立 SKILL.md

为每个prep生成可独立运行的skill文件：

```markdown
---
name: interview-prep-{slug}
description: "{company} {role} 面试模拟与准备材料"
user-invocable: true
---

# {company} — {role} 面试准备

## 公司速览
{company_brief.md 核心内容}

## 面试题库
{questions.md 内容}

## 模拟面试模式
启动后直接开始模拟面试。
面试官风格：{公司面试风格描述}
提问策略：Behavioral {n1}题 + Technical {n2}题 + Situational {n3}题

## 运行规则
1. 进入后直接开始模拟面试
2. 按照该公司面试风格提问
3. 每题追问1-2次深挖细节
4. 结束后给出整体评分+改进方向
```

### 7d. 完成提示

```
面试准备材料已生成。

文件位置：preps/{slug}/
触发词：
   /mock {slug}     — 再次模拟面试
   /update-prep {slug} — 追加新情报

面完之后记得回来说"我面完了"，我帮你复盘+把真题录入系统。
```