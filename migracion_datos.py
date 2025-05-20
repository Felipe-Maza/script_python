import pandas as pd
import requests
import psycopg2
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()

EXCEL_URL = os.getenv("SHAREPOINT_EXCEL_URL")

def get_excel_from_sharepoint():
    response = requests.get(EXCEL_URL)
    if response.status_code != 200:
        raise Exception(f"No se pudo descargar el archivo: {response.status_code}")
    return pd.read_excel(BytesIO(response.content),engine="openpyxl")

def insert_data_to_supabase(df):
    conn = psycopg2.connect(
        dbname = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        host = os.getenv("DB_HOST"),
        port = os.getenv("DB_PORT")
    )
    cursor = conn.cursor()
    table = os.getenv("DB_TABLE")

    for _, row in df.iterrows():
        placeholders = ', '.join(['%s']*len(row))
        columns = ', '.join(row.index)
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) ON CONFLICT DO NOTHING;"
        cursor.execute(sql,tuple(row))
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    df = get_excel_from_sharepoint()
    insert_data_to_supabase(df)
    print("Datos sincronizados con supabase")