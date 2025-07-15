# cipher/vigenere.py
from .base_cipher import BaseCipher

class VigenereCipher(BaseCipher):
    def encrypt(self, plaintext: str, key: str) -> str:
        result = []
        key = key.lower()
        key_index = 0

        for char in plaintext:
            if char.isalpha():
                shift = ord(key[key_index % len(key)]) - ord('a')
                base = ord('A') if char.isupper() else ord('a')
                shifted = chr((ord(char) - base + shift) % 26 + base)
                result.append(shifted)
                key_index += 1
            else:
                result.append(char)
        return ''.join(result)

    def decrypt(self, ciphertext: str, key: str) -> str:
        result = []
        key = key.lower()
        key_index = 0

        for char in ciphertext:
            if char.isalpha():
                shift = ord(key[key_index % len(key)]) - ord('a')
                base = ord('A') if char.isupper() else ord('a')
                shifted = chr((ord(char) - base - shift) % 26 + base)
                result.append(shifted)
                key_index += 1
            else:
                result.append(char)
        return ''.join(result)

    def name(self):
        return "Vigenère"
