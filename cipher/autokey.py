from .base_cipher import BaseCipher

class AutokeyCipher(BaseCipher):
    def encrypt(self, plaintext: str, key: str) -> str:
        key = key.lower() + plaintext.lower()
        return ''.join(
            chr((ord(p) - 97 + ord(k) - 97) % 26 + 97)
            for p, k in zip(plaintext.lower(), key)
        )

    def decrypt(self, ciphertext: str, key: str) -> str:
        key = key.lower()
        result = ''
        for i, c in enumerate(ciphertext.lower()):
            shift = ord(key[i]) - 97
            p = chr((ord(c) - 97 - shift) % 26 + 97)
            result += p
            key += p
        return result

    def name(self):
        return "Autokey"