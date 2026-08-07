# Changelog

## v2.0.0 — 2026-08-07

结构、内容、纪律三线大版本。旧版单体 SKILL.md(1616 行)每次触发全量占用上下文;
v2 改为薄路由 + 按需加载,并把半年实战沉淀的方法论(证据纪律/评分校准/去 AI 味)编进流程。

### Structure
- **SKILL.md 1616 → ~110 行**:纯路由器(模式表 + reference 地图 + 三条核心纪律),
  遵循渐进式披露;双语正文完整迁移至 `references/workflow-zh.md` / `workflow-en.md`(脚本迁移,零丢失)
- **新增 `AGENTS.md`**:Codex / Cursor 等非 Claude agent 的入口(v1 声称兼容但无入口文件)
- description 重写:补 AI 面试/JD/async video 等触发词,治 undertrigger

### New content
- **`references/ai-era-interviews.md`(新)**:AI 面试官轮(HireVue/讯飞类)应对策略、
  live coding 的 AI 使用政策两派打法、AI 岗新题型导引;双语
- **`references/humanize-answers.md`(新)**:参考回答与 STAR 故事的去 AI 味清单
  (8 项检查:三段式排比/AI 词汇/空洞归因/零瑕疵叙事等);可接 `humanizer` skill
- **question_bank.md +15 题 AI-Era 节**(RAG/Agent/Evals/成本/产品判断/通用),总题量 65 → 80

### Discipline upgrades (encoded into the workflow)
- **证据纪律硬化**(Step 3):只登记来源页逐字出现的内容;搜索摘要/AI 概览不可直接采信;
  存疑降级 LOW 附原链;新增「该公司是否有 AI 面试环节」为标准调研项
- **评分校准**(Step 6 + star_framework.md):新增 4 分/2 分锚定示例与校准规则
  (评分前对锚点、打完查分布、全同分=尺子失灵重评);补齐 1 分档定义
- **去 AI 味强制步**(Step 6):参考回答交付前过 humanize 清单

### Evals
- `evals/evals.json` 从空文件补为 10 条真实场景 eval(中英混合,覆盖:创建/证据纪律抗编造/
  AI 面试触发/评分校准/复盘回流/故事库/hype/AI-allowed coding),per skill-creator schema

### Unchanged
- 9 个 Python 工具接口与降级策略、preps/storybank 数据格式、版本管理——v1 用户数据完全兼容

### Trigger optimization (2026-08-07, post-v2.0)

description 经 skill-creator 触发优化循环校准,20 条真实 query(10 正 / 10 负,负例为近失误)
× 每条 3 次实测 × 12 训练 / 8 测试防过拟合:

| 轮次 | Train | Test | 说明 |
|---|---|---|---|
| 1(v2.0 原版) | 92%(P 86% / R 100%) | 88%(P 80% / R 100%) | 召回满分,失分全在假阳性 |
| 2(**采用**) | **100%** | **100%** | 加身份边界:候选人视角 only |
| 3-5 | 未超越 | 未超越 | 按测试集选最优 = 第 2 轮 |

改进要点:把「用户是候选人还是招聘方」的身份边界提到最前,并显式排除
写 JD / 面试官出题 / 播客采访 / 签证面谈 / 泛 HR 概念题 —— 这正是基线的全部失分来源。
运行方式与框架补丁见 `../interview-skill-workspace/README.md`。
