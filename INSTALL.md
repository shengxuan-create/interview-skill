# 安装说明 / Installation Guide

---

## Claude Code（推荐 / Recommended）

> **重要**：Claude Code 从 git 仓库根目录的 `.claude/skills/` 查找 skill。
> **Important**: Claude Code looks for skills in `.claude/skills/` from the git repo root.

```bash
# 在 git 仓库根目录执行 / Run from git repo root
cd $(git rev-parse --show-toplevel)

# 方式1：安装到当前项目 / Install to current project
mkdir -p .claude/skills
git clone https://github.com/shengxuan-create/interview-skill .claude/skills/interview-skill

# 方式2：安装到全局 / Install globally
git clone https://github.com/shengxuan-create/interview-skill ~/.claude/skills/interview-skill
```

然后输入 `/interview-prep` 或说「帮我准备面试」即可启动。
Then type `/interview-prep` or say "Help me prepare for an interview" to start.

---

## OpenClaw

```bash
git clone https://github.com/shengxuan-create/interview-skill ~/.openclaw/workspace/skills/interview-skill
```

---

## Cursor / Codex

按照各平台的 Agent Skills 安装方式，将本仓库克隆到对应 skills 目录即可。
Follow each platform's Agent Skills installation method and clone this repo to the appropriate skills directory.

---

## 依赖安装 / Dependencies

```bash
# 基础依赖（推荐安装）/ Core dependencies (recommended)
pip3 install requests beautifulsoup4

# PDF简历解析（可选）/ PDF resume parsing (optional)
pip3 install pdfplumber

# 或一次性安装全部 / Or install all at once
pip3 install -r requirements.txt
```

| 包 / Package | 用途 / Purpose | 必须？/ Required? |
|---|---|---|
| `requests` | HTTP请求，用于JD抓取和面经搜索 | 推荐 / Recommended |
| `beautifulsoup4` | HTML解析，提取JD结构化信息 | 推荐 / Recommended |
| `pdfplumber` | 解析PDF简历 | 可选 / Optional |

---

## 验证安装 / Verify Installation

```bash
cd .claude/skills/interview-skill  # 或你的安装路径

# 测试工具
python3 tools/jd_parser.py --help
python3 tools/interview_scraper.py --help
python3 tools/prep_writer.py --action list --base-dir ./preps
```

---

## 常见问题 / Troubleshooting

| 报错 / Error | 原因 / Cause | 解决 / Fix |
|---|---|---|
| `ModuleNotFoundError: requests` | 依赖未装 | `pip3 install requests` |
| `ModuleNotFoundError: bs4` | bs4未装 | `pip3 install beautifulsoup4` |
| `ModuleNotFoundError: pdfplumber` | PDF依赖未装 | `pip3 install pdfplumber`（仅在需要解析PDF简历时） |
| WebSearch无结果 | 网络限制 | 检查代理/VPN设置，确保可访问外网 |
| PDF简历解析失败 | 格式不支持 | 改用粘贴简历文本的方式 |
| Skill未触发 | 安装路径不对 | 确认在 `.claude/skills/interview-skill/` 下有 `SKILL.md` |
