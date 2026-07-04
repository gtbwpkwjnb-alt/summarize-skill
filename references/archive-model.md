# 归档模型详细说明

## 目录结构

```
harvests/
  error-ledger.md              ← 全局错误（跨项目复用）
  _self-stats.md               ← 技能自身运行统计
  _pending.json                ← 待确认队列
  _degradation.json            ← 降级状态持久化
  index.md                     ← 收割索引（同会话只保留最新一条）
  {project}/
    errors.md                  ← 项目错误
    {session-id}.md            ← 当前会话归档（每次总结覆盖更新，非追加）
```

## 更新策略

同一个会话多次 `总结` → 覆盖写入同一归档文件，文件头记录最后更新时间戳。避免数据重复，保持精炼。

## 归档文件格式

```markdown
# 会话归档 — {project} — {session-id}
> 最后更新: 2026-06-28T20:00:00 | 轮次: 12 | 压力: 🟢

## 摘要
{3-5句事实摘要}

## 文件清单
| 操作 | 文件 | 函数/类 |
|:--:|------|---------|
| ✏️ | path/to/file1.py | ClassName.method |
| ➕ | path/to/file2.ts | — |
| 🗑️ | path/to/file3.js | — |

## 关键决策
| # | 决策 | 理由 |
|---|------|------|
| 1 | 选A弃B | 因为... |

## 错误记录
| 简述 | 分类 | 次数 | 状态 |
|------|:--:|:--:|:--:|
| ... | ... | ... | ... |
```

## 跨Agent交接

归档的"压缩上下文"标准化为五段式，下一个会话 Agent 可直接解析：

1. **目标** — 当前会话的核心目标
2. **状态** — 完成/待办/阻塞
3. **决策** — 关键决策及理由
4. **技能** — 使用的技能及效果
5. **产出物** — 修改/新增的文件清单

## 归档压缩（`总结 压缩`）

```
1. 明文压缩: archive/{date}-errors-compact.md
2. headroom_compress(明文内容) → hash
3. hash 写入 archive/{date}-errors-compact.md.hr

检索优先级:
  ① 有 headroom MCP → headroom_retrieve(hash) → 解压 (更快)
  ② 无 headroom     → 读取明文 .md 文件 (fallback)
```

**降级安全**：headroom 不可用时，退化为纯明文模式。

---

## 压缩凭证格式

> 所有折叠标记必须附带可追溯路径，确保任意用户部署后仍可找回原文。

### 路径变量

| 变量 | 值 | 层级 |
|------|-----|:----:|
| `$HARVEST_BASE` | `~/.agents/skills/summarize/harvests/` | 技能级（固定） |
| `{project}` | 当前项目目录名 | 项目级（自动提取） |
| `{session-id}` | 当前会话 ID | 会话级（自动提取） |
| `{anchor}` | `#文件清单` / `#关键决策` / `#错误记录` | 模块级 |

### 凭证模板

```
📦 等{N}个{Noun} → $HARVEST_BASE/{project}/{session-id}.md#{anchor}
```

示例：
```
📦 等6条错误 → $HARVEST_BASE/ZCodeProject/sess_abc123.md#错误记录
```

### 跨用户兼容性

- `~` 自动展开为用户 home 目录（Linux: `/home/user/`、Windows: `C:\Users\username\`）
- 路径不含绝对硬编码，仅依赖技能目录相对位置
- 项目名从工作目录自动提取，非硬编码

---

## 压缩自检

写入模块6（分层写入）前，对输出内容执行一轮自检，确保关键信息未因压缩而丢失。

### 检查项

| # | 检查 | PASS 条件 | 失败处理 |
|:-:|------|----------|---------|
| 1 | 错误覆盖 | 所有唯一错误类型在模块4中至少以计数形式呈现 | 追加一行 `ℹ️ 补充: {缺失类型} (已压缩)` |
| 2 | 主任务保留 | 模块1中主任务描述完整 | 追加一行 `ℹ️ 主任务: {任务名} (详情见归档)` |
| 3 | 架构决策 | 模块1架构性决策（高优先级）未被折叠 | 追加一行 `ℹ️ 架构决策已归档 → $HARVEST_BASE/{project}/{session}.md#关键决策` |

### 自检记录

自检结果写入 `_self-stats.md`：

```yaml
compression_self_checks:
  total: {累计自检次数}
  passes: {通过次数}
  failures: {失败次数}
  last_failure: "{最近失败项} | {日期}"
  recovery_lines_added: {累计追加恢复行数}
```
