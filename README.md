# Welding App - Calculadora de Soldadura SMAW

Welding App es una aplicación web desarrollada en Flask para el cálculo de parámetros fundamentales de soldadura SMAW, generación de reportes en PDF y visualización de gráficos técnicos. Está orientada a fines educativos y de apoyo a estudiantes de ingeniería.

## Características

- Selección de materiales y electrodos desde una base de datos.
- Ingreso de parámetros de soldadura.
- Cálculo automático de:
  - Aporte de calor (Hnet)
  - Zona afectada por calor (ZAC)
  - Velocidad crítica de enfriamiento (VCT)
  - Velocidad de solidificación
  - Carbono equivalente (CE y CET)
  - Dureza estimada
  - Velocidad de enfriamiento T8/5
  - Energía total de fusión
  - Temperaturas de precalentamiento (AWS, Seferian, IIW, Yurioka)
- Gráficos:
  - Curvas de precalentamiento
  - Curva de enfriamiento
  - Diagrama de soldabilidad
- Generación de reportes en PDF.
- Despliegue compatible con VPS y acceso remoto mediante ngrok o dominio.

## Tecnologías utilizadas

- Backend: Python 3, Flask
- Frontend: HTML5, CSS3, Bootstrap
- Gráficos: Matplotlib
- Generación de PDF: pdfkit + wkhtmltopdf
- Otros: Jinja2, WeasyPrint, Virtualenv

## Instalación local

1. Clona el repositorio:
   ```bash
   git clone https://github.com/cristhianchimbo50/welding_app.git
   cd welding_app
