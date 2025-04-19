from pathlib import Path
from typing import List, Dict
from tutorbot.utils import get_submission_paths, get_solution_path, list_aufgaben

def load_student_submission(subject: str, lastname: str, firstname: str) -> List[Dict[str, str]]:
    """
    Loads all student submissions for a given student and the solutions for the corresponding subject.

    :param subject: Example: "ssd4"
    :param lastname: Example: "sample"
    :param firstname: Example: "max"
    :return: List of dictionaries with task_id, solution_text and student_text
    """
    submissions_path = Path(__file__).parent.parent / "data" / get_submission_paths(subject, lastname, firstname)
    solutions_path = Path(__file__).parent.parent / "data"/ get_solution_path(subject)

    tasks = []
    for task_id in list_aufgaben(submissions_path):
        submission_file = submissions_path / f"{task_id}.md"
        solution_file = solutions_path / f"{task_id}.md"

        if not (submission_file.exists() and solution_file.exists()):
            continue

        tasks.append({
            "task_id": task_id,
            "solution_text": solution_file.read_text(encoding="utf-8").strip(),
            "student_text": submission_file.read_text(encoding="utf-8").strip()
        })

    return tasks