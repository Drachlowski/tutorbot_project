# import tutorbot.config as config
# from openai import OpenAI
#
# client = OpenAI(
#     api_key=config.OPENAI_API_KEY
# )
#
# response = client.responses.create(
#     model="gpt-4o",
#     instructions="You are a coding assistant that talks like a pirate.",
#     input="How do I check if a Python object is an instance of a class?",
# )
#
# print(response.output_text)

from tutorbot import feedback_generator

task = "Berechne die Kraft, die auf einen Körper mit 10 kg Masse wirkt, wenn die Beschleunigung 2 m/s² beträgt."
solution = "F = m * a → F = 10 * 2 = 20 N"
student = "Ich habe F = m + a gemacht und komme auf 12. Ich glaube, das passt auch."

feedback = feedback_generator.generate_feedback(student, solution, task, max_points=10)

from pathlib import Path
from tutorbot.latex_client import render_latex
from tutorbot.formatter import render_single_feedback

base_path = Path(__file__).parent / "templates/feedback_template.tex"
f = render_single_feedback(Path("temp/output.tex"), 9, 10, "jasödlfkjsöadlkfj", solution)

latex = render_latex(f, Path("temp/output.pdf"))

# print(d)

print(feedback)