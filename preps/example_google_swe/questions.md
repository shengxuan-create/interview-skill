# Google SWE L4 — 面试题库

> 共21题：Behavioral 8 + Technical/Coding 8 + System Design 3 + Situational 2

---

## Behavioral Questions（基于Googleyness & Leadership）

1. **[HIGH频] Tell me about a time you led a project with ambiguous requirements.**
   - 考察点：leadership, navigating ambiguity
   - Google偏好：重视你如何主动clarify而非等指示
   - 参考思路：STAR框架，强调主动性和structured approach

2. **[HIGH频] Describe a time you had a conflict with a teammate. How did you resolve it?**
   - 考察点：collaboration, conflict resolution
   - Google偏好：看你是否能maintain psychological safety
   - 参考思路：强调理解对方perspective + data-driven resolution

3. **[HIGH频] Tell me about a time you failed. What did you learn?**
   - 考察点：humility, growth mindset, self-awareness
   - Google偏好：Googleyness核心——intellectual humility
   - 参考思路：选有impact的失败，重点在learning和后续改进

4. **[MEDIUM频] Describe a situation where you went above and beyond.**
   - 考察点：initiative, ownership
   - Google偏好：10x thinking — 不只完成任务，而是超预期
   - 参考思路：展示你看到了别人没看到的机会
5. **[MEDIUM频] Tell me about a time you had to make a decision with incomplete data.**
   - 考察点：decision-making under uncertainty
   - Google偏好：balanced risk-taking + data awareness
   - 参考思路：说明你如何assess risk和seek signal

6. **[MEDIUM频] How do you handle competing priorities from different stakeholders?**
   - 考察点：prioritization, communication
   - 参考思路：展示framework-based prioritization

7. **[MEDIUM频] Describe how you mentored or helped grow a junior engineer.**
   - 考察点：mentorship, leadership at L4
   - Google偏好：L4开始看leadership signal
   - 参考思路：具体的mentoring行为和对方的成长

8. **[LOW频] Why Google? Why this team?**
   - 考察点：motivation, culture fit
   - 参考思路：genuine connection to Google's mission + specific team interest

---

## Technical / Coding Questions

1. **[HIGH频] Design and implement an LRU Cache (LeetCode #146)**
   - 考察点：data structures, hash map + doubly linked list
   - 难度：Medium
   - 时间：25min coding + 5min follow-up
   - Follow-up：How would you make it thread-safe?

2. **[HIGH频] Given a grid, count the number of islands (LeetCode #200)**
   - 考察点：BFS/DFS, graph traversal
   - 难度：Medium
   - Follow-up：What if the grid doesn't fit in memory?

3. **[HIGH频] Merge overlapping intervals (LeetCode #56)**
   - 考察点：sorting, interval logic
   - 难度：Medium
   - Follow-up：Streaming version — intervals arrive one by one
4. **[MEDIUM频] Find all courses you can finish given prerequisites (LeetCode #207)**
   - 考察点：topological sort, cycle detection
   - 难度：Medium
   - Follow-up：Return the actual ordering (LeetCode #210)

5. **[MEDIUM频] Serialize and Deserialize a Binary Tree (LeetCode #297)**
   - 考察点：tree traversal, serialization design
   - 难度：Hard
   - Follow-up：What encoding minimizes space?

6. **[MEDIUM频] Minimum number of coins to make a given amount (LeetCode #322)**
   - 考察点：dynamic programming
   - 难度：Medium
   - Follow-up：Print the actual coins used

7. **[MEDIUM频] Meeting Rooms II — minimum conference rooms needed (LeetCode #253)**
   - 考察点：interval scheduling, heap/priority queue
   - 难度：Medium

8. **[LOW频] Implement a trie with insert, search, and startsWith (LeetCode #208)**
   - 考察点：trie data structure
   - 难度：Medium

---

## System Design Questions

1. **[HIGH频] Design a URL shortener (like bit.ly)**
   - 考察点：hashing, database design, caching, scalability
   - L4标准：清晰的高层设计 + 基本scalability考虑
   - 时间分配：5min需求 + 15min高层 + 15min深入 + 5min扩展
   - 重点讨论：hash collision, read-heavy优化, analytics

2. **[HIGH频] Design a web crawler**
   - 考察点：distributed systems, queue management, deduplication
   - 重点讨论：politeness policy, URL frontier, fault tolerance

3. **[MEDIUM频] Design Google Docs (collaborative editing)**
   - 考察点：CRDT/OT, real-time sync, conflict resolution
   - 注意：这是Google内部产品，展示对其技术挑战的理解

---

## Situational Questions

1. **You join a new team and find the codebase has no tests. What do you do?**
   - 考察点：engineering judgment, initiative, pragmatism
   - 参考思路：不是一来就重写，而是incrementally improve + earn trust

2. **Your tech lead proposes a design you disagree with. How do you handle it?**
   - 考察点：communication, assertiveness with respect
   - 参考思路：先理解context → 用data提出alternative → respect final decision