# Google SWE L4 — 模拟面试记录

> 模拟日期：2026-04-01 | 总时长：35min | 题目数：6 | 总评：3.5/5

---

## 题目 1：Tell me about a time you led a project with ambiguous requirements.

**面试官**: Hi, thanks for coming in today. I'm a senior engineer on the Cloud team. Let's start with a behavioral question — can you tell me about a time you led a project where the requirements weren't clear?

**候选人**: Sure. Last year at my internship, I was assigned to build a data pipeline but the PM only gave a vague description...

**面试官**: Can you be more specific about what was ambiguous?

**候选人**: The PM said "we need to process user data faster" but didn't specify which data, what latency target, or who the downstream consumers were. So I scheduled a meeting with the PM and the data science team to clarify...

**面试官**: Good. What specifically did you do after that meeting?

**候选人**: I wrote a one-page design doc outlining three options with trade-offs, got approval on Option B, and implemented it in 2 weeks. The pipeline reduced processing time from 4 hours to 20 minutes.

### 评分：(4/5)

**STAR分析：**
- Situation: [GOOD] 清楚（internship, data pipeline, vague requirements）
- Task: [GOOD] 明确（lead the project despite ambiguity）
- Action: [GOOD] 具体（scheduled meeting, wrote design doc, 3 options）
- Result: [GOOD] 有量化（4h → 20min）

**改进建议：** 加一句反思/学到什么会更好。
---

## 题目 2：Describe a time you had a conflict with a teammate.

**面试官**: Tell me about a time you disagreed with a coworker. How did you handle it?

**候选人**: In a group project, my teammate wanted to use MongoDB but I thought PostgreSQL was better for our relational data. We argued about it for a while and eventually went with PostgreSQL.

**面试官**: How did you resolve the disagreement specifically?

**候选人**: I showed him some benchmarks comparing the two for our use case. He agreed PostgreSQL was better.

### 评分：(3/5)

**STAR分析：**
- Situation: [OK] 偏简略（"group project"缺少具体背景）
- Task: [OK] 不够明确（你的角色是什么？）
- Action: [OK] 太简单（"showed benchmarks"缺少过程细节）
- Result: [WEAK] 缺失（选了PostgreSQL之后呢？项目结果？关系如何？）

**改进建议：**
- 加入背景：什么项目、什么阶段、为什么这个决定重要
- Action加细节：如何准备benchmark、如何沟通（私下还是会上）
- 必须有Result：项目outcome + 关系维护 + learning

---

## 题目 3：Implement LRU Cache (Coding)

**面试官**: Let's move to a coding question. Please implement an LRU Cache with get and put operations, both in O(1) time.

**候选人**: Sure, I'll use a hash map combined with a doubly linked list. The hash map gives O(1) lookup and the linked list maintains the access order...

*[候选人在CoderPad上写出完整实现，包含Node class、HashMap、head/tail sentinel nodes]*

**面试官**: Looks good. What's the space complexity?

**候选人**: O(capacity) for both the hash map and the linked list nodes.
**面试官**: How would you make this thread-safe?

**候选人**: I would add a lock around both get and put operations. For better performance, we could use a read-write lock since get operations only need read access... actually, since get also modifies the linked list order, we'd need a write lock for both. Alternatively, we could use a ConcurrentHashMap with finer-grained locking.

### 评分：(4/5)

**技术分析：**
- 正确性: [GOOD] 实现正确，O(1) get/put
- 深度: [GOOD] 能讨论thread-safety和trade-offs
- 沟通: [GOOD] 边写边解释思路
- 工程素养: [OK] 可以提到eviction callback、metrics等

---

## 题目 4：Number of Islands (Coding)

**面试官**: Given a 2D grid of '1's (land) and '0's (water), count the number of islands.

**候选人**: I'll use BFS. Iterate through the grid, when I find a '1', increment count and BFS to mark all connected '1's as visited...

*[写出BFS实现]*

**面试官**: What if the grid is very large and doesn't fit in memory?

**候选人**: Hmm... I'm not sure. Maybe divide it into chunks?

### 评分：(3/5)

**技术分析：**
- 正确性: [GOOD] BFS实现正确
- 深度: [WEAK] Follow-up没有好的思路（应提到distributed BFS或union-find with boundary merging）
- 沟通: [GOOD] 清晰
- 工程素养: [OK] 没考虑visited数组的in-place优化

---

## 题目 5：Design a URL Shortener (System Design)

**面试官**: Design a URL shortening service like bit.ly.

**候选人**: First, let me clarify requirements. Read-heavy or write-heavy? Expected QPS? Do we need analytics?

**面试官**: Assume 100:1 read to write ratio, 100M URLs created per month.

**候选人**: OK. I'll design with three main components: an API gateway, a shortening service, and a redirect service. For storage, I'll use a relational DB with the short code as primary key and Redis for caching hot URLs...

*[画出高层架构图，讨论hash generation策略、cache层、数据库选型]*

### 评分：(4/5)

**设计分析：**
- 需求确认: [GOOD] 主动问了关键参数
- 高层设计: [GOOD] 组件划分合理
- 深入讨论: [OK] Hash collision处理可以更深入
- 扩展性: [GOOD] 考虑了caching和sharding
---

## 题目 6：Why Google?

**面试官**: Last question — why do you want to work at Google?

**候选人**: I've always admired Google's engineering culture and the scale of problems you solve. I want to work on systems that serve billions of users.

### 评分：(2/5)

**分析：**
- 太泛泛，听起来像模板答案
- 没有提到specific team或product
- 没有connect到个人经历

**改进后的参考回答：**
> "I'm drawn to Google Cloud specifically because I've spent the past year building data pipelines, and I've seen firsthand how GCP's BigQuery and Dataflow simplify what used to be weeks of infrastructure work. I want to be on the team that builds these tools — not just uses them. Also, Google's culture of psychological safety resonates with me. In my last team, I saw how fear of speaking up led to a critical bug shipping to production. I want to work somewhere that values the kind of candor Google is known for."

---

## 整体评估

| 指标 | 得分 |
|------|------|
| 总体表现 | 3.5/5 |
| Behavioral平均 | 3.5/5 |
| Coding平均 | 3.5/5 |
| System Design | 4/5 |
| 沟通表达 | 4/5 |

**强项：** 技术实现能力、沟通边coding边解释、system design需求确认
**需要提升：** Behavioral回答缺少Result和反思、coding follow-up准备不足、"Why Google"缺少个人化
**建议重点练习：** 题目2（conflict）、题目4 follow-up（distributed scenario）、题目6（Why Google）