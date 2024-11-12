FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 8000

# Run FastAPI
CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]