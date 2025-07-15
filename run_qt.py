# run_qt.py
import sys
from PyQt5.QtWidgets import QApplication
from gui.qt_app import CryptoWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CryptoWindow()
    window.show()
    sys.exit(app.exec_())
