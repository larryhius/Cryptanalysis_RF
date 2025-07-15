from .base_cipher import BaseCipher

def modinv(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    raise ValueError("No modular inverse")

class AffineCipher(BaseCipher):
    def encrypt(self, plaintext: str, key: tuple) -> str:
        a, b = key
        return ''.join(
            chr(((a * (ord(c) - 97) + b) % 26) + 97) if c.isalpha() else c
            for c in plaintext.lower()
        )

    def decrypt(self, ciphertext: str, key: tuple) -> str:
        a, b = key
        a_inv = modinv(a, 26)
        return ''.join(
            chr(((a_inv * ((ord(c) - 97) - b)) % 26) + 97) if c.isalpha() else c
            for c in ciphertext.lower()
        )

    def name(self):
        return "Affine"