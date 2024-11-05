import math
from concurrent import futures
import logging
import freecurrencyapi
import grpc
import moeda_pb2
import moeda_pb2_grpc

# Chave de API para acessar o serviço de câmbio
API_KEY = 'fca_live_PejqVyXV4C9giEKy2roO9m4uTpkiB1IUgnumO3js'


class Moeda(moeda_pb2_grpc.MoedaServicer):
    # Método para converter o valor de uma moeda de origem para uma moeda de destino
    def converter(self, request, context):
        try:
            # Obtém os parâmetros do cliente
            moeda_origem = request.moeda_origem
            valor_origem = request.valor_origem
            moeda_destino = request.moeda_destino

            # Lista de moedas aceitas pela aplicação
            moedas_validas = ["AUD", "BGN", "BRL", "CAD", "CHF", "CNY", "CZK", "DKK", "EUR",
                              "GBP", "HKD", "HRK", "HUF", "IDR", "ILS", "INR", "ISK", "JPY",
                              "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PLN", "RON", "RUB",
                              "SEK", "SGD", "THB", "TRY", "USD", "ZAR"]

            # Verifica se as moedas de origem e destino são válidas
            if moeda_origem not in moedas_validas:
                context.set_details("Moeda de origem inválida.")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return moeda_pb2.ConverterReply()

            if moeda_destino not in moedas_validas:
                context.set_details("Moeda de destino inválida.")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return moeda_pb2.ConverterReply()

            # Cria um cliente para acessar a API de câmbio
            client = freecurrencyapi.Client(API_KEY)
            try:
                # Obtém as moedas e as taxas de câmbio da API
                moedas = client.currencies(
                    currencies=[moeda_origem, moeda_destino])['data']
                taxas_cambio = client.latest()['data']
            except Exception as e:
                # Tratamento de erro caso ocorra falha ao conectar com a API
                context.set_details("Erro ao conectar com a API de câmbio.")
                context.set_code(grpc.StatusCode.INTERNAL)
                return moeda_pb2.ConverterReply()

            # Trunca o valor de origem para o número adequado de casas decimais
            valor_origem = self.truncar_float(
                valor_origem, moedas[moeda_origem]['decimal_digits'])
            
            # Realiza a conversão de moedas usando as taxas de câmbio
            valor_destino = (
                valor_origem / taxas_cambio[moeda_origem] * taxas_cambio[moeda_destino])
            
            # Ajusta o valor de destino para o número correto de casas decimais
            valor_destino = self.truncar_float(
                valor_destino, moedas[moeda_destino]['decimal_digits'])

            # Retorna a resposta com os valores convertidos
            return moeda_pb2.ConverterReply(valor_origem=valor_origem, valor_destino=valor_destino)
        except Exception as e:
            # Tratamento de erros inesperados durante a conversão
            logging.error(f"Erro inesperado: {e}")
            context.set_details("Erro inesperado durante a conversão.")
            context.set_code(grpc.StatusCode.INTERNAL)
            return moeda_pb2.ConverterReply()

    # Método auxiliar para truncar um float com um número de casas decimais especificado
    def truncar_float(self, valor, escala):
        return math.trunc(valor * (10 ** escala)) / (10 ** escala)

# Configura e inicia o servidor gRPC
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
