FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir fastapi uvicorn pyfiglet

COPY entretien-technique.py /app/code.py

EXPOSE 8000

CMD ["python", "code.py"]

