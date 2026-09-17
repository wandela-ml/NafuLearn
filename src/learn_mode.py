import json
from pathlib import Path

from lesson_navigator import (
    load_lesson,
    get_learning_sections,
    get_section,
)

from lesson_evaluator import evaluate_answer


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# CURRENT LESSON
# ============================================================

LESSON_ID = (
    "grade10_computer_studies_evolution_01"
)


# ============================================================
# TEACHING CONTENT
# ============================================================

TEACHING_DIR = (
    BASE_DIR
    / "data"
    / "teaching"
)


_teaching_cache = {}


# ============================================================
# INITIALIZE LEARN MODE
# ============================================================

def initialize_learn_mode(lesson_id):
    """
    Initialize Learn Mode for a specific lesson.
    """

    chunks = load_lesson(lesson_id)

    sections = get_learning_sections(chunks)

    return sections




# ============================================================
# LOAD TEACHING CONTENT
# ============================================================

def load_teaching_content(lesson_id):
    """
    Load teaching content for a specific lesson.
    """

    if lesson_id in _teaching_cache:
        return _teaching_cache[lesson_id]

    teaching_files = {
        "grade10_computer_studies_evolution_01":
            "lesson_01_teaching.json",

        "grade10_computer_studies_architecture_01":
            "lesson_02_teaching.json",
    }

    teaching_filename = teaching_files.get(lesson_id)

    if teaching_filename is None:
        raise ValueError(
            f"No teaching file configured for lesson "
            f"'{lesson_id}'"
        )

    teaching_path = (
        TEACHING_DIR
        / teaching_filename
    )

    if not teaching_path.exists():
        raise FileNotFoundError(
            f"Teaching content not found for lesson "
            f"'{lesson_id}': {teaching_path}"
        )

    with open(
        teaching_path,
        "r",
        encoding="utf-8"
    ) as file:
        teaching_content = json.load(file)

    _teaching_cache[lesson_id] = teaching_content

    return teaching_content

# ============================================================
# GET LEARNING SECTION
# ============================================================

def get_learning_section(sections, position, lesson_id):

    if position < 0 or position >= len(sections):
        return None

    section = get_section(
        sections,
        position
    )

    if section is None:
        return None

    teaching_content = load_teaching_content(
        lesson_id
    )

    teaching = next(
        (
            item
            for item in teaching_content
            if item["position"] == position
        ),
        None
    )

    if teaching is None:
        return None

    return {
        "position": position,
        "total": len(sections),
        "section": section,
        "explanation": teaching["explanation"],
        "question": teaching["question"]
    }


# ============================================================
# GET RAW SECTION FOR EVALUATION
# ============================================================

def get_section_for_evaluation(sections, position):
    """
    Return the original lesson section without calling Gemini.

    This is used when evaluating a student's answer.
    """

    if position < 0 or position >= len(sections):
        return None

    return get_section(
        sections,
        position
    )


# ============================================================
# EVALUATE STUDENT ANSWER
# ============================================================

def evaluate_student_answer(
    section,
    question,
    student_answer
):
    """
    Evaluate a student's answer using the existing
    lesson evaluator.
    """

    evaluation = evaluate_answer(
        section,
        question,
        student_answer
    )

    return {
        "evaluation": evaluation,
        "result": get_result(evaluation)
    }


# ============================================================
# GET RESULT
# ============================================================

def get_result(evaluation):
    """
    Extract the evaluation result from Gemini's response.
    """

    evaluation_lower = evaluation.lower()

    if "result: correct" in evaluation_lower:
        return "correct"

    if "result: partially correct" in evaluation_lower:
        return "partially correct"

    if "result: needs improvement" in evaluation_lower:
        return "needs improvement"

    return "unknown"


# ============================================================
# TERMINAL DISPLAY
# ============================================================

def display_header():

    print("\n" + "=" * 70)
    print("NAFULEARN — LEARN MODE")
    print("=" * 70)


def display_current_section(
    section,
    position,
    total
):

    metadata = section["metadata"]

    print("\n" + "=" * 70)
    print(f"SECTION {position + 1} OF {total}")
    print(f"{metadata['section']}")
    print("=" * 70)


def display_evaluation(evaluation):

    print("\n" + "=" * 70)
    print("NAFULEARN EVALUATION")
    print("=" * 70)

    print(evaluation)

    print("=" * 70)


# ============================================================
# TERMINAL QUESTION / ANSWER
# ============================================================

def ask_student_question(section, question):

    max_attempts = 2
    attempt = 1

    while attempt <= max_attempts:

        print("\n" + "-" * 70)

        if attempt == 1:
            print("YOUR ANSWER:")
        else:
            print("LET'S TRY AGAIN!")
            print(
                "Take another look at the feedback "
                "and try once more."
            )
            print("\nYOUR ANSWER:")

        student_answer = input("> ").strip()

        while not student_answer:

            print(
                "\nPlease provide an answer before continuing."
            )

            student_answer = input("> ").strip()

        print("\nNafuLearn is checking your answer...")

        evaluation = evaluate_answer(
            section,
            question,
            student_answer
        )

        display_evaluation(evaluation)

        result = get_result(evaluation)

        if result == "correct":

            print(
                "\nExcellent! You are ready to continue."
            )

            return evaluation

        if attempt < max_attempts:

            print(
                "\nWould you like to try the question again?"
            )

            retry_choice = input(
                "Press R to retry or C to continue: "
            ).strip().lower()

            if retry_choice == "r":

                attempt += 1
                continue

            return evaluation

        print(
            "\nYou've given this question a good try."
        )

        print(
            "Don't worry — learning takes practice!"
        )

        return evaluation

    return evaluation


# ============================================================
# TERMINAL LEARN MODE
# ============================================================

def run_learn_mode(lesson_id):
    display_header()

    sections = initialize_learn_mode(
        lesson_id
    )

    total_sections = len(sections)

    print(
        f"\nLearning sections available: "
        f"{total_sections}"
    )

    current_position = 0

    while True:

        current_section = get_section(
            sections,
            current_position
        )

        if current_section is None:
            print("\nNo section found.")
            break

        display_current_section(
            current_section,
            current_position,
            total_sections
        )

        print("\nNAFULEARN TEACHES:")
        print("-" * 70)

        lesson = get_learning_section(
            sections,
            current_position,
            lesson_id
        )

        if lesson is None:
            print(
                "\nNo teaching content found "
                "for this section."
            )
            break

        explanation = lesson["explanation"]
        question = lesson["question"]

        print(explanation)

        print("\n" + "-" * 70)
        print("CHECK YOUR UNDERSTANDING")
        print("-" * 70)

        print(question)

        ask_student_question(
            current_section,
            question
        )

        print("\nOPTIONS:")

        if current_position > 0:
            print("P — Previous section")

        if current_position < total_sections - 1:
            print("N — Next section")

        print("Q — Quit Learn Mode")

        choice = input(
            "\nYour choice: "
        ).strip().lower()

        if choice == "n":

            if current_position < total_sections - 1:
                current_position += 1

            else:
                print(
                    "\nYou have reached the "
                    "end of the lesson!"
                )
                break

        elif choice == "p":

            if current_position > 0:
                current_position -= 1

            else:
                print(
                    "\nYou are already at "
                    "the beginning of the lesson."
                )

        elif choice == "q":

            print(
                "\nThank you for learning "
                "with NafuLearn!"
            )
            break

        else:

            print(
                "\nPlease choose N, P, or Q."
            )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    run_learn_mode(
        "grade10_computer_studies_architecture_01"
)
    