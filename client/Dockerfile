FROM python:3.11-slim

WORKDIR /app

COPY ./client/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./client/app.py /app/app.py
COPY ./datasets /app/datasets/
COPY ./client/benchmark.py .
COPY ./client/parallel_client.py .

CMD ["python", "app.py"]
