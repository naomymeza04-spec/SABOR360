from decimal import Decimal
from conexion import obtener_conexion


class MovimientoInventario:
    TIPOS = ("ENTRADA", "SALIDA")

    @classmethod
    def registrar(cls, id_inventario, tipo_movimiento, cantidad, motivo="", id_administrador=None):
        tipo_movimiento = tipo_movimiento.upper()
        if tipo_movimiento not in cls.TIPOS:
            raise ValueError("El movimiento debe ser ENTRADA o SALIDA.")

        cantidad = Decimal(str(cantidad))
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT cantidad_actual FROM Inventario WHERE id_inventario = %s FOR UPDATE",
                (id_inventario,),
            )
            inventario = cursor.fetchone()
            if inventario is None:
                raise ValueError("El producto de inventario no existe.")

            actual = Decimal(str(inventario["cantidad_actual"]))
            nuevo = actual + cantidad if tipo_movimiento == "ENTRADA" else actual - cantidad
            if nuevo < 0:
                raise ValueError("No hay suficiente stock para realizar la salida.")

            cursor.execute(
                "UPDATE Inventario SET cantidad_actual = %s WHERE id_inventario = %s",
                (nuevo, id_inventario),
            )
            cursor.execute(
                """
                INSERT INTO MovimientoInventario
                    (id_inventario, id_administrador, tipo_movimiento, cantidad, motivo)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (id_inventario, id_administrador, tipo_movimiento, cantidad, motivo.strip()),
            )
            id_movimiento = cursor.lastrowid
            conexion.commit()
            return id_movimiento
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
                SELECT m.id_movimiento, m.tipo_movimiento, m.cantidad,
                       m.motivo, m.fecha_movimiento,
                       i.producto, i.unidad_medida,
                       u.nombre AS administrador
                FROM MovimientoInventario m
                INNER JOIN Inventario i ON i.id_inventario = m.id_inventario
                LEFT JOIN Administrador a ON a.id_administrador = m.id_administrador
                LEFT JOIN Usuario u ON u.id_usuario = a.id_usuario
                ORDER BY m.id_movimiento DESC
                """
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conexion.close()
