import logging
import grpc
import moeda_pb2
import moeda_pb2_grpc


# Função principal que coleta as entradas do usuário e solicita a conversão ao servidor
def run():
    # Exibe ao usuário as moedas válidas
    print("\nMoedas válidas:" +
          "\nAUD, BGN, BRL, CAD, CHF, CNY, CZK, DKK, EUR," +
          "\nGBP, HKD, HRK, HUF, IDR, ILS, INR, ISK, JPY," +
          "\nKRW, MXN, MYR, NOK, NZD, PHP, PLN, RON, RUB," +
          "\nSEK, SGD, THB, TRY, USD, ZAR")

    # Solicita ao usuário a moeda de origem e o valor de origem
    moeda_origem = input("\nDigite a moeda de origem: ").upper()
    try:
        valor_origem = float(input("Digite o valor de origem: "))
    except ValueError:
        # Trata erro caso o valor de origem não seja um número válido
        print("\nErro: O valor de origem deve ser um número válido.")
        return
    
    # Solicita ao usuário a moeda de destino
    moeda_destino = input("Digite a moeda de destino: ").upper()

    try:
        # Abre uma conexão gRPC com o servidor
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = moeda_pb2_grpc.MoedaStub(channel)
            try:
                # Realiza a solicitação de conversão ao servidor
                reply = stub.converter(moeda_pb2.ConverterRequest(
                    moeda_origem=moeda_origem, valor_origem=valor_origem, moeda_destino=moeda_destino))
                
                # Exibe o resultado da conversão
                print(
                    f'\n{moeda_origem} {reply.valor_origem} = {moeda_destino} {reply.valor_destino}')

            # Tratamento de possíveis erros ao chamar o servidor
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                    print(f"\nErro de argumento inválido: {e.details()}")
                elif e.code() == grpc.StatusCode.INTERNAL:
                    print(f"\nErro interno do servidor: {e.details()}")
                else:
                    print(f"\nErro inesperado: {e.code()} - {e.details()}")

    # Tratamento de erro em caso de falha de conexão com o servidor
    except grpc.RpcError as e:
        print("\nErro de conexão com o servidor.")
        logging.error(f"Erro ao tentar conectar com o servidor: {e}")


if __name__ == "__main__":
    logging.basicConfig()
    run()
