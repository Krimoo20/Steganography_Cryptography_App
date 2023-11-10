from PySide6.QtWidgets import QApplication, QFileDialog, QLabel
from PySide6.QtGui import QPixmap
from app_Feautres import *
from Crypto.Random import get_random_bytes
from PIL import Image
import sys
from PySide6.QtUiTools import QUiLoader
import os

loader = QUiLoader()
app = QApplication(sys.argv)
window = loader.load("appInterface.ui", None)


def startHidding():
    key = get_random_bytes(16)
    hex_key = key.hex()
    data = window.message_Area_Encode.toPlainText()
    file_path = window.path_Filed_Encode.text()
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            image = Image.open(file)
            encode_enc(image, data, key)
            image.save("test.png", str("test.png".split(".")[1].upper()))
        window.encreption_filed.setText(hex_key)
    else:
        print("File not found:", file_path)

def startUnhidding():
    key_hex = window.decreption_Key.text()
    key = bytes.fromhex(key_hex)
    file_path = window.path_Filed_Decode.text()

    if os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            image = Image.open(file)
            data=unhide(key,image)
    else:

        print("File not found:",file_path)
    window.message_Area_Decode.setPlainText(data)

def findImageEncode():
    frame, _ = QFileDialog.getOpenFileName(None, "Open file", "c/")
    window.path_Filed_Encode.setText(frame[45:67])
    pximap = QPixmap(str(window.path_Filed_Encode.text()))
    window.imagToEncode.setPixmap(pximap)
def findImageDencode():
    frame, _ = QFileDialog.getOpenFileName(None, "Open file", "c/")
    window.path_Filed_Decode.setText(frame[45:67])
    pximap = QPixmap(str(window.path_Filed_Decode.text()))
    window.imagToDecode.setPixmap(pximap)

window.encode_button.clicked.connect(startHidding)
window.browse_button_encode.clicked.connect(findImageEncode)
window.browse_button_decode.clicked.connect(findImageDencode)
window.decode_button.clicked.connect(startUnhidding)
window.show()
app.exec()
