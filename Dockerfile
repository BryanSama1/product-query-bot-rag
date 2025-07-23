# Usar Python 3.11 como imagen base
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements first para optimizar cache
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Crear directorio para el índice FAISS si no existe
RUN mkdir -p faiss_index

# Variables de entorno para producción
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Indexar documentos al construir la imagen
RUN python index.py

# Exponer puerto (Cloud Run usa PORT env variable)
EXPOSE $PORT

# Comando para ejecutar la aplicación en Cloud Run
CMD uvicorn app:app --host 0.0.0.0 --port $PORT