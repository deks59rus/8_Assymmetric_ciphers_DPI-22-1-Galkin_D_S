import socket
import random
import os
from cryptography.fernet import Fernet
p = 42  # Пример простого числа
g = 25   # Генератор
private_key_file = 'server_private_key.txt'
public_key_file = 'server_public_key.txt'

def save_keys(private_key, public_key):
    with open(private_key_file, 'w') as f:
        f.write(str(private_key))
    with open(public_key_file, 'w') as f:
        f.write(str(public_key))

def load_keys():
    if os.path.exists(private_key_file) and os.path.exists(public_key_file):
        with open(private_key_file, 'r') as f:
            b = int(f.read())
        with open(public_key_file, 'r') as f:
            B = int(f.read())
        return b, B
    else:
        b = random.randint(1, p-1)
        B = pow(g, b, p)
        save_keys(b, B)
        return b, B

def create_key(shared_secret):
    """Создание симметричного ключа на основе общего секрета."""
    return Fernet.generate_key()

def decrypt_message(encrypted_message, key):
    """Дешифрование сообщения."""
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message).decode()

def main():
    b, B = load_keys()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 65432))
    server_socket.listen(1)

    print("Сервер запущен и ждет подключения...")
    conn, addr = server_socket.accept()
    print(f"Подключено к {addr}")

    # Отправляем открытый ключ сервера клиенту
    conn.send(str(B).encode())

    # Получаем открытый ключ клиента
    A = int(conn.recv(1024).decode())
    print(f"Получен открытый ключ клиента: {A}")

    # Вычисляем общий секрет
    K = pow(A, b, p)
    print(f"Общий секрет (K): {K}")

    # Создаем симметричный ключ
    symmetric_key = create_key(K)
    print(f"Симметричный ключ: {symmetric_key}")

    # Получаем зашифрованное сообщение от клиента
    encrypted_message = conn.recv(1024)
    decrypted_message = decrypt_message(encrypted_message, symmetric_key)
    print(f"Расшифрованное сообщение от клиента: {decrypted_message}")

    # Закрываем соединение
    conn.close()

if __name__ == "__main__":
    main()