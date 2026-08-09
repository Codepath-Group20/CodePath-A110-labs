import os

def load_docs(folder="sample_docs"):
    docs = {}
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            path = os.path.join(folder, filename)
            with open(path, "r", encoding="utf-8") as f:
                docs[filename] = f.read()
    return docs


def retrieve(query, docs, k=2):
    query_words = query.lower().split()
    scored = []

    for name, text in docs.items():
        text_lower = text.lower()
        score = sum(1 for word in query_words if word in text_lower)
        if score > 0:
            scored.append((name, text, score))

    scored.sort(key=lambda x: x[2], reverse=True)
    return scored[:k]
