# Post Interview — 面后复盘模式

> **Trigger**: "我面完了" / "面试结束了" / `/debrief {slug}`
> **Operates on**: existing `preps/{slug}/` | **Related**: merger.md, correction_handler.md

> 收集真实面试数据，对比预测准确度，数据回流到prep系统。

---

## 输入

- `slug`: 对应的prep标识
- 现有 `preps/{slug}/` 下的所有文件

## 执行流程

### 1. 收集面试信息

逐步询问：

```
面试辛苦了！来做个复盘，帮你总结经验。

Q1: 实际被问了哪些题？（尽量回忆，逐题列出）
Q2: 每题你觉得自己表现如何？（好/一般/差）
Q3: 面试官是什么风格？（友善/严肃/压力面/聊天式）
Q4: 有没有意外情况？（没准备到的题、流程变化、意外问题）
Q5: 整体感觉如何？觉得能过吗？
```
### 2. 预测 vs 实际分析

对比我们的准备和实际面试情况：

```markdown
## 预测准确度分析

### 命中的题目
{列出我们预测到且实际被问的题目，标注命中率}

### 未命中的题目
{实际被问但我们未预测的题目}

### 准备但未考的内容
{我们准备了但没被问到的}

### 面试流程对比
- 预测流程：{from company_brief}
- 实际流程：{from user feedback}
- 差异：{if any}
```

### 3. 表现评估

```
基于你的自评和我们的预测模型：
  - 准备充分的题目表现：{分析}
  - 没准备到的题目应对：{分析}
  - 整体建议：{if有下一轮 → 下一轮侧重点}
```

### 4. 数据回流

将真实面试数据更新到prep系统：

1. **版本备份**：
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action backup --slug {slug} --base-dir ./preps
   ```

2. **更新文件**：
   - 真实题目追加到 `questions.md`，标记 `[REAL]`
   - 流程信息更新 `company_brief.md`
   - 面试风格信息更新

3. **更新 meta.json**：
   - `real_interview_completed: true`
   - `updated_at: {now}`
   - `version: {increment}`

### 5. 复盘总结

```
复盘完成，已更新到你的面试准备库。

本次预测命中率：{X}%
更新文件：preps/{slug}/
如果拿到下一轮面试通知，告诉我，我帮你针对性准备。
如果拿到offer，恭喜。
如果没过，这些经验已经录入系统，下次更准。
```