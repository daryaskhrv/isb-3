import os

from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from encryption import decryption_of_symmetric_key

def text_decryption(private_key_path: str,symmetric_key_path: str,encrypted_file_path: str, decrypted_file_path: str) -> None:
    """
    Считывает из файла зашифрованный текст, дешифрует его и сохраняет результат в файл по указанному пути.
    """
    key=decryption_of_symmetric_key(private_key_path,symmetric_key_path)
    with open(encrypted_file_path, 'rb') as f:
        en_text = f.read()
    with open("iv.bin", "rb") as f:
        iv = f.read()
    cipher = Cipher(algorithms.SM4(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    dc_text = decryptor.update(en_text) + decryptor.finalize()
    unpadder = sym_padding.ANSIX923(128).unpadder()
    unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()
    print(unpadded_dc_text.decode("UTF-8"))
    print("Текст расшифрован!")
    with open(decrypted_file_path, 'w') as f:
        f.write(unpadded_dc_text.decode("UTF_8"))

