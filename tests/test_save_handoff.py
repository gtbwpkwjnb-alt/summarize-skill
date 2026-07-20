#!/usr/bin/env python3
"""Regression tests for summarize handoff validation and atomic replacement."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "save_handoff.py"
HEADER = "<!-- summarize-handoff schema=1 created_at=2026-07-11T00:00:00Z -->\n"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(SCRIPT), *args], text=True, capture_output=True, check=False)


def main() -> None:
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    for trigger in ("复盘", "handoff", "总结 保存", "总结 恢复", "summarize save"):
        assert trigger in manifest["triggers"], f"manifest 缺少触发词: {trigger}"
    with tempfile.TemporaryDirectory(prefix="summarize-handoff-") as temporary:
        root = Path(temporary)
        source = root / "report.md"
        target = root / ".transfers" / "latest.md"
        source.write_text(HEADER + "# 交接\n\n安全内容。\n", encoding="utf-8")
        first = run("--input", str(source), "--output", str(target))
        assert first.returncode == 0, first.stderr
        assert target.read_text(encoding="utf-8") == source.read_text(encoding="utf-8")

        source.write_text(HEADER + "# 交接\n\n更新内容。\n", encoding="utf-8")
        second = run("--input", str(source), "--output", str(target))
        assert second.returncode == 0, second.stderr
        assert target.with_name("latest.md.bak").read_text(encoding="utf-8").endswith("安全内容。\n")

        invalid = run("--input", str(source), "--output", str(root / "wrong.md"))
        assert invalid.returncode == 4, invalid.stderr
        target.with_name("latest.md.lock").write_text("pid=other\n", encoding="utf-8")
        locked = run("--input", str(source), "--output", str(target))
        assert locked.returncode == 4, locked.stderr
        target.with_name("latest.md.lock").unlink()

        secret = root / "secret.md"
        fake_github_token = "ghp_" + "abcdefghijklmnopqrstuvwxyz123456"
        secret.write_text(HEADER + f"token: {fake_github_token}\n", encoding="utf-8")
        rejected = run("--input", str(secret), "--check-only")
        assert rejected.returncode == 3, rejected.stderr
        assert "疑似密钥" in rejected.stderr
    print("save_handoff tests passed")


if __name__ == "__main__":
    main()
