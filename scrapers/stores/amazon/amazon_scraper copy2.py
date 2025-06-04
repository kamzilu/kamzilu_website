import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from scrapers.tools.user_agent_manager import get_random_user_agent
from scrapers.tools.json_writer import write_prices_json

# BASE_DIR apunta a /kamzilu/
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.insert(0, os.path.join(BASE_DIR, 'scrapers'))

PRODUCTS = {
    "Nintendo Switch": "https://www.amazon.com.mx/dp/B0B1NC16VR",
    "PS5 Slim": "https://www.amazon.com.mx/dp/B0CTD19GBT",
    "Xbox X": "https://www.amazon.com.mx/dp/B08H75RTZ8",
    "Xbox S": "https://www.amazon.com.mx/dp/B08G9J44ZN",
}

JSON_OUTPUT_PATH = os.path.join(BASE_DIR, "website/data/amazon.json")

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

def scrape_amazon():
    prices = {}
    for name, url in PRODUCTS.items():
        print(f"📦 Cargando página: {name}")
        try:
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
                prices[name] = price_float
                print(f"💰 {name}: {price_float}")
            except:
                prices[name] = None
                print(f"❌ No se encontró precio para {name}")
        except Exception as e:
            print(f"⚠️ Error en {name}: {e}")
            prices[name] = None
        finally:
            if 'driver' in locals():
                driver.quit()

    write_prices_json(JSON_OUTPUT_PATH, "Amazon", prices)

if __name__ == "__main__":
    scrape_amazon()
