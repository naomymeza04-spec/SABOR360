# Sabor 360

Sistema de gestión y control para restaurante mediante código QR.

## Ejecutar todo de una vez

Doble clic en `iniciar.bat` (o `.\iniciar.bat` en la terminal). Esto:
1. Carga la base de datos (crea las tablas si no existen).
2. Inicia el backend (API) en http://127.0.0.1:8000/docs
3. Inicia el frontend en http://localhost:5173
4. Abre el navegador con ambos servicios.

Cierra las dos ventanas que se abren para detener los servidores.

## Estructura del proyecto

```
Sabor360/
├── backend/    # API REST con Python + FastAPI
├── frontend/   # Interfaz web con React + Vite
├── cli/        # Prototipo en consola (referencia funcional)
├── db/         # Scripts SQL de la base de datos
└── docs/       # Documentación del proyecto (Word)
```

## Backend (FastAPI)

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Copia `.env.example` → `.env` y pon la contraseña de tu usuario MySQL.

Ejecutar la API:

```bash
uvicorn app.main:app --reload
```

Documentación automática: http://127.0.0.1:8000/docs

## Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

## Base de datos (MySQL)

El script `db/sabor360.sql` crea la base `sabor360` con todas las tablas
(Usuario, Administrador, Inventario, Menu, Plato, Consumo, etc.).

Importar desde el prototipo CLI (requiere el entorno del root):

```bash
python cli/crear_bd.py
```

## Prototipo CLI (referencia funcional)

El código en `cli/` (`main.py`, `modelos/`, `conexion.py`) es un prototipo en
consola que ya funciona contra MySQL y sirve como referencia de la lógica de
negocio para implementar en la API de FastAPI.

## Roles

- **Usuario**: se identifica con código QR y registra su consumo.
- **Administrador**: gestiona usuarios, menú, precios, inventario y reportes.