from lesson_navigator import (
    load_lesson,
    get_learning_sections,
)

from gemini_service import generate_content



# ---------------------------------------------------------
# BUILD TEACHING PROMPT
# ---------------------------------------------------------

def build_teaching_prompt(section):

    metadata = section["metadata"]

    section_title = metadata["section"]
    content = section["content"]

    prompt = f"""
You are NafuLearn, a friendly educational tutor for
Grade 10 Computer Studies students in Kenya.

You are currently teaching the following lesson section:

SECTION:
{section_title}

LESSON CONTENT:
----------------
{content}
----------------

Your task is to teach this section clearly using the
lesson content provided above.

IMPORTANT RULES:

1. Stay faithful to the provided lesson content.
2. Do not introduce facts that are unrelated to this section.
3. Do not invent information.
4. Explain difficult ideas in simple language suitable
   for a Grade 10 student.
5. You may use a simple everyday example when it helps
   the student understand the concept.
6. Keep the explanation engaging and conversational.
7. Use short paragraphs and bullet points where useful.
8. Do not mention RAG, embeddings, vectors, prompts,
   or other internal system processes.
9. You may begin with a friendly greeting when appropriate.
10. End with ONE short "Check your understanding" question.
11. Do not provide the answer to the question.
12. Do not move to another lesson section.
13. Teach only the section provided.

IMPORTANT OUTPUT FORMAT:

Return your response using EXACTLY this structure:

EXPLANATION:
[Your student-friendly explanation]

CHECK_QUESTION:
[One short question that tests the student's understanding
of the section]

Do not add anything before "EXPLANATION:".
Do not add anything after the question.
"""

    return prompt


# ---------------------------------------------------------
# TEACH SECTION
# ---------------------------------------------------------

def teach_section(section):

    prompt = build_teaching_prompt(section)

    text = generate_content(prompt).strip()

    explanation = ""
    question = ""

    if "EXPLANATION:" in text and "CHECK_QUESTION:" in text:

        explanation_part, question_part = text.split(
            "CHECK_QUESTION:",
            1
        )

        explanation = explanation_part.replace(
            "EXPLANATION:",
            "",
            1
        ).strip()

        question = question_part.strip()

    else:
        # Fallback in case Gemini does not follow the format
        explanation = text
        question = (
            "What is the main idea you learned from this section?"
        )

    return {
        "explanation": explanation,
        "question": question,
    }


# ---------------------------------------------------------
# TEST THE TEACHER
# ---------------------------------------------------------

if __name__ == "__main__":

    print("\n" + "=" * 70)
    print("NAFULEARN — LESSON TEACHER TEST")
    print("=" * 70)

    chunks = load_lesson()

    sections = get_learning_sections(chunks)

    print(
        f"\nLearning sections available: "
        f"{len(sections)}"
    )

    current_position = 0

    section = sections[current_position]

    metadata = section["metadata"]

    print(
        f"\nTeaching section "
        f"{current_position + 1} of {len(sections)}"
    )

    print(
        f"Section: {metadata['section']}"
    )

    print("\n" + "-" * 70)
    print("NAFULEARN TEACHES:")
    print("-" * 70)

    lesson = teach_section(section)

    print(lesson["explanation"])

    print("\n" + "-" * 70)
    print("CHECK YOUR UNDERSTANDING")
    print("-" * 70)

    print(lesson["question"])

    print("\n" + "=" * 70)