import json
from pathlib import Path

from lesson_navigator import (
    load_lesson,
    get_learning_sections,
)

from lesson_teacher import teach_section


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

TEACHING_DIR = (
    BASE_DIR
    / "data"
    / "teaching"
)

TEACHING_PATH = (
    TEACHING_DIR
    / "lesson_01_teaching.json"
)


# ============================================================
# GENERATE TEACHING CONTENT
# ============================================================

def generate_teaching_content():

    print("\n" + "=" * 70)
    print("NAFULEARN — GENERATING TEACHING CONTENT")
    print("=" * 70)

    # --------------------------------------------------------
    # Create teaching directory
    # --------------------------------------------------------

    TEACHING_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Load lesson
    # --------------------------------------------------------

    print("\nLoading lesson...")

    chunks = load_lesson()

    sections = get_learning_sections(
        chunks
    )

    print(
        f"Learning sections found: {len(sections)}"
    )

    # --------------------------------------------------------
    # Load existing teaching content
    # --------------------------------------------------------

    existing_content = {}

    if TEACHING_PATH.exists():

        print(
            "\nExisting teaching file found."
        )

        try:

            with open(
                TEACHING_PATH,
                "r",
                encoding="utf-8"
            ) as file:

                saved_data = json.load(file)

            for item in saved_data:

                existing_content[
                    item["position"]
                ] = item

            print(
                f"Existing sections loaded: "
                f"{len(existing_content)}"
            )

        except (json.JSONDecodeError, KeyError):

            print(
                "Existing file could not be read."
            )

            print(
                "Starting with an empty teaching cache."
            )

            existing_content = {}

    # --------------------------------------------------------
    # Generate missing sections
    # --------------------------------------------------------

    teaching_content = []

    for position, section in enumerate(sections):

        metadata = section["metadata"]

        section_title = metadata["section"]

        print("\n" + "-" * 70)

        print(
            f"SECTION {position + 1} "
            f"OF {len(sections)}"
        )

        print(
            f"Title: {section_title}"
        )

        # ----------------------------------------------------
        # Use existing content if available
        # ----------------------------------------------------

        if position in existing_content:

            print(
                "Already generated — skipping Gemini."
            )

            teaching_content.append(
                existing_content[position]
            )

            continue

        # ----------------------------------------------------
        # Generate with Gemini
        # ----------------------------------------------------

        print(
            "Generating with Gemini..."
        )

        lesson = teach_section(
            section
        )

        item = {
            "position": position,
            "section": section_title,
            "explanation": lesson["explanation"],
            "question": lesson["question"]
        }

        teaching_content.append(
            item
        )

        # ----------------------------------------------------
        # Save immediately
        # ----------------------------------------------------

        with open(
            TEACHING_PATH,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                teaching_content,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(
            "Saved."
        )

    # --------------------------------------------------------
    # Final save
    # --------------------------------------------------------

    with open(
        TEACHING_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            teaching_content,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n" + "=" * 70)

    print(
        "TEACHING CONTENT GENERATION COMPLETE"
    )

    print("=" * 70)

    print(
        f"\nSaved to:"
        f"\n{TEACHING_PATH}"
    )

    print(
        f"\nTotal sections saved: "
        f"{len(teaching_content)}"
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    generate_teaching_content()

