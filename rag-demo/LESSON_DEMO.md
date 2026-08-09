# Instructor Demo Guide — Mini-RAG Demo

**~15 minutes | 4 acts + optional bonus beat**

This demo shows students why retrieval matters by contrasting a general-purpose LLM (ChatGPT) with a simple retrieval system that can search local documents. The demo ends with a live code fix that bridges directly into the Tinker activity.

---

## Pre-Demo Checklist

- [ ] ChatGPT open in a browser tab
- [ ] Terminal `cd`'d into this repo
- [ ] `sample_docs/mock_syllabus.txt` open in an editor
- [ ] `sample_docs/faq.txt` open in an editor
- [ ] `retriever.py` open in an editor
- [ ] Verified `python demo.py` runs (type `password` to confirm)

---

## Act 1 — Show the Ground Truth (2 min)

Show `mock_syllabus.txt` in your editor. Point out specific facts students will ask about:

- "The final exam is Thursday, July 31."
- "The late policy is 10% per day, max 3 days late."
- "Office hours are Tuesday & Thursday 12:00–1:30 PM."

> "This file lives on my laptop. ChatGPT has never seen it."

---

## Act 2 — Show the Failure (3 min)

Switch to the ChatGPT browser tab. Ask:

- `When is the final exam for CS 101 at College University, Summer 2025?`
- `What is the late policy for CS 101?`

ChatGPT will either hallucinate specific dates/policies or refuse to answer.

> "The model sounds confident, but it has no idea. It's guessing based on patterns."

---

## Act 3 — Show the Fix (and Its Flaw) (3 min)

Switch to the terminal. Run:

```bash
python demo.py
```

**Type:** `When is the final exam?`

- The vanilla answer is generic — "I don't have any documents to look at."
- The grounded answer retrieves `mock_syllabus.txt` with the actual exam date.
- **But it also retrieves `intro.txt`** — which is about authentication, not exams.

> "Wait — why is intro.txt showing up? It's about authentication, not exams."

Run again. **Type:** `How do I reset my password?`

- Retrieves `faq.txt` (correct) but also `intro.txt` again.

> "Our retriever is matching every word in the question, including 'is' and 'the'. Those appear in every document — they're noise."

---

## Act 4 — Fix It Live (4 min)

Switch to `retriever.py` in your editor. The current `retrieve()` function splits the query into words and counts matches — but it counts *every* word, including common ones.

> "We need to ignore common words before scoring. This is called stopword filtering."

**Step 1:** Add a stopword set above the `retrieve` function:

```python
STOPWORDS = {"a", "an", "the", "is", "are", "was", "were", "do", "does",
             "how", "what", "when", "where", "which", "who", "why",
             "i", "my", "me", "you", "your", "it", "its", "this", "that",
             "in", "on", "at", "to", "for", "of", "by", "with", "from"}
```

**Step 2:** Replace the first line inside `retrieve()`:

```python
# Before:
query_words = query.lower().split()

# After:
query_words = [w for w in query.lower().split() if w not in STOPWORDS]
if not query_words:
    query_words = query.lower().split()
```

**Step 3:** Save the file. Run `python demo.py` again.

**Type:** `When is the final exam?`

- Now returns only `mock_syllabus.txt` — no more irrelevant results.

> "One small change, and our retrieval just got dramatically better. This is exactly what you'll be doing in the Tinker — improving retrieval so the right docs come back."

---

## Bonus Beat — Live Edit (3 min)

*Flex segment — trim if running behind on time.*

Open `sample_docs/faq.txt` in your editor. Add a new line:

```
To change your username, contact support@example.edu.
```

Save the file. Run `python demo.py` again.

**Type:** `username`

The new information appears immediately in the grounded answer — no retraining needed.

> "We just updated the system's knowledge by editing a text file. Try doing that with ChatGPT's training data."

---

## After the Demo

Pause for 1-2 questions, then continue to the CFU slides.
