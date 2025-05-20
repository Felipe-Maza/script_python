import psycopg2 
from dotenv import load_dotenv 
import os 
import pandas as pd 

load_dotenv()

USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

try:
    connection = psycopg2.connect(
        user = USER,
        password = PASSWORD,
        host = HOST,
        port = PORT,
        dbname = DB_NAME
    )
    print("Conexion exitosa")
    query = "SELECT * FROM datos"
    df = pd.read_sql_query(query,connection)
    print(df)
except Exception as e:
    print("Ocurrio un error inesperado: ",e)