FROM python:3.11-slim

WORKDIR /app

COPY ./service2-preprocess/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./service2-preprocess/app.py .

EXPOSE 8062

CMD ["python", "app.py"]
