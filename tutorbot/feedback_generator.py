from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from tutorbot import config
from openai import OpenAI
from pathlib import Path

client = OpenAI(
    api_key=config.OPENAI_API_KEY
)

def load_prompt(path: Path, **kwargs) -> str:
    text = path.read_text(encoding="utf-8")
    return text.format(**kwargs)


def generate_feedback1(student_text: str, solution_text: str, task_description: str, max_points: int = 10) -> str:
    base_path = Path(__file__).parent / "prompts"

    system_prompt = load_prompt(base_path / "system_prompt.txt", max_points=max_points)
    user_prompt = load_prompt(
        base_path / "user_prompt.txt",
        task_description=task_description,
        solution_text=solution_text,
        student_text=student_text,
        max_points=max_points
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

    print(response.usage)

    return response.choices[0].message.content.strip()

def generate_feedback(student_text: str, solution_text: str, task_description: str, max_points: int = 10) -> str:
    return """- Punkte: 4 / 10
- Feedback: 

Hallo! Vielen Dank, dass du deine Lösung eingereicht hast. Es ist toll zu sehen, dass du dich mit der Aufgabe auseinandergesetzt hast. Lass uns gemeinsam schauen, wie du deine Herangehensweise verbessern kannst.

Zunächst einmal hast du die Formel für die Berechnung der Kraft ein wenig durcheinandergebracht. Die korrekte Formel lautet \\( F = m \\times a \\), was bedeutet, dass du die Masse mit der Beschleunigung multiplizieren solltest. In deinem Fall wäre das \\( 10 \\, \\text{kg} \\times 2 \\, \\text{m/s}^2 = 20 \\, \\text{N} \\).

Du hast stattdessen die Masse und die Beschleunigung addiert, was zu einem falschen Ergebnis geführt hat. Es ist wichtig, die physikalischen Formeln korrekt anzuwenden, da sie die Grundlage für die Berechnung physikalischer Größen bilden.

Ich schätze deine Bemühungen und möchte dich ermutigen, die Formel noch einmal zu überprüfen und die Berechnung erneut durchzuführen. Du bist auf dem richtigen Weg, und mit ein wenig Übung wirst du die Konzepte sicher meistern. Wenn du Fragen hast oder weitere Unterstützung benötigst, stehe ich dir gerne zur Verfügung. Weiter so! 😊"""
