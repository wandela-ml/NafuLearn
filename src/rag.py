from retriever import search
from gemini_service import generate_content



# ============================================================
# RAG PROMPT
# ============================================================

def build_prompt(question, retrieved_chunks):
    """
    Build a grounded prompt using the student's question
    and the relevant NafuLearn knowledge-base chunks.
    """

    context_parts = []

    for chunk in retrieved_chunks:
        context_parts.append(
            f"""
Section: {chunk['metadata']['section']}

Content:
{chunk['content']}
"""
        )

    context = "\n".join(context_parts)

    prompt = f"""
You are NafuLearn, an educational assistant for Grade 10
Computer Studies students in Kenya.

Answer the student's question using the lesson content
provided below.

IMPORTANT RULES:

1. Use the provided lesson content as your primary source.
2. Do not invent facts that are not supported by the context.
3. Explain concepts clearly at a Grade 10 level.
4. Be helpful and educational rather than simply giving
   a one-line answer.
5. If the answer cannot be found in the provided lesson
   content, clearly say that the current lesson does not
   contain enough information to answer the question.
6. Do not mention embeddings, vectors, similarity scores,
   retrieval, RAG, or internal system processes.

LESSON CONTENT:
----------------
{context}
----------------

STUDENT QUESTION:
{question}

Provide a clear answer suitable for a Grade 10 student.
"""

    return prompt


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(question, top_k=3):
    """
    Retrieve relevant lesson content and generate a
    grounded answer using Gemini.
    """

    # Retrieve relevant chunks
    retrieved_chunks = search(
        question,
        top_k
    )

    # If nothing relevant was found
    if not retrieved_chunks:
        return (
            "I could not find relevant information in the "
            "current lesson to answer that question."
        )

    # Build the grounded prompt
    prompt = build_prompt(
        question,
        retrieved_chunks
    )

    # Ask Gemini to generate an answer
    return generate_content(prompt)


# ============================================================
# TEST RAG
# ============================================================

if __name__ == "__main__":

    print("\n" + "=" * 70)
    print("NAFULEARN RAG TEST")
    print("=" * 70)

    question = "Who invented the Pascaline?"

    print("\nStudent question:")
    print(question)

    print("\n" + "-" * 70)
    print("NafuLearn answer:")
    print("-" * 70)

    answer = generate_answer(question)

    print(answer)

    print("\n" + "=" * 70)