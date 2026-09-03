import json
import numpy as np
from pathlib import Path
import os

from google import genai
from dotenv import load_dotenv


# ============================================================
# PROJECT PATHS
# ============================================================

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Saved chunks and embeddings
EMBEDDINGS_PATH = (
    BASE_DIR
    / "data"
    / "embeddings"
    / "lesson_01_embeddings.json"
)


# ============================================================
# GEMINI SETUP
# ============================================================

load_dotenv()

api_key = os.getenv("Gemini_api_key")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env file")

client = genai.Client(api_key=api_key)


# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================

def load_embeddings():
    """Load chunks and their embeddings from the JSON file."""

    with open(EMBEDDINGS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


# ============================================================
# QUERY EMBEDDING
# ============================================================

def create_query_embedding(query):
    """Convert a student's question into an embedding."""

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=query
    )

    return np.array(response.embeddings[0].values)


# ============================================================
# COSINE SIMILARITY
# ============================================================

def cosine_similarity(vector_a, vector_b):
    """Calculate cosine similarity between two vectors."""

    denominator = (
        np.linalg.norm(vector_a) *
        np.linalg.norm(vector_b)
    )

    if denominator == 0:
        return 0.0

    return np.dot(vector_a, vector_b) / denominator


# ============================================================
# ASK MODE
# ============================================================

def search(query, top_k=3):
    """
    Search the knowledge base using semantic similarity.

    Only educational content is considered.
    Practice questions and answer keys are excluded.
    """

    chunks = load_embeddings()

    query_embedding = create_query_embedding(query)

    results = []

    for chunk in chunks:

        content_type = chunk["metadata"]["content_type"]

        # Don't use practice questions or answer keys
        # when answering normal student questions.
        if content_type in ["practice", "answer_key"]:
            continue

        chunk_embedding = np.array(chunk["embedding"])

        similarity = cosine_similarity(
            query_embedding,
            chunk_embedding
        )

        results.append({
            "id": chunk["id"],
            "content": chunk["content"],
            "metadata": chunk["metadata"],
            "similarity": float(similarity)
        })

    # Highest similarity first
    results.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return results[:top_k]


# ============================================================
# LEARN MODE
# ============================================================

def get_lesson_content():
    """
    Return lesson content in curriculum order.

    Practice questions and answer keys are excluded.
    """

    chunks = load_embeddings()

    lesson_chunks = []

    for chunk in chunks:

        content_type = chunk["metadata"]["content_type"]

        if content_type in ["lesson_content", "summary", "activity"]:
            lesson_chunks.append(chunk)

    # Sort according to the original lesson order
    lesson_chunks.sort(
        key=lambda x: x["metadata"]["section_order"]
    )

    return lesson_chunks


def get_section(section_order):
    """Return a specific lesson section by its order."""

    lesson_chunks = get_lesson_content()

    for chunk in lesson_chunks:

        if chunk["metadata"]["section_order"] == section_order:
            return chunk

    return None


def get_next_section(current_section_order):
    """Return the next lesson section."""

    lesson_chunks = get_lesson_content()

    for chunk in lesson_chunks:

        if chunk["metadata"]["section_order"] > current_section_order:
            return chunk

    return None


# ============================================================
# PRACTICE MODE
# ============================================================

def get_practice_questions():
    """
    Return practice questions only.

    Answer keys are deliberately excluded.
    """

    chunks = load_embeddings()

    practice_questions = []

    for chunk in chunks:

        if chunk["metadata"]["content_type"] == "practice":
            practice_questions.append(chunk)

    # Keep the original question order
    practice_questions.sort(
        key=lambda x: x["metadata"]["section_order"]
    )

    return practice_questions


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("NAFULEARN RETRIEVAL SYSTEM")
    print("=" * 60)


    # --------------------------------------------------------
    # ASK MODE TEST
    # --------------------------------------------------------

    question = "Who invented the Pascaline?"

    print("\nASK MODE")
    print("-" * 60)
    print(f"Question: {question}")

    results = search(question)

    for result in results:

        print(f"\nID: {result['id']}")
        print(f"Similarity: {result['similarity']:.4f}")
        print(f"Section: {result['metadata']['section']}")
        print(f"Content type: {result['metadata']['content_type']}")
        print("-" * 60)
        print(result["content"][:300])


    # --------------------------------------------------------
    # LEARN MODE TEST
    # --------------------------------------------------------

    print("\n\nLEARN MODE")
    print("-" * 60)

    lesson = get_lesson_content()

    print(f"Number of learning sections: {len(lesson)}")

    for chunk in lesson[:5]:

        print(
            f"{chunk['metadata']['section_order']}. "
            f"{chunk['metadata']['section']}"
        )


    # --------------------------------------------------------
    # PRACTICE MODE TEST
    # --------------------------------------------------------

    print("\n\nPRACTICE MODE")
    print("-" * 60)

    questions = get_practice_questions()

    print(f"Number of practice questions: {len(questions)}")

    for question in questions:

        print(
            f"{question['metadata']['section_order']}. "
            f"{question['metadata']['section']}"
        )

    print("\n" + "=" * 60)