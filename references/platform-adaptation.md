# 平台适配

> 首次运行时自动检测当前 Agent 平台，适配 L0 全局规则路径、项目记忆文件路径、技能目录路径。

## 平台检测表

检测顺序：依次检查以下路径是否存在，首次命中即确定平台。

| 优先级 | 平台 | L0 全局规则路径 | 项目记忆文件 | 技能目录 | 检测方式 |
|:------:|------|-----------------|-------------|---------|---------|
| 1 | **ZCode** | `~/.agents/AGENTS.md` | `./MEMORY.md` | `~/.agents/skills/` | 默认 |
| 2 | **CodeBuddy** | `~/.codebuddy/AGENTS.md` | `./CODEBUDDY.md` | `~/.codebuddy/skills/` | 检查 `~/.codebuddy/` |
| 3 | **Claude Code** | `~/.claude/CLAUDE.md` | `./CLAUDE.md` | `~/.claude/skills/` | 检查 `~/.claude/` |
| 4 | **Codex** | `~/.codex/AGENTS.md` | `./MEMORY.md` | `~/.codex/skills/` | 检查 `~/.codex/` |
| 5 | **Reasonix** | `~/.reasonix/AGENTS.md` | `./REASONIX.md` | `~/.reasonix/skills/` | 检查 `~/.reasonix/` 或 `reasonix.toml` |

## 路径变量映射表

| 变量 | 含义 | 模块6写入时使用 |
|------|------|---------------|
| `$L0_RULES` | 平台对应的 L0 全局规则路径 | 全局级规则写入 |
| `$L0_MEM_DIR` | L0 规则同目录下的 memories/ 子目录 | 全局级记忆写入 |
| `$PROJ_MEMORY` | 平台对应的项目记忆文件名 | 项目摘要写入 |
| `$SKILL_BASE` | 平台对应的技能目录 | 技能级写入 |

> **降级安全**：L0 规则文件不可读时不影响核心功能。写入目标目录不存在时自动创建。
