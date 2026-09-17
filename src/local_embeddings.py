import json

from sentence_transformers import SentenceTransformer

from chunker import (
    BASE_DIR,
    chunk_all_lessons
)


# ============================================================
# LOAD LOCAL EMBEDDING MODEL
# ============================================================

print("\n" + "=" * 60)
print("NafuLearn — LOCAL EMBEDDING GENERATION")
print("=" * 60)

print("\nLoading local embedding model...")

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

print("Model loaded successfully.")


# ============================================================
# LOAD ALL LESSON CHUNKS
# ============================================================

chunks = chunk_all_lessons()

print(f"\nTotal chunks loaded: {len(chunks)}")


# ============================================================
# GENERATE LOCAL EMBEDDINGS
# ============================================================

for index, chunk in enumerate(chunks, start=1):

    content = chunk["content"]

    embedding = model.encode(
        content,
        normalize_embeddings=True
    )

    chunk["embedding"] = embedding.tolist()

    metadata = chunk["metadata"]

    print(
        f"{index}/{len(chunks)} | "
        f"{metadata['lesson']} | "
        f"{metadata['section']} | "
        f"Dimensions: {len(embedding)}"
    )


# ============================================================
# CREATE EMBEDDINGS DIRECTORY
# ============================================================

embeddings_dir = (
    BASE_DIR
    / "data"
    / "embeddings"
)

embeddings_dir.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# SAVE LOCAL EMBEDDINGS
# ============================================================

output_path = (
    embeddings_dir
    / "all_embeddings_local.json"
)

with open(
    output_path,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        chunks,
        file,
        ensure_ascii=False,
        indent=2
    )


# ============================================================
# COMPLETE
# ============================================================

print("\n" + "=" * 60)
print("LOCAL EMBEDDINGS SAVED SUCCESSFULLY")
print("=" * 60)

print(f"\nTotal embeddings: {len(chunks)}")
print("Embedding dimensions: 384")
print(f"Saved to: {output_path}")