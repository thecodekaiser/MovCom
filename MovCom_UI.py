# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MovCom.ui'
#
# Created: Sun Feb 21 13:51:48 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MovCom(object):
    def setupUi(self, MovCom):
        MovCom.setObjectName(_fromUtf8("MovCom"))
        MovCom.resize(480, 640)
        self.button_select = QtGui.QPushButton(MovCom)
        self.button_select.setGeometry(QtCore.QRect(30, 20, 98, 27))
        self.button_select.setObjectName(_fromUtf8("button_select"))
        self.button_update = QtGui.QPushButton(MovCom)
        self.button_update.setGeometry(QtCore.QRect(140, 20, 191, 27))
        self.button_update.setObjectName(_fromUtf8("button_update"))
        self.button_quit = QtGui.QPushButton(MovCom)
        self.button_quit.setGeometry(QtCore.QRect(340, 20, 98, 27))
        self.button_quit.setObjectName(_fromUtf8("button_quit"))
        self.list_window = QtGui.QTextEdit(MovCom)
        self.list_window.setGeometry(QtCore.QRect(30, 90, 411, 191))
        self.list_window.setObjectName(_fromUtf8("list_window"))
        self.button_com = QtGui.QPushButton(MovCom)
        self.button_com.setGeometry(QtCore.QRect(110, 600, 231, 27))
        self.button_com.setObjectName(_fromUtf8("button_com"))
        self.progressBar = QtGui.QProgressBar(MovCom)
        self.progressBar.setGeometry(QtCore.QRect(30, 570, 401, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.label = QtGui.QLabel(MovCom)
        self.label.setGeometry(QtCore.QRect(30, 60, 121, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(MovCom)
        self.label_2.setGeometry(QtCore.QRect(30, 290, 111, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.list_fetched = QtGui.QListWidget(MovCom)
        self.list_fetched.setGeometry(QtCore.QRect(30, 321, 411, 221))
        self.list_fetched.setObjectName(_fromUtf8("list_fetched"))

        self.retranslateUi(MovCom)
        QtCore.QObject.connect(self.button_quit, QtCore.SIGNAL(_fromUtf8("clicked()")), MovCom.close)
        QtCore.QMetaObject.connectSlotsByName(MovCom)

    def retranslateUi(self, MovCom):
        MovCom.setWindowTitle(_translate("MovCom", "Form", None))
        self.button_select.setText(_translate("MovCom", "SELECT FILES", None))
        self.button_update.setText(_translate("MovCom", "UPDATE LIST", None))
        self.button_quit.setText(_translate("MovCom", "EXIT", None))
        self.button_com.setText(_translate("MovCom", "MAKE COMPARISIONS", None))
        self.label.setText(_translate("MovCom", "SELECTED FILES:", None))
        self.label_2.setText(_translate("MovCom", "FETCHED FILES:", None))

