from decimal import Decimal
from conexion import obtener_conexion


class Plato:
    TIPOS = ("DESAYUNO", "ALMUERZO", "CENA")

    @classmethod
    def crear(cls, nombre, descripcion, precio, tipo):
        tipo = tipo.upper()
        if tipo not in cls.TIPOS:
            raise ValueError("El tipo debe ser DESAYUNO, ALMUERZO o CENA.")

        precio = Decimal(str(precio))
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO Plato (nombre, descripcion, precio, tipo)
                VALUES (%s, %s, %s, %s)
                """,
                (nombre.strip(), descripcion.strip(), precio, tipo),
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
    def listar(tipo=None, solo_activos=True):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        try:
            condiciones = []
            parametros = []
            if tipo:
                tipo = tipo.upper()
                if tipo not in Plato.TIPOS:
                    raise ValueError("Tipo de plato no válido.")
                condiciones.append("tipo = %s")
                parametros.append(tipo)
            if solo_activos:
                condiciones.append("activo = TRUE")

            sql = "SELECT id_plato, nombre, descripcion, precio, tipo, activo FROM Plato"
            if condiciones:
                sql += " WHERE " + " AND ".join(condiciones)
            sql += " ORDER BY tipo, nombre"
            cursor.execute(sql, tuple(parametros))
            return cursor.fetchall()
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def asociar_ingrediente(id_plato, id_inventario, cantidad_necesaria):
        cantidad = Decimal(str(cantidad_necesaria))
        if cantidad <= 0:
            raise ValueError("La cantidad necesaria debe ser mayor que cero.")

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO PlatoInventario (id_plato, id_inventario, cantidad_necesaria)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE cantidad_necesaria = VALUES(cantidad_necesaria)
                """,
                (id_plato, id_inventario, cantidad),
            )
            conexion.commit()
        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def ingredientes(id_plato):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT i.id_inventario, i.producto, i.unidad_medida,
                       pi.cantidad_necesaria, i.cantidad_actual
                FROM PlatoInventario pi
                INNER JOIN Inventario i ON i.id_inventario = pi.id_inventario
                WHERE pi.id_plato = %s
                ORDER BY i.producto
                """,
                (id_plato,),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conexion.close()
