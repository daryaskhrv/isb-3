import logging
import os

from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key

logger = logging.getLogger()
logger.setLevel('INFO')

def decryption_of_symmetric_key(private_key_path: str,symmetric_key_path: str)-> bytes:
    """
    Считывает из файла зашифрованный симметричный ключ и дешифрует его
    Parameters
    ----------
        private_key_path (str):  путь до закрытого ключа
        symmetric_key_path (str): путь до симметричного ключа
    Returns
    --------
        dc_key (bytes): расшифрованный симметричный ключ
    """
    try:
        with open(symmetric_key_path, mode="rb") as f:
            en_key = f.read()
        logging.info(f'Симметричный ключ успешно прочитан')
    except OSError as err:
        logging.warning(f'{err} ошибка чтении из файла {symmetric_key_path}')
    try:
        with open(private_key_path, 'rb') as pem_in:
            private_key = pem_in.read()
        logging.info(f'Закрытый ключ успешно прочитан')
    except OSError as err:
        logging.warning(f'{err} ошибка чтении из файла {private_key_path}')
    d_private_key = load_pem_private_key(private_key, password=None)
    dc_key = d_private_key.decrypt(en_key,
                                   padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),
                                                label=None))
    return dc_key  


def text_encryption(private_key_path: str,symmetric_key_path: str,initial_text_path: str, encrypt_text_path: str,iv_path:str) -> None:
    """
    Считывает текст из файла, шифрует его и сохраняет результат в файл по указанному пути
    Parameters
    ----------
        private_key_path (str):  путь до закрытого ключа
        symmetric_key_path (str): путь до симметричного ключа
        initial_text_path (str): путь до исходного текста
        encrypt_text_path (str): путь до зашифрованного текста
        iv_path (str): путь для сохранения ключа шифрования текста
    """
    key=decryption_of_symmetric_key(private_key_path,symmetric_key_path)
    try:
        with open(initial_text_path, 'r', encoding='utf-8') as f:
            text = f.read()
        logging.info(f'Исходный текст прочитан')
    except OSError as err:
        logging.warning(f'{err} ошибка чтении из файла {initial_text_path}')
    padder = sym_padding.ANSIX923(128).padder()
    padded_text = padder.update(bytes(text, 'utf-8')) + padder.finalize()
    iv = os.urandom(16)
    try:
        with open(iv_path, 'wb') as key_file:
            key_file.write(iv)
        logging.info(f'Ключ для шифрования текста прочитан')
    except OSError as err:
        logging.warning(f'{err} ошибка чтении из файла {iv_path}')
    cipher = Cipher(algorithms.SM4(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    c_text = encryptor.update(padded_text) + encryptor.finalize()
    try:
        with open(encrypt_text_path, 'wb') as f_text:
            f_text.write(c_text)
        logging.info(f'Текст зашифрован и записан в файл')
    except OSError as err:
        logging.warning(f'{err} ошибка записи в файл{encrypt_text_path}')