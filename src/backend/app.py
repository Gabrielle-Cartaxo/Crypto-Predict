from flask import Flask, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
import numpy as np
import requests
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)
CORS(app)

# Carregar o modelo LSTM
model = load_model('models/model_lstm.h5')

# Função para obter os últimos preços do Bitcoin do CoinGecko
def get_last_prices():
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=30'
    response = requests.get(url)
    data = response.json()
    prices = [price[1] for price in data['prices']]
    return prices

# Parâmetros do modelo
sequence_length = 30

@app.route('/predict', methods=['GET'])
def predict():
    try:
        # Obter os últimos 30 preços
        last_prices = get_last_prices()
        
        # Escalar os dados
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(np.array(last_prices).reshape(-1, 1))

        # Criar sequências de entrada para previsão
        sequence_length = 30  # Usar os últimos 30 preços
        X_input = scaled_data[-sequence_length:].reshape((1, sequence_length, 1))

        # Fazer a previsão para os próximos 7 dias
        predicted_prices = []
        for _ in range(7):
            # Fazer a previsão
            predicted = model.predict(X_input)
            
            # Reescalar o preço previsto e converter para float
            predicted_price = scaler.inverse_transform(predicted)
            predicted_prices.append(float(predicted_price[0][0]))
            
            # Atualizar a entrada com o novo preço previsto
            new_input = np.append(X_input[:, 1:, :], predicted.reshape(1, 1, 1), axis=1)
            X_input = new_input

        # Converter resultados para listas normais
        last_prices = last_prices[-30:]  # Últimos 30 preços reais

        # Retornar os resultados como JSON
        return jsonify({
            'last_prices': last_prices,
            'predicted_prices': predicted_prices
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
