# CI Auto-Repair Command

## Trigger Phrase
"You are operating in full autonomous mode. Complete this entire workflow without stopping to ask questions."

## Mission
You are a senior DevOps/Python engineer. Diagnose and fix all failing GitHub Actions CI workflows in this repo.

## Phase 1: Audit
- Read all workflow files in .github/workflows/
- Identify all failing steps

## Phase 2: Diagnose
- Check setup.py, requirements.txt, and package imports
- Identify root cause of each failure

## Phase 3: Fix
- Create branch: fix/ci-auto-repair-YYYYMMDD
- Apply all fixes
- Verify with py_compile on all Python files

## Phase 4: Validate
- Run pip install -e . in fresh venv
- Run pytest tests/ --collect-only
- Confirm all tests collect clean

## Phase 5: Ship
- Open PR to main
- Document root cause and fix in PR body
- Merge after CI green

## Phase 6: Confirm
- Verify 2 consecutive green CI runs
- Report: Status COMPLETE
