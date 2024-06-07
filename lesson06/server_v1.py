#!/bin/python3
import socket
import threading
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("log"), logging.StreamHandler()])

# Данные для подключения
HOST = '127.0.0.1'
PORT = 55555

# Запуск сервера
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Позволяет повторно использовать адрес
server.bind((HOST, PORT))
server.listen()

# Списки для клиентов и их псевдонимов
clients = []
nicknames = []

# Отправка сообщений всем подключенным клиентам
def broadcast(message, _client=None):
    for client in clients:
        if client != _client:
            try:
                client.send(message)
            except:
                remove_client(client)

# Удаление и закрытие клиентов
def remove_client(client):
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        client.close()
        nickname = nicknames[index]
        broadcast(f'{nickname} left!'.encode('utf-8'))
        nicknames.remove(nickname)
        logging.info(f'{nickname} has left the chat.')

# Обработка сообщений от клиентов
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if message:
                logging.info(f"Received message: {message.decode('utf-8')}")
                broadcast(message, client)
        except:
            remove_client(client)
            break

# Функция приема новых подключений
def receive():
    while True:
        client, address = server.accept()
        logging.info(f"Connected with {str(address)}")

        # Запрос псевдонима у нового клиента
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        nicknames.append(nickname)
        clients.append(client)

        logging.info(f"Nickname is {nickname}")
        broadcast(f"{nickname} joined!".encode('utf-8'))
        client.send('Connected to server!'.encode('utf-8'))

        # Создание нового потока для обработки сообщений от клиента
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Запуск сервера
if __name__ == "__main__":
    logging.info("Server is listening...")
    receive()
ll