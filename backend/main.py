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
    generated_dir = Path("../template/generated")
    generated_dir.mkdir(exist_ok=True)
    markdown_file = generated_dir / "resume.md"
    markdown_file.write_text(markdown, encoding="utf-8") # Save the .md file
    print("Markdown saved!!")

    return
