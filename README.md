# Procesador de Datos de Campañas

Este script procesa datos de campañas publicitarias desde archivos CSV.

## Requisitos previos

-Tener una cuenta publicitaria en Meta Ads de donde extraer tus datos de campaña.

## Configuración

1. Instalar las dependencias (linea a linea en la terminal):
```bash
python3 -m venv venv
source venv/bin/activate
pip install pandas openpyxl
python3 meta_ads_import.py

```

2. Descargar archivo csv de la campaña publicitaria.

## Uso

1. Coloca tu archivo CSV con el nombre 'datos_campanas.csv' o el nombre que desees (hay que modificar la funcion main en meta_ads_import.py) en el directorio campanas.

2. Ejecuta el script:
```bash
python meta_ads_import.py
```
El script generará un nuevo archivo CSV con los datos procesados.
