FROM python:3.9-slim

WORKDIR /app

COPY Requirements.txt .
RUN pip install --no-cache-dir -r Requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
