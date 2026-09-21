import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def obtener_conexion(usar_bd=True):
    config = {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
    }

    if usar_bd:
        config["database"] = os.getenv("DB_NAME", "sabor360")

    return mysql.connector.connect(**config)
