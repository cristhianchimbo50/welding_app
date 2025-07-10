def calcular_hnet(voltage, amperage, efficiency, speed):
    """Cálculo del aporte de calor neto Hnet."""
    if speed == 0:
        return 0
    return round((voltage * amperage * efficiency) / speed, 2)


def calcular_zac(hnet, density, specific_heat, critical_temp):
    """Cálculo simplificado de la zona afectada por el calor (ZAC)."""
    temp_ambient = 25
    delta_temp = critical_temp - temp_ambient
    if density == 0 or specific_heat == 0 or delta_temp <= 0:
        return 0
    return round(hnet / (density * specific_heat * delta_temp), 4)


def calcular_vct(hnet, thickness):
    """Velocidad crítica de enfriamiento (simplificada)."""
    coeficiente = 0.8
    if thickness == 0:
        return 0
    return round(hnet / (thickness * coeficiente), 2)


def calcular_solidificacion(melting_point, critical_temp, hnet):
    """Velocidad de solidificación simplificada."""
    delta_temp = melting_point - critical_temp
    if hnet == 0:
        return 0
    return round(delta_temp / hnet, 4)


def calcular_carbono_equivalente(material):
    """Carbono equivalente clásico (AWS)."""
    C = material.get("CarbonContent", 0)
    Mn = material.get("ManganeseContent", 0)
    Cr = material.get("ChromiumContent", 0)
    Mo = material.get("MolybdenumContent", 0)
    V = material.get("VanadiumContent", 0)
    Ni = material.get("NickelContent", 0)
    Cu = material.get("CopperContent", 0)

    CE = C + (Mn / 6) + ((Cr + Mo + V) / 5) + ((Ni + Cu) / 15)
    return round(CE, 3)


def calcular_carbono_equivalente_cet(material):
    """Carbono equivalente CET."""
    C = material.get("CarbonContent", 0)
    Mn = material.get("ManganeseContent", 0)
    Cr = material.get("ChromiumContent", 0)
    Mo = material.get("MolybdenumContent", 0)
    Ni = material.get("NickelContent", 0)
    Cu = material.get("CopperContent", 0)

    CET = C + ((Mn + Mo) / 10) + ((Cr + Cu) / 20) + (Ni / 40)
    return round(CET, 3)


def calcular_dureza(ce, vct):
    """Predicción básica de dureza bajo el cordón."""
    dureza = (ce * 300) + (vct * 2)
    return round(dureza, 2)


def calcular_precalentamiento_aws(carbon_equivalent):
    """Temperatura de precalentamiento según AWS."""
    return round(carbon_equivalent * 75, 2)


def calcular_precalentamiento_seferian(carbon_equivalent, thickness):
    """Temperatura de precalentamiento según Seferian."""
    return round((carbon_equivalent * 100) + (thickness * 2), 2)


def calcular_precalentamiento_iiw(carbon_equivalent):
    """Temperatura de precalentamiento según IIW."""
    return round(50 + (carbon_equivalent * 150), 2)


def calcular_precalentamiento_yurioka(carbon_equivalent, hnet):
    """Temperatura de precalentamiento según Yurioka."""
    return round((carbon_equivalent * hnet) / 2, 2)


def calcular_enfriamiento_t85(thickness):
    """Cálculo de velocidad de enfriamiento T8/5 basado en el espesor."""
    if thickness <= 5:
        return round(35, 2)  # chapa fina
    elif 5 < thickness <= 20:
        return round(25, 2)  # chapa media
    else:
        return round(15, 2)  # chapa gruesa


def calcular_energia_fusion(density, fusion_heat):
    """Cálculo de la energía total de fusión por cm³."""
    if density == 0 or fusion_heat == 0:
        return 0
    return round(density * fusion_heat, 2)  # J/cm³


def clasificar_chapa(thickness):
    """Clasificación visual de la chapa."""
    if thickness <= 5:
        return "Chapa fina"
    elif 5 < thickness <= 20:
        return "Chapa media"
    else:
        return "Chapa gruesa"
