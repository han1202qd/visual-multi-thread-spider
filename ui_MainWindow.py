# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindowrucRxS.ui'
##
## Created by: Qt User Interface Compiler version 6.0.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1197, 832)
        MainWindow.setMinimumSize(QSize(0, 0))
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setLayoutDirection(Qt.LeftToRight)
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.groupBox_3 = QGroupBox(self.groupBox)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setMinimumSize(QSize(280, 0))
        self.groupBox_3.setMaximumSize(QSize(280, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.checkBox_3 = QCheckBox(self.groupBox_3)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox_3)

        self.checkBox_4 = QCheckBox(self.groupBox_3)
        self.checkBox_4.setObjectName(u"checkBox_4")
        self.checkBox_4.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox_4)

        self.label_5 = QLabel(self.groupBox_3)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_2.addWidget(self.label_5)

        self.label_6 = QLabel(self.groupBox_3)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_2.addWidget(self.label_6)

        self.line = QFrame(self.groupBox_3)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.label_7 = QLabel(self.groupBox_3)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_2.addWidget(self.label_7)

        self.label_8 = QLabel(self.groupBox_3)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_2.addWidget(self.label_8)

        self.line_2 = QFrame(self.groupBox_3)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_2)

        self.tableWidget = QTableWidget(self.groupBox_3)
        if (self.tableWidget.columnCount() < 2):
            self.tableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(102)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)

        self.verticalLayout_2.addWidget(self.tableWidget)

        self.label_21 = QLabel(self.groupBox_3)
        self.label_21.setObjectName(u"label_21")
        font = QFont()
        font.setBold(True)
        self.label_21.setFont(font)
        self.label_21.setScaledContents(False)
        self.label_21.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_21)

        self.textEdit_4 = QTextEdit(self.groupBox_3)
        self.textEdit_4.setObjectName(u"textEdit_4")
        self.textEdit_4.setMinimumSize(QSize(0, 200))
        self.textEdit_4.setMaximumSize(QSize(16777215, 200))

        self.verticalLayout_2.addWidget(self.textEdit_4)


        self.horizontalLayout_2.addWidget(self.groupBox_3)

        self.tabWidget = QTabWidget(self.groupBox)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.horizontalLayout_4 = QHBoxLayout(self.tab_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.groupBox_12 = QGroupBox(self.tab_2)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.groupBox_12.setMinimumSize(QSize(400, 0))
        self.groupBox_12.setMaximumSize(QSize(400, 16777215))
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_12)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.groupBox_13 = QGroupBox(self.groupBox_12)
        self.groupBox_13.setObjectName(u"groupBox_13")
        self.groupBox_13.setMinimumSize(QSize(0, 60))
        self.groupBox_13.setMaximumSize(QSize(16777215, 60))
        self.gridLayout_2 = QGridLayout(self.groupBox_13)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_14 = QLabel(self.groupBox_13)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_2.addWidget(self.label_14, 0, 2, 1, 1)

        self.label_15 = QLabel(self.groupBox_13)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_2.addWidget(self.label_15, 0, 3, 1, 1)

        self.label_13 = QLabel(self.groupBox_13)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_2.addWidget(self.label_13, 0, 1, 1, 1)

        self.label_12 = QLabel(self.groupBox_13)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_2.addWidget(self.label_12, 0, 0, 1, 1)


        self.verticalLayout_8.addWidget(self.groupBox_13)

        self.tableWidget_5 = QTableWidget(self.groupBox_12)
        if (self.tableWidget_5.columnCount() < 4):
            self.tableWidget_5.setColumnCount(4)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_5.setHorizontalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_5.setHorizontalHeaderItem(1, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_5.setHorizontalHeaderItem(2, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_5.setHorizontalHeaderItem(3, __qtablewidgetitem5)
        self.tableWidget_5.setObjectName(u"tableWidget_5")
        self.tableWidget_5.setMinimumSize(QSize(0, 0))
        self.tableWidget_5.setMaximumSize(QSize(16777215, 16777215))
        self.tableWidget_5.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_5.horizontalHeader().setDefaultSectionSize(49)
        self.tableWidget_5.horizontalHeader().setStretchLastSection(False)
        self.tableWidget_5.verticalHeader().setVisible(False)

        self.verticalLayout_8.addWidget(self.tableWidget_5)

        self.textEdit_2 = QTextEdit(self.groupBox_12)
        self.textEdit_2.setObjectName(u"textEdit_2")
        self.textEdit_2.setMinimumSize(QSize(0, 300))
        self.textEdit_2.setMaximumSize(QSize(16777215, 300))

        self.verticalLayout_8.addWidget(self.textEdit_2)


        self.horizontalLayout_4.addWidget(self.groupBox_12)

        self.groupBox_6 = QGroupBox(self.tab_2)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.groupBox_5 = QGroupBox(self.groupBox_6)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setMinimumSize(QSize(0, 60))
        self.groupBox_5.setMaximumSize(QSize(16777215, 60))
        self.gridLayout = QGridLayout(self.groupBox_5)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_37 = QLabel(self.groupBox_5)
        self.label_37.setObjectName(u"label_37")

        self.gridLayout.addWidget(self.label_37, 1, 6, 1, 1)

        self.label_32 = QLabel(self.groupBox_5)
        self.label_32.setObjectName(u"label_32")

        self.gridLayout.addWidget(self.label_32, 0, 6, 1, 1)

        self.label_25 = QLabel(self.groupBox_5)
        self.label_25.setObjectName(u"label_25")

        self.gridLayout.addWidget(self.label_25, 0, 1, 1, 1)

        self.label_33 = QLabel(self.groupBox_5)
        self.label_33.setObjectName(u"label_33")

        self.gridLayout.addWidget(self.label_33, 1, 2, 1, 1)

        self.label_31 = QLabel(self.groupBox_5)
        self.label_31.setObjectName(u"label_31")

        self.gridLayout.addWidget(self.label_31, 0, 5, 1, 1)

        self.label_30 = QLabel(self.groupBox_5)
        self.label_30.setObjectName(u"label_30")

        self.gridLayout.addWidget(self.label_30, 0, 4, 1, 1)

        self.label_23 = QLabel(self.groupBox_5)
        self.label_23.setObjectName(u"label_23")

        self.gridLayout.addWidget(self.label_23, 0, 0, 1, 1)

        self.label_35 = QLabel(self.groupBox_5)
        self.label_35.setObjectName(u"label_35")

        self.gridLayout.addWidget(self.label_35, 1, 4, 1, 1)

        self.label_34 = QLabel(self.groupBox_5)
        self.label_34.setObjectName(u"label_34")

        self.gridLayout.addWidget(self.label_34, 1, 3, 1, 1)

        self.label_24 = QLabel(self.groupBox_5)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout.addWidget(self.label_24, 1, 0, 1, 1)

        self.label_29 = QLabel(self.groupBox_5)
        self.label_29.setObjectName(u"label_29")

        self.gridLayout.addWidget(self.label_29, 0, 3, 1, 1)

        self.label_28 = QLabel(self.groupBox_5)
        self.label_28.setObjectName(u"label_28")

        self.gridLayout.addWidget(self.label_28, 0, 2, 1, 1)

        self.label_36 = QLabel(self.groupBox_5)
        self.label_36.setObjectName(u"label_36")

        self.gridLayout.addWidget(self.label_36, 1, 5, 1, 1)

        self.label_26 = QLabel(self.groupBox_5)
        self.label_26.setObjectName(u"label_26")

        self.gridLayout.addWidget(self.label_26, 1, 1, 1, 1)


        self.verticalLayout_7.addWidget(self.groupBox_5)

        self.tableWidget_3 = QTableWidget(self.groupBox_6)
        self.tableWidget_3.setObjectName(u"tableWidget_3")
        self.tableWidget_3.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableWidget_3.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.tableWidget_3.setAutoScrollMargin(2)
        self.tableWidget_3.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_3.setAlternatingRowColors(True)
        self.tableWidget_3.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_3.horizontalHeader().setDefaultSectionSize(80)
        self.tableWidget_3.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_7.addWidget(self.tableWidget_3)


        self.horizontalLayout_4.addWidget(self.groupBox_6)

        self.tabWidget.addTab(self.tab_2, "")

        self.horizontalLayout_2.addWidget(self.tabWidget)


        self.gridLayout_3.addWidget(self.groupBox, 1, 0, 1, 1)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMaximumSize(QSize(16777215, 60))
        self.groupBox_2.setSizeIncrement(QSize(0, 0))
        self.horizontalLayout = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(self.groupBox_2)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.line_5 = QFrame(self.groupBox_2)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.VLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_5)

        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.spinBox = QSpinBox(self.groupBox_2)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimum(1)
        self.spinBox.setValue(1)

        self.horizontalLayout.addWidget(self.spinBox)

        self.line_4 = QFrame(self.groupBox_2)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_4)

        self.line_3 = QFrame(self.groupBox_2)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_3)

        self.pushButton = QPushButton(self.groupBox_2)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_4 = QPushButton(self.groupBox_2)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout.addWidget(self.pushButton_4)

        self.button_switch_ip = QPushButton(self.groupBox_2)
        self.button_switch_ip.setObjectName(u"button_switch_ip")

        self.horizontalLayout.addWidget(self.button_switch_ip)

        self.pushButton_3 = QPushButton(self.groupBox_2)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout.addWidget(self.pushButton_3)

        self.pushButton_2 = QPushButton(self.groupBox_2)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)


        self.gridLayout_3.addWidget(self.groupBox_2, 0, 0, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout_3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle("")
        self.groupBox_3.setTitle("")
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"\u4fe1\u606f\u83b7\u53d6\u7ebf\u7a0b", None))
        self.checkBox_4.setText(QCoreApplication.translate("MainWindow", u"\u6587\u6863\u4fdd\u5b58\u7ebf\u7a0b", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u7ebf\u7a0b\u603b\u6570\uff1a", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u5b88\u62a4\u7ebf\u7a0b\uff1a", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"0", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u7ebf\u7a0b", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u72b6\u6001", None));
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"\u7cfb\u7edf\u4fe1\u606f", None))
        self.groupBox_12.setTitle("")
        self.groupBox_13.setTitle("")
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"\u5931\u8d25\u8bb0\u5f55\u6570\uff1a", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u6210\u529f\u8bb0\u5f55\u6570\uff1a", None))
        ___qtablewidgetitem2 = self.tableWidget_5.horizontalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\u7ebf\u7a0b", None));
        ___qtablewidgetitem3 = self.tableWidget_5.horizontalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"\u6210\u529f", None));
        ___qtablewidgetitem4 = self.tableWidget_5.horizontalHeaderItem(2)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"\u5931\u8d25", None));
        ___qtablewidgetitem5 = self.tableWidget_5.horizontalHeaderItem(3)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"\u603b\u6570", None));
        self.groupBox_6.setTitle("")
        self.groupBox_5.setTitle("")
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"\u672a\u4fdd\u5b58\u8bb0\u5f55", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"[\u5931\u8d25\u8bb0\u5f55]", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"\u5df2\u8bfb\u53d6\u6709\u6548\u8bb0\u5f55\uff1a", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"[\u6210\u529f\u8bb0\u5f55]", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"\u961f\u5217\u4e2d\u5269\u4f59\u8bb0\u5f55\uff1a", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"[\u6210\u529f\u8bb0\u5f55]", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"\u5df2\u4fdd\u5b58\u8bb0\u5f55\uff1a", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"[\u5931\u8d25\u8bb0\u5f55]", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\u4e3b\u7ebf\u7a0b", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u533a", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u7f51\u5740\uff1a", None))
        self.lineEdit.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u7ebf\u7a0b\u6570\uff1a", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u786e\u8ba4", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"\u8bfb\u53d6\u6587\u4ef6", None))
        self.button_switch_ip.setText(QCoreApplication.translate("MainWindow", u"\u5207\u6362IP", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u7a7a\u8868\u683c", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u624b\u52a8\u4fdd\u5b58", None))
    # retranslateUi

