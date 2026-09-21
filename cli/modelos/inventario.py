from decimal import Decimal
from conexion import obtener_conexion


class Inventario:
    @staticmethod
    def crear(producto, unidad_medida, cantidad_actual=0, stock_minimo=0):
        cantidad_actual = Decimal(str(cantidad_actual))
        stock_minimo = Decimal(str(stock_minimo))
        if cantidad_actual < 0 or stock_minimo < 0:
            raise ValueError("Las cantidades del inventario no pueden ser negativas.")

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO Inventario
                    (producto, unidad_medida, cantidad_actual, stock_minimo)
                VALUES (%s, %s, %s, %s)
                """,
                (producto.strip(), unidad_medida.strip(), cantidad_actual, stock_minimo),
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
    def listar():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT id_inventario, producto, unidad_medida,
                       cantidad_actual, stock_minimo, fecha_actualizacion,
                       CASE WHEN cantidad_actual <= stock_minimo THEN TRUE ELSE FALSE END AS stock_bajo
                FROM Inventario
                ORDER BY producto
                """
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conexion.close()
