import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = input('Entre com o IP do servidor: ')
PORTA = int(input('Entre com a porta do servidor: '))
ID = input('Entre com o ID do sensor: ')

try:
    s.connect((IP, PORTA))
except:
    print('erro de conexao')

# Envia o ID automaticamente após a conexão
s.send(bytes(ID, 'utf-8'))

while True:
    try:
        print('digite o texto a ser transmitido ou linha vazia para encerrar o programa')
        line = input()
        if not line:
            print('linha vazia encerra o programa')
            break
    except:
        print('programa abortado com CTRL+C')
    data = bytes(line, 'utf-8')
    tam = s.send(data)

    print('enviei ', tam, 'bytes')
    print(data)

print('cliente encerrado')