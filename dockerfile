FROM python:3.11-slim

WORKDIR /app

# ---- Install system dependencies for WeasyPrint ----
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    libcairo2 \
    libjpeg62-turbo \
    libopenjp2-7 \
    libgobject-2.0-0 \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# ---- Python dependencies ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- App code ----
COPY ./app /app/app

# ---- Alembic migrations ----
COPY ./alembic.ini /app/alembic.ini
COPY ./alembic /app/alembic

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
