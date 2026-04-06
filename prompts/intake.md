# Step 1: 信息收集 / Intake

> **Previous**: None (entry point) | **Next**: Step 2 resume_matcher.md (if resume provided) or Step 3a search_strategist.md

Ask the user 5 questions. All questions except Q1 and Q2 can be skipped.
Summarize answers and confirm before proceeding.

---

## Q1：目标公司（必填 / Required）
```
你要面哪家公司？/ Which company are you interviewing at?
例 / Example：Google / 字节跳动 / https://careers.google.com/jobs/xxx
```

## Q2：目标职位（必填 / Required）
```
什么职位？/ What role?
例 / Example：Software Engineer L4 / 后端工程师 / Product Manager
```

## Q3：JD来源 / JD Source（5种方式，可跳过 / 5 options, skippable）
```
有JD吗？怎么提供？/ Do you have a JD? How to provide it?

  [A] 粘贴JD文本 / Paste JD text
  [B] 给URL（LinkedIn/Indeed/官网），自动抓取 / Give URL, auto-fetch
  [C] 上传PDF/截图 / Upload PDF or screenshot
  [D] 手动描述（大概要求和技术栈）/ Describe manually
  [E] 跳过 / Skip
```

Processing rules:
- A → Use as text directly
- B → `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/jd_parser.py --url {url} --output /tmp/jd_parsed.json`
- C → `Read` tool to read PDF/image
- D → Use as text directly
- E → Skip, use generic framework later

## Output

After collecting all answers, summarize and confirm with the user before proceeding:

```
收集到的信息 / Information Collected:
  - 公司 / Company: {company}
  - 职位 / Role: {role}
  - JD: {provided / skipped}
  - 面试轮次 / Round: {round or "未指定"}
  - 简历 / Resume: {provided / skipped}

确认以上信息正确？/ Confirm and proceed?
```

Pass confirmed data to Step 2 (resume_matcher) if resume was provided, otherwise to Step 3a (search_strategist).
