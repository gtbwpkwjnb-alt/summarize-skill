from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
RECOMMENDATIONS = (ROOT / "references" / "recommendations.md").read_text(encoding="utf-8")


def test_compact_mode_keeps_non_discardable_state() -> None:
    required = ("目标", "当前状态", "未完成项/阻塞", "验证结果", "UNKNOWN", "唯一下一步")
    compact_line = next(line for line in SKILL.splitlines() if "必须保留：目标、当前状态" in line)
    assert all(item in compact_line for item in required)


def test_high_density_report_layout_is_explicit() -> None:
    assert "先结论、后行动、再证据" in SKILL
    assert "证据覆盖：observed N / confirmed N / inferred N / estimated N / unavailable N" in SKILL
    assert all(item in SKILL for item in ("P0 阻塞", "P1 风险", "P2 优化", "问题—影响—证据—动作"))
    assert "## 建议" in SKILL and "最后保留 `## 建议`" in SKILL


def test_skill_identity_and_version_are_aligned() -> None:
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    sutras = (ROOT / "sutras.yaml").read_text(encoding="utf-8")
    interface = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
    assert "name: session-summarize" in SKILL
    assert manifest["id"] == "session-summarize"
    assert manifest["version"] == "1.2.0"
    assert "session-summarize" in manifest["triggers"]
    assert "name: session-summarize" in sutras
    assert 'version: "1.2.0"' in sutras
    assert 'display_name: "Session Summarize"' in interface


def test_first_screen_counts_hidden_parallel_risks() -> None:
    assert "证据覆盖：observed N / confirmed N / inferred N / estimated N / unavailable N" in SKILL
    assert "阻塞" in SKILL and "UNKNOWN" in SKILL and "unavailable" in SKILL


def test_evidence_and_unknown_are_structured() -> None:
    assert all(item in SKILL for item in ("observed", "confirmed", "inferred", "estimated", "unavailable"))
    assert all(item in SKILL for item in ("问题：", "影响：", "证据：", "动作："))


def test_recommendations_bind_to_executable_objects() -> None:
    assert "失败命令、文件路径、测试命令、配置项或待用户提供的信息" in RECOMMENDATIONS
    assert "当前证据不足，先定位，不提出具体修复" in RECOMMENDATIONS


def test_manifest_and_version_are_aligned() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    assert version == "1.2.0"
    assert manifest["version"] == version


def test_history_diagnostics_is_explicit_and_separated() -> None:
    history = (ROOT / "references" / "history-diagnostics.md").read_text(encoding="utf-8")
    assert "总结 诊断 历史" in SKILL
    assert "当前证据" in history and "历史信号" in history
    assert "不得自动写入错误账本、记忆、规则或项目文件" in history


def test_layered_handoff_and_checkpoint_are_explicit() -> None:
    layered = (ROOT / "references" / "layered-handoff.md").read_text(encoding="utf-8")
    assert "总结 交接 分层" in SKILL
    assert "总结 checkpoint" in SKILL
    assert all(item in layered for item in ("snapshot", "decisions", "validation", "risks", "backlog"))
    assert "默认只输出，不写文件" in layered


def test_trigger_metadata_mentions_new_modes() -> None:
    assert "总结 checkpoint" in SKILL
    assert "总结 诊断 历史" in SKILL
    assert "总结 交接 分层" in SKILL
    sutras = (ROOT / "sutras.yaml").read_text(encoding="utf-8")
    assert "总结 交接 分层" in sutras
    assert "总结 诊断 历史" in sutras
