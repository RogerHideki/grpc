from concurrent import futures
import logging
import grpc
import moeda_pb2
import moeda_pb2_grpc
import freecurrencyapi
import math

API_KEY = 'fca_live_PejqVyXV4C9giEKy2roO9m4uTpkiB1IUgnumO3js'


class Moeda(moeda_pb2_grpc.MoedaServicer):
    def Converter(self, request, context):
        try:
            moedaOrigem = request.moedaOrigem
            valorOrigem = request.valorOrigem
            moedaDestino = request.moedaDestino

            moedasValidas = ["AUD", "BGN", "BRL", "CAD", "CHF", "CNY", "CZK", "DKK", "EUR",
                             "GBP", "HKD", "HRK", "HUF", "IDR", "ILS", "INR", "ISK", "JPY",
                             "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PLN", "RON", "RUB",
                             "SEK", "SGD", "THB", "TRY", "USD", "ZAR"]

            if moedaOrigem not in moedasValidas:
                context.set_details("Moeda de origem inválida.")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return moeda_pb2.ConverterReply()

            if moedaDestino not in moedasValidas:
                context.set_details("Moeda de destino inválida.")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return moeda_pb2.ConverterReply()

            client = freecurrencyapi.Client(API_KEY)
            try:
                moedas = client.currencies(
                    currencies=[moedaOrigem, moedaDestino])['data']
                taxasCambio = client.latest()['data']
            except Exception as e:
                context.set_details("Erro ao conectar com a API de câmbio.")
                context.set_code(grpc.StatusCode.INTERNAL)
                return moeda_pb2.ConverterReply()

            valorOrigem = self.truncarFloat(
                valorOrigem, moedas[moedaOrigem]['decimal_digits'])
            valorDestino = (
                valorOrigem / taxasCambio[moedaOrigem] * taxasCambio[moedaDestino])
            valorDestino = self.truncarFloat(
                valorDestino, moedas[moedaDestino]['decimal_digits'])

            return moeda_pb2.ConverterReply(valorOrigem=valorOrigem, valorDestino=valorDestino)
        except Exception as e:
            logging.error(f"Erro inesperado: {e}")
            context.set_details("Erro inesperado durante a conversão.")
            context.set_code(grpc.StatusCode.INTERNAL)
            return moeda_pb2.ConverterReply()

    def truncarFloat(self, valor, escala):
        return math.trunc(valor * (10 ** escala)) / (10 ** escala)


def serve():
    porta = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    moeda_pb2_grpc.add_MoedaServicer_to_server(Moeda(), server)
    server.add_insecure_port("[::]:" + porta)
    server.start()
    print("Servidor iniciado, escutando em " + porta)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
