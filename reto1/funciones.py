import numpy as np

# Para el caso de este reto
# def obtenerDatos(registros):
#     filas = []
#     columnas = []
#     for registro in registros:

def obtenerClaveCompuesta(registro, encabezados, *claves):
    compuesta = []
    for clave in claves:
        indice = encabezados.get(clave, -1)
        if (indice != -1):
            compuesta.append(registro[indice])
    return tuple(compuesta)

def obtenerIndiceColumna(regiones, region, valor):
    indice = -1
    infoRegion = regiones.get(region, None)
    if infoRegion is not None:
        inicio = infoRegion.get('startIndex', -1)
        data = infoRegion.get('data', [])
        if data and inicio != -1:
            if valor in data:
                indice = data.index(valor)
                indice += inicio
    return indice
