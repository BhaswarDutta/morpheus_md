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

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
TEMPLATE_DIR = BASE_DIR / "template"
GENERATED_DIR = TEMPLATE_DIR / "generated"


app = FastAPI()

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key, http_options={'api_version': 'v1beta'})


# Serve frontend folder as static
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

app.mount(
    "/generated",
    StaticFiles(directory=GENERATED_DIR),
    name="generated",
)

app.mount(
    "/template",
    StaticFiles(directory=TEMPLATE_DIR),
    name="template",
)

@app.get("/health")
def check_health():
    return {"status": "ok"}

@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.post("/convert", response_class=HTMLResponse)
async def convert(markdown: str = Form(...), font_size: str = Form(...)):

    generated_dir = GENERATED_DIR

    generated_dir.mkdir(parents=True, exist_ok=True)

    markdown_file = generated_dir / "resume.md"
    pdf_file = generated_dir / "resume.pdf"
    css_file = TEMPLATE_DIR / "resume_style_default.css"
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


    boilerplate_path = TEMPLATE_DIR / "boilerplate_resume.md"
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





@app.post("/ai/tailor_to_jd", response_class=HTMLResponse)
async def tailor_to_jd(markdown: str = Form(...), markdown_jd: str = Form(...)):
    if not api_key:
        error_message = """
            ❌ ERROR: GOOGLE_API_KEY not found in .env
            Unable to access Gemini API
        """
        return f'<textarea id="resumeTextDisplay" name="markdown" rows="15" cols="80">{error_message}</textarea>'

    prompt = f"""
    Act as a Senior Staff Engineer and ATS Optimizer.
    I am applying for a job. I will provide my BASE RESUME and the JOB DESCRIPTION.

    ### CONTEXT:
    HR often includes an absurd amount of "fluff" in JDs. Your goal is to identify the ACTUAL technical requirements and core competencies, then inject them aggressively into my resume.

    ### INPUT DATA:
    1. **JOB DESCRIPTION:**
    {markdown_jd}

    2. **BASE RESUME (MARKDOWN):**
    {markdown}

    ### RULES:
    1. **STRICT FORMATTING:** Maintain the exact Markdown structure of the BASE RESUME. Do not change header levels, font styles, or the general layout.
    2. **KEYWORD INJECTION:** Aggressively weave high-value keywords from the JD (e.g., specific tech stacks, "Operational Excellence", "System Design", "Agile") into my existing project descriptions and skills.
    3. **NO HALLUCINATIONS:** Keep my project facts, dates, and companies exactly as they are. Only change the *phrasing* to align with the JD's vocabulary.
    4. **ATS SCORING:** Use terminology that an ATS or a non-technical recruiter would look for, but keep it technically accurate for the hiring manager.
    5. **CLEAN OUTPUT:** Return ONLY the updated markdown text. No conversational filler or code fences.

    ### UPDATED RESUME:
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
