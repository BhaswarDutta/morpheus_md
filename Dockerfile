FROM python:3.14

WORKDIR /app

RUN apt-get update && apt-get install -y pandoc weasyprint

RUN pip install uv

COPY backend/pyproject.toml .
COPY backend/uv.lock .

RUN uv sync

COPY . .

CMD ["uv", "run", "fastapi", "run", "backend/main.py", "--host", "0.0.0.0", "--port", "8000"]
