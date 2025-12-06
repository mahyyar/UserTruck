FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-dev gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN mkdir -p /app/data

EXPOSE 8000

CMD ["python3", "main.py"]
