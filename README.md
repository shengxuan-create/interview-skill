<div align="center">

# interview-skill

> 面试助手——自动调研目标公司，生成定制化面试准备材料，模拟真实面试，STAR框架逐题评分。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

[**English**](README_EN.md) · [安装说明](INSTALL.md) · [架构文档](docs/ARCHITECTURE.md)

</div>

---

## 和手动准备的区别

| | 自己搜 | interview-skill |
|---|---|---|
| 搜索 | 一个query碰运气 | 5个维度，每个维度3条query，共15次搜索 |
| 结果 | 10条链接自己挑 | 自动评分过滤，只留高质量信息 |
| 分析 | 自己看完自己总结 | 跨15+条面经统计，标注置信度 |
| 题目 | 通用面试题 | 针对该公司、该职位、该轮次定制 |
| 练习 | 没有反馈 | AI按该公司面试官风格追问，逐题评分 |

## 功能

- **4层Research Engine** — 多维搜索 → 评分过滤 → 交叉验证 → 用户补充
- **面经统计分析** — 跨多条面经做统计（比如"12/15条来源提到System Design"→ 大概率考）
- **STAR框架评分** — 模拟面试后逐题打分1-5，给改进建议和参考答案
- **模拟面试** — AI扮演该公司面试官风格，追问细节，不给提示
- **面后复盘** — 真实面试结束后回填真题，数据回流，下次更准
- **中英双语** — 根据你第一句话的语言自动切换

## Quick Start

### 🟢 Claude Desktop / Cowork 用户（最简单）

1. **下载** [最新 Release 的 zip 包](https://github.com/shengxuan-create/interview-skill/releases/latest)（`interview-skill-vX.X.X.zip`）
2. 在 Claude 桌面端打开 **Settings → Capabilities → Skills → Upload skill**
3. **拖入 zip 文件**到弹窗的虚线框
4. **完全退出 Claude 应用**（Cmd+Q / Ctrl+Q），然后**重新打开** —— ⚠️ 仅重启会话不够，必须退出整个 app
5. 新会话中输入：「帮我准备 Google 的 SWE 面试」即可触发

> ⚠️ **不要 git clone 到 `~/.claude/skills/`** —— Cowork / Claude Desktop 不读那个目录，必须通过 Upload skill 弹窗上传 zip 安装。

### 🛠 Claude Code（CLI 用户）

```bash
# 安装到Claude Code当前项目
mkdir -p .claude/skills
git clone https://github.com/shengxuan-create/interview-skill .claude/skills/interview-skill

# 安装依赖（可选）
pip3 install -r .claude/skills/interview-skill/requirements.txt
```

在Claude Code中输入：

```
帮我准备Google的SWE面试
```

Skill会自动引导你完成全部流程。

> 📖 详细安装说明（含 OpenClaw / Cursor / Codex）：[INSTALL.md](INSTALL.md)

## 项目结构

```
interview-skill/
├── SKILL.md              # 入口（AgentSkills标准frontmatter）
├── prompts/              # 14个Prompt模板（7步主流程+进化/纠正/复盘）
├── tools/                # 7个Python工具（JD解析/面经聚合/简历分析等）
├── references/           # 4个参考文档（STAR框架/题库/公司文化/面试形式）
├── preps/                # 生成的面试准备材料（含3组完整示例）
├── evals/                # 触发测试用例
└── docs/                 # 架构文档
```

## 管理命令

| 命令 | 说明 |
|------|------|
| `/interview-prep` | 开始新的面试准备 |
| `/mock {slug}` | 对已有prep进行模拟面试 |
| `/update-prep {slug}` | 追加新面经或情报 |
| `/list-preps` | 列出所有已生成的prep |
| `/prep-rollback {slug} {v}` | 回滚到历史版本 |
| `/debrief {slug}` | 面试结束后复盘 |

## 兼容平台

Claude Code · OpenClaw · Cursor · Codex

## 注意事项

- 搜索结果依赖网络，建议在有稳定网络的环境下使用
- 面经数据量因公司而异：FAANG等大公司信息丰富（A级），小公司可能较少（C/D级）
- 模拟面试质量取决于面经数据量——面后复盘可以让真题回流，逐步改善
- LeetCode高频题追踪依赖公开数据，可能不完全准确

## License

MIT © [shengxuan-create](https://github.com/shengxuan-create)
