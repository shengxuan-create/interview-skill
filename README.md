<div align="center">

# interview-skill

> 面试准备 skill:**调研公司不编造 · STAR 评分带锚点 · 答案去 AI 味 · AI 面试官轮应对**
> 帮你自己拿 offer,不是帮公司招人。中英双语。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.0.0-orange.svg)](CHANGELOG.md)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

[**English**](README_EN.md) · [安装说明](INSTALL.md) · [更新日志](CHANGELOG.md) · [架构文档](docs/ARCHITECTURE.md)

</div>

<div align="center">
  <img src="assets/demo-scoring.png" alt="interview-skill 对一段 STAR 回答的评分:逐维度打分、指出「加班是负面信号」、给出改写骨架" width="100%">
  <sub>真实输出,未经修饰。一次 STAR 评分:逐维度扣分 → 点破隐藏问题 → 给改写骨架。</sub>
</div>

---

## 为什么不是「直接问 AI」就够了

**AI 会编公司信息。** 你问「这家公司面试常问什么」,得到的列表里有真的,也有它根据全网面经平均出来的,你分不清——但拿着它进考场的是你。这个 skill 的公司简报里,每条信息都带来源和置信度标签(HIGH / MEDIUM / LOW / GAP);查不到就写 GAP 并建议你直接问 recruiter,**绝不编一个看起来很像的**。一份 60% 覆盖但全可信的简报,比一份 100% 覆盖混着幻觉的有用得多。

**评分会漂移。** 没有锚点的打分,连着看几个好答案就变严、看几个差答案就变松。这里的 STAR 评分先读两个锚定示例(一个 4 分、一个 2 分)再打分,打完还回看分布——六道题全同一个分,说明尺子坏了,重评。

**面试官现在听得出 AI 写的答案。** 三段排比、每段结尾「这体现了我的 XX 能力」、全程零失误的叙事。一段被听出 AI 味的「完美回答」,比一段朴素的真实回答伤害大。生成的参考答案交付前会过一遍去 AI 味清单。

**AI 面试官轮是新战场。** 异步视频面每题 90 秒、前 15 秒权重最高;live coding 有的公司禁用 Copilot、有的要求你用。这两种情况的准备方式完全不同,skill 里都有对应打法。

## v2.0 新特性

- **AI 时代面试**:AI 面试官轮(异步视频面)应对、live coding 的 AI 使用政策两派打法、AI 岗 15 道新题型
- **证据纪律**:公司简报只登记来源页逐字出现的信息,搜不到就标 GAP——绝不编造高频题
- **评分校准**:STAR 评分带 4 分/2 分锚定示例,分数不漂移
- **答案去 AI 味**:参考回答交付前过 8 项 humanize 清单(可接 humanizer skill)
- **架构瘦身**:SKILL.md 1616 → 87 行路由器,按需加载;新增 AGENTS.md 支持 Codex/Cursor
- **触发准确率 100%**(优化前 92%/88%):20 条真实 query × 3 次实测 × 训练-测试切分
- 详见 [CHANGELOG.md](CHANGELOG.md)

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
