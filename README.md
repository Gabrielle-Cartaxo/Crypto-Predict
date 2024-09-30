# Documentação do Sistema de Previsão de Criptoativos

## Índice

1. [Descrição do Sistema](#descrição-do-sistema)
2. [Funcionalidades](#funcionalidades)
3. [Arquitetura do Sistema](#arquitetura-do-sistema)
4. [Requisitos](#requisitos)
5. [Instruções de Instalação](#instruções-de-instalação)
6. [Guia de Execução](#guia-de-execução)
7. [Uso do Sistema](#uso-do-sistema)
8. [Considerações Finais](#considerações-finais)

## Descrição do Sistema

O Sistema de Previsão de Criptoativos é uma aplicação que utiliza técnicas de Machine Learning para analisar dados históricos de preços de criptomoedas, especificamente do Bitcoin, coletados através da API da CoinGecko (para mais detalhes sobre o acesso a API, acesse ````src/exploracao/import_data.py``` e prever os melhores momentos de compra e venda. O sistema é dividido em duas partes principais: um frontend interativo para visualização e interação do usuário e um backend que processa as solicitações e executa um modelo de previsão. O modelo escolhido foi um LSTM, e para ver mais detalhes da exploração dos dados e escolha dos modelos, acesse os notebooks que estão no diretório ```src/exploracao```, sendo eles **exploracao.ipynb** e **modelo.ipynb**.

## Funcionalidades

- **Análise Histórica**: O sistema coleta dados históricos de criptomoedas da API do CoinGecko.
- **Previsão de Preços**: Utiliza um modelo LSTM para prever os preços futuros de criptoativos.
- **Interface Interativa**: Um dashboard que permite aos usuários visualizar gráficos de preços e previsões.
- **Botão de Retreinamento**: Permite ao usuário retreinar o modelo com dados recentes, atualizando as previsões.
- **Alertas de Preço**: Exibe mensagens de alerta com base na média dos valores previstos em comparação com o último valor histórico.
- **Escolha de Período**: Usuários podem escolher o número de dias de previsão (7, 14 ou 30 dias).

Para visualizar o funcionamento do sistema, assista aos vídeos abaixo:

### Sistema de previsões de Bitcoin + Retreinamento
[![Assista ao vídeo](https://img.youtube.com/vi/49Lh5dwHcpU/0.jpg)](https://youtu.be/49Lh5dwHcpU)

### Logs do Sistema
[![Assista ao vídeo](https://img.youtube.com/vi/Uxm8aGU16FY/0.jpg)](https://youtu.be/Uxm8aGU16FY)

## Arquitetura do Sistema

O sistema é composto por duas partes principais:

1. **Frontend**:
   - Construído usando Flask, HTML, CSS e JavaScript.
   - Interage com o usuário e apresenta as informações de maneira visual.

2. **Backend**:
   - Também implementado em Flask, com a lógica de negócio para processamento de dados e modelagem.
   - Utiliza TensorFlow para o treinamento e execução do modelo de Machine Learning.
   - Utiliza SQLite para armazenar os dados dos logs do sistema.

## Requisitos

### Software

- **Docker**: Para executar a aplicação em contêineres.
- **Docker Compose**: Para gerenciar múltiplos contêineres.
- **Python**: O backend requer Python 3.7 ou superior.

### Dependências

As dependências estão listadas no arquivo `requirements.txt`. Algumas delas incluem:

- Flask
- TensorFlow
- NumPy
- Pandas
- Requests
- Matplotlib

## Instruções de Instalação

1. **Instalação do Docker**:
   - Baixe e instale o Docker do site oficial: [Docker](https://www.docker.com/get-started).

2. **Instalação do Docker Compose**:
   - O Docker Compose geralmente vem incluído com a instalação do Docker. Caso contrário, siga as instruções no site oficial: [Docker Compose](https://docs.docker.com/compose/install/).

3. **Clone o Repositório**:
   - Clone o repositório do projeto:
     ```bash
     git clone https://github.com/Gabrielle-Cartaxo/Crypto-Predict.git
     ```

## Guia de Execução

1. **Navegue até o Diretório do Projeto**:
   ```bash
    cd Crypto-Predict
   ```

2. **Inicie os Contêineres**:
   - Execute o seguinte comando para iniciar os contêineres:
   ```bash
   docker-compose up
   ```

3. **Acesse o Frontend**:
   - Abra seu navegador e vá para `http://localhost:8000` para acessar o dashboard do frontend.

4. **Verifique o Backend**:
   - Para verificar se o backend está funcionando, você pode acessar `http://localhost:5000`.

## Uso do Sistema

1. **Visualização de Preços**:
   - Ao acessar o dashboard, você verá gráficos de preços históricos e previsões.

2. **Escolha de Dias de Previsão**:
   - Use o seletor para escolher quantos dias de previsão deseja visualizar (7, 14 ou 30).

3. **Retreinamento do Modelo**:
   - Clique no botão de retreinamento para atualizar o modelo com dados recentes. O sistema exibirá uma mensagem indicando se o treinamento foi bem-sucedido e apresentará as métricas do modelo (MSE, RMSE e R²).

4. **Alertas de Preço**:
   - O sistema mostrará alertas com base na comparação entre a média dos valores previstos e o último valor histórico.

5. **Logs do Sistema**:
    - É possível acessar todos os logs do sistema acessando a rota localhost/5000/logs.

## Considerações Finais

Este sistema de previsão de criptoativos é uma ferramenta poderosa para auxiliar na tomada de decisões de investimento. Com a capacidade de prever tendências de preços e visualizar dados de maneira intuitiva, os usuários podem aproveitar as oportunidades do mercado de criptomoedas. Lembre-se de que, como todo modelo de previsão, ele pode não ser 100% preciso e deve ser utilizado com cautela.

Para contribuições ou melhorias, sinta-se à vontade para abrir uma issue ou pull request no repositório.
