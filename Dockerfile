# Usa la última imagen base de Python 3.11 slim (puedes ajustar a la versión más reciente disponible)
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Actualiza los paquetes del sistema para mitigar vulnerabilidades
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends gcc build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copia los archivos de requerimientos
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
COPY . .

# Expone el puerto 5000 (usado por Flask/Gunicorn)
EXPOSE 5000

# Comando para ejecutar la app con Gunicorn en producción (ajusta 'app:app' si tu archivo o instancia Flask se llaman diferente)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
