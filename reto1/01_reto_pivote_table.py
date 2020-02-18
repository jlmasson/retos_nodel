from __future__ import print_function
import pickle
import funciones as fn
import numpy as np
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# EL ID del link del Spreadsheet que se envió.
SAMPLE_SPREADSHEET_ID = '18SIxsNHlXLXLPOrmYguEBa0Shz_7ufobEgID1LXrCXI'
# SAMPLE_SPREADSHEET_ID = '1DRD97TAw2WIuTCG0Nh6BW-aVvDKAgY1wvJb38V-3vU8'
SAMPLE_RANGE_NAME = ''

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()

    resultado = sheet.get(spreadsheetId=SAMPLE_SPREADSHEET_ID).execute()

    hojas_calculo = resultado.get('sheets', [])

    if not hojas_calculo:
        print('No data found.')
    else:
        info_hoja_reto = hojas_calculo[0]
        source_sheet = info_hoja_reto.get('properties')
        source_sheet_id = source_sheet.get('sheetId')
        source_sheet_title = source_sheet.get('title')

        # Debo crear la hoja de cálculo de Pivote
        # if len(hojas_calculo) == 1:
        body = {
            'requests': [{
                'addSheet': {}
            }]
        }
        batch_update_response = sheet.batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=body).execute()
        target_sheet_id = batch_update_response.get('replies')[0] \
        .get('addSheet').get('properties').get('sheetId')
        # else:
        #     info_hoja_tabla = hojas_calculo[1]
        #     target_sheet_id = info_hoja_tabla.get('properties').get('sheetId')
        SAMPLE_RANGE_NAME = "{}!A:D".format(source_sheet_title)

        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        encabezados = dict()
        filas = set()
        columnas = dict()

        if not values:
            print('No data found.')
        else:
                # No contar el encabezado

                columnas_clave_comp = ['Author', 'Sentiment']

                cantidad_filas = len(values) - 1
                for i, registro in enumerate(values):
                    if i == 0:
                        for ind, encabezado in enumerate(registro):
                            encabezados[encabezado] = ind
                            if encabezado == 'Country' or encabezado == 'Theme':
                                existe = columnas.get(encabezado, None)
                                if not(existe):
                                    columnas[encabezado] = set()
                    else:
                        clave_compuesta = fn.obtenerClaveCompuesta(registro, encabezados, *(columnas_clave_comp))
                        indice_country = encabezados.get('Country', -1)
                        indice_theme = encabezados.get('Theme', -1)
                        if (indice_country != -1 and indice_theme != -1):
                            columnas['Country'].add(registro[indice_country])
                            columnas['Theme'].add(registro[indice_theme])
                            filas.add(clave_compuesta)

                # Una vez que se tienen conjuntos se procede a trabajar con el procesamiento de la data
                filas = list(filas)
                n = len(filas)
                m = 0
                for region, valores in columnas.items():
                    columnas[region] = {
                        'startIndex': m,
                        'length': len(valores),
                        'data': list(valores)
                    }
                    m += len(valores)
                
                # Procedo a armar una matriz de NumPY para colocar el verdadero y falso, obviamente con condiciones
                matriz = np.zeros((n, m), dtype=bool)
                for i, registro in enumerate(values[1: ]):
                    clave_compuesta = fn.obtenerClaveCompuesta(registro, encabezados, 'Author', 'Sentiment')
                    indice_country = encabezados.get('Country', -1)
                    indice_theme = encabezados.get('Theme', -1)

                    valor_country = registro[indice_country]
                    valor_theme = registro[indice_theme]

                    indice_col_country = fn.obtenerIndiceColumna(columnas, 'Country', valor_country)
                    indice_col_theme = fn.obtenerIndiceColumna(columnas, 'Theme', valor_theme)
        
                    ind_fila = filas.index(clave_compuesta)
                    matriz[ind_fila, indice_col_country] = True
                    matriz[ind_fila, indice_col_theme] = True
                
                # Se ordenan las regiones para proceder a armar los encabezados correspondientes
                # de acuerdo al inicio de la región, así se tiene el problema resuelto
                regiones_ordenadas = sorted(columnas.items(), key = lambda x: x[1]['startIndex'])
                celdas_hoja = []

                celdas_encabezado = []
                celdas_subtitulo = []

                for elemento in columnas_clave_comp:

                    celda_enc = {
                        'userEnteredValue': {
                            'stringValue': ''
                        }
                    }
                    celdas_encabezado.append(celda_enc)

                    celda = {
                        'userEnteredValue': {
                            'stringValue': str(elemento)
                        }
                    }
                    celdas_subtitulo.append(celda)

                merge_cells_request = []

                cantidad_columnas_desplazar = len(columnas_clave_comp)

                for region, infoRegion in regiones_ordenadas:
                    elem_merge = {
                        "mergeCells": {
                            "range": {
                                "sheetId": target_sheet_id,
                                "startRowIndex": 0,
                                "endRowIndex": 1,
                                "startColumnIndex": cantidad_columnas_desplazar + infoRegion['startIndex'],
                                "endColumnIndex": cantidad_columnas_desplazar + infoRegion['startIndex'] + infoRegion['length']
                            },
                            "mergeType": "MERGE_ROWS"
                        }
                    }

                    merge_cells_request.append(elem_merge)

                    celda_enc = {
                        'userEnteredValue': {
                            'stringValue': str(region)
                        },
                        "userEnteredFormat": {
                            "horizontalAlignment" : "CENTER",
                        }
                    }
                    celdas_encabezado.append(celda_enc)

                    #Añadir tantas celdas sean necesarias para el correcto merging
                    for indice in range(infoRegion['length'] - 1):
                        celda_enc = {
                            'userEnteredValue': {
                                'stringValue': ''
                            },
                            "userEnteredFormat": {
                                "horizontalAlignment" : "CENTER",
                            }
                        }
                        celdas_encabezado.append(celda_enc)

                    for elemento in infoRegion['data']:
                        celda = {
                            'userEnteredValue': {
                                'stringValue': str(elemento)
                            }
                        }
                        celdas_subtitulo.append(celda)

                print(celdas_encabezado)
                print(celdas_subtitulo)

                valores_encabezado = {
                    'values': celdas_encabezado
                }

                valores_subtitulo = {
                    'values': celdas_subtitulo
                }

                celdas_hoja.append(valores_encabezado)
                celdas_hoja.append(valores_subtitulo)
                
                # A partir de aquí, se procede a armar la tabla dinámica con el formato deseado
                for i in range(matriz.shape[0]):
                    celdas_fila = []

                    for elemento in filas[i]:
                        celda = {
                            'userEnteredValue': {
                                'stringValue': str(elemento)
                            }
                        }
                        celdas_fila.append(celda)
                    for j in range(matriz.shape[1]):
                        celda = {
                            'userEnteredValue': {
                                'stringValue': str(matriz[i, j]).upper(),
                            },
                            "userEnteredFormat": {
                                "horizontalAlignment" : "CENTER",
                            }
                        },
                        
                        celdas_fila.append(celda)

                    valores = {
                        'values': celdas_fila,
                    }
                    celdas_hoja.append(valores)

                print(len(filas))
                print(len(celdas_hoja))


                # Procedo a guardar en la hoja de la nube
                requests = []
                requests.append({
                    'updateSheetProperties': {
                        'properties': {
                            'sheetId': target_sheet_id,
                            'gridProperties': {
                                'rowCount': n + 10,
                                'columnCount': m + 10
                            }
                        },
                        'fields': 'gridProperties(rowCount,columnCount)'
                    }
                })

                requests.append({
                    'updateCells': {
                        'start': {
                            'sheetId': target_sheet_id,
                            'rowIndex': 0,
                            'columnIndex': 0
                        },
                        'rows': celdas_hoja,
                        'fields': '*'
                    }
                })

                requests.extend(merge_cells_request)

                body = {
                    'requests': requests    
                }
                
                batch_update_response = sheet.batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=body).execute()

                # Actualización para merging
                # body = {
                #     'requests': merge_cells_request
                # }
                
                # print(merge_cells_request)

                # batch_update_response = sheet.batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=body).execute()

                print(batch_update_response)

if __name__ == '__main__':
    main()