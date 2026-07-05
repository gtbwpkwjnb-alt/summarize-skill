---
name: summarize
version: "7.0.0"
description: 会话精炼 → 轮转就绪·进度追踪·错误收割·分层记忆写入
license: MIT
compatibility: [ZCode, CodeBuddy, Claude Code, Codex, Reasonix]
---

# summarize v7.0.0 — 会话轮转与错误免疫

> AI 编程助手的错误免疫系统 + 会话轮转引擎。收割错误、5维分类、分层记忆写入、生成预防规则，并精炼长对话为结构化轮转报告。

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
- **技能库健康检查**：当发现已安装技能较多、或频繁出现工具选择错误时，建议运行 `技能总结` 触发 [skills-summarize-audit](https://github.com/gtbwpkwjnb-alt/skills-summarize-audit-skill) 审查技能库健康度

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
	扩展模块7: 知识关联 (Knowledge Association)        ← 跨会话图衰减·实体关联·权重自进化

四级闭环:
  回测 → 规则沉淀 → 下次验证 → 更新干净天数
  分级 → 错误检测 → 全局/项目分流
  自进化 → 错误模式 → 规则建议 → 全局/项目分流
	  技能分析 → 调用追踪 → token 估算 → 效果评估（[skill-analytics.md](references/skill-analytics.md)）

	扩展模块 — 跨会话知识关联层（自研，非mnemon集成）:
	  ├─ 每次触发时构建轻量知识图（实体/关系/频次/时效）
	  ├─ 图衰减算法 → 低频旧连接自动弱化，高频新连接强化
	  ├─ 同一实体跨 session 出现 ≥3 次 → 自动提升权重
	  └─ 数据存储: harvests/association-graph.json（本地文件，无外部依赖）
```

---

## 输出精炼模型（轮转模式 v7）

> **核心原则**：精炼报告即新会话的完整上下文。设计为 `/clear` 或新开会话后**替代全量历史对话**。每一行在脱离原始会话后也必须自明、无歧义。

### 行预算

| 复杂度 | 行预算 | 判断条件 |
|:------:|:------:|---------|
| 🟢 简单 | ≤15行 | <10轮 且 ≤2文件 |
| 🟡 中等 | ≤25行 | 10-30轮 或 3-8文件（默认）|
| 🔴 复杂 | ≤35行 | >30轮 或 >8文件 |

超限折叠顺序：知识→错误→决策。凭证行不计入上限。

### 轮转模板（v7 标准格式）

```
📋 {项目} — {1句结果状态，≤60字}

🎯 目标
  {主目标} · {次目标1} · {次目标2}

📌 状态
  ✅ 完成: {项1} · {项2}
  ⏳ 进行: {项1} (N%)
  🔒 阻塞: {原因}
  📊 ~{N}轮 · {N}文件 · 净省 ~{N}K

📁 文件变更 ({N})
  M {path} — {变更简述+原因}
  A {path} — {变更简述+原因}
  D {path} — {变更简述+原因}
  > 等{N}个 → $HARVEST_BASE/{project}/{session}.md#文件清单

🔑 决策 ({N})
  #{N} {标题} → {结论}
  └ 上下文: {背景·权衡·否定的替代方案}
  #{N} {标题} → {结论}
  └ 上下文: {背景·权衡·否定的替代方案}
  > 等{N}条 → $HARVEST_BASE/{project}/{session}.md#关键决策

⚠️ 错误 ({N})
  {类型}({N}次) | {简述} | {分类}
  → 规则: {预防措施，禁止空规则}
  {类型}({N}次) | {简述} | {分类}
  → 规则: {预防措施，禁止空规则}
  > 等{N}条 → $HARVEST_BASE/{project}/{session}.md#错误记录

⚡ 知识 ({N})
  - {工具对比/架构发现/最佳路径}
  - {工具对比/架构发现/最佳路径}

💡 下一步
  1. {可独立执行的具体行动}
  2. {可独立执行的具体行动}

🪖 凭证: HARVEST={session} | FILE=$HARVEST_BASE/{project}/{session}.md | VERSION=v7
```

#### 各字段规则

| 字段 | 强制规则 | 示例 |
|------|---------|------|
| 📋 标题 | 项目名 + 含结果状态的概括句，≤60字 | `ZCodeProject — 完成技能质量迭代，12项问题修复` |
| 🎯 目标 | 主目标精炼，次目标·分隔≤3个 | `技能质量迭代 · 验证修复 · 安装Rust core` |
| 📌 状态 | ✅⏳🔒 各≤3项；📊行含轮数/文件数/token节省 | `~120轮 · 7文件 · 净省~2K` |
| 📁 文件 | `M/A/D`前缀 + 变更原因（缺原因=无效记录） | `M SKILL.md — frontmatter修复+压缩测量` |
| 🔑 决策 | 每条含 `└ 上下文:`（防止新会话重新决策） | `#{N} 方案选择 → 预编译wheel \| └ 上下文: 源码编译超时...` |
| ⚠️ 错误 | 每错误必须带 `→ 规则:`，否则无效 | `→ 规则: 改前先输出方案等批准` |
| ⚡ 知识 | 信息熵排序，最重要的在前 | `codegraph 命中率远超 glob+grep` |
| 💡 下一步 | 可独立执行，不依赖历史 | `配置 Headroom proxy API路由` |
| 🪖 凭证 | HARVEST + FILE + VERSION 必填 | `HARVEST=sess_xxx \| FILE=$HARVEST_BASE/...` |

### 行预算分配

| 区段 | 行数 | 说明 |
|------|:---:|------|
| 📋 标题 | 1 | |
| 🎯 目标 | 1 | 主+次 |
| 📌 状态 | 1-4 | 完成/进行/阻塞+数据 |
| 📁 文件 | 2-8 | 每文件1行 |
| 🔑 决策 | 2-5 | 每决策2行（含上下文）|
| ⚠️ 错误 | 2-5 | 每错误2行（含规则）|
| ⚡ 知识 | 1-3 | 每知识1行 |
| 💡 下一步 | 1-3 | |
| 🪖 凭证 | 1 | |
| **合计** | **≤30** | 折叠标记不计入 |

### 自指代词清零规则

轮转报告进入新会话后，原始历史不可见。以下词禁止使用：

| ❌ 禁止 | ✅ 替换 |
|---------|--------|
| 本轮、本次会话 | （直接说做了什么）|
| 上文、如上、前述 | （重复必要信息）|
| 这、那、该方案 | `方案X: {具体名}` |
| 继续、同上 | `重复上一步操作` → `重复操作：{具体操作}` |

### 决策上下文必要性

每条决策必须附带 `└ 上下文:`。原因：新会话会重新评估所有选择。没有上下文的决策=没有决策。

```
# 坏（无上下文）
🔑 决策: 使用预编译 wheel

# 好（有上下文）——新会话读到就知道为什么
🔑 #1 Headroom Rust core → 预编译 wheel 提取 _core.pyd
  └ 上下文: 源码编译需要拉取全量 crates.io 索引（225+依赖），
    通过代理 SSH 超时。v0.29.0 的 Windows wheel 含 15MB _core.pyd，
    提取即可用，无需编译
```

### 错误-规则绑定规则

每条错误记录必须附带 `→ 规则:`。没有规则的错误记录是无效的，不会进入轮转报告。

```
# 有效（带规则）
⚠️ ASSU(2次) | 数据未算占比就下结论 | PROC
  → 规则: 任何增长/异常先算占比再归因

# 无效（无规则，不输出）
⚠️ TOOL(1次) | 工具超时
```

### 信息熵排序规则

各模块按信息密度重排（非时间顺序）：

| 模块 | 高（完整显式） | 中（聚合） | 低（跳过） |
|:----:|---------------|-----------|-----------|
| 🔑 决策 | 架构性（影响结构/选型）| 配置性（工具/环境）| 过程性（临时方案）|
| ⚠️ 错误 | 首次出现类型 | 同类2-3次聚合 | ≥3次+已有规则 |
| ⚡ 知识 | 工具效用对比 | 成功路径记录 | 单次操作 |

### 跨 Session 去重聚合

```
{类型}(累计{N}次, 涉及{Y}个session) | {分类} | {状态}
```

同 5维分类 + 同简述 = 同类型。累计数 = 当前 + 温区 + 冷区。

### 折叠凭证

超限时附带可追溯路径（使用 `$HARVEST_BASE` 变量跨用户兼容）：

```
📦 等{N}个{Noun} → $HARVEST_BASE/{project}/{session}.md#{anchor}
```

- `$HARVEST_BASE` = `~/.agents/skills/summarize/harvests/`
- `{project}` = 当前项目名
- `{session}` = 当前会话 ID
- `{anchor}` = `#文件清单` / `#关键决策` / `#错误记录` / `#经验记录`

### 轮转自检清单

输出前逐项检查：

- [ ] 📋 标题含项目名+结果状态（≤60字）
- [ ] 🎯 目标覆盖本轮核心任务
- [ ] 📌 完成/进行/阻塞完整
- [ ] 📁 每个文件变更附带原因
- [ ] 🔑 每条决策附带上下文（防止重新决策）
- [ ] ⚠️ 每条错误附带规则（预防复发）
- [ ] ⚡ 知识按重要度排序
- [ ] 💡 下一步可独立执行
- [ ] 🪖 凭证可追溯（含 VERSION）
- [ ] 总行数 ≤ 预算（折叠标记不计）
- [ ] 无自指代词（`这` `那` `本轮` `上文` 等）

### Token 节省测量

> 用户 `/clear` 或新开会话后，精炼报告将替代全量历史进入新上下文。**此时节省是真实发生的**。

测量方式：
1. 统计当前对话轮数
2. 估算全量 token = `轮数 × 500`
3. 统计精炼报告行数
4. 估算精炼 token = `行数 × 60`
5. 节省 token = `全量估算 - 精炼估算`
6. 压缩率 = `1 - 精炼估算 / 全量估算`
7. 仅保留整数，不提供小数精度
8. 多轮触发加权平均：`Σ(各次节省) / Σ(各次全量)`

输出到 `_self-stats.md`：
```
| {日期} | {项目} | (当前) | {错误数} | {规则数} | ~{轮数} | ~{精炼行} | ~{全量K}→~{精炼K} | ~{节省K} |
```

省略号 `—` 表示历史数据未测量（v7.0.0 起启用）。

归档详情见 [references/archive-model.md](references/archive-model.md)。

---

## 输出示例

一次典型 `总结` 的轮转模式输出（v7）：

```
📋 ZCodeProject — 完成技能质量迭代，12 项问题修复（5 Critical+7 Major）

🎯 技能质量迭代 · 验证修复 · 安装 Headroom Rust core

📌 状态
  ✅ 完成: 12 项问题修复 · 3 轮测试 · Rust core 激活
  ⏳ 进行: Headroom proxy 配置 (60%)
  📊 ~120 轮 · 7 文件 · 净省 ~2K

📁 文件变更 (7)
  M SKILL.md — frontmatter 修复+压缩测量+Headroom集成
  M README.md — 版本号 6.6.3→6.8.0 + 安装路径修复
  M sutras.yaml — 平台列表同步
  M references/installation.md — 全部 5 处旧仓库名→新名
  M harvests/_self-stats.md — 虚假压缩率移除+真实测量
  A references/skill-analytics.md — 新增技能调用统计
  M ../../ZCodeProject/AGENTS.md — 新增用户偏好哨兵检测

🔑 决策 (3)
  #1 Headroom Rust core 激活方式 → 从 v0.29.0 wheel 提取 _core.pyd
  └ 上下文: 源码编译超时（crates.io 索引太慢），预编译 wheel 含 15MB
  #2 压缩率测量 → 轮数×500 估算法，声明非精确
  └ 上下文: 无法从平台 API 获取真实消耗
  #3 P0-改前批准 → L0 > 技能指令
  └ 上下文: skill-improver 指令与 L0 冲突，L0 必须优先

⚠️ 错误 (1)
  PROC(1次) | 未批准直接修改 7 个文件 | PROC
  → 规则: 任何技能/配置修改必须先输出方案等批准

⚡ 知识
  - codegraph 优先: 符号/调用链查询用 codegraph，命中率远超 grep
  - Headroom MCP 工具可用，但 proxy 需 Rust core 才生效
  - 哨兵检测: 写入 AGENTS.md，下次对话检测记忆是否丢失

💡 下一步
  1. 配置 Headroom proxy 代理路由（API key → localhost:8787）
  2. 运行 `总结 统计` 查看采纳率

🪖 凭证: HARVEST=sess_xxx | FILE=$HARVEST_BASE/ZCodeProject/sess_xxx.md | VERSION=v7
```

各模块的详细格式与规则见 references/ 下对应文件。

---

## 模块总览

触发后按模块顺序执行；**生成每个模块的输出前，先读取对应 reference 文件**获取详细格式、规则与示例。

| 模块 | 名称 | 职责 | 详细参考 |
|:----:|------|------|---------|
| 1 | 会话精炼 | 主/次任务分层、进度、文件清单、关键决策 | [module-1-session-condense.md](references/module-1-session-condense.md) |
| 2 | 进度总结 | 完成项、待办项、下一步行动、压力等级 | [module-2-progress.md](references/module-2-progress.md) |
| 3 | 建议总结 | 链路优化、错误收割与5维分类分析、知识沉淀、记忆健康度 | [module-3-suggestions.md](references/module-3-suggestions.md) |
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
| 🔥**热区** | `$L0_RULES` P0表 | ≤5条 | hook 每次 session 自动注入；**写入前需用户确认** |
| 🔶**温区** | `$HARVEST_BASE/{project}/errors.md` | ≤30条 | 按需检索 |
| 🔵**冷区** | `$HARVEST_BASE/error-ledger.md` | ≤100条 | 总结时 + 主动检索 |
| ⬜**归档** | `$HARVEST_BASE/archive/` | 无上限 | 显式恢复，永不自动加载 |

**常驻负担**：仅热区 ~2KB / ~500 token（hook 注入），温冷区按需加载。

**安全约束**：热区（`$L0_RULES`）为 Agent 全局行为规则，修改可能改变 Agent 行为准则。每次写入前必须向用户展示待写入内容并获取明确确认，禁止自动写入。

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
	│   ├── CHANGELOG.md                      # 完整变更日志
	│   ├── trigger-examples.md
	│   ├── archive-model.md
	│   ├── platform-adaptation.md            # 平台适配详情
	│   ├── skill-analytics.md                # 技能调用统计
│   ├── subcommands.md                    # 子命令一览
│   ├── module-1-session-condense.md      # 模块1：会话精炼
│   ├── module-2-progress.md              # 模块2：进度总结
│   ├── module-3-suggestions.md           # 模块3：建议总结
│   ├── module-4-errors.md                # 模块4：错误总结
│   ├── module-5-success.md               # 模块5：成功经验
│   ├── module-6-write.md                 # 模块6：分层写入
│   ├── deep-write.md                     # 深度子命令：写入
│   └── learned/                          # 技能级经验（运行时填充）
	├── archive/                              # 压缩归档（运行时生成）
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
