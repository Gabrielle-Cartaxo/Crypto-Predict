import requests
import pandas as pd

def get_crypto_data(crypto_symbol, days=365):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_symbol}/market_chart?vs_currency=usd&days={days}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Falha ao obter dados da API")

# Obtém dados do Bitcoin (últimos 365 dias)
data = get_crypto_data('bitcoin', days=365)

# Converte os dados em um DataFrame do pandas
df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])

# Converte o timestamp para uma data legível
df['date'] = pd.to_datetime(df['timestamp'], unit='ms')

# Salva o DataFrame em um arquivo CSV
df.to_csv('data/bitcoin_data.csv', index=False)