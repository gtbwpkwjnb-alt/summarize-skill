#!/usr/bin/env python3
"""Validate and atomically persist a sanitized summarize handoff."""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

METADATA = re.compile(
    r"\A<!-- summarize-handoff schema=1 created_at=\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z -->\r?\n"
)
SECRET_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b", re.I),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?im)^\s*(?:authorization\s*:\s*bearer|(?:api[_-]?key|access[_-]?token|password)\s*[:=])\s*\S+"),
)


def validate_text(text: str) -> list[str]:
    errors: list[str] = []
    if not METADATA.match(text):
        errors.append("缺少或格式错误的 summarize-handoff 元数据")
    if len(text.encode("utf-8")) > 128 * 1024:
        errors.append("交接报告超过 128 KiB 上限")
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            errors.append("检测到疑似密钥、令牌或密码")
            break
    return errors


def acquire_lock(lock: Path) -> int:
    try:
        return os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise RuntimeError(f"保存锁已存在：{lock}；不要覆盖另一会话的交接报告") from exc


def atomic_save(text: str, output: Path) -> None:
    if output.name != "latest.md" or output.parent.name != ".transfers":
        raise RuntimeError("输出必须是项目 .transfers/latest.md")
    output.parent.mkdir(parents=True, exist_ok=True)
    lock = output.with_name(f"{output.name}.lock")
    descriptor = acquire_lock(lock)
    temporary: Path | None = None
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(f"pid={os.getpid()}\n")
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=output.parent, prefix=f".{output.name}.", delete=False) as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
            temporary = Path(handle.name)
        if output.exists():
            shutil.copy2(output, output.with_name(f"{output.name}.bak"))
        os.replace(temporary, output)
        temporary = None
    finally:
        if temporary and temporary.exists():
            temporary.unlink()
        lock.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and atomically save a sanitized summarize handoff.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    if args.check_only and args.output:
        parser.error("--check-only 不能与 --output 一起使用")
    try:
        text = args.input.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"无法读取输入：{exc}", file=sys.stderr)
        return 2
    errors = validate_text(text)
    if errors:
        print("；".join(errors), file=sys.stderr)
        return 3
    if args.check_only:
        print("handoff validation passed")
        return 0
    if not args.output:
        parser.error("保存时必须提供 --output")
    try:
        atomic_save(text, args.output)
    except (OSError, RuntimeError) as exc:
        print(f"保存失败：{exc}", file=sys.stderr)
        return 4
    print(f"saved: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
