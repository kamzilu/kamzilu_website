import sys
import os
import json
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from datetime import datetime

# BASE_DIR apunta a /kamzilu/
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.insert(0, os.path.join(BASE_DIR, 'scrapers'))
from tools.user_agent_manager import get_random_user_agent

PRODUCTS = {
    "Nintendo Switch": "https://www.amazon.com.mx/dp/B0B1NC16VR",
    "PS5 Slim": "https://www.amazon.com.mx/dp/B0CTD19GBT",
    "Xbox X": "https://www.amazon.com.mx/dp/B08H75RTZ8",
    "Xbox S": "https://www.amazon.com.mx/dp/B08G9J44ZN",
}

CSV_FILENAME = os.path.join(BASE_DIR, "scrapers/stores/amazon/precios_consolas.csv")
JSON_FILENAME = os.path.join(BASE_DIR, "scrapers/stores/amazon/data/precios.json")
JSON_WEBSITE_PATH = os.path.join(BASE_DIR, "website/data/amazon.json")

# Asegurar carpetas
os.makedirs(os.path.dirname(JSON_FILENAME), exist_ok=True)
os.makedirs(os.path.dirname(JSON_WEBSITE_PATH), exist_ok=True)

if not os.path.exists(CSV_FILENAME):
    with open(CSV_FILENAME, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Hora"] + list(PRODUCTS.keys()))

now = datetime.now().strftime("%Y-%m-%d %I:%M %p")
row = [now]
prices_dict = {"hora": now}

# Determinar rutas de Chromium y Chromedriver
if sys.platform.startswith("linux"):
    CHROMIUM_PATH = "/usr/bin/chromium-browser"
    CHROMEDRIVER_PATH = "/usr/bin/chromedriver"
elif sys.platform.startswith("darwin"):
    CHROMIUM_PATH = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
    CHROMEDRIVER_PATH = "/opt/homebrew/bin/chromedriver"
elif sys.platform.startswith("win"):
    CHROMIUM_PATH = "C:\\Program Files\\Chromium\\Application\\chrome.exe"
    CHROMEDRIVER_PATH = "C:\\path\\to\\chromedriver.exe"
else:
    raise Exception("Sistema operativo no soportado.")

for name, url in PRODUCTS.items():
    try:
        print(f"Scrapeando {name}...")

        options = Options()
        options.binary_location = CHROMIUM_PATH
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument(f"user-agent={get_random_user_agent()}")

        service = Service(CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(url)
        time.sleep(4)

        try:
            whole = driver.find_element(By.CSS_SELECTOR, "span.a-price-whole").text.strip().replace(',', '').replace('.', '')
            fraction_elements = driver.find_elements(By.CSS_SELECTOR, "span.a-price-fraction")
            fraction = fraction_elements[0].text.strip() if fraction_elements else "00"
            price_str = f"{whole}.{fraction}"
            price_float = float(price_str)
            print(f"  ✅ Precio encontrado: {price_float:.2f}")
        except:
            price_float = None
            print(f"  ⚠️ No se encontró precio para {name}")

        row.append(price_float if price_float is not None else "N/D")
        prices_dict[name] = price_float if price_float is not None else None
    except Exception as e:
        print(f"  🛑 Error al obtener precio de {name}: {e}")
        row.append("N/D")
        prices_dict[name] = None
    finally:
        if 'driver' in locals():
            driver.quit()

# Guardar CSV
with open(CSV_FILENAME, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(row)

print(f"\n✅ Fila guardada en CSV: {CSV_FILENAME}")

# Guardar JSON en scrapers y website
with open(JSON_FILENAME, mode="w", encoding="utf-8") as json_file:
    json.dump(prices_dict, json_file, indent=4, ensure_ascii=False)
print(f"📁 JSON exportado en: {JSON_FILENAME}")

with open(JSON_WEBSITE_PATH, mode="w", encoding="utf-8") as json_file:
    json.dump(prices_dict, json_file, indent=4, ensure_ascii=False)
print(f"📁 JSON exportado para website en: {JSON_WEBSITE_PATH}")
