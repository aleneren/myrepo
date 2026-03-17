FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y ffmpeg libsndfile1
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir torch==2.4.0+cpu \
  --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "run.py"]