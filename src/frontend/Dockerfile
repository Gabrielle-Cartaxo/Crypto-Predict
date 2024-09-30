# Dockerfile do frontend
FROM python:3.10

WORKDIR /app

# Copia o requirements.txt da raiz
COPY ../requirements.txt .

# Copia o restante do código do frontend
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
