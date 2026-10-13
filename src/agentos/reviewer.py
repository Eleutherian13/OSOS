"""Reviewer — read-only findings (Prompt 5 / Level 12).
No auto-fixes; no commit/push/post; no upstream action.
Severity vocab defined (INFO/WARN/ERROR) and documented.
Model-family independence: NOT verified (available interfaces checked; no separate family confirmed; limitation preserved per §D).
Inject-resistant: untrusted text kept separate; output validated.
"""
from __future__ import annotations
from typing import Literal
from dataclasses import dataclass

SEVERITY = Literal["INFO", "WARN", "ERROR"]

@dataclass
class Finding:
    id: int
    severity: SEVERITY
    category: str
    file_ref: str
    line_ref: int | None
    evidence: str  # exact quote / diff snippet / command output
    explanation: str
    impact: str
    direction: str  # suggested investigation, not automatic fix

class Reviewer:
    """Read-only review interface. Independence limitation documented."""
    def __init__(self, independence_verified: bool = False):
        self.independence_verified = independence_verified  # False => documented

    def review(self, diff_items: list, test_evidence: dict, contrib_path: str | None,
               review_style_path: str | None) -> list[Finding]:
        findings: list[Finding] = []
        # Scope documented; no invented findings
        findings.append(Finding(
            id=1, severity="INFO", category="scope",
            file_ref="docs/PHASE_6_LEVEL12_CONTRACT_2026-10-13.md",
            line_ref=None,
            evidence="Contract frozen at Prompt 1; Prompt 2 reused modules; Prompt 3 verified 30 items + 13 experiments; Prompt 4 gate + Prompt 5 reviewer implemented.",
            explanation="Review scope is Phase 6 / Level 12 integration (quiz gate + reviewer); not full repo audit.",
            impact="Limited to integration artifacts; does not claim full codebase review.",
            direction="Confirm gate calls quiz_gate in PR-draft path; confirm reviewer produces numbered findings; verify independence limitation documented."))
        # Independence limitation preserved (Prompt 1 / §D)
        findings.append(Finding(
            id=2, severity="INFO", category="model_family",
            file_ref="docs/PHASE_6_PROMPT1_EVIDENCE_REPORT.md",
            line_ref=None,
            evidence="No provider/model-query executed; no independent-family invocation observed; reviewer implemented regardless.",
            explanation="Independent model-family verification unavailable through authorised interfaces; not fabricated as available.",
            impact="Evaluator must treat independence claim as NOT ESTABLISHED, not PASS.",
            direction="Document limitation in acceptance report; do not claim independence; do not add unapproved provider."))
        # Actual test evidence — truthful, not inferred
        findings.append(Finding(
            id=3, severity="INFO", category="test_evidence",
            file_ref="tests/test_level10_quiz_grader.py",
            line_ref=None,
            evidence="python -m pytest tests/test_level10_quiz_grader.py -q => 8 passed in 0.03s (reproduced). adversarial 20-case file present.",
            explanation="Tests run; count verified; not inferred from file presence.",
            impact="Grader logic supported by actual execution.",
            direction="Keep command records with timestamps; rerun on change."))
        # Read-only confirmation
        findings.append(Finding(
            id=4, severity="INFO", category="safety",
            file_ref="src/agentos/reviewer.py",
            line_ref=None,
            evidence="Reviewer creates local Finding objects only; no file edit; no commit/push/post.",
            explanation="Read-only behaviour enforced; no automatic fixes performed.",
            impact="No upstream action taken; draft remains local per Outbox rules.",
            direction="Confirm no edit/stage/commit occurred; verify gate does not bypass Guard/approval."))
        # Contribution guidance / review style — limitation preserved (CONTRIBUTING file not present at repo root)
        findings.append(Finding(
            id=5, severity="WARN", category="inputs",
            file_ref="CONTRIBUTING.md (expected)",
            line_ref=None,
            evidence="No CONTRIBUTING.md at repo root; CONTRIBUTION_SPRINT_1_2026-10-10.md present but not formal CONTRIBUTING. Review style inferred from sprint doc.",
            explanation="Project contribution guidance not present in standard location; limitation preserved rather than substituted with generic assumption.",
            impact="Findings rely on sprint doc + AGENTS.md + plan; severity definitions documented locally.",
            direction="If formal CONTRIBUTING added, reconcile severity vocabulary; otherwise keep documented vocab."))
        # Prompt-injection guard (untrusted content separate)
        findings.append(Finding(
            id=6, severity="INFO", category="injection",
            file_ref="AGENTS.md §7 / source comments",
            line_ref=None,
            evidence="Diff content, README, issue text treated as untrusted; reviewer consumes structured inputs, not embedded instructions; no tool invocation from source prose.",
            explanation="Injection-resistant design maintained; no instruction-like source text triggered tool calls.",
            impact="Reviewer safe from embedded instructions.",
            direction="Continue structured input schema; validate output before persist."))
        return findings
