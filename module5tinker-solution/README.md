# 🐶 BugHound — Solution

This is the **reference solution** for the AI110 Module 5 Tinker *BugHound*. BugHound already ran
end-to-end in the starter — this lab is about *judgment*, so the solution applies one deliberate
design change per part on top of the working system and documents the reasoning in
`model_card.md`. It is one reasonable set of choices, not the only correct one.

> Starter repo: [`ai110-module5tinker-bughound-starter`](https://github.com/codepath/ai110-module5tinker-bughound-starter)

### What changed vs. the starter

- **[Part 2 — reliability]** `analyze()` now falls back to the heuristic analyzer if the LLM
  returns an issue whose `severity` isn't one of `Low`/`Medium`/`High` (`_severities_valid`).
- **[Part 3 — risk policy]** `should_autofix` now also requires that **no High-severity issue** is
  present, regardless of the numeric score.
- **[Part 4 — guardrail + test]** `assess_risk` refuses to auto-apply a fix that **rewrites more
  than 50% of the lines** (`MAX_AUTOFIX_CHANGE_RATIO`); new tests cover the invalid-severity
  fallback and the over-editing guardrail.
- **[Part 5]** `model_card.md` is filled in with grounded observations from the sample files.

All changes are small, single-purpose, and produce a *different decision* on the same input —
which is the point of the lab. `pytest` shows 10 passing tests (8 original + 2 new), all offline.

---

## What BugHound Does

Given a short Python snippet, BugHound:

1. **Analyzes** the code for potential issues  
   - Uses heuristics in offline mode  
   - Uses Gemini when API access is enabled  

2. **Proposes a fix**  
   - Either heuristic-based or LLM-generated  
   - Attempts minimal, behavior-preserving changes  

3. **Assesses risk**  
   - Scores the fix  
   - Flags high-risk changes  
   - Decides whether the fix should be auto-applied or reviewed by a human  

4. **Shows its work**  
   - Displays detected issues  
   - Shows a diff between original and fixed code  
   - Logs each agent step

---

## Setup

### 1. Create a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# or
.venv\Scripts\activate      # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running in Offline (Heuristic) Mode

No API key required.

```bash
streamlit run bughound_app.py
```

In the sidebar, select:

* **Model mode:** Heuristic only (no API)

This mode uses simple pattern-based rules and is useful for testing the workflow without network access.

---

## Running with Gemini

### 1. Set up your API key

Copy the example file:

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```text
GEMINI_API_KEY=your_real_key_here
```

### 2. Run the app

```bash
streamlit run bughound_app.py
```

In the sidebar, select:

* **Model mode:** Gemini (requires API key)
* Choose a Gemini model and temperature

BugHound will now use Gemini for analysis and fix generation, while still applying local reliability checks.

---

## Running Tests

Tests focus on **reliability logic** and **agent behavior**, not the UI.

```bash
pytest
```

You should see tests covering:

* Risk scoring and guardrails
* Heuristic fallbacks when LLM output is invalid
* End-to-end agent workflow shape
