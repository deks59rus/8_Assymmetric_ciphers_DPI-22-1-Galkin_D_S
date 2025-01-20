import socket
import logging

# Настройка логирования
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Создаем сокет и привязываем его к адресу и порту
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 65432))
    server_socket.listen(1)
    logging.info("Сервер запущен и ожидает подключения...")

    # Принимаем соединение от клиента
    client_socket, addr = server_socket.accept()
    logging.info("Подключение установлено с клиентом: %s", addr)

    # Получаем открытый ключ клиента
    A = int(client_socket.recv(1024).decode())
    logging.info("Получен открытый ключ клиента: %d", A)

    # Генерируем свой открытый ключ (для упрощения используем фиксированное значение)
    B = 30  # Здесь можно использовать алгоритм для генерации собственного ключа
    client_socket.send(str(B).encode())
    logging.info("Отправлен открытый ключ клиенту: %d", B)

    # Получаем зашифрованное сообщение от клиента
    encrypted_message = client_socket.recv(1024)
    logging.info("Получено зашифрованное сообщение от клиента.")

    # Здесь можно добавить логику для расшифровки сообщения, если это необходимо

    # Закрываем соединение
    client_socket.close()
    logging.info("Соединение с клиентом закрыто.")
    server_socket.close()
    logging.info("Сервер остановлен.")

if __name__ == "__main__":
    main()
