# /总结 v4.0 — 精炼 · 进度 · 自进化

> **Condense · Progress · Self-Evolve** — 任务开发超过1天，扫一眼就了解会话全貌。
> Essential for 1+ day dev tasks. One glance tells you everything.

[![Version](https://img.shields.io/badge/version-4.0.0-blue)](VERSION)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-ZCode%20%7C%20Claude%20Code-lightgrey)]()

---

## Overview / 概述

**EN**: A ZCode skill that condenses long sessions into a glanceable summary — progress, key decisions, file changes, and error-driven self-evolution. Triggered by `/总结`. Designed to be indispensable for multi-day development sessions.

**CN**: 精炼长对话为一眼可读的摘要——进度、关键决策、文件变更、错误驱动的自进化。输入`/总结`触发。专为超1天任务开发设计，必备工具。

### Core Capabilities / 核心能力

| Feature | 功能 |
|---------|------|
| 🗜️ **Session Condense** | 会话精炼 — ≤5句关键摘要 + 涉文件清单 + 关键决策 |
| 📋 **Task Progress** | 任务进度 — 完成/待办/下一步 + 压力等级 |
| ⚡ **Error Self-Evolve** | 错误自进化 — 5维分类 + 规则回测 + 全局/项目分流 |

**设计原则**: 一句话能表达清楚绝不用两句。`/总结`完整输出≤15行，`/总结 统计`≤5行。

---

## Architecture / 架构

```
/总结 触发
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
│   错误检测 → 全局(AGENTS.md) / 项目(.zcode) │
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
│   └── rules.md              # ⚡ 进化规则（P0/P1/项目）
└── harvests/                 # 运行时数据 / Runtime data
    ├── index.md              # 收割索引
    ├── error-ledger.md       # 全局错误账本
    ├── _self-stats.md        # 自反馈统计
    └── {project}/
        ├── errors.md         # 项目错误账本
```

---

## Usage / 使用方式

### Commands / 触发

| 触发 / Trigger | Output / 产出 |
|----------------|---------------|
| `总结` 或 `summarize` | 3模块完整输出（≤15行） |
| `总结 统计` | 错误分布+进化状态（≤5行） |

> ⚠️ 只认独立词：单独打出 `总结` 或 `summarize`（前后空格/标点）即触发。在句子中不触发。

### Auto-Reminder / 主动提醒

| Condition | Threshold | Message |
|-----------|:--------:|---------|
| 会话轮次过多 | ≥20 rounds | 💡 已{N}轮，建议/总结 |
| 错误频繁 | ≥3 errors | ⚠️ 已{N}个错误，建议/总结 |
| 工具调用密集 | ≥30 calls | 🔧 {N}次调用，建议/总结 |

---

## Error Classification / 错误分类体系

| Code | Category | 分类 | Example |
|:----:|----------|------|---------|
| PROC | Process Violation | 流程违规 | Edit without Read, claiming done without verification |
| ASSU | Assumption Error | 假设错误 | Fabricating API names, assuming file paths exist |
| ENVR | Environment Issue | 环境问题 | GitHub blocked, cmd.exe doesn't support Unix commands |
| TOOL | Tool Misuse | 工具误用 | Using Bash instead of Grep, old_string mismatch |
| KNOW | Knowledge Gap | 知识盲区 | Unfamiliar with conventions, missing project context |

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

## Changelog / 变更日志

### v4.0.0 (2026-06-18) — 精炼版

**Major: 5 modules → 3 core modules. Line count 275→133 (-52%).**

- 🗜️ **New: Session Condense (模块1)** — ≤5句关键摘要 + 文件清单 + 关键决策
- 📋 **New: Task Progress (模块2)** — 完成/待办/下一步 + 压力等级
- ⚡ **New: Error Self-Evolve (模块3)** — 5维分类 + 规则回测 + 全局/项目分流
- ❌ **Removed** — 技能库扫描(Module 4.3), Memory Bank收割格式, 版本检查
- ❌ **Removed** — 6个冗余参考文件 (harvest-format, optimization-triggers, example-output, error-record-spec, harvest-workflow, rule-template)
- ✅ **Strengthened** — 极简输出原则: `/总结`≤15行, `/总结 统计`≤5行
- ✅ **Bilingual** — 中英双语技能描述，国际化支持

### v3.0.0 (2026-06-17)

- Backtest verification, three-level error scoping, skill self-evolution
- 9 modules → 5 modules

### v2.0.0 (2026-06-16)

- Memory Bank harvest format, 5-dimension classification, sub-commands

### v1.0.0

- Basic session diagnosis and progress tracking

---

## Installation / 安装

### 一键安装（全平台通用）

```bash
curl -sL https://raw.githubusercontent.com/gtbwpkwjnb-alt/summarize-skill/master/install.sh | bash
```

Windows PowerShell:

```powershell
iwr https://raw.githubusercontent.com/gtbwpkwjnb-alt/summarize-skill/master/install.ps1 | iex
```

### 手动安装

```bash
git clone git@github.com:gtbwpkwjnb-alt/summarize-skill.git ~/.agent-skills/summarize
```

### 更新

```bash
cd ~/.agent-skills/summarize && git pull
```

或运行`/总结 统计`自动检测 GitHub 新版本。安装后输入`/总结`即可触发。

---

## 反馈 / Feedback

🐛 [GitHub Issues](https://github.com/gtbwpkwjnb-alt/summarize-skill/issues/new)

---

## License

MIT — see [LICENSE](LICENSE) file.