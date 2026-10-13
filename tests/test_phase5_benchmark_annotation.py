"""Prompt 5 annotation workflow (offline-capable; no benchmark claim).
Synthetic fixtures clearly labelled; never mixed with production evidence.
"""
import json

BENCHMARK_TARGET = 50
REQUIRED_CLASS = "not a public candidate"
PRECISION_THRESHOLD = 0.90

class BenchmarkRecord:
    def __init__(self, issue_id: str, url: str, observed_at: str, machine_pred: str, human_label: str = "PENDING_HUMAN_REVIEW"):
        self.issue_id = issue_id
        self.url = url
        self.observed_at = observed_at
        self.machine_pred = machine_pred
        self.human_label = human_label  # never auto-set from machine_pred
        self.adjudication_rationale = ""
        self.review_status = "PENDING_HUMAN_REVIEW"
        self.version = "v2.1-bench-2026-10-13"
        self.synthetic = False

def load_dataset(path: str) -> list:
    # Real dataset only; synthetic fixtures kept separate and labelled
    try:
        data = json.load(open(path, encoding="utf-8"))
        return data.get("records", [])
    except Exception:
        return []

# Synthetic fixtures (labelled) — for metric test only; never benchmark evidence
SYNTHETIC_FIXTURES = [
    {"issue_id":"S01","machine_pred":"PUBLIC_CANDIDATE","human":"NOT_CANDIDATE","fixture":"SYNTHETIC"},
    {"issue_id":"S02","machine_pred":"NOT_CANDIDATE","human":"NOT_CANDIDATE","fixture":"SYNTHETIC"},
]
