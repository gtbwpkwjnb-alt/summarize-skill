---
name: summarize
version: "8.2.1"
description: >
  当用户发送独立词"总结"或"summarize"时触发（句中不触发）。适用于：长对话需精炼、进度需轮转保存、错误需收割时。
  中英文独立触发。
  Triggered by standalone "总结"/"summarize" only (not mid-sentence). Use when conversation needs condensing, progress rotation, or error harvesting.
  Keywords: 总结, summarize, 会话精炼, 轮转, 错误收割, session rotation, error harvest.
license: MIT
compatibility: [ZCode, CodeBuddy, Claude Code, Codex, Reasonix]
---

# summarize v8.2.1 — 会话轮转与错误免疫（对齐 L0 v8.2）

> AI 编程助手的错误免疫系统 + 会话轮转引擎。收割错误、5维分类、单层记忆写入、生成预防规则，并精炼长对话为结构化轮转报告。
> 本技能输出**豁免 L0 完成协议**（已验证/受阻/需澄清），用专门的 `已总结：` 标记收尾。

---

## 触发方式

**唯一触发词**：`总结` 或 `summarize`，必须作为独立词单独发送。

| 会触发 | 不会触发 |
|-----------|-------------|
| `总结`（单独发送） | "总结一下今天的工作"（在句中） |
| `summarize`（单独发送） | "帮我总结一下进度"（在句中） |
| `总结 统计`（独立词+参数） | 会话达到任意阈值（无自动提醒） |

> 无自动提醒、无定时触发、无其它激活路径。仅独立词触发。

完整触发示例见 [references/trigger-examples.md](references/trigger-examples.md)。

---

## When to Use / 何时使用

- 会话较长或任务完成后，需精炼进度/决策/待办时
- 出现工具报错、执行失败或环境缺失等错误，需收割错误并沉淀规则时
- 需健康检查、使用子命令（统计/压缩/查看/清理）或归档压缩时
- **技能库健康检查**：已安装技能较多或频繁工具选择错误时，运行 `技能总结` 触发 skills-summarize-audit

## When NOT to Use / 何时不使用

- 单次极简对话（无错误、无任务、无文件修改）——无需额外总结开销
- 用户明确只需要直接回答，不需要进度/错误/记忆处理时
- 记忆目录不可写且已触发 L4 降级后——仅输出单行摘要，不再执行写入
- 低资源环境或需要严格控制 token 消耗时——可改用 `总结 统计` 等轻量子命令

---

## 架构（v8.2 单层化）

```
触发（独立词 总结 / summarize）
    │
    ├─ 模块1: 会话精炼 (Session Condense)         ← 主/次任务分层+进度条
    ├─ 模块2: 进度总结 (Task Progress)            ← 完成/待办/下一步
    ├─ 模块3: 建议总结 (Suggestions)              ← 链路优化+知识沉淀
    ├─ 模块4: 错误总结 (Error Harvest)            ← ≤5错误，5维分类
    ├─ 模块5: 成功经验 (Success Harvest)          ← 工具效用对比+最佳路径
    └─ 模块6: 分层写入 (Layered Write)            ← 决策树+待确认队列

闭环: 回测 → 规则沉淀 → 下次验证 → 更新干净天数
分流: 错误检测 → 项目温区 / 跨项目冷区
技能分析 → 调用追踪 → token 估算 → 效果评估（见 references/skill-analytics.md）
```

**v8.2 单层化**：删除 v7.1 的 4 层温冷区自动升降级机制（对 DeepSeek-v4-flash 过于复杂）。保留温区/冷区/归档作为**静态存储位置**，不再做自动升降级。

---

## 输出精炼模型（轮转模式 v8.2）

> **核心原则**：精炼报告即新会话的完整上下文。设计为 `/clear` 或新开会话后**替代全量历史对话**。每一行在脱离原始会话后也必须自明、无歧义。

### 行预算

| 复杂度 | 行预算（含空行分隔） | 判断条件 |
|:------:|:--------------------:|---------|
| 简单 | ≤30 行 | <10 轮 且 ≤2 文件 |
| 中等 | ≤50 行 | 10-30 轮 或 3-8 文件（默认）|
| 复杂 | ≤80 行 | >30 轮 或 >8 文件 |

超限时按优先级折叠：知识→错误→决策。`<!-- ... -->` 标记行和空行不计入"有效信息行"。

### 轮转模板（v8.2 标准格式）

> **双通道输出**：普通 markdown 展示（当前会话直接阅读）+ `.transfers/latest.md` 文件转储（随项目归档）+ 报告路径代码块快速复制。

```总结报告
## {项目名} — {结果状态句，≤60字}

### 目标
- **主目标**: {主任务描述}
- **次目标**: {次目标1} · {次目标2} · {次目标3}

### 进度
- 完成: {完成项1} · {完成项2} · {完成项3}
- 进行: {进行项1} (N%) · {进行项2} (N%)
- 阻塞: {阻塞原因（无则省略）}
- 数据: ~{N}轮 · {N}文件 · 估算 {全量K}K→{精炼K}K

### 文件变更
| 动作 | 文件 | 原因 |
|:----:|------|------|
| M | `{path}` | {变更原因} |
| A | `{path}` | {变更原因} |
| D | `{path}` | {变更原因} |

### 决策
**#{N} {标题}**
- 结论: {结论}
- 原因: {为什么}
- 被否: {否定了什么方案}

### 错误
**{类型}** ({N}次)
- 简述: {错误描述}
- 分类: {5维分类}
- 规则: {预防措施}

### 知识
- {工具对比/架构发现/最佳路径}

### 下一步
1. {可独立执行的具体行动}
2. {可独立执行的具体行动}

### 凭证
- 归档: `$HARVEST_BASE/{project}/{session}.md`
- 版本: v8.2
```

#### 格式说明（v8.2）

| 元素 | 含义 | 原因 |
|------|------|------|
| `<!-- ✂️ ... -->` | 转移标记（HTML注释） | 机器可检测，人类可见，不影响渲染 |
| `## 标题` | 信息区块 | AI 依赖 markdown 标题理解结构 |
| `---` | 区块分隔 | 视觉分层 |
| `> 引用` | 区块说明 | 提示该区块在新会话中的用途 |
| `→ 原因:` / `→ 被否:` | 决策上下文 | **关键字段**——新会话需要知道为什么 |
| `→ 规则:` | 错误预防 | **关键字段**——无规则=无效记录 |

> **v8.2 变更**：删除所有装饰性 emoji（🪖📋🎯📌📁🔑⚠️⚡💡）。仅保留 `✅❌⚠️` 状态标记。原因：对齐 L0 v8.2 反装饰硬规则，减少小模型注意力消耗。

### 文件转储机制

- **展示输出**：普通 markdown 格式精炼报告，供当前会话直接阅读
- **文件转储**：AI 自动写入 `{project}/.transfers/latest.md`（覆盖旧文件，零冗余）
- **快速复制**：下方报告路径代码块，极简摘要 + 文件路径
- **清理方式**：删除 `.transfers/` 目录即可，无残留文件

> AI 执行 `总结` 时：将完整精炼报告内容写入 `{project}/.transfers/latest.md`（覆盖模式），然后输出展示内容与复制块。

```报告路径
{项目名} — {结果状态句}
附件: .transfers/latest.md
```

### 行预算分配

| 区段 | 行数 | 说明 |
|------|:---:|------|
| 标题 | 1 | |
| 目标 | 1 | 主+次 |
| 状态 | 1-4 | 完成/进行/阻塞+数据 |
| 文件 | 2-8 | 每文件1行 |
| 决策 | 2-5 | 每决策2行（含上下文）|
| 错误 | 2-5 | 每错误2行（含规则）|
| 知识 | 1-3 | 每知识1行 |
| 下一步 | 1-3 | |
| 凭证 | 1 | |
| **合计** | **≤30** | 折叠标记不计入 |

### 输出规则

输出精炼报告前先读取 [references/rules.md](references/rules.md)——含自指代词清零、决策上下文、错误-规则绑定、信息熵排序、跨Session去重、折叠凭证、自检清单、Token节省测量。

---

## 输出示例（v8.2）

一次典型 `总结` 的轮转模式输出：

```总结报告
## ZCodeProject — 完成技能质量迭代，12 项问题修复

### 目标
- **主目标**: 技能质量迭代 · 验证修复
- **次目标**: Headroom core · 全链路

### 进度
- 完成: 12 项修复
- 进行: Headroom (60%)
- 数据: ~200 轮 · 30 文件 · 估算 30K→2K

### 文件变更
| 动作 | 文件 | 原因 |
|:----:|------|------|
| M | SKILL.md | 轮转模板 |
| M | README.md | 版本号 |
| A | _core.pyd | 15MB 预编译 |

### 决策
**#1 轮转模板改报告路径代码块**
- 结论: 用代码块包裹
- 原因: HTML 注释在 IDE 不可见
- 被否: 纯文本标记

### 错误
**PROC** (1 次)
- 简述: 未批准修改 7 文件
- 分类: 流程违规
- 规则: 改前输出方案

### 知识
- codegraph > grep
- Xiaping 两步发布

### 下一步
1. Headroom proxy 修复
2. Xiaping 转正

### 凭证
- 归档: `$HARVEST_BASE/ZCodeProject/sess_v8.2.md`
- 版本: v8.2
```

精炼报告已保存到 `.transfers/latest.md`，新会话粘贴下方代码块加载：

```报告路径
ZCodeProject — 完成技能质量迭代，12项修复
附件: .transfers/latest.md
```

各模块的详细格式与规则见 [references/](references/) 下对应文件。

---

## 模块总览

触发后按模块顺序执行；**生成每个模块的输出前，先读取对应 reference 文件**获取详细格式、规则与示例。

| 模块 | 名称 | 职责 | 详细参考 |
|:----:|------|------|---------|
| 1 | 会话精炼 | 主/次任务分层、进度、文件清单、关键决策 | [module-1-session-condense.md](references/module-1-session-condense.md) |
| 2 | 进度总结 | 完成项、待办项、下一步行动、压力等级 | [module-2-progress.md](references/module-2-progress.md) |
| 3 | 建议总结 | 链路优化、知识沉淀 | [module-3-suggestions.md](references/module-3-suggestions.md) |
| 4 | 错误总结 | 5维分类、6类失败、规则、即时优化 | [module-4-errors.md](references/module-4-errors.md) |
| 5 | 成功经验 | 成功模式、工具效用对比、最佳路径 | [module-5-success.md](references/module-5-success.md) |
| 6 | 分层写入 | 写入层级决策树、目标文件、待确认队列 | [module-6-write.md](references/module-6-write.md) |

---

## 平台适配

首次运行前，先读取 `references/platform-adaptation.md` 完成平台检测与路径变量映射；后续运行时按已映射的变量执行写入。

---

## 运行时操作

运行时逻辑（存储层级、边界降级、自维护规则、Headroom 集成）详见 [references/operations.md](references/operations.md)。

---

## 子命令

执行子命令前，先读取 `references/subcommands.md` 获取完整命令列表与输出格式；`总结 深度 写入` 的详细步骤与错误处理见 `references/deep-write.md`。

---

## v8.2 完成协议豁免

> 本技能输出**豁免 L0 完成协议**（已验证/受阻/需澄清）。

summarize 输出末尾用专门标记替代：

```
已总结：{写入路径或会话 ID}
```

示例：`已总结：$HARVEST_BASE/ZCodeProject/sess_v8.2.md`

原因：summarize 的"完成"概念是"已写入归档"，与 L0 的"已贴证据"语义不同。强行套用 L0 协议会破坏报告结构。

---

## 文件结构

```
summarize/
├── SKILL.md              # 技能主文件
├── references/           # 模块细则·规则·操作手册·安装
├── scripts/              # 安装脚本
├── harvests/             # 运行时数据（自动生成）
│   └── {project}/errors.md · {session}.md
└── archive/              # 压缩归档（`总结 压缩` 生成）
```

完整文件清单见仓库 [README](README.md)。

---

## 安装

一键安装与手动安装详见 [references/installation.md](references/installation.md)。

安装后输入 `总结` 或 `summarize` 即可触发。

---

## 反馈

[GitHub Issues](https://github.com/gtbwpkwjnb-alt/summarize-skill/issues/new)

---

## License

MIT — see [LICENSE](LICENSE) file.
