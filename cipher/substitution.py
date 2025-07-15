from .base_cipher import BaseCipher
import string

class SubstitutionCipher(BaseCipher):
    def encrypt(self, plaintext: str, key: str) -> str:
        table = str.maketrans(string.ascii_lowercase, key.lower())
        return plaintext.lower().translate(table)

    def decrypt(self, ciphertext: str, key: str) -> str:
        reverse_key = {v: k for k, v in zip(key.lower(), string.ascii_lowercase)}
        return ''.join(reverse_key.get(c, c) for c in ciphertext.lower())

    def name(self):
        return "Substitution"