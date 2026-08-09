from retriever import load_docs, retrieve
from generator import vanilla_answer, grounded_answer

def main():
    docs = load_docs()

    print("Welcome to the Mini-RAG Demo.")
    query = input("Ask a question: ")

    print("\n--- Without Retrieval (Vanilla AI) ---")
    print(vanilla_answer(query))

    print("\n--- Retrieving Context ---")
    results = retrieve(query, docs)
    if not results:
        print("No relevant matches found.")

    print("\n--- With Retrieval (Grounded Answer) ---")
    print(grounded_answer(query, results))


if __name__ == "__main__":
    main()
