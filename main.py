import sys
from pathlib import Path
import argparse

from tutorbot.feedback_generator import generate_feedback
from tutorbot.formatter import render_template_to_file
from tutorbot.latex_client import render_latex
from tutorbot.parser import load_student_submission
from tutorbot.utils import sanitize_feedback

base_path = Path().resolve()
sys.path.append(str(base_path))

def ask_user_action(feedback: str, score: int, max_score: int) -> str:
    print("\n--- Feedback preview ---")
    print(feedback)
    print(f"Score: {score} / {max_score}")
    print("--------------------------")
    print("[1] Confirm and apply")
    print("[2] Skip")
    print("[3] Adjust score manually")
    print("[4] New evaluation with additional instructions")
    return input("Selection: ").strip()


def process_task(task_id, task) -> dict | None:
    print(f"\nTask {task_id}: {task['task_id']}")
    additional_instruction = ""

    while True:
        feedback = generate_feedback(
            student_text=task["student_text"],
            solution_text=task["solution_text"],
            task_description=task["task_description"],
            additional_instructions=additional_instruction
        )

        action = ask_user_action(feedback['feedback'], feedback['score'], feedback['max_score'])

        if action == "1":
            print("Task confirmed and applied.")
            return feedback

        elif action == "2":
            print("Task skipped.")
            return None

        elif action == "3":
            new_score = input("New score: ").strip()
            try:
                new_score = float(new_score)
                if new_score < 0 or new_score > feedback['max_score']:
                    raise ValueError()
                feedback['score'] = new_score
                return feedback
            except ValueError:
                print("Invalid input. Score not changed.")

        elif action == "4":
            additional_instruction = input("Additional instructions: ").strip()
            print("Feedback will be generated with additional instructions.")

        else:
            print("Invalid input. Action not accepted.")


def process_student(subject: str, lastname: str, firstname: str) -> None:
    submission = load_student_submission(subject, lastname, firstname)

    if not submission:
        print(f"No submission found for student {lastname} {firstname} in subject {subject}.")
        return#
    else:
        print(f"Found {len(submission)} tasks for student {lastname} {firstname} in subject {subject}.")

    task_results = list()
    total_score = 0
    real_max_score = 0

    for i, task in enumerate(submission, start=1):
        print(f"\nTask {i}: {task['task_id']}")
        feedback = process_task(i, task)
        print(feedback)
        feedback['submission'] = sanitize_feedback(feedback['submission'])
        feedback['feedback'] = sanitize_feedback(feedback['feedback'])

        if feedback:
            task_results.append(feedback)
            total_score += feedback['score']
            real_max_score += feedback['max_score']

    output_dir = Path("data/output") / subject
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "tex").mkdir(exist_ok=True)
    (output_dir / "pdf").mkdir(exist_ok=True)
    tex_path = output_dir / "tex" / f"{subject}_{lastname}_{firstname}_feedback.tex"
    pdf_path = output_dir / "pdf" / f"{subject}_{lastname}_{firstname}_feedback.pdf"

    print(task_results)

    tex_content = render_template_to_file(
        template_name="feedback_template_multi.tex",
        output_path=tex_path,
        context={
            "score": total_score,
            "max_score": real_max_score,
            "task_results": task_results
        }
    )

    render_latex(tex_content, pdf_path)
    print(
        f"PDF created successfully: {pdf_path}\n"
        f"Total score: {total_score} / {real_max_score}"
    )


def parse_arguments() -> dict:
    parser = argparse.ArgumentParser(description="Tutorbot Feedback Generator")
    parser.add_argument("--subject", required=True, help="Übung, z.B. fach_ue01")
    parser.add_argument("--lastname", help="Last name of a student (optional)")
    parser.add_argument("--firstname", help="Last name of a student (optional)")
    args = parser.parse_args()

    args_dict = dict()
    args_dict["subject"] = args.subject
    args_dict["lastname"] = args.lastname
    args_dict["firstname"] = args.firstname

    if args.lastname and not args.firstname:
        print("Error: First name must be provided if last name is provided.")
        sys.exit(1)

    elif args.firstname and not args.lastname:
        print("Error: Last name must be provided if first name is provided.")
        sys.exit(1)

    return args_dict


def load_all_students(subject: str) -> list:
    students = list()

    for student_dir in Path(f"data/submissions/{subject}").iterdir():
        if student_dir.is_dir():
            lastname = student_dir.name.split("_")[2]
            firstname = student_dir.name.split("_")[3]
            students.append((lastname, firstname))
    return students


if __name__ == "__main__":

    args = parse_arguments()

    if args["lastname"] and args["firstname"]:
        process_student(args["subject"], args["lastname"], args["firstname"])
        exit()

    for student in load_all_students(args["subject"]):
        process_student(args["subject"], student[0], student[1])
