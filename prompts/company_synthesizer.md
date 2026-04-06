# Step 3e: Company Synthesizer — 汇总公司简报

> 本模板汇总 Research Engine Layer 1-4 所有数据，生成 company_brief.md。
> 这是整个研究阶段的最终输出，也是后续题目生成和模拟面试的核心输入。

---

## 输入

- `search_results`: Layer 1 搜索原始结果
- `filtered_results`: Layer 2 评分过滤后结果
- `cross_validation`: Layer 3 交叉验证输出
- `user_supplement`: Layer 4 用户补充（如有）
- `company_intel_json`: tools/company_intel.py 输出
- `interview_scraper_json`: tools/interview_scraper.py 输出
- `leetcode_json`: tools/leetcode_tracker.py 输出（技术岗）

## 输出格式

生成 `preps/{slug}/company_brief.md`，结构如下：
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
{每个考点标注：出现频率、置信度标签（HIGH/MEDIUM/LOW）、来源数}

## LeetCode高频题（技术岗）
{top 10题，含题号/题名/难度/频率排名}

## 近期动态
{3个月内新闻，每条标注日期和来源}

## 信息缺口
{列出未能获取的信息，建议用户如何补充}
```
## 执行规则

1. **每条信息必须标注来源**（glassdoor/blind/1point3acres/official/user_provided等）
2. **置信度标签必须出现**在关键结论旁
3. **信息缺口不能隐藏**——诚实标注比编造更重要
4. **如果是 C/D 级研究**：在文档顶部加醒目警告
   ```
   注意：本简报基于有限数据源生成（{research_grade}级），部分信息可能不完整。
   建议配合用户自行调研使用。
   ```
5. **格式保持统一**：所有 company_brief.md 遵循相同结构，方便对比不同公司

## 预览确认 Checkpoint #1

生成后展示摘要给用户确认：

```
公司简报摘要：
  - 公司：{name}，{industry}，{size}
  - 面试流程：{process summary}
  - 高频考点：{top 3}
  - 研究置信度：{A/B/C/D}
  - 信息缺口：{gaps}

确认继续？还是需要调整？
```

用户确认后进入 Step 4 question_generator。