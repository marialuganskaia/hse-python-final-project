FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

WORKDIR /app

# зависимости
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# код
COPY alembic.ini /app/alembic.ini
COPY alembic /app/alembic
COPY src /app/src
COPY docs /app/docs

# по умолчанию запускаем бота (можно переопределить в compose)
CMD ["python", "-m", "hackathon_assistant.infra.main"]
