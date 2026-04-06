# Merger — 进化模式：增量合并

> 触发条件："我有新面经" / "追加" / `/update-prep {slug}`
> 将用户提供的新情报增量合并到现有prep中，保持版本历史。

---

## 输入

- `slug`: 目标prep标识
- `new_content`: 用户提供的新信息（粘贴文本/上传文件）
- 现有 `preps/{slug}/` 下的所有文件

## 执行流程

### 1. 读取现有数据

```bash
# 读取当前prep状态
cat preps/{slug}/meta.json
cat preps/{slug}/company_brief.md
cat preps/{slug}/questions.md
```

### 2. 分析新内容

对用户提供的新信息进行分类：

| 类型 | 去向 | 操作 |
|------|------|------|
| 新面试题/真题 | questions.md | 追加，标记 [NEW] |
| 公司信息更新 | company_brief.md | 更新对应section |
| 面试流程变化 | company_brief.md | 更新流程section |
| 新面经故事 | company_brief.md | 追加到面经数据 |
| 薪资/offer信息 | company_brief.md | 追加到补充信息 |
### 3. 冲突检测

新信息与现有结论矛盾时：

```
发现信息冲突：

现有记录：{old_info}（来源：{source}，{date}）
新信息：{new_info}（来源：用户提供）

请选择：
  [A] 采用新信息（替换旧的）
  [B] 保留两者（标注为不一致）
  [C] 忽略新信息
```

### 4. 版本备份

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action backup --slug {slug} --base-dir ./preps
```

### 5. 执行合并

使用 `Edit` 工具追加增量内容到对应文件。

### 6. 更新衍生文件

- 重新生成 `preps/{slug}/SKILL.md`（整合新内容）
- 更新 `meta.json`：
  - `version`: increment
  - `updated_at`: now
  - `research_sources`: increment if new source

### 7. 完成提示

```
已更新 {slug} 的面试准备材料。

更新内容：
  - {summary of changes}

文件位置：preps/{slug}/
版本：{old_version} → {new_version}
```