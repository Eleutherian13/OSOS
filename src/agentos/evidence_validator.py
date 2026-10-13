"""Evidence-location validator (Level 12 / Prompt 2). Reuses file-system + source-content anchor.
No new external provider; deterministic only. Marks stale/missing/invalid; never silently picks nearby line.
SYNTHETIC test fixtures used for deletions/stale changes; real repo references preserved.
"""
from __future__ import annotations
import os
import hashlib
from pathlib import Path
from typing import Literal

REPO_ROOT = Path(__file__).resolve().parents[3]  # src/agentos/ -> repo root

def _read_first_lines(file_path: Path, n: int = 3) -> str:
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read(2000)
    except Exception:
        return ""

def resolve_ref(ref: str) -> dict:
    """Validate file:line evidence reference against repo."""
    result = {"ref": ref, "valid": False, "file_exists": False,
              "line_exists": False, "line_number": None,
              "stale_risk": False, "anchor_hash": None,
              "reason": None}
    if not ref or not isinstance(ref, str):
        result["reason"] = "empty or non-string ref"
        return result
    if ":" not in ref:
        result["reason"] = "missing colon separator"
        return result
    file_part, line_part = ref.rsplit(":", 1)
    if not file_part or not line_part:
        result["reason"] = "missing file or line component"
        return result
    try:
        line_no = int(line_part)
    except ValueError:
        result["reason"] = f"invalid line number: {line_part}"
        return result
    if line_no < 1:
        result["reason"] = f"line number must be >=1: {line_no}"
        return result
    # Resolve relative to repo root; support both relative and absolute
    target = REPO_ROOT / file_part
    if not target.exists():
        # Try from cwd / relative
        target = Path(file_part)
    result["file_exists"] = target.exists() and target.is_file()
    if not result["file_exists"]:
        result["reason"] = f"missing file: {file_part} (tried {target})"
        return result
    result["line_number"] = line_no
    try:
        with open(target, "r", encoding="utf-8", errors="replace") as f:
            lines = f.read().splitlines()
    except Exception as e:
        result["reason"] = f"read error: {e}"
        return result
    if line_no > len(lines):
        result["reason"] = f"line {line_no} exceeds file length {len(lines)}"
        result["line_exists"] = False
        return result
    result["line_exists"] = True
    # Source-content anchor (first ~200 chars of file + line content) for stale detection
    line_text = lines[line_no - 1] if line_no <= len(lines) else ""
    anchor = (target.read_text(encoding="utf-8", errors="replace")[:200] if target.exists() else "") + "|" + line_text[:120]
    result["anchor_hash"] = hashlib.sha256(anchor.encode("utf-8", "replace")).hexdigest()[:16]
    # Stale check: compute current anchor vs nothing to compare (stored value must be passed in for full check)
    result["stale_risk"] = False  # caller compares anchors across versions
    result["valid"] = True
    result["reason"] = None
    return result

def validate_evidence_for_fact(ref: str, expected_substring: str | None = None) -> dict:
    """Full validation for a fact: reference resolves, line content relates to expected claim."""
    res = resolve_ref(ref)
    if not res["valid"]:
        res["reason"] = (res.get("reason") or "unresolved") + " (prevents PASS per contract)"
        res["valid"] = False
        return res
    # If expected_substring given, check line contains it (weak relevance guard)
    if expected_substring is not None:
        try:
            target = REPO_ROOT / ref.split(":")[0]
            if not target.exists():
                target = Path(ref.split(":")[0])
            with open(target, "r", encoding="utf-8", errors="replace") as f:
                lines = f.read().splitlines()
            line_text = lines[int(ref.split(":")[1]) - 1] if int(ref.split(":")[1]) <= len(lines) else ""
            if expected_substring not in line_text:
                res["valid"] = False
                res["reason"] = f"line content does not contain expected substring '{expected_substring[:40]}...' (relevance failure)"
        except Exception as e:
            res["valid"] = False
            res["reason"] = f"relevance check error: {e}"
    return res
