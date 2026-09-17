from lesson_navigator import (
    load_lesson,
    get_learning_sections,
)

from gemini_service import generate_content



#=============================================================
#BUILD EVALUATOR
#=============================================================

def build_evaluation_prompt(section, question, student_answer):
    metadata = section["metadata"]

    section_title = metadata["section"]
    lesson_content = section["content"]

    prompt = f"""
You are NafuLearn, a friendly Grade 10 Computer Studies tutor
for students in Kenya.

Evaluate the student's answer using ONLY the lesson content
provided.

LESSON SECTION:
{section_title}

LESSON CONTENT:
{lesson_content}

QUESTION:
{question}

STUDENT ANSWER:
{student_answer}

Classify the answer as exactly ONE of:

Correct
Partially correct
Needs improvement

Use these rules:

- Correct: the student clearly and accurately understands
  the important idea being tested.
- Partially correct: the student understands part of the idea
  but misses an important point or has a minor misunderstanding.
- Needs improvement: the answer does not show sufficient
  understanding.
- Accept different wording when the meaning is correct.
- Base the evaluation only on the lesson content.
- Be encouraging and concise.
- If improvement is needed, explain what the student should add
  or understand.
- Do not simply repeat the lesson.

Return exactly this format:

RESULT: [classification]

FEEDBACK:
[Brief explanation]

WHAT TO IMPROVE:
[What the student should add or understand, or:
"Nothing important is missing. Well done!"]

ENCOURAGEMENT:
[One short encouraging sentence.]
"""

    return prompt

#=================================================
#EVALUATE STUDENT ANSWER
#=================================================

def evaluate_answer(section, question, student_answer):
    prompt = build_evaluation_prompt(
        section,
        question,
        student_answer
    )

    return generate_content(prompt)
#----------------------
#TEST THE EVALUATOR
#----------------------
if __name__ == "__main__":

    print("\n" + "=" * 70)
    print("NAFULEARN — LESSON EVALUATOR TEST")
    print("=" * 70)

    chunks = load_lesson()

    sections = get_learning_sections(chunks)

    print(f"\nLearning sections available: {len(sections)}")

    # Use the first lesson section for testing
    current_section = sections[0]

    print(
        f"\nTesting section: "
        f"{current_section['metadata']['section']}"
    )

    # This is the understanding question generated
    # during our Learn Mode test.
    question = (
        "Why did ancient people stop relying only on "
        "fingers, stones, and marks on sticks as their "
        "communities grew?"
    )

    # Example student answer
    student_answer = (
        "They needed better ways to count and keep track "
        "of information because their communities became "
        "larger and things became more difficult to manage."
    )

    print("\nQUESTION:")
    print(question)

    print("\nSTUDENT ANSWER:")
    print(student_answer)

    print("\n" + "-" * 70)
    print("NAFULEARN EVALUATION:")
    print("-" * 70)

    evaluation = evaluate_answer(
        current_section,
        question,
        student_answer
    )

    print(evaluation)

    print("\n" + "=" * 70)
