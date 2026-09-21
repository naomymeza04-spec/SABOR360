import runpy
import sys
from pathlib import Path

ruta_cli = Path(__file__).resolve().parent / "cli"
sys.path.insert(0, str(ruta_cli))
runpy.run_path(str(ruta_cli / "main.py"), run_name="__main__")