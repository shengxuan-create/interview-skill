# Competency Taxonomy — 能力标签体系

> 供 storybank_manager.py 做故事匹配和缺口分析使用。
> 每个能力标签定义了：含义、常见面试问题关键词、公司特定映射。

---

## 核心能力标签 / Core Competencies

### leadership
- **定义**: 带领团队达成目标，做决策，承担责任
- **关键词**: led, managed, directed, drove, spearheaded, team lead, took charge, coordinated
- **常见问题**: "Tell me about a time you led...", "Describe when you had to take charge..."
- **公司映射**:
  - Amazon LP: Hire and Develop the Best, Have Backbone
  - Google: Googleyness (collaboration + leadership)
  - Meta: Focus on Impact

### conflict
- **定义**: 处理人际冲突、意见分歧、跨团队矛盾
- **关键词**: disagreed, conflict, pushed back, opposing views, tension, compromise, negotiate
- **常见问题**: "Tell me about a time you disagreed with...", "How do you handle conflict..."
- **公司映射**:
  - Amazon LP: Have Backbone; Disagree and Commit
  - Google: Googleyness (respectful disagreement)

### failure
- **定义**: 项目失败、错误决策、未达目标，及从中学到的教训
- **关键词**: failed, mistake, wrong, missed deadline, underperformed, learned from, setback
- **常见问题**: "Tell me about a time you failed...", "Describe your biggest mistake..."
- **公司映射**:
  - Amazon LP: Learn and Be Curious, Insist on the Highest Standards
  - Google: Growth mindset, intellectual humility

### teamwork
- **定义**: 跨职能协作、团队合作、支持他人
- **关键词**: collaborated, cross-functional, partnered, together, helped, supported, aligned
- **常见问题**: "How do you work in a team...", "Tell me about successful collaboration..."
- **公司映射**:
  - Amazon LP: Earn Trust
  - Google: Googleyness (collaboration)
  - Meta: Be Open

### customer_obsession
- **定义**: 以客户/用户为中心做决策，深入理解用户需求
- **关键词**: customer, user, client, feedback, user research, NPS, retention, experience
- **常见问题**: "Tell me about a time you went above and beyond for a customer..."
- **公司映射**:
  - Amazon LP: Customer Obsession (LP #1)
  - Google: Focus on the user
  - Meta: Build Social Value

### innovation
- **定义**: 提出新方案、挑战现状、创造性解决问题
- **关键词**: innovative, creative, new approach, rethought, redesigned, proposed, invented
- **常见问题**: "Tell me about a time you came up with a creative solution..."
- **公司映射**:
  - Amazon LP: Invent and Simplify
  - Google: 10x thinking
  - Apple: Innovation, Think Different

### communication
- **定义**: 清晰表达、说服他人、向非技术受众解释技术概念
- **关键词**: presented, explained, convinced, articulated, stakeholder, demo, written
- **常见问题**: "How do you explain complex topics...", "Tell me about a difficult conversation..."
- **公司映射**:
  - All companies value this
  - Amazon LP: Earn Trust (through clear communication)

### technical_decision
- **定义**: 做技术选型、架构决策、权衡 trade-off
- **关键词**: architecture, chose, trade-off, evaluated, designed, scalability, migration
- **常见问题**: "Walk me through a technical decision you made...", "How did you choose..."
- **公司映射**:
  - Google: Technical depth + thinking process
  - Meta: Move Fast (pragmatic choices)
  - Amazon LP: Dive Deep

### mentoring
- **定义**: 指导他人成长、知识分享、培养团队
- **关键词**: mentored, coached, taught, onboarded, grew, developed, pair programming
- **常见问题**: "Tell me about a time you mentored someone..."
- **公司映射**:
  - Amazon LP: Hire and Develop the Best
  - Google: Googleyness (supporting others)

### ambiguity
- **定义**: 在信息不完整或需求不明确的情况下做决策和推进
- **关键词**: ambiguous, unclear, uncertain, no direction, figured out, scoped, defined
- **常见问题**: "Tell me about a time you had to work with ambiguity..."
- **公司映射**:
  - Amazon LP: Bias for Action
  - Startup: essential trait
  - Google: Navigating complexity

### ownership
- **定义**: 主动承担超出职责范围的工作，端到端负责
- **关键词**: owned, end-to-end, took initiative, volunteered, beyond my role, responsible
- **常见问题**: "Tell me about a time you took ownership beyond your job description..."
- **公司映射**:
  - Amazon LP: Ownership (LP #2)
  - Startup: "wear multiple hats"
  - Meta: Focus on Impact

### influence_without_authority
- **定义**: 在没有直接管理权的情况下推动他人行动
- **关键词**: influenced, persuaded, aligned, no authority, cross-team, buy-in, stakeholder
- **常见问题**: "Tell me about a time you had to convince others without authority..."
- **公司映射**:
  - Amazon LP: Earn Trust, Have Backbone
  - All large companies with matrix structures

### prioritization
- **定义**: 在资源有限时做取舍，管理多个优先级
- **关键词**: prioritized, trade-off, deadline, competing, triaged, said no, focused, scoped
- **常见问题**: "How do you prioritize when everything is urgent..."
- **公司映射**:
  - Amazon LP: Deliver Results, Frugality
  - Startup: resource constraints
  - Meta: Move Fast

### adaptability
- **定义**: 应对变化、快速学习新技术/领域、调整计划
- **关键词**: adapted, pivoted, changed, new technology, learned quickly, shifted, flexible
- **常见问题**: "Tell me about a time you had to quickly adapt..."
- **公司映射**:
  - Startup: essential trait
  - Amazon LP: Learn and Be Curious
  - Meta: Move Fast

### ethical_dilemma
- **定义**: 面对道德或价值观冲突时的决策
- **关键词**: ethical, right thing, integrity, pushback, transparency, honest, principle
- **常见问题**: "Tell me about a time you had to make an ethical decision..."
- **公司映射**:
  - Amazon LP: Insist on the Highest Standards, Earn Trust
  - All companies in regulated industries (finance, healthcare)

---

## 使用说明

**storybank_manager.py match 算法**：
1. 从问题文本中提取关键词
2. 与上述每个能力标签的关键词列表做模糊匹配
3. 匹配到的能力标签与故事的 competencies 做交集
4. 如果指定了 company-culture，额外加权该公司重视的能力标签
5. 最终排序：competency_match_score × 0.5 + culture_alignment × 0.3 + story_strength × 0.2
