import os

def create_directory(dir_name):
    """
    Check if a directory exists, and create it if it does not.
    Args:
        dir_name (str): The name or path of the directory to check and create.
    """
    # Check if directory exists
    if not os.path.exists(dir_name):
        # Create directory if it does not exist
        os.makedirs(dir_name)


def remove_key_and_enc_files(verbose=True):
    """
    Удаляет все файлы с расширениями .key и .enc в текущей директории.

    Args:
        verbose (bool): Если True, выводит информацию о процессе удаления.
                       По умолчанию True.

    Returns:
        tuple: (success_count, error_count) - количество успешно удаленных файлов
               и количество ошибок при удалении.

    Examples:
        >>> remove_key_and_enc_files()
        Удалён файл: secret.key
        Удалён файл: config.enc
        (2, 0)
    """
    success = 0
    errors = 0

    for filename in os.listdir('.'):
        if filename.endswith(('.key', '.enc')):
            try:
                os.remove(filename)
                success += 1
                if verbose:
                    print(f"Удалён файл: {filename}")
            except Exception as e:
                errors += 1
                if verbose:
                    print(f"Ошибка при удалении {filename}: {e}")

    return success, errors

