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
    / "all_embeddings_local.json"
)


# ============================================================
# LOAD ALL EMBEDDINGS
# ============================================================

def load_all_embeddings():
    """
    Load all chunks from the combined embeddings file.
    """

    with open(
        EMBEDDINGS_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ============================================================
# CURRICULUM NAVIGATION
# ============================================================

def get_curriculum_structure():
    """
    Build the curriculum hierarchy.

    Structure:

        Grade
            ↓
        Subject
            ↓
        Strand
            ↓
        Sub-strand
            ↓
        Lesson

    All Grades (10, 11, 12) and all subjects are
    created even when no lessons currently exist.

    Existing lesson metadata is then used to populate
    the appropriate subject, strand, sub-strand and lesson.
    """

    # =========================================================
    # CURRICULUM SUBJECTS
    # =========================================================

    categories = {
        "Core subjects": [
            "English",
            "Kiswahili",
            "Mathematics",
            "Community service"
        ],

        "STEM pathway subjects": [
            "Biology",
            "Physics",
            "Chemistry",
            "Agriculture",
            "Computer studies",
            "Home science",
            "Aviation",
            "Metal work",
            "Electricity",
            "Building and construction",
            "Power mechanics",
            "Wood work"
        ],

        "Social sciences": [
            "History and Citizenship",
            "Geography",
            "Business studies",
            "Religious Education"
        ],

        "Arts and Sports sciences": [
            "Music and Dance",
            "Sports and Recreation",
            "Theatre and Film",
            "Fine Arts"
        ],

        "Non-examinable": [
            "Physical Education",
            "Information and Communication technology"
        ]
    }

    # =========================================================
    # INITIALIZE CURRICULUM
    # =========================================================

    curriculum = {}

    for grade in ["Grade 10", "Grade 11", "Grade 12"]:

        curriculum[grade] = {}

        for category, subjects in categories.items():

            for subject in subjects:

                curriculum[grade][subject] = {
                    "category": category,
                    "strands": {}
                }

    # =========================================================
    # LOAD EXISTING LESSON DATA
    # =========================================================

    data = load_all_embeddings()

    # Keep track of lessons already added.
    seen_lessons = set()

    for chunk in data:

        metadata = chunk.get("metadata", {})

        lesson_id = metadata.get("lesson_id")

        if not lesson_id:

            chunk_id = chunk.get("id", "")

            if "_chunk_" in chunk_id:

                lesson_id = chunk_id.rsplit("_chunk_", 1)[0]

                if not lesson_id:
                    continue

        # Avoid adding the same lesson repeatedly.
        if lesson_id in seen_lessons:
            continue

        # =====================================================
        # GET METADATA
        # =====================================================

        grade = metadata.get("grade")
        subject = metadata.get("subject")
        strand = metadata.get("strand")
        sub_strand = metadata.get("sub_strand")
        lesson = metadata.get("lesson")

        # Skip incomplete metadata.
        if not all([
            grade,
            subject,
            strand,
            sub_strand,
            lesson
        ]):
            continue

        # =====================================================
        # NORMALIZE GRADE
        # =====================================================

        if isinstance(grade, int):
            grade = f"Grade {grade}"

        elif isinstance(grade, str):

            if grade.isdigit():
                grade = f"Grade {grade}"

        # =====================================================
        # NORMALIZE SUBJECT
        # =====================================================

        subject_map = {
            "Computer Studies": "Computer studies"
        }

        subject = subject_map.get(subject, subject)

        # =====================================================
        # MAKE SURE GRADE EXISTS
        # =====================================================

        if grade not in curriculum:
            curriculum[grade] = {}

        # =====================================================
        # MAKE SURE SUBJECT EXISTS
        # =====================================================

        if subject not in curriculum[grade]:

            curriculum[grade][subject] = {
                "category": "Other",
                "strands": {}
            }

        # =====================================================
        # STRAND
        # =====================================================

        strands = curriculum[grade][subject]["strands"]

        if strand not in strands:
            strands[strand] = {}

        # =====================================================
        # SUB-STRAND
        # =====================================================

        if sub_strand not in strands[strand]:
            strands[strand][sub_strand] = []

        # =====================================================
        # LESSON
        # =====================================================

        strands[strand][sub_strand].append({
            "lesson": lesson,
            "lesson_id": lesson_id,
            "lesson_number": metadata.get("lesson_number")
        })

        seen_lessons.add(lesson_id)

    return curriculum
# ============================================================
# LOAD LESSON DATA
# ============================================================

def load_lesson(lesson_id):
    """
    Load chunks belonging to one specific lesson.

    The embeddings file contains multiple lessons.
    lesson_id is used to select the requested lesson.
    """

    with open(
        EMBEDDINGS_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    lesson_chunks = [
        chunk
        for chunk in data
        if chunk["metadata"].get("lesson_id") == lesson_id
        or chunk["id"].startswith(f"{lesson_id}_chunk_")
    ]

    if not lesson_chunks:
        raise ValueError(
            f"No chunks found for lesson ID: {lesson_id}"
        )

    return lesson_chunks


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
# DISPLAY CURRICULUM STRUCTURE
# ============================================================

def display_curriculum_structure(curriculum):
    """
    Display the curriculum hierarchy in a readable format.
    """

    print("\n" + "=" * 70)
    print("NAFULEARN CURRICULUM STRUCTURE")
    print("=" * 70)

    for grade in sorted(
        curriculum.keys(),
        key=lambda value: int(value)
    ):

        print(f"\nGRADE {grade}")
        print("-" * 70)

        subjects = curriculum[grade]

        for subject in subjects:

            print(f"\n  SUBJECT: {subject}")

            strands = subjects[subject]

            for strand in strands:

                print(f"    STRAND: {strand}")

                sub_strands = strands[strand]

                for sub_strand in sub_strands:

                    print(
                        f"      SUB-STRAND: {sub_strand}"
                    )

                    lessons = sub_strands[sub_strand]

                    for lesson in lessons:

                        print(
                            f"        LESSON: "
                            f"{lesson['lesson']}"
                        )

                        print(
                            f"          ID: "
                            f"{lesson['lesson_id']}"
                        )

    print("\n" + "=" * 70)


# ============================================================
# TEST LESSON NAVIGATOR
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # TEST CURRICULUM STRUCTURE
    # --------------------------------------------------------

    curriculum = get_curriculum_structure()

    display_curriculum_structure(
        curriculum
    )

    # --------------------------------------------------------
    # LESSON 1
    # --------------------------------------------------------

    lesson_1_id = (
        "grade10_computer_studies_evolution_01"
    )

    lesson_1_chunks = load_lesson(
        lesson_1_id
    )

    lesson_1_sections = get_learning_sections(
        lesson_1_chunks
    )

    print("\nLESSON 1")
    print("-" * 70)

    print(
        f"Total chunks: {len(lesson_1_chunks)}"
    )

    print(
        f"Learning sections: {len(lesson_1_sections)}"
    )

    for section in lesson_1_sections[:5]:

        metadata = section["metadata"]

        print(
            f"{metadata['section_order']}. "
            f"{metadata['section']}"
        )

    # --------------------------------------------------------
    # LESSON 2
    # --------------------------------------------------------

    lesson_2_id = (
        "grade10_computer_studies_architecture_01"
    )

    lesson_2_chunks = load_lesson(
        lesson_2_id
    )

    lesson_2_sections = get_learning_sections(
        lesson_2_chunks
    )

    print("\nLESSON 2")
    print("-" * 70)

    print(
        f"Total chunks: {len(lesson_2_chunks)}"
    )

    print(
        f"Learning sections: {len(lesson_2_sections)}"
    )

    for section in lesson_2_sections:

        metadata = section["metadata"]

        print(
            f"{metadata['section_order']}. "
            f"{metadata['section']}"
        )

    # --------------------------------------------------------
    # TEST NAVIGATION
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("NAVIGATION TEST — LESSON 1")
    print("=" * 70)

    current_position = 0

    current_section = get_section(
        lesson_1_sections,
        current_position
    )

    print("\nCurrent:")

    if current_section:
        print(
            current_section["metadata"]["section"]
        )

    next_section = get_next_section(
        lesson_1_sections,
        current_position
    )

    print("\nNext:")

    if next_section:
        print(
            next_section["metadata"]["section"]
        )

    previous_section = get_previous_section(
        lesson_1_sections,
        current_position
    )

    print("\nPrevious:")

    if previous_section:
        print(
            previous_section["metadata"]["section"]
        )
    else:
        print("None — already at the beginning.")

    print("\n" + "=" * 70)