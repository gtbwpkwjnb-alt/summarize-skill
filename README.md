# /总结 v5.4.0 — 精炼 · 进度 · 自进化 · 技能统计 · 可逆 · 跨Agent · 三级自愈（多平台通用）

> **Condense · Progress · Self-Evolve · Analytics** — 任务开发超过1天，扫一眼就了解会话全貌。
> Essential for 1+ day dev tasks. One glance tells you everything.
> **跨平台**: ZCode · Claude Code · Codex · Cursor · Windsurf

[![Version](https://img.shields.io/badge/version-5.4.0-blue)](VERSION)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-ZCode%20%7C%20Claude%20Code%20%7C%20Codex%20%7C%20Cursor%20%7C%20Windsurf-lightgrey)]()

---

## Overview / 概述

**EN**: A multi-platform agent skill that condenses long sessions into a glanceable summary — progress, key decisions, file changes, error-driven self-evolution, and skill call analytics. Triggered ONLY by standalone `总结` or `summarize` (not in a sentence, no auto-reminder). Designed for multi-day development sessions. Works across ZCode, Claude Code, Codex, Cursor, and Windsurf.

**CN**: 跨平台 AI 编程助手技能，精炼长对话为一眼可读的摘要——进度、关键决策、文件变更、错误驱动的自进化、技能调用统计。**仅**独立词`总结`或`summarize`触发（句中不触发，无自动提醒）。专为超1天任务开发设计。支持 ZCode / Claude Code / Codex / Cursor / Windsurf。

### Core Capabilities / 核心能力

| Feature | 功能 |
|---------|------|
| 🗜️ **Session Condense** | 会话精炼 — ≤5句关键摘要 + 涉文件清单 + 关键决策 |
| 📋 **Task Progress** | 任务进度 — 完成/待办/下一步 + 压力等级 |
| ⚡ **Error Self-Evolve** | 错误自进化 — 5维分类 + 规则回测 + 全局/项目分流 |
| 📊 **Skill Analytics** | 技能调用统计 — 调用次数 + token 估算 + 效果评估 🆕 |

**设计原则**: 一句话能表达清楚绝不用两句。`总结`完整输出≤20行（自动折叠超限内容到归档），`总结 统计`≤6行。

---

## 触发方式

**唯一触发词**：`总结` 或 `summarize`，且必须作为独立词单独发送。

| ✅ 会触发 | ❌ 不会触发 |
|-----------|-------------|
| `总结`（单独发送） | "总结一下今天的工作"（在句中） |
| `summarize`（单独发送） | "帮我总结一下进度"（在句中） |
| `总结 统计`（独立词+参数） | 会话达到任意阈值（无自动提醒） |

> ⚠️ 无自动提醒、无定时触发、无其它激活路径。仅独立词触发。

---

## Architecture / 架构

```
触发（独立词 总结 / summarize）
    │
    ├─ 模块1: 会话精炼 (Session Condense)         ← 核心  ≤8文件/≤5决策
    ├─ 模块2: 任务进度 (Task Progress)             ← 核心
    ├─ 模块3: 错误自进化 (Error Self-Evolve)       ← 核心  ≤5错误
    └─ 模块4: 技能调用统计 (Skill Analytics)       ← 新增  ≤5行
    │
    └─ 超限内容 → 📦 归档 (harvests/{project}/{session-id}.md)

四级闭环 / Four Closed Loops:
┌─────────────────────────────────────────┐
│ 🔄 回测 / Backtest                       │
│   规则沉淀 → 下次验证 → 更新干净天数     │
├─────────────────────────────────────────┤
│ 📊 分级 / Scoping                        │
│   错误检测 → 全局 / 项目分流             │
├─────────────────────────────────────────┤
│ 🧬 自进化 / Self-Evolution               │
│   错误模式 → 规则建议 → 全局/项目分流     │
├─────────────────────────────────────────┤
│ 📈 技能分析 / Skill Analytics  🆕        │
│   调用追踪 → token 估算 → 效果评估       │
└─────────────────────────────────────────┘
```

### 输出精炼模型 🆕

每个模块有硬上限。超出部分自动折叠为 `📦 详见归档`，完整内容写入归档文件。

| 模块 | 上限 | 超出处理 |
|------|------|---------|
| 模块1 文件清单 | 8个 | `…等{N}个文件 📦` |
| 模块1 关键决策 | 5条 | `…等{N}条决策 📦` |
| 模块3 错误列表 | 5条 | `…等{N}条错误 📦` |
| 整体输出 | ≤20行 | 超限优先折叠模块3→1 |

### 归档模型 🆕

```
harvests/
  error-ledger.md              ← 全局错误（跨项目复用）
  _self-stats.md               ← 技能自身运行统计
  index.md                     ← 收割索引（同会话只保留最新一条）
  {project}/
    errors.md                  ← 项目错误
    {session-id}.md            ← 当前会话归档（每次总结覆盖更新，非追加）
```

**更新策略**: 同一个会话多次 `总结` → 覆盖写入同一归档文件，文件头记录最后更新时间戳。避免数据重复，保持精炼。

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
└── harvests/                 # 运行时数据 / Runtime data
    ├── index.md              # 收割索引
    ├── error-ledger.md       # 全局错误账本
    ├── _self-stats.md        # 自反馈统计（含技能调用统计）
    └── {project}/
        ├── errors.md         # 项目错误账本
        └── {session-id}.md   # 会话归档（覆盖更新）
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
📋 {项目} —— {1句总结}
> {3-5句关键摘要}
📁 文件({N}): {前8个}({操作}: {函数/类名}), …等{N}个文件 📦

🔑 关键决策({N}):
- {前5条}

✅ 完成({N}): {简述}
⏳ 待办({N}): {简述}
💡 下一步: {建议}
📊 ~{N}轮 | 🟢/🟡/🔴

⚠️ 错误({N}):
| {前5条} | {分类} | {N}次 | {标记}
  …等{N}条错误 📦

🛡️ 规则:
✅ {规则} 干净+{N}
⚠️ {规则} 违反
🔄 {规则} 复发

⚡ 进化:
全局→ {规则建议}
项目→ {规则建议}

📊 技能调用:
| {技能名} | {N}次 | token ~{估算} | {效果}
```

---

## Skill Analytics / 技能调用统计 🆕

### Token 数据来源

| 优先级 | 来源 | 精度 |
|:--:|------|:--:|
| 1 | ZCode 上下文窗口使用率（输入框下方统计） | 精确 |
| 2 | 字符估算（中文 ~1.5 字符/token，英文 ~4 字符/token） | 估算 `~` |
| 3 | 无数据 → 仅显示调用次数，token 列留空 | - |

### 效果标记

| 标记 | 含义 | 示例 |
|:--:|------|------|
| ✅ | 节省 token | summarize 压缩上下文 |
| ⚠️ | 消耗 token | skills-audit 完整审计 |
| ➡️ | 中性 | 工具性调用 |

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
| 会话历史访问 | ✅ 必需 | 模块1/2/3/4都需要读取当前会话 |
| 上下文使用率数据 | 🟡 可选 | 模块4 token统计；无数据时自动降级为字符估算 |

如果平台不支持某些能力，对应模块会自动降级。

---

## Changelog / 变更日志

### v5.4.0 (2026-06-22) — 三级自愈 + Git版本化 + 块大小限制

- 🔥🔶🔵 **三级自愈架构** — 热区(AGENTS.md≤5)/温区(errors.md≤30)/冷区(error-ledger.md≤100)，超限自动降级归档
- 🔍 **温区语义检索** — 每次总结前检索温/冷区相似错误，命中则累计不新增
- ⚡ **冲突检测** — 新规则写入前比对热区已有规则，重叠/矛盾时输出合并建议
- ✏️ **自编辑块** — 直接输出可追加至 AGENTS.md 的完整行（非建议），用户一次确认即生效
- 📦 **Git版本化** — harvests/ + AGENTS.md 规则变更自动 commit，支持回溯
- 📏 **块大小上限** — 热≤5/温≤30/冷≤100，超限按 clean 天数降级到下一层
- 🧠 **自检表升级** — 规则有效性 ✅/⚠️/❌ + 月度违规趋势 + ↕️ 升降级日志

### v5.3.2 (2026-06-22) — 正文精炼·体检优化

- 🏷️ **描述修正** — "自动迭代"→"错误进化"，与模块3机制对齐
- 📋 **触发表合并** — 触发方式+产出为空合并为一张"触发行为矩阵"
- 🧹 **去冗余** — 首次初始化并入归档模型，跨Agent发现并入更新策略，模块4双格式块合并
- 🔧 **漏洞修复** — 模块3重试阈值≥2对齐P0-换路，5维分类增加规则ID映射列
- ⏱️ **可落地判定** — "10轮内"改为"1h内"（基于归档时间戳），不再依赖不可获取的轮次数据
- 📦 **附录精简** — 错误字段规范移到error-ledger.md，安装/前置/反馈精简为1行引用
- 📉 **283行→221行**（省62行/22%），description 36字符

### v5.3.1 (2026-06-22) — 逻辑精炼 + 降级矩阵 + 行为细则

- 🔧 **逻辑链路重组** — 平台前置条件移到安装方式之前，错误分流规则移到模块3，消除结构跳跃
- 🎯 **模块3检测细化** — 区分"工具报错"和"用户纠正"，防止误分类；增加 AGENTS.md 缺失时的降级说明
- 🤝 **跨Agent发现机制** — 归档模型增加 Agent 如何定位和读取归档文件的流程说明
- 📊 **输出精炼规则补全** — 明确模块2/4无单独上限，超20行时完整折叠优先级（3→1→4→2）
- 🟢🟡🔴 **压力等级量化** — 模块2增加阈值定义：<50% / 50-80% / >80%
- 🏷️ **模块4去新增标记** — 移除过时的"（新增）"标记，增加无token数据时的降级示例
- 📋 **产出为空场景补全** — 增加模块4的空产出场景
- 🔄 **版本检查降级** — `总结 统计` 的 `latest` 字段离线/被墙时显示`未知`，不阻断

### v5.3.0 (2026-06-22) — 可逆压缩 + 跨Agent交接 + 代码感知

- 🔄 **可逆压缩** — 归档错误列表+关键决策附带原文锚定引用，防止反向理解偏差
- 🤝 **跨Agent交接** — 归档"压缩上下文"标准化为五段式（目标/状态/决策/技能/产出物），下一个会话 Agent 可直接解析
- 🌳 **代码AST感知** — 文件清单标注函数/类级修改，支持无git/非代码项目自动降级
- 📋 **表格优先原则** — 归档数据用表格格式替代JSON代码块，减少token开销
- 🖼️ **图片降级** — 会话含图片时生成文本描述替代（可选，需平台多模态支持）

### v5.2.0 (2026-06-21) — 输出精炼 + 技能统计 + 归档单文件化

- 🎯 **输出精炼规则** — 每个模块硬上限（文件≤8、决策≤5、错误≤5），超限自动折叠到归档
- 📊 **新模块4: 技能调用统计** — 追踪技能调用次数、token 估算（从ZCode上下文统计或字符估算）、效果评估（✅节省/⚠️消耗/➡️中性）
- 📦 **归档单文件化** — `harvests/{project}/{session-id}.md` 每次总结覆盖更新（非追加），带时间戳，避免数据重复
- 📈 **`总结 统计` 增强** — 新增技能调用汇总行
- 🔧 **_self-stats.md 增强** — 新增技能调用统计、输出精炼统计字段

### v5.1.0 (2026-06-20) — 触发词锁定版

- 🔒 **触发词锁定** — 仅独立词 `总结` / `summarize` 触发，句中不触发
- 🔇 **移除主动提醒** — 删除 ≥20轮/≥3错误/≥30调用 的自动提醒，消除误触
- 📋 **修正不触发场景** — 改为"产出可能为空的场景"，与触发逻辑解耦
- 🌐 **通用触发方式** — 所有平台统一：独立词 `总结` 或 `summarize`

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
