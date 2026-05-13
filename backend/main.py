from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import Form
import subprocess
from pathlib import Path
import os
from dotenv import load_dotenv
from google import genai
import asyncio

app = FastAPI()

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key, http_options={'api_version': 'v1beta'})


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



@app.post("/ai/format", response_class=HTMLResponse)
async def format_resume(markdown: str = Form(...)):


    boilerplate_path = Path("../template/boilerplate_resume.md")
    boilerplate = boilerplate_path.read_text(encoding="utf-8")

    if not api_key:
        error_message = """
            ❌ ERROR: GOOGLE_API_KEY not found in .env
            Unable to access Gemini API
        """
        return f'<textarea id="resumeTextDisplay" name="markdown" rows="15" cols="80">{error_message}</textarea>'

    prompt = f"""
    Act as a Professional Resume Writer. Your goal is to convert messy, unstructured RAW text (like LinkedIn profiles) into a clean, high-impact Markdown resume.

    ### STRICT RULES:
        1. **Dynamic Content:** Use the BOILERPLATE as a structural guide for the layout, but DO NOT include sections (like GitHub, Twitter, or specific Tech Stacks) if they are missing from the RAW text.
        2. **Executive Summary:** Extract a concise 2-3 sentence summary from the "About" section and place it at the top.
        3. **Action-Oriented Bullets:** Refine work experience into bullet points starting with strong action verbs (e.g., "Engineered," "Spearheaded," "Analyzed").
        4. **Smart Filtering:** Ignore "noise" like "436 connections" or "Contact info" labels.
        5. **Strict Cleanliness:** Return ONLY the markdown. No backticks (```), no introductory text.

    ### BOILERPLATE TEMPLATE:
    {boilerplate}

    ### RAW TEXT TO PROCESS:
    {markdown}

    ### FINAL OUTPUT:
    """
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        if response.text:
            return f'<textarea id="resumeTextDisplay" name="markdown" rows="15" cols="80">{response.text}</textarea>'
        else:
            error_message = """
                ❌ ERROR: No message received from Gemini API
            """
            return f'<textarea id="resumeTextDisplay" name="markdown" rows="15" cols="80">{error_message}</textarea>'

    except Exception as e:
        error_message = f"""
            ❌ ERROR:{e}
        """

        return f'<textarea id="resumeTextDisplay" name="markdown" rows="15" cols="80">{error_message}</textarea>'





@app.post("/ai/optimize_test", response_class=HTMLResponse)
async def optimize_test(markdown: str = Form(...), markdown_jd: str = Form(...)):
    # 1. Emulate AI thinking time
    await asyncio.sleep(2)

    # 2. Build a confirmation message showing both inputs were received
    dummy_output = f"""# AI OPTIMIZATION TEST SUCCESSFUL

## RECEIVED JOB DESCRIPTION:
{markdown_jd}

## RECEIVED ORIGINAL RESUME:
{markdown[:100]}... (truncated for brevity)

## SYSTEM CHECK:
- Remote Indicator: Targeted #mainTailorBtn
- Multi-Input: Captured both #resumeTextDisplay and #jobDescriptionTextDisplay
- Transition: Modal closed, user returned to main dashboard.
"""

    # 3. Swap the main editor with this confirmation
    return f'<textarea id="resumeTextDisplay" name="markdown" rows="15" cols="80">{dummy_output}</textarea>'



# @app.post("/ai/format", response_class=HTMLResponse)
# async def format_resume(markdown: str = Form(...)):
#     # 1. Emulate the API delay
#     await asyncio.sleep(2)

#     # 2. Mock "Formatted" output
#     # This simulates Gemini taking the input and wrapping it in your structure
#     dummy_markdown = f"""# DUMMY FORMATTED RESUME

# ## CONTACT
# [Name from input]
# Email: dummy@example.com

# ## EXPERIENCE
# - Successfully tested HTMX loading states
# - Simulated a 2-second API latency with asyncio.sleep
# - Verified that the .my-indicator pulse animation works

# ## ORIGINAL INPUT (for verification):
# {markdown}
# """

#     # 3. Return the textarea for HTMX to swap
#     return f'<textarea id="resumeTextDisplay" name="markdown" rows="15" cols="80">{dummy_markdown}</textarea>'
