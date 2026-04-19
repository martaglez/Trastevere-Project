### PARA CONSTRUIR WEB EN RENDER ###
# Imagen base ligera de Python
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias para psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias Python primero (aprovecha caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

# Copiar el resto del proyecto
COPY . .

# Crear directorio de imágenes de storage
RUN mkdir -p storage/images

# Exponer el puerto que usará gunicorn
EXPOSE 10000

# Comando de arranque: gunicorn en lugar de flask run (más robusto para producción)
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--workers", "2", "backend.appy:app"]
