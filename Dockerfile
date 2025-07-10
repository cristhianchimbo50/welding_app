# Usa la imagen oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Actualiza, instala dependencias de sistema y wkhtmltopdf
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wkhtmltopdf \
        build-essential \
        gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copia e instala las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
COPY . .

# Expone el puerto para Flask/Gunicorn
EXPOSE 5000

# Arranca Gunicorn, ajusta si tu objeto Flask no es "app"
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
