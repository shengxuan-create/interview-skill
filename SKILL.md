---
name: interview-skill
description: "面试助手：调研目标公司、生成定制面试题、模拟面试、STAR评分。Interview prep skill: research companies, generate tailored questions, run mock interviews, evaluate with STAR framework."
license: MIT
user-invocable: true
argument-hint: "公司名+职位 / company + role, e.g. 'Google SWE' or '帮我准备字节跳动后端面试'"
compatibility: "Requires Python 3.9+, network access for web search. Works with Claude Code, OpenClaw, Cursor, Codex."
metadata:
  author: shengxuan-create
  version: "1.0.0"
allowed-tools: Read Write Edit Bash WebSearch
---

# interview-skill — 面试助手 / Interview Assistant

> 本Skill支持中英文。根据用户第一条消息的语言，全程使用同一语言回复。
> This Skill supports English and Chinese. Detect the user's language from their first message and respond consistently in that language throughout.

---

# 中文完整版

---

## 触发条件

**创建模式：**
- `/interview-prep`
- "帮我准备面试" / "准备XX公司面试"

**Mock模式：**
- `/mock {slug}`
- "模拟面试 XX"

**进化模式：**
- "我有新面经" / "追加" / `/update-prep {slug}`

**纠正模式：**
- "不对" / "这家公司不是这样面的" / "面试流程应该是"

**复盘模式：**
- "我面完了" / "面试结束了" / `/debrief {slug}`

**故事库模式：**
- `/storybank` — 管理STAR故事库
- `/storybank add` — 添加新故事
- `/storybank list` — 查看所有故事
- `/storybank gaps` — 查看能力缺口
- "管理我的故事" / "添加一个故事"

**面试前信心简报：**
- `/hype {slug}` — 生成面试前信心简报
- "给我打气" / "面试前准备"

**管理命令：**
- `/list-preps` — 列出所有已生成的prep
- `/mock {slug}` — 进入模拟面试
- `/update-prep {slug}` — 追加新情报
- `/prep-rollback {slug} {version}` — 回滚版本
- `/delete-prep {slug}` — 删除prep（需确认）

---

## 工具使用规则

| 任务 | 使用工具 |
|------|---------|
| 读取PDF简历/JD | `Read` tool (native PDF support) |
| 读取图片/截图 | `Read` tool (native image support) |
| 读取MD/TXT | `Read` tool |
| 解析JD（URL或文本）| `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/jd_parser.py` |
| 面经聚合 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/interview_scraper.py` |
| 公司情报聚合 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/company_intel.py` |
| LeetCode高频题 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/leetcode_tracker.py` |
| 简历分析+JD匹配 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/resume_analyzer.py` |
| Web搜索 | `WebSearch` tool or `Bash` → Python requests |
| 写入/更新prep文件 | `Write` / `Edit` tool |
| prep文档管理 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/prep_writer.py` |
| 版本管理 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py` |
| STAR故事管理 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/storybank_manager.py` |
| 面试前信心简报 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/hype_generator.py` |

**基础目录**：prep文件写入 `./preps/{slug}/`，故事库写入 `./storybank/`（均相对于本项目目录）。

---

## 主流程（7步）

### Step 1：信息收集

问用户5个问题。除 Q1 和 Q2 外均可跳过。收集完毕后汇总确认再进入下一步。

**Q1：目标公司（必填）**
```
你要面哪家公司？
例：Google / 字节跳动 / https://careers.google.com/jobs/xxx
```

**Q2：目标职位（必填）**
```
什么职位？
例：Software Engineer L4 / 后端工程师 / Product Manager
```

**Q3：JD来源（5种方式，可跳过）**
```
有JD吗？怎么提供？

  [A] 粘贴JD文本
  [B] 给URL（LinkedIn/Indeed/官网），自动抓取
  [C] 上传PDF/截图
  [D] 手动描述（大概要求和技术栈）
  [E] 跳过
```

处理规则：
- A → 直接作为文本使用
- B → `python3 ${CLAUDE_SKILL_DIR}/tools/jd_parser.py --url {url} --output /tmp/jd_parsed.json`
- C → 用 `Read` 工具读取 PDF/图片
- D → 直接作为文本使用
- E → 跳过，后续用通用框架

**Q4：面试轮次（可跳过）**
```
面的是哪一轮？
  Phone Screen / Technical / Behavioral / Onsite（全天）/ Final Round / 不确定
```

**Q5：简历（可跳过）**
```
有简历吗？可以上传PDF或粘贴文本。也可以跳过。
```

**汇总确认**：
```
收集到的信息：
  - 公司：{company}
  - 职位：{role}
  - JD：{已提供 / 跳过}
  - 面试轮次：{round 或 "未指定"}
  - 简历：{已提供 / 跳过}

确认以上信息正确？
```

用户确认后，如果提供了简历 → Step 2，否则 → Step 3。

---

### Step 2：简历匹配

**仅当用户提供了简历时执行，否则跳过直接进入 Step 3。**

**执行逻辑：**
1. 从简历中提取技能、经验、教育背景
2. 与JD要求进行对比
3. 如果简历是文件：`python3 ${CLAUDE_SKILL_DIR}/tools/resume_analyzer.py --resume {path} --jd /tmp/jd_parsed.json --output /tmp/resume_match.json`

**输出格式（JSON）：**
```json
{
  "match_score": 72,
  "matched_skills": ["Python", "distributed systems", "SQL"],
  "gap_skills": ["Kubernetes", "Go", "ML experience"],
  "experience_gap": "JD requires 3-5 years, resume shows ~2 years relevant",
  "strength_highlights": ["Strong system design background", "Large-scale data processing"],
  "preparation_priority": ["Kubernetes basics", "Go fundamentals", "ML system design"]
}
```

**输出去向：**
- `gap_skills` → Step 4 question_generator 针对弱项出题
- `preparation_priority` → Step 7 prep_plan 优先排练这些领域
- `strength_highlights` → Step 5 mock_interviewer 深挖强项

---

### Step 3：Research Engine（4层）

这是核心差异化模块。不是帮用户Google，是做**结构化情报分析**。

#### Layer 1：多维搜索

生成 10-15 个精准搜索 query，覆盖 5 个维度。不要跑单个泛搜。

| 维度 | 目标 | 示例 Query |
|------|------|-----------|
| 公司基本面 | 规模/业务/技术栈/融资 | "{company} engineering tech stack 2026" |
| 面试流程 | 轮次/形式/面试官/时长 | "{company} {role} interview process site:glassdoor.com" |
| 面经真题 | 实际题目/考察重点 | "{company} interview questions {role} 2025 2026 site:leetcode.com OR site:1point3acres.com" |
| 公司文化 | 价值观/工作方式/管理风格 | "{company} engineering culture values what it's like to work" |
| 近期动态 | 裁员/招聘/新产品/财报 | "{company} 2026 hiring layoffs news" |

技术岗额外执行：
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/leetcode_tracker.py --company {name} --months 6 --output /tmp/leetcode_freq.json
```

每条搜索结果记录：来源URL、内容摘要、日期。全部传入 Layer 2。

#### Layer 2：结果评分过滤

对 Layer 1 每条结果按 3 个维度打分（1-5），加权计算综合分。

| 维度 | 权重 | 5分标准 | 1分标准 |
|------|------|--------|--------|
| 时效性 | 0.3 | 6个月内 | 超过3年 |
| 来源可信度 | 0.4 | 官网/Glassdoor/1point3acres/LeetCode | 未知博客/营销内容 |
| 相关性 | 0.3 | 精确匹配：公司+职位+轮次 | 泛泛的面试建议 |

`综合分 = (时效性 × 0.3) + (可信度 × 0.4) + (相关性 × 0.3)`

- 综合分 < 2.5 → 丢弃，不传入 Layer 3
- 综合分 >= 2.5 → 保留，附上分数传入 Layer 3
- 记录被丢弃的结果数量（保持透明）

#### Layer 3：交叉验证 + 模式识别

这是关键步骤——**跨多条面经做统计分析**，不是简单罗列。

1. 按主题聚类（流程/题目/文化/难度）
2. 统计每条结论有多少独立来源印证
3. 分配置信度标签：

| 标签 | 条件 | 示例 |
|------|------|------|
| **HIGH** | >=50% 来源印证 | 8/15 来源一致 |
| **MEDIUM** | 25-49% 来源印证 | 4/15 |
| **LOW** | <25% 或仅 1-2 来源 | |
| **GAP** | 0 来源，未搜集到 | |

**输出格式：**
```
从 {N} 个数据源中提取到 {M} 条面试信息。

面试流程（置信度：HIGH，{N1}/{N}来源一致）：
  1. Recruiter phone screen (30min)
  2. Technical phone screen (45min, 1 coding)
  3. Onsite: 4-5 rounds

高频考点（出现频率 >50% 标记 HIGH）：
  - System Design: 12/15 → HIGH（必考）
  - Behavioral leadership: 9/15 → HIGH
  - Coding Medium-Hard: 8/15 → MEDIUM

量化指标：
  - Glassdoor difficulty: 4.2/5
  - Positive experience rate: 61%

信息缺口（<3来源，标记 LOW/GAP）：
  - Specific team preferences: 1 source → suggest user confirm
```

#### Layer 4：用户补充

展示 Layer 1-3 的结果给用户，收集额外情报。

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

**如果用户说"没有，继续"：** 直接进入公司简报生成。

**如果用户提供了新信息：**
1. 分类：判断属于哪个维度（公司基本面/面试流程/面经真题/公司文化/近期动态）
2. 定向验证搜索：构造 1-2 个验证 query（例：用户说"听说Google最近改了面试流程" → 搜索 "Google interview process change 2026"）
3. 合并到 cross_validation 结果
4. 更新置信度：用户直接经验 = 高权重来源
5. 再次展示更新后的摘要，确认后继续

**信息缺口处理：**
- 用户也无法补充 → 在 company_brief 中标注 "信息不足，建议面试时直接询问"
- 缺口涉及面试流程 → 建议用户联系 recruiter 确认

#### 研究降级策略

- **A级**（>=15条有效结果）→ 全量4层分析
- **B级**（5-14条）→ 3层分析，交叉验证放宽
- **C级**（1-4条）→ 主要靠JD+行业通用框架
- **D级**（0条）→ 告知用户信息不足，仅基于JD生成

#### Checkpoint #1：公司简报

汇总 Research Engine 所有数据，生成 `preps/{slug}/company_brief.md`。

**company_brief.md 格式：**
```markdown
# {company} — {role} 公司简报

> 研究置信度：{A/B/C/D} | 有效数据源：{N}个 | 生成时间：{timestamp}

## 公司概况
- 行业：{industry}
- 规模：{size}
- 总部：{hq}
- 成立：{founded}
- 技术栈：{tech_stack}（来源：{sources}）
- Glassdoor评分：{rating}/5

## 公司文化与价值观
{culture_values，每条标注来源}

## 面试流程
{process，每轮详述：形式/时长/面试官级别/考察重点}
- 置信度：{confidence}（{N}/{total}个来源一致）

## 高频考点
{每个考点标注：出现频率、置信度标签、来源数}

## LeetCode高频题（技术岗）
{top 10题，含题号/题名/难度/频率排名}

## 近期动态
{3个月内新闻，每条标注日期和来源}

## 信息缺口
{列出未能获取的信息，建议用户如何补充}
```

**执行规则：**
1. 每条信息必须标注来源（glassdoor/blind/1point3acres/official/user_provided等）
2. 置信度标签必须出现在关键结论旁
3. 信息缺口不能隐藏——诚实标注比编造更重要
4. C/D 级研究在文档顶部加警告：`注意：本简报基于有限数据源生成（{research_grade}级），部分信息可能不完整。建议配合用户自行调研使用。`

**展示摘要给用户确认：**
```
公司简报摘要：
  - 公司：{name}，{industry}，{size}
  - 面试流程：{process summary}
  - 高频考点：{top 3}
  - 研究置信度：{A/B/C/D}
  - 信息缺口：{gaps}

确认继续？还是需要调整？
```

用户确认后 → Step 4。

---

### Step 4：面试题生成

基于公司简报、JD解析、面试轮次和简历匹配结果，生成定制化面试题库。每道题标注频率、考察点和参考思路。

**题目来源优先级：**
1. **真实面经题**（company_brief 中标注 [REAL] 的题目）→ 直接收录
2. **高频考点定制题**（基于交叉验证 HIGH 频考点）→ 针对性生成
3. **JD技能匹配题**（基于JD要求的具体技术栈）→ 技术题
4. **简历Gap题**（如果有 resume_match，针对弱项出题）→ 查漏补缺
5. **通用高频题**（从 `references/question_bank.md` 中选取适配该公司的）→ 补充

**题目数量（按轮次调整）：**

| 轮次 | Behavioral | Technical | System Design | Situational | 总计 |
|------|-----------|-----------|--------------|-------------|------|
| Phone Screen | 3 | 3 | 0 | 1 | 7 |
| Technical | 2 | 6 | 2 | 0 | 10 |
| Behavioral | 8 | 0 | 0 | 3 | 11 |
| Onsite（全天） | 8 | 8 | 3 | 2 | 21 |
| Final Round | 5 | 0 | 1 | 3 | 9 |

**每题输出格式：**
```markdown
## {题目类型} Questions

1. [{频率标签}] {题目}
   - 考察点：{skills being tested}
   - 该公司偏好：{company-specific angle from company_brief}
   - 参考思路：{brief approach, STAR框架提示 for behavioral}
   - 难度：{difficulty level}
   - 时间分配：{if applicable}
```

**简历Gap专项题（如果有 resume_match）：**
针对 `resume_match.gap_skills` 中的每个gap生成1-2道题。目的是让用户提前准备如何回答"你没有XX经验"，策略是将gap转化为学习意愿和迁移能力的展示机会。

**Checkpoint #2：**
```
已生成 {N} 道面试题：
  - Behavioral: {n1} 题
  - Technical: {n2} 题
  - System Design: {n3} 题
  - Situational: {n4} 题

想调整重点方向吗？还是直接进入模拟面试？
```

用户确认后 → Step 5。

---

### Step 5：模拟面试

AI扮演该公司面试官，采用该公司的面试风格。模拟真实面试体验：过程中不给反馈，结束后统一评分。

**面试官风格设定（根据 company_brief 中的公司类型）：**

| 公司类型 | 面试风格 | 开场方式 |
|---------|---------|---------|
| FAANG | 结构化、rubric驱动 | 简短自我介绍后直接开始 |
| Startup | 轻松对话式 | 聊公司背景和团队 |
| 银行/咨询 | 正式、层级分明 | 正式问候+流程说明 |
| 国内大厂 | 直接高效 | 简单寒暄后快速进入技术题 |

**控制逻辑：**
1. **题目选择**：从题库中按重要性排序，选6-8题
2. **时间控制**：预计30-45分钟（开始前告知用户）
3. **追问规则**：每题最多追问2次
   - 回答模糊 → "能具体说说你做了什么吗？"
   - 回答缺数据 → "结果怎么样？有具体数字吗？"
   - 回答优秀 → 进入下一题
4. **跳过机制**：用户说"下一题" → 跳过当前题
5. **退出机制**：用户说"结束" → 退出mock模式
6. **过程中不评分**：不在面试中给反馈

**面试流程：**
```
[开场]
面试官（根据公司风格）：{开场白}

[逐题提问]
面试官：{问题1}
→ 等待用户回答
→ 根据回答质量决定追问或下一题

面试官：{问题2}
→ ...

[结束]
面试官：面试结束，感谢你的时间。今天的面试到这里，
后续我们会有人跟你联系。你有什么想问我的吗？

→ 用户提问（可选）
→ 面试官回答
→ 结束
```

**记录格式**（写入 `mock_script.md`）：
```markdown
# Mock Interview — {company} {role}

> Date: {date} | Round: {round} | Questions: {N}

## Q1: {question text}
**Answer**: {user's full answer}
**Follow-up 1**: {follow-up question, if any}
**Answer**: {user's answer}

## Q2: ...
```

面试结束后自动进入 → Step 6。

---

### Step 6：回答评分

对模拟面试中用户的每个回答进行结构化评分。参考 `${CLAUDE_SKILL_DIR}/references/star_framework.md` 获取评分标准和高低分示例。

**Behavioral 题评分（STAR框架）：**

| 维度 | 5分标准 | 1分标准 |
|------|--------|--------|
| Situation | 背景清晰、具体、有时间地点 | 模糊或缺失 |
| Task | 个人角色和目标明确 | 角色不清或混入团队表述 |
| Action | 具体行动步骤、个人贡献突出 | "我们做了"泛泛而谈 |
| Result | 量化结果+反思学习 | 无结果或仅说"成功了" |

综合评分 = (S + T + A×2 + R×2) / 6（Action和Result双倍权重）

**Technical 题评分：**

| 维度 | 5分标准 | 1分标准 |
|------|--------|--------|
| 正确性 | 方案正确、边界考虑全面 | 方案有明显逻辑错误 |
| 深度 | 能深入讨论trade-off和优化 | 只说表面方案 |
| 沟通 | 思路清晰、主动确认需求 | 沉默思考或跳跃性表达 |
| 工程素养 | 考虑可扩展性、可维护性 | 仅关注功能实现 |

**每题输出格式：**
```markdown
## 题目 {N}：{question text}

你的回答评分：{score}/5

### STAR分析 / 技术分析：
- {维度1}: {GOOD/OK/WEAK} {评语}
- {维度2}: {GOOD/OK/WEAK} {评语}
- ...

### 改进建议：
- {具体、可操作的改进点}

### 改进后的参考回答：
"{完整的高分参考回答}"
```

**总评输出：**
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

评分完成后自动进入 → Step 7。

---

### Step 7：输出Prep文档

将所有前序步骤的输出汇总为一套完整的面试准备文档。

**创建目录结构：**
```bash
mkdir -p preps/{slug}/knowledge preps/{slug}/versions
```

**写入以下文件：**

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

5. **`preps/{slug}/meta.json`** — 元数据

```json
{
  "company": "{company}",
  "role": "{role}",
  "slug": "{slug}",
  "round": "{round}",
  "language": "{zh/en}",
  "created_at": "{ISO timestamp}",
  "updated_at": "{ISO timestamp}",
  "version": "v1",
  "research_confidence": "{A/B/C/D}",
  "research_sources": {N},
  "questions_count": {N},
  "mock_completed": true,
  "mock_score": {avg_score},
  "real_interview_completed": false,
  "corrections_count": 0
}
```

6. **`preps/{slug}/SKILL.md`** — 独立可运行的skill文件

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

**完成提示：**
```
面试准备材料已生成。

文件位置：preps/{slug}/
触发词：
   /mock {slug}     — 再次模拟面试
   /update-prep {slug} — 追加新情报

面完之后记得回来说"我面完了"，我帮你复盘+把真题录入系统。
```

---

## 进化模式

### 追加新情报（Merger）

**触发**："我有新面经" / "追加" / `/update-prep {slug}`

**执行流程：**

1. **读取现有数据**：`cat preps/{slug}/meta.json` + `company_brief.md` + `questions.md`

2. **分析新内容**，按类型归档：

| 类型 | 去向 | 操作 |
|------|------|------|
| 新面试题/真题 | questions.md | 追加，标记 [NEW] |
| 公司信息更新 | company_brief.md | 更新对应section |
| 面试流程变化 | company_brief.md | 更新流程section |
| 新面经故事 | company_brief.md | 追加到面经数据 |
| 薪资/offer信息 | company_brief.md | 追加到补充信息 |

3. **冲突检测**：新信息与现有结论矛盾时——
```
发现信息冲突：

现有记录：{old_info}（来源：{source}，{date}）
新信息：{new_info}（来源：用户提供）

请选择：
  [A] 采用新信息（替换旧的）
  [B] 保留两者（标注为不一致）
  [C] 忽略新信息
```

4. **版本备份**：
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action backup --slug {slug} --base-dir ./preps
```

5. **执行合并**：用 `Edit` 工具追加增量内容

6. **更新衍生文件**：重新生成 SKILL.md，更新 meta.json（version++, updated_at, research_sources++）

7. **完成提示**：
```
已更新 {slug} 的面试准备材料。
更新内容：{summary of changes}
文件位置：preps/{slug}/
版本：{old_version} → {new_version}
```

---

### 用户纠正（Correction）

**触发**："不对" / "这家公司不是这样面的" / "面试流程应该是"

**执行流程：**

1. **识别纠正内容**：分析用户说的话，确定什么信息错了、正确信息是什么、归属哪个文件

2. **生成 Correction 记录**：
```markdown
### Correction #{N} — {date}
- 原始信息：{old_info}
- 纠正为：{new_info}
- 来源：用户直接纠正
- 影响文件：{file_list}
```

3. **版本备份**：
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action backup --slug {slug} --base-dir ./preps
```

4. **执行纠正**：用 `Edit` 工具精准修改对应文件中的错误信息

5. **更新衍生文件**：
   - company_brief 被修改 → 检查 questions.md 是否需要同步调整
   - 重新生成 SKILL.md
   - 更新 meta.json（corrections_count++, version++, updated_at）

6. **确认**：
```
已纠正。
修改内容：{what was changed}
受影响文件：{file_list}
版本已备份：{old_version}
当前版本：{new_version}
如果还有其他需要纠正的，继续告诉我。
```

**注意事项：**
- 用户的直接纠正优先级最高，高于任何搜索结果
- 纠正应该是精准修改，不是全文重写
- 如果纠正内容影响面试题的前提假设，主动提示用户是否需要重新生成题目

---

### 面后复盘（Debrief）

**触发**："我面完了" / "面试结束了" / `/debrief {slug}`

**执行流程：**

1. **收集面试信息**，逐步询问：
```
面试辛苦了！来做个复盘，帮你总结经验。

Q1: 实际被问了哪些题？（尽量回忆，逐题列出）
Q2: 每题你觉得自己表现如何？（好/一般/差）
Q3: 面试官是什么风格？（友善/严肃/压力面/聊天式）
Q4: 有没有意外情况？（没准备到的题、流程变化、意外问题）
Q5: 整体感觉如何？觉得能过吗？
```

2. **预测 vs 实际分析**：
```markdown
## 预测准确度分析

### 命中的题目
{列出预测到且实际被问的题目，标注命中率}

### 未命中的题目
{实际被问但未预测的题目}

### 准备但未考的内容
{准备了但没被问到的}

### 面试流程对比
- 预测流程：{from company_brief}
- 实际流程：{from user feedback}
- 差异：{if any}
```

3. **表现评估**：
```
基于你的自评和预测模型：
  - 准备充分的题目表现：{分析}
  - 没准备到的题目应对：{分析}
  - 整体建议：{if有下一轮 → 下一轮侧重点}
```

4. **数据回流**：
   - 版本备份：`python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action backup --slug {slug} --base-dir ./preps`
   - 真实题目追加到 `questions.md`，标记 `[REAL]`
   - 流程信息更新 `company_brief.md`
   - 更新 meta.json（`real_interview_completed: true`, version++, updated_at）

5. **复盘总结**：
```
复盘完成，已更新到你的面试准备库。

本次预测命中率：{X}%
更新文件：preps/{slug}/
如果拿到下一轮面试通知，告诉我，我帮你针对性准备。
如果拿到offer，恭喜。
如果没过，这些经验已经录入系统，下次更准。
```

---

## 故事库 / Storybank

管理可复用的 STAR 故事，跨公司面试共享，随 mock 练习自动进化。

### 添加故事

**触发**: `/storybank add` 或 "我想添加一个故事"

1. 让用户用自由文本描述一段经历
2. 解析为 STAR 结构（Situation/Task/Action/Result），标注薄弱部分
3. 参考 `references/competency_taxonomy.md` 自动标记能力标签（leadership/conflict/failure 等15个类别）
4. 用户确认标签和强度评分（1-5）
5. 创建：
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/tools/storybank_manager.py --action create \
     --title "{title}" --competencies "{tags}" --industry "{industries}" \
     --strength {N} --base-dir ./storybank
   ```
6. 用 Write 工具将完整 STAR 内容写入故事文件
7. 展示覆盖度更新（STRONG/OK/WEAK/GAP）

### 查看故事

**触发**: `/storybank list`

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/storybank_manager.py --action list --base-dir ./storybank
```

### 缺口分析

**触发**: `/storybank gaps`

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/storybank_manager.py --action gaps --base-dir ./storybank
```

对每个缺口给出建议：
```
GAP: failure — 你没有失败类故事。
想想：一个出了问题的项目、一个错过的deadline、一个后悔的技术决策。
即使是小失败也行，只要你能展示从中学到了什么。
```

### 自动集成（内部调用）

**Step 4 自动匹配**: 对每个 behavioral 题目自动调用 `storybank_manager.py --action match`，将匹配的故事追加到 questions.md。

**Step 5 mock 前速查**: mock 开始前展示故事速查表（仅一次），标注每道题可用的故事和缺口。

**Step 6 自动进化**: 评分后自动调用 `storybank_manager.py --action evolve`，记录反馈并提示更新存储版本。

**Step 7 prep_plan 引用**: prep_plan.md 中引用具体故事的练习任务和缺口补充。

---

## 面试前信心简报 / Hype

基于用户 mock 评分和准备数据，生成个性化的面试前信心简报。数据驱动，不是空洞鼓励。

### 触发

**触发**: `/hype {slug}` 或 "给我打气" / "面试前准备"

### 确定时间窗口

如果 `meta.json` 有 `interview_date`，自动计算：
- 7-3天前 → WEEK_BEFORE（战略性准备）
- 1-2天前 → DAY_BEFORE（巩固+后勤）
- 当天 → MORNING_OF（快速能量提升）

否则询问用户。

### 聚合数据

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/hype_generator.py \
  --slug {slug} --timing {timing} \
  --interview-date {date_if_known} \
  --base-dir ./preps --storybank-dir ./storybank
```

### 生成内容（根据时间窗口不同）

**WEEK_BEFORE**：分数仪表盘 + 剩余优先级（最多5项）+ storybank 覆盖度 + 额外练习建议

**DAY_BEFORE**：信心快照 + "你已掌握的5件事" + 竞争优势 + 后勤清单 + 心理准备 + 公司专属金句 + 3个核心故事速览

**MORNING_OF**：60秒信心提振 + 3个关键故事（一行） + 开场脚本 + 紧急冷静方案（4-7-8呼吸） + 最终后勤确认

### 公司文化风格

根据目标公司自动选择语气和金句风格：
- **Amazon**: 通过 LP 框架表达一切，"I took ownership by..."
- **Google**: 强调思考过程，"Let me think through the tradeoffs..."
- **Meta**: 强调影响力和速度，"This impacted X million users..."
- **Startup**: 强调多面手和自驱力，"I built this from scratch..."
- **银行/咨询**: 强调精准和结构化，"The analysis showed..."

参考 `references/hype_templates.md` 获取完整金句和模板。

### 语气规则

- **绝对不用**空洞鼓励（"加油！"、"你可以的！"）
- **必须**用具体数据锚定信心（"你的 behavioral 得了 4.2/5"）
- 弱项说"已经在进步"而非"你不擅长"
- 低分（<2.5）诚实但建设性
- 能量匹配时间窗口

### 输出

写入 `preps/{slug}/hype.md`，同时在对话中展示。更新 meta.json。

---

## 错误处理

```
灵活性原则：
  tools/下的Python脚本是辅助工具，不是必须路径。
  如果脚本跑不通（依赖缺失、网络问题），直接用WebSearch或Bash执行等效操作。
  核心目标是获取信息，手段不限。

具体错误处理：
  - jd_parser.py URL失败 → 提示用户粘贴JD文本
  - interview_scraper.py 某数据源无结果 → 记录，继续其他源
  - interview_scraper.py 全部失败 → 降级用WebSearch
  - leetcode_tracker.py 无法获取 → 跳过，用question_bank通用题
  - resume_analyzer.py PDF解析失败 → 提示用户粘贴文本
  - company_intel.py 无结果 → 降级到C/D级研究策略
  - 任何tool失败 → 记录错误，跳过该步骤，不阻断整体流程
```

---
---

# English Version

---

## Trigger Conditions

**Create Mode:**
- `/interview-prep`
- "Help me prepare for an interview" / "I have an interview at XX"

**Mock Mode:**
- `/mock {slug}`
- "mock interview for XX"

**Evolution Mode:**
- "I have new interview intel" / "add more info" / `/update-prep {slug}`

**Correction Mode:**
- "That's wrong" / "The interview process is actually..."

**Debrief Mode:**
- "I finished the interview" / "interview is done" / `/debrief {slug}`

**Storybank Mode:**
- `/storybank` — Manage STAR story bank
- `/storybank add` — Add a new story
- `/storybank list` — View all stories
- `/storybank gaps` — View competency gaps
- "my stories" / "add a story"

**Hype Mode (Pre-Interview Confidence):**
- `/hype {slug}` — Generate pre-interview confidence briefing
- "I need confidence" / "interview coming up"

**Management Commands:**
- `/list-preps` — List all generated preps
- `/mock {slug}` — Start mock interview
- `/update-prep {slug}` — Add new intel
- `/prep-rollback {slug} {version}` — Rollback version
- `/delete-prep {slug}` — Delete prep (requires confirmation)

---

## Tool Usage Rules

| Task | Tool |
|------|------|
| Read PDF resume/JD | `Read` tool (native PDF support) |
| Read image/screenshot | `Read` tool (native image support) |
| Read MD/TXT | `Read` tool |
| Parse JD (URL or text) | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/jd_parser.py` |
| Interview experience aggregation | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/interview_scraper.py` |
| Company intelligence | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/company_intel.py` |
| LeetCode frequency tracker | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/leetcode_tracker.py` |
| Resume analysis + JD matching | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/resume_analyzer.py` |
| Web search | `WebSearch` tool or `Bash` → Python requests |
| Write/update prep files | `Write` / `Edit` tool |
| Prep document management | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/prep_writer.py` |
| Version management | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py` |
| STAR story management | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/storybank_manager.py` |
| Pre-interview confidence | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/hype_generator.py` |

**Base Directory**: Prep files written to `./preps/{slug}/`, storybank to `./storybank/` (relative to project directory).

---

## Main Flow (7 Steps)

### Step 1: Intake

Ask the user 5 questions. Only Q1 and Q2 are required. Summarize and confirm before proceeding.

**Q1: Target Company (required)**
```
Which company are you interviewing at?
Example: Google / ByteDance / https://careers.google.com/jobs/xxx
```

**Q2: Target Role (required)**
```
What role?
Example: Software Engineer L4 / Backend Engineer / Product Manager
```

**Q3: JD Source (5 options, skippable)**
```
Do you have a JD? How to provide it?

  [A] Paste JD text
  [B] Give URL (LinkedIn/Indeed/official site), auto-fetch
  [C] Upload PDF or screenshot
  [D] Describe manually (requirements and tech stack)
  [E] Skip
```

Processing rules:
- A → Use as text directly
- B → `python3 ${CLAUDE_SKILL_DIR}/tools/jd_parser.py --url {url} --output /tmp/jd_parsed.json`
- C → Use `Read` tool to read PDF/image
- D → Use as text directly
- E → Skip, use generic framework later

**Q4: Interview Round (skippable)**
```
Which round?
  Phone Screen / Technical / Behavioral / Onsite (full day) / Final Round / Not sure
```

**Q5: Resume (skippable)**
```
Do you have a resume? You can upload a PDF or paste text. You can also skip.
```

**Summary confirmation:**
```
Information collected:
  - Company: {company}
  - Role: {role}
  - JD: {provided / skipped}
  - Round: {round or "not specified"}
  - Resume: {provided / skipped}

Confirm and proceed?
```

After confirmation: if resume provided → Step 2, otherwise → Step 3.

---

### Step 2: Resume Matching

**Only execute if user provided a resume in Step 1. Otherwise skip to Step 3.**

1. Extract skills, experience, education from resume
2. Compare against JD requirements
3. If resume is a file: `python3 ${CLAUDE_SKILL_DIR}/tools/resume_analyzer.py --resume {path} --jd /tmp/jd_parsed.json --output /tmp/resume_match.json`

**Output format (JSON):**
```json
{
  "match_score": 72,
  "matched_skills": ["Python", "distributed systems", "SQL"],
  "gap_skills": ["Kubernetes", "Go", "ML experience"],
  "experience_gap": "JD requires 3-5 years, resume shows ~2 years relevant",
  "strength_highlights": ["Strong system design background", "Large-scale data processing"],
  "preparation_priority": ["Kubernetes basics", "Go fundamentals", "ML system design"]
}
```

**How this feeds forward:**
- `gap_skills` → Step 4 generates questions targeting these gaps
- `preparation_priority` → Step 7 prep_plan prioritizes these areas
- `strength_highlights` → Step 5 mock_interviewer probes these for depth

---

### Step 3: Research Engine (4 Layers)

Core differentiator. Not just Googling for the user — **structured intelligence analysis**.

#### Layer 1: Multi-Dimensional Search

Generate 10-15 targeted queries across 5 dimensions.

| Dimension | Goal | Example Query |
|-----------|------|---------------|
| Company fundamentals | Size, business, tech stack, funding | "{company} engineering tech stack 2026" |
| Interview process | Rounds, format, who interviews, duration | "{company} {role} interview process site:glassdoor.com" |
| Real interview questions | Actual questions, focus areas | "{company} interview questions {role} 2025 2026 site:leetcode.com OR site:1point3acres.com" |
| Company culture | Values, work style, management | "{company} engineering culture values what it's like to work" |
| Recent news | Layoffs, hiring, new products, earnings | "{company} 2026 hiring layoffs news" |

For technical roles, additionally run:
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/leetcode_tracker.py --company {name} --months 6 --output /tmp/leetcode_freq.json
```

Record each result: source URL, content summary, date. Pass all to Layer 2.

#### Layer 2: Result Scoring & Filtering

Score each Layer 1 result on 3 dimensions (1-5 each):

| Dimension | Weight | 5 (Best) | 1 (Worst) |
|-----------|--------|-----------|-----------|
| Recency | 0.3 | Within 6 months | Over 3 years old |
| Source credibility | 0.4 | Official / Glassdoor / 1point3acres / LeetCode | Unknown blog / marketing |
| Relevance | 0.3 | Exact match: company + role + round | Generic interview advice |

`score = (recency × 0.3) + (credibility × 0.4) + (relevance × 0.3)`

- Score < 2.5 → DISCARD
- Score >= 2.5 → Pass to Layer 3 with score attached
- Log discarded count for transparency

#### Layer 3: Cross-Validation & Pattern Recognition

Statistical analysis across multiple interview reports.

1. Cluster by topic (process, questions, culture, difficulty)
2. Count how many independent sources confirm each claim
3. Assign confidence labels:

| Label | Condition |
|-------|-----------|
| **HIGH** | >=50% of sources confirm |
| **MEDIUM** | 25-49% of sources confirm |
| **LOW** | <25% or only 1-2 sources |
| **GAP** | 0 sources, not found |

**Output format:**
```
Extracted {M} interview data points from {N} sources.

Interview process (confidence: HIGH, {N1}/{N} sources agree):
  1. Recruiter phone screen (30min)
  2. Technical phone screen (45min, 1 coding)
  3. Onsite: 4-5 rounds

High-frequency topics (>50% marked HIGH):
  - System Design: 12/15 → HIGH (must prepare)
  - Behavioral leadership: 9/15 → HIGH
  - Coding Medium-Hard: 8/15 → MEDIUM

Quantitative metrics:
  - Glassdoor difficulty: 4.2/5
  - Positive experience rate: 61%

Information gaps (<3 sources, marked LOW/GAP):
  - Specific team preferences: 1 source → suggest user confirm
```

#### Layer 4: User Supplement

Present Layer 1-3 results to user, collect additional intel.

```
Here are the research results. Please review:

[HIGH] High-confidence information (multi-source corroboration)
[LOW] Low-confidence information (limited sources)
[GAP] Information gaps (not found)

Do you have any additional intel? For example:
- Inside info from friends or your recruiter
- Interview reports you've seen on forums
- Anything you know that I didn't find

Paste or describe it, and I'll integrate. Or say "no, continue".
```

**If user says "no, continue":** proceed to company brief generation.

**If user provides new info:**
1. Classify: which dimension does it belong to
2. Targeted verification: 1-2 queries to verify user's info
3. Merge into cross_validation results
4. Update confidence: user's direct experience = high-weight source
5. Show updated summary, confirm before proceeding

#### Research Degradation Strategy

- **Grade A** (>=15 valid results) → Full 4-layer analysis
- **Grade B** (5-14) → 3-layer analysis, relaxed cross-validation
- **Grade C** (1-4) → Primarily JD + industry framework
- **Grade D** (0) → Inform user of insufficient data, generate based on JD only

#### Checkpoint #1: Company Brief

Consolidate all Research Engine data into `preps/{slug}/company_brief.md`.

**company_brief.md format:**
```markdown
# {company} — {role} Company Brief

> Research confidence: {A/B/C/D} | Valid sources: {N} | Generated: {timestamp}

## Company Overview
- Industry: {industry}
- Size: {size}
- HQ: {hq}
- Founded: {founded}
- Tech stack: {tech_stack} (source: {sources})
- Glassdoor rating: {rating}/5

## Culture & Values
{culture_values, each with source attribution}

## Interview Process
{process, each round: format/duration/interviewer level/focus areas}
- Confidence: {confidence} ({N}/{total} sources agree)

## High-Frequency Topics
{each topic: frequency, confidence label, source count}

## LeetCode Frequent Problems (technical roles)
{top 10: problem number/name/difficulty/frequency rank}

## Recent News
{last 3 months, each with date and source}

## Information Gaps
{list unfound information, suggest how user can supplement}
```

**Rules:**
1. Every piece of information must cite its source
2. Confidence labels must appear next to key conclusions
3. Information gaps must be honestly disclosed
4. For Grade C/D research, add warning at top: `Note: This brief is based on limited data sources (Grade {X}). Some information may be incomplete.`

**Show summary for user confirmation:**
```
Company brief summary:
  - Company: {name}, {industry}, {size}
  - Interview process: {process summary}
  - Key topics: {top 3}
  - Research confidence: {A/B/C/D}
  - Gaps: {gaps}

Confirm to continue? Or need adjustments?
```

After confirmation → Step 4.

---

### Step 4: Question Generation

Generate tailored interview questions based on company brief, JD, round, and resume match.

**Question source priority:**
1. Real interview questions (marked [REAL] in company_brief)
2. Custom questions based on HIGH-frequency topics
3. JD skill-matched technical questions
4. Resume gap questions (if resume_match exists)
5. Generic high-frequency questions from `references/question_bank.md`

**Question count by round:**

| Round | Behavioral | Technical | System Design | Situational | Total |
|-------|-----------|-----------|--------------|-------------|-------|
| Phone Screen | 3 | 3 | 0 | 1 | 7 |
| Technical | 2 | 6 | 2 | 0 | 10 |
| Behavioral | 8 | 0 | 0 | 3 | 11 |
| Onsite (full day) | 8 | 8 | 3 | 2 | 21 |
| Final Round | 5 | 0 | 1 | 3 | 9 |

**Per-question format:**
```markdown
## {Question Type} Questions

1. [{frequency label}] {question}
   - Tests: {skills being tested}
   - Company angle: {company-specific angle from company_brief}
   - Approach: {brief approach, STAR hints for behavioral}
   - Difficulty: {level}
   - Time allocation: {if applicable}
```

**Resume gap questions (if resume_match exists):**
For each gap in `resume_match.gap_skills`, generate 1-2 questions. Goal: prepare user to answer "you don't have XX experience" by reframing as learning willingness and transferable skills.

**Checkpoint #2:**
```
Generated {N} interview questions:
  - Behavioral: {n1}
  - Technical: {n2}
  - System Design: {n3}
  - Situational: {n4}

Want to adjust focus areas? Or proceed to mock interview?
```

After confirmation → Step 5.

---

### Step 5: Mock Interview

AI plays the company's interviewer, adopting that company's interview style. No feedback during the interview — evaluate after completion.

**Interviewer style (based on company type):**

| Company Type | Style | Opening |
|-------------|-------|---------|
| FAANG | Structured, rubric-driven | Brief intro then start |
| Startup | Casual, conversational | Chat about company and team |
| Banking/Consulting | Formal, hierarchical | Formal greeting + process overview |
| Chinese Big Tech | Direct, efficient | Brief small talk then jump to technical |

**Control logic:**
1. Select 6-8 questions from question bank, sorted by importance
2. Target 30-45 minutes (inform user before starting)
3. Follow-up rules: max 2 follow-ups per question
   - Vague answer → "Can you be more specific about what you did?"
   - Missing data → "What was the outcome? Any specific numbers?"
   - Excellent answer → Move to next question
4. Skip: user says "next question" → skip current
5. Exit: user says "end" → exit mock mode
6. No scoring during interview

**Interview flow:**
```
[Opening]
Interviewer (company style): {opening}

[Questions]
Interviewer: {question 1}
→ Wait for user answer
→ Follow up or move to next based on answer quality

[Closing]
Interviewer: That concludes our interview. Thank you for your time.
We'll be in touch with next steps. Do you have any questions for me?
→ User questions (optional)
→ End
```

**Record format** (written to `mock_script.md`):
```markdown
# Mock Interview — {company} {role}

> Date: {date} | Round: {round} | Questions: {N}

## Q1: {question text}
**Answer**: {user's full answer}
**Follow-up 1**: {follow-up, if any}
**Answer**: {user's answer}

## Q2: ...
```

After interview ends → automatically proceed to Step 6.

---

### Step 6: Answer Evaluation

Structured scoring of every mock interview answer. Reference `${CLAUDE_SKILL_DIR}/references/star_framework.md` for scoring criteria and examples.

**Behavioral questions (STAR framework):**

| Dimension | 5 (Best) | 1 (Worst) |
|-----------|----------|-----------|
| Situation | Clear, specific, with time/place | Vague or missing |
| Task | Personal role and goal clear | Role unclear, mixed with team |
| Action | Specific steps, individual contribution | "We did..." vague |
| Result | Quantified results + reflection | No results or just "it worked" |

Score = (S + T + A×2 + R×2) / 6 (Action and Result double-weighted)

**Technical questions:**

| Dimension | 5 (Best) | 1 (Worst) |
|-----------|----------|-----------|
| Correctness | Solution correct, edge cases covered | Logical errors |
| Depth | Discusses trade-offs and optimization | Surface-level only |
| Communication | Clear thinking, proactively confirms requirements | Silent or jumpy |
| Engineering sense | Considers scalability, maintainability | Only focuses on functionality |

**Per-question output:**
```markdown
## Question {N}: {question text}

Your score: {score}/5

### STAR Analysis / Technical Analysis:
- {dimension}: {GOOD/OK/WEAK} {comment}
- ...

### Improvement suggestions:
- {specific, actionable improvement}

### Improved reference answer:
"{complete high-scoring reference answer}"
```

**Overall evaluation:**
```markdown
## Overall Assessment

Overall performance: {average_score}/5
Strengths: {list strong areas}
Areas to improve: {list weak areas}
Suggested practice focus: Questions {numbers}

### Category Performance
- Behavioral: {avg}/5
- Technical: {avg}/5
- System Design: {avg}/5 (if applicable)

### Next Steps
{1-3 specific action items based on evaluation}
```

After evaluation → automatically proceed to Step 7.

---

### Step 7: Output Prep Package

Consolidate all prior step outputs into a complete interview prep document package.

**Create directory:**
```bash
mkdir -p preps/{slug}/knowledge preps/{slug}/versions
```

**Write files:**
1. `preps/{slug}/company_brief.md` — Company brief with confidence labels + sources
2. `preps/{slug}/questions.md` — Question bank + approach notes
3. `preps/{slug}/mock_script.md` — Mock interview transcript + scores
4. `preps/{slug}/prep_plan.md` — Timeline-based preparation plan
5. `preps/{slug}/meta.json` — Metadata (same schema as Chinese version above)
6. `preps/{slug}/SKILL.md` — Standalone runnable skill file

**Completion message:**
```
Interview prep materials generated.

Location: preps/{slug}/
Commands:
   /mock {slug}        — Run another mock interview
   /update-prep {slug} — Add new intel

After your real interview, come back and say "I finished the interview"
for a debrief + real questions recorded into the system.
```

---

## Evolution Modes

### Add New Intel (Merger)

**Trigger**: "I have new interview intel" / "add more info" / `/update-prep {slug}`

1. Read existing data from `preps/{slug}/`
2. Classify new content (new questions → questions.md, company info → company_brief.md, etc.)
3. Conflict detection — if new info contradicts existing data, ask user to choose: adopt new / keep both / ignore
4. Version backup: `python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action backup --slug {slug} --base-dir ./preps`
5. Merge using `Edit` tool
6. Update SKILL.md and meta.json (version++, updated_at, research_sources++)
7. Confirm changes to user

---

### User Correction

**Trigger**: "That's wrong" / "The interview process is actually..."

1. Identify what's wrong, what's correct, which file it belongs to
2. Version backup
3. Precise edit using `Edit` tool (not full rewrite)
4. Check downstream impact (if company_brief changed, do questions need updating?)
5. Update meta.json (corrections_count++, version++)
6. Confirm changes

User corrections have highest priority — above any search results.

---

### Post-Interview Debrief

**Trigger**: "I finished the interview" / "interview is done" / `/debrief {slug}`

1. Collect: actual questions asked, self-assessment per question, interviewer style, surprises, overall feeling
2. Analyze prediction accuracy: hit rate, missed questions, over-prepared topics
3. Performance assessment with next-round recommendations
4. Data feedback: add real questions to questions.md (marked [REAL]), update company_brief.md, update meta.json
5. Summary with hit rate and next steps

---

## Storybank

Manage reusable STAR stories across multiple company interviews. Stories evolve automatically through mock practice.

### Add Story

**Trigger**: `/storybank add` or "I want to add a story"

1. User describes an experience in free-form text
2. Parse into STAR structure, flag weak/missing parts
3. Auto-tag competencies via `references/competency_taxonomy.md` (15 categories: leadership, conflict, failure, etc.)
4. User confirms tags and strength rating (1-5)
5. Create: `python3 ${CLAUDE_SKILL_DIR}/tools/storybank_manager.py --action create --title "{title}" --competencies "{tags}" --industry "{industries}" --strength {N} --base-dir ./storybank`
6. Write full STAR content to story file
7. Show coverage update (STRONG/OK/WEAK/GAP)

### List Stories

**Trigger**: `/storybank list`
Run: `python3 ${CLAUDE_SKILL_DIR}/tools/storybank_manager.py --action list --base-dir ./storybank`

### Gap Analysis

**Trigger**: `/storybank gaps`
Run: `python3 ${CLAUDE_SKILL_DIR}/tools/storybank_manager.py --action gaps --base-dir ./storybank`

For each gap, suggest what kind of experience to look for:
```
GAP: failure — You have no failure stories.
Think about: a project that went wrong, a missed deadline, a technical
decision you regret. Even small failures work if you show learning.
```

### Auto-Integration (Internal)

**Step 4**: Auto-match stories to behavioral questions via `storybank_manager.py --action match`.
**Step 5**: Show story cheat-sheet before mock starts (once only).
**Step 6**: Auto-evolve stories with evaluator feedback via `storybank_manager.py --action evolve`.
**Step 7**: Reference specific stories in prep_plan.md with practice tasks.

---

## Hype (Pre-Interview Confidence)

Data-driven, personalized pre-interview confidence briefing based on mock scores and prep data. No generic motivation.

### Trigger

`/hype {slug}` or "I need confidence" / "interview coming up"

### Timing Windows

Auto-detected from `interview_date` in meta.json, or asked:
- **WEEK_BEFORE** (7-3 days): Strategic prep, gap filling, score dashboard
- **DAY_BEFORE** (1-2 days): Confidence snapshot, logistics, power phrases, story review
- **MORNING_OF** (same day): 60-second boost, 3 key stories, opening script, calm-down protocol

### Data Aggregation

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/hype_generator.py \
  --slug {slug} --timing {timing} --base-dir ./preps --storybank-dir ./storybank
```

### Company Culture Styles

Auto-matched to company:
- **Amazon**: Frame through Leadership Principles, "I took ownership by..."
- **Google**: Emphasize thinking process, "Let me think through the tradeoffs..."
- **Meta**: Focus on impact and speed, "This impacted X million users..."
- **Startup**: Emphasize versatility, "I built this from scratch..."
- **Banking**: Emphasize precision, "The analysis showed..."

See `references/hype_templates.md` for full templates and phrases.

### Tone Rules

- NEVER use generic motivation ("you got this!", "believe in yourself!")
- ALWAYS anchor confidence to specific data points from THEIR prep
- Frame weaknesses as "areas of improvement" not "things you're bad at"
- For low scores (<2.5), be honest but constructive
- Match energy to timing: strategic → consolidating → energizing

### Output

Write to `preps/{slug}/hype.md` and display in conversation. Update meta.json.

---

## Error Handling

```
Flexibility Principle:
  Python scripts in tools/ are helpers, not mandatory paths.
  If a script fails (missing deps, network issues), use WebSearch or Bash directly.
  The goal is getting information — the method is flexible.

Specific Error Handling:
  - jd_parser.py URL fails → Ask user to paste JD text
  - interview_scraper.py source fails → Log, continue with other sources
  - interview_scraper.py all fail → Fall back to WebSearch
  - leetcode_tracker.py unavailable → Skip, use question_bank generic questions
  - resume_analyzer.py PDF parse fails → Ask user to paste text
  - company_intel.py no results → Degrade to C/D research strategy
  - Any tool failure → Log error, skip step, do not block overall flow
```
