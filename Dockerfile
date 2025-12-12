FROM python:3.12-slim

WORKDIR /app

# устанавливаем uv
RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
RUN uv sync --dev

COPY . .

CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
