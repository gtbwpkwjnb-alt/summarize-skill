# /总结 v5.0 — 精炼 · 进度 · 自进化（多平台通用）

> **Condense · Progress · Self-Evolve** — 任务开发超过1天，扫一眼就了解会话全貌。
> Essential for 1+ day dev tasks. One glance tells you everything.
> **跨平台**: ZCode · Claude Code · Codex · Cursor · Windsurf

[![Version](https://img.shields.io/badge/version-5.0.0-blue)](VERSION)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-ZCode%20%7C%20Claude%20Code%20%7C%20Codex%20%7C%20Cursor%20%7C%20Windsurf-lightgrey)]()
[![skills.sh](https://img.shields.io/badge/skills.sh-listed-6f42c1)](https://skills.sh/gtbwpkwjnb-alt/summarize-skill)

---

## Overview / 概述

**EN**: A multi-platform agent skill that condenses long sessions into a glanceable summary — progress, key decisions, file changes, and error-driven self-evolution. Triggered by standalone `总结` or `summarize`. Designed to be indispensable for multi-day development sessions. Works across ZCode, Claude Code, Codex, Cursor, and Windsurf.

**CN**: 跨平台 AI 编程助手技能，精炼长对话为一眼可读的摘要——进度、关键决策、文件变更、错误驱动的自进化。单独输入`总结`或`summarize`触发。专为超1天任务开发设计。支持 ZCode / Claude Code / Codex / Cursor / Windsurf。

### Core Capabilities / 核心能力

| Feature | 功能 |
|---------|------|
| 🗜️ **Session Condense** | 会话精炼 — ≤5句关键摘要 + 涉文件清单 + 关键决策 |
| 📋 **Task Progress** | 任务进度 — 完成/待办/下一步 + 压力等级 |
| ⚡ **Error Self-Evolve** | 错误自进化 — 5维分类 + 规则回测 + 全局/项目分流 |

**设计原则**: 一句话能表达清楚绝不用两句。`总结`完整输出≤15行，`总结 统计`≤5行。

---

## 触发方式（按平台）

| 平台 | 触发方式 | 示例 |
|------|---------|------|
| **ZCode** | 独立词 `总结` 或 `summarize` | `> 总结` |
| **Claude Code** | 建议配置 `/summarize` 别名 | `> /summarize` |
| **Codex (OpenAI)** | 独立词 `总结` 或 `summarize` | `> 总结` |
| **Cursor** | 建议配置 `@summarize` 命令 | `> @summarize` |
| **Windsurf** | 独立词 `总结` 或 `summarize` | `> 总结` |
| **通用** | 在提示中引入"请总结当前会话" | |

> ⚠️ 只认独立词：单独打出 `总结` 或 `summarize`（前后空格/标点）即触发。在句子中不触发。

### Auto-Reminder / 主动提醒

| Condition | Threshold | Message |
|-----------|:--------:|---------|
| 会话轮次过多 | ≥20 rounds | 💡 已{N}轮，建议/总结 |
| 错误频繁 | ≥3 errors | ⚠️ 已{N}个错误，建议/总结 |
| 工具调用密集 | ≥30 calls | 🔧 {N}次调用，建议/总结 |

---

## Architecture / 架构

```
触发（按平台方式）
    │
    ├─ 模块1: 会话精炼 (Session Condense)         ← 核心
    ├─ 模块2: 任务进度 (Task Progress)             ← 核心
    └─ 模块3: 错误自进化 (Error Self-Evolve)       ← 核心
    
三级闭环 / Three Closed Loops:
┌─────────────────────────────────────────┐
│ 🔄 回测 / Backtest                       │
│   规则沉淀 → 下次验证 → 更新干净天数     │
├─────────────────────────────────────────┤
│ 📊 分级 / Scoping                        │
│   错误检测 → 全局 / 项目分流             │
├─────────────────────────────────────────┤
│ 🧬 自进化 / Self-Evolution               │
│   错误模式 → 规则建议 → 全局/项目分流     │
└─────────────────────────────────────────┘
```

### Error Storage / 错误存储层级

```
harvests/
  error-ledger.md              ← 全局错误（跨项目复用）
  {project}/
    errors.md                  ← 项目错误（仅本项目）
  _self-stats.md               ← 技能自身运行统计
  index.md                     ← 收割索引
```

---

## File Structure / 文件结构

```
summarize/
├── SKILL.md                  # 技能主文件 / Main skill definition
├── VERSION                   # 版本号 / Version
├── README.md                 # 本文件 / This file
├── references/
│   └── rules.md              # ⚡ 进化规则
└── harvests/                 # 运行时数据 / Runtime data
    ├── index.md              # 收割索引
    ├── error-ledger.md       # 全局错误账本
    ├── _self-stats.md        # 自反馈统计
    └── {project}/
        ├── errors.md         # 项目错误账本
```

---

## Error Classification / 错误分类体系（通用版）

| Code | Category | 分类 | 说明 |
|:----:|----------|------|------|
| PROC | Process Violation | 流程违规 | 跳过必要步骤 |
| ASSU | Assumption Error | 假设错误 | 用了未确认的标识符/路径 |
| ENVR | Environment Issue | 环境问题 | 网络/系统/权限限制 |
| TOOL | Tool Misuse | 工具误用 | 选了不适当的工具 |
| KNOW | Knowledge Gap | 知识盲区 | 缺乏领域/项目上下文 |

### Output Format / 输出格式

```
⚠️ 错误({N}):
| {错误} | {分类} | {N}次 | {标记}

🛡️ 规则:
✅ {规则} 干净+{N}
⚠️ {规则} 违反
🔄 {规则} 复发——修订建议:{行动}

⚡ 进化:
全局→ {规则建议}
项目→ {规则建议}
```

---

## Installation / 安装

### 一键安装（全平台通用，自动检测目标平台）

```bash
curl -sL https://raw.githubusercontent.com/gtbwpkwjnb-alt/summarize-skill/master/install.sh | bash
```

Windows PowerShell:

```powershell
iwr https://raw.githubusercontent.com/gtbwpkwjnb-alt/summarize-skill/master/install.ps1 | iex
```

安装脚本会自动检测当前平台（ZCode / Claude Code / Cursor / Codex / Windsurf）并安装到对应目录。如果检测不到，会回退到 `~/.agent-skills/summarize`。

### 手动安装

```bash
# ZCode
git clone git@github.com:gtbwpkwjnb-alt/summarize-skill.git ~/.zcode/skills/summarize

# Claude Code
git clone git@github.com:gtbwpkwjnb-alt/summarize-skill.git ~/.claude/skills/summarize

# Cursor
git clone git@github.com:gtbwpkwjnb-alt/summarize-skill.git ~/.cursor/agent-skills/summarize

# Codex
git clone git@github.com:gtbwpkwjnb-alt/summarize-skill.git ~/.codex/skills/summarize

# Windsurf
git clone git@github.com:gtbwpkwjnb-alt/summarize-skill.git ~/.windsurf/skills/summarize
```

### 更新

```bash
cd ~/.agent-skills/summarize && git pull
```

安装后输入`总结`或`summarize`即可触发。

---

## Platform Requirements / 平台前置条件

| 能力 | 是否必需 | 说明 |
|------|---------|------|
| 自定义技能/命令注入 | ✅ 必需 | 用于注入触发方式 |
| 文件系统读写 | ✅ 必需 | 存储收割数据和规则文件 |
| 会话历史访问 | ✅ 必需 | 模块1/2/3都需要读取当前会话 |
| 工具调用统计 API | 🟡 可选 | 模块3需要检测工具调用次数 |

如果平台不支持某些能力，对应模块会自动降级。

---

## Changelog / 变更日志

### v5.0.0 (2026-06-18) — 多平台通用版

- 🌍 **Major: 多平台通用化** — 支持 ZCode / Claude Code / Codex / Cursor / Windsurf
- 📦 **Multi-platform auto-detect installer** — 安装脚本自动检测目标平台
- 📋 **Platform trigger table** — SKILL.md/README 新增按平台触发表
- 🔧 **Generic error examples** — 5维分类例子去 ZCode 特化，改为通用说明
- 📚 **Platform requirements** — SKILL.md 新增平台前置条件说明
- 🔄 **保留 v4.x 所有功能** — 模块1/2/3 核心不变

### v4.1.0 (2026-06-18) — 自然词触发

- 🎯 **New: Natural word trigger** — `总结` / `summarize` standalone trigger replaces `/总结` slash command
- ⚠️ **Non-trigger** — 句子中出现不触发（如"总结一下今天的工作"）

### v4.0.0 (2026-06-18) — 精炼版

**Major: 5 modules → 3 core modules. Line count 275→133 (-52%).**

- 🗜️ **New: Session Condense (模块1)** — ≤5句关键摘要 + 文件清单 + 关键决策
- 📋 **New: Task Progress (模块2)** — 完成/待办/下一步 + 压力等级
- ⚡ **New: Error Self-Evolve (模块3)** — 5维分类 + 规则回测 + 全局/项目分流
- ✅ **Bilingual** — 中英双语技能描述，国际化支持

### v3.0.0 (2026-06-17)

- Backtest verification, three-level error scoping, skill self-evolution

### v2.0.0 (2026-06-16)

- Memory Bank harvest format, 5-dimension classification, sub-commands

### v1.0.0

- Basic session diagnosis and progress tracking

---

## 反馈 / Feedback

🐛 [GitHub Issues](https://github.com/gtbwpkwjnb-alt/summarize-skill/issues/new)

---

## License

MIT — see [LICENSE](LICENSE) file.