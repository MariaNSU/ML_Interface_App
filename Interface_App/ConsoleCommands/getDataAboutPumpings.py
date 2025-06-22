import subprocess
import paramiko
# Список проектов
projects = [
    "MHAD2010",
    "MHAD2011",
    "MHAD2012",
    "MHAD2017",
    "MHAD2019",
    "MHAD2020",
    "MHAD2021",
    "MHAD2022",
    "MHAD2023",
    "MHAD2024",
    "RHO_2013",
    "RHO_2018",
    "RHO_2019",
    "RHO_2024",
    "PHI_2024",
]


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

# Имя выходного файла
output_file = "../ExperimentsData/pumping_data.txt"

'''
# Открываем файл для записи
with open(output_file, "w", encoding="utf-8") as file:
    for project in projects:
        try:
            # Формируем команду
            command = ["recolist", "pointstable", "-s", project]

            # Выполняем команду и получаем её вывод
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = result.stdout.strip()  # Берём стандартный вывод

            # Записи в файл имя проекта и результат команды
            file.write(f"{project}\n")
            file.write(f"{output}\n\n")

            print(f"Результаты для проекта {project} записаны.")
        except Exception as e:
            print(f"Ошибка при выполнении команды для проекта {project}: {e}")

print(f"Все данные успешно записаны в файл '{output_file}'.")
'''

def getModelingData():
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
    with open(output_file, "w", encoding="utf-8") as file:
        for project_name in projects:
            recolist_command = f"cd /online/users2/petrovam/R008-002 && recolist pointstable -s {project_name}"
            stdin, stdout, stderr = second_client.exec_command(recolist_command)
            res = stdout.read().decode()
            print(res)
            file.write(project_name + "\n" + res + "\n")
    # Закрытие соединений
    second_client.close()
    first_client.close()
    print("[INFO] All connections are closed.")

