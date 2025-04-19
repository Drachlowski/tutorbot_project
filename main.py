import sys
from pathlib import Path
import argparse

# Pfad zur Projektstruktur ergänzen
sys.path.append(str(Path(__file__).parent.resolve()))

from tutorbot.config import OPENAI_MODEL
from tutorbot.feedback_generator import generate_feedback
from tutorbot.formatter import render_template_to_file
from tutorbot.latex_client import render_latex
from tutorbot.parser import load_student_submission
from tutorbot.utils import sanitize_latex_text


def ask_user_action(feedback: str, punkte: int, max_punkte: int) -> str:
    print("\n--- Vorschau Feedback ---")
    print(feedback)
    print(f"Punkte: {punkte} / {max_punkte}")
    print("--------------------------")
    print("[1] Bestätigen und übernehmen")
    print("[2] Überspringen")
    print("[3] Punkte manuell anpassen")
    print("[4] Neu bewerten mit Zusatzinstruktion")
    return input("Auswahl: ").strip()


def main():
    parser = argparse.ArgumentParser(description="Tutorbot Feedback Generator (interaktiv)")
    parser.add_argument("--fach", required=True, help="Übung, z.B. fach_ue01")
    parser.add_argument("--nachname", required=True, help="Nachname des Schülers")
    parser.add_argument("--vorname", required=True, help="Vorname des Schülers")
    parser.add_argument("--max", type=int, default=10, help="Maximale Punkte pro Aufgabe")
    args = parser.parse_args()

    fach_ue = args.fach
    nachname = args.nachname
    vorname = args.vorname
    max_punkte = args.max

    aufgaben = load_student_submission(fach_ue, nachname, vorname)

    if not aufgaben:
        print("Keine Aufgaben gefunden.")
        sys.exit(1)

    aufgaben_resultate = []

    for i, aufgabe in enumerate(aufgaben, start=1):
        print(f"\nAufgabe {i}: {aufgabe['task_id']}")
        instruction = ""
        while True:
            feedback = generate_feedback(
                student_text=aufgabe["student_text"],
                solution_text=aufgabe["solution_text"],
                task_description=instruction,
                max_points=max_punkte
            )

            try:
                punkte = int(feedback.split("Punkte: ")[-1].split("/")[0].strip())
            except Exception:
                punkte = 0

            action = ask_user_action(feedback, punkte, max_punkte)

            if action == "1":
                aufgaben_resultate.append({
                    "punkte": punkte,
                    "max_punkte": max_punkte,
                    "feedback": sanitize_latex_text(feedback),
                    "student_text": sanitize_latex_text(aufgabe["student_text"])
                })
                break

            elif action == "2":
                print("Aufgabe übersprungen.")
                break

            elif action == "3":
                new_punkte = input("Neue Punktezahl eingeben: ").strip()
                try:
                    punkte = int(new_punkte)
                except ValueError:
                    print("Ungültige Eingabe. Punkte bleiben unverändert.")
                aufgaben_resultate.append({
                    "punkte": punkte,
                    "max_punkte": max_punkte,
                    "feedback": sanitize_latex_text(feedback + "\n\n[Hinweis: Punkte manuell angepasst]"),
                    "student_text": sanitize_latex_text(aufgabe["student_text"])
                })
                break

            elif action == "4":
                instruction = input("Zusätzliche Anweisungen an Tutorbot: ").strip()
                print("Bewertung wird mit zusätzlicher Instruktion neu generiert...")
                continue

            else:
                print("⚠️ Ungültige Eingabe.")
                continue

    if not aufgaben_resultate:
        print("Keine Aufgaben wurden bewertet.")
        sys.exit(0)

    output_dir = Path("data/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    tex_path = output_dir / f"{fach_ue}_{nachname}_{vorname}_feedback.tex"
    pdf_path = tex_path.with_suffix(".pdf")

    tex_content = render_template_to_file(
        template_name="feedback_template_multi.tex",
        output_path=tex_path,
        context={
            "total_punkte": sum(a["punkte"] for a in aufgaben_resultate),
            "total_max": max_punkte * len(aufgaben_resultate),
            "aufgaben": aufgaben_resultate
        }
    )

    render_latex(tex_content, pdf_path)
    print(f"PDF erfolgreich erstellt: {pdf_path}")


if __name__ == "__main__":
    main()
