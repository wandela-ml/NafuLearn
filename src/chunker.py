from pathlib import Path
import re

from content_loader import load_all_lessons
# ============================================================
# PROJECT PATHS
# ============================================================

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Knowledge-base document



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

def get_content_type(section, section_order, parent_section=None, parent_content_type=None):
    """
    Identify the type of educational content.

    Classification is based on section titles and their
    parent sections rather than fixed section numbers.
    """

    # Get the section title
    section_title, section_level = get_section_info(section)

    title = section_title.lower().strip()

    # Remove section numbering such as "36. " or "5.1 "

    title = re.sub(r"^\d+(?:\.\d+)*\.\s*", "", title)

    # Get the parent title if one exists
    parent = ""

    if parent_section:
        parent = parent_section.lower().strip()


    # --------------------------------------------------------
    # Document and curriculum information
    # --------------------------------------------------------

    document_sections = {
        "learning objectives",
        "prior knowledge",
    }

    if title in document_sections:
        return "document_metadata"


    # --------------------------------------------------------
    # Activities
    # --------------------------------------------------------

    if (
        "activity" in title
        or "activity" in parent
    ):
        return "activity"


    # --------------------------------------------------------
    # Guided questions
    # --------------------------------------------------------

    if (
        "guided question" in title
        or "guided question" in parent
    ):
        return "guided_questions"


    


    # --------------------------------------------------------
    # Answer key
    # --------------------------------------------------------

    if (
        "answer key" in title
        or "answer key" in parent
    ):
        return "answer_key"

    if parent_content_type == "answer_key":
        return "answer_key"


    # --------------------------------------------------------
    # Practice questions
    # --------------------------------------------------------
    
    if (
        "practice question" in title
        or "practice question" in parent
        ):
        return "practice"
    
    
    # --------------------------------------------------------
    # Quiz
    # --------------------------------------------------------
    
    if (
         title == "quiz"
         or "quiz" in parent
         ):
        return "quiz"

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    if "summary" in title:
        return "summary"


    # --------------------------------------------------------
    # Revision notes
    # --------------------------------------------------------

    if (
        "revision" in title
        or "revision" in parent
    ):
        return "revision"


    # --------------------------------------------------------
    # Normal lesson content
    # --------------------------------------------------------

    return "lesson_content"


# ============================================================
# ADD METADATA
# ============================================================

def add_metadata(sections, lesson_metadata):
    """
    Attach curriculum and structural metadata to every section.
    """

    chunks = []

    for index, section in enumerate(sections):

        # Original position in the document
        section_order = index + 1

        # Extract title and Markdown heading level
        section_title, section_level = get_section_info(section)


        # Find the parent heading
        parent_section = get_parent_section(
            chunks,
            section_level
            )

        parent_content_type = None

        if parent_section:
            for previous_chunk in reversed(chunks):
                if previous_chunk["metadata"]["section"] == parent_section:

                    parent_content_type = previous_chunk["metadata"]["content_type"]
                    break



        content_type = get_content_type(
            section,
            section_order,
            parent_section,
            parent_content_type
            )

        
        # Create the chunk
        chunk = {
            "id": f"{lesson_metadata['id']}_chunk_{section_order}",
            "content": section,


            "metadata": {
                # Curriculum information
                "subject": lesson_metadata["subject"],
                "grade": lesson_metadata["grade"],
                "strand": lesson_metadata["strand"],
                "sub_strand": lesson_metadata["sub_strand"],
                "lesson": lesson_metadata["title"],

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
# CHUNK ALL LESSONS
# ============================================================

def chunk_all_lessons():
    """
    Load every lesson from the knowledge base,
    split each lesson into sections,
    add metadata to each section,
    and return all chunks together.
    """

    lessons = load_all_lessons()

    all_chunks = []

    for lesson in lessons:

        sections = split_into_sections(
            lesson["content"]
        )

        chunks = add_metadata(
            sections,
            lesson
        )

        all_chunks.extend(chunks)

    return all_chunks


# ============================================================
# TEST CHUNKER
# ============================================================

if __name__ == "__main__":

    all_chunks = chunk_all_lessons()

    print("\n" + "=" * 80)
    print("CHUNKER TEST")
    print("=" * 80)

    print(f"\nTotal chunks across all lessons: {len(all_chunks)}")

    for chunk in all_chunks:

        metadata = chunk["metadata"]

        print(
            f"{metadata['lesson']} | "
            f"{metadata['section_order']}. "
            f"{metadata['section']} | "
            f"type: {metadata['content_type']}"
        )

    print("\n" + "=" * 80)

