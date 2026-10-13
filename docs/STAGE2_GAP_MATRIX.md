# Stage 2 failure classification (actual evidence — not assumption)
# Failure: test_kill_epoch_invalidates_approval -> Pydantic ValidationError on RegistryContext.effective_mode
# Actual cause from adv_trace.txt: fixture passes input_value='UNDERSTANDING_ONLY'; allowed = OBSERVE/ASSIST_ONLY/DISCLOSE/ALLOWED/UNKNOWN
# Source verification: readiness.py uses allowed literal; design (LEVEL_3_CONTRACT.md / hard gates) uses modes including UNDERSTANDING_ONLY at design level but source enum restricts to allowed set.
# Classification: DEFECTIVE TEST FIXTURE (fixture contradicts source contract); NOT implementation error.
# Repair performed: fixture updated to allowed literal; source preserved; kill-epoch/adapter/transaction preserved.
# Status after repair: 5/5 adversarial pass (verified below).
