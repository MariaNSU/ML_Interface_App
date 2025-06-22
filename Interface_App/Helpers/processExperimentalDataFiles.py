import os
from Constants.lists import PUMPINGS, LATEST_PUMPINGS

# Определяем базовую папку проекта
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_vocabulary_pumping_release(filename='ExperimentsData/pumping_release.txt'):
    '''
    Создает словарь из данных о перекачках и релизах.
    Возвращает словарь, в котором каждой перекачке соответвествует её версия и релиз
    :param filename:
    :return:
    '''
    # Вычисляем абсолютный путь к файлу
    abs_path = os.path.join(BASE_PATH, filename)
    with open(abs_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    data = {}
    for line in lines:
        parts = line.split()
        if len(parts) != 2:
            continue
        name, release = parts[0], parts[1]

        version = int(name.split('-')[-1])
        data[name.split('-')[0]] = [version, release]

    return data

def latest_pumpings():
    """
    Список перекачек просто зададим переменной вместо чтения из файла. Выберем прекачки с последней версией
    :return: список из перекачек с последней версией
    """

    data = [
        "MHAD2010-4", "MHAD2011-6", "MHAD2012-6", "MHAD2017-4", "MHAD2017-5", "MHAD2017-6",
        "MHAD2019-2", "MHAD2019-3", "MHAD2020-1", "MHAD2020-3", "MHAD2021-1", "MHAD2021-2",
        "MHAD2022-3", "MHAD2023-0", "MHAD2023-1", "MHAD2023-2", "MHAD2024-0", "MHAD2024-1",
        "MHAD2024-2", "RHO_2013-4", "RHO_2018-2", "RHO_2018-3", "RHO_2018-4", "RHO_2018-5",
        "RHO_2018-6", "RHO_2018-8", "RHO_2019-1", "RHO_2019-2", "RHO_2024-0", "PHI_2024-0"
    ]

    # Словарь для хранения максимальных версий
    max_versions = {}

    # Обрабатываем данные
    for entry in data:
        # Разделяем название на основную часть и версию
        name, version = entry.rsplit("-", 1)
        version = int(version)  # Преобразуем версию в число

        # Если название ещё не встречалось или текущая версия больше
        if name not in max_versions or version > max_versions[name][1]:
            max_versions[name] = (entry, version)

    # Извлекаем только названия с максимальными версиями
    result = [item[0] for item in max_versions.values()]

    # Вывод результата
    return result


def modeling_list_for_pumping(pumping):
    '''
    Возвращает список моделирований для конкретной перекачки
    :param pumping: название перекачки
    :return: список моделирований
    '''
    # Путь к файлам
    latest_pumpings_path = os.path.join(BASE_PATH, "ExperimentsData/latest_pumpings.txt")
    modeling_path = os.path.join(BASE_PATH, "ExperimentsData/modeling.txt")

    # ищем какой релиз соответсвует выбранной перекачке
    with open(latest_pumpings_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    release_for_pump = ""
    for line in lines:
        parts = line.split()
        if len(parts) != 2:
            continue
        name, release = parts[0], parts[1]
        if pumping == name:
            release_for_pump = release
            break

    # достаем названия моделирований
    with open(modeling_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    for line in lines:
        parts = line.split(":")
        if len(parts) != 2:
            continue
        release, modelings = parts[0], parts[1]
        if release == release_for_pump:
            return modelings.split(',')
    return []

def create_vocabulary_pumping_data(filename='ExperimentsData/pumping_data.txt'):
    '''
    Возвращает словарь, в котором каждому названию перекачки
    соотвествует количество точек по энергии,
    сами точки и интегральная светимость
    :param filename:
    :return:
    '''
    abs_path = os.path.join(BASE_PATH, filename)
    with open(abs_path, 'r') as file:
        lines = file.readlines()

    results = {}
    current_section = None
    energy_points = []
    luminosities = []

    for line in lines:
        line = line.strip()

        if not line:  # Пустая строка указывает на конец текущего блока
            if current_section:  # Сохраняем результаты текущей секции
                results[current_section] = {
                    "count": len(energy_points),
                    "energy_points": energy_points,
                    "luminosity_sum": sum(luminosities),
                }
                current_section = None
                energy_points = []
                luminosities = []
        elif not line[0].isdigit():  # Новая секция с именем перекачки
            if current_section:  # Сохраняем данные предыдущей перекачки
                results[current_section] = {
                    "count": len(energy_points),
                    "energy_points": energy_points,
                    "luminosity_sum": sum(luminosities),
                }
            current_section = line
            energy_points = []
            luminosities = []
        else:  # Строка с данными
            parts = line.split()
            energy = float(parts[0])  # Первая колонка — энергия
            luminosity = float(parts[2])  # Третья колонка — светимость
            energy_points.append(energy)
            luminosities.append(luminosity)

    # Сохраняем данные последней секции
    if current_section:
        results[current_section] = {
            "count": len(energy_points),
            "energy_points": energy_points,
            "luminosity_sum": sum(luminosities),
        }

    return results


def print_vocabulary_pumping_data():
    '''
    Принтует словарь, в котором каждому названию перекачки
    соотвествует количество точек по энергии,
    сами точки и интегральная светимость
    :return:
    '''
    results = create_vocabulary_pumping_data()
    for section, data in results.items():
        first_point, second_point = data['energy_points'][:2]
        last_point, prev_point = data['energy_points'][-3:-1]
        info = (f"Перекачка: {section}\nКоличество точек энергии: {data['count']}\nЗначения точек энергии: {first_point},"
                f" {second_point}...{last_point}, {prev_point}\nСуммарная светимость: {data['luminosity_sum']: .2f}\n")

        print(info)


def create_vocabulary_ntuples(filename='ExperimentsData/hist-neu.txt'):
    """
    Возвращает словарь, в котором каждой переменной NTuple
    соотвествует комментарий.
    Имена берет из файла fwk/hist-neu.fwi
    Формат данных: Hists.tuple("my", "sts[nst]/I := st.sector" )
    имя переменной = sts[nst]/I
    комментарий = st.sector
    :param filename:
    :return:
    """
    result = {}
    abs_path = os.path.join(BASE_PATH, filename)
    with open(abs_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()  # Убираем лишние пробелы
            if not line or not line.startswith("Hists.tuple"):
                # Пропускаем пустые строки и строки, которые не начинаются с Hists.tuple
                continue

            # Извлекаем содержимое скобок (после "my")
            start_index = line.find('"my",') + len('"my",')
            content = line[start_index:].strip()

            # Разбиваем на имя переменной и комментарий
            if ":=" in content:
                variable, comment = content.split(":=", 1)
                variable = variable.strip()  # Убираем пробелы вокруг имени переменной
                comment = comment.strip()  # Убираем пробелы вокруг комментария

                # Сохраняем в словарь
                result[variable[1:]] = comment[:-1] #берём срезы, чтобы убрать лишнюю кавычку от имени переменной и скубку от коммента

    return result


def list_of_ntuple_vars(filename="ExperimentsData/ntuple_variables.txt"):
    abs_path = os.path.join(BASE_PATH, filename)
    result = []
    with open(abs_path, "r", encoding="utf-8") as file:
        for line in file:
            result.append(line[:-1])

    return result


def formatted_info_about_pumping(pumping="MHAD2010"):
    """
    Возвращает отформатированную информацию о перекачке в читаемом виде.
    Если передано несуществующее название выводит сообщение об ошибке
    :param pumping: Название перекачки
    :return: string
    """
    results = create_vocabulary_pumping_data()
    try:
        data = results[pumping]
        first_point, second_point = data['energy_points'][:2]
        last_point, prev_point = data['energy_points'][-3:-1]
        info = (f"Перекачка: {pumping}\nКоличество точек энергии: {data['count']}\nЗначения точек энергии: {first_point},"
                    f" {second_point} ... {last_point}, {prev_point} Мэв\nСуммарная светимость: {data['luminosity_sum']: .2f} нб-1")
        return info
    except KeyError as err:
        print(f"{err}! Перекачки {pumping} не существует!")


def get_data_folder(user_choice: str) -> str:
    """
    Функция принимает название эксперимента, выбранного юзером, и возвращает название папки с данными,
    соответствующее эксперименту, на основе списка версий.
    Если выбранный эксперимент не найден, выбрасывается исключение ValueError.
    """
    try:
        # Находим индекс эксперимента в списке pumpings
        index = PUMPINGS.index(user_choice)
        # По найденному индексу возвращаем соответствующий элемент из latest_pumpings
        return LATEST_PUMPINGS[index]
    except ValueError:
        return f"Эксперимент '{user_choice}' не найден в списке доступных экспериментов."

