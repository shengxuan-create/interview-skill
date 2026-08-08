# 安装说明 / Installation Guide

> 根据你使用的 Claude 形态选择安装方式 / Choose based on your Claude client.

| 你在用 / You're using | 走哪条路 / Which section |
|---|---|
| 🟢 **Claude Desktop / Cowork** （桌面 app） | [→ Claude Desktop / Cowork](#claude-desktop--cowork-推荐--recommended) |
| 🛠 **Claude Code**（终端 CLI） | [→ Claude Code](#claude-code) |
| 🐳 **OpenClaw** | [→ OpenClaw](#openclaw) |
| 📝 **Cursor / Codex** | [→ Cursor / Codex](#cursor--codex) |

---

## Claude Desktop / Cowork（推荐 / Recommended）

> ⚠️ **Cowork / Claude Desktop 不读 `~/.claude/skills/` 目录！** Skill 必须通过 app 内的 Upload skill 弹窗上传 zip 安装。
> ⚠️ **Cowork / Claude Desktop does NOT read `~/.claude/skills/`!** Skills must be installed via the in-app Upload skill dialog as a zip.

### 步骤 / Steps

1. **下载 zip / Download zip**
   - 打开 [GitHub Releases](https://github.com/shengxuan-create/interview-skill/releases/latest)
   - 下载 `interview-skill-vX.X.X.zip`

2. **打开 Upload skill 弹窗 / Open Upload skill dialog**
   - Claude Desktop → **Settings** → **Capabilities** → **Skills** → **Upload skill**

3. **拖入 zip / Drag the zip**
   - 把刚下载的 zip 拖到弹窗的虚线框，或点击虚线框选择文件
   - Drag the zip into the dashed dropzone, or click to file-pick

4. **完全退出 Claude，再重新打开 / Fully quit Claude, then reopen**
   - macOS: `Cmd+Q`（不是关窗口）→ 重新打开 Claude
   - Windows / Linux: `Ctrl+Q` → reopen
   - ⚠️ **仅重启会话不够 / Restarting the session alone is NOT enough** —— 必须退出整个 app，新装的 skill 才会被加载

5. **触发 skill / Trigger the skill**
   - 在新会话中输入 / In a new conversation, type:
     - 中文：「帮我准备 Google 的 SWE 面试」
     - English: "Help me prepare for a Google SWE interview"

### 常见问题 / Troubleshooting

| 报错 / Error | 原因 / Cause | 解决 / Fix |
|---|---|---|
| `Zip must contain exactly one SKILL.md file` | 上传的 zip 不是从 Releases 下载的，是自己 git clone 后压缩的，包含示例 prep 里的额外 SKILL.md | 用本仓库 [Releases 页面](https://github.com/shengxuan-create/interview-skill/releases/latest) 的官方 zip，已经处理过 |
| 安装后 skill 列表里找不到 | 没有完全退出 app | `Cmd+Q` 退出 Claude，重新打开 |
| 触发后 skill 没响应 | 当前会话是装 skill 之前开的 | 开一个新会话再试 |

---

## Claude Code

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
