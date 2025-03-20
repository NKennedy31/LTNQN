import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi
import pandas as pd

# Cargar variables de entorno
load_dotenv()

def inicializar_api():
    """Inicializa la API de Facebook con las credenciales."""
    access_token = os.getenv('META_ACCESS_TOKEN')
    ad_account_id = os.getenv('META_AD_ACCOUNT_ID')
    
    if not access_token or not ad_account_id:
        raise ValueError("Por favor, configura las variables de entorno META_ACCESS_TOKEN y META_AD_ACCOUNT_ID")
    
    FacebookAdsApi.init(access_token=access_token)
    return AdAccount(ad_account_id)

def obtener_datos_campanas(ad_account, dias_atras=30):
    """Obtiene datos de las campañas de los últimos N días."""
    # Calcular fechas
    fecha_fin = datetime.now()
    fecha_inicio = fecha_fin - timedelta(days=dias_atras)
    
    # Campos que queremos obtener
    campos = [
        'name',
        'objective',
        'status',
        'spend',
        'impressions',
        'clicks',
        'reach',
        'cpc',
        'ctr',
        'frequency',
        'start_time',
        'stop_time'
    ]
    
    # Obtener datos de las campañas
    campanas = ad_account.get_campaigns(
        fields=campos,
        params={
            'time_range': {
                'since': fecha_inicio.strftime('%Y-%m-%d'),
                'until': fecha_fin.strftime('%Y-%m-%d')
            }
        }
    )
    
    return campanas

def procesar_datos(campanas):
    """Procesa los datos de las campañas y los convierte en un DataFrame."""
    datos = []
    for campana in campanas:
        datos.append({
            'nombre': campana['name'],
            'objetivo': campana['objective'],
            'estado': campana['status'],
            'gasto': float(campana.get('spend', 0)),
            'impresiones': int(campana.get('impressions', 0)),
            'clicks': int(campana.get('clicks', 0)),
            'alcance': int(campana.get('reach', 0)),
            'cpc': float(campana.get('cpc', 0)),
            'ctr': float(campana.get('ctr', 0)),
            'frecuencia': float(campana.get('frequency', 0)),
            'fecha_inicio': campana.get('start_time', ''),
            'fecha_fin': campana.get('stop_time', '')
        })
    
    return pd.DataFrame(datos)

def main():
    try:
        # Inicializar API
        print("Inicializando API de Meta Ads...")
        ad_account = inicializar_api()
        
        # Obtener datos de campañas
        print("Obteniendo datos de campañas...")
        campanas = obtener_datos_campanas(ad_account)
        
        # Procesar datos
        print("Procesando datos...")
        df = procesar_datos(campanas)
        
        # Guardar resultados
        fecha_actual = datetime.now().strftime('%Y%m%d')
        nombre_archivo = f'meta_ads_data_{fecha_actual}.csv'
        df.to_csv(nombre_archivo, index=False, encoding='utf-8-sig')
        
        print(f"Datos guardados exitosamente en {nombre_archivo}")
        print(f"Total de campañas procesadas: {len(df)}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 