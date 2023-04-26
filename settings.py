import logging
import json

settings = {
    'initial_file':'files/initial_file.txt',
    'encrypted_file': 'files/encrypted_file.txt',
    'decrypted_file': 'files/decrypted_file.txt',
    'symmetric_key': 'files/symmetric_key.txt',
    'public_key': 'files/public_key.pem',
    'secret_key': 'files/secret_key.pem',
    'iv_key':'files/iv.bin'
}

def load_settings(settings_file: str) -> dict:
    """
    Считывает из файла параметры.
    Parameters
    ----------
        settings_file (str):  путь до файла с параметрами
    Returns
    --------
        settings (dict): параметры
    """
    settings = None
    try:
        with open(settings_file) as json_file:
            settings = json.load(json_file)
        logging.info('Настройки успешно считаны')
    except OSError as err:
        logging.warning(f'{err} ошибка при чтении из файла {settings_file}')
    return settings

def record_settings(settings_file: str, settings: dict) -> None:
    """
    Записывает в файл параметры.
    Parameters
    ----------
        settings_file (str):  путь до файла с параметрами
        settings (dict): параметры
    """
    try:
        with open(settings_file, 'w') as fp:
            json.dump(settings, fp)
        logging.info('Настройки успешно записаны')
    except OSError as err:
        logging.warning(f'{err} ошибка при записи в файл {settings_file}')


if __name__ == "__main__":
    record_settings('settings.json',settings)