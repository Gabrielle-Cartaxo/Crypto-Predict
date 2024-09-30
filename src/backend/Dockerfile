# Escolha uma imagem base que tenha Python
FROM python:3.10

# Defina o diretório de trabalho
WORKDIR /app

# Copie o arquivo de requisitos para o contêiner
COPY requirements.txt .

# Crie e ative um ambiente virtual
RUN python -m venv venv
RUN . venv/bin/activate && pip install -r requirements.txt


# Copie o restante do código para o contêiner
COPY . .

# Exponha a porta que o aplicativo utilizará
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["venv/bin/python", "app.py"]
