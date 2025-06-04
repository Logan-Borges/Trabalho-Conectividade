import socket
import json

def main():
    nome = input("Nome do dispositivo: ")
    estado = "desligado"

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 12345))
    client.send(nome.encode())  # Primeiro envio: nome do dispositivo

    while True:
        try:
            data = client.recv(1024)
            if not data:
                break

            msg = json.loads(data.decode())
            comando = msg['comando']

            if comando == "ligar":
                estado = "ligado"
            elif comando == "desligar":
                estado = "desligado"

            resposta = {
                "tipo": "resposta",
                "dispositivo": nome,
                "estado": estado
            }
            client.send(json.dumps(resposta).encode())

        except:
            break

    client.close()

if __name__ == "__main__":
    main()