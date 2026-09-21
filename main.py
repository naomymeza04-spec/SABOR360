import sys
import subprocess
import time
import webbrowser
from pathlib import Path

ruta_raiz = Path(__file__).resolve().parent
python = ruta_raiz / ".venv" / "Scripts" / "python.exe"


def iniciar_backend():
    print("Iniciando backend en http://127.0.0.1:8000 ...")
    return subprocess.Popen(
        [str(python), "-m", "uvicorn", "backend.app.main:app", "--port", "8000"],
        cwd=ruta_raiz,
    )


def iniciar_frontend():
    print("Iniciando frontend en http://localhost:5173 ...")
    return subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=ruta_raiz / "frontend",
        shell=True,
    )


def iniciar_todo():
    backend = iniciar_backend()
    frontend = iniciar_frontend()
    time.sleep(4)
    webbrowser.open("http://localhost:5173")
    print("\nBackend y frontend en marcha. Presiona Ctrl+C para detenerlos.")
    try:
        while backend.poll() is None or frontend.poll() is None:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        backend.terminate()
        frontend.terminate()


if "cli" in sys.argv[1:]:
    import runpy

    ruta_cli = ruta_raiz / "cli"
    sys.path.insert(0, str(ruta_cli))
    runpy.run_path(str(ruta_cli / "main.py"), run_name="__main__")
elif "api" in sys.argv[1:]:
    import uvicorn

    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000)
else:
    iniciar_todo()