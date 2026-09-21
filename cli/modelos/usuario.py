import hashlib
from conexion import obtener_conexion


class Usuario:
    """Representa un usuario/cliente de Sabor 360."""

    def __init__(self, nombre, correo, tipo_usuario="CLIENTE", id_usuario=None):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.correo = correo
        self.tipo_usuario = tipo_usuario

    @staticmethod
    def _hash_contrasena(contrasena):
        return hashlib.sha256(contrasena.encode("utf-8")).hexdigest()

    @classmethod
    def crear(cls, nombre, correo, contrasena, tipo_usuario="CLIENTE"):
        tipo_usuario = tipo_usuario.upper()
        if tipo_usuario not in ("CLIENTE", "ADMINISTRADOR"):
            raise ValueError("El tipo de usuario debe ser CLIENTE o ADMINISTRADOR.")

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO Usuario (nombre, correo, contrasena_hash, tipo_usuario)
                VALUES (%s, %s, %s, %s)
                """,
                (nombre.strip(), correo.strip().lower(), cls._hash_contrasena(contrasena), tipo_usuario),
            )
            conexion.commit()
            return cls(nombre, correo, tipo_usuario, cursor.lastrowid)
        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def listar():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT id_usuario, nombre, correo, tipo_usuario, fecha_registro
                FROM Usuario
                ORDER BY id_usuario
                """
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def buscar_por_id(id_usuario):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT id_usuario, nombre, correo, tipo_usuario, fecha_registro
                FROM Usuario
                WHERE id_usuario = %s
                """,
                (id_usuario,),
            )
            return cursor.fetchone()
        finally:
            cursor.close()
            conexion.close()
