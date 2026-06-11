import math

def calcular_distancia(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula la distancia en metros entre dos puntos GPS usando la fórmula de Haversine.
    lat1, lon1: Coordenadas del pasante (enviadas desde Vue)
    lat2, lon2: Coordenadas de la Facultad (guardadas en PostgreSQL)
    """
    R = 6371000  

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2.0) ** 2
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distancia_metros = R * c
    return distancia_metros

def validar_ubicacion(lat_pasante: float, lon_pasante: float, lat_facultad: float, lon_facultad: float, radio_permitido: int = 50) -> bool:
    """
    Retorna True si el pasante está dentro del radio permitido (ej. 50 metros).
    """
    distancia = calcular_distancia(lat_pasante, lon_pasante, lat_facultad, lon_facultad)
    return distancia <= radio_permitido