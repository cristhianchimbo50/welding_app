from flask import Flask, render_template, request, make_response
from services.charts import (
    generar_grafico_precalentamiento,
    generar_grafico_enfriamiento,
    generar_grafico_soldabilidad
)
from services.materials import load_materials
from services.electrodes import load_electrodes
from services.calculations import (
    calcular_hnet,
    calcular_zac,
    calcular_vct,
    calcular_solidificacion,
    calcular_carbono_equivalente,
    calcular_carbono_equivalente_cet,
    calcular_dureza,
    calcular_precalentamiento_aws,
    calcular_precalentamiento_seferian,
    calcular_precalentamiento_iiw,
    calcular_precalentamiento_yurioka,
    calcular_enfriamiento_t85,
    calcular_energia_fusion,
    clasificar_chapa
)
import pdfkit
import os

app = Flask(__name__)

config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

@app.route('/')
def index():
    materials = load_materials()
    electrodes = load_electrodes()
    return render_template('index.html', materials=materials, electrodes=electrodes)

@app.route('/results', methods=['POST'])
def results():
    selected_material = request.form['material']
    selected_electrode = request.form['electrode']
    amperage = float(request.form['amperage'])
    voltage = float(request.form['voltage'])
    efficiency = float(request.form['efficiency'])
    speed = float(request.form['speed'])
    thickness = float(request.form['thickness'])

    materials = load_materials()
    electrodes = load_electrodes()

    material = next((m for m in materials if m["Name"] == selected_material), None)
    electrode = next((e for e in electrodes if e["Name"] == selected_electrode), None)

    # Cálculos
    hnet = calcular_hnet(voltage, amperage, efficiency, speed)
    zac = calcular_zac(hnet, material["Density"], material["SpecificHeat"], material["CriticalTemperature"])
    vct = calcular_vct(hnet, thickness)
    solidificacion = calcular_solidificacion(material["MeltingPoint"], material["CriticalTemperature"], hnet)
    ce = calcular_carbono_equivalente(material)
    cet = calcular_carbono_equivalente_cet(material)
    dureza = calcular_dureza(ce, vct)
    prec_aws = calcular_precalentamiento_aws(ce)
    prec_seferian = calcular_precalentamiento_seferian(ce, thickness)
    prec_iiw = calcular_precalentamiento_iiw(ce)
    prec_yurioka = calcular_precalentamiento_yurioka(ce, hnet)
    enfriamiento_t85 = calcular_enfriamiento_t85(thickness)
    energia_fusion = calcular_energia_fusion(material["Density"], material["FusionHeat"])
    tipo_chapa = clasificar_chapa(thickness)

    # Genera los gráficos requeridos y obtiene el nombre de archivo de cada uno
    img_precal = generar_grafico_precalentamiento()
    img_enfriamiento = generar_grafico_enfriamiento()
    img_soldabilidad = generar_grafico_soldabilidad(ce, material["CarbonContent"])

    return render_template(
        'results.html',
        material=material,
        electrode=electrode,
        amperage=amperage,
        voltage=voltage,
        efficiency=efficiency,
        speed=speed,
        thickness=thickness,
        hnet=hnet,
        zac=zac,
        vct=vct,
        solidificacion=solidificacion,
        ce=ce,
        cet=cet,
        dureza=dureza,
        prec_aws=prec_aws,
        prec_seferian=prec_seferian,
        prec_iiw=prec_iiw,
        prec_yurioka=prec_yurioka,
        enfriamiento_t85=enfriamiento_t85,
        energia_fusion=energia_fusion,
        tipo_chapa=tipo_chapa,
        img_precal=img_precal,
        img_enfriamiento=img_enfriamiento,
        img_soldabilidad=img_soldabilidad
    )

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    selected_material = request.form['material']
    selected_electrode = request.form['electrode']
    amperage = float(request.form['amperage'])
    voltage = float(request.form['voltage'])
    efficiency = float(request.form['efficiency'])
    speed = float(request.form['speed'])
    thickness = float(request.form['thickness'])
    img_zac = request.form['img_zac']
    img_precal = request.form['img_precal']
    img_enfriamiento = request.form['img_enfriamiento']
    img_soldabilidad = request.form['img_soldabilidad']

    materials = load_materials()
    electrodes = load_electrodes()

    material = next((m for m in materials if m["Name"] == selected_material), None)
    electrode = next((e for e in electrodes if e["Name"] == selected_electrode), None)

    # Cálculos (idénticos)
    hnet = calcular_hnet(voltage, amperage, efficiency, speed)
    zac = calcular_zac(hnet, material["Density"], material["SpecificHeat"], material["CriticalTemperature"])
    vct = calcular_vct(hnet, thickness)
    solidificacion = calcular_solidificacion(material["MeltingPoint"], material["CriticalTemperature"], hnet)
    ce = calcular_carbono_equivalente(material)
    cet = calcular_carbono_equivalente_cet(material)
    dureza = calcular_dureza(ce, vct)
    prec_aws = calcular_precalentamiento_aws(ce)
    prec_seferian = calcular_precalentamiento_seferian(ce, thickness)
    prec_iiw = calcular_precalentamiento_iiw(ce)
    prec_yurioka = calcular_precalentamiento_yurioka(ce, hnet)
    enfriamiento_t85 = calcular_enfriamiento_t85(thickness)
    energia_fusion = calcular_energia_fusion(material["Density"], material["FusionHeat"])
    tipo_chapa = clasificar_chapa(thickness)

    static_folder = os.path.join(app.root_path, 'static')

    # Construye las rutas absolutas (¡con los tres /!)
    def ruta_file_url(archivo):
        ruta = os.path.join(static_folder, archivo).replace("\\", "/")
        return 'file:///' + ruta

    img_absoluta_zac = ruta_file_url(img_zac)
    img_absoluta_precal = ruta_file_url(img_precal)
    img_absoluta_enfriamiento = ruta_file_url(img_enfriamiento)
    img_absoluta_soldabilidad = ruta_file_url(img_soldabilidad)

    print("Ruta ZAC:", img_absoluta_zac)
    print("¿Existe ZAC?:", os.path.isfile(img_absoluta_zac[8:]))
    print("Ruta PRECAL:", img_absoluta_precal)
    print("¿Existe PRECAL?:", os.path.isfile(img_absoluta_precal[8:]))
    print("Ruta ENFRIAMIENTO:", img_absoluta_enfriamiento)
    print("¿Existe ENFRIAMIENTO?:", os.path.isfile(img_absoluta_enfriamiento[8:]))
    print("Ruta SOLDABILIDAD:", img_absoluta_soldabilidad)
    print("¿Existe SOLDABILIDAD?:", os.path.isfile(img_absoluta_soldabilidad[8:]))

    html = render_template(
        'report.html',
        material=material,
        electrode=electrode,
        amperage=amperage,
        voltage=voltage,
        efficiency=efficiency,
        speed=speed,
        thickness=thickness,
        hnet=hnet,
        zac=zac,
        vct=vct,
        solidificacion=solidificacion,
        ce=ce,
        cet=cet,
        dureza=dureza,
        prec_aws=prec_aws,
        prec_seferian=prec_seferian,
        prec_iiw=prec_iiw,
        prec_yurioka=prec_yurioka,
        enfriamiento_t85=enfriamiento_t85,
        energia_fusion=energia_fusion,
        tipo_chapa=tipo_chapa,
        img_zac=img_zac,
        img_precal=img_precal,
        img_enfriamiento=img_enfriamiento,
        img_soldabilidad=img_soldabilidad,
        imagen_absoluta_zac=img_absoluta_zac,
        imagen_absoluta_precal=img_absoluta_precal,
        imagen_absoluta_enfriamiento=img_absoluta_enfriamiento,
        imagen_absoluta_soldabilidad=img_absoluta_soldabilidad
    )

    options = {
        'enable-local-file-access': None
    }
    pdf = pdfkit.from_string(html, False, configuration=config, options=options)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename="informe_soldadura.pdf"'
    return response

if __name__ == '__main__':
    app.run(debug=True)
