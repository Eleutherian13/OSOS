# Stage B — Command allowlist (verified; design preserved)
# Per verified_cmds.yaml; executable + arguments verified; no shell metacharacter expansion; no redirect to unapproved executable; command preserved in record.
# Not executed (runtime BLOCKED).

verified_commands:
  - pytest (bounded output; verified against pyproject.toml config — reused existing)
  - ruff check src/
  - mypy src/

rejection_of_unlisted: TRUE (fail-closed)
no_exec_from_issue_text: TRUE
no_llm_safety_claim_accepted_as_verification: TRUE (per §E)
execution_path: DISABLED (no container)
