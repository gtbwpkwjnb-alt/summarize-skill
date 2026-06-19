---
name: summarize
description: Use when the user wants to condense a long AI coding session into a glanceable summary showing progress, key decisions, file changes, and error patterns with self-evolving rules. Multi-platform: ZCode, Claude Code, Codex, Cursor, Windsurf.
license: MIT
compatibility: ZCode, Claude Code, Codex, Cursor, Windsurf, any agent with custom-skill support
metadata:
  author: gtbwpkwjnb-alt
  version: "5.0.0"
  tags: [session-management, summarize, progress-tracking, error-tracking, self-evolution]
---

# 总结 v5.0 — 精炼 · 进度 · 自进化（多平台通用）

> **设计目标**: 任务开发>1天时，让你扫一眼就了解会话全貌。
> **核心原则**: 一句话能表达清楚绝不用两句。不得输出与3模块无关的内容。
> **平台**: ZCode / Claude Code / Codex / Cursor / Windsurf / 任何支持自定义技能的 AI 编程助手

---

## 触发方式（按平台）

| 平台 | 触发方式 | 示例 |
|------|---------|------|
| **ZCode** | 独立词 `总结` 或 `summarize`（前后空格/标点不算在句） | `> 总结` |
| **Claude Code** | 建议配置 `/summarize` 别名 | `> /summarize` |
| **Codex (OpenAI)** | 独立词 `总结` 或 `summarize` | `> 总结` |
| **Cursor** | 建议配置 `@summarize` 命令 | `> @summarize` |
| **Windsurf** | 独立词 `总结` 或 `summarize` | `> 总结` |
| **通用** | 在提示中引入"请总结当前会话" | |

### 不触发场景

| ❌ 不触发 | 原因 |
|-----------|------|
| "总结一下今天的工作" | 在句中，非独立词 |
| 会话<5轮无错误 | 无可收割内容 |
| 纯对话无工具调用 | 模块3不会产出 |
| 同一会话10轮内已执行过 | 间隔太短增量不足 |

## 首次初始化

自动创建技能目录下的 `harvests/` + `error-ledger.md` + `_self-stats.md`

**错误分流**: 工具/流程错误→全局`error-ledger.md` | 项目配置→`harvests/{project}/errors.md` | 代码实现→模块3建议不入账

## 主动提醒（仅提醒一次，不打断任务）

| 条件 | 提醒 |
|------|------|
| ≥20轮 | 💡 已{N}轮，建议/总结 |
| ≥3错误 | ⚠️ 已{N}个错误，建议/总结 |
| ≥30工具调用 | 🔧 {N}次调用，建议/总结 |

---

## 模块 1：会话精炼（核心）

**任务**: 会话→≤5句关键摘要 + 涉文件清单

```
📋 {项目} —— {1句总结}
> {3-5句关键摘要}
📁 文件: {路径}({操作}), ...

🔑 关键决策({N}):
- {决策}
```

---

## 模块 2：任务进度（核心）

```
✅ 完成({N}): {简述}
⏳ 待办({N}): {简述}
💡 下一步: {建议}
📊 ~{N}轮 | 🟢/🟡/🔴
```

---

## 模块 3：错误自进化（核心）

> 执行前加载本地规则文件 (`references/rules.md`)，如不存在则从 0 开始。

**检测**: 工具error / 用户纠正 / 同一操作重试≥3次

**5 维分类**（通用版，按你的平台替换例子）：

| 代码 | 分类 | 说明 | 示例 |
|:----:|------|------|------|
| PROC | 流程违规 | 跳过必要步骤 | 改文件前没读原内容 |
| ASSU | 假设错误 | 用了未确认的标识符/路径 | 编造不存在的函数名 |
| ENVR | 环境问题 | 网络/系统/权限限制 | 外网不可达，命令不支持 |
| TOOL | 工具误用 | 选了不适当的工具 | 用通用命令代替专用工具 |
| KNOW | 知识盲区 | 缺乏领域/项目上下文 | 不熟悉项目约定 |

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

**标记**: 🆕首次 / ⚠️2次 / ⚠️⚠️⚠️≥3次

---

## `总结 统计`

```
📊 运行{N}次 | 检测{N}错误 | 累计{N}规则
🔝 高频: {Top 3}
⚡ 进化: {模块健康度}
📦 版本: v{current} | latest: v{latest}
```

---

## 安装方式

```bash
# 一键安装（脚本自动检测平台）
curl -sL https://raw.githubusercontent.com/gtbwpkwjnb-alt/summarize-skill/master/install.sh | bash
```

```powershell
# Windows PowerShell
iwr https://raw.githubusercontent.com/gtbwpkwjnb-alt/summarize-skill/master/install.ps1 | iex
```

详见 [README.md](README.md) 或 [GitHub 仓库](https://github.com/gtbwpkwjnb-alt/summarize-skill)。

---

## 平台前置条件

- 支持自定义技能/命令注入（本平台原生支持，其他平台可能需要手动配置）
- 文件系统读写权限（存储收割数据）
- 能够访问当前会话的对话历史

---

## 反馈

🐛 [GitHub Issues](https://github.com/gtbwpkwjnb-alt/summarize-skill/issues/new)

---

## 错误记录字段规范

| 字段 | 说明 |
|------|------|
| `错误类型` | 简短描述 |
| `次数` | 累计触发次数 |
| `分类` | PROC/ASSU/ENVR/TOOL/KNOW |
| `首次` | 首次出现日期 |
| `最近` | 最近出现日期 |
| `days_clean` | 自上次后连续未再犯天数 |
| `避免规则` | 对应规则ID |
| `已验证` | 规则是否回测通过 |

---

## 格式原则

- **先结论后过程**: 每个模块先说结果
- **一行一事**: 不堆砌
- **高频高亮**: ≥3次 ⚠️⚠️⚠️
- **收割内聚**: 所有数据在 `harvests/` 内
- **建议非待办**: 用户自主选择