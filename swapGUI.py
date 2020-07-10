# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'morth.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from faceswap import *
import os


class Ui_Swap(QMainWindow):
    def __init__(self):
        super(Ui_Swap, self).__init__()
        self.setupUi(self)

    def swapface(self):
        swap(self.fname,self.fname2)

    def loadFile2(self):
        print("load--file")
        self.fname2, _ = QFileDialog.getOpenFileName(self, '选择图片', 'c:\\', 'Image files(*.jpg *.gif *.png)')
        print(self.fname2)
        self.label_2.setPixmap(QPixmap(self.fname2))
        self.label_2.setScaledContents(True)
        path=os.path.dirname(self.fname2)
        self.fname2=self.fname2[len(path)+1:]


    def loadFile(self):
        print("load--file")
        self.fname, _ = QFileDialog.getOpenFileName(self, '选择图片', 'c:\\', 'Image files(*.jpg *.gif *.png)')
        self.label.setPixmap(QPixmap(self.fname))
        self.label.setScaledContents(True)
        path = os.path.dirname(self.fname)
        self.fname = self.fname[len(path) + 1:]

    def setupUi(self, Morph):
        Morph.setObjectName("Morph")
        Morph.resize(858, 800)
        Morph.setStyleSheet("font: 18pt \"Malgun Gothic\";\n"
"\n"
"\n"
"background-color: rgb(255, 255, 255);")
        #self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        #self.setMouseTracking(True)
        #self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color:#1976D2;")
        self.centralwidget = QtWidgets.QWidget(Morph)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(580, 610, 161, 51))
        #self.pushButton.setStyleSheet("font: 25 9pt \"Microsoft YaHei UI\";")
        self.pushButton.setStyleSheet("QPushButton{background-color:#16A085;border:none;color:#ffffff;font: 25 9pt \"Microsoft YaHei UI\";}"

                               "QPushButton:hover{background-color:#333333;}")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.loadFile2)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 110, 400, 400))
        self.label.setText("")
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(120, 610, 161, 51))
        self.pushButton_2.setStyleSheet("QPushButton{background-color:#16A085;border:none;color:#ffffff;font: 25 9pt \"Microsoft YaHei UI\";}"

                               "QPushButton:hover{background-color:#333333;}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.loadFile)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(450, 110, 400, 400))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(350, 610, 161, 51))
        self.pushButton_4.setStyleSheet("QPushButton{background-color:#16A085;border:none;color:#ffffff;font: 25 9pt \"Microsoft YaHei UI\";}"

                               "QPushButton:hover{background-color:#333333;}")
        self.pushButton_4.setObjectName("pushButton_3")
        self.pushButton_4.clicked.connect(self.swapface)


        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(300, 20, 271, 61))
        self.label_3.setStyleSheet("font: 30 25pt \"Microsoft YaHei UI\";color:#ffffff")
        self.label_3.setObjectName("label_3")


        Morph.setCentralWidget(self.centralwidget)

        self.retranslateUi(Morph)
        QtCore.QMetaObject.connectSlotsByName(Morph)

    def retranslateUi(self, Morph):
        _translate = QtCore.QCoreApplication.translate
        Morph.setWindowTitle(_translate("Morph", "Swap"))
        self.pushButton.setText(_translate("Morph", "上传图片2"))
        self.pushButton_2.setText(_translate("Morph", "上传图片1"))
        #self.pushButton_3.setText(_translate("Morph", "生成gif"))
        self.pushButton_4.setText(_translate("Morph", "生成图片"))
        self.label_3.setText(_translate("Morph", "Face Swap"))
        #self.labelAlpha.setText("%s" %("white", "Face Motphing"))
        #self.labelAlpha.setText((_translate("Morph","输入参数(0-1)")))
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     fileload =Ui_Swap()
#     fileload.show()
#     sys.exit(app.exec_())