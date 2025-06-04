import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from scrapers.tools.user_agent_manager import get_random_user_agent
from scrapers.tools.json_writer import write_prices_json
from scrapers.tools.path_manager import add_scrapers_to_sys_path, get_browser_paths

add_scrapers_to_sys_path()
paths = get_browser_paths()
CHROMIUM_PATH = paths["browser"]
CHROMEDRIVER_PATH = paths["driver"]

PRODUCTS = {
    "Nintendo Switch": "https://www.amazon.com.mx/dp/B0B1NC16VR",
    "PS5 Slim": "https://www.amazon.com.mx/dp/B0CTD19GBT",
    "Xbox Series X": "https://www.amazon.com.mx/dp/B08H75RTZ8",
    "Xbox Series S": "https://www.amazon.com.mx/dp/B08G9J44ZN",
}

def get_amazon_price(driver):
    """Obtiene el precio de Amazon usando múltiples estrategias con verificación"""
    price_strategies = [
        {
            'name': 'Precio principal (centro)',
            'selector': 'span.a-price.reinventPricePriceToPayMargin span.a-offscreen',
            'fallback': 'span.a-price.priceToPay span.a-offscreen'
        },
        {
            'name': 'Precio secundario (esquina)',
            'selector': '#corePrice_feature_div span.a-offscreen',
            'fallback': None
        }
    ]
    
    found_prices = []
    
    for strategy in price_strategies:
        try:
            # Intentar con el selector principal
            try:
                price_element = driver.find_element(By.CSS_SELECTOR, strategy['selector'])
            except:
                # Si falla, intentar con el fallback si existe
                if strategy['fallback']:
                    price_element = driver.find_element(By.CSS_SELECTOR, strategy['fallback'])
                else:
                    continue
            
            price_text = price_element.get_attribute("textContent").strip()
            price_text = price_text.replace('$', '').replace(',', '').strip()
            price_float = float(price_text)
            found_prices.append({
                'value': price_float,
                'source': strategy['name']
            })
            
        except Exception as e:
            continue
    
    # Lógica de decisión
    if not found_prices:
        print("⚠️ No se encontró ningún precio en la página")
        return None
    
    if len(found_prices) == 1:
        print(f"ℹ️ Solo se encontró un precio ({found_prices[0]['source']}): {found_prices[0]['value']}")
        return found_prices[0]['value']
    
    if abs(found_prices[0]['value'] - found_prices[1]['value']) > 0.01:
        print(f"⚠️ Los precios difieren: {found_prices[0]['source']}={found_prices[0]['value']}, {found_prices[1]['source']}={found_prices[1]['value']}")
    
    # Priorizar el precio principal si está disponible
    primary_price = next((p for p in found_prices if 'principal' in p['source']), None)
    if primary_price:
        return primary_price['value']
    
    return found_prices[0]['value']  # Si no, devolver el primero encontrado

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
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            service = Service(CHROMEDRIVER_PATH, log_path=os.devnull)

            driver = webdriver.Chrome(service=service, options=options)
            driver.get(url)
            time.sleep(5)  # Espera ajustable

            price_float = get_amazon_price(driver)
            prices[name] = price_float

            if price_float is None:
                print(f"❌ No se pudo extraer precio para {name}")
            else:
                print(f"💰 Precio obtenido para {name}: {price_float}")

        except Exception as e:
            print(f"⚠️ Error en {name}: {e}")
            prices[name] = None
        finally:
            if 'driver' in locals():
                driver.quit()

    write_prices_json("amazon", "Amazon", prices)

if __name__ == "__main__":
    scrape_amazon()
