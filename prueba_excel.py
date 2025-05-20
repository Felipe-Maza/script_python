import pandas as pd
import requests
from io import BytesIO

EXCEL_URL = "https://everisgroup-my.sharepoint.com/:x:/g/personal/fmazaper_emeal_nttdata_com/EUm7atJPTCVGo57epRlrodwB0RFenJagVVH-HqNMKVk96A?e=gO0AO8&download=1"

def get_excel_from_sharepoint():
    response = requests.get(EXCEL_URL)
    if response.status_code != 200:
        raise Exception(f"No se pudo descargar el archivo: {response.status_code}")
    return pd.read_excel(BytesIO(response.content),engine="openpyxl")

df = get_excel_from_sharepoint()
print(df)