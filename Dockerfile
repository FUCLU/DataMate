FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir pandas==2.2.2 openpyxl==3.1.5
COPY src/ /app/
ENV DATA_DIR=/data OUT_PATH=/result/submission.jsonl
CMD ["python", "/app/run.py"]