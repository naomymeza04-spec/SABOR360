from conexion import obtener_conexion


class Administrador:
    """Datos adicionales de un usuario con rol de administrador."""

    NIVELES = ("BASICO", "TOTAL")

    @staticmethod
    def crear(id_usuario, nivel_acceso="BASICO"):
        nivel_acceso = nivel_acceso.upper()
        if nivel_acceso not in Administrador.NIVELES:
            raise ValueError("El nivel debe ser BASICO o TOTAL.")

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT id_usuario FROM Usuario WHERE id_usuario = %s", (id_usuario,))
            if cursor.fetchone() is None:
                raise ValueError("El usuario indicado no existe.")

            cursor.execute(
                """
                INSERT INTO Administrador (id_usuario, nivel_acceso)
                VALUES (%s, %s)
                """,
                (id_usuario, nivel_acceso),
            )
            id_administrador = cursor.lastrowid
            cursor.execute(
                "UPDATE Usuario SET tipo_usuario = 'ADMINISTRADOR' WHERE id_usuario = %s",
                (id_usuario,),
            )
            conexion.commit()
            return id_administrador
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
                SELECT a.id_administrador, a.nivel_acceso,
                       u.id_usuario, u.nombre, u.correo
                FROM Administrador a
                INNER JOIN Usuario u ON u.id_usuario = a.id_usuario
                ORDER BY a.id_administrador
                """
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conexion.close()
