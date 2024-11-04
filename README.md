# Conversor de Moedas com gRPC

Este projeto implementa um serviço de conversão de moedas utilizando gRPC, permitindo ao cliente realizar conversões entre diversas moedas suportadas.

## Estrutura do Projeto

- **`moeda.proto`**: Arquivo de definição gRPC que define o serviço `Moeda` e o método `Converter`, usado para conversão de moedas.
- **`moeda_server.py`**: Servidor gRPC que implementa o serviço de conversão. O servidor utiliza a API `freecurrencyapi` para obter taxas de câmbio em tempo real.
- **`moeda_client.py`**: Cliente gRPC que se conecta ao servidor e solicita a conversão de uma moeda de origem para uma moeda de destino.

## Funcionalidades

O serviço permite a conversão entre as seguintes moedas:
AUD, BGN, BRL, CAD, CHF, CNY, CZK, DKK, EUR, GBP, HKD, HRK, HUF, IDR, ILS, INR, ISK, JPY, KRW, MXN, MYR, NOK, NZD, PHP, PLN, RON, RUB, SEK, SGD, THB, TRY, USD, ZAR.

### Requisitos

- Python 3.6 ou superior
- `grpcio` e `grpcio-tools` para gRPC
- `freecurrencyapi` para consultar taxas de câmbio

### Instalação

1. Clone o repositório.
2. Instale as dependências:
   ```bash
   pip install grpcio grpcio-tools freecurrencyapi
   ```

3. Gere os arquivos gRPC a partir do arquivo `.proto` (caso necessário):
   ```bash
   python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. moeda.proto
   ```

### Uso

1. Inicie o servidor:
   ```bash
   python moeda_server.py
   ```

   O servidor estará ativo na porta `50051`.

2. Em outro terminal, execute o cliente:
   ```bash
   python moeda_client.py
   ```

   O cliente solicitará ao usuário a moeda de origem, o valor e a moeda de destino. Após enviar a requisição, exibirá o valor convertido.

### Configuração em Máquinas Diferentes

Se o **cliente** e o **servidor** estiverem em máquinas diferentes, siga estas etapas adicionais:

1. **Servidor**: Certifique-se de que o servidor está configurado para aceitar conexões de outras máquinas. No código do servidor (`moeda_server.py`), verifique se a linha `server.add_insecure_port("[::]:50051")` está configurada corretamente. A configuração `[::]:50051` permite que o servidor aceite conexões de qualquer endereço IP.

2. **Cliente**: Atualize o endereço do servidor no código do cliente (`moeda_client.py`).
   - Substitua `'localhost:50051'` pelo endereço IP da máquina do servidor. Por exemplo:
     ```python
     with grpc.insecure_channel('ENDEREÇO_IP_DO_SERVIDOR:50051') as channel:
     ```
   - **Exemplo**: Se o servidor tiver o endereço IP `192.168.1.10`, o código deve ser:
     ```python
     with grpc.insecure_channel('192.168.1.10:50051') as channel:
     ```

3. **Firewall e Redes**: Verifique se a porta `50051` está aberta no firewall da máquina do servidor e se não há restrições de rede que impeçam a conexão entre o cliente e o servidor.

### Exemplo de Execução

- **Servidor**:
  ```
  Servidor iniciado, escutando em 50051
  ```

- **Cliente**:
  ```
  Moedas válidas:
  AUD, BGN, BRL, CAD, CHF, CNY, CZK, DKK, EUR,
  GBP, HKD, HRK, HUF, IDR, ILS, INR, ISK, JPY,
  KRW, MXN, MYR, NOK, NZD, PHP, PLN, RON, RUB,
  SEK, SGD, THB, TRY, USD, ZAR

  Digite a moeda de origem: USD
  Digite o valor de origem: 100
  Digite a moeda de destino: EUR

  USD 100.0 = EUR 85.73
  ```

### Estrutura da API gRPC

- **Serviço**: `Moeda`
  - **Método**: `Converter`
    - **Requisição** (`ConverterRequest`):
      - `moedaOrigem` (string): Código da moeda de origem (ex: USD).
      - `valorOrigem` (double): Valor a ser convertido.
      - `moedaDestino` (string): Código da moeda de destino (ex: EUR).
    - **Resposta** (`ConverterReply`):
      - `valorOrigem` (double): Valor original fornecido na moeda de origem.
      - `valorDestino` (double): Valor convertido na moeda de destino.

### Tratamento de Erros

- **Moeda inválida**: Se a moeda de origem ou destino não for válida, o servidor retorna um erro `INVALID_ARGUMENT`.
- **Falha de API**: Em caso de erro na conexão com a API de câmbio, o servidor retorna um erro `INTERNAL`.
- **Erro inesperado**: Caso ocorra uma exceção não prevista, o servidor retorna um erro `INTERNAL` com a descrição do problema.

### Licença

Este projeto é distribuído sob a licença MIT.