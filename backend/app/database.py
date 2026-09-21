import mysql.connector
from .config import db_config


def obtener_conexion(usar_bd=True):
    return mysql.connector.connect(**db_config(usar_bd))