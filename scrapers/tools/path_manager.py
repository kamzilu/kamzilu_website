from pathlib import Path
import sys
import platform

def find_project_root(current_path=None):
    """Busca hacia arriba hasta encontrar el directorio raíz del proyecto"""
    path = Path(current_path or __file__).absolute()
    while not (path / 'scrapers').exists() and path.parent != path:
        path = path.parent
    return path

# Detectar la raíz del proyecto
PROJECT_ROOT = find_project_root()

def add_scrapers_to_sys_path():
    """Añade la carpeta scrapers al sys.path para imports consistentes"""
    sys.path.insert(0, str(PROJECT_ROOT / 'scrapers'))

def get_output_path(subfolder="website/data"):
    """Devuelve la ruta absoluta para guardar datos"""
    return PROJECT_ROOT / subfolder

def get_browser_paths():
    """Devuelve paths para Chromium y Chromedriver según OS"""
    system = platform.system().lower()
    driver_dir = PROJECT_ROOT / "scrapers" / "tools" / "drivers"
    if system.startswith("linux"):
        return {
            "browser": "/usr/bin/chromium-browser",
            "driver": str(driver_dir / "chromedriver_linux")
        }
    elif system.startswith("darwin"):  # macOS
        return {
            "browser": "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
            "driver": str(driver_dir / "chromedriver_mac")
        }
    elif system.startswith("windows"):
        return {
            "browser": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",  # Cambiado aquí
            "driver": str(driver_dir / "chromedriver_win.exe")
        }
    else:
        raise Exception("Sistema operativo no soportado.")
