# summarize — 保存与恢复操作（v10）

仅在用户明确要求 `总结 保存` / `summarize save` 时读取并执行本文件。默认总结和诊断均为只读。

## 保存前检查

1. 读取当前工作区的 `AGENTS.md` 或同级写入规则。
2. 按以下顺序确定项目根目录：用户明确指定的项目根目录；客户端当前工作区根目录；当前目录的 `git rev-parse --show-toplevel`。候选不唯一、与用户指定任务冲突或无法确定时，不写入。
3. 清除密钥、访问令牌、个人数据、完整原始对话和未经验证的推测；先用 `scripts/save_handoff.py --check-only` 拦截常见凭据模式。
4. 将报告限制为目标、状态、证据、决策、阻塞和下一步，并以首行元数据 `<!-- summarize-handoff schema=1 created_at=<UTC ISO-8601> -->` 开头。

## 保存位置与方式

- 目标唯一为 `{项目根目录}/.transfers/latest.md`。
- 可以创建缺失的 `.transfers/` 目录；只覆盖 `latest.md`，不创建自动归档、计数器或全局记忆。
- 用 `python scripts/save_handoff.py --input <已生成的临时报告> --output {项目根目录}/.transfers/latest.md` 写入。该脚本拒绝常见密钥、同目录创建 `latest.md.bak`、使用 `latest.md.lock` 防并发覆盖，并以临时文件原子替换目标。
- 写入后必须读取目标文件并运行 `python scripts/save_handoff.py --input {项目根目录}/.transfers/latest.md --check-only` 回测。失败时如实报告失败原因，不声称已保存。
- 报告中仅在回测成功后输出实际绝对路径。

## 恢复

- `总结 恢复` 只读取 `{项目根目录}/.transfers/latest.md`；元数据缺失时标为“旧格式，未验证”，仍可展示但不得称为可验证交接。
- 文件不存在、项目根目录不明或读取受限时，说明原因并停止；不要创建占位文件。

## 旧版数据

`harvests/`、`_counters.md`、`error-ledger.md`、`_pending.json` 与 `_degradation.json` 是旧版遗留数据。本版本不自动读取、写入、迁移或删除它们。需要处理旧数据时，先由用户明确指定文件和操作。
