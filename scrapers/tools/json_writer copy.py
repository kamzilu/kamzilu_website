import os
import json
from datetime import datetime

def write_prices_json(output_path, store_name, prices):
    """
    Guarda un JSON uniforme con hora y precios.
    - output_path: ruta del archivo JSON.
    - store_name: nombre de la tienda (para logs).
    - prices: dict con productos y precios, ej: {"Nintendo Switch": 5299.0}.
    """
    data = {
        "hora": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
        "Nintendo Switch": None,
        "PS5 Slim": None,
        "Xbox Series X": None,
        "Xbox Series S": None
    }
    data.update(prices)  # Actualiza solo los productos con datos nuevos

    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"✅ Datos guardados exitosamente en {output_path} 📦 ({store_name})")
