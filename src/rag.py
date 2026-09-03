import os
from dotenv import load_dotenv
from google import genai

from retriever import search

#=========================================================================
#GEMINI SETUP
#=========================================================================
load_dotenv()
api_key = os.getenv("Gemini_api_key")

if not api_key:
    raise ValueError("Gemini_Api_key not found in .env file")

client = genai.Client(api_key=api_key)


#=======================================================================
#RAG PROMPT
#=======================================================================

def build_prompt(question, retrieved_chunks):
    """
    Build a grounded prompt using the student's question 
    and the relevant NafuLearn knowledge-base chunks.
    """
    context_parts = []

    for chunk in retrieved_chunks:
        context_parts.append(
            f"""section: chunk['metadata']['section']
            content:{chunk['content']}
            """
            )
        context = "\n".join(context_parts)

        prompt = f"""

You are NafuLearn, an educational assistant for Grade 10 Computer Studies students in Kenya. 
Answer the student's question using the lesson content provided below. 

IMPORTANT RULES:
 . Use the provided lesson content as your primary source. 
2. Do not invent facts that are not supported by the context. 
3. Explain concepts clearly at a Grade 10 level. 
4. Be helpful and educational rather than simply giving a one-line answer. 
5. If the answer cannot be found in the provided lesson content, 
clearly say that the current lesson does not contain enough information to answer the question. 
6. Do not mention embeddings, vectors, similarity scores, retrieval, RAG, or internal system processes.

LESSON CONTENT: 
---------------- 
{context} 
---------------- 

STUDENT QUESTION: 
{question} 
Provide a clear answer suitable for a Grade 10 student.
"""
        return prompt

#========================================================
#Generate Answer
#========================================================
def generate_answer(question, top_k=3):
    """
    Retrieve relevant lesson content and generate a grounded answer using Gemini
    """
    #Retrieve relevant chunks
    retrieved_chunks = search(
        question,
        top_k
    )
    # if nothing relevant was found
    if not retrieved_chunks:
        return(
            "I could not find relevant information in the current lesson to answe that question"
        )
    # Build the grounded prompt
    prompt = build_prompt(
        question,
        retrieved_chunks
    )
    # Ask Gemini to generate an answer
    response = client.models.generate_content( 
        model="gemini-3.6-flash", 
        contents=prompt 
        )
    return response.text


    
#=========================================================
#TEST RAG
#=========================================================

if __name__ == "__main__": 
    print("\n" + "=" * 70) 
    print("NAFULEARN RAG TEST") 
    print("=" * 70) 
    question = "What is quantum computing?" 
    print("\nStudent question:") 
    print(question) 
    print("\n" + "-" * 70) 
    print("NafuLearn answer:") 
    print("-" * 70) 
    answer = generate_answer(question) 
    print(answer) 
    print("\n" + "=" * 70)
