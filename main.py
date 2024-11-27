import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_google_finance(ticker):
    url = f'https://www.google.com/finance/quote/{ticker}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontrar os elementos de preço e nome
        price_div = soup.find('div', class_='YMlKec fxKbKc')
        name_div = soup.find('div', class_='zzDege')  # Nome da ação
        variation_div = soup.find('div', class_='JwB6zf')
        info_divs = soup.find_all('div', class_='P6K39c')  # Usar find_all para pegar todos os elementos
        
        if price_div and name_div:
            price = price_div.text
            name = name_div.text  # Nome da ação
            variation = variation_div.text if variation_div else "N/A"
            info_list = [info.text for info in info_divs]  # Criar uma lista com todos os textos
            
            return ticker, name, price, variation, info_list  # Retornar o ID, nome e informações
        else:
            return None, None
    else:
        return None, None


tickers = [
    'AAPL:NASDAQ',      # Apple Inc.
    '.DJI:INDEXDJX',    # Dow Jones Industrial Average
    '.INX:INDEXSP',     # S&P 500
    '.IXIC:INDEXNASDAQ', # NASDAQ Composite
    'BTC-BRL',          # Bitcoin em Reais
    'USD-BRL',          # Dólar em Reais
    'EUR-BRL',          # Euro em Reais
    'CLW00:NYMEX',      # Petróleo WTI
    'GCW00:COMEX',      # Ouro
    'IBOV:INDEXBVMF',   # Índice Bovespa
    'SIW00:COMEX',      # Prata
    'NVDA:NASDAQ',      # NVIDIA Corporation
    'BBAS3:BVMF',       # Banco do Brasil
    'GOOGL:NASDAQ',     # Alphabet Inc. (Google)
    'AMZN:NASDAQ',      # Amazon.com Inc.
    'MSFT:NASDAQ',      # Microsoft Corporation
    'TSLA:NASDAQ',      # Tesla Inc.
    'META:NASDAQ',        # Meta Platforms, Inc. (Facebook)
    'BRK.A:NYSE',       # Berkshire Hathaway Inc. (Classe A)
    'JPM:NYSE',         # JPMorgan Chase & Co.
    'V:NYSE',           # Visa Inc.
    'PG:NYSE',          # Procter & Gamble Co.
    'DIS:NYSE',         # The Walt Disney Company
    'NFLX:NASDAQ',      # Netflix Inc.
    'INTC:NASDAQ',      # Intel Corporation
    'CSCO:NASDAQ',      # Cisco Systems, Inc.
    'PFE:NYSE',         # Pfizer Inc.
    'KO:NYSE',          # The Coca-Cola Company
]


# Lista para armazenar os resultados
results = []

for i, ticker in enumerate(tickers):
    result = scrape_google_finance(ticker)
    if result:
        id_codigo, name, price, variation, info_list = result
        # Adiciona o ID e as informações em uma linha
        results.append({
            'ID/Código': id_codigo,  # ID ou código do ativo
            'Nome': name,             # Nome da ação
            'Preço': price,
            'Variação': variation,
            'Info': '; '.join(info_list)  # Usar ponto e vírgula para separar as informações
        })
    
    # Exibir progresso
    progress = (i + 1) / len(tickers) * 100
    print(f'Progresso: {progress:.2f}% completo')

# Criar um DataFrame do pandas
df = pd.DataFrame(results)

# Reorganizar as colunas para que o ID fique à esquerda
df = df[['ID/Código', 'Nome', 'Preço', 'Variação', 'Info']]

# Dividir a coluna 'Info' em múltiplas colunas
info_split = df['Info'].str.split('; ', expand=True)

# Concatenar as novas colunas ao DataFrame original
df = pd.concat([df[['ID/Código', 'Nome', 'Preço', 'Variação']], info_split], axis=1)

# Exportar para um arquivo CSV com ponto e vírgula como delimitador
df.to_csv('resultados_google_finance.csv', sep=';', index=False)

print("Os resultados foram salvos em 'resultados_google_finance.csv'.")
