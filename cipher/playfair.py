from .base_cipher import BaseCipher

class PlayfairCipher(BaseCipher):
    def __init__(self):
        self.matrix = []

    def _generate_matrix(self, key):
        key = key.lower().replace('j', 'i')
        seen = set()
        self.matrix = []
        for char in key + 'abcdefghiklmnopqrstuvwxyz':
            if char not in seen:
                seen.add(char)
                self.matrix.append(char)

    def _find_position(self, ch):
        idx = self.matrix.index(ch)
        return divmod(idx, 5)

    def _process(self, text, key, enc=True):
        self._generate_matrix(key)
        text = text.lower().replace('j', 'i')
        pairs = [text[i:i+2] if text[i] != text[i+1] else text[i]+'x' for i in range(0, len(text)-1, 2)]
        if len(text) % 2: pairs.append(text[-1]+'x')

        result = ''
        for a, b in pairs:
            r1, c1 = self._find_position(a)
            r2, c2 = self._find_position(b)
            if r1 == r2:
                shift = 1 if enc else -1
                result += self.matrix[r1*5 + (c1+shift)%5]
                result += self.matrix[r2*5 + (c2+shift)%5]
            elif c1 == c2:
                shift = 1 if enc else -1
                result += self.matrix[((r1+shift)%5)*5 + c1]
                result += self.matrix[((r2+shift)%5)*5 + c2]
            else:
                result += self.matrix[r1*5 + c2]
                result += self.matrix[r2*5 + c1]
        return result

    def encrypt(self, plaintext: str, key: str) -> str:
        return self._process(plaintext, key, True)

    def decrypt(self, ciphertext: str, key: str) -> str:
        return self._process(ciphertext, key, False)

    def name(self):
        return "Playfair"