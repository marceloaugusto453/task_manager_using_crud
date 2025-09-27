# Imagem base
FROM python:3.12

# Definir diretório de trabalho no container
WORKDIR /app

# Copiar requirements.txt (que está dentro da pasta backend)
COPY ./backend/requirements.txt /app/requirements.txt

# Instalar dependências
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiar todo o código da pasta backend para dentro do container
COPY ./backend /app/backend

# Comando para rodar a aplicação
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
