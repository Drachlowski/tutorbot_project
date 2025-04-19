from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from tutorbot import config
from openai import OpenAI
from pathlib import Path

client = OpenAI(
    api_key=config.OPENAI_API_KEY
)

def load_prompt(path: Path, **kwargs) -> str:
    """
    This function loads a prompt from a file and replaces placeholders with the given values.

    :param path: Path to the prompt file. Example: "prompts/user_prompt.txt"
    :param kwargs: Placeholders and their values. Example: {"task_description": "Calculate the force of a mass."}
    :return: The formatted prompt. Example: "Calculate the force of a mass.\n\nSolution: F = m \\times a"
    """
    text = path.read_text(encoding="utf-8")
    return text.format(**kwargs)


def generate_feedback1(student_text: str, solution_text: str, task_description: str, max_score: int = 10) -> str:
    """
    This function generates feedback for a student submission. It uses the OpenAI API to generate a response.

    :param student_text: Student submission. Example: "Calculate the force of a mass."
    :param solution_text: Solution to the task. Example: "F = m \\times a"
    :param task_description: Task description. Example: "Calculate the force of a mass."
    :param max_score: Maximum score possible. Example: 10
    :return: Generated feedback. Example: "Punkte: 4 / 10\nFeedback: ..."
    """
    base_path = Path(__file__).parent / "prompts"

    system_prompt = load_prompt(base_path / "system_prompt.txt", max_points=max_score)
    user_prompt = load_prompt(
        base_path / "user_prompt.txt",
        task_description=task_description,
        solution_text=solution_text,
        student_text=student_text,
        max_points=max_score
    )

    system_message = ChatCompletionSystemMessageParam(role="system", content=system_prompt)
    user_message = ChatCompletionUserMessageParam(role="user", content=user_prompt)

    response = client.chat.completions.create(
        model=config.OPENAI_MODEL,
        messages=[
            system_message,
            user_message
        ],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()

def generate_feedback(student_text: str, solution_text: str, task_description: str, max_points: int = 10) -> str:
    """
    This is just a test function. It returns a static response.

    :param student_text:
    :param solution_text:
    :param task_description:
    :param max_points:
    :return:
    """
    return """- Punkte: 4 / 10
- Feedback: 

Hallo! Vielen Dank, dass du deine Lösung eingereicht hast. Es ist toll zu sehen, dass du dich mit der Aufgabe auseinandergesetzt hast. Lass uns gemeinsam schauen, wie du deine Herangehensweise verbessern kannst.

Zunächst einmal hast du die Formel für die Berechnung der Kraft ein wenig durcheinandergebracht. Die korrekte Formel lautet \\( F = m \\times a \\), was bedeutet, dass du die Masse mit der Beschleunigung multiplizieren solltest. In deinem Fall wäre das \\( 10 \\, \\text{kg} \\times 2 \\, \\text{m/s}^2 = 20 \\, \\text{N} \\).

Du hast stattdessen die Masse und die Beschleunigung addiert, was zu einem falschen Ergebnis geführt hat. Es ist wichtig, die physikalischen Formeln korrekt anzuwenden, da sie die Grundlage für die Berechnung physikalischer Größen bilden.

Ich schätze deine Bemühungen und möchte dich ermutigen, die Formel noch einmal zu überprüfen und die Berechnung erneut durchzuführen. Du bist auf dem richtigen Weg, und mit ein wenig Übung wirst du die Konzepte sicher meistern. Wenn du Fragen hast oder weitere Unterstützung benötigst, stehe ich dir gerne zur Verfügung. Weiter so! 😊"""
