# Monitor de Transações USDT Ethereum

Um sistema de monitoramento em tempo real de transações USDT na rede Ethereum com interface web interativa. O sistema monitora transferências acima de um valor mínimo configurável e exibe as informações em uma interface web amigável.

## Tecnologias Utilizadas

- Python 3.8+
- Web3.py
- Flask
- HTML/CSS/JavaScript
- Infura API

## Pré-requisitos

- Python 3.8 ou superior
- Conta Infura com URL da API da rede Ethereum
- Conexão com internet

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/juniorVOPJ/UsdtEthTxScanner.git
    cd UsdtEthTxScanner
    ```

2. Crie um ambiente virtual e ative-o:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    # ou
    venv\Scripts\activate  # Windows
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Crie um arquivo .env na raiz do projeto:
    ```
    INFURA_URL=https://mainnet.infura.io/v3/sua-chave-infura
    MIN_USDT_VALUE=100000
    ```

## Uso

1. Ative o ambiente virtual (se ainda não estiver ativo)

2. Execute o programa:
    ```bash
    python monitor.py
    ```

3. Acesse a interface web:
   - Abra seu navegador
   - Acesse http://localhost:12701

## Funcionalidades

- Monitoramento em tempo real de transações USDT na rede Ethereum
- Interface web responsiva com atualizações automáticas
- Rastreamento de transações acima do valor mínimo configurado
- Exibição de estatísticas (total, média, número de transações)
- Links diretos para o Etherscan para cada transação
- Armazenamento de transações em arquivo CSV
- Fuso horário configurado para Brasil (São Paulo)

## Configurações

- INFURA_URL: URL da API Infura (obrigatório)
- MIN_USDT_VALUE: Valor mínimo em USDT para monitorar (padrão: 100000)

## Visualização de Dados

A interface web inclui:
- Lista de transações em tempo real
- Valor total de USDT movimentado
- Número total de transações
- Média de valor por transação
- Atualização automática a cada 5 segundos

## Segurança

- Nunca compartilhe seu arquivo .env
- Mantenha sua chave Infura em segredo
- Use ambiente virtual para isolamento de dependências

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.