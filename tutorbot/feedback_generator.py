from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from tutorbot import config
from openai import OpenAI
from pathlib import Path

from tutorbot.parser import parse_feedback

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


def generate_feedback(student_text: str, solution_text: str, task_description: str, additional_instructions: str = "") -> dict:
    """
    This function generates feedback for a student submission. It uses the OpenAI API to generate a response.

    :param student_text: Student submission. Example: "Calculate the force of a mass."
    :param solution_text: Solution to the task. Example: "F = m \\times a"
    :param task_description: Task description. Example: "Calculate the force of a mass."
    :param additional_instructions: Additional instructions for the student. Example: "Don't forget to include the unit of the force.
    :return: Generated feedback. Example: "Punkte: 4 / 10\nFeedback: ..."
    """
    base_path = Path(__file__).parent / "prompts"

    system_prompt = load_prompt(base_path / "system_prompt.txt")
    user_prompt = load_prompt(
        base_path / "user_prompt.txt",
        task_description=task_description,
        solution_text=solution_text,
        student_text=student_text,
        additional_instructions=additional_instructions
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

    return parse_feedback(response.choices[0].message.content)
