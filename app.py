from hashlib import pbkdf2_hmac, sha1
import sys

import secretstorage
from importlib import import_module
import secretstorage
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from PyQt6.QtWidgets import QApplication, QLabel, QWidget
import password

app = QApplication([])

window = QWidget()
window.setWindowTitle("PyQt App")
window.setGeometry(100, 100, 280, 80)
helloMsg = QLabel("<h1>Hello, World!</h1>", parent=window)
helloMsg.move(60, 15)

window.show()

sys.exit(app.exec())