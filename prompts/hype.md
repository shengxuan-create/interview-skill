# Hype — 面试前信心简报

> **Trigger**: `/hype {slug}`, "给我打气" / "I need confidence" / "面试前准备" / "interview coming up"
> **Operates on**: existing `preps/{slug}/` | **Related**: prep_builder.md, storybank.md, answer_evaluator.md
> **References**: `references/hype_templates.md`, `references/company_culture_tags.md`

---

## 执行流程

### 1. 确定时间窗口

如果 `meta.json` 包含 `interview_date`：
- 计算距面试天数
- 7-3天 → WEEK_BEFORE
- 1-2天 → DAY_BEFORE
- 0天（当天）→ MORNING_OF

如果没有 `interview_date`：
```
你的面试是什么时候？
  [A] 大概一周后
  [B] 明天
  [C] 今天 / 几小时后
  [D] 只是想看看准备进度
```

### 2. 聚合数据

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/hype_generator.py \
  --slug {slug} --timing {timing} \
  --interview-date {date_if_known} \
  --base-dir ./preps --storybank-dir ./storybank
```

### 3. 生成信心简报

使用工具输出的 JSON + `references/hype_templates.md` 对应时间窗口的模板 + `references/company_culture_tags.md` 对应公司风格：

#### WEEK_BEFORE 内容：
- 分数仪表盘（如果有多次 mock，展示进步轨迹）
- 剩余准备优先级（最多5项）
- storybank 覆盖度（如有）
- 额外 mock 练习建议
- 公司文化对齐自检

#### DAY_BEFORE 内容：
- 信心快照（正面呈现分数 — 强调优势）
- "你已经掌握的5件事"
- 你的竞争优势分析
- 后勤清单（远程 vs 现场）
- 心理准备方案
- 公司专属金句（来自 culture tag）
- 3个核心故事速览（来自 storybank，如有）

#### MORNING_OF 内容：
- 60秒信心提振（3条最强数据点）
- 3个关键故事（每个一行，触发记忆）
- 开场能量脚本（面试前30秒）
- 紧急冷静方案（4-7-8呼吸 + 接地练习）
- 最终后勤确认

### 4. 写入文件

用 Write 工具将生成内容写入 `preps/{slug}/hype.md`。

### 5. 展示给用户

直接在对话中展示完整 hype 文档。语气规则：
- 自信但不自大
- 数据驱动，不是空洞鼓励
- 匹配公司文化（Amazon 用 LP 语言，Google 用 Googleyness 语言等）
- 包含可操作项
- 鼓励但不居高临下

### 6. 更新 meta.json

添加 `hype_generated: true` 和 `hype_timing: "{timing}"` 到 meta.json。

---

## 语气规则

- **绝对不用**空洞鼓励（"加油！"、"你可以的！"、"believe in yourself！"）
- **必须**把信心锚定到用户准备过程中的**具体数据点**
- 弱项表述为"已经在进步的领域"而不是"你不擅长的"
- 如果分数确实低（<2.5），诚实但建设性：
  ```
  你的技术题得分是2.3——这是一个成长空间。把剩余时间集中在{具体话题}上。
  记住：面试题常常和mock题不同，而你的沟通能力（3.8）会帮助你
  在不确定时清晰地表达思路。
  ```
- 能量匹配时间窗口：WEEK_BEFORE=战略性, DAY_BEFORE=巩固性, MORNING_OF=能量型
