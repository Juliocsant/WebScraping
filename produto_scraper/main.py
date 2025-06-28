from tools.playwright_tools import scrape_page
from utils.parser import extract_prices, find_cheapest_product
from datetime import datetime

url = "https://www.amazon.com.br/s?k=iPhone+15&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss"

html = scrape_page(url)

products = extract_prices(html)

cheapest_product = find_cheapest_product(products)







if cheapest_product:
        print("📦 Produto mais barato encontrado:")
        print(f"🛒 Título: {cheapest_product['title']}")
        print(f"💰 Preço: R$ {cheapest_product['price']:.2f}")
        print(f"📅 Coletado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
else:
    print("❌ Nenhum produto encontrado.")
