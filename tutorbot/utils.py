from pathlib import Path
import re

PATTERN = re.compile(r'(\\begin\{verbatim\}.*?\\end\{verbatim\})', re.DOTALL)

def sanitize_latex_text(text: str) -> str:
    """
    This function is used to sanitize the text for a LaTeX file to process it properly.

    :param text: The text to sanitize. Example: "Hello & World!"
    :return: The sanitized text. Example: "Hello \\& World!"
    """
    return (
        text.replace("\u202f", " ")  # NNBSP
            .replace("\\", r"\textbackslash{}")
            .replace("&", r"\&")
            .replace("%", r"\%")
            .replace("$", r"\$")
            .replace("#", r"\#")
            .replace("_", r"\_")
            .replace("{", r"\{")
            .replace("}", r"\}")
            .replace("~", r"\textasciitilde{}")
            .replace("^", r"\textasciicircum{}")
    )

def sanitize_feedback(text: str) -> str:

    parts = PATTERN.split(text)

    for i in range(len(parts)):
        if not parts[i].startswith(r'\begin{verbatim}'):
            parts[i] = sanitize_latex_text(parts[i])

    return ''.join(parts)


def print_divider(title: str = ""):
    print("\n" + "=" * 40)
    if title:
        print("🔧 " + title)
    print("=" * 40)


def safe_filename(name: str) -> str:
    return "".join(c if c.isalnum() or c in "-_." else "_" for c in name).strip("_")


def get_assignment_paths(subject: str) -> Path:
    """
    Delivers the submission path for a given subject.

    :param subject: Example: "ssd4_ue01"
    :return: Path to the assignment folder for the given subject. Example: "assignments/ssd4_ue01
    """
    return Path("assignments") / subject


def get_submission_paths(subject: str, lastname: str, firstname: str) -> Path:
    """
    Delivers the submission path of a given student.

    :param subject: Example: "ssd4_ue01"
    :param lastname: Example: "sample"
    :param firstname: Example: "max"
    :return: Path to the submission folder for the given student. Example: "submissions/ssd4_ue01_sample_max
    """
    return Path("submissions") / subject / f"{subject}_{lastname}_{firstname}"


def get_solution_path(subject: str) -> Path:
    """
    Delivers the path to the solution folder for a given subject.

    :param subject: Example: "ssd4_ue01"
    :return: Path to the solution folder for the given subject. Example: "solutions/ssd4_ue01
    """
    return Path("solutions") / subject


def list_tasks(submission_path: Path) -> list[str]:
    """
    Delivers a list of all submission files a given submission path. (examples: aufgabe_1.md, aufgabe_2.md, ...)

    :param submission_path: Path to the submission folder for a given student. Example: submissions/ssd4_ue01_sample_max
    :return: List of task ids. Example: ["aufgabe1", "aufgabe2", ...]
    """
    return sorted([p.stem for p in submission_path.glob("aufgabe*.md")])
