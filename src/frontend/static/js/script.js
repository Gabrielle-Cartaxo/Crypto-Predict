document.addEventListener('DOMContentLoaded', function() {
    fetch('http://127.0.0.1:5000/predict')  // A requisição deve ir para o backend na porta 5000
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const lastPrices = data.last_prices;
            const predictedPrices = data.predicted_prices;

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

            const layout = {
                title: 'Preços de Bitcoin',
                xaxis: { title: 'Data' },
                yaxis: { title: 'Preço (USD)' },
            };

            Plotly.newPlot('bitcoin-price-graph', [trace1, trace2], layout);
        })
        .catch(error => console.error('Erro ao carregar os dados:', error));
});
