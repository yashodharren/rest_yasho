FROM python:3.11-slim

WORKDIR /app

COPY ./service1-input/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./service1-input/app.py .

EXPOSE 8061

CMD ["python", "app.py"]
