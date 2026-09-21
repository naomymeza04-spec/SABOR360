from decimal import Decimal
from conexion import obtener_conexion


class Consumo:
    @staticmethod
    def registrar(id_usuario, id_plato, cantidad=1, id_menu=None):
        cantidad = int(cantidad)
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT id_usuario FROM Usuario WHERE id_usuario = %s",
                (id_usuario,),
            )
            if cursor.fetchone() is None:
                raise ValueError("El usuario no existe.")

            cursor.execute(
                "SELECT nombre, precio, activo FROM Plato WHERE id_plato = %s FOR UPDATE",
                (id_plato,),
            )
            plato = cursor.fetchone()
            if plato is None:
                raise ValueError("El plato no existe.")
            if not plato["activo"]:
                raise ValueError("El plato está inactivo.")

            if id_menu is not None:
                cursor.execute(
                    "SELECT 1 FROM MenuPlato WHERE id_menu = %s AND id_plato = %s",
                    (id_menu, id_plato),
                )
                if cursor.fetchone() is None:
                    raise ValueError("Ese plato no pertenece al menú indicado.")

            cursor.execute(
                """
                SELECT pi.id_inventario, pi.cantidad_necesaria,
                       i.producto, i.cantidad_actual
                FROM PlatoInventario pi
                INNER JOIN Inventario i ON i.id_inventario = pi.id_inventario
                WHERE pi.id_plato = %s
                FOR UPDATE
                """,
                (id_plato,),
            )
            ingredientes = cursor.fetchall()

            for ingrediente in ingredientes:
                necesario = Decimal(str(ingrediente["cantidad_necesaria"])) * cantidad
                disponible = Decimal(str(ingrediente["cantidad_actual"]))
                if disponible < necesario:
                    raise ValueError(
                        f"Stock insuficiente de {ingrediente['producto']}. "
                        f"Disponible: {disponible}; necesario: {necesario}."
                    )

            total = Decimal(str(plato["precio"])) * cantidad
            cursor.execute(
                """
                INSERT INTO Consumo (id_usuario, id_plato, id_menu, cantidad, total)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (id_usuario, id_plato, id_menu, cantidad, total),
            )
            id_consumo = cursor.lastrowid

            for ingrediente in ingredientes:
                necesario = Decimal(str(ingrediente["cantidad_necesaria"])) * cantidad
                cursor.execute(
                    """
                    UPDATE Inventario
                    SET cantidad_actual = cantidad_actual - %s
                    WHERE id_inventario = %s
                    """,
                    (necesario, ingrediente["id_inventario"]),
                )
                cursor.execute(
                    """
                    INSERT INTO MovimientoInventario
                        (id_inventario, id_administrador, tipo_movimiento, cantidad, motivo)
                    VALUES (%s, NULL, 'SALIDA', %s, %s)
                    """,
                    (
                        ingrediente["id_inventario"],
                        necesario,
                        f"Consumo #{id_consumo}: {plato['nombre']}",
                    ),
                )

            conexion.commit()
            return id_consumo, total
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
                SELECT c.id_consumo, c.fecha_consumo, c.cantidad, c.total,
                       u.nombre AS usuario,
                       p.nombre AS plato, p.tipo,
                       m.nombre AS menu
                FROM Consumo c
                INNER JOIN Usuario u ON u.id_usuario = c.id_usuario
                INNER JOIN Plato p ON p.id_plato = c.id_plato
                LEFT JOIN Menu m ON m.id_menu = c.id_menu
                ORDER BY c.id_consumo DESC
                """
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conexion.close()
