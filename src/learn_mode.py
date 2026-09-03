from lesson_navigator import (
    load_lesson,
    get_learning_sections,
    get_section,
)

from lesson_teacher import teach_section
from lesson_evaluator import evaluate_answer


def display_header():
    print("\n" + "=" * 70)
    print("NAFULEARN — LEARN MODE")
    print("=" * 70)


def display_current_section(section, position, total):
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


def ask_student_question(section, question):
    """
    Ask the student the understanding question
    and evaluate the answer.

    Returns the final evaluation.
    """

    max_attempts = 2
    attempt = 1

    while attempt <= max_attempts:

        print("\n" + "-" * 70)

        if attempt == 1:
            print("YOUR ANSWER:")
        else:
            print("LET'S TRY AGAIN!")
            print("Take another look at the feedback and try once more.")
            print("\nYOUR ANSWER:")

        student_answer = input("> ").strip()

        # ---------------------------------------------
        # EMPTY ANSWER
        # ---------------------------------------------

        while not student_answer:
            print("\nPlease provide an answer before continuing.")
            student_answer = input("> ").strip()

        # ---------------------------------------------
        # EVALUATE
        # ---------------------------------------------

        print("\nNafuLearn is checking your answer...")

        evaluation = evaluate_answer(
            section,
            question,
            student_answer
        )

        display_evaluation(evaluation)

        result = get_result(evaluation)

        # ---------------------------------------------
        # CORRECT
        # ---------------------------------------------

        if result == "correct":
            print("\nExcellent! You are ready to continue.")
            return evaluation

        # ---------------------------------------------
        # TRY AGAIN
        # ---------------------------------------------

        if attempt < max_attempts:

            print("\nWould you like to try the question again?")

            retry_choice = input(
                "Press R to retry or C to continue: "
            ).strip().lower()

            if retry_choice == "r":
                attempt += 1
                continue

            return evaluation

        # ---------------------------------------------
        # MAX ATTEMPTS REACHED
        # ---------------------------------------------

        print(
            "\nYou've given this question a good try."
        )

        print(
            "Don't worry — learning takes practice!"
        )

        return evaluation

    return evaluation


def run_learn_mode():

    display_header()

    chunks = load_lesson()

    sections = get_learning_sections(chunks)

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

        # -------------------------------------------------
        # DISPLAY SECTION
        # -------------------------------------------------

        display_current_section(
            current_section,
            current_position,
            total_sections
        )

        # -------------------------------------------------
        # TEACH SECTION
        # -------------------------------------------------

        print("\nNAFULEARN TEACHES:")
        print("-" * 70)

        lesson = teach_section(current_section)

        explanation = lesson["explanation"]
        question = lesson["question"]

        print(explanation)

        # -------------------------------------------------
        # CHECK UNDERSTANDING
        # -------------------------------------------------

        print("\n" + "-" * 70)
        print("CHECK YOUR UNDERSTANDING")
        print("-" * 70)

        print(question)

        # -------------------------------------------------
        # ASK AND EVALUATE
        # -------------------------------------------------

        ask_student_question(
            current_section,
            question
        )

        # -------------------------------------------------
        # NAVIGATION
        # -------------------------------------------------

        print("\nOPTIONS:")

        if current_position > 0:
            print("P — Previous section")

        if current_position < total_sections - 1:
            print("N — Next section")

        print("Q — Quit Learn Mode")

        choice = input(
            "\nYour choice: "
        ).strip().lower()

        # -------------------------------------------------
        # NEXT
        # -------------------------------------------------

        if choice == "n":

            if current_position < total_sections - 1:
                current_position += 1
            else:
                print(
                    "\nYou have reached the end "
                    "of the lesson!"
                )
                break

        # -------------------------------------------------
        # PREVIOUS
        # -------------------------------------------------

        elif choice == "p":

            if current_position > 0:
                current_position -= 1
            else:
                print(
                    "\nYou are already at the beginning "
                    "of the lesson."
                )

        # -------------------------------------------------
        # QUIT
        # -------------------------------------------------

        elif choice == "q":

            print(
                "\nThank you for learning with NafuLearn!"
            )

            break

        # -------------------------------------------------
        # INVALID CHOICE
        # -------------------------------------------------

        else:

            print(
                "\nPlease choose N, P, or Q."
            )


if __name__ == "__main__":
    run_learn_mode()