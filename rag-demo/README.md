# Mini-RAG Demo

A simple demonstration of Retrieval-Augmented Generation (RAG) that showcases the difference between vanilla AI responses and grounded, context-aware answers.

## Overview

This application demonstrates a basic RAG system that:

- Loads documents from a local folder
- Retrieves relevant documents based on user queries
- Provides both vanilla AI answers and grounded answers using retrieved context
- Shows how retrieval improves answer quality and accuracy

## Features

- **Document Loading**: Automatically loads text documents from the `sample_docs/` folder
- **Simple Retrieval**: Uses keyword-based scoring to find relevant documents
- **Dual Response Mode**:
  - Vanilla answers without context
  - Grounded answers using retrieved documents
- **Interactive CLI**: Easy-to-use command-line interface

## Installation

1. Clone or download this repository
2. Ensure you have Python 3.6+ installed
3. No additional dependencies required (uses only Python standard library)

## Usage

Run the demo from the command line:

```bash
python demo.py
```

The application will:

1. Load all `.txt` files from the `sample_docs/` folder
2. Prompt you to ask a question
3. Show a vanilla AI response (without context)
4. Retrieve relevant documents based on your query
5. Show a grounded response using the retrieved context

### Example Session

```text
Welcome to the Mini-RAG Demo.
Ask a question: How do I reset my password?

--- Without Retrieval (Vanilla AI) ---
I'm answering your question 'How do I reset my password?', but I don't have any documents to look at. My answer may be incomplete.

--- Retrieving Context ---

--- With Retrieval (Grounded Answer) ---
Answer based on retrieved docs for 'How do I reset my password?':

- From faq.txt (score 2): Students often ask how to reset passwords. Password reset links expire after 15 minutes for security reasons. Users must verify email ownership...

This answer is grounded in retrieved context.
```
