FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY scripts ./scripts
COPY templates ./templates

RUN mkdir -p /app/logs

EXPOSE 5000

CMD ["python", "scripts/web_app.py"]
