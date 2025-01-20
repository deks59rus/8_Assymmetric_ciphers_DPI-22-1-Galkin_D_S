import socket
import os
import random
import logging
from cryptography.fernet import Fernet

# Настройка логирования
logging.basicConfig(filename='client.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Параметры для протокола Диффи-Хеллмана
p = 42  # Пример простого числа
g = 25  # Генератор

private_key_file = 'client_private_key.txt'
public_key_file = 'client_public_key.txt'

def save_keys(private_key, public_key):
    with open(private_key_file, 'w') as f:
        f.write(str(private_key))
    with open(public_key_file, 'w') as f:
        f.write(str(public_key))
    logging.info("Ключи сохранены: приватный ключ = %d, публичный ключ = %d", private_key, public_key)

def load_keys():
    if os.path.exists(private_key_file) and os.path.exists(public_key_file):
        with open(private_key_file, 'r') as f:
            a = int(f.read())
        with open(public_key_file, 'r') as f:
            A = int(f.read())
        logging.info("Ключи загружены: приватный ключ = %d, публичный ключ = %d", a, A)
        return a, A
    else:
        a = random.randint(1, p-1)
        A = pow(g, a, p)
        save_keys(a, A)
        logging.info("Сгенерированы новые ключи: приватный ключ = %d, публичный ключ = %d", a, A)
        return a, A

def encrypt_message(message, key):
    """Шифрование сообщения."""
    fernet = Fernet(key)
    encrypted = fernet.encrypt(message.encode())
    logging.info("Сообщение зашифровано: %s", message)
    return encrypted

def main():
    a, A = load_keys()

    # Создаем сокет и подключаемся к серверу
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 65432))
    logging.info("Подключение к серверу установлено.")

    # Отправляем открытый ключ сервера
    client_socket.send(str(A).encode())
    logging.info("Отправлен открытый ключ: %d", A)

    # Получаем открытый ключ сервера
    B = int(client_socket.recv(1024).decode())
    logging.info("Получен открытый ключ сервера: %d", B)

    # Вычисляем общий секрет
    K = pow(B, a, p)
    logging.info("Вычислен общий секрет (K): %d", K)

    # Создаем симметричный ключ
    symmetric_key = Fernet.generate_key()
    logging.info("Сгенерирован симметричный ключ: %s", symmetric_key)

    # Запрашиваем сообщение у пользователя
    message = input("Введите сообщение для шифрования: ")
    encrypted_message = encrypt_message(message, symmetric_key)
    client_socket.send(encrypted_message)

    # Закрываем соединение
    client_socket.close()
    logging.info("Соединение с сервером закрыто.")

if __name__ == "__main__":
    main()
