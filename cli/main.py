from modelos import (
    Usuario,
    Administrador,
    Plato,
    Menu,
    Inventario,
    MovimientoInventario,
    Consumo,
)


def pedir_entero(mensaje, permitir_vacio=False):
    valor = input(mensaje).strip()
    if permitir_vacio and valor == "":
        return None
    return int(valor)


def mostrar_usuarios():
    usuarios = Usuario.listar()
    print("\n--- USUARIOS ---")
    for u in usuarios:
        print(f"{u['id_usuario']}. {u['nombre']} | {u['correo']} | {u['tipo_usuario']}")


def mostrar_platos():
    platos = Plato.listar(solo_activos=False)
    print("\n--- PLATOS ---")
    for p in platos:
        estado = "ACTIVO" if p["activo"] else "INACTIVO"
        print(f"{p['id_plato']}. {p['nombre']} | {p['tipo']} | ${p['precio']} | {estado}")


def mostrar_inventario():
    productos = Inventario.listar()
    print("\n--- INVENTARIO ---")
    for p in productos:
        aviso = " ⚠ STOCK BAJO" if p["stock_bajo"] else ""
        print(
            f"{p['id_inventario']}. {p['producto']} | "
            f"{p['cantidad_actual']} {p['unidad_medida']} | mínimo: {p['stock_minimo']}{aviso}"
        )


def mostrar_menus():
    menus = Menu.listar()
    print("\n--- MENÚS ---")
    for m in menus:
        print(f"{m['id_menu']}. {m['nombre']} | {m['fecha_menu']} | {m['descripcion'] or ''}")
        for p in Menu.platos(m["id_menu"]):
            print(f"   - {p['nombre']} ({p['tipo']}) ${p['precio']}")


def mostrar_consumos():
    consumos = Consumo.listar()
    print("\n--- CONSUMOS ---")
    for c in consumos:
        menu = c["menu"] or "Sin menú"
        print(
            f"#{c['id_consumo']} | {c['fecha_consumo']} | {c['usuario']} | "
            f"{c['plato']} ({c['tipo']}) x{c['cantidad']} | ${c['total']} | {menu}"
        )


def menu_principal():
    while True:
        print("\n" + "=" * 42)
        print("              SABOR 360")
        print("=" * 42)
        print("1. Registrar usuario")
        print("2. Ver usuarios")
        print("3. Convertir usuario en administrador")
        print("4. Registrar plato")
        print("5. Ver platos")
        print("6. Crear menú")
        print("7. Agregar plato a un menú")
        print("8. Ver menús")
        print("9. Registrar producto de inventario")
        print("10. Ver inventario")
        print("11. Registrar entrada/salida de inventario")
        print("12. Asociar ingrediente a un plato")
        print("13. Registrar consumo")
        print("14. Ver consumos")
        print("15. Ver movimientos de inventario")
        print("0. Salir")

        opcion = input("Seleccione una opción: ").strip()

        try:
            if opcion == "1":
                nombre = input("Nombre: ").strip()
                correo = input("Correo: ").strip()
                contrasena = input("Contraseña: ").strip()
                u = Usuario.crear(nombre, correo, contrasena)
                print(f"✅ Usuario guardado con ID {u.id_usuario}.")

            elif opcion == "2":
                mostrar_usuarios()

            elif opcion == "3":
                mostrar_usuarios()
                id_usuario = pedir_entero("ID del usuario: ")
                print("1. BASICO\n2. TOTAL")
                nivel = "TOTAL" if input("Nivel: ").strip() == "2" else "BASICO"
                id_admin = Administrador.crear(id_usuario, nivel)
                print(f"✅ Administrador creado con ID {id_admin}.")

            elif opcion == "4":
                nombre = input("Nombre del plato: ").strip()
                descripcion = input("Descripción: ").strip()
                precio = input("Precio: ").strip()
                print("1. DESAYUNO\n2. ALMUERZO\n3. CENA")
                seleccion = input("Tipo: ").strip()
                tipos = {"1": "DESAYUNO", "2": "ALMUERZO", "3": "CENA"}
                if seleccion not in tipos:
                    raise ValueError("Selección de tipo inválida.")
                id_plato = Plato.crear(nombre, descripcion, precio, tipos[seleccion])
                print(f"✅ Plato guardado con ID {id_plato}.")

            elif opcion == "5":
                mostrar_platos()

            elif opcion == "6":
                nombre = input("Nombre del menú: ").strip()
                fecha = input("Fecha (AAAA-MM-DD): ").strip()
                descripcion = input("Descripción: ").strip()
                id_menu = Menu.crear(nombre, fecha, descripcion)
                print(f"✅ Menú creado con ID {id_menu}.")

            elif opcion == "7":
                mostrar_menus()
                mostrar_platos()
                id_menu = pedir_entero("ID del menú: ")
                id_plato = pedir_entero("ID del plato: ")
                Menu.agregar_plato(id_menu, id_plato)
                print("✅ Plato agregado al menú.")

            elif opcion == "8":
                mostrar_menus()

            elif opcion == "9":
                producto = input("Producto/ingrediente: ").strip()
                unidad = input("Unidad de medida (kg, g, L, unidad...): ").strip()
                cantidad = input("Cantidad inicial: ").strip()
                minimo = input("Stock mínimo: ").strip()
                id_inv = Inventario.crear(producto, unidad, cantidad, minimo)
                print(f"✅ Producto guardado con ID {id_inv}.")

            elif opcion == "10":
                mostrar_inventario()

            elif opcion == "11":
                mostrar_inventario()
                id_inv = pedir_entero("ID del producto: ")
                print("1. ENTRADA\n2. SALIDA")
                tipo = "SALIDA" if input("Tipo: ").strip() == "2" else "ENTRADA"
                cantidad = input("Cantidad: ").strip()
                motivo = input("Motivo: ").strip()
                id_admin = pedir_entero("ID administrador (Enter si no aplica): ", permitir_vacio=True)
                id_mov = MovimientoInventario.registrar(id_inv, tipo, cantidad, motivo, id_admin)
                print(f"✅ Movimiento registrado con ID {id_mov}.")

            elif opcion == "12":
                mostrar_platos()
                mostrar_inventario()
                id_plato = pedir_entero("ID del plato: ")
                id_inv = pedir_entero("ID del ingrediente: ")
                cantidad = input("Cantidad usada por cada plato: ").strip()
                Plato.asociar_ingrediente(id_plato, id_inv, cantidad)
                print("✅ Ingrediente asociado al plato.")

            elif opcion == "13":
                mostrar_usuarios()
                mostrar_platos()
                id_usuario = pedir_entero("ID del usuario: ")
                id_plato = pedir_entero("ID del plato: ")
                cantidad = pedir_entero("Cantidad de platos: ")
                id_menu = pedir_entero("ID del menú (Enter si no aplica): ", permitir_vacio=True)
                id_consumo, total = Consumo.registrar(id_usuario, id_plato, cantidad, id_menu)
                print(f"✅ Consumo #{id_consumo} guardado. Total: ${total}.")

            elif opcion == "14":
                mostrar_consumos()

            elif opcion == "15":
                print("\n--- MOVIMIENTOS DE INVENTARIO ---")
                for m in MovimientoInventario.listar():
                    admin = m["administrador"] or "Automático/Sin administrador"
                    print(
                        f"#{m['id_movimiento']} | {m['fecha_movimiento']} | "
                        f"{m['tipo_movimiento']} {m['cantidad']} {m['unidad_medida']} | "
                        f"{m['producto']} | {m['motivo'] or ''} | {admin}"
                    )

            elif opcion == "0":
                print("Hasta luego. Sabor 360 cerrado correctamente.")
                break

            else:
                print("⚠ Opción no válida.")

        except ValueError as error:
            print(f"⚠ {error}")
        except Exception as error:
            print(f"❌ Ocurrió un error: {error}")


if __name__ == "__main__":
    menu_principal()
