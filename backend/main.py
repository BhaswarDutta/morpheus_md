from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Form
import subprocess
from pathlib import Path

app = FastAPI()

# Serve frontend folder as static
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/health")
def check_health():
    return {"status": "ok"}

@app.get("/")
def home():
    return FileResponse("../frontend/index.html")

@app.post("/convert")
async def convert(markdown: str = Form(...)):
    workspace = Path("../workspace")

    markdown_file = workspace / "resume.md"
    pdf_file = workspace / "resume.pdf"
    print(markdown)

    markdown_file.write_text(markdown, encoding="utf-8") # Save md file

    return {"status": "received"}
