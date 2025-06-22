import urllib3
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

username = "petrovam"
password = "ijAubird7"

# Отключаем предупреждения для отсутствия проверки сертификата SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_html(url="https://wwwsnd.inp.nsk.su/trac/wiki/SND2K/Data", username=username, password=password):
    """
    Функция для получения HTML страницы по ссылке.

    Возвращает:
    код страницы
    """

    try:
        # Передача логина и пароля через параметры auth
        response = requests.get(url, auth=(username, password), verify=False)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Не удалось загрузить страницу {url}. Статус: {response.status_code}")
            return None
    except requests.exceptions.SSLError as e:
        print(f"Ошибка SSL при подключении к {url}: {e}")
        return None


def extract_links(html_content, base_url="https://wwwsnd.inp.nsk.su/"):
    """
    Извлекает ссылки из HTML-кода в секции "По перекачкам".

    Аргументы:
    - html_content (str): HTML-код страницы
    - base_url (str): Базовый URL сайта (для создания полного пути ссылки)

    Возвращает:
    - list: Список полных URL-ссылок
    """
    soup = BeautifulSoup(html_content, "html.parser")
    links = []

    # Ищем секцию <h2> с id="Поперекачкам:", затем <ul> с <a>
    section = soup.find("h2", id="Поперекачкам:")
    if section:
        ul = section.find_next("ul", style="list-style-type:none")  # Находим следующий <ul>, где ссылки
        if ul:
            for a in ul.find_all("a"):  # Ищем все <a> внутри <ul>
                href = a.get("href")  # Извлекаем ссылку из атрибута href
                if href:
                    # Генерируем полный URL
                    full_url = base_url.rstrip("/") + href
                    links.append(full_url)

    return links


def get_release_name(transfer_url):
    """
    Получение информации о релизе для конкретной перекачки

    Возвращает:
    номер релиза, соотвествующий перекачке

    """

    html = get_html(transfer_url)
    if not html:
        return None

    soup = BeautifulSoup(html, 'html.parser')

    # Ищем таблицу
    table = soup.find('table', class_='wiki')

    if table:
        # Если таблица найдена, ищем строки в таблице
        rows = table.find_all('tr')
        if len(rows) > 1:
            # Если строки найдены, ищем нужную ячейку для релиза (четвертая колонка второй строки)
            release_cell = rows[1].find_all('td')[3]
            release_number = release_cell.get_text(strip=True)
            return release_number
        else:
            return None
    else:
        return None


# Основная функция для создания таблицы соответствия
def create_transfer_release_table():
    """
    Основная функция для создания таблицы соответствия

    """
    html = get_html()
    transfer_links = extract_links(html)
    if not transfer_links:
        return

    transfer_release_map = {}

    for link in transfer_links:
        release_name = get_release_name(link)
        if release_name:
            transfer_release_map[link.split('/')[-1]] = release_name

    return transfer_release_map


def download_page_with_resources(pumping_name: str, base_url="https://wwwsnd.inp.nsk.su/trac/wiki/SND2K/Data/",
                                 username=username, password=password):
    """
    Скачивает HTML-страницу вместе со всеми её зависимостями (изображения, CSS, JS)
    и сохраняет всё в локальную папку с названием, соответствующим последнему сегменту URL.
    Для скачивания обязательна авторизация! НЕ ЗАБУДЬТЕ УКАЗАТЬ ИМЯ ЮЗЕРА И ПАРОЛЬ!!!
    :param pumping_name название перекачки, пример "MHAD2020-3"
    :return абсолютный путь к скачанным данным в случае успеха, в противном случае - пустая строка
    """
    try:
        url = base_url + pumping_name
        # Получение HTML страницы
        response = requests.get(url, auth=(username, password), verify=False)
        if response.status_code != 200:
            print(f"Ошибка: Не удалось загрузить страницу. Код: {response.status_code}")
            return

        # Парсинг HTML с помощью BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Получить название папки из URL
        parsed_url = urlparse(url)
        folder_name = os.path.basename(parsed_url.path.rstrip('/')) or "index"
        if not folder_name:
            folder_name = "downloaded_page"

        # Создать папку для ресурсов
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Подпапки для ресурсов
        resources_folder = os.path.join(folder_name, "resources")
        if not os.path.exists(resources_folder):
            os.makedirs(resources_folder)

        # Загрузка и обработка ресурсов
        for tag, attribute in [
            ("img", "src"),  # Изображения
            ("script", "src"),  # Скрипты
            ("link", "href")  # CSS (и других файлов)
        ]:
            for element in soup.find_all(tag):
                resource_url = element.get(attribute)
                if not resource_url:
                    continue

                # Если ресурс указан как относительный, преобразуем его в абсолютный
                full_resource_url = urljoin(url, resource_url)

                # Получение имени файла из URL
                resource_name = os.path.basename(urlparse(full_resource_url).path)
                if not resource_name:
                    resource_name = "resource"

                # Путь для локального сохранения
                local_resource_path = os.path.join(resources_folder, resource_name)

                try:
                    # Скачивание ресурса
                    resource_response = requests.get(full_resource_url, auth=(username, password), verify=False, stream=True)
                    if resource_response.status_code == 200:
                        with open(local_resource_path, "wb") as resource_file:
                            for chunk in resource_response.iter_content(chunk_size=8192):
                                resource_file.write(chunk)

                        # Обновление ссылки на ресурс в HTML
                        element[attribute] = os.path.join("resources", resource_name)
                    else:
                        print(f"Не удалось загрузить ресурс: {full_resource_url}")
                        return ""
                except Exception as e:
                    print(f"Ошибка при загрузке ресурса {full_resource_url}: {e}")
                    return ""

        # Сохранение обновленного HTML
        html_path = os.path.join(folder_name, "index.html")
        with open(html_path, "w", encoding="utf-8") as file:
            file.write(soup.prettify())

        absolute_folder_path = os.path.abspath(folder_name)
        return absolute_folder_path
        #print(f"Страница успешно сохранена в папке: {folder_name}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return ""


latest_pumpings = [
    "MHAD2020-3",
    "MHAD2021-2",
    "MHAD2022-3",
    "MHAD2023-2",
    "MHAD2024-2",
    "RHO_2013-4",
    "RHO_2018-8",
    "RHO_2019-2",
    "RHO_2024-0",
    "PHI_2024-0"
]
for pump in latest_pumpings:
    print(download_page_with_resources(pump))

