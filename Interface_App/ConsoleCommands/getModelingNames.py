import os
import paramiko




def get_folder_structure(root_folder):
    folder_structure = {}

    # Проход по всем подпапкам внутри root_folder
    for subfolder in os.listdir(root_folder):
        subfolder_path = os.path.join(root_folder, subfolder)

        # Проверяем, что это папка и ее имя начинается на "R00"
        if os.path.isdir(subfolder_path) and subfolder.startswith("R00"):
            # Получаем список всех папок внутри этой подпапки
            inner_folders = [
                folder for folder in os.listdir(subfolder_path)
                if os.path.isdir(os.path.join(subfolder_path, folder))
            ]
            folder_structure[subfolder] = inner_folders  # Добавляем в словарь

    return folder_structure

username = ''
pswd = ''
# Информация о первом хосте (первоначальное подключение)
FIRST_HOST = {
    'hostname': 'sndxt1.inp.nsk.su',  # IP/домен первого хоста
    'port': 22,  # Порт SSH (обычно 22)
    'username': username,  # Логин первого хоста
    'password': pswd  # Пароль первого хоста
}

# Информация о втором хосте (команда передается через первый хост)
SECOND_HOST = {
    'hostname': 'sndhw3.inp.nsk.su',  # IP/домен второго хоста
    'username': username,  # Логин второго хоста
    'password': pswd  # Пароль второго хоста
}


def ssh_jump():
    # Подключение к первому хосту
    print("[INFO] Connecting to the first host...")
    first_client = paramiko.SSHClient()
    first_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Отключение проверки ключа
    first_client.connect(
        hostname=FIRST_HOST['hostname'],
        port=FIRST_HOST['port'],
        username=FIRST_HOST['username'],
        password=FIRST_HOST['password']
    )
    print("[INFO] Successfully connected to the first host.")

    # Настройка SSH-туннеля через первый хост для второго
    print("[INFO] Initiating SSH forwarding to the second host...")
    transport = first_client.get_transport()
    dest_addr = (SECOND_HOST['hostname'], 22)  # Адрес второго хоста и порт
    local_bind_addr = ('127.0.0.1', 10022)  # Локальный адрес и порт туннеля
    channel = transport.open_channel("direct-tcpip", dest_addr, local_bind_addr)

    # Подключение ко второму хосту через открытый туннель
    print("[INFO] Connecting to the second host through the tunnel...")
    second_client = paramiko.SSHClient()
    second_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    second_client.connect(
        hostname='127.0.0.1',  # Используем локальный адрес туннеля
        port=10022,  # Используем порт туннеля
        username=SECOND_HOST['username'],
        password=SECOND_HOST['password'],
        sock=channel  # Предоставляем сокет туннеля
    )
    print("[INFO] Successfully connected to the second host.")

    # Выполнение команд на втором хосте

    command = "cd /online/users2/petrovam/R008-002 && recolist pointstable -s MHAD2010"
    stdin, stdout, stderr = second_client.exec_command(command)
    print("[INFO] Output from the second host:")
    res = stdout.read().decode()
    print(res)
    '''with open("../ExperimentsData/modeling.txt", "w") as file:
        file.write(res)'''

    """
    Это результат на 06.12.2024
    {'R007-002': ['fwk4hadrons, hadrons'], ' R007-001': ['ee, test, 3pi, 4pi, eta4pi, kskl, 4pi0g, etapg, ppc, pap, ff, eegg, nan'], ' R008-001': ['3pi, ee, ppc, 4pi, 2kc, kskl, etg, hadrons, test, waste, 2k2pi, om2pi0, kkpi, pi0g, ff, gg, etapg'], ' R006-004': ['4pi, ee, eta4pi, 4pi0g, etapg'], ' R008-003': ['3pi, gg, 3g, kskl, etag, ee, pi0g, hadrons, mumu, ppc, 2pi0g, eeNg, 2pi0g4LK, etapi0g, ometapi0, om2pi0, kkpi, Ng'], ' R008-002': ['ee, 3pi, 4pi, 2kc, kskl, 2k2pi, eeeta, eeetap, hadrons, kskl4VD-m2hcrskl_0_95, 2pi0g, pi0g, etag, etapi0g, 2etag, kketa, etapg, 2pi0g4LK, 3g, 4g, 5g, om2pi0, gg, ometapi0, kkpi, etaee, mumu, compton, 4ONLINE, 4pi0g, pi0ee, diz, nan, pap, Ng, eta4pi]}']}
    """

    # Закрытие соединений
    second_client.close()
    first_client.close()
    print("[INFO] All connections are closed.")


