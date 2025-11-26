FROM python:3.11-slim

WORKDIR /app

COPY ./service3-analysis/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./service3-analysis/app.py .

EXPOSE 8063

CMD ["python", "app.py"]
