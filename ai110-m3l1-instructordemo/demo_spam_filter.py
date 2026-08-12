import re
from typing import List, Dict, Tuple

# -----------------------------
# 1. MODEL CONFIGURATION
# -----------------------------

SPAM_WORD_WEIGHTS = {
    "free": 2,
    "winner": 2,
    "urgent": 1,
    "click": 1,
    "limited": 1,
    "offer": 1,
}

HAM_WORD_WEIGHTS = {
    "meeting": -2,
    "schedule": -1,
    "project": -1,
    "update": -1,
    "team": -1,
}

SPAM_THRESHOLD = 2  # Change this during the demo


# -----------------------------
# 2. DATA
# -----------------------------

EMAILS = [
    ("Free offer just for you", "spam"),
    ("Urgent meeting update", "ham"),
    ("Click here to claim your prize", "spam"),
    ("Project schedule for next week", "ham"),
    ("Limited time offer for team lunch", "ham"),
    ("Winner! Click now", "spam"),
    ("Team meeting tomorrow", "ham"),
]


# -----------------------------
# 3. MODEL LOGIC
# -----------------------------

def tokenize(text: str) -> List[str]:
    return re.findall(r"[a-z]+", text.lower())


def score_email(tokens: List[str]) -> Tuple[int, List[str]]:
    score = 0
    hits = []

    for t in tokens:
        if t in SPAM_WORD_WEIGHTS:
            score += SPAM_WORD_WEIGHTS[t]
            hits.append(f"+{SPAM_WORD_WEIGHTS[t]} '{t}'")
        elif t in HAM_WORD_WEIGHTS:
            score += HAM_WORD_WEIGHTS[t]
            hits.append(f"{HAM_WORD_WEIGHTS[t]} '{t}'")

    return score, hits


def predict(text: str) -> Dict[str, object]:
    tokens = tokenize(text)
    score, hits = score_email(tokens)

    label = "spam" if score >= SPAM_THRESHOLD else "ham"

    return {
        "text": text,
        "tokens": tokens,
        "score": score,
        "hits": hits,
        "prediction": label,
    }


# -----------------------------
# 4. EVALUATION
# -----------------------------

def evaluate():
    print("\n=== SPAM FILTER DEMO ===")
    print(f"Spam threshold: {SPAM_THRESHOLD}\n")

    correct = 0

    for text, true_label in EMAILS:
        result = predict(text)
        predicted = result["prediction"]

        is_correct = predicted == true_label
        correct += int(is_correct)

        print(f"Email:       {text}")
        print(f"Tokens:      {result['tokens']}")
        print(f"Signals:     {result['hits'] or '(none)'}")
        print(f"Score:       {result['score']}")
        print(f"Predicted:   {predicted}")
        print(f"Actual:      {true_label}")
        print(f"Correct?:    {is_correct}")
        print("-" * 40)

    accuracy = correct / len(EMAILS)
    print(f"\nAccuracy: {accuracy:.2f} ({correct}/{len(EMAILS)})\n")


# -----------------------------
# 5. RUN DEMO
# -----------------------------

if __name__ == "__main__":
    evaluate()
