from .base_cipher import BaseCipher

class RailFenceCipher(BaseCipher):
    def encrypt(self, plaintext: str, key: int) -> str:
        rails = ['' for _ in range(key)]
        row, direction = 0, 1
        for char in plaintext:
            rails[row] += char
            row += direction
            if row == 0 or row == key - 1:
                direction *= -1
        return ''.join(rails)

    def decrypt(self, ciphertext: str, key: int) -> str:
        rail_len = [0] * key
        index, direction = 0, 1
        for _ in ciphertext:
            rail_len[index] += 1
            index += direction
            if index == 0 or index == key - 1:
                direction *= -1

        rails = []
        i = 0
        for l in rail_len:
            rails.append(ciphertext[i:i+l])
            i += l

        result, idx = '', [0] * key
        index, direction = 0, 1
        for _ in ciphertext:
            result += rails[index][idx[index]]
            idx[index] += 1
            index += direction
            if index == 0 or index == key - 1:
                direction *= -1
        return result

    def name(self):
        return "Rail Fence"