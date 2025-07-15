# cipher/caesar.py
from .base_cipher import BaseCipher

class CaesarCipher(BaseCipher):
    def encrypt(self, plaintext: str, key: int) -> str:
        result = ''
        for char in plaintext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - base + key) % 26 + base)
            else:
                result += char
        return result

    def decrypt(self, ciphertext: str, key: int) -> str:
        return self.encrypt(ciphertext, -key)

    def name(self) -> str:
        return "Caesar"
