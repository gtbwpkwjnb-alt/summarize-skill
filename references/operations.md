# summarize — 运行时操作手册（v8.2 单层化）

> 技能内部运行时逻辑。包括存储层级、降级链、自维护、Headroom 集成。
> SKILL.md 指示"详见此文件"时读取。

---

## 存储层级 — v8.2 静态三层

**基址**：`$HARVEST_BASE=~/.agents/skills/summarize/harvests/`（固定路径，文件不存在时自动创建）。

| 层级 | 位置 | 容量建议 | 加载方式 |
|:----:|------|:---:|:--------:|
| **温区** | `$HARVEST_BASE/{project}/errors.md` | ≤30条 | 按需检索 |
| **冷区** | `$HARVEST_BASE/error-ledger.md` | ≤100条 | 总结时 + 主动检索 |
| **归档** | `$HARVEST_BASE/archive/` | 无上限 | 显式恢复，永不自动加载 |

**常驻负担**：无 hook 注入（v8.2 已删除热区自动注入机制）。温冷区按需加载。

**v8.2 变更**：删除 v7.1 的"热区"（L0 P0 表自动写入）。L0 规则由用户手动维护，不再由 summarize 自动注入。原因：自动写入热区对 DeepSeek-v4-flash 不可靠，且会绕过 L0 P0-4「改用户配置前先输出方案」。

**安全约束**：L0 全局规则（`~/.agents/AGENTS.md`）为 Agent 行为准则。任何对 L0 的修改建议必须以"待确认提案"形式输出，禁止自动写入。

---

## 边界场景与降级

### 场景处置（自动修复型）

| 场景 | 行为 | 输出 |
|------|------|------|
| 基址目录缺失 | 自动创建 `harvests/` | `ℹ️ 已创建 harvests 目录` |
| 归档文件损坏 | 跳过该文件，重建空文件 | `⚠️ 归档损坏，已重建` |
| 旧版数据格式（v5/v7） | 自动迁移到 v8.2 结构（删除热区字段） | `↻ 数据格式已迁移 v7→v8.2` |
| 会话 ID 冲突 | 保留新归档，旧归档标 `[superseded]` | `↻ 会话已覆盖旧归档` |
| 温区/冷区文件编码错误 | 重建空文件，原文件备份为 `.bak` | `⚠️ 编码异常，已重建（原文件→.bak）` |

### 降级链（v8.2 简化 · 3 级递进）

> **核心原则**：降级后每次仍尝试写入（检测恢复条件）。逐级恢复（非跳回 L0）。
> v8.2 简化：从 v7.1 的 5 级降级链压缩到 3 级，合并模块3.3+4 为同一降级单位。

```
L0 正常（全模块：1+2+3+4+5+6）
  │  触发条件: 无异常
  ▼
L1 错误轨降级（模块3.3+4 跳过，仅内存统计）+ 模块5+6正常
  │  触发条件: 温区/冷区 写入失败(1次)
  ▼
L2 仅进度+事实（模块1+2精简输出，5仅内存，6跳过）
  │  触发条件: 温区/冷区写入连续2次失败 OR harvests/ 不可访问
  ▼
L3 单行摘要（极限降级）
  │  触发条件: harvests/ 整体不可访问 + L0 规则不可读 OR 连续3次任意写入失败
```

**恢复规则（逐级恢复）**：
- L3→L2: 连续2次温区写入成功
- L2→L1: 连续2次冷区写入成功 + L0 规则恢复可读
- L1→L0: 连续2次温区+冷区同时写入成功

降级状态持久化到 `$HARVEST_BASE/_degradation.json`。

---

## 自维护规则

每次 `总结` 执行时自动执行以下自检。

### 版本自同步

写入 `_self-stats.md` 前，从本 SKILL.md frontmatter 读取 `version` 字段，同步到 `_self-stats.md` 第1行标题版本号。消除版本漂移。

### 子命令埋点

每次执行子命令（`总结 统计`、`总结 压缩` 等），在 `_self-stats.md` 的「子命令调用」表追加一条记录：

```
| {子命令} | {日期} | {项目} |
```

### Headroom 自检

每次执行检测 Headroom 状态，结果写入 `_self-stats.md` 的 Headroom 统计块。python_only 降级超过 30 天 → 自动在 Headroom 行追加 `⚠️ 已降级{N}天，建议修复`。

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

依据实际检测结果分级输出（v8.2 删除装饰 emoji，仅保留状态标记）：

- Rust core 缺失（`proxy.log` 含 `rust_core_missing`）→ `Headroom: 降级 (仅python_only，0 token节省) ❌`
- 完全不可用（文件不存在/读取失败）→ `Headroom: 不可用 ❌`
- 正常且有节省 → `Headroom: 正常 ({节省} token) ✅`
- 0 节省但正常运行 → `Headroom: 待确认 (0 token) ⚠️` → 检查环境变量

### 双轨存档（`总结 压缩`）

```
1. 明文压缩: archive/{date}-errors-compact.md
2. headroom_compress(明文) → hash
3. hash → archive/{date}-errors-compact.md.hr
```

检索优先级:
1. headroom MCP → headroom_retrieve(hash) → 解压
2. 无 headroom → 读取明文 .md (fallback)

**降级安全**：headroom 不可用时退化为纯明文模式。
