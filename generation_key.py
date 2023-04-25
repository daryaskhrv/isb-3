import logging
import os

from cryptography.hazmat.primitives import hashes, padding, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.serialization import load_pem_public_key

logger = logging.getLogger()
logger.setLevel('INFO')

def generation_symmetric_key() -> bytes:
    """
    Генерирует случайный ключ.
    Returns
    --------
        key (bytes): сгенерированный симметричный ключ
    """
    key = os.urandom(16)
    return key


def generation_asymmetric_keys(private_key_path: str,  public_key_path: str) -> None:
    """
    Записывает по указанным путям в файлы сгенерированные асимметричные открытый и закрытый ключи.
    Parameters
    ----------
    private_key_path (str):  путь до закрытого ключа
    public_key_path (str):  путь до открытого ключа
    """
    keys = rsa.generate_private_key(public_exponent=65537,key_size=2048)
    private_key = keys
    public_key = keys.public_key()
    try:
        with open(public_key_path, 'wb') as public_out:
            public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                 format=serialization.PublicFormat.SubjectPublicKeyInfo))
        logging.info(f'Открытый ключ успешно сгенерирован и записан в файл {public_key_path}')
    except OSError as err:
        logging.warning(f'{err} - ошибка при записи в файл {public_key_path}')
    try:
        with open(private_key_path, 'wb') as private_out:
            private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                    encryption_algorithm=serialization.NoEncryption()))
            logging.info(f'Закрытый ключ успешно сгенерирован и записан в файл {private_key_path}')
    except OSError as err:
        logging.warning(f'{err} - ошибка при записи в файл {private_key_path}')


def symmetric_key_encryption(public_key_path: str, symmetric_key_path: str) -> None:
    """
     Считывает из файла сгенерированный открытый ключ, шифрует его и
     записывает по указанному пути в файл зашифрованный симметричный ключ.
    Parameters
    ----------
    public_key_path (str):  путь до открытого ключа
    symmetric_key_path (str): путь до симметричного ключа
    """
    try:
        with open(public_key_path, "rb") as pem_in:
            public_bytes = pem_in.read()
    except OSError as err:
        logging.warning(f'{err} - ошибка при чтении из файла {public_key_path}')
    d_public_key = load_pem_public_key(public_bytes)
    key = generation_symmetric_key()
    c_key = d_public_key.encrypt(key,
                                 padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),
                                              label=None))
    try:
        with open(symmetric_key_path, "wb") as f:
            f.write(c_key)
            logging.info(f'Симметричный ключ успешно сгенерирован и записан в файл {symmetric_key_path}')
    except OSError as err:
        logging.warning(f'{err} - ошибка при записи в файл {symmetric_key_path}')