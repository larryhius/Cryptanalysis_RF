# cipher/base_cipher.py
class BaseCipher:
    def encrypt(self, plaintext: str, key):
        raise NotImplementedError

    def decrypt(self, ciphertext: str, key):
        raise NotImplementedError

    def name(self):
        return self.__class__.__name__
