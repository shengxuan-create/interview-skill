# AI 时代面试 / AI-Era Interviews(v2.0 新增)

> 何时读本文件:用户提到 AI 面试官、异步视频面(HireVue/讯飞/牛客类)、AI 初筛、
> "面试能不能用 AI/Copilot"、或目标岗位是 AI/LLM 相关时。
> 创建模式 Step 3(调研该公司是否用 AI 面试环节)与 Step 4(出题)也应查阅本文件。

---

## 一、AI 面试官轮(异步视频面 / AI 初筛)

2024 年起,AI 面试环节已成为大厂初筛和大批量校招的标配:北美常见 HireVue、Paradox、
Karat(真人+AI 混合);国内常见讯飞智聘、牛客 AI 面、用友大易等。特征:无真人、录像作答、
限时(每题 1-3 分钟)、可能限次重录。

### 应对策略(写进 prep_plan 的具体动作)

1. **结构前置**:AI 评分对"结构信号"极敏感。答案第一句直接给结论/框架("我会分三步处理:…"),
   再展开。人面可以铺垫,AI 面不行——前 15 秒权重最高。
2. **关键词覆盖**:AI 评分通常对照 JD 关键词。准备阶段把 JD 核心技能词列成清单,
   每个答案自然带到 1-2 个(生硬堆砌会被真人复核环节识破,自然带入即可)。
3. **镜头纪律**:看镜头不看屏幕上的自己;背景整洁;光源在脸前不在脑后。
   语速比平时慢 10%——ASR 转写错误会直接拉低评分。
4. **限时练习**:mock 时按"90 秒版"重练核心 STAR 故事——AI 面的时限比人面短得多,
   故事库里每个故事都应有 3 分钟完整版和 90 秒压缩版两档。
5. **重录策略**:允许重录时,第一次当草稿,第二次交卷;超过两次收益急剧下降,不如保留自然度。

### Mock 支持

模拟 AI 面试轮时:逐题限时(用户说完即计时结束)、不追问、结束后按"结构前置/关键词覆盖/
时长控制"三维度额外评分,并与常规 STAR 分并列展示。

---

## 二、「能不能用 AI」政策应对(live coding)

2026 年的现实:公司分裂成两派,面试前必须搞清楚目标公司属于哪派(调研 Step 3 应查,
查不到就建议用户直接问 recruiter——这是完全正当的问题)。

### A 派:禁用 AI(仍是多数大厂 onsite)

- 练习时**关掉** Copilot/Cursor 刷题——平时依赖补全,考场手写会现原形,
  尤其是语法细节和标准库 API。prep_plan 中的刷题任务默认按此模式安排。
- 重点恢复"裸写"肌肉:白板/CoderPad 无补全环境至少练 5 题。

### B 派:允许甚至要求用 AI(增长最快的新形态)

- 考察点变成:**prompt 质量、对 AI 输出的批判性审查、debug AI 代码的速度**。
- 练习模式:拿一道中等题,故意让 AI 生成有缺陷的方案,练"读别人的代码找错"。
- 面试中出声思考:"我会先让它生成骨架,但这里的边界条件我要自己验——"
  展示你是 AI 的主人不是乘客,这正是这类面试想看的。

---

## 三、AI 岗位新题型(Step 4 出题时按岗位混入)

目标岗位含 AI/ML/LLM 关键词时,从下列题型中按轮次混入 3-6 题
(通用题库见 `question_bank.md` 的 AI-Era 节):

| 题型 | 考察点 | 示例 |
|---|---|---|
| RAG 系统设计 | 检索/重排/上下文预算/评估 | "设计一个客服知识库问答系统,怎么控制幻觉?" |
| Agent 架构 | 工具调用/状态/失败恢复 | "一个多步 agent 中途工具报错,你的重试与回退策略?" |
| Evals | 数据集构建/指标/回归 | "你怎么证明新 prompt 比旧的好?" |
| LLM 安全基础 | 注入/越狱/数据泄漏 | "用户输入里藏指令怎么防?" |
| 成本与延迟 | 缓存/蒸馏/路由 | "推理成本砍一半,质量少掉多少,怎么权衡?" |

**非 AI 岗也会被问的一题**:"你平时怎么用 AI 提效?"——准备一个真实、具体、
带产出数字的例子(参考 storybank 的 efficiency 类故事),避免"我用 ChatGPT 查资料"这种零信息答案。

---

# English Version

## 1. AI-interviewer rounds (async video / AI screening)

Since 2024 AI screening rounds are standard for high-volume hiring: HireVue, Paradox, Karat
(human+AI hybrid) in North America; iFlytek, Nowcoder AI in China. Traits: no human, recorded
answers, hard time limits (1-3 min/question), limited retakes.

**Strategies (turn into concrete prep_plan tasks):**
1. **Structure first** — open with the conclusion/framework in sentence one; the first 15 seconds
   carry the most scoring weight.
2. **Keyword coverage** — list the JD's core skill terms; weave 1-2 naturally into each answer.
3. **Camera discipline** — look at the lens, clean background, light in front; speak ~10% slower
   (ASR transcription errors directly hurt scores).
4. **Timed drills** — every storybank story needs a 3-minute full version AND a 90-second cut;
   AI rounds only ever use the cut.
5. **Retake policy** — take one: draft; take two: submit. Beyond two, naturalness drops faster
   than polish rises.

**Mock support:** simulate AI rounds with per-question timing, no follow-ups, and an extra
score row (structure-first / keyword coverage / timing) alongside the regular STAR score.

## 2. "Can I use AI?" policy (live coding)

Find out which camp the company is in during Step 3 research; if unknown, tell the user to ask
the recruiter directly — a fully legitimate question.

- **AI banned (most big-tech onsites):** practice with Copilot/Cursor OFF; schedule at least
  5 problems in a bare CoderPad/whiteboard environment to rebuild unassisted muscle memory.
- **AI allowed/required (fastest-growing format):** the test becomes prompt quality, critical
  review of AI output, and debugging speed. Practice on intentionally-flawed AI solutions.
  Think aloud in the interview: "I'll let it scaffold this, but I'll verify the boundary
  conditions myself —" show you're the pilot, not the passenger.

## 3. AI-role question types (mix into Step 4 by role)

RAG system design · agent architecture & failure recovery · evals methodology ·
LLM safety basics (injection/jailbreak/leakage) · cost-latency tradeoffs.
And the one question now asked in *every* role: "How do you use AI to work better?" —
prepare one real, specific, quantified example; "I use ChatGPT for research" is a zero-information answer.
