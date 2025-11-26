FROM python:3.11-slim

WORKDIR /app

COPY ./service4-loadbalancer/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./service4-loadbalancer/app.py .

EXPOSE 8064

CMD ["python", "app.py"]
