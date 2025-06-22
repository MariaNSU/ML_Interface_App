import getpass
import paramiko
from cryptography.fernet import Fernet

# Файл для хранения зашифрованного пароля и имени пользователя
CREDENTIALS_FILE = "credentials.txt"


# Функция для генерации и сохранения ключа шифрования
def generate_key():
    key = Fernet.generate_key()
    with open("encryption_key.key", "wb") as key_file:
        key_file.write(key)
    return key


# Функция для загрузки ключа шифрования
def load_key():
    with open("encryption_key.key", "rb") as key_file:
        return key_file.read()


# Функция для сохранения зашифрованных данных
def save_credentials(username, encrypted_password):
    with open(CREDENTIALS_FILE, "w") as file:
        file.write(f"{username}\n")
        file.write(encrypted_password.decode("utf-8"))


# Функция для загрузки зашифрованных данных
def load_credentials():
    with open(CREDENTIALS_FILE, "r") as file:
        lines = file.readlines()
        username = lines[0].strip()
        encrypted_password = lines[1].strip()
        return username, encrypted_password.encode("utf-8")


# Подключение к SSH
def ssh_connect(host, port, username, password):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=host, port=port, username=username, password=password)
        print("Успешное подключение к серверу по SSH!")
        ssh_client.close()
    except paramiko.AuthenticationException:
        print("Ошибка аутентификации. Проверьте пароль!")
    except Exception as e:
        print(f"Ошибка подключения: {e}")


# Основной код
def main():
    host = "example.com"  # Укажите IP-адрес или доменное имя
    port = 22  # Стандартный порт SSH

    # Первый запуск: запрос пароля и шифрование
    if not os.path.exists(CREDENTIALS_FILE):
        print("Первый запуск. Нужно ввести данные для подключения.")
        username = input("Введите имя пользователя: ")
        password = getpass.getpass("Введите пароль: ")

        # Генерация ключа (если его ещё нет)
        if not os.path.exists("encryption_key.key"):
            key = generate_key()
        else:
            key = load_key()

        # Шифрование пароля
        fernet = Fernet(key)
        encrypted_password = fernet.encrypt(password.encode("utf-8"))

        # Сохранение зашифрованных данных
        save_credentials(username, encrypted_password)

        # Подключение по SSH
        ssh_connect(host, port, username, password)
    else:
        print("Данные найдены. Подключение с использованием сохранённого пароля.")

        # Загрузка ключа
        key = load_key()
        fernet = Fernet(key)

        # Загрузка учётных данных
        username, encrypted_password = load_credentials()
        password = fernet.decrypt(encrypted_password).decode("utf-8")

        # Подключение по SSH
        ssh_connect(host, port, username, password)


if __name__ == "__main__":
    import os

    main()
