from .base_cipher import BaseCipher

class AtbashCipher(BaseCipher):
    def encrypt(self, plaintext: str, key=None) -> str:
        return self._atbash(plaintext)

    def decrypt(self, ciphertext: str, key=None) -> str:
        return self._atbash(ciphertext)

    def _atbash(self, text: str) -> str:
        return ''.join(
            chr(122 - (ord(c.lower()) - 97)) if c.isalpha() else c
            for c in text
        )
    def name(self):
        return "Atbash"