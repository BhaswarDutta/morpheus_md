from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Form

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
    print(markdown)

    return {"status": "received"}
