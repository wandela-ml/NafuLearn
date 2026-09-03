import os
from dotenv import load_dotenv
from google import genai
from lesson_navigator import (
    load_lesson,
    get_learning_sections,
)


#==============================================================
#GEMINI SETUP
#==============================================================

load_dotenv()

api_key = os.getenv("Gemini_api_key")
if not api_key:
    raise ValueError("Gemini_api_key not found in .env file")

client = genai.Client(api_key=api_key)

#=============================================================
#BUILD EVALUATOR
#=============================================================

def build_evaluation_prompt(section, question, student_answer):
    metadata = section["metadata"]

    section_title = metadata["section"]

    lesson_content = section["content"]

    prompt = f"""
You are NafuLearn, a friendly educational tutor for
Grade 10 Computer Studies students in Kenya.

You are evaluating a student's answer based ONLY on the
lesson content provided below.

LESSON SECTION:
{section_title}

LESSON CONTENT:
------------------
{lesson_content}
------------------
QUESTION:

{question}


STUDENT'S ANSWER:

{student_answer}

Evaluate the student's understanding.

Use exactly ONE of these classifications:

Correct
Partially correct
Needs improvement

Evaluation rules:

1. "Correct" means the student demonstrates a clear and
   accurate understanding of the important idea being tested.

2. "Partially correct" means the student understands some
   of the idea but misses an important point or has a minor
   misunderstanding.

3. "Needs improvement" means the answer does not demonstrate
   sufficient understanding of the concept.

4. Base your evaluation ONLY on the lesson content provided.

5. Do not introduce unrelated information.

6. Do not punish the student for using different wording
   from the lesson.

7. Be encouraging and educational.

8. If the answer is incomplete, clearly explain what the
   student should add or understand.

9. Keep the feedback concise and suitable for a Grade 10
   student.

10. Do not simply repeat the lesson content.

Use this exact format:

RESULT: [Correct / Partially correct / Needs improvement]

FEEDBACK:
[Explain briefly why the answer received this result.]

WHAT TO IMPROVE:
[If improvement is needed, explain what the student should
understand or add. If the answer is fully correct, say
"Nothing important is missing. Well done!"]

ENCOURAGEMENT:
[One short encouraging sentence.]

"""
    return prompt

#=================================================
#EVALUATE STUDENT ANSWER
#=================================================

def evaluate_answer(section, question, student_answer):
    prompt = build_evaluation_prompt(section, question, student_answer)

    response = client.models.generate_content(
        model = "gemini-3.6-flash",
        contents=prompt
    )
    return response.text
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
