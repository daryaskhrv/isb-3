import logging

from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from encryption import decryption_of_symmetric_key

logger = logging.getLogger()
logger.setLevel('INFO')

def text_decryption(private_key_path: str,symmetric_key_path: str,encrypt_file_path: str, decrypt_file_path: str,iv_path:str) -> None:
    """
    Считывает из файла зашифрованный текст, дешифрует его и сохраняет результат в файл по указанному пути.
    Parameters
    ----------
        private_key_path (str):  путь до закрытого ключа
        symmetric_key_path (str): путь до симметричного ключа
        decrypt_file_path (str): путь до расщифрованного текста
        encrypt_text_path (str): путь до зашифрованного текста
        iv_path (str): путь для чтения ключа шифрования текста
    """
    key=decryption_of_symmetric_key(private_key_path,symmetric_key_path)
    try:
        with open(encrypt_file_path, 'rb') as f:
            en_text = f.read()
        logging.info(f'Зашифрованный текст прочитан')
    except OSError as err:
        logging.warning(f'{err} ошибка чтении из файла {encrypt_file_path}')
    try:
        with open(iv_path, "rb") as f:
            iv = f.read()
        logging.info(f'Ключ для дешифрации прочитан')
    except OSError as err:
        logging.warning(f'{err} ошибка чтении из файла {iv_path}')
    cipher = Cipher(algorithms.SM4(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    dc_text = decryptor.update(en_text) + decryptor.finalize()
    unpadder = sym_padding.ANSIX923(128).unpadder()
    unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()
    try:
        with open(decrypt_file_path, 'w') as f:
            f.write(unpadded_dc_text.decode("UTF_8"))
        logging.info(f'Текст расшифрован и записан в файл')
    except OSError as err:
        logging.warning(f'{err} ошибка записи в файл {decrypt_file_path}')