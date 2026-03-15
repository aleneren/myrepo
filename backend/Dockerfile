FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y ffmpeg libsndfile1 && \
  pip install --no-cache-dir --upgrade pip && \
  pip install --no-cache-dir torch==2.2.2+cpu \
  --index-url https://download.pytorch.org/whl/cpu && \
  pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["python", "run.py"]