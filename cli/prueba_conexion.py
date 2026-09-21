from conexion import obtener_conexion


def probar():
    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT DATABASE() AS base_actual")
        print("✅ Conectado a:", cursor.fetchone()["base_actual"])

        cursor.execute("SELECT id_plato, nombre, precio, tipo FROM Plato ORDER BY id_plato")
        platos = cursor.fetchall()

        print("\nPlatos guardados:")
        for plato in platos:
            print(
                f"- {plato['id_plato']}: {plato['nombre']} | "
                f"{plato['tipo']} | ${plato['precio']}"
            )

        # Prueba de inserción y consulta
        cursor.execute(
            """
            INSERT INTO Plato (nombre, descripcion, precio, tipo)
            VALUES (%s, %s, %s, %s)
            """,
            ("Plato temporal", "Prueba de conexión Python-MySQL", 5000, "DESAYUNO"),
        )
        id_nuevo = cursor.lastrowid
        conexion.commit()

        cursor.execute(
            "SELECT id_plato, nombre, tipo FROM Plato WHERE id_plato = %s",
            (id_nuevo,),
        )
        guardado = cursor.fetchone()
        print("\n✅ INSERT correcto:", guardado)

        cursor.execute("DELETE FROM Plato WHERE id_plato = %s", (id_nuevo,))
        conexion.commit()
        print("✅ DELETE de prueba correcto. La conexión funciona bien.")

    except Exception as error:
        print(f"❌ Falló la conexión o la prueba: {error}")
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()


if __name__ == "__main__":
    probar()
