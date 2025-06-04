import os
import json
from datetime import datetime
from scrapers.tools.path_manager import get_output_path

def write_prices_json(store_subfolder, store_name, prices):
    """
    Guarda un JSON uniforme con hora y precios en dos ubicaciones.
    - store_subfolder: subcarpeta específica del store (ej: "amazon", "walmart").
    - store_name: nombre del store (para logs).
    - prices: dict con precios, ej: {"Nintendo Switch": 5299.0}.
    """
    data = {
        "hora": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
        "Nintendo Switch": None,
        "PS5 Slim": None,
        "Xbox Series X": None,
        "Xbox Series S": None
    }
    data.update(prices)

    # Guardar en scrapers/stores/{store_subfolder}/data
    path1 = get_output_path(f"scrapers/stores/{store_subfolder}/data/{store_subfolder}.json")
    os.makedirs(os.path.dirname(path1), exist_ok=True)
    with open(path1, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"✅ Datos guardados en {path1} 📦 ({store_name})")

    # Guardar en website/data
    path2 = get_output_path(f"website/data/{store_subfolder}.json")
    os.makedirs(os.path.dirname(path2), exist_ok=True)
    with open(path2, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"✅ Copia guardada en {path2} 📦 ({store_name})")
