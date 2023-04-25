import os

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key

def decryption_of_symmetric_key(private_key_path,symmetric_key_path)-> bytes:
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
    with open(symmetric_key_path, mode="rb") as f:
        en_key = f.read()
    with open(private_key_path, 'rb') as pem_in:
        private_key = pem_in.read()
    d_private_key = load_pem_private_key(private_key, password=None)
    dc_key = d_private_key.decrypt(en_key,
                                   padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),
                                                label=None))
    return dc_key  


def text_encryption(private_key_path,symmetric_key_path,initial_text_path, encrypt_text_path) -> None:
    """
    Считывает текст из файла, шифрует его и сохраняет результат в файл по указанному пути
    Parameters
    ----------
        private_key_path (str):  путь до закрытого ключа
        symmetric_key_path (str): путь до симметричного ключа
        initial_text_path (str): путь до исходного текста
        encrypt_text_path (str): путь до зашифрованного текста
    """
    key=decryption_of_symmetric_key(private_key_path,symmetric_key_path)
    text = ""
    with open(initial_text_path, 'r', encoding='utf-8') as f:
        text = f.read()
    padder = padding.ANSIX923(1024).padder()
    padded_text = padder.update(bytes(text, 'utf-8')) + padder.finalize()
    iv = os.urandom(8)
    cipher = Cipher(algorithms.SM4(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    c_text = encryptor.update(padded_text) + encryptor.finalize()
    print("Текст зашифрован!")
    with open(encrypt_text_path, 'wb') as f_text:
        f_text.write(c_text)