import socket, threading


nickname = input("Выберите имя пользователя: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Инициализация клиетского сокета
client.connect( ('127.0.0.1', 7976) )  # Клиентский сокет конектится к серверному сокету


def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICKNAME':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("Ошибка!")
            client.close()
            break


def write():
    while True:  # Вывод сообщений в чат
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=receive)  # Получение всех сообщений
receive_thread.start()
write_thread = threading.Thread(target=write)  # Отправка всех сообщений
write_thread.start()

