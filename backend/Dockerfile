FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY backend /app/backend
COPY ml /app/ml
COPY data/sample /app/data/sample

WORKDIR /app
EXPOSE 8000
CMD ["sh", "-c", "python backend/manage.py migrate --noinput && python backend/manage.py runserver 0.0.0.0:8000"]

