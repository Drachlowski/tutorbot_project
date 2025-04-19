import os
import requests
from pathlib import Path

LATEX_RENDERER_URL = os.getenv("LATEX_RENDERER_URL")

def render_latex(tex_content: str, output_path: Path):
    """
    This function renders a LaTeX document and saves it to a file. The service latex-service is used.

    :param tex_content: The LaTeX content as a string.
    :param output_path: The path where the rendered PDF should be saved.
    :return: None
    """

    files = {'file': ('document.tex', tex_content.encode('utf-8'))}
    response = requests.post(LATEX_RENDERER_URL, files=files)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(response.content)