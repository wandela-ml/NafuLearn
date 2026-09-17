import json
from lesson_navigator import get_curriculum_structure

from flask import (
    Flask,
    jsonify,
    request,
    render_template,
    Response,
    stream_with_context,
)

from learn_mode import (
    initialize_learn_mode,
    get_learning_section,
    get_section_for_evaluation,
)
from lesson_evaluator import build_evaluation_prompt
from rag import generate_answer
from gemini_service import stream_content


app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)


# ============================================================
# HOMEPAGE
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")

# ============================================================
# MAIN DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/dashboard/grade/<int:grade>")
def grade_dashboard(grade):

    curriculum = get_curriculum_structure()

    grade_key = f"Grade {grade}"

    # Make sure the requested grade exists.
    if grade_key not in curriculum:
        return "Grade not found", 404

    grade_data = curriculum[grade_key]

    # Collect categories while preserving their order.
    categories = []

    for subject_data in grade_data.values():

        category = subject_data.get("category")

        if category and category not in categories:
            categories.append(category)

    return render_template(
        "grade_dashboard.html",
        grade=grade_key,
        categories=categories
    )

@app.route("/dashboard/grade/<int:grade>/<category>")
def category_dashboard(grade, category):

    curriculum = get_curriculum_structure()

    grade_key = f"Grade {grade}"

    # Make sure the requested grade exists.
    if grade_key not in curriculum:
        return "Grade not found", 404

    grade_data = curriculum[grade_key]

    # Find subjects belonging to the selected category.
    subjects = []

    for subject, subject_data in grade_data.items():

        if subject_data.get("category") == category:
            subjects.append(subject)

    # Make sure the category exists for this grade.
    if not subjects:
        return "Category not found", 404

    return render_template(
        "category_dashboard.html",
        grade=grade_key,
        category=category,
        subjects=subjects
    )
@app.route("/dashboard/grade/<int:grade>/<category>/<subject>")
def subject_dashboard(grade, category, subject):

    curriculum = get_curriculum_structure()

    grade_key = f"Grade {grade}"

    # Make sure the requested grade exists.
    if grade_key not in curriculum:
        return "Grade not found", 404

    grade_data = curriculum[grade_key]

    # Make sure the subject exists.
    if subject not in grade_data:
        return "Subject not found", 404

    subject_data = grade_data[subject]

    # Make sure the subject belongs to the selected category.
    if subject_data.get("category") != category:
        return "Category does not match subject", 404

    return render_template(
        "subject_dashboard.html",
        grade=grade_key,
        category=category,
        subject=subject,
        strands=subject_data.get("strands", {})
    )

@app.route("/dashboard/grade/<int:grade>/<category>/<subject>/<strand>")
def strand_dashboard(grade, category, subject, strand):

    curriculum = get_curriculum_structure()

    grade_key = f"Grade {grade}"

    # Make sure the requested grade exists.
    if grade_key not in curriculum:
        return "Grade not found", 404

    grade_data = curriculum[grade_key]

    # Make sure the subject exists.
    if subject not in grade_data:
        return "Subject not found", 404

    subject_data = grade_data[subject]

    # Make sure the subject belongs to the selected category.
    if subject_data.get("category") != category:
        return "Category does not match subject", 404

    strands = subject_data.get("strands", {})

    # Make sure the selected strand exists.
    if strand not in strands:
        return "Strand not found", 404

    sub_strands = strands[strand]

    return render_template(
        "strand_dashboard.html",
        grade=grade_key,
        category=category,
        subject=subject,
        strand=strand,
        sub_strands=sub_strands
    )

@app.route(
    "/dashboard/grade/<int:grade>/<category>/<subject>/<strand>/<sub_strand>"
)
def sub_strand_dashboard(
    grade,
    category,
    subject,
    strand,
    sub_strand
):

    curriculum = get_curriculum_structure()

    grade_key = f"Grade {grade}"

    if grade_key not in curriculum:
        return "Grade not found", 404

    grade_data = curriculum[grade_key]

    if subject not in grade_data:
        return "Subject not found", 404

    subject_data = grade_data[subject]

    if subject_data.get("category") != category:
        return "Category does not match subject", 404

    strands = subject_data.get("strands", {})

    if strand not in strands:
        return "Strand not found", 404

    sub_strands = strands[strand]

    if sub_strand not in sub_strands:
        return "Sub-strand not found", 404

    lessons = sub_strands[sub_strand]

    return render_template(
        "sub_strand_dashboard.html",
        grade=grade_key,
        category=category,
        subject=subject,
        strand=strand,
        sub_strand=sub_strand,
        lessons=lessons
    )


# ============================================================
# CURRICULUM STRUCTURE
# ============================================================

@app.route("/api/curriculum")
def curriculum():

    try:

        curriculum_data = get_curriculum_structure()

        return jsonify({
            "success": True,
            "curriculum": curriculum_data
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# ============================================================
# LEARN PAGE
# ============================================================

@app.route("/learn")
def learn():
    return render_template("learn.html")


# ============================================================
# ASK PAGE
# ============================================================

@app.route("/ask")
def ask():
    return render_template("ask.html")


# ============================================================
# SETTINGS PAGE
# ============================================================

@app.route("/settings")
def settings():
    return render_template("settings.html")


# ============================================================
# START LEARN MODE
# ============================================================

@app.route(
    "/api/learn/start",
    methods=["POST"]
)
def start_learning():
    """
    Start Learn Mode for a specific lesson.

    The lesson_id is supplied by the frontend
    in the JSON request body.
    """

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False,
            "error": "No data provided"
        }), 400

    lesson_id = data.get("lesson_id")

    if not lesson_id:

        return jsonify({
            "success": False,
            "error": "Lesson ID is required"
        }), 400

    try:

        sections = initialize_learn_mode(
            lesson_id
        )

        return jsonify({
            "success": True,
            "lesson_id": lesson_id,
            "total_sections": len(sections)
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 400

# ============================================================
# GET LEARNING SECTION
# ============================================================

@app.route("/api/learn/section/<int:position>")
def get_learn_section(position):
    """
    Get a specific section from a selected lesson.
    """

    lesson_id = request.args.get("lesson_id")

    if not lesson_id:

        return jsonify({
            "success": False,
            "error": "Lesson ID is required"
        }), 400

    try:

        sections = initialize_learn_mode(
            lesson_id
        )
        section_position = position - 1

        section_data = get_learning_section(
            sections,
            position,
            lesson_id
        )

        if section_data is None:

            return jsonify({
                "success": False,
                "error": "Section not found"
            }), 404

        section = section_data["section"]

        return jsonify({
            "success": True,
            "lesson_id": lesson_id,
            "position": section_data["position"],
            "total": section_data["total"],
            "section": section["metadata"]["section"],
            "explanation": section_data["explanation"],
            "question": section_data["question"]
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 400


# ============================================================
# EVALUATE LEARN ANSWER — STREAMING
# ============================================================

@app.route(
    "/api/learn/evaluate",
    methods=["POST"]
)
def evaluate_learn_answer():
    """
    Evaluate a student's answer using Gemini streaming.

    Gemini's response is sent to the browser progressively
    instead of waiting for the entire response first.
    """

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False,
            "error": "No data provided"
        }), 400

    lesson_id = data.get("lesson_id")
    position = data.get("position")
    question = data.get("question")
    student_answer = data.get("student_answer")

    if not lesson_id:

        return jsonify({
            "success": False,
            "error": "Lesson ID is required"
        }), 400

    if position is None:

        return jsonify({
            "success": False,
            "error": "Section position is required"
        }), 400

    if not question:

        return jsonify({
            "success": False,
            "error": "Question is required"
        }), 400

    if not student_answer:

        return jsonify({
            "success": False,
            "error": "Student answer is required"
        }), 400

    # --------------------------------------------------------
    # LOAD THE CURRENT LESSON
    # --------------------------------------------------------

    try:

        sections = initialize_learn_mode(
            lesson_id
        )

    except Exception as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 400

    section_position = position - 1

    section = get_section_for_evaluation(
        sections,
        position
    )

    if section is None:

        return jsonify({
            "success": False,
            "error": "Section not found"
        }), 404

    # --------------------------------------------------------
    # BUILD THE EVALUATION PROMPT
    # --------------------------------------------------------

    prompt = build_evaluation_prompt(
        section,
        question,
        student_answer
    )

    # --------------------------------------------------------
    # STREAM GEMINI RESPONSE
    # --------------------------------------------------------

    @stream_with_context
    def generate_stream():

        full_response = ""

        try:

            # ------------------------------------------------
            # Tell browser that evaluation has started
            # ------------------------------------------------

            yield (
                json.dumps({
                    "type": "start"
                })
                + "\n"
            )

            # ------------------------------------------------
            # Receive Gemini response chunk by chunk
            # ------------------------------------------------

            for chunk in stream_content(prompt):

                full_response += chunk

                yield (
                    json.dumps({
                        "type": "chunk",
                        "text": chunk
                    })
                    + "\n"
                )

            # ------------------------------------------------
            # Extract final result
            # ------------------------------------------------

            response_lower = full_response.lower()

            if "result: correct" in response_lower:

                result = "correct"

            elif "result: partially correct" in response_lower:

                result = "partially correct"

            elif "result: needs improvement" in response_lower:

                result = "needs improvement"

            else:

                result = "unknown"

            # ------------------------------------------------
            # Send final result to browser
            # ------------------------------------------------

            yield (
                json.dumps({
                    "type": "result",
                    "result": result
                })
                + "\n"
            )

            # ------------------------------------------------
            # Tell browser streaming is finished
            # ------------------------------------------------

            yield (
                json.dumps({
                    "type": "done"
                })
                + "\n"
            )

        except Exception as error:

            yield (
                json.dumps({
                    "type": "error",
                    "error": str(error)
                })
                + "\n"
            )

    return Response(
        generate_stream(),
        mimetype="application/x-ndjson",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


# ============================================================
# ASK NAFULEARN
# ============================================================

@app.route(
    "/api/ask",
    methods=["POST"]
)
def ask_nafulearn():
    """
    Answer a student's question using NafuLearn RAG.
    """

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False,
            "error": "No data provided"
        }), 400

    question = data.get("question")

    if not question or not question.strip():

        return jsonify({
            "success": False,
            "error": "Question is required"
        }), 400

    answer = generate_answer(
        question.strip()
    )

    return jsonify({
        "success": True,
        "question": question.strip(),
        "answer": answer
    })


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )