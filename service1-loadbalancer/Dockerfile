FROM python:3.11-slim

WORKDIR /app

COPY ./service1-loadbalancer/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./service1-loadbalancer/app.py .

EXPOSE 8061

CMD ["python", "app.py"]
