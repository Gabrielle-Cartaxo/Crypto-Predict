document.addEventListener('DOMContentLoaded', function() {
    const daysSelect = document.getElementById('days-select');

    // Função para atualizar o gráfico
    function updateGraph(days) {
        fetch(`http://127.0.0.1:5000/predict?days=${days}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                const lastPrices = data.last_prices;
                const predictedPrices = data.predicted_prices;

                // Criar traços para o gráfico
                const trace1 = {
                    x: Array.from({ length: lastPrices.length }, (_, i) => new Date(Date.now() - (lastPrices.length - i) * 24 * 60 * 60 * 1000)),
                    y: lastPrices,
                    mode: 'lines+markers',
                    name: 'Últimos 30 dias',
                    line: { color: 'blue' }
                };

                const trace2 = {
                    x: Array.from({ length: predictedPrices.length }, (_, i) => new Date(Date.now() + (i + 1) * 24 * 60 * 60 * 1000)),
                    y: predictedPrices,
                    mode: 'lines+markers',
                    name: 'Previsões',
                    line: { color: 'red', dash: 'dash' }
                };

                // Calcular a média dos preços previstos e o último preço
                const averagePredicted = predictedPrices.reduce((a, b) => a + b, 0) / predictedPrices.length;
                const lastPrice = lastPrices[lastPrices.length - 1];

                // Atualizar a mensagem de alerta
                const alertMessage = document.getElementById('alert-message');
                alertMessage.innerHTML = '';
                if (averagePredicted < lastPrice) {
                    alertMessage.innerHTML = '<p style="color: red;">Alerta: O Bitcoin está desvalorizando!</p>';
                } else {
                    alertMessage.innerHTML = '<p style="color: green;">Alerta: O Bitcoin está valorizando!</p>';
                }

                // Configurar o layout do gráfico
                const layout = {
                    title: 'Preços de Bitcoin',
                    xaxis: { title: 'Data' },
                    yaxis: { title: 'Preço (USD)' },
                };

                // Criar o gráfico
                Plotly.newPlot('bitcoin-price-graph', [trace1, trace2], layout);

                // Exibir as análises na interface
                document.getElementById('price-analysis').innerText = `O Bitcoin estará ${data.price_analysis} nos próximos dias.`;
                document.getElementById('best-buy-date').innerText = `A melhor data prevista para compra é em ${data.best_buy_date} dias.`;
                document.getElementById('trend-analysis').innerText = `O Bitcoin estará em tendência de ${data.trend_analysis}.`;
            })
            .catch(error => console.error('Erro ao carregar os dados:', error));
    }

    // Adicionar listener para a seleção de dias
    daysSelect.addEventListener('change', function() {
        updateGraph(this.value);
    });

    // Chamar a função com o valor padrão ao carregar
    updateGraph(7);
});
