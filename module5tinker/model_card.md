# BugHound Mini Model Card (Reflection)

Filled in for the reference **solution**. Observations below come from running BugHound in
Heuristic mode on the four `sample_code/` files (no Gemini key required); Gemini-mode notes
describe expected behavior.

---

## 1) What is this system?

**Name:** BugHound
**Purpose:** Analyze a Python snippet, propose a fix, and run reliability checks before
suggesting whether the fix should be auto-applied.
**Intended users:** Students learning agentic workflows and AI reliability concepts.

---

## 2) How does it work?

BugHound runs a five-stage agent loop in `BugHoundAgent.run()`:
**PLAN** (decide to scan + propose a fix) → **ANALYZE** (detect issues) → **ACT** (propose a
fix) → **TEST** (`assess_risk` scores the change) → **REFLECT** (decide whether to auto-apply).

- **Heuristic mode** (offline, deterministic): `_heuristic_analyze` flags exactly three patterns
  — `print(` (Code Quality/Low), bare `except:` (Reliability/High), `TODO` (Maintainability/Medium)
  — and `_heuristic_fix` rewrites them.
- **Gemini mode**: the analyzer/fixer prompts in `prompts/` are sent to the LLM; if the call
  fails or the output doesn't match our contract, the agent falls back to heuristics.

The *code*, not the model, makes the trust decision — that's the whole point.

---

## 3) Inputs and outputs

**Inputs:** the four sample files — `cleanish.py` (no issues), `print_spam.py` (prints),
`flaky_try_except.py` (bare except), `mixed_issues.py` (print + bare except + TODO).

**Outputs (Heuristic mode):**

| Input | Issues | Risk level | Score | Auto-fix? |
|-------|--------|-----------|-------|-----------|
| cleanish.py | 0 | low | 100 | yes (nothing to change) |
| print_spam.py | 1 (Low) | low | 95 | yes |
| flaky_try_except.py | 1 (High) | medium | 55 | no |
| mixed_issues.py | 3 | high | 30 | no |

---

## 4) Reliability and safety rules

Two rules from `assess_risk`:

1. **High severity deducts 40 points.** *Checks:* whether a serious issue (e.g. bare `except:`)
   is present. *Why it matters:* serious issues shouldn't be silently auto-patched.
   *False positive:* a bare `except:` that is genuinely intentional (e.g. a top-level crash
   guard) still tanks the score. *False negative:* a subtle logic bug the heuristic never labels
   "High" sails through at full score.
2. **Missing-return penalty (−30).** *Checks:* the original had `return` but the fix doesn't.
   *Why it matters:* dropping a return often changes behavior. *False positive:* a refactor that
   legitimately moves the return into a helper. *False negative:* a fix that keeps `return` but
   returns the wrong value.

Added in this solution:
- **[Part 3] No auto-fix when any issue is High severity**, regardless of score — an explicit
  belt-and-suspenders policy.
- **[Part 4] No auto-fix when the fix rewrites > 50% of the lines** — large diffs need human eyes.

---

## 5) Observed failure modes

1. **Missed issue (false negative):** the heuristic's reliability rule only matches a *bare*
   `except:`. A broad `except Exception:` — which still swallows every error but names the class —
   slips through with **0 issues flagged**, and more generally the analyzer is blind to anything
   outside its three patterns (`print(` / bare `except:` / `TODO`), so real logic bugs, resource
   leaks, or overly-broad catches go unreported.
2. **Risky/needless fix (over-editing):** the heuristic fixer prepends `import logging` whenever a
   `print(` exists — even if `logging` is already imported — producing a **duplicate import**. On
   a file that already imports logging, the "fix" introduces a new problem. This is exactly the
   over-editing case the Part 4 guardrail now catches before auto-applying.

---

## 6) Heuristic vs Gemini comparison

- **Heuristic** catches its three patterns consistently and never hallucinates — but it is blind
  to everything else (naming, logic bugs, security).
- **Gemini** typically finds more nuanced issues and writes more natural fixes, but on
  `cleanish.py` it tends to *invent* problems (flagging `logging.info` as verbose, proposing
  renames) — a false-positive failure mode heuristics don't have.
- The risk scorer generally agreed with intuition on the samples: it correctly refused to
  auto-fix `flaky_try_except.py` and `mixed_issues.py`, and allowed the tiny `print_spam.py` fix.

---

## 7) Human-in-the-loop decision

**Scenario:** BugHound should refuse to auto-fix when the proposed change rewrites most of the
file, because a large diff can quietly change behavior.

- **Trigger:** proposed fix differs from the original by more than 50% of lines.
- **Where implemented:** `reliability/risk_assessor.py` (`MAX_AUTOFIX_CHANGE_RATIO`), so the
  policy lives with the other guardrails and is inspectable/reversible.
- **Message to show:** "This fix rewrites most of the file and needs human review before it can be
  applied."

---

## 8) Improvement idea

Make the heuristic fixer idempotent: only add `import logging` if it isn't already imported (and
add it after any existing import block). This removes the duplicate-import failure mode from §5
with a one-line guard — low complexity, real reliability gain.
