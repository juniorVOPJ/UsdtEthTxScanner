from web3 import Web3
import time
from datetime import datetime
import os
from dotenv import load_dotenv
import csv
import pytz
from flask import Flask, render_template, jsonify
from threading import Thread

# Carrega variáveis de ambiente
load_dotenv()

# Configurações
INFURA_URL = os.getenv('INFURA_URL')
USDT_CONTRACT = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
MIN_VALUE = float(os.getenv('MIN_USDT_VALUE', 100000))
CSV_FILE = "transactions.csv"

# Inicializa Web3
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Timezone Brasil
BR_TZ = pytz.timezone('America/Sao_Paulo')

# Inicializa Flask
app = Flask(__name__)

# ABI do contrato USDT (simplificado)
USDT_ABI = '''[
    {
        "anonymous": false,
        "inputs": [
            {"indexed": true, "name": "from", "type": "address"},
            {"indexed": true, "name": "to", "type": "address"},
            {"indexed": false, "name": "value", "type": "uint256"}
        ],
        "name": "Transfer",
        "type": "event"
    }
]'''

def get_br_datetime():
    return datetime.now(BR_TZ).strftime('%Y-%m-%d %H:%M:%S')

def save_to_csv(timestamp, tx_hash, value):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Data/Hora', 'Hash da Transação', 'Valor (USDT)'])
        # Formatação do valor com separador de milhares e 2 casas decimais
        formatted_value = f"{value:,.2f}"
        writer.writerow([timestamp, tx_hash, formatted_value])

# Rotas Flask
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_transactions')
def get_transactions():
    transactions = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Pula o cabeçalho
            transactions = list(csv_reader)
    return jsonify(transactions)

# Template HTML atualizado com AJAX
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Monitor de Transações USDT</title>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f0f0f0;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            table-layout: fixed;
            margin-bottom: 20px;
        }
        th, td {
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #ddd;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        th {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        th:nth-child(1), td:nth-child(1) { width: 20%; }
        th:nth-child(2), td:nth-child(2) { width: 60%; }
        th:nth-child(3), td:nth-child(3) { width: 20%; }
        
        tr:hover {
            background-color: #f5f5f5;
        }
        a {
            color: #2196F3;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .header {
            margin-bottom: 20px;
            padding: 20px;
            background-color: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            border-radius: 4px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .status {
            font-size: 14px;
            color: #666;
            background-color: #f8f8f8;
            padding: 8px 15px;
            border-radius: 4px;
        }
        #lastUpdate {
            font-weight: bold;
            color: #4CAF50;
        }
        .valor {
            text-align: right;
            font-family: 'Courier New', monospace;
        }
        .totals {
            background-color: white;
            padding: 20px;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .total-item {
            text-align: center;
            flex: 1;
            padding: 0 20px;
        }
        .total-label {
            font-size: 14px;
            color: #666;
            margin-bottom: 5px;
        }
        .total-value {
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
            font-family: 'Courier New', monospace;
        }
        .total-item:not(:last-child) {
            border-right: 1px solid #ddd;
        }
    </style>
    <script>
        let totalValue = 0;
        let totalTransactions = 0;
        let averageValue = 0;

        function formatNumber(num) {
            return new Intl.NumberFormat('pt-BR', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }).format(num);
        }

        function updateTotals(transactions) {
            totalValue = 0;
            totalTransactions = transactions.length;
            
            transactions.forEach(tx => {
                // Remove vírgulas e converte para número
                const value = parseFloat(tx[2].replace(/,/g, ''));
                totalValue += value;
            });
            
            averageValue = totalTransactions > 0 ? totalValue / totalTransactions : 0;

            document.getElementById('totalValue').textContent = formatNumber(totalValue);
            document.getElementById('totalTransactions').textContent = totalTransactions;
            document.getElementById('averageValue').textContent = formatNumber(averageValue);
        }

        function updateTable() {
            fetch('/get_transactions')
                .then(response => response.json())
                .then(data => {
                    const tbody = document.querySelector('tbody');
                    tbody.innerHTML = '';
                    
                    data.forEach(tx => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${tx[0]}</td>
                            <td><a href="https://etherscan.io/tx/${tx[1]}" target="_blank">${tx[1]}</a></td>
                            <td class="valor">${tx[2]}</td>
                        `;
                        tbody.insertBefore(row, tbody.firstChild);
                    });
                    
                    document.getElementById('lastUpdate').textContent = 
                        new Date().toLocaleTimeString('pt-BR', {
                            hour: '2-digit',
                            minute: '2-digit',
                            second: '2-digit',
                            hour12: false
                        });

                    updateTotals(data);
                })
                .catch(error => console.error('Erro:', error));
        }

        // Atualiza a cada 5 segundos
        setInterval(updateTable, 5000);
        
        // Primeira atualização
        document.addEventListener('DOMContentLoaded', updateTable);
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Monitor de Transações USDT</h1>
            <div class="status">
                Última atualização: <span id="lastUpdate">--:--:--</span>
            </div>
        </div>

        <div class="totals">
            <div class="total-item">
                <div class="total-label">Total USDT</div>
                <div class="total-value">$<span id="totalValue">0.00</span></div>
            </div>
            <div class="total-item">
                <div class="total-label">Total Transações</div>
                <div class="total-value"><span id="totalTransactions">0</span></div>
            </div>
            <div class="total-item">
                <div class="total-label">Média por Transação</div>
                <div class="total-value">$<span id="averageValue">0.00</span></div>
            </div>
        </div>

        <table>
            <thead>
                <tr>
                    <th>Data/Hora</th>
                    <th>Hash da Transação</th>
                    <th>Valor (USDT)</th>
                </tr>
            </thead>
            <tbody>
            </tbody>
        </table>
    </div>
</body>
</html>
"""

# Cria o diretório templates se não existir
if not os.path.exists('templates'):
    os.makedirs('templates')

# Cria o arquivo de template
with open('templates/index.html', 'w') as f:
    f.write(html_template)

class TransactionMonitor:
    def __init__(self):
        self.contract = w3.eth.contract(
            address=USDT_CONTRACT,
            abi=USDT_ABI
        )
        self.latest_block = w3.eth.block_number

    def handle_transfer_event(self, event):
        try:
            value = event.args.value / 1e6
            if value >= MIN_VALUE:
                tx_hash = event.transactionHash.hex()
                timestamp = get_br_datetime()
                
                print(f"\nNova transação detectada:")
                print(f"Data/Hora: {timestamp}")
                print(f"Hash: {tx_hash}")
                print(f"Valor: {value:,.2f} USDT")
                
                save_to_csv(timestamp, tx_hash, value)

        except Exception as e:
            print(f"Erro ao processar evento: {e}")

    def monitor_transfers(self):
        print(f"Monitorando transferências USDT maiores que {MIN_VALUE:,} USDT...")
        
        while True:
            try:
                transfer_filter = self.contract.events.Transfer.create_filter(
                    fromBlock=self.latest_block
                )
                
                for event in transfer_filter.get_new_entries():
                    self.handle_transfer_event(event)
                
                self.latest_block = w3.eth.block_number
                time.sleep(5)
                
            except Exception as e:
                print(f"Erro no monitoramento: {e}")
                time.sleep(5)
                continue

def start_flask():
    app.run(host='0.0.0.0', port=12701)

def main():
    flask_thread = Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    monitor = TransactionMonitor()
    try:
        monitor.monitor_transfers()
    except KeyboardInterrupt:
        print("\nMonitoramento interrompido pelo usuário.")

if __name__ == "__main__":
    if not w3.is_connected():
        print("Erro: Não foi possível conectar à rede Ethereum")
        exit(1)

    print("Conectado à rede Ethereum")
    print(f"Último bloco: {w3.eth.block_number}")
    
    main()