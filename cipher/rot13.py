from .base_cipher import BaseCipher

class ROT13Cipher(BaseCipher):
    def encrypt(self, plaintext: str, key=None) -> str:
        return self._rot13(plaintext)

    def decrypt(self, ciphertext: str, key=None) -> str:
        return self._rot13(ciphertext)

    def _rot13(self, text: str) -> str:
        return ''.join(
            chr((ord(c.lower()) - 97 + 13) % 26 + 97) if c.isalpha() else c
            for c in text
        )
    def name(self):
        return "ROT13"