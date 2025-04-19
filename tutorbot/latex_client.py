import os
import requests
from pathlib import Path

LATEX_RENDERER_URL = os.getenv("LATEX_RENDERER_URL")

def render_latex(tex_content: str, output_path: Path):
    files = {'file': ('document.tex', tex_content.encode('utf-8'))}
    response = requests.post(LATEX_RENDERER_URL, files=files)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(response.content)