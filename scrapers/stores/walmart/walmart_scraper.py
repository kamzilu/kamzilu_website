from scrapers.tools.user_agent_manager import get_random_user_agent
from scrapers.tools.json_writer import write_prices_json
import requests
from bs4 import BeautifulSoup

def scrape_walmart():
    urls = {
        "Nintendo Switch": "https://www.walmart.com.mx/ip/nintendo-switch/consola-nintendo-switch-modelo-oled-blanco/00004549688338",
        "PS5 Slim": "https://www.walmart.com.mx/ip/playstation-5/consola-playstation-5-sony-1tb-slim-con-ratchet-y-clank-y-returnal/00071171957088",
        "Xbox X": "https://www.walmart.com.mx/ip/xbox-series/consola-xbox-series-x-de-1-tb-negra-xbox-xbox-series-x/00088984264072",
        "Xbox S": "https://www.walmart.com.mx/ip/xbox-series/consola-xbox-series-s-512-gb-digital-blanco/00088984265135"
    }
    headers = {"User-Agent": get_random_user_agent()}
    prices = {}

    for product, url in urls.items():
        print(f"📦 Cargando página: {product}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Buscar directamente todos los precios con itemprop="price"
            price_elements = soup.find_all("span", itemprop="price")
            if price_elements:
                # Tomar el primer precio válido
                price_text = price_elements[0].get_text(strip=True).replace("$", "").replace(",", "")
                prices[product] = float(price_text)
                print(f"💰 {product}: {price_text}")
            else:
                print(f"❌ No se encontró ningún precio válido para {product}.")

        except requests.RequestException as e:
            print(f"⚠️ Error en {product}: {e}")

    write_prices_json("website/data/walmart.json", "Walmart", prices)

if __name__ == "__main__":
    scrape_walmart()
