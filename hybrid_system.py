import argparse

from generation_key import generation_asymmetric_keys,symmetric_key_encryption
from encryption import text_encryption
from decryption import text_decryption
from settings import load_settings

SETTINGS_FILE = 'settings.json'

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-set', '--settings', type=str,
                        help='Использовать собственный файл с настройками (Указать путь к файлу)')
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('-gen','--generation',help='Запускает режим генерации ключей')
    group.add_argument('-enc','--encryption',help='Запускает режим шифрования')
    group.add_argument('-dec','--decryption',help='Запускает режим дешифрования')
    args = parser.parse_args()
    if args.settings:
        settings = load_settings(args.settings)
    else:
        settings = load_settings(SETTINGS_FILE)
    if settings:
        if args.generation:
            generation_asymmetric_keys(settings['secret_key'],settings['public_key'])
            symmetric_key_encryption(settings['public_key'],settings['symmetric_key'])
        elif args.encryption:
            text_encryption(settings['secret_key'],settings['symmetric_key'],settings['initial_file'],settings['encrypted_file'],settings['iv_key'])
        else:
            text_decryption(settings['secret_key'],settings['symmetric_key'],settings['encrypted_file'],settings['decrypted_file'],settings['iv_key'])