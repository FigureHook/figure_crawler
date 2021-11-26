import os

from cryptography.fernet import Fernet


def str_to_bytes(value: str) -> bytes:
    return value.encode('utf-8')


def bytes_to_str(value: bytes) -> str:
    return value.decode('utf-8')


_secret = os.getenv('SECRET')
assert _secret
fernet = Fernet(_secret)


class EncryptHelper:

    @staticmethod
    def encrypt_str(data: str) -> str:
        byte_data = str_to_bytes(data)
        encrypted_byte_data = fernet.encrypt(byte_data)
        return bytes_to_str(encrypted_byte_data)

    @staticmethod
    def decrypt_str(data: str) -> str:
        byte_data = str_to_bytes(data)
        decrypted_byte_data = fernet.decrypt(byte_data)
        return bytes_to_str(decrypted_byte_data)
