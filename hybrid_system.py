import argparse
import json
import logging

from generation_key import generation_asymmetric_keys,symmetric_key_encryption
from encryption import text_encryption
from decryption import text_decryption

SETTINGS_FILE = 'settings.json'

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('-gen','--generation',help='Запускает режим генерации ключей')
    group.add_argument('-enc','--encryption',help='Запускает режим шифрования')
    group.add_argument('-dec','--decryption',help='Запускает режим дешифрования')
    args = parser.parse_args()
    try:
        with open(SETTINGS_FILE) as json_file:
            settings = json.load(json_file)
        logging.info('Параметры успешно прочитаны')
    except OSError as err:
        logging.warning(f'{err} ошибка чтении из файла {SETTINGS_FILE}')
    if settings:
        if args.generation:
            generation_asymmetric_keys(settings['secret_key'],settings['public_key'])
            symmetric_key_encryption(settings['public_key'],settings['symmetric_key'])
        elif args.encryption:
            text_encryption(settings['secret_key'],settings['symmetric_key'],settings['initial_file'],settings['encrypted_file'],settings['iv_key'])
        else:
            text_decryption(settings['secret_key'],settings['symmetric_key'],settings['encrypted_file'],settings['decrypted_file'],settings['iv_key'])