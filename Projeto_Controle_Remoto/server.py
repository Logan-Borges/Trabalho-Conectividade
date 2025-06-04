import socket
import threading
import json

clients = {}  # nome_dispositivo: conexão

def handle_client(conn, addr):
    nome = conn.recv(1024).decode()
    clients[nome] = conn
    print(f"[SERVIDOR] {nome} conectado de {addr}")

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
    except:
        pass
    finally:
        del clients[nome]
        conn.close()
        print(f"[SERVIDOR] {nome} desconectado")

def handle_panel(conn):
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            msg = json.loads(data.decode())

            destino = msg['destino']
            if destino in clients:
                clients[destino].send(data)
                resposta = clients[destino].recv(1024)
                conn.send(resposta)
            else:
                erro = {"tipo": "erro", "mensagem": f"Dispositivo '{destino}' não encontrado"}
                conn.send(json.dumps(erro).encode())
    except:
        pass
    finally:
        conn.close()
        print("[SERVIDOR] Painel desconectado")

def main():
    host = 'localhost'
    port = 12345
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print("[SERVIDOR] Servidor iniciado em localhost:12345")

    while True:
        conn, addr = server.accept()
        tipo = conn.recv(1024).decode()

        if tipo == 'painel':
            print("[SERVIDOR] Painel conectado")
            threading.Thread(target=handle_panel, args=(conn,)).start()
        else:
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()