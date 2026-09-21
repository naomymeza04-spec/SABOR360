from conexion import obtener_conexion


class Menu:
    @staticmethod
    def crear(nombre, fecha_menu, descripcion=""):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO Menu (nombre, fecha_menu, descripcion)
                VALUES (%s, %s, %s)
                """,
                (nombre.strip(), fecha_menu, descripcion.strip()),
            )
            conexion.commit()
            return cursor.lastrowid
        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def agregar_plato(id_menu, id_plato):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT IGNORE INTO MenuPlato (id_menu, id_plato) VALUES (%s, %s)",
                (id_menu, id_plato),
            )
            conexion.commit()
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
                SELECT id_menu, nombre, fecha_menu, descripcion
                FROM Menu
                ORDER BY fecha_menu DESC, id_menu DESC
                """
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def platos(id_menu):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT p.id_plato, p.nombre, p.tipo, p.precio
                FROM MenuPlato mp
                INNER JOIN Plato p ON p.id_plato = mp.id_plato
                WHERE mp.id_menu = %s
                ORDER BY p.tipo, p.nombre
                """,
                (id_menu,),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conexion.close()
