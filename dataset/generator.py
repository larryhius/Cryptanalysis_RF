import random
import string
import pandas as pd

from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.substitution import SubstitutionCipher
from cipher.affine import AffineCipher
from cipher.atbash import AtbashCipher
from cipher.rot13 import ROT13Cipher
from cipher.railfence import RailFenceCipher
from cipher.autokey import AutokeyCipher

# Optional: Hill and Playfair are placeholders
#from cipher.hill import HillCipher
#from cipher.playfair import PlayfairCipher

class DatasetGenerator:
    def __init__(self):
        self.ciphers = [
            CaesarCipher(),
            VigenereCipher(),
            SubstitutionCipher(),
            AffineCipher(),
            AtbashCipher(),
            ROT13Cipher(),
            RailFenceCipher(),
            AutokeyCipher(),
            #HillCipher(),       # Stub
            #PlayfairCipher(),   # Stub
        ]
        print("Loaded ciphers:", [c.name() for c in self.ciphers])

    def _random_plaintext(self, length=20):
        return ''.join(random.choices(string.ascii_lowercase + ' ', k=length))

    def _random_substitution_key(self):
        return ''.join(random.sample(string.ascii_lowercase, 26))

    def _random_affine_key(self):
        valid_a = [a for a in range(1, 26) if self._gcd(a, 26) == 1]
        a = random.choice(valid_a)
        b = random.randint(0, 25)
        return (a, b)

    def _gcd(self, a, b):
        while b:
            a, b = b, a % b
        return a

    def generate(self, n=10000):
        rows = []

        for _ in range(n):
            plaintext = self._random_plaintext()

            cipher = random.choice(self.ciphers)
            cipher_type = cipher.name()

            try:
                if cipher_type == "Caesar":
                    key = random.randint(1, 25)
                elif cipher_type == "Vigenère":
                    key = ''.join(random.choices(string.ascii_lowercase, k=5))
                elif cipher_type == "Substitution":
                    key = self._random_substitution_key()
                elif cipher_type == "Affine":
                    key = self._random_affine_key()
                elif cipher_type == "Atbash":
                    key = None
                elif cipher_type == "ROT13":
                    key = None
                elif cipher_type == "Rail Fence":
                    key = random.randint(2, 5)
                elif cipher_type == "Autokey":
                    key = ''.join(random.choices(string.ascii_lowercase, k=5))
                elif cipher_type == "Hill":
                    key = None
                elif cipher_type == "Playfair":
                    key = None
                else:
                    continue

                ciphertext = cipher.encrypt(plaintext, key)
                rows.append({
                    'plaintext': plaintext,
                    'ciphertext': ciphertext,
                    'key': key if isinstance(key, str) else str(key),
                    'cipher_type': cipher_type
                })

            except Exception as e:
                print(f"[Skipped] {cipher_type} failed: {e}")
                continue

        return pd.DataFrame(rows)

def test_all_ciphers():
    generator = DatasetGenerator()
    for cipher in generator.ciphers:
        try:
            plaintext = "hello world"
            if cipher.name() == "Caesar":
                key = 3
            elif cipher.name() == "Vigenère":
                key = "KEY"
            elif cipher.name() == "Substitution":
                key = ''.join(random.sample(string.ascii_lowercase, 26))
            elif cipher.name() == "Affine":
                key = (5, 8)
            elif cipher.name() == "Atbash":
                key = None
            elif cipher.name() == "ROT13":
                key = None
            elif cipher.name() == "Rail Fence":
                key = 3
            elif cipher.name() == "Autokey":
                key = "AUTO"
            else:
                continue

            ciphertext = cipher.encrypt(plaintext, key)
            print(f"✅ {cipher.name()}: {plaintext} → {ciphertext} with key={key}")

        except Exception as e:
            print(f"❌ {cipher.name()} failed: {e}")

def main():
    generator = DatasetGenerator()
    df = generator.generate(10000)
    df.to_csv("multi_cipher_dataset.csv", index=False)
    print("✅ Dataset generated:", df.shape)

if __name__ == "__main__":
    main()