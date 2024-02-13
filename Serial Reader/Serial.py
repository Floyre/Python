import os
import sys
import csv
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

form_class = uic.loadUiType("ui\Main.ui")[0]
print(form_class)

class SelWindow(QDialog):
    def __init__(self, parent):
        print("그래픽카드 브랜드 설정 윈도우 출력 받음")

        super(SelWindow, self).__init__(parent)
        print("phase 1")

        uic.loadUi("ui\\SelWindow.ui", self)
        print("그래픽카드 브랜드 설정 윈도우 UI 로드됨")
        self.show()

class MenuWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.graphic_button.clicked.connect(self.graphic_sel)
        # self.motherboard_button.clicked.connect(self.graphic_sel)
        # self.cpu_button.clicked.connect(self.graphic_sel)

    def graphic_sel(self):
        print('그래픽카드 브랜드 설정 윈도우 출력')
        SelWindow(self)


app = QApplication(sys.argv)
mainWindow = MenuWindow()
mainWindow.show()
app.exec()