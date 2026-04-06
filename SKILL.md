---
name: interview-skill
description: "面试助手：调研目标公司、生成定制面试题、模拟面试、STAR评分。Interview prep skill: research companies, generate tailored questions, run mock interviews, evaluate with STAR framework."
license: MIT
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

## 触发条件 / Trigger Conditions

**创建模式 / Create Mode：**
- `/interview-prep`
- "帮我准备面试" / "准备XX公司面试"
- "Help me prepare for an interview" / "I have an interview at XX"

**Mock模式 / Mock Mode：**
- `/mock {slug}`
- "模拟面试 XX" / "mock interview for XX"

**进化模式 / Evolution Mode：**
- "我有新面经" / "追加" / `/update-prep {slug}`
- "I have new interview intel" / "add more info"

**纠正模式 / Correction Mode：**
- "不对" / "这家公司不是这样面的" / "面试流程应该是"
- "That's wrong" / "The interview process is actually..."

**复盘模式 / Debrief Mode：**
- "我面完了" / "面试结束了" / `/debrief {slug}`
- "I finished the interview" / "interview is done"

**管理命令 / Management Commands：**
- `/list-preps` — 列出所有已生成的prep / List all generated preps
- `/mock {slug}` — 进入模拟面试 / Start mock interview
- `/update-prep {slug}` — 追加新情报 / Add new intel
- `/prep-rollback {slug} {version}` — 回滚版本 / Rollback version
- `/delete-prep {slug}` — 删除prep（需确认）/ Delete prep (requires confirmation)

---

## 工具使用规则 / Tool Usage Rules

| 任务 / Task | 使用工具 / Tool |
|------|---------|
| 读取PDF简历/JD | `Read` tool (native PDF support) |
| 读取图片/截图 | `Read` tool (native image support) |
| 读取MD/TXT | `Read` tool |
| 解析JD（URL或文本）| `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/jd_parser.py` |
| 面经聚合（多数据源）| `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/interview_scraper.py` |
| 公司情报聚合 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/company_intel.py` |
| LeetCode高频题 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/leetcode_tracker.py` |
| 简历分析+JD匹配 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/resume_analyzer.py` |
| Web搜索 | `WebSearch` tool or `Bash` → Python requests |
| 写入/更新prep文件 | `Write` / `Edit` tool |
| prep文档管理 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/prep_writer.py` |
| 版本管理 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py` |

**基础目录 / Base Directory**：prep文件写入 `./preps/{slug}/`（相对于本项目目录）。

---

## 主流程 / Main Flow（7 Steps）

### Step 1：信息收集 / Intake
参考 `${CLAUDE_SKILL_DIR}/prompts/intake.md`。
问用户5个问题：目标公司（必填）、目标职位（必填）、JD来源（5种方式，可跳过）、面试轮次、简历（可跳过）。
收集完后汇总确认再进入下一步。

### Step 2：简历匹配 / Resume Matching
**仅当用户提供了简历时执行，否则跳过。**
参考 `${CLAUDE_SKILL_DIR}/prompts/resume_matcher.md`。
输出：match_score, matched_skills, gap_skills, preparation_priority。

### Step 3：Research Engine（4层）

这是核心差异化模块。不是帮用户Google，是做**结构化情报分析**。

**Layer 1: 多维搜索** — 参考 `${CLAUDE_SKILL_DIR}/prompts/search_strategist.md`
5个维度（公司基本面/面试流程/面经真题/公司文化/近期动态），每维度2-3个精准query，总计10-15个搜索。
技术岗额外执行：`python3 ${CLAUDE_SKILL_DIR}/tools/leetcode_tracker.py`

**Layer 2: 结果评分** — 参考 `${CLAUDE_SKILL_DIR}/prompts/result_evaluator.md`
每条结果按时效性(0.3)×可信度(0.4)×相关性(0.3)打分，低于2.5分丢弃。

**Layer 3: 交叉验证** — 参考 `${CLAUDE_SKILL_DIR}/prompts/cross_validator.md`
跨多条面经做统计分析，输出置信度标签（HIGH/MEDIUM/LOW）和来源计数。

**Layer 4: 用户补充** — 参考 `${CLAUDE_SKILL_DIR}/prompts/user_supplement.md`
展示结果+信息缺口，让用户补充内部情报，做定向二次搜索验证。

**Research降级策略：**
- A级（≥15条有效结果）→ 全量4层分析
- B级（5-14条）→ 3层分析，交叉验证放宽
- C级（1-4条）→ 主要靠JD+行业通用框架
- D级（0条）→ 告知用户信息不足，仅基于JD生成

**→ Checkpoint #1**：展示公司简报摘要，确认再继续。
参考 `${CLAUDE_SKILL_DIR}/prompts/company_synthesizer.md` 生成 company_brief.md。

### Step 4：面试题生成 / Question Generation
参考 `${CLAUDE_SKILL_DIR}/prompts/question_generator.md` + `${CLAUDE_SKILL_DIR}/references/question_bank.md`。
根据company_brief、JD、面试轮次、resume_match生成定制题目。
每类5-8题，带考察点、频率标签、参考思路。
**→ Checkpoint #2**：展示题目摘要，确认或调整后进入mock。

### Step 5：模拟面试 / Mock Interview
参考 `${CLAUDE_SKILL_DIR}/prompts/mock_interviewer.md`。
AI扮演该公司面试官，采用该公司面试风格。默认选6-8题，每题最多追问2次。
面试过程中不给反馈。全部结束后说"面试结束，感谢你的时间。"自动进入Step 6。

### Step 6：回答评分 / Answer Evaluation
参考 `${CLAUDE_SKILL_DIR}/prompts/answer_evaluator.md` + `${CLAUDE_SKILL_DIR}/references/star_framework.md`。
对每个回答按STAR框架评分（1-5），标注S/T/A/R各部分是否完整。
给出改进建议和改进后的参考回答。最后给出总评。

### Step 7：输出Prep文档 / Output Prep Package
参考 `${CLAUDE_SKILL_DIR}/prompts/prep_builder.md`。
创建 `preps/{slug}/` 目录，写入：
1. `company_brief.md` — 公司简报
2. `questions.md` — 题库+参考思路
3. `mock_script.md` — 模拟面试记录+评分
4. `prep_plan.md` — 时间线准备计划
5. `meta.json` — 元数据
6. `SKILL.md` — 生成独立可运行的skill

完成后显示文件位置和后续触发词。

---

## 进化模式 / Evolution Modes

### 追加新情报 / Update
触发："我有新面经" / `/update-prep {slug}`
1. 读取新内容 → 分类（新面试题/公司信息/流程变化）
2. 冲突检测 → 提示用户决定
3. `python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action backup --slug {slug} --base-dir ./preps`
4. 增量合并 → 更新文件 → 更新meta.json
参考 `${CLAUDE_SKILL_DIR}/prompts/merger.md`。

### 用户纠正 / Correction
触发："不对" / "这家公司不是这样面的"
参考 `${CLAUDE_SKILL_DIR}/prompts/correction_handler.md`。
识别纠正内容 → 判断归属文件 → Edit对应文件 → meta.json corrections_count++。

### 面后复盘 / Post-Interview Debrief
触发："我面完了" / `/debrief {slug}`
参考 `${CLAUDE_SKILL_DIR}/prompts/post_interview.md`。
收集真实面试题目和表现 → 分析预测命中率 → 真题追加到questions.md（标记[REAL]）→ 更新文件。

---

## 错误处理 / Error Handling

```
灵活性原则 / Flexibility Principle:
  tools/下的Python脚本是辅助工具，不是必须路径。
  如果脚本跑不通（依赖缺失、网络问题），直接用WebSearch或Bash执行等效操作。
  核心目标是获取信息，手段不限。

  Python scripts in tools/ are helpers, not mandatory paths.
  If a script fails (missing deps, network issues), use WebSearch or Bash directly.
  The goal is getting information — the method is flexible.

具体错误处理 / Specific Error Handling:
  - jd_parser.py URL失败 → 提示用户粘贴JD文本
  - interview_scraper.py 某数据源无结果 → 记录，继续其他源
  - interview_scraper.py 全部失败 → 降级用WebSearch
  - leetcode_tracker.py 无法获取 → 跳过，用question_bank通用题
  - resume_analyzer.py PDF解析失败 → 提示用户粘贴文本
  - company_intel.py 无结果 → 降级到C/D级研究策略
  - 任何tool失败 → 记录错误，跳过该步骤，不阻断整体流程
```
