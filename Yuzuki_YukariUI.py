# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Yuzuki_Yukari.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 630)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidgetLog = QtWidgets.QListWidget(self.centralwidget)
        self.listWidgetLog.setGeometry(QtCore.QRect(30, 10, 321, 451))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.listWidgetLog.setFont(font)
        self.listWidgetLog.setObjectName("listWidgetLog")
        self.radioButton_1 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_1.setGeometry(QtCore.QRect(30, 480, 150, 21))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.radioButton_1.setFont(font)
        self.radioButton_1.setChecked(True)
        self.radioButton_1.setObjectName("radioButton_1")
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(190, 480, 150, 21))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setObjectName("radioButton_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 520, 680, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.buttonTalk = QtWidgets.QPushButton(self.centralwidget)
        self.buttonTalk.setGeometry(QtCore.QRect(720, 520, 160, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.buttonTalk.setFont(font)
        self.buttonTalk.setObjectName("buttonTalk")
        self.labelShowImg = QtWidgets.QLabel(self.centralwidget)
        self.labelShowImg.setGeometry(QtCore.QRect(490, 0, 300, 300))
        self.labelShowImg.setText("")
        self.labelShowImg.setPixmap(QtGui.QPixmap(":/re/img/talk.gif"))
        self.labelShowImg.setAlignment(QtCore.Qt.AlignCenter)
        self.labelShowImg.setObjectName("labelShowImg")
        self.labelResponce = QtWidgets.QTextEdit(self.centralwidget)
        self.labelResponce.setGeometry(QtCore.QRect(400, 300, 431, 181))
        self.labelResponce.setObjectName("labelResponce")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 31))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.buttonTalk.clicked.connect(MainWindow.buttonTalkSlot)
        self.radioButton_1.clicked.connect(MainWindow.showResponderName)
        self.radioButton_2.clicked.connect(MainWindow.hiddenResponderName)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.radioButton_1.setText(_translate("MainWindow", "Responderを表示"))
        self.radioButton_2.setText(_translate("MainWindow", "Responderを非表示"))
        self.buttonTalk.setText(_translate("MainWindow", "話す"))

import qt_resource_rc
