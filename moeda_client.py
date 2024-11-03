import logging
import grpc
import moeda_pb2
import moeda_pb2_grpc


def run():
    print("\nMoedas válidas:" +
          "\nAUD, BGN, BRL, CAD, CHF, CNY, CZK, DKK, EUR," +
          "\nGBP, HKD, HRK, HUF, IDR, ILS, INR, ISK, JPY," +
          "\nKRW, MXN, MYR, NOK, NZD, PHP, PLN, RON, RUB," +
          "\nSEK, SGD, THB, TRY, USD, ZAR")

    moedaOrigem = input("\nDigite a moeda de origem: ").upper()
    try:
        valorOrigem = float(input("Digite o valor de origem: "))
    except ValueError:
        print("\nErro: O valor de origem deve ser um número válido.")
        return
    moedaDestino = input("Digite a moeda de destino: ").upper()

    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = moeda_pb2_grpc.MoedaStub(channel)
            try:
                reply = stub.Converter(moeda_pb2.ConverterRequest(
                    moedaOrigem=moedaOrigem, valorOrigem=valorOrigem, moedaDestino=moedaDestino))
                print(f'\n{moedaOrigem} {reply.valorOrigem} = {
                    moedaDestino} {reply.valorDestino}')
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                    print(f"\nErro de argumento inválido: {e.details()}")
                elif e.code() == grpc.StatusCode.INTERNAL:
                    print(f"\nErro interno do servidor: {e.details()}")
                else:
                    print(f"\nErro inesperado: {e.code()} - {e.details()}")
    except grpc.RpcError as e:
        print("\nErro de conexão com o servidor.")
        logging.error(f"Erro ao tentar conectar com o servidor: {e}")


if __name__ == "__main__":
    logging.basicConfig()
    run()
