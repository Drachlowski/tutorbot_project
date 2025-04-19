from pathlib import Path
from typing import Dict, List
from jinja2 import Environment, FileSystemLoader

# Jinja2-Umgebung konfigurieren
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
    Rendert ein LaTeX-Template mit Jinja2 und schreibt das Ergebnis in die angegebene Datei.

    :param template_name: Name der .tex-Template-Datei im templates/-Ordner
    :param output_path: Pfad zur Zieldatei (.tex), die erstellt werden soll
    :param context: Dictionary mit Platzhaltern und Werten für das Template
    """
    template = env.get_template(template_name)
    rendered = template.render(**context)
    output_path.write_text(rendered, encoding="utf-8")
    return rendered


def render_single_feedback(output_path: Path, punkte: int, max_punkte: int, feedback: str, student_text: str) -> str:
    """
    Rendert ein Einzelfeedback mit Punktzahl und GPT-Ausgabe.
    Verwendet: feedback_template_single.tex

    :param output_path: Zielpfad der .tex-Datei
    :param punkte: Vergebene Punkte
    :param max_punkte: Maximal mögliche Punkte
    :param feedback: Feedback-Text
    """
    context = {
        "punkte": punkte,
        "max_punkte": max_punkte,
        "feedback": sanitize_latex_text(feedback),
        "student_text": sanitize_latex_text(student_text)
    }
    return render_template_to_file("feedback_template_single.tex", output_path, context)


def render_multi_feedback(output_path: Path, aufgaben: List[Dict]) -> str:
    """
    Rendert ein Feedback-Dokument mit mehreren Aufgaben.

    Jede Aufgabe ist ein Dictionary mit:
    - punkte
    - max_punkte
    - feedback

    :param output_path: Zielpfad der .tex-Datei
    :param aufgaben: Liste von Aufgaben mit Bewertung
    """
    sanitized_aufgaben = []
    total_punkte = 0
    total_max = 0

    for aufgabe in aufgaben:
        punkte = int(aufgabe["punkte"])
        max_punkte = int(aufgabe["max_punkte"])
        total_punkte += punkte
        total_max += max_punkte

        sanitized_aufgaben.append({
            "punkte": punkte,
            "max_punkte": max_punkte,
            "feedback": sanitize_latex_text(aufgabe["feedback"]),
            "student_text": sanitize_latex_text(aufgabe.get("student_text", ""))
        })

    context = {
        "total_punkte": total_punkte,
        "total_max": total_max,
        "aufgaben": sanitized_aufgaben
    }

    render_template_to_file("feedback_template_multi.tex", output_path, context)

def sanitize_latex_text(text: str) -> str:
    return (
        text.replace("\u202f", " ")  # NNBSP → normales Leerzeichen
            .replace("&", r"\&")
            .replace("%", r"\%")
            .replace("$", r"\$")
            .replace("#", r"\#")
            .replace("_", r"\_")
            .replace("{", r"\{")
            .replace("}", r"\}")
            .replace("~", r"\textasciitilde{}")
            .replace("^", r"\textasciicircum{}")
            .replace("\\", r"\textbackslash{}")
    )