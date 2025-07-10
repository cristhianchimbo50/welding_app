import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import os
import uuid


def generar_grafico_precalentamiento(carpeta='static'):
    """Genera el gráfico de curvas de temperatura de precalentamiento."""
    entrada_calor = np.linspace(0, 60, 100)
    curvas = {
        'A (50°C)': 20 - 0.3 * entrada_calor,
        'B (100°C)': 17 - 0.28 * entrada_calor,
        'C (150°C)': 15 - 0.25 * entrada_calor,
        'D (200°C)': 12 - 0.21 * entrada_calor,
        'E (250°C)': 10 - 0.18 * entrada_calor
    }
    os.makedirs(carpeta, exist_ok=True)
    unique_id = uuid.uuid4().hex
    filename = f"grafico_precalentamiento_{unique_id}.png"
    filepath = os.path.join(carpeta, filename)
    plt.figure(figsize=(6,5))
    for label, y in curvas.items():
        plt.plot(entrada_calor, y, label=label)
    plt.xlabel('Entrada de Calor (kJ/cm)')
    plt.ylabel('Índice de Enfriamiento a 540°C')
    plt.title('Temperatura de Precalentamiento (°C)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()
    return filename

def generar_grafico_enfriamiento(carpeta='static'):
    """Genera la curva de enfriamiento temperatura vs tiempo."""
    t = np.linspace(0, 60, 100)
    T = 900 * np.exp(-0.08 * t) + 300 * np.exp(-((t-2)**2)/5)
    os.makedirs(carpeta, exist_ok=True)
    unique_id = uuid.uuid4().hex
    filename = f"grafico_enfriamiento_{unique_id}.png"
    filepath = os.path.join(carpeta, filename)
    plt.figure(figsize=(6,4))
    plt.plot(t, T, label="Enfriamiento")
    plt.axhline(723, color='r', linestyle='--', label='723°C')
    plt.text(1, 740, '723°C', color='r')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Temperatura (°C)')
    plt.title('Curva de Enfriamiento')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()
    return filename

def generar_grafico_soldabilidad(ce, c_percent, carpeta='static'):
    """Genera el diagrama de soldabilidad CE vs %C, ubicando el punto actual."""
    os.makedirs(carpeta, exist_ok=True)
    unique_id = uuid.uuid4().hex
    filename = f"grafico_soldabilidad_{unique_id}.png"
    filepath = os.path.join(carpeta, filename)
    plt.figure(figsize=(7,5))
    plt.axvline(0.50, color='k', linestyle='--')
    plt.axhline(0.20, color='k', linestyle='--')
    plt.axhline(0.30, color='k', linestyle='--')
    plt.text(0.25, 0.08, "Zona 1\nBuena soldabilidad", fontsize=10)
    plt.text(0.25, 0.22, "Zona 2", fontsize=10)
    plt.text(0.55, 0.35, "Zona 3\nDifícil soldabilidad", fontsize=10)
    plt.plot(ce, c_percent, 'ko', markersize=10)
    plt.xlabel('C.E. (Carbono Equivalente)')
    plt.ylabel('%C (Porcentaje de carbono)')
    plt.title('Diagrama de Soldabilidad')
    plt.xlim(0.2, 0.7)
    plt.ylim(0, 0.45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()
    return filename
