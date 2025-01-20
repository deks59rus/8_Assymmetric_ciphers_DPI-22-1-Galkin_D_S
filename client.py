import socket
import os
import random
from cryptography.fernet import Fernet

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


def load_keys():
    if os.path.exists(private_key_file) and os.path.exists(public_key_file):
        with open(private_key_file, 'r') as f:
            a = int(f.read())
        with open(public_key_file, 'r') as f:
            A = int(f.read())
        return a, A
    else:
        a = random.randint(1, p - 1)
        A = pow(g, a, p)
        save_keys(a, A)
        return a, A


def encrypt_message(message, key):
    """Шифрование сообщения."""
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())


def main():
    a, A = load_keys()

    # Создаем сокет и подключаемся к серверу
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 65432))

    # Отправляем открытый ключ сервера
    client_socket.send(str(A).encode())

    # Получаем открытый ключ сервера
    B = int(client_socket.recv(1024).decode())
    print(f"Получен открытый ключ сервера: {B}")

    # Вычисляем общий секрет
    K = pow(B, a, p)
    print(f"Общий секрет (K): {K}")

    # Создаем симметричный ключ
    symmetric_key = Fernet.generate_key()
    print(f"Симметричный ключ: {symmetric_key}")

    # Шифруем сообщение и отправляем его серверу
    message = "Привет, сервер!"
    encrypted_message = encrypt_message(message, symmetric_key)
    client_socket.send(encrypted_message)

    # Закрываем соединение
    client_socket.close()


if __name__ == "__main__":
    main()
