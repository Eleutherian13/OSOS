"""CLI entry: agentos report. Deterministic, uses persistent tables, exits appropriately."""
import sys
from agentos.cli_report import report

def main():
    r = report()
    for k, v in r.items():
        if k == "warnings":
            for w in v:
                print(f"WARNING: {w}")
        elif k == "alert" and v:
            print("ALERT: cost per ledger item exceeds USD 10")
        else:
            print(f"{k}: {v}")
    # Exit appropriate — critical DB failure would raise; here partial report with warning
    sys.exit(0 if not r["warnings"] else 1)
