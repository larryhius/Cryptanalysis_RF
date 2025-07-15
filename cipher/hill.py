from .base_cipher import BaseCipher
import numpy as np

class HillCipher(BaseCipher):
    def _modinv(self, a, m):
        for i in range(1, m):
            if (a * i) % m == 1:
                return i
        raise ValueError("No modular inverse")

    def _matrix_mod_inv(self, matrix, mod):
        det = int(np.round(np.linalg.det(matrix)))
        det_inv = self._modinv(det % mod, mod)
        matrix_mod_inv = (
            det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % mod
        )
        return matrix_mod_inv % mod

    def _process(self, text, key_matrix, encrypt=True):
        text = text.lower().replace(" ", "")
        while len(text) % len(key_matrix) != 0:
            text += 'x'
        chunks = [text[i:i+len(key_matrix)] for i in range(0, len(text), len(key_matrix))]
        vectors = [np.array([ord(c) - ord('a') for c in chunk]) for chunk in chunks]

        result = ''
        matrix = key_matrix if encrypt else self._matrix_mod_inv(key_matrix, 26)

        for vec in vectors:
            transformed = np.dot(matrix, vec) % 26
            result += ''.join(chr(int(v) + ord('a')) for v in transformed)
        return result

    def encrypt(self, plaintext: str, key_matrix) -> str:
        return self._process(plaintext, key_matrix, True)

    def decrypt(self, ciphertext: str, key_matrix) -> str:
        return self._process(ciphertext, key_matrix, False)

    def name(self):
        return "Hill"