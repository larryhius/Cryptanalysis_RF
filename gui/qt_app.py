# gui/qt_app.py
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QComboBox, QTextEdit, QLineEdit, QMessageBox
)
from PyQt5.QtGui import QFont

from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.substitution import SubstitutionCipher
from cipher.affine import AffineCipher
from cipher.atbash import AtbashCipher
from cipher.rot13 import ROT13Cipher
from cipher.railfence import RailFenceCipher
from cipher.autokey import AutokeyCipher

from ml.model import KeyPredictor


class CryptoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ML Cryptanalysis GUI")
        self.setGeometry(100, 100, 600, 400)

        self.predictor = KeyPredictor()
        self.predictor.train(*self.predictor.load_data("cipher_dataset.csv"))

        self.ciphers = {
            "Caesar": CaesarCipher(),
            "Vigenère": VigenereCipher(),
            "Substitution": SubstitutionCipher(),
            "Affine": AffineCipher(),
            "Atbash": AtbashCipher(),
            "ROT13": ROT13Cipher(),
            "Rail Fence": RailFenceCipher(),
            "Autokey": AutokeyCipher(),
        }

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.cipher_label = QLabel("Cipher Type:")
        self.cipher_box = QComboBox()
        self.cipher_box.addItems(list(self.ciphers.keys()))
        self.cipher_box.currentTextChanged.connect(self.toggle_key_field)

        self.mode_label = QLabel("Mode:")
        self.mode_box = QComboBox()
        self.mode_box.addItems(["Encrypt", "Decrypt"])
        self.mode_box.currentTextChanged.connect(self.toggle_key_field)

        self.input_label = QLabel("Input Text:")
        self.input_text = QTextEdit()

        self.key_label = QLabel("Key:")
        self.key_input = QLineEdit()

        self.output_label = QLabel("Output:")
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)

        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.run_cipher)

        layout.addWidget(self.cipher_label)
        layout.addWidget(self.cipher_box)
        layout.addWidget(self.mode_label)
        layout.addWidget(self.mode_box)
        layout.addWidget(self.input_label)
        layout.addWidget(self.input_text)
        layout.addWidget(self.key_label)
        layout.addWidget(self.key_input)
        layout.addWidget(self.run_button)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_text)

        self.setLayout(layout)
        self.toggle_key_field()  # initial state

        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                color: #ecf0f1;
                font-family: Segoe UI;
                font-size: 14px;
            }

            QComboBox, QTextEdit, QLineEdit {
                background-color: #34495e;
                color: #ecf0f1;
                border: 1px solid #7f8c8d;
                border-radius: 5px;
                padding: 5px;
            }

            QPushButton {
                background-color: #2980b9;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 7px;
            }

            QPushButton:hover {
                background-color: #3498db;
            }

            QLabel {
                font-weight: bold;
                margin-top: 8px;
            }
        """)

    def toggle_key_field(self):
        cipher = self.cipher_box.currentText()
        mode = self.mode_box.currentText()

        if cipher in ["Atbash", "ROT13"]:
            self.key_input.setDisabled(True)
            self.key_input.setPlaceholderText("Key not required for this cipher")
        elif cipher == "Caesar" and mode == "Decrypt":
            self.key_input.setDisabled(False)
            self.key_input.setPlaceholderText("Leave blank to predict Caesar key")
        else:
            self.key_input.setDisabled(False)
            self.key_input.setPlaceholderText("Enter key")

    def run_cipher(self):
        cipher_name = self.cipher_box.currentText()
        mode = self.mode_box.currentText()
        text = self.input_text.toPlainText().strip()
        key_text = self.key_input.text().strip()

        if not text:
            QMessageBox.warning(self, "Error", "Input text is empty.")
            return

        cipher = self.ciphers.get(cipher_name)
        if not cipher:
            QMessageBox.critical(self, "Error", f"Cipher '{cipher_name}' not found.")
            return

        try:
            key = self.parse_key(cipher_name, key_text, text, mode)

            if mode == "Encrypt":
                result = cipher.encrypt(text, key)
            elif mode == "Decrypt":
                result = cipher.decrypt(text, key)
            else:
                raise ValueError("Unknown mode selected.")

            self.output_text.setPlainText(str(result))

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def parse_key(self, cipher_name, key_text, text, mode):
        if cipher_name in ["Atbash", "ROT13"]:
            return None

        if cipher_name == "Caesar":
            if mode == "Decrypt" and not key_text:
                return self.predictor.predict(text)
            return int(key_text)

        if cipher_name == "Vigenère":
            if not key_text.isalpha():
                raise ValueError("Key must be alphabetic.")
            return key_text.lower()

        if cipher_name == "Substitution":
            if len(key_text) != 26 or not key_text.isalpha():
                raise ValueError("Substitution key must be 26 unique letters.")
            return key_text.lower()

        if cipher_name == "Affine":
            parts = key_text.replace("(", "").replace(")", "").split(",")
            if len(parts) != 2:
                raise ValueError("Affine key must be like (a,b)")
            return (int(parts[0]), int(parts[1]))

        if cipher_name == "Rail Fence":
            return int(key_text)

        if cipher_name == "Autokey":
            return key_text.lower()

        raise ValueError("Unsupported cipher key format.")
