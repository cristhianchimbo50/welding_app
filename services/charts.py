import matplotlib.pyplot as plt
import os
import uuid

def generar_grafico_zac(zac, carpeta='static'):
    """
    Genera un gráfico PNG que muestra la zona afectada por el calor (ZAC).
    Parámetros:
      - zac: valor numérico del ZAC.
      - carpeta: carpeta donde se guarda la imagen (por defecto 'static').
    Devuelve:
      - El nombre único del archivo generado (str), que puede usarse en url_for('static', filename=nombre).
    """
    # Asegura que la carpeta exista
    os.makedirs(carpeta, exist_ok=True)

    # Genera un nombre único para el archivo (para evitar sobrescribir imágenes previas)
    unique_id = uuid.uuid4().hex
    filename = f"grafico_zac_{unique_id}.png"
    filepath = os.path.join(carpeta, filename)

    # Configuración del gráfico
    fig, ax = plt.subplots(figsize=(4, 4))
    base_radio = 2
    zac_radio = base_radio + zac * 10  # Puedes ajustar la escala visual si lo deseas

    # Metal base (círculo gris)
    circle_base = plt.Circle((0, 0), base_radio, color='lightgray', alpha=0.5, label='Metal base')
    ax.add_artist(circle_base)
    # Zona afectada (ZAC)
    circle_zac = plt.Circle((0, 0), zac_radio, color='orange', alpha=0.4, label='Zona afectada (ZAC)')
    ax.add_artist(circle_zac)

    ax.set_xlim(-zac_radio - 0.5, zac_radio + 0.5)
    ax.set_ylim(-zac_radio - 0.5, zac_radio + 0.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.legend(loc='upper right')
    plt.title('Zona afectada por calor (ZAC)')

    # Guarda el gráfico
    plt.savefig(filepath, bbox_inches='tight', transparent=True)
    plt.close()

    return filename  # SOLO el nombre, úsalo así: url_for('static', filename=filename)
