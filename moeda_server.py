import math
from concurrent import futures
import logging
import freecurrencyapi
import grpc
import moeda_pb2
import moeda_pb2_grpc

API_KEY = 'fca_live_PejqVyXV4C9giEKy2roO9m4uTpkiB1IUgnumO3js'


class Moeda(moeda_pb2_grpc.MoedaServicer):
    def converter(self, request, context):
        try:
            moeda_origem = request.moeda_origem
            valor_origem = request.valor_origem
            moeda_destino = request.moeda_destino

            moedas_validas = ["AUD", "BGN", "BRL", "CAD", "CHF", "CNY", "CZK", "DKK", "EUR",
                              "GBP", "HKD", "HRK", "HUF", "IDR", "ILS", "INR", "ISK", "JPY",
                              "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PLN", "RON", "RUB",
                              "SEK", "SGD", "THB", "TRY", "USD", "ZAR"]

            if moeda_origem not in moedas_validas:
                context.set_details("Moeda de origem inválida.")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return moeda_pb2.ConverterReply()

            if moeda_destino not in moedas_validas:
                context.set_details("Moeda de destino inválida.")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return moeda_pb2.ConverterReply()

            client = freecurrencyapi.Client(API_KEY)
            try:
                moedas = client.currencies(
                    currencies=[moeda_origem, moeda_destino])['data']
                taxas_cambio = client.latest()['data']
            except Exception as e:
                context.set_details("Erro ao conectar com a API de câmbio.")
                context.set_code(grpc.StatusCode.INTERNAL)
                return moeda_pb2.ConverterReply()

            valor_origem = self.truncar_float(
                valor_origem, moedas[moeda_origem]['decimal_digits'])
            valor_destino = (
                valor_origem / taxas_cambio[moeda_origem] * taxas_cambio[moeda_destino])
            valor_destino = self.truncar_float(
                valor_destino, moedas[moeda_destino]['decimal_digits'])

            return moeda_pb2.ConverterReply(valor_origem=valor_origem, valor_destino=valor_destino)
        except Exception as e:
            logging.error(f"Erro inesperado: {e}")
            context.set_details("Erro inesperado durante a conversão.")
            context.set_code(grpc.StatusCode.INTERNAL)
            return moeda_pb2.ConverterReply()

    def truncar_float(self, valor, escala):
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
