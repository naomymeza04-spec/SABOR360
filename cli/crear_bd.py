from pathlib import Path
from conexion import obtener_conexion


def ejecutar_script_sql():
    ruta_sql = Path(__file__).resolve().parent.parent / "db" / "sabor360.sql"
    script = ruta_sql.read_text(encoding="utf-8")

    conexion = obtener_conexion(usar_bd=False)
    cursor = conexion.cursor()

    try:
        for sentencia in script.split(";"):
            sentencia = sentencia.strip()
            if sentencia:
                cursor.execute(sentencia)
        conexion.commit()
        print("✅ Base de datos Sabor 360 creada correctamente.")
    except Exception as error:
        conexion.rollback()
        print(f"❌ Error al crear la base de datos: {error}")
        raise
    finally:
        cursor.close()
        conexion.close()


if __name__ == "__main__":
    ejecutar_script_sql()
