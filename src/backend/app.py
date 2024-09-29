import os
import json
import numpy as np
import requests
import pandas as pd
import logging
from datetime import datetime
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score

app = Flask(__name__)
CORS(app)

# Carregar o modelo LSTM
model = load_model('models/model_lstm.h5')

# Definir o caminho do arquivo de log (JSON)
log_file_path = 'logs/system_logs.json'

# Função para adicionar um log ao arquivo JSON
def log_action(action, details):
    log_entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'action': action,
        'details': details
    }
    if not os.path.exists('logs'):
        os.makedirs('logs')  # Cria o diretório de logs se não existir
    
    # Carregar o conteúdo existente do arquivo JSON ou criar um novo
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as f:
            logs = json.load(f)
    else:
        logs = []

    # Adicionar o novo log e salvar no arquivo
    logs.append(log_entry)
    with open(log_file_path, 'w') as f:
        json.dump(logs, f, indent=4)

# Função para obter os últimos preços do Bitcoin do CoinGecko
def get_last_month_prices():
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=30'
    response = requests.get(url)
    data = response.json()
    prices = [price[1] for price in data['prices']]
    return prices

# Função para obter os últimos 365 preços do Bitcoin do CoinGecko
def get_last_year_prices():
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=365'
    response = requests.get(url)
    data = response.json()
    prices = [price[1] for price in data['prices']]
    return prices

@app.route('/')
def index():
    return render_template('index.html')  # Renderizando o template

@app.route('/predict', methods=['GET'])
def predict():
    try:
        days = request.args.get('days', default=7, type=int)

        # Obter os últimos 30 preços
        last_prices = get_last_month_prices()

        # Escalar os dados
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(np.array(last_prices).reshape(-1, 1))

        # Criar sequências de entrada para previsão
        X_input = scaled_data[-30:].reshape((1, 30, 1))

        # Fazer a previsão para os próximos dias
        predicted_prices = []
        for _ in range(days):
            predicted = model.predict(X_input)
            predicted_price = scaler.inverse_transform(predicted)
            predicted_prices.append(float(predicted_price[0][0]))
            new_input = np.append(X_input[:, 1:, :], predicted.reshape(1, 1, 1), axis=1)
            X_input = new_input

        # Análise de tendência
        last_prices = last_prices[-30:]
        current_price = last_prices[-1]
        price_analysis = "mais caro" if predicted_prices[0] > current_price else "mais barato"
        best_buy_date = predicted_prices.index(min(predicted_prices))
        trend_analysis = "desvalorização" if np.mean(predicted_prices) < current_price else "valorização"

        # Adicionar um log de previsão
        log_action('predict', {
            'last_prices': last_prices,
            'predicted_prices': predicted_prices,
            'price_analysis': price_analysis,
            'best_buy_date': best_buy_date,
            'trend_analysis': trend_analysis
        })

        return jsonify({
            'last_prices': last_prices,
            'predicted_prices': predicted_prices,
            'price_analysis': price_analysis,
            'best_buy_date': best_buy_date,
            'trend_analysis': trend_analysis
        })
    except Exception as e:
        log_action('predict_error', {'error': str(e)})
        return jsonify({"error": str(e)}), 500

@app.route('/retrain', methods=['POST'])
def retrain():
    try:
        # Obter os últimos 365 preços
        last_year_prices = get_last_year_prices()

        # Preparação dos dados
        df = pd.DataFrame(last_year_prices, columns=['price'])
        df['moving_avg'] = df['price'].rolling(window=30).mean()

        # Normalização dos dados
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(df['moving_avg'].dropna().values.reshape(-1, 1))

        # Criar sequências de entrada (X) e saídas correspondentes (y)
        X, y = create_sequences(scaled_data, 30)

        # Divisão em treino e teste
        train_size = int(len(X) * 0.8)
        X_train, X_test = X[:train_size], X[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]

        # Remodelar para [samples, time steps, features]
        X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
        X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

        # Criar o modelo LSTM
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(30, 1)))
        model.add(Dropout(0.2))
        model.add(LSTM(50))
        model.add(Dropout(0.2))
        model.add(Dense(1))

        # Compilar o modelo
        model.compile(optimizer='adam', loss='mean_squared_error')

        # Treinar o modelo
        history = model.fit(X_train, y_train, epochs=500, batch_size=32, validation_data=(X_test, y_test), verbose=0)

        # Fazer previsões
        predicted = model.predict(X_test)

        # Calcular métricas
        mse = mean_squared_error(y_test, predicted)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, predicted)

        # Salvar o modelo treinado
        model.save('models/model_lstm.h5')

        # Adicionar um log de retreinamento
        log_action('retrain', {
            'mse': mse,
            'rmse': rmse,
            'r2': r2
        })

        return jsonify({
            'success': True,
            'mse': mse,
            'rmse': rmse,
            'r2': r2
        })
    except Exception as e:
        log_action('retrain_error', {'error': str(e)})
        return jsonify({"error": str(e)}), 500

# Função para criar sequências (definida anteriormente)
def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data)-seq_length-1):
        X.append(data[i:(i+seq_length), 0])
        y.append(data[i + seq_length, 0])
    return np.array(X), np.array(y)

@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        # Carregar os logs do arquivo JSON
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as f:
                logs = json.load(f)
            return jsonify({"logs": logs[-100:]})  # Retorna os últimos 100 logs
        else:
            return jsonify({"logs": []})
    except Exception as e:
        return jsonify({"error": "Não foi possível acessar os logs."}), 500

if __name__ == '__main__':
    app.run(debug=True)
