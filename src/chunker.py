from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Knowledge-base document
LESSON_PATH = (
    BASE_DIR
    / "data"
    / "knowledge_base"
    / "grade10"
    / "computer_studies"
    / "foundation"
    / "evolution_of_computers"
    / "lesson_01_early_computing.md"
)


# ============================================================
# LOAD DOCUMENT
# ============================================================

def load_document(file_path):
    """Read a Markdown document and return its contents."""

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


# ============================================================
# SPLIT DOCUMENT INTO SECTIONS
# ============================================================

def split_into_sections(text):
    """
    Split the document using Markdown headings.

    Each heading starts a new section.
    """

    sections = []
    current_section = []

    for line in text.splitlines():

        if (
            line.startswith("# ")
            or line.startswith("## ")
            or line.startswith("### ")
        ):

            if current_section:
                sections.append(
                    "\n".join(current_section).strip()
                )

            current_section = [line]

        else:
            current_section.append(line)

    # Add the final section
    if current_section:
        sections.append(
            "\n".join(current_section).strip()
        )

    return sections


# ============================================================
# IDENTIFY SECTION INFORMATION
# ============================================================

def get_section_info(section):
    """
    Extract the section title and Markdown heading level.

    Returns:
        title: The heading text
        level: Markdown heading level (1, 2, or 3)
    """

    for line in section.splitlines():

        if line.startswith("### "):
            return line[4:].strip(), 3

        if line.startswith("## "):
            return line[3:].strip(), 2

        if line.startswith("# "):
            return line[2:].strip(), 1

    return "Untitled Section", None


# ============================================================
# FIND PARENT SECTION
# ============================================================

def get_parent_section(processed_sections, current_level):
    """
    Find the most recent higher-level heading.

    Example:

        ## 4. The Pascaline
        ### Physical Description

    The parent of "Physical Description" is
    "4. The Pascaline".
    """

    if current_level is None:
        return None

    for previous in reversed(processed_sections):

        previous_level = previous["metadata"]["section_level"]

        if (
            previous_level is not None
            and previous_level < current_level
        ):
            return previous["metadata"]["section"]

    return None


# ============================================================
# IDENTIFY CONTENT TYPE
# ============================================================

def get_content_type(section, section_order):
    """
    Identify the type of educational content.

    The lesson follows a known structure, so section order
    is used to classify special sections reliably.
    """

    # --------------------------------------------------------
    # Document and curriculum information
    # --------------------------------------------------------

    if section_order <= 6:
        return "document_metadata"


    # --------------------------------------------------------
    # Activities
    # --------------------------------------------------------

    if section_order in [34, 35, 36]:
        return "activity"


    # --------------------------------------------------------
    # Guided questions
    # --------------------------------------------------------

    if section_order == 37:
        return "guided_questions"


    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    if section_order == 42:
        return "summary"


    # --------------------------------------------------------
    # Revision notes
    # --------------------------------------------------------

    if section_order in [43, 44, 45, 46]:
        return "revision"


    # --------------------------------------------------------
    # Practice questions
    # --------------------------------------------------------

    if section_order == 47:
        return "practice"


    # --------------------------------------------------------
    # Quiz
    # --------------------------------------------------------

    if section_order == 48:
        return "quiz"


    # --------------------------------------------------------
    # Individual practice questions
    # --------------------------------------------------------

    if 49 <= section_order <= 53:
        return "practice"


    # --------------------------------------------------------
    # Answer key
    # --------------------------------------------------------

    if section_order == 54:
        return "answer_key"


    # --------------------------------------------------------
    # Normal lesson content
    # --------------------------------------------------------

    return "lesson_content"


# ============================================================
# ADD METADATA
# ============================================================

def add_metadata(sections):
    """
    Attach curriculum and structural metadata to every section.
    """

    chunks = []

    for index, section in enumerate(sections):

        # Original position in the document
        section_order = index + 1

        # Extract title and Markdown heading level
        section_title, section_level = get_section_info(section)

        # Identify type of educational content
        content_type = get_content_type(
            section,
            section_order
        )

        # Find the parent heading
        parent_section = get_parent_section(
            chunks,
            section_level
        )

        # Create the chunk
        chunk = {
            "id": f"lesson_01_chunk_{section_order}",

            "content": section,

            "metadata": {
                # Curriculum information
                "subject": "Computer Studies",
                "grade": "10",
                "strand": "Foundation of Computer Studies",
                "sub_strand": "Evolution and Development of Computers",
                "lesson": "Early Computing Devices",

                # Structural information
                "section": section_title,
                "section_order": section_order,
                "section_level": section_level,
                "parent_section": parent_section,

                # Educational purpose
                "content_type": content_type,
            }
        }

        chunks.append(chunk)

    return chunks


# ============================================================
# TEST THE CHUNKER
# ============================================================

if __name__ == "__main__":

    # Load the lesson
    document = load_document(LESSON_PATH)

    # Split it into sections
    sections = split_into_sections(document)

    # Add metadata
    chunks = add_metadata(sections)

    print(f"Number of chunks: {len(chunks)}")

    print("\n" + "=" * 80)

    for chunk in chunks:

        metadata = chunk["metadata"]

        print(
            f"{metadata['section_order']}. "
            f"{metadata['section']} "
            f"| level: {metadata['section_level']} "
            f"| parent: {metadata['parent_section']} "
            f"| type: {metadata['content_type']}"
        )

    print("\n" + "=" * 80)
