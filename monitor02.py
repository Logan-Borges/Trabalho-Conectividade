import socket
import sys
import threading

#--------------------------------------------------------------
# FUNÇÕES
def TrataSensor(conn, addr):
    print('uma thread foi criada para:', addr)

    # O sensor deve enviar seu ID apos a conexao
    sensor = conn.recv(10)
    SENSORES[sensor] = conn

    # usar metodo getpeername para obter o endereço IP e a porta do sensor
    print('sensor ', sensor, ' registrado no socket', conn.getpeername())

    while True:
        data = conn.recv(100)
        print('sensor ', sensor, 'enviou ', data)

        if not data:
            break

    conn.close()
    print('sensor', sensor, 'encerrou')

#--------------------------------------------------------------
# PROGRAMA PRINCIPAL

HOST = ''               # ANY_IP = todos os IPs do HOST
SENSORES={}     # lista de sensores conectados
CONSOLE=None  # conexao com o console remoto

PORTA = int(input('Entre com a porta do servidor: '))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((HOST, PORTA))
except:
   print('# erro de bind')
   sys.exit()
hostname = socket.gethostname()
hostip = socket.gethostbyname(hostname)
print('host: {} ip: {}'.format(hostname, hostip))

s.listen(2)
print('aguardando conexoes em ', PORTA)

#--------------------------------------------------------------
# LOOP para tratar clientes
while True:
    conn, addr = s.accept()
    print('recebi uma conexao do sensor ', addr)

    t = threading.Thread( target=TrataSensor, args=(conn,addr,))
    t.start()

print('o servidor encerrou')
s.close()