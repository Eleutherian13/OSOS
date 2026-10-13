"""Benchmark metric calculations — deterministic, test-only on synthetic fixtures (labelled SYNTHETIC).
Never uses these fixtures as benchmark acceptance evidence.
Real benchmark requires 50 human-labelled records (BLOCKED).
"""
from typing import List, Dict

def compute_precision(confusion: Dict) -> float:
    tp = confusion.get("tp", 0)
    fp = confusion.get("fp", 0)
    if tp + fp == 0:
        return 0.0
    return tp / (tp + fp)

def compute_recall(confusion: Dict) -> float:
    tp = confusion.get("tp", 0)
    fn = confusion.get("fn", 0)
    if tp + fn == 0:
        return 0.0
    return tp / (tp + fn)

def report(confusion: Dict, total_records: int, labeled: int, pending: int) -> Dict:
    return {
        "total_unique_records": total_records,
        "human_labeled": labeled,
        "pending_human_review": pending,
        "positive_class": "not a public candidate",
        "tp": confusion.get("tp"), "fp": confusion.get("fp"), "tn": confusion.get("tn"), "fn": confusion.get("fn"),
        "precision": compute_precision(confusion),
        "recall": compute_recall(confusion),
        "status": "BLOCKED_PENDING_HUMAN_ANNOTATION" if labeled < 50 else "PENDING_PRECISION_CHECK",
        "synthetic_fixture_warning": "If confusion from synthetic fixtures — NOT acceptance evidence.",
    }
