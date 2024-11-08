# Conversor de Moedas com gRPC

Este projeto implementa um serviço de conversão de moedas utilizando gRPC, permitindo ao cliente realizar conversões entre diversas moedas suportadas.

## Introdução à Arquitetura gRPC

gRPC é um framework de chamada de procedimento remoto (RPC) de alta performance, desenvolvido pelo Google. Ele permite a comunicação eficiente entre clientes e servidores através de protocolos baseados em HTTP/2, facilitando a troca de dados estruturados em diversos idiomas e sistemas operacionais.

### Funcionamento do gRPC na Aplicação

1. **Definição do Serviço com `.proto`**:
   - No arquivo `moeda.proto`, definimos o serviço `Moeda` e o método `converter`. Esse arquivo `.proto` é utilizado para gerar os códigos gRPC necessários para o cliente e o servidor, garantindo que ambos sigam o mesmo contrato de comunicação.
   - A definição inclui:
     - `ConverterRequest`: mensagem de requisição contendo a moeda de origem, valor e moeda de destino.
     - `ConverterReply`: mensagem de resposta com o valor original e o valor convertido.

2. **Servidor gRPC (`moeda_server.py`)**:
   - O servidor implementa a lógica do serviço `Moeda`, com o método `converter` responsável por calcular a conversão de moedas.
   - Quando o cliente faz uma requisição, o servidor recebe os dados, realiza a consulta das taxas de câmbio via API e retorna o valor convertido.
   - A arquitetura do servidor gRPC permite que múltiplas requisições sejam processadas simultaneamente, utilizando uma `ThreadPoolExecutor`.

3. **Cliente gRPC (`moeda_client.py`)**:
   - O cliente configura um canal de comunicação com o servidor (`localhost:50051` por padrão) e faz uma chamada ao método `converter`.
   - A chamada envia uma `ConverterRequest` e espera uma `ConverterReply` como resposta, exibindo o valor convertido ao usuário.

### Vantagens do gRPC

- **Desempenho**: A comunicação gRPC utiliza HTTP/2, permitindo multiplexação de requisições, compressão e transmissão de dados binários, o que o torna mais eficiente do que protocolos baseados em texto como JSON/REST.
- **Definição Estruturada**: O uso de arquivos `.proto` garante uma definição de API rigorosa e compartilhada entre cliente e servidor, minimizando erros de incompatibilidade.
- **Escalabilidade**: gRPC suporta balanceamento de carga, chamadas paralelas e manuseio eficiente de erros, tornando-o adequado para sistemas distribuídos de larga escala.

Essa arquitetura garante que a aplicação seja eficiente, robusta e escalável para cenários em que cliente e servidor estejam na mesma máquina ou em sistemas distintos.


## Estrutura do Projeto

- **`moeda.proto`**: Arquivo de definição gRPC que define o serviço `Moeda` e o método `converter`, usado para conversão de moedas.
- **`moeda_server.py`**: Servidor gRPC que implementa o serviço de conversão. O servidor utiliza a API `freecurrencyapi` para obter taxas de câmbio em tempo real.
- **`moeda_client.py`**: Cliente gRPC que se conecta ao servidor e solicita a conversão de uma moeda de origem para uma moeda de destino.

## Funcionalidades

O serviço permite a conversão entre as seguintes moedas:

<table>
  <tr>
    <td>
      <ul>
        <li><code>AUD - Dólar australiano</code></li>
        <li><code>BRL - Real brasileiro</code></li>
        <li><code>CHF - Franco suíço</code></li>
        <li><code>CZK - Coroa checa</code></li>
        <li><code>EUR - Euro</code></li>
        <li><code>HKD - Dólar de Hong Kong</code></li>
        <li><code>HUF - Forint húngaro</code></li>
        <li><code>ILS - Novo shekel israelita</code></li>
        <li><code>ISK - Coroa islandesa</code></li>
        <li><code>KRW - Won coreano</code></li>
        <li><code>MYR - Ringgit malaio</code></li>
        <li><code>NZD - Dólar neozelandês</code></li>
        <li><code>PLN - Zloti polaco</code></li>
        <li><code>RUB - Rublo russo</code></li>
        <li><code>SGD - Dólar de Singapura</code></li>
        <li><code>TRY - Lira turca</code></li>
        <li><code>ZAR - Rand sul-africano</code></li>
      </ul>
    </td>
    <td>
      <ul>
        <li><code>BGN - Leve búlgaro</code></li>
        <li><code>CAD - Dólar canadiano</code></li>
        <li><code>CNY - Yuan Renmimbi chinês</code></li>
        <li><code>DKK - Coroa dinamarquesa</code></li>
        <li><code>GBP - Libra esterlina britânica</code></li>
        <li><code>HRK - Kuna croata</code></li>
        <li><code>IDR - Rupia indonésia</code></li>
        <li><code>INR - Rupia indiana</code></li>
        <li><code>JPY - Iene japonês</code></li>
        <li><code>MXN - Peso mexicano</code></li>
        <li><code>NOK - Coroa norueguesa</code></li>
        <li><code>PHP - Peso filipino</code></li>
        <li><code>RON - Novo leu romeno</code></li>
        <li><code>SEK - Coroa sueca</code></li>
        <li><code>THB - Baht tailandês</code></li>
        <li><code>USD - Dólar norte-americano</code></li>
      </ul>
    </td>
  </tr>
</table>

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
  - **Método**: `converter`
    - **Requisição** (`ConverterRequest`):
      - `moeda_origem` (string): Código da moeda de origem (ex: USD).
      - `valor_origem` (double): Valor a ser convertido.
      - `moeda_destino` (string): Código da moeda de destino (ex: EUR).
    - **Resposta** (`ConverterReply`):
      - `valor_origem` (double): Valor original fornecido na moeda de origem.
      - `valor_destino` (double): Valor convertido na moeda de destino.

### Tratamento de Erros

- **Moeda inválida**: Se a moeda de origem ou destino não for válida, o servidor retorna um erro `INVALID_ARGUMENT`.
- **Falha de API**: Em caso de erro na conexão com a API de câmbio, o servidor retorna um erro `INTERNAL`.
- **Erro inesperado**: Caso ocorra uma exceção não prevista, o servidor retorna um erro `INTERNAL` com a descrição do problema.