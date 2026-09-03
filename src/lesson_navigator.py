import json
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

EMBEDDINGS_PATH = (
    BASE_DIR
    / "data"
    / "embeddings"
    / "lesson_01_embeddings.json"
)


# ============================================================
# LOAD LESSON DATA
# ============================================================

def load_lesson():
    """
    Load the lesson chunks from the embeddings JSON file.
    """

    with open(
        EMBEDDINGS_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    return data


# ============================================================
# FILTER LEARNING CONTENT
# ============================================================

def get_learning_sections(chunks):
    """
    Return only sections that should appear in Learn Mode.

    Excluded:
        - document metadata
        - activities
        - guided questions
        - practice questions
        - quizzes
        - answer keys

    Summary and revision material remain available.
    """

    excluded_types = {
        "document_metadata",
        "activity",
        "guided_questions",
        "practice",
        "quiz",
        "answer_key",
    }

    learning_sections = []

    for chunk in chunks:

        content_type = chunk["metadata"]["content_type"]

        if content_type not in excluded_types:
            learning_sections.append(chunk)

    # Sort according to curriculum order
    learning_sections.sort(
        key=lambda chunk: chunk["metadata"]["section_order"]
    )

    return learning_sections


# ============================================================
# GET SECTION BY POSITION
# ============================================================

def get_section(sections, position):
    """
    Return a section using its Learn Mode position.

    Position starts at 0.
    """

    if position < 0 or position >= len(sections):
        return None

    return sections[position]


# ============================================================
# GET NEXT SECTION
# ============================================================

def get_next_section(sections, current_position):
    """
    Return the section after the current section.
    """

    next_position = current_position + 1

    return get_section(
        sections,
        next_position
    )


# ============================================================
# GET PREVIOUS SECTION
# ============================================================

def get_previous_section(sections, current_position):
    """
    Return the section before the current section.
    """

    previous_position = current_position - 1

    return get_section(
        sections,
        previous_position
    )


# ============================================================
# DISPLAY SECTION
# ============================================================

def display_section(section, position, total):
    """
    Display a lesson section in a readable format.
    """

    if section is None:
        print("\nNo section found.")
        return

    metadata = section["metadata"]

    print("\n" + "=" * 70)

    print(
        f"LEARN MODE — SECTION {position + 1} OF {total}"
    )

    print("=" * 70)

    print(
        f"\n{metadata['section']}"
    )

    print("-" * 70)

    print(section["content"])

    print("-" * 70)

    print(
        f"Content type: {metadata['content_type']}"
    )

    print(
        f"Curriculum order: {metadata['section_order']}"
    )


# ============================================================
# TEST LEARN MODE
# ============================================================

if __name__ == "__main__":

    print("\n" + "=" * 70)
    print("NAFULEARN — LEARN MODE")
    print("=" * 70)

    # --------------------------------------------------------
    # Load all chunks
    # --------------------------------------------------------

    chunks = load_lesson()

    print(
        f"\nTotal chunks loaded: {len(chunks)}"
    )

    # --------------------------------------------------------
    # Get learning sections
    # --------------------------------------------------------

    sections = get_learning_sections(chunks)

    print(
        f"Learning sections available: {len(sections)}"
    )

    # --------------------------------------------------------
    # Show first section
    # --------------------------------------------------------

    current_position = 0

    current_section = get_section(
        sections,
        current_position
    )

    display_section(
        current_section,
        current_position,
        len(sections)
    )

    # --------------------------------------------------------
    # Show next section
    # --------------------------------------------------------

    next_section = get_next_section(
        sections,
        current_position
    )

    print("\n" + "=" * 70)
    print("NEXT SECTION")
    print("=" * 70)

    if next_section:

        next_metadata = next_section["metadata"]

        print(
            f"\n{next_metadata['section']}"
        )

    # --------------------------------------------------------
    # Show last learning section
    # --------------------------------------------------------

    last_position = len(sections) - 1

    last_section = get_section(
        sections,
        last_position
    )

    print("\n" + "=" * 70)
    print("LAST LEARNING SECTION")
    print("=" * 70)

    if last_section:

        last_metadata = last_section["metadata"]

        print(
            f"\n{last_metadata['section']}"
        )

    print("\n" + "=" * 70)