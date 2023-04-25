import argparse
import json
import logging
import os

SETTINGS_FILE = 'settings.json'

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('-gen','--generation',help='Запускает режим генерации ключей')
    group.add_argument('-enc','--encryption',help='Запускает режим шифрования')
    group.add_argument('-dec','--decryption',help='Запускает режим дешифрования')
    args = parser.parse_args()
    with open(SETTINGS_FILE) as json_file:
        settings = json.load(json_file)
    
    if settings:
        if args.generation:
            print("первый")
        elif args.encryption:
            print("второй")
            print(settings)
        else:
            print("третий")
    




