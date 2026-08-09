def vanilla_answer(query):
    return (
        f"I'm answering your question '{query}', "
        "but I don't have any documents to look at. "
        "My answer may be incomplete."
    )


def grounded_answer(query, retrieved_docs):
    if not retrieved_docs:
        return f"No relevant documents found for '{query}'."

    answer = [f"Answer based on retrieved docs for '{query}':\n"]
    for name, text, score in retrieved_docs:
        text_lower = text.lower()
        stopwords = {"a", "an", "the", "is", "are", "was", "were", "do", "does",
                     "how", "what", "when", "where", "which", "who", "why",
                     "i", "my", "me", "you", "your", "it", "its", "this", "that",
                     "in", "on", "at", "to", "for", "of", "by", "with", "from"}
        query_words = [w for w in query.lower().split() if w not in stopwords]
        if not query_words:
            query_words = query.lower().split()
        best_pos = len(text)
        for word in query_words:
            pos = text_lower.find(word)
            if 0 <= pos < best_pos:
                best_pos = pos

        start = max(0, best_pos - 50)
        end = start + 300
        snippet = text[start:end].strip().replace("\n", " ")
        if start > 0:
            snippet = "..." + snippet
        if end < len(text):
            snippet = snippet + "..."
        answer.append(f"- From {name} (score {score}): {snippet}")
    answer.append("\nThis answer is grounded in retrieved context.")
    return "\n".join(answer)
