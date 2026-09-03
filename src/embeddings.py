import os
from dotenv import load_dotenv
from google import genai
import json

from chunker import (
    BASE_DIR,
    LESSON_PATH,
    load_document,
    split_into_sections,
    add_metadata
)


load_dotenv()

api_key = os.getenv('Gemini_api_key')

if not api_key:
    raise ValueError("GEMINI_API_KEY, was not found in .env file")

client = genai.Client(api_key=api_key)

# load the lesson 
document = load_document(LESSON_PATH)

# split the lessons into sections
sections = split_into_sections(document)

# add metadata
chunks = add_metadata(sections)

print(f"Lesson loaded successfully.")
print(f"Number of chunks: {len(chunks)}")


for chunk in chunks:
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=chunk['content']
        )

    embedding = response.embeddings[0].values

    chunk['embedding'] = embedding

    print("\n" + "=" * 60)
    print(f"ID: {chunk['id']}")
    print(f"Embedding dimensions: {len(embedding)}")
    print(f"First 10 values: {embedding[:10]}")


#create embeddings directory
embeddings_dir = BASE_DIR / "data"/"embeddings"
embeddings_dir.mkdir(parents=True, exist_ok=True)

# save chunks and embeddings
output_path = embeddings_dir/"lesson_01_embeddings.json"

with open(output_path, "w", encoding="utf-8") as file:
    json.dump(chunks, file, ensure_ascii=False, indent=2)


print("\n" + "=" * 60)
print("Embeddings saved successfully.")
print(f"Saved to: {output_path}")