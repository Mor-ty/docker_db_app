FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app/ ./app
EXPOSE 8084
CMD ["python", "app/app.py"]

