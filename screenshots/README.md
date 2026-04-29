# Screenshots

Manual screenshot guide for networking-labs-cli portfolio documentation.

Screenshots cannot be auto-generated in this environment. Capture each one manually using the steps below and save it to this folder.

---

## Screenshots to Capture

### 1. `repo-home.png` — Repository home page
**What to show:** GitHub.com repo page with the description, file tree, and README visible above the fold.
**Why:** First thing a recruiter sees — proves the repo is clean and professional.

**How to capture:**
1. Go to `https://github.com/CartierC/networking-labs-cli`
2. Make sure the README renders below the file tree
3. Screenshot the full page or crop to show description + file tree + top of README
4. Save as `screenshots/repo-home.png`

---

### 2. `readme-overview.png` — README overview section
**What to show:** The Role Alignment and Skills Demonstrated tables in the README.
**Why:** Shows the recruiter-readiness framing immediately.

**How to capture:**
1. Open `https://github.com/CartierC/networking-labs-cli#readme`
2. Scroll to the Role Alignment and Skills Demonstrated sections
3. Screenshot both tables together
4. Save as `screenshots/readme-overview.png`

---

### 3. `sample-output-folder.png` — Sample output folder contents
**What to show:** The `sample-output/` directory listing on GitHub showing all four output files.
**Why:** Proves there is real, readable output — not just code.

**How to capture:**
1. Go to `https://github.com/CartierC/networking-labs-cli/tree/main/sample-output`
2. Screenshot the folder listing showing all four `.txt` files
3. Save as `screenshots/sample-output-folder.png`

---

### 4. `actions-passing.png` — Successful GitHub Actions run
**What to show:** A green CI run in GitHub Actions with all 5 tests passing.
**Why:** Proves the CI pipeline works end-to-end — the strongest proof item.

**How to capture:**
1. Go to `https://github.com/CartierC/networking-labs-cli/actions`
2. Click the most recent passing run
3. Expand the "Run tests" step to show the pytest output with `5 passed`
4. Screenshot the step output
5. Save as `screenshots/actions-passing.png`

---

### 5. `runbook-preview.png` — Runbook doc open in GitHub
**What to show:** `docs/network-support-runbook.md` rendered in GitHub.
**Why:** Demonstrates technical writing and NOC documentation skills.

**How to capture:**
1. Go to `https://github.com/CartierC/networking-labs-cli/blob/main/docs/network-support-runbook.md`
2. Screenshot the rendered Markdown showing the escalation checklist and tables
3. Save as `screenshots/runbook-preview.png`

---

## Capture Tips

**macOS:**
- Full screen: `Cmd + Shift + 3`
- Selection: `Cmd + Shift + 4`, then drag to select area
- Files save to Desktop — move them to this folder and rename

**Linux:**
- Full screen: `Print Screen`
- Selection: `Shift + Print Screen` (GNOME), then drag
- Or use: `gnome-screenshot -a -f screenshots/<name>.png`

**Terminal output:**
- Make the terminal window wide (120+ cols) before running CLI commands
- Use a dark theme for legibility in screenshots
- Run the command, let it complete, then screenshot

---

## After Capturing

Add image references to the README if desired:

```markdown
![Repo Home](screenshots/repo-home.png)
![Skills Table](screenshots/readme-overview.png)
![CI Passing](screenshots/actions-passing.png)
```
