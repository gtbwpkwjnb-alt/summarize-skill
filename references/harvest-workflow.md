# 收割写入工作流 / Harvest Write Workflow

> 模块 3.3 详细步骤。主文件 SKILL.md 中引用此处。

---

## Step 1: 确定项目名

从当前工作目录的尾段提取项目名。例如 `C:\Users\Administrator\ZCodeProject` → `ZCodeProject`。

## Step 2: 写入收割文件

**路径**：`harvests/{project}/YYYY-MM-DD-{id}.md`

**格式**：6 分区结构，详见 `references/harvest-format.md`

| 分区 | 字段 | 内容 |
|------|------|------|
| `activeContext` | 当前活动上下文 | 会话目标、环境约束 |
| `progress` | 进度 | 完成/进行/未开始 |
| `decisions` | 决策 | `[DECISION]` 标注 |
| `errors` | 错误 | `[ERROR]` 标注 + 根因分类 |
| `patterns` | 模式 | `[INSIGHT]` + `[RULE]` 标注 |
| `nextSteps` | 建议 | 下一步行动建议 |

## Step 3: 更新错误账本

**全局错误** → `harvests/error-ledger.md`
- 追加新错误记录
- 更新已有错误的 `次数`、`最近`、`涉及项目` 字段
- 更新 `days_clean`、`last_seen`、`verified` 字段

**项目错误** → `harvests/{project}/errors.md`
- 不存在则创建，从 `references/rule-template.md` 复制表头
- 同样更新各字段

**字段更新规则**：
- `days_clean`：本次未复发则 +1，复发则归零
- `verified`：回测确认规则有效后标记 ✅
- `last_seen`：更新为当前日期

## Step 4: 更新索引

追加到 `harvests/index.md`：

```markdown
| {date} | {project} | {id} | {错误数} | {决策数} | {洞察数} |
```

## Step 5: 确认输出

```
✅ 已收割 — {project} 项目
   文件: harvests/{project}/YYYY-MM-DD-{id}.md
   全局错误: {N} 条（新增 {M}，高频 ⚠️⚠️⚠️ {H}）
   项目错误: {N} 条（新增 {M}，高频 ⚠️⚠️⚠️ {H}）
   标注: {D} 决策 / {E} 错误 / {I} 洞察 / {R} 规则建议
   回测: {通过} 条规则遵守 / {违反} 条规则违反 / {复发} 条错误复发
```

## Step 6: 更新自反馈统计

追加到 `harvests/_self-stats.md`，更新累计统计和模块使用计数。
