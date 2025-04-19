from pathlib import Path
from typing import Dict, List
from jinja2 import Environment, FileSystemLoader

from tutorbot.utils import sanitize_latex_text

# Jinja2-Environment
env = Environment(
    loader=FileSystemLoader(searchpath=str(Path("templates"))),
    block_start_string="{%",
    block_end_string="%}",
    variable_start_string="{{",
    variable_end_string="}}",
    autoescape=False
)


def render_template_to_file(template_name: str, output_path: Path, context: Dict) -> str:
    """
    Renders a LaTeX-Template by using Jinja2 and writes the result to a file.

    :param template_name: Name of the .tex-template-file in the templates-folder
    :param output_path: Path of the file, which should be created
    :param context: Dictionary with placeholders for the values which should be inserted into the template
    """
    template = env.get_template(template_name)
    rendered = template.render(**context)
    output_path.write_text(rendered, encoding="utf-8")
    return rendered


def render_single_feedback(output_path: Path, score: int, max_score: int, feedback: str, student_text: str) -> str:
    """
    Renders single feedback with reached points and the GPT-output.
    Normally uses the file feedback_template_single.tex

    :param output_path: Destination for the .tex-file
    :param score: reached score
    :param max_score: the maximum score possible
    :param feedback: feedback from GPT
    :param student_text: The submission from the student
    """
    context = {
        "punkte": score,
        "max_punkte": max_score,
        "feedback": sanitize_latex_text(feedback),
        "student_text": sanitize_latex_text(student_text)
    }
    return render_template_to_file("feedback_template_single.tex", output_path, context)


def render_multi_feedback(output_path: Path, tasks: List[Dict]) -> str:
    """
    Renders a feedback document with multiple tasks.

    Each task is represented as a dictionary with:
    - score
    - max score
    - feedback

    :param output_path: Destination for the .tex-file
    :param tasks: List of task dictionaries (actual tasks for the student)
    """
    sanitized_tasks = []
    total_score = 0
    total_max_score = 0

    for task in tasks:
        score = int(task["punkte"])
        max_score = int(task["max_punkte"])
        total_score += score
        total_max_score += max_score

        sanitized_tasks.append({
            "punkte": score,
            "max_punkte": max_score,
            "feedback": sanitize_latex_text(task["feedback"]),
            "student_text": sanitize_latex_text(task.get("student_text", ""))
        })

    context = {
        "total_punkte": total_score,
        "total_max": total_max_score,
        "aufgaben": sanitized_tasks
    }

    return render_template_to_file("feedback_template_multi.tex", output_path, context)
