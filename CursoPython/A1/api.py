from threading import Thread  # Multithreading
import socket as ss  # ss = socket (alias)


class Server:
    def __init__(self):
        self.routes = {
            "/pato": {
                "data_type": "text",
                "data": "pato"
            },
            "/batata": {
                "data_type": "text",
                "data": "<h1>cuzin</h1>"
            }
        }
        self.socket = self.start_server()
        self.accept_clients()

    def recv_data(self, client: ss.socket) -> str:
        while True:
            package = client.recv(1024)
            if package:
                return package.decode("utf-8")

    def handle_client(self, client: ss.socket, address: tuple[str, int]):
        print(f"Client {address[0]} conectado!")
        request = self.recv_data(client)
        route = self.handle_request(request)

        print([route,])

        if route in self.routes.keys():
            data_type = self.routes[route]["data_type"]
            data = self.routes[route]["data"]
            self.send_data(client, data_type, data)
        else:
            self.send_data(client, "text", "Route not found!")
        client.close()

    def send_data(self, client: ss.socket, data_type: str, data: str):
        if data_type == "html":
            msg = f"HTTP/1.1 200 OK\r\nContent-Type text/html\r\n\r\n{data}"
        elif data_type == "text":
            msg = f"HTTP/1.1 200 OK\r\n\r\n{data}"

        client.send(msg.encode("utf-8"))

    def handle_request(self, request: str) -> str:
        final_route = request.index(" HTTP/1.1")
        return request[4:final_route]

    def accept_clients(self):
        # Aceitando clientes com o nosso socket self.socket usando o metodo accept().
        # Após usar o metodo accept() ele não irá sair da linha do accept() até que um cliente se conecte.
        # Receberemos como retorno a informação: socket do cliente conectado e endereço do cliente.
        while True:
            client, address = self.socket.accept()
            Thread(target=self.handle_client, args=[client, address]).start()
            print(f"Client {address[0]} conectado!")

    def start_server(self):
        # Criando objeto de socket com a camada de rede e especificando:
        # - Adress family (familia de endereço) [PROTOCOLO DE REDE]
        # - TCP (SOCK_STREAM) [PROTOCOLSO DE TRANSPORTE]
        socket = ss.socket(ss.AF_INET, ss.SOCK_STREAM)

        # (De Paula) -> Pegar ipv4 automaticamente
        ip_address = ss.gethostbyname(ss.gethostname())

        # - Hospendando nosso socket em um endereço para que ele possa ser encontrado por outros sockets.
        socket.bind((ip_address, 23230))

        # - Disponibilizando acessa a placa de rede.
        socket.listen(5)

        print("Servidor iniciado!")

        return socket


Server = Server()
