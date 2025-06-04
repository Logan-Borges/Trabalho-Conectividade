import socket
import json

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 12345))
    client.send('painel'.encode())  # Indica que é painel

    print("=== PAINEL DE CONTROLE ===")
    print("Comandos: ligar, desligar, status")
    
    while True:
        destino = input("\nDispositivo destino: ")
        comando = input("Comando (ligar/desligar/status): ").lower()

        msg = {
            "tipo": "comando",
            "destino": destino,
            "comando": comando
        }

        client.send(json.dumps(msg).encode())
        resposta = client.recv(1024)
        print("[RESPOSTA]", resposta.decode())

if __name__ == "__main__":
    main()