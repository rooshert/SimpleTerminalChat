import socket, threading  # Импорт библиотек

host = '127.0.0.1'  # Локальный хост компьютера
port = 7976  # Выбор незарезервированного порта

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Инициализация сокета
server.bind( (host, port) )  # Назначение хоста и порта к сокету
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} покинул чат!'.format(nickname).encode('utf-8'))
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server.accept()

        client.send('NICKNAME'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        print('USER %s добавлен на SERVER=[%s / %s]' % (nickname, host, port))

        broadcast("{} присоединился!".format(nickname).encode('utf-8'))
        # client.send('Подключён к серверу!'.encode('utf-8'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print('SERVER=[%s / %s] was start!' % (host, port))
receive()

