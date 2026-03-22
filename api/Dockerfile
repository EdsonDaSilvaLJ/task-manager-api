FROM python:3.12-slim   
# imagem base enxuta

# evita arquivos .pyc e deixa logs imediatos no terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# instala dependências primeiro (camada cacheada pelo Docker)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# copia o restante do código
COPY . .

# coleta arquivos estáticos para o Nginx servir
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# gunicorn como servidor de produção
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]