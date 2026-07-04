---
name: summarize
version: "6.8.0"
description: 当用户独立发送 `总结`/`summarize` 或相关子命令（如 `总结 统计`、`总结 压缩`）时，对当前会话进行精炼、进度追踪、错误收割与分层记忆写入。触发词必须单独发送，句中不触发。
license: MIT
compatibility: ZCode, CodeBuddy, Claude Code, Codex, Reasonix
---

# summarize v6.8.0 — 会话精炼与错误免疫

> AI 编程助手的错误免疫系统 + 会话压缩引擎。收割错误、5维分类、分层记忆写入、生成预防规则，并精炼长对话为结构化进度报告。

---

## 触发方式

**唯一触发词**：`总结` 或 `summarize`，必须作为独立词单独发送。

| ✅ 会触发 | ❌ 不会触发 |
|-----------|-------------|
| `总结`（单独发送） | "总结一下今天的工作"（在句中） |
| `summarize`（单独发送） | "帮我总结一下进度"（在句中） |
| `总结 统计`（独立词+参数） | 会话达到任意阈值（无自动提醒） |

> ⚠️ 无自动提醒、无定时触发、无其它激活路径。仅独立词触发。

完整触发示例见 [references/trigger-examples.md](references/trigger-examples.md)。

---

## When to Use / 何时使用

- 会话较长、需要快速回顾当前进度与关键决策时
- 完成一轮任务后，需要整理完成项、待办项与下一步行动时
- 出现工具报错、执行失败、环境缺失等错误，需要收割并沉淀规则时
- 需要定期健康检查（热区/温区/冷区）并压缩归档时
- 使用子命令进行统计、压缩、知识库查看、台账查看、遗忘清理或深度写入时

## When NOT to Use / 何时不使用

- 单次极简对话（无错误、无任务、无文件修改）——无需额外总结开销
- 用户明确只需要直接回答，不需要进度/错误/记忆处理时
- 记忆目录不可写且已触发 L4 降级后——仅输出单行摘要，不再执行写入
- 低资源环境或需要严格控制 token 消耗时——可改用 `总结 统计` 等轻量子命令

---

## 架构

```
触发（独立词 总结 / summarize）
    │
    ├─ 模块1: 会话精炼 (Session Condense)         ← 主/次任务分层+进度条
    ├─ 模块2: 进度总结 (Task Progress)            ← 完成/待办/下一步
    ├─ 模块3: 建议总结 (Suggestions)              ← 链路优化+知识沉淀+记忆健康度
    ├─ 模块4: 错误总结 (Error Harvest)            ← ≤5错误
    ├─ 模块5: 成功经验 (Success Harvest)          ← 工具效用对比+最佳路径
    └─ 模块6: 分层写入 (Layered Write)            ← 决策树+待确认队列

四级闭环:
  回测 → 规则沉淀 → 下次验证 → 更新干净天数
  分级 → 错误检测 → 全局/项目分流
  自进化 → 错误模式 → 规则建议 → 全局/项目分流
  技能分析 → 调用追踪 → token 估算 → 效果评估
```

---

## 输出精炼模型

> **核心原则**：按信息密度排序，优先保留高信息量条目。同类/重复项自动聚合，折叠时附带可追溯路径凭证。

### 自适应行预算

总行数上限根据 Session 复杂度自动调整：

| 复杂度 | 行预算 | 判断条件 |
|:------:|:------:|---------|
| 🟢 简单 | ≤15行 | <10轮对话 且 ≤2个文件改动 |
| 🟡 中等 | ≤25行 | 10-30轮对话 或 3-8个文件（默认）|
| 🔴 复杂 | ≤35行 | >30轮对话 或 >8个文件 |

超限折叠顺序：模块4→模块3→模块5，压缩凭证行不计入上限。

### 信息熵排序规则

各模块输出前按信息密度重新排序，非简单按时间/位置截断：

| 模块 | 项目 | 高优先级（完整显示） | 中优先级（聚合显示） | 低优先级（仅计数） |
|:----:|------|-------------------|-------------------|-----------------|
| 1 | 决策 | 架构性决策（影响项目结构） | 配置性决策（工具/环境选择） | 过程性决策（临时方案） |
| 4 | 错误 | 首次出现的错误类型 | 同类错误出现2-3次 | 同类错误≥3次（已有规则） |
| 5 | 经验 | 工具效用对比结论 | 成功路径记录 | 单次操作经验 |

### 去重聚合规则

同类型错误跨 Session 聚合时，引用温区/冷区历史数据，格式：

```
{类型} (累计{N}次, 涉及{Y}个session) | {分类} | {状态}
```

### 压缩凭证格式

信息被折叠归档时，必须附带可追溯路径，格式使用路径变量（跨用户兼容）：

```
📦 等{N}条{Noun} → 见 $HARVEST_BASE/{project}/{session-id}.md#{anchor}
```

- `$HARVEST_BASE` = `~/.agents/skills/summarize/harvests/`（技能级固定路径，自动展开）
- `{project}` = 当前项目名
- `{session-id}` = 当前会话 ID
- `{anchor}` = 对应模块锚点（如 `#错误记录`、`#关键决策`）

### 模块上限（信息熵排序后仍受此约束）

| 模块 | 上限 | 超出处理 |
|------|------|---------|
| 模块1 文件清单 | 8个 | `…等{N}个文件 📦 → $HARVEST_BASE/{project}/{session}.md#文件清单` |
| 模块1 关键决策 | 5条 | `…等{N}条决策 📦 → $HARVEST_BASE/{project}/{session}.md#关键决策` |
| 模块4 错误列表 | 5条 | `…等{N}条错误 📦 → $HARVEST_BASE/{project}/{session}.md#错误记录` |
| 整体输出 | 自适应 | 压缩凭证行不计入行数上限 |

### 压缩自检

写入模块6前执行一轮自检：

```
✅ 检查: 所有唯一错误类型已呈现（至少计数）
✅ 检查: 主任务及进度已保留
✅ 检查: 架构性决策未丢失
⚠️ 任意失败 → 追加一行恢复说明，并记入 _self-stats.md 的 compression_loss 计数器
```

归档详情见 [references/archive-model.md](references/archive-model.md)。

---

## 输出示例

一次典型 `总结` 的输出：

```
📋 ZCodeProject — 完成 skills-audit 与 summarize 的迭代优化

🎯 主任务
  优化技能文件结构与触发描述
  进度 ██████████ 100%
  > 完成: 修复 summarize 命名不一致、拆出 7 个 reference 文件、瘦身主文件
  > 待办: 无

📁 涉及文件(3)
  ✏️ 修改: skills-audit/SKILL.md, summarize/SKILL.md
  ➕ 新增: summarize/references/subcommands.md

✅ 本轮完成(2)
  - skills-audit 执行流程外迁，新增输出示例
  - summarize 子命令与平台适配外迁，清理冗余 frontmatter

⏳ 待办(0)

💡 下一步
  1. 用 `总结 统计` 查看采纳率
  > 建议运行测试提示验证输出格式

⚠️ 错误(0)

📝 写入(1):
  ├ → 项目级(1): 🏗️架构: 技能主文件保留入口，详情拆入 references/

🪖 Headroom: 正常 (~1200 token) ｜ Kompress
```

各模块的详细格式与规则见 references/ 下对应文件。

---

## 模块总览

触发后按模块顺序执行；**生成每个模块的输出前，先读取对应 reference 文件**获取详细格式、规则与示例。

| 模块 | 名称 | 职责 | 详细参考 |
|:----:|------|------|---------|
| 1 | 会话精炼 | 主/次任务分层、进度、文件清单、关键决策 | [module-1-session-condense.md](references/module-1-session-condense.md) |
| 2 | 进度总结 | 完成项、待办项、下一步行动、压力等级 | [module-2-progress.md](references/module-2-progress.md) |
| 3 | 建议总结 | 链路优化、知识沉淀、记忆健康度 | [module-3-suggestions.md](references/module-3-suggestions.md) |
| 4 | 错误总结 | 5维分类、6类失败、规则、即时优化 | [module-4-errors.md](references/module-4-errors.md) |
| 5 | 成功经验 | 成功模式、工具效用对比、最佳路径 | [module-5-success.md](references/module-5-success.md) |
| 6 | 分层写入 | 写入层级决策树、目标文件、待确认队列 | [module-6-write.md](references/module-6-write.md) |

---

## 平台适配

首次运行前，先读取 `references/platform-adaptation.md` 完成平台检测与路径变量映射；后续运行时按已映射的变量执行写入。

---

## 存储层级 — 4层金字塔

**基址**：`$HARVEST_BASE=~/.agents/skills/summarize/harvests/`（固定路径，文件不存在时自动创建）。

| 层级 | 位置 | 定容 | 加载方式 |
|:----:|------|:---:|:--------:|
| 🔥**热区** | `$L0_RULES` P0表 | ≤5条 | hook 每次 session 自动注入 |
| 🔶**温区** | `$HARVEST_BASE/{project}/errors.md` | ≤30条 | 按需检索 |
| 🔵**冷区** | `$HARVEST_BASE/error-ledger.md` | ≤100条 | 总结时 + 主动检索 |
| ⬜**归档** | `$HARVEST_BASE/archive/` | 无上限 | 显式恢复，永不自动加载 |

**常驻负担**：仅热区 ~2KB / ~500 token（hook 注入），温冷区按需加载。

---

## 边界场景与降级

### 场景处置（自动修复型）

| 场景 | 行为 | 输出 |
|------|------|------|
| 基址目录缺失 | 自动创建 `harvests/` | `ℹ️ 已创建 harvests 目录` |
| 归档文件损坏 | 跳过该文件，重建空文件 | `⚠️ 归档损坏，已重建` |
| 旧版数据格式（v5） | 自动迁移到 v6 结构 | `↻ 数据格式已迁移 v5→v6` |
| 会话 ID 冲突 | 保留新归档，旧归档标 `[superseded]` | `↻ 会话已覆盖旧归档` |
| 温区/冷区文件编码错误 | 重建空文件，原文件备份为 `.bak` | `⚠️ 编码异常，已重建（原文件→.bak）` |

### 降级链（5级递进 · 双轨独立降级）

> **核心原则**：降级后每次仍尝试写入（检测恢复条件）。逐级恢复（非跳回L0）。模块5(成功轨) 与模块4(错误轨) 独立降级。

```
L0 正常（全模块：1+2+3+4+5+6）
  │  触发条件: 无异常
  ▼
L1 模块4降级（仅内存统计）+ 模块5+6正常
  │  触发条件: 温区/冷区/索引 写入失败(1次)
  ▼
L2 模块3.3+4 跳过 + 模块5+6正常
  │  触发条件: 温区/冷区写入连续2次失败
  ▼
L3 仅进度+事实（模块1+2精简输出，5仅内存，6跳过）
  │  触发条件: harvests/ 整体不可访问 OR L0 规则不可读
  ▼
L4 单行摘要（极限降级）
  │  触发条件: harvests/ 整体不可访问 + L0 规则不可读 OR 连续3次任意写入失败
```

**恢复规则（逐级恢复）**：
- L4→L3: 连续2次温区写入成功
- L3→L2: 连续2次冷区写入成功 + L0 规则恢复可读
- L2→L1: 连续2次温区+冷区同时写入成功
- L1→L0: 连续2次温区+冷区+索引全部写入成功

降级状态持久化到 `$HARVEST_BASE/_degradation.json`。

---

## 自维护规则

> 每次 `总结` 执行时自动执行以下自检，确保技能自身元数据一致。

### 版本自同步

写入 `_self-stats.md` 前，从本 SKILL.md frontmatter 读取 `version` 字段，同步到 `_self-stats.md` 第1行标题版本号。消除版本漂移。

### 子命令埋点

每次执行子命令（`总结 统计`、`总结 压缩` 等），在 `_self-stats.md` 的「子命令调用」表追加一条记录：

```
| {子命令} | {日期} | {项目} |
```

季度末可汇总分析哪些子命令被实际使用。

### Headroom 自检

每次执行检测 Headroom 状态，结果写入 `_self-stats.md` 的 Headroom 统计块。python_only 降级超过 30 天 → 自动在 `🪖 Headroom` 行追加 `⚠️ 已降级{N}天，建议修复`。

### 技能级经验写入

模块5（成功经验）或模块4（错误总结）产出对技能执行优化的经验时，写入 `references/learned/{技能名}.md`。格式：

```markdown
# {技能名} — 执行优化笔记

## {日期}
- 场景: {触发场景描述}
- 经验: {具体经验}
- 来源: 模块5/模块4 | 会话 {session-id}
```

---

## Headroom 集成（可选）

> 如本地已安装 headroom，每次 `总结` 自动检查代理健康与节省统计。若未安装，则退化到明文归档，不报错。

### 检测链路

```
Read ~/.headroom/logs/proxy.log (末20行)
  → ERROR/WARNING 含 rust_core_missing/python_only_degraded
  → 记入 error-ledger.md (PROC | TOOL:Headroom)

Read ~/.headroom/proxy_savings.json
  → lifetime.tokens_saved / total_input_tokens / compression_savings_usd
  → 记入 _self-stats.md
```

### 输出

依据实际检测结果分级输出：

- Rust core 缺失（`proxy.log` 含 `rust_core_missing`）→ `🪖 Headroom: 降级 (仅python_only，0 token节省) ❌`
- 完全不可用（文件不存在/读取失败）→ `🪖 Headroom: 不可用 ❌`
- 正常且有节省 → `🪖 Headroom: 正常 ({节省} token) ✅`
- 0 节省但正常运行 → `🪖 Headroom: 待确认 (0 token) ⚠️` → 检查环境变量

### 双轨存档（`总结 压缩`）

```
1. 明文压缩: archive/{date}-errors-compact.md
2. headroom_compress(明文) → hash
3. hash → archive/{date}-errors-compact.md.hr
```

检索优先级:
  ① headroom MCP → headroom_retrieve(hash) → 解压
  ② 无 headroom   → 读取明文 .md (fallback)

**降级安全**：headroom 不可用时退化为纯明文模式。

---

## 子命令

执行子命令前，先读取 `references/subcommands.md` 获取完整命令列表与输出格式；`总结 深度 写入` 的详细步骤与错误处理见 `references/deep-write.md`。

---

## 文件结构

```
summarize/
├── SKILL.md                              # 技能主文件
├── VERSION                               # 版本号
├── LICENSE                               # MIT
├── README.md                             # 概览与安装
├── sutras.yaml                           # 规则配置
├── scripts/                              # 安装脚本
├── references/                           # 参考文档
│   ├── trigger-examples.md
│   ├── archive-model.md
│   ├── platform-adaptation.md            # 平台适配详情
│   ├── subcommands.md                    # 子命令一览
│   ├── module-1-session-condense.md      # 模块1：会话精炼
│   ├── module-2-progress.md              # 模块2：进度总结
│   ├── module-3-suggestions.md           # 模块3：建议总结
│   ├── module-4-errors.md                # 模块4：错误总结
│   ├── module-5-success.md               # 模块5：成功经验
│   ├── module-6-write.md                 # 模块6：分层写入
│   ├── deep-write.md                     # 深度子命令：写入
│   └── learned/                          # 技能级经验（运行时填充）
└── harvests/                             # 运行时数据
    ├── index.md
    ├── error-ledger.md
    ├── _self-stats.md
    ├── _pending.json
    ├── _degradation.json
    └── {project}/
        ├── errors.md
        └── {session-id}.md
```

---

## 安装

一键安装与手动安装详见 [references/installation.md](references/installation.md)。

安装后输入 `总结` 或 `summarize` 即可触发。

---

## 反馈

🐛 [GitHub Issues](https://github.com/gtbwpkwjnb-alt/summarize-skill/issues/new)

---

## License

MIT — see [LICENSE](LICENSE) file.
