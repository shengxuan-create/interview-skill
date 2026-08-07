# Interview Question Bank — 高频面试题库

> 通用题库，供 question_generator.md 选取和定制化。
> 每题标注：考察能力、常见于哪类公司、难度。

---

## Behavioral Questions（30题）

### Leadership & Influence

1. **Tell me about a time you led a project with ambiguous requirements.**
   - 考察：leadership, ambiguity tolerance
   - 常见于：FAANG, consulting
   - 难度：Medium

2. **Describe a situation where you had to convince others to adopt your idea.**
   - 考察：influence without authority, communication
   - 常见于：All companies
   - 难度：Medium

3. **Tell me about a time you mentored someone.**
   - 考察：mentorship, growth mindset
   - 常见于：FAANG (senior+), startups
   - 难度：Easy

4. **Describe a time you made a decision without all the information you needed.**
   - 考察：decision-making under uncertainty
   - 常见于：Amazon (bias for action), startups
   - 难度：Medium
5. **Tell me about your biggest professional failure.**
   - 考察：self-awareness, resilience, learning
   - 常见于：All companies
   - 难度：Hard（容易踩坑）

### Teamwork & Collaboration

6. **Tell me about a time you worked with a difficult teammate.**
   - 考察：collaboration, emotional intelligence
   - 常见于：All companies
   - 难度：Medium

7. **Describe a project where you had to collaborate across teams.**
   - 考察：cross-functional skills, communication
   - 常见于：FAANG, large enterprises
   - 难度：Medium

8. **Tell me about a time you received critical feedback. How did you respond?**
   - 考察：growth mindset, humility
   - 常见于：Google (googleyness), Meta
   - 难度：Medium

9. **Describe a situation where you had to prioritize competing demands.**
   - 考察：prioritization, time management
   - 常见于：Amazon, startups
   - 难度：Easy

10. **Tell me about a time you went above and beyond for a customer/user.**
    - 考察：customer obsession, initiative
    - 常见于：Amazon (customer obsession LP)
    - 难度：Medium
### Problem Solving & Innovation

11. **Describe a creative solution you came up with for a complex problem.**
    - 考察：creativity, analytical thinking
    - 常见于：Google, startups
    - 难度：Hard

12. **Tell me about a time you improved a process or system.**
    - 考察：initiative, optimization mindset
    - 常见于：Amazon (invent and simplify), all companies
    - 难度：Medium

13. **Describe a data-driven decision you made.**
    - 考察：analytical skills, data literacy
    - 常见于：Meta, Google, fintech
    - 难度：Medium

14. **Tell me about a time you had to learn something quickly.**
    - 考察：learning agility, adaptability
    - 常见于：Startups, fast-paced companies
    - 难度：Easy

15. **Describe a time you identified a risk before it became a problem.**
    - 考察：foresight, risk management
    - 常见于：Banks, enterprise, Amazon
    - 难度：Medium

### Communication & Influence

16. **Tell me about a time you explained a complex concept to a non-technical audience.**
    - 考察：communication, simplification
    - 常见于：All companies
    - 难度：Medium

17. **Describe a time you had to deliver bad news.**
    - 考察：honesty, empathy, professionalism
    - 常见于：All companies, especially management roles
    - 难度：Hard
18. **Tell me about a time you managed up (influenced your manager/leadership).**
    - 考察：upward management, persuasion
    - 常见于：Senior roles, all companies
    - 难度：Hard

19. **Describe how you handle competing priorities from multiple stakeholders.**
    - 考察：stakeholder management, negotiation
    - 常见于：PM roles, cross-functional roles
    - 难度：Medium

20. **Tell me about a time you had to say no to a request.**
    - 考察：boundary setting, prioritization
    - 常见于：All companies
    - 难度：Medium

### Adaptability & Growth

21-25. **Additional behavioral questions covering**: dealing with ambiguity, handling rapid change, working with limited resources, recovering from a setback, adapting to a new team/culture.

### Amazon Leadership Principles Specific

26-30. **LP-specific questions**: customer obsession, ownership, dive deep, earn trust, deliver results.

---

## Technical Questions — General（20题）

### System Design

1. **Design a URL shortener (like bit.ly)**
   - 考察：system design basics, database, caching
   - 难度：Medium
   - 时间分配：5min需求 + 15min高层 + 15min深入 + 5min扩展

2. **Design a chat system (like WhatsApp/Slack)**
   - 考察：real-time systems, WebSocket, message delivery
   - 难度：Hard
   - 常见于：Meta, Google, ByteDance
3. **Design a news feed system (like Facebook/Twitter)**
   - 考察：fan-out, ranking, caching, real-time updates
   - 难度：Hard
   - 常见于：Meta, Twitter/X, ByteDance

4. **Design a rate limiter**
   - 考察：distributed systems, algorithms
   - 难度：Medium
   - 常见于：All tech companies

5. **Design a file storage system (like Google Drive/Dropbox)**
   - 考察：storage, sync, conflict resolution
   - 难度：Hard

### Coding (Algorithm & Data Structure)

6-15. **Common coding patterns**: Two pointers, sliding window, BFS/DFS, dynamic programming, graph algorithms, tree traversal, hash map optimization, binary search variants, stack/queue applications, greedy algorithms.

### System Knowledge

16-20. **Infrastructure questions**: Database indexing and optimization, caching strategies (Redis, CDN), message queues (Kafka, RabbitMQ), containerization and orchestration, CI/CD pipeline design.

---

## Case / Situational Questions（15题）

### Product Sense (PM roles)

1. **How would you improve [product X]?**
   - 考察：product thinking, user empathy, prioritization
   - 常见于：Google APM, Meta PM, all PM roles
   - 难度：Medium

2. **A key metric dropped 10% this week. How would you investigate?**
   - 考察：analytical thinking, root cause analysis
   - 常见于：All PM and data roles
   - 难度：Medium

3-5. **Additional PM cases**: launch strategy, feature prioritization, A/B test design.

### Business Case (Consulting/Banking)

6-10. **Market sizing, profitability analysis, M&A evaluation, market entry, operational improvement.**

### Situational

11-15. **Hypothetical workplace scenarios**: new project with no guidance, disagreement with skip-level, ethical dilemma, resource constraint, deadline pressure.
---

## AI-Era Questions(v2.0 新增,15题)

> 适用:岗位含 AI/ML/LLM 关键词时按轮次混入;最后 3 题任何岗位都可能被问。
> 深度应对策略见 `ai-era-interviews.md`。

### RAG / 检索增强(技术岗)
1. 设计一个基于内部文档的问答系统,如何控制幻觉率?(考察:检索质量/引用溯源/拒答机制)
2. 你的 RAG 召回率不错但答案质量差,排查思路?(考察:重排/chunk 策略/上下文预算)
3. 知识库每天更新,如何保证索引新鲜度与成本平衡?(考察:增量索引/缓存失效)

### Agent / 系统(技术岗)
4. 设计一个能自动处理退款工单的 agent,失败恢复怎么做?(考察:状态机/幂等/人工兜底)
5. 多步 agent 中途工具超时,重试还是回退?依据是什么?(考察:错误分类/预算控制)
6. 怎么防止 agent 被用户输入里藏的指令劫持?(考察:注入防御/权限边界)

### Evals / 质量(技术岗+产品岗)
7. 你怎么证明新 prompt 比旧的好?(考察:数据集构建/指标选取/统计显著性)
8. 线上模型质量疑似回退,但没有报错,怎么定位?(考察:回归集/漂移监控)
9. 主观任务(如文案生成)怎么做自动化评估?(考察:LLM-judge 及其偏差)

### 成本与工程(技术岗)
10. 推理成本要砍一半,你有哪些手段?各损失什么?(考察:缓存/蒸馏/路由/量化 trade-off)
11. P99 延迟 8 秒的 LLM 功能,产品要求 2 秒,怎么办?(考察:流式/预取/异步化)

### 产品与判断(产品岗+通用)
12. 什么功能不该用 LLM 做?举一个你判断"不用 AI"的例子。(考察:技术判断力/成本意识)
13. 用户投诉 AI 功能"一本正经胡说",你的处理框架?(考察:预期管理/兜底设计)

### 通用(任何岗位)
14. 你平时怎么用 AI 提高工作效率?给一个具体例子。(考察:真实使用深度;要求带产出数字)
15. 如果这个岗位一半的日常工作明年被 AI 接管,你怎么规划自己的价值?(考察:成长心态/不设防的诚实)
