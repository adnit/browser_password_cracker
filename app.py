import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget
from PasswordCrawler import PasswordCrawler

app = QApplication([])

window = QWidget()
window.setWindowTitle("PyQt App")
window.setGeometry(100, 100, 280, 80)
helloMsg = QLabel("<h1>Hello, World!</h1>", parent=window)
helloMsg.move(60, 15)

window.show()

browsers = PasswordCrawler()
print(browsers.dump_passwords)


sys.exit(app.exec())