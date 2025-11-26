FROM python:3.11-slim

WORKDIR /app

COPY ./service2-loadbalancer/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./service2-loadbalancer/app.py .

EXPOSE 8062

CMD ["python", "app.py"]
