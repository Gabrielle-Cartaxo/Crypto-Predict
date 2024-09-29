from flask import Flask, jsonify
import numpy as np
import requests
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)

# Carregar o modelo
model = load_model('../models/model_lstm.h5')

# Inicializar o scaler
scaler = MinMaxScaler(feature_range=(0, 1))


# Função para obter os preços dos últimos 30 dias
def get_last_30_days_prices(crypto_symbol):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_symbol}/market_chart?vs_currency=usd&days=30"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return np.array([price[1] for price in data['prices']])  # Extrai apenas os preços
    else:
        raise Exception("Failed to retrieve data from API")

# Rota para prever os preços da proxima semana com base no ultimo mês
@app.route('/predict', methods=['GET'])
def predict():
    last_prices = get_last_30_days_prices('bitcoin')

    # Normaliza os preços
    last_prices_scaled = scaler.fit_transform(last_prices.reshape(-1, 1))

    # Cria a sequência para a previsão
    X_input = last_prices_scaled[-30:].reshape(1, 30, 1)

    # Lista para armazenar as previsões
    predicted_prices = []

    for _ in range(7):  # Prever os próximos 7 dias
        predicted = model.predict(X_input)
        predicted_price = scaler.inverse_transform(predicted.reshape(-1, 1))
        
        # Converte para float e adiciona à lista
        predicted_prices.append(float(predicted_price[0][0]))

        # Atualiza a sequência de entrada para a próxima previsão
        X_input = np.append(X_input[:, 1:, :], predicted.reshape(1, 1, 1), axis=1)

    return jsonify({
        "last_prices": last_prices.tolist(),
        "predicted_prices": predicted_prices
    })

if __name__ == '__main__':
    app.run(debug=True)
