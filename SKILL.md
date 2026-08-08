---
name: interview-skill
description: "候选人视角的面试备战助手——帮用户自己拿 offer，不是帮公司招人。Use ONLY when the USER is the job candidate: they have an upcoming interview or recruiter contact, want to prep for a specific company/role, match their resume against a JD, practice mock interviews or behavioral/STAR stories, grind company-specific LeetCode, handle AI-interviewer or async video screening rounds, calm pre-interview nerves, or debrief after an interview — even without the words \"interview prep\" (e.g. \"明天要面字节\", \"phone screen this Friday\"). Researches the target company with evidence discipline, generates tailored questions, runs mocks with calibrated STAR scoring, and humanizes prepared answers. Do NOT use when the user is on the hiring/interviewer side — designing questions to assess candidates, conducting or grading interviews, writing JDs, screening applicants — or for non-job interviews (podcasts, journalism, visas) or generic HR-concept questions."
license: MIT
user-invocable: true
argument-hint: "公司+职位 company+role · /mock {slug} · /storybank · /hype {slug} · /debrief {slug}"
compatibility: "Python 3.9+ for optional tools; network for web search. Works with Claude Desktop, Cowork, Claude Code, Claude.ai, OpenClaw, Cursor, Codex (non-Claude agents: see AGENTS.md). Desktop/Cowork install via in-app zip upload — see INSTALL.md."
metadata:
  author: shengxuan-create
  version: "2.1.0"
allowed-tools: Read Write Edit Bash WebSearch
---

# interview-skill — 面试助手 / Interview Assistant

> 双语:根据用户第一条消息的语言,全程使用同一语言。
> Bilingual: detect the user's language from their first message and stay consistent throughout.

本文件只是路由器。**按下表找到模式后,立即 Read 对应 reference 文件获取完整执行细节**——不要凭本文件的摘要行动。
This file is a router. **Find the mode below, then Read the matching reference file for full instructions** — do not act from summaries alone.

---

## 模式路由 / Mode Routing

| 触发 / Trigger | 模式 | 执行细节所在 |
|---|---|---|
| `/interview-prep` · "帮我准备面试" · "I have an interview at X" | 创建(七步主流程) | `references/workflow-zh.md` §主流程 / `workflow-en.md` §Main Flow |
| `/mock {slug}` · "模拟面试" | 模拟面试 | workflow §Step 5-6 |
| "我有新面经" · `/update-prep {slug}` | 进化(Merger) | workflow §进化模式 |
| "不对,这家不是这样面的" | 纠正(Correction) | workflow §用户纠正 |
| "我面完了" · `/debrief {slug}` | 复盘(Debrief) | workflow §面后复盘 |
| `/storybank [add|list|gaps]` · "管理我的故事" | STAR 故事库 | workflow §故事库 |
| `/hype {slug}` · "给我打气" | 面试前信心简报 | workflow §Hype + `references/hype_templates.md` |
| `/list-preps` · `/prep-rollback` · `/delete-prep` | 管理命令 | workflow §管理命令(同节内) |
| **"AI 面试" · "AI interviewer" · async video · "能用 Copilot 吗"** | **AI 时代面试(v2 新增)** | **`references/ai-era-interviews.md`** |

**按语言选文件**:中文会话读 `workflow-zh.md`,英文读 `workflow-en.md`,内容等价。只读当前模式需要的节,不必整读。

---

## 何时读哪个 reference / When to read what

- `references/workflow-{zh,en}.md` — 一切模式的执行细节与输出模板(公司简报/题库/mock 记录/prep 计划/meta)。**进入任何模式前必读对应节。**
- `references/ai-era-interviews.md` — AI 面试官轮、异步视频面、AI 使用政策应对、AI 岗新题型。创建模式 Step 3/4 与用户提到 AI 面试时读。
- `references/star_framework.md` — STAR 评分维度、权重、**分档锚定示例(v2 校准用,评分前必读)**。
- `references/humanize-answers.md` — 参考答案与 STAR 故事的去 AI 味清单(Step 6 生成参考回答后过一遍;装了 `humanizer` skill 就用它,没装用本清单)。
- `references/question_bank.md` — 通用题库(含 v2 新增 AI 时代题型节),Step 4 补充题目时读。
- `references/industry-canon/` — **行业考纲(v2.1)**。目标岗位命中该行业时,Step 4 出题**先读这份**再补公司专属层。
  现有:`investment-banking.md`(IB / capital markets / ER / PE / 公司金融)。目录里没有的行业,按通用流程走。
- `references/competency_taxonomy.md` / `company_culture_tags.md` / `interview_formats.md` / `hype_templates.md` — 各自被 workflow 对应步骤点名时读。

---

## 工具速查 / Tools

脚本均为**辅助**,跑不通就用 WebSearch/Bash 等效替代,不阻断流程(详细错误处理见 workflow 尾节)。

| 任务 | 命令 |
|---|---|
| JD 解析(URL/文本) | `python3 ${CLAUDE_SKILL_DIR}/tools/jd_parser.py` |
| 面经聚合 | `python3 ${CLAUDE_SKILL_DIR}/tools/interview_scraper.py` |
| 公司情报 | `python3 ${CLAUDE_SKILL_DIR}/tools/company_intel.py` |
| LeetCode 高频 | `python3 ${CLAUDE_SKILL_DIR}/tools/leetcode_tracker.py` |
| 简历×JD 匹配 | `python3 ${CLAUDE_SKILL_DIR}/tools/resume_analyzer.py` |
| prep 写入/版本 | `prep_writer.py` / `version_manager.py` |
| 故事库 | `storybank_manager.py` |
| 信心简报 | `hype_generator.py` |
| PDF/图片/文本读取 | `Read` 工具原生支持 |

产物目录:prep → `./preps/{slug}/`,故事库 → `./storybank/`(相对当前项目)。

---

## 四条核心纪律 / Four Core Disciplines

这四条贯穿所有模式,优先级高于任何模板:

1. **证据纪律 / Evidence discipline** — 公司简报里每条事实必须带来源与置信度标签(HIGH/MEDIUM/LOW/GAP);**搜不到就标 GAP,绝不编造**。宁可交一份 60% 覆盖但全部可信的简报,不交一份 100% 覆盖但混入幻觉的。用户拿着编造的"高频题"进考场,是这个 skill 能犯的最严重错误。
   **【v2.1 延伸到题库】**每道题带证据标签,Checkpoint #2 必须报出「非本公司实证占多少」;
   **面经证据不足时不许退回通用题库交差**,要把预算转投 Step 3.5 锚定层(公司真实交易/近期动作/
   行业当下数字)。真实使用判例:某次 prep 因此被评「问题都很 general」,而定向补采轻松挖到硬货——
   材料一直都在,只是没去挖。
2. **评分校准 / Calibrated scoring** — STAR 评分前先读 `star_framework.md` 的锚定示例,把自己的尺子对准锚点再打分。没有锚点的评分会漂移:要么全 4 分的安慰局,要么全 2 分的打击局,两者都毁掉练习价值。
3. **答案像人 / Human-sounding answers** — 生成的参考回答与 STAR 故事,交付前按 `humanize-answers.md` 过一遍(装了 `humanizer` skill 则直接用)。2026 年的面试官都在识别 AI 写的答案;一段被听出 AI 味的"完美回答"比一段朴素的真实回答伤害大得多。

---

## 语言与语气 / Language & Tone

- 全程跟随用户语言;prep 产物用用户语言生成(meta.json 记录 language 字段)。
- 反馈具体、可操作、诚实——低分不粉饰,弱项说"怎么补"而不是"你不行"。
- 绝不用空洞鼓励;信心必须锚定在用户自己的数据上("你的 behavioral 均分 4.2")。
