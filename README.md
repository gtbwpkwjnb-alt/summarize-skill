# /summarize — Session Diagnosis · Error Tracking · Self-Evolution Skill

> **/总结** — 会话诊断 · 错误追踪 · 自进化技能

[![Version](https://img.shields.io/badge/version-3.0.0-blue)](VERSION)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-ZCode%20%7C%20Claude%20Code-lightgrey)]()

---

## Overview / 概述

**EN**: A ZCode/Claude Code skill that diagnoses the current session, tracks errors across projects, harvests decisions & insights, and continuously evolves its own rules. Triggered by `/总结`.

**CN**: 一键诊断当前会话进度、跨项目追踪错误、收割决策与洞察、持续进化规则的 ZCode/Claude Code 技能。输入 `/总结` 触发。

### Core Capabilities / 核心能力

| Feature | 功能 |
|---------|------|
| 📋 **Progress Snapshot** | 进度快照 — 完成/进行/待做 + 下一步建议 |
| ⚠️ **Error Diagnosis** | 错误诊断 — 5维根因分类 + 自动检测 + 跨会话追踪 |
| 🛡️ **Backtest Verification** | 回测验证 — 检查已沉淀规则是否被遵守，追踪干净天数 |
| 🚜 **Experience Harvest** | 经验收割 — 决策/错误/洞察/规则 自动标注与持久化 |
| 🧬 **Rule Evolution** | 规则进化 — 三级作用域分流（全局/项目/代码） |
| 🔧 **Optimization Suggestions** | 优化建议 — 代码优化 + 技能自进化 |
| 🗜️ **Context Compression** | 上下文压缩 — 会话摘要，可复制到新会话续接 |

---

## Architecture / 架构

```
/总结 触发
    │
    ├─ 模块1: 进度快照 (Progress Snapshot)
    ├─ 模块2: 错误诊断 (Error Diagnosis) ← 含回测验证
    ├─ 模块3: 经验收割 (Experience Harvest)
    ├─ 模块4: 优化建议 (Optimization) ← 🆕 v3.0
    └─ 模块5: 上下文压缩 (Context Compression)
    
三级闭环 / Three Closed Loops:
┌─────────────────────────────────────────────┐
│ 🔄 回测 / Backtest                           │
│   规则沉淀 → 下次验证 → 更新days_clean       │
│   → 复发则修订规则                            │
├─────────────────────────────────────────────┤
│ 📊 分级 / Scoping                            │
│   错误检测 → 自动判断作用域                   │
│   → 全局(AGENTS.md) / 项目(.zcode) / 代码(建议) │
├─────────────────────────────────────────────┤
│ 🧬 自进化 / Self-Evolution                   │
│   模块使用统计 → 识别低价值模块               │
│   → 建议裁剪/增强 → 技能持续优化              │
└─────────────────────────────────────────────┘
```

### Error Storage / 错误存储层级

```
harvests/
  error-ledger.md              ← 全局错误（跨项目复用）
  {project}/
    errors.md                  ← 项目错误（仅本项目）
    YYYY-MM-DD-{id}.md         ← 会话收割文件
  _self-stats.md               ← 技能自身运行统计
  index.md                     ← 收割索引
```

---

## File Structure / 文件结构

```
summarize/
├── SKILL.md                  # 技能主文件 / Main skill definition
├── RULES.md                  # 进化规则（三级作用域）
├── VERSION                   # 版本号
├── README.md                 # 本文件 / This file
├── .gitignore                # 排除会话数据 / Exclude session data
├── references/
│   ├── harvest-format.md     # 收割文件格式规范
│   └── rule-template.md      # 规则卡片模板
└── harvests/                 # 运行时数据 / Runtime data
    ├── index.md              # 收割索引
    ├── error-ledger.md       # 全局错误账本
    ├── _self-stats.md        # 自反馈统计
    └── {project}/
        ├── errors.md         # 项目错误账本
        └── YYYY-MM-DD-*.md  # 会话收割文件 (gitignored)
```

---

## Usage / 使用方式

### Triggers / 触发命令

| Command / 命令 | Action / 行为 |
|----------------|---------------|
| `/总结` | 完整诊断（5 模块全部执行） |
| `/总结 历史` | 查看收割索引，按项目浏览 |
| `/总结 错误` | 查看错误账本（全局 + 本项目） |
| `/总结 统计` | 技能自身统计 + 自进化建议 |

### Auto-Reminder / 主动提醒

Even without explicit trigger, the skill proactively suggests running `/总结` when:

| Condition | Threshold | Message |
|-----------|:--------:|---------|
| 会话轮次过多 | ≥ 20 rounds | "💡 已 {N} 轮，建议 /总结 压缩上下文" |
| 错误频繁 | ≥ 3 errors | "⚠️ 本会话已 {N} 个错误，建议 /总结 收割经验" |
| 工具调用密集 | ≥ 30 calls | "🔧 工具调用 {N} 次，建议 /总结 归档进度" |

---

## Error Classification / 错误分类体系

| Code | Category | 分类 | Example |
|:----:|----------|------|---------|
| PROC | Process Violation | 流程违规 | Edit without Read, claiming done without verification |
| ASSU | Assumption Error | 假设错误 | Fabricating API names, assuming file paths exist |
| ENVR | Environment Issue | 环境问题 | GitHub blocked, cmd.exe doesn't support Unix commands |
| TOOL | Tool Misuse | 工具误用 | Using Bash instead of Grep, old_string mismatch |
| KNOW | Knowledge Gap | 知识盲区 | Unfamiliar with conventions, missing project context |

### Error Record Fields / 错误记录字段

```markdown
| 错误类型 | 次数 | 分类 | 首次 | 最近 | days_clean | 避免规则 | 已验证 | 涉及项目 | 状态 |
|---------|:---:|:--:|------|------|:--------:|---------|:-----:|---------|------|
```

- **days_clean**: Days since last occurrence (positive reinforcement)
- **避免规则 / Avoidance Rule**: Linked prevention rule ID
- **已验证 / Verified**: Whether the rule has been backtest-confirmed

---

## Changelog / 变更日志

### v3.0.0 (2026-06-17) — Current

**Major: 9 modules → 5 modules + 3 closed loops**

- 🔄 **New: Backtest verification** — checks if previously-established rules were followed
- 📊 **New: Three-level error scoping** — global/project/code separation
- 🧬 **New: Skill self-evolution** — module usage tracking, auto-suggests trimming
- 🔧 **New: Optimization suggestions** — code optimization based on error patterns
- ✅ Simplified module structure: 9→5 (removed noise, merged overlapping)
- ❌ Removed `/总结 审批` (never used)
- 📝 All "待办/TODO" changed to "建议/Suggestion" — user choice, not mandatory

### v2.0.0 (2026-06-16)

- Memory Bank 6-section harvest format
- 5-dimension root cause classification
- Error ledger with cross-session frequency tracking
- Rule approval workflow
- `/总结 历史` `/总结 错误` `/总结 统计` sub-commands

### v1.0.0

- Basic session diagnosis and progress tracking

---

## Installation / 安装

### 方法一：市场安装（推荐，跨平台通用）

> 🚧 即将上线 CCPM 市场，届时一条命令即可安装：
> ```
> /plugin install summarize@daymade/claude-code-skills
> ```

当前可用的跨平台安装方式：

```bash
# 任意平台，一行命令
git clone git@github.com:gtbwpkwjnb-alt/summarize-skill.git ~/.zcode-skills/summarize
```

> 目录名任意，AI 按 `SKILL.md` 的 `name: summarize` 字段识别，与路径无关。

### 方法二：按平台安装

| 平台 | 安装路径 |
|------|---------|
| **ZCode** | `~/.zcode/skills/summarize` |
| **Claude Code** | `~/.claude/skills/summarize` |
| **Cursor** | `~/.cursor/skills/summarize` |
| **Codex CLI** | `~/.codex/skills/summarize` |
| **Windsurf** | `~/.windsurf/skills/summarize` |
| **通用（推荐）** | `~/.zcode-skills/summarize` 或任意路径 |

```bash
git clone git@github.com:gtbwpkwjnb-alt/summarize-skill.git {你的平台路径}
```

安装后输入 `/总结` 即可触发。

---

## Distribution / 分发渠道

| 渠道 | 状态 | 安装方式 |
|------|:--:|------|
| GitHub Releases | ✅ 已发布 | `git clone` (见上方) |
| CCPM 市场 (daymade/claude-code-skills) | 🚧 待提交 | `/plugin install summarize` |
| claude-skill-registry | 🚧 待提交 | `sk install summarize` |
| Anthropic 社区插件 | 🚧 待提交 | `/plugin marketplace add` |

### 推荐管理工具

| 工具 | 用途 | 安装 |
|------|------|------|
| **[sutras](https://github.com/agentskills/sutras)** | 技能脚手架、校验、打包、发布 | `pip install sutras` |
| **[skillet](https://github.com/joshrotenberg/skillet)** | MCP 原生技能注册中心 + CLI | `cargo install skillet` |
| **[aigent](https://github.com/wkusnierczyk/aigent)** | 技能校验评分 (0-100) + 格式化 | `cargo install aigent` |
| **[skills-cli](https://pypi.org/project/skills-cli/)** | 创建、校验、打包、推送到 Anthropic | `pip install skills-cli` |

> 💡 建议优先接入 **CCPM**（daymade/claude-code-skills），用户量最大，安装体验最简。

---

## Credits / 致谢

Inspired by these open-source projects:

| Project | What We Learned |
|---------|----------------|
| [claude-engram](https://github.com/20alexl/claude-engram) | Per-project memory scoping, recency-decayed errors, causal attribution |
| [ork/errors](https://github.com/yonatangross/orchestkit) | Structured error→resolution pattern mapping |
| [agenttrace](https://github.com/luoyuctl/agenttrace) | Session health scoring, regression detection, baseline comparison |
| [agent-profiler](https://github.com/DevonPeroutky/agent-profiler) | Repeated-step detection, context bloat profiling |

---

## License

MIT — see [LICENSE](LICENSE) file.
