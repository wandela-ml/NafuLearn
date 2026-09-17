from pathlib import Path
import yaml


# =============================================================
# CONTENT LOADER
# =============================================================

# Location of the lesson files
KNOWLEDGE_BASE = Path(__file__).resolve().parent.parent / "data" / "knowledge_base"


# =============================================================
# REQUIRED LESSON METADATA
# =============================================================

REQUIRED_METADATA = [
    "id",
    "title",
    "subject",
    "grade",
    "strand",
    "sub_strand",
    "lesson_number",
]

# =============================================================
# LOAD ONE LESSON
# =============================================================

def load_lesson(file_path):
    """
    Load one Markdown lesson file.

    Returns:
        A dictionary containing:
        - lesson metadata
        - lesson content
        - file path
    """

    file_path = Path(file_path)

    text = file_path.read_text(encoding="utf-8")

    # ---------------------------------------------------------
    # Check that the file contains YAML front matter
    # ---------------------------------------------------------

    if not text.startswith("---"):
        raise ValueError(
            f"Lesson file does not start with YAML front matter: {file_path}"
        )

    # ---------------------------------------------------------
    # Separate YAML metadata from lesson content
    # ---------------------------------------------------------

    parts = text.split("---", 2)

    if len(parts) != 3:
        raise ValueError(
            f"Invalid YAML front matter in lesson file: {file_path}"
        )

    yaml_text = parts[1]
    lesson_content = parts[2].strip()

    # ---------------------------------------------------------
    # Convert YAML into a Python dictionary
    # ---------------------------------------------------------

    metadata = yaml.safe_load(yaml_text)

    if not isinstance(metadata, dict):
        raise ValueError(
            f"Lesson metadata must be a dictionary: {file_path}"
        )

    # ---------------------------------------------------------
# Validate required metadata
# ---------------------------------------------------------

    missing_fields = [
        field
        for field in REQUIRED_METADATA
        if field not in metadata or metadata[field] is None
        ]


    if missing_fields:
        raise ValueError(
            f"Missing required metadata in {file_path}: "
            f"{', '.join(missing_fields)}"
              )

    # ---------------------------------------------------------
    # Return everything the application needs
    # ---------------------------------------------------------

    return {
        "id": metadata.get("id"),
        "title": metadata.get("title"),
        "subject": metadata.get("subject"),
        "grade": metadata.get("grade"),
        "strand": metadata.get("strand"),
        "sub_strand": metadata.get("sub_strand"),
        "lesson_number": metadata.get("lesson_number"),
        "content": lesson_content,
        "path": str(file_path),
    }


# =============================================================
# FIND ALL LESSON FILES
# =============================================================

def find_lesson_files():
    """
    Find all Markdown lesson files inside the knowledge base.

    rglob() searches through all subfolders automatically.
    """

    return sorted(KNOWLEDGE_BASE.rglob("*.md"))


# =============================================================
# LOAD ALL LESSONS
# =============================================================

def load_all_lessons():
    """
    Find and load every Markdown lesson in the knowledge base.
    """

    lessons = []

    for file_path in find_lesson_files():
        lesson = load_lesson(file_path)
        lessons.append(lesson)

    return lessons


# =============================================================
# TEST CONTENT LOADER
# =============================================================

if __name__ == "__main__":

    lessons = load_all_lessons()

    print(f"\nLessons found: {len(lessons)}")

    for lesson in lessons:
        print("\n-----------------------------")
        print("ID:", lesson["id"])
        print("Title:", lesson["title"])
        print("Subject:", lesson["subject"])
        print("Grade:", lesson["grade"])
        print("Strand:", lesson["strand"])
        print("Sub-strand:", lesson["sub_strand"])
        print("Lesson number:", lesson["lesson_number"])
        print("Content characters:", len(lesson["content"]))
        print("Path:", lesson["path"])

        print("\nFirst 500 characters of content:")
        print(lesson["content"][:500])