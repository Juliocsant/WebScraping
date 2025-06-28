from bs4 import BeautifulSoup
import re


def smart_price_conversion(price_text):

    """Converte preços  para float"""
    if not price_text:
        return None


    price_clean = re.sub(r'(R\$|\$|USD|&nbsp;|\s)', '', price_text)

    comma_count = price_clean.count(',')
    dot_count = price_clean.count('.')
    dot_position = price_clean.rfind('.')
    comma_position = price_clean.rfind(',')
# Caso 1: Formato americano 1,299.99

    try:
        if comma_count >= 1 and len(price_clean) - dot_position == 3:  
              # .99, .50, .00
                # É formato americano!
                # Remove todas as vírgulas (milhares)
                price_clean = price_clean.replace(',', '')
                # Mantém o ponto (decimais)
                return float(price_clean)

    # Caso 2: Formato brasileiro 1.299,99
        elif dot_count >=1 and len(price_clean) - comma_position == 3:           
            # Verifica se a vírgula está nos últimos 3 caracteres
                # Substitui a vírgula por ponto e remove o ponto
                price_clean = price_clean.replace('.','')
                price_clean = price_clean.replace(',', '.')
                return float(price_clean)

    # Caso 3: Formato Americano 299.99
        elif dot_count == 1 and comma_count == 0:
            return float(price_clean)

    # Caso 4: Formato Brasileiro 299,99
        elif comma_count == 1 and dot_count == 0:

            price_clean = price_clean.replace(',', '.')
            return float(price_clean)

        else:
            return float(price_clean)

    except ValueError:
            return None


def extract_prices(html):
    """
    Extrai preços de produtos da Amazon
    
    Por que essa função?
    - Centraliza a lógica de parsing
    - Facilita testes e debugging
    - Reutilizável para diferentes páginas
    """
    soup = BeautifulSoup(html,"html.parser")


    products = []

# Por que usar .select() em vez de .find()?
    # .select() usa seletores CSS (como no navegador)
    # É mais intuitivo se você conhece CSS

    # Encontra todos os produtos
    items = soup.select('.s-result-item')
    # print(f"🔍 Encontrados {len(items)} produtos na página")
 # Para cada produto encontrado
    for item in items:
        # Procurar o título dentro deste item específico

        title_element = item.select_one('h2')
        price_element = item.select_one('.a-offscreen')

           
        if title_element and price_element:
            title = title_element.get_text(strip=True)
            price_text = price_element.get_text(strip=True)
            print(f"Título encontrado: {title}")
            print(f"Preço bruto: {price_text}")


            price = smart_price_conversion(price_text)
            print(f"Preço convertido: {price}")


            if price is not None and isinstance(price, (int, float)):

                produto = {
                    'title': title,
                    'price': price,
                    'price_text': price_text
                }

                products.append(produto)
                print(f"✅ Produto adicionado: R$ {price:.2f}")
            else:
                    print(f"❌ Não conseguiu converter preço: {price_text}")
        else:
            print("⚠️ Produto sem título ou preço")

    return products





def find_cheapest_product(products):
    """Encontra o produto mais barato"""
    if not products:
        return None
    
    cheapest = min(products, key=lambda x: x["price"])
    return cheapest




# if __name__ == "__main__":
#     # HTML de teste
#     html_teste = """
#     <div class="s-result-item">
#         <h2><span>iPhone 15 Pro</span></h2>
#         <span class="a-price">
#             <span class="a-offscreen">R$ 999,00</span>
#         </span>
#     </div>
    
#     <div class="s-result-item">
#         <h2><span>Samsung Galaxy S24</span></h2>
#         <span class="a-price">
#             <span class="a-offscreen">$299.99</span>
#         </span>
#     </div>
#     """
    
#     # Teste suas funções
#     print("=== TESTANDO PARSER ===")
    
#     # Teste 1: Conversão de preços
#     print("\n1. Testando conversão de preços:")
#     print(f"R$ 8.999,00 → {smart_price_conversion('R$ 8.999,00')}")
#     print(f"$1,299.99 → {smart_price_conversion('$1,299.99')}")
    
#     # Teste 2: Extração completa
#     print("\n2. Testando extração de produtos:")
#     produtos = extract_prices(html_teste)
#     # print(find_cheapest_product(produtos))

#     for i, produto in enumerate(produtos):
#         print(f"Posição {i+1}: {produto}")

#     # for i in range(len(produtos)):
#     #     produto = produtos[i]
#     #     print(f"Produto {i}: {produto}")  