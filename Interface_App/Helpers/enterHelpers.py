import os
from cryptography.fernet import Fernet
import json

def process_file(file_path, content):
    """
    Проверяет существование файла, читает из него строку, если файл существует.
    Если файл отсутствует, создает его и записывает в него строку.

    :param file_path: Путь к файлу.
    :param content: Строка для записи, если файл отсутствует.
    :return: Строка из файла.
    """
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) == 1:
                return lines[0].strip()
            else:
                raise ValueError(f'Too many lines in file {file_path}!')
    else:
        with open(file_path, 'wb') as f:
            f.write(content)
        return content


def create_key():
    key = Fernet.generate_key()
    return process_file('../AppData/secret.key', key)


def encrypt_passwd(password):
    key = create_key()
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(password.encode())
    return cipher_text


def add_user_to_file(username, password, filename='user_data.txt'):
    with open(filename, "wb") as file:
        encrypted_password = encrypt_passwd(password)
        file.write(f"{username} {encrypted_password}\n".encode())



def encrypt_credentials(username, password, key_file="secret.key", cred_file="creds.enc"):
    """
    Шифрует пароль и сохраняет его вместе с юзернеймом в файл.
    Генерирует новый ключ, если его нет.

    :param username: Логин пользователя
    :param password: Пароль в открытом виде
    :param key_file: Файл, где хранится ключ шифрования (по умолчанию "secret.key")
    :param cred_file: Файл, куда сохраняются зашифрованные данные (по умолчанию "creds.enc")
    :return: True, если успешно
    """
    # Генерируем или загружаем ключ
    if not os.path.exists(key_file):
        key = Fernet.generate_key()
        with open(key_file, "wb") as f:
            f.write(key)
    else:
        with open(key_file, "rb") as f:
            key = f.read()

    # Шифруем пароль
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode()).decode()

    # Сохраняем данные в JSON
    data = {
        "username": username,
        "encrypted_password": encrypted_password
    }
    with open(cred_file, "w") as f:
        json.dump(data, f)

    return True


def decrypt_credentials(key_file="secret.key", cred_file="creds.enc"):
    """
    Расшифровывает пароль из файла и возвращает (username, password).

    :param key_file: Файл с ключом шифрования (по умолчанию "secret.key")
    :param cred_file: Файл с зашифрованными данными (по умолчанию "creds.enc")
    :return: (username, password) или (None, None), если ошибка
    """
    if not os.path.exists(key_file) or not os.path.exists(cred_file):
        return None, None

    # Загружаем ключ
    with open(key_file, "rb") as f:
        key = f.read()

    # Загружаем зашифрованные данные
    with open(cred_file, "r") as f:
        data = json.load(f)

    # Расшифровываем пароль
    fernet = Fernet(key)
    try:
        password = fernet.decrypt(data["encrypted_password"].encode()).decode()
        return data["username"], password
    except Exception as e:
        print(f"Ошибка дешифровки: {e}")
        return None, None


# Пример использования
if __name__ == "__main__":
    # Шифруем и сохраняем
    encrypt_credentials("admin", "my_secure_password123")

    # Читаем и расшифровываем
    username, password = decrypt_credentials()
    print(f"Username: {username}, Password: {password}")

