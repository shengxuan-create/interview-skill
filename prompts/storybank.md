# Storybank — STAR故事库管理

> **Trigger**: `/storybank`, `/storybank add`, `/storybank list`, `/storybank gaps`, "管理我的故事" / "my stories" / "add a story"
> **Operates on**: `./storybank/` directory | **Related**: question_generator.md, answer_evaluator.md, mock_interviewer.md

---

## Mode A: 添加故事 / Add Story

**触发**: `/storybank add` 或 "我想添加一个故事"

1. 让用户用自由文本描述一段经历
2. 将叙述解析为 STAR 结构：
   - 提取 Situation, Task, Action, Result
   - 标注哪些部分薄弱或缺失
3. 参考 `references/competency_taxonomy.md`，自动标记能力标签
4. 让用户确认/调整标签，评估强度（1-5），或根据 STAR 完整度自动评估
5. 询问行业相关性（从 taxonomy 中提供选项）
6. 创建故事：
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/tools/storybank_manager.py --action create \
     --title "{title}" --competencies "{tags}" --industry "{industries}" \
     --strength {N} --base-dir ./storybank
   ```
7. 用 Write 工具将完整 STAR 内容写入生成的故事文件
8. 展示覆盖度更新：
   ```
   故事已添加。你的能力覆盖度：
     leadership: 3 stories (STRONG)
     conflict: 1 story (OK)
     failure: 0 stories (GAP — 建议补充一个)
     ...
   ```

---

## Mode B: 查看故事列表 / List Stories

**触发**: `/storybank list`

1. 执行：`python3 ${CLAUDE_SKILL_DIR}/tools/storybank_manager.py --action list --base-dir ./storybank`
2. 按能力标签分组展示，附上强度评分

---

## Mode C: 缺口分析 / Gap Analysis

**触发**: `/storybank gaps`

1. 执行：`python3 ${CLAUDE_SKILL_DIR}/tools/storybank_manager.py --action gaps --base-dir ./storybank`
2. 展示缺失的能力标签
3. 对每个缺口，建议用户从什么经历中找素材：
   ```
   GAP: failure — 你没有失败类故事。
   想想：一个出了问题的项目、一个错过的 deadline、一个后悔的技术决策。
   即使是小失败也行，只要你能展示从中学到了什么。
   ```

---

## Mode D: 自动匹配故事到面试题（内部调用）

此模式由 Step 4 question_generator 自动调用，不是用户直接触发。

1. 对每个生成的 behavioral 题目：
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/tools/storybank_manager.py --action match \
     --question "{question_text}" --company-culture "{culture_tag}" \
     --base-dir ./storybank
   ```
2. 将匹配结果追加到 questions.md 的题目下方：
   ```
   - 建议故事:
     [1] story_003 "跨团队API迁移" (匹配度: 92%, 强度: 4/5)
     [2] story_007 "解决PM与工程的冲突" (匹配度: 78%, 强度: 3/5)
     [GAP] 此能力标签没有匹配的故事 — 建议补充
   ```

---

## Mode E: 故事进化（内部调用）

此模式由 Step 6 answer_evaluator 自动调用。

1. 评分完一个 behavioral 回答后，检查回答是否引用了 storybank 中的故事
2. 如果是：
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/tools/storybank_manager.py --action evolve \
     --id {story_id} --feedback "{evaluator_feedback}" \
     --source-prep {slug} --new-score {score} --base-dir ./storybank
   ```
3. 将具体改进建议追加到故事文件
4. 如果用户 mock 中的回答比存储版本更好，提示是否更新：
   ```
   你在 mock 中讲的 story_003 得了 4.2/5，比存储版本的 3.5 更好。
   要不要用这个改进版本更新存储的故事？
   ```

---

## 与主流程的集成

**Step 4 (Question Generator)**: 生成 behavioral 题后，自动调用 Mode D 匹配故事。如果某题的目标能力是 storybank 的缺口，显式标注。

**Step 5 (Mock Interviewer)**: mock 开始前（如果 storybank 存在），展示速查表：
```
你的故事速查表：
  Q1 (leadership): 参考 story_001 "微服务迁移" (强度: 4)
  Q3 (conflict): 参考 story_002 "PM排序争议" (强度: 3)
  Q5 (failure): [无故事] — 需要临场发挥
```
仅在 mock 开始前展示一次，过程中不再提示。

**Step 6 (Answer Evaluator)**: 评分后自动调用 Mode E。

**Step 7 (Prep Builder)**: prep_plan.md 中引用具体故事：
```
### 第1天
- [ ] 练习 story_001 (leadership) — 重点改善 Result 的量化
- [ ] 练习 story_002 (conflict) — 重点改善 Action 的具体性
- [ ] 补充一个 failure 故事来填补 GAP
```
