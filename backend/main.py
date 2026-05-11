from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import Form
import subprocess
from pathlib import Path

app = FastAPI()

# Serve frontend folder as static
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

app.mount(
    "/generated",
    StaticFiles(directory="../template/generated"),
    name="generated",
)

app.mount(
    "/template",
    StaticFiles(directory="../template"),
    name="template",
)

@app.get("/health")
def check_health():
    return {"status": "ok"}

@app.get("/")
def home():
    return FileResponse("../frontend/index.html")

@app.post("/convert", response_class=HTMLResponse)
async def convert(markdown: str = Form(...), font_size: str = Form(...)):

    generated_dir = Path("../template/generated")

    generated_dir.mkdir(exist_ok=True)

    markdown_file = generated_dir / "resume.md"
    pdf_file = generated_dir / "resume.pdf"
    css_file = Path("../template/resume_style_default.css")
    css_content = css_file.read_text(encoding="utf-8")

    css_content = css_content.replace(
        "--txt-size: 8pt;",
        f"--txt-size: {font_size}pt;"
    )

    generated_css_file = generated_dir / "generated_style.css"
    generated_css_file.write_text(
        css_content,
        encoding="utf-8"
    )

    markdown_file.write_text(markdown, encoding="utf-8") # Save the .md file
    print("Markdown saved!!")
    print(font_size)
    subprocess.run(
        [
            "pandoc",
            str(markdown_file),
            "-o",
            str(pdf_file),
            "--pdf-engine=weasyprint",
            "-c",
            str(generated_css_file),
        ],
        check=True
    )

    print("PDF generated")

    return """
    <iframe
        id="pdf-preview"
        class="pdf-preview"
        src="/generated/resume.pdf">
    </iframe>
    """

import asyncio
from fastapi import Form
from fastapi.responses import HTMLResponse

# ... (other imports)

@app.post("/ai/format", response_class=HTMLResponse)
async def format_resume(markdown: str = Form(...)):
    # 1. Emulate the API delay
    await asyncio.sleep(2)

    # 2. Mock "Formatted" output
    # This simulates Gemini taking the input and wrapping it in your structure
    dummy_markdown = f"""# DUMMY FORMATTED RESUME

## CONTACT
[Name from input]
Email: dummy@example.com

## EXPERIENCE
- Successfully tested HTMX loading states
- Simulated a 2-second API latency with asyncio.sleep
- Verified that the .my-indicator pulse animation works

## ORIGINAL INPUT (for verification):
{markdown}
"""

    # 3. Return the textarea for HTMX to swap
    return f'<textarea id="resumeTextDisplay" name="markdown" rows="15" cols="80">{dummy_markdown}</textarea>'
