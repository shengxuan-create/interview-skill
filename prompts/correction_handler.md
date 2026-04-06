# Correction Handler — 纠正模式

> 触发条件："不对" / "这家公司不是这样面的" / "面试流程应该是"
> 处理用户对现有prep内容的纠正，更新对应文件。

---

## 输入

- `user_correction`: 用户的纠正内容
- `slug`: 对应的prep标识（从上下文推断或询问用户）
- 现有 `preps/{slug}/` 下的所有文件

## 执行流程

### 1. 识别纠正内容

分析用户说的话，确定：
- **什么信息错了**（面试流程/题目类型/公司信息/评分标准等）
- **正确信息是什么**
- **归属哪个文件**（company_brief.md / questions.md / mock_script.md）

### 2. 生成 Correction 记录

```markdown
### Correction #{N} — {date}
- 原始信息：{old_info}
- 纠正为：{new_info}
- 来源：用户直接纠正
- 影响文件：{file_list}
```
### 3. 版本备份

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action backup --slug {slug} --base-dir ./preps
```

### 4. 执行纠正

使用 `Edit` 工具修改对应文件中的错误信息。

### 5. 更新衍生文件

- 如果 company_brief 被修改 → 检查 questions.md 是否需要同步调整
- 重新生成 `preps/{slug}/SKILL.md`
- 更新 `meta.json`：
  - `corrections_count`: increment
  - `updated_at`: now
  - `version`: increment

### 6. 确认

```
已纠正。

修改内容：
  - {what was changed}

受影响文件：
  - {file_list}

版本已备份：{old_version}
当前版本：{new_version}

如果还有其他需要纠正的，继续告诉我。
```

## 注意事项

- 用户的直接纠正优先级最高，高于任何搜索结果
- 纠正应该是精准修改，不是全文重写
- 每次纠正都要记录，方便追溯
- 如果纠正内容影响面试题的前提假设，要主动提示用户是否需要重新生成题目