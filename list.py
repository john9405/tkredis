# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'list.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(600, 400)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.add = QPushButton(Form)
        self.add.setObjectName(u"add")

        self.horizontalLayout_2.addWidget(self.add)

        self.refreshBtn = QPushButton(Form)
        self.refreshBtn.setObjectName(u"refreshBtn")

        self.horizontalLayout_2.addWidget(self.refreshBtn)

        self.searchEdit = QLineEdit(Form)
        self.searchEdit.setObjectName(u"searchEdit")

        self.horizontalLayout_2.addWidget(self.searchEdit)

        self.searchBtn = QPushButton(Form)
        self.searchBtn.setObjectName(u"searchBtn")

        self.horizontalLayout_2.addWidget(self.searchBtn)

        self.clearBtn = QPushButton(Form)
        self.clearBtn.setObjectName(u"clearBtn")

        self.horizontalLayout_2.addWidget(self.clearBtn)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.tableWidget = QTableWidget(Form)
        if (self.tableWidget.columnCount() < 6):
            self.tableWidget.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout.addWidget(self.tableWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.spinBox = QSpinBox(Form)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout.addWidget(self.spinBox)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(5, 16777215))

        self.horizontalLayout.addWidget(self.label)

        self.total = QLabel(Form)
        self.total.setObjectName(u"total")
        self.total.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout.addWidget(self.total)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.home = QPushButton(Form)
        self.home.setObjectName(u"home")
        self.home.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout.addWidget(self.home)

        self.previous = QPushButton(Form)
        self.previous.setObjectName(u"previous")
        self.previous.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout.addWidget(self.previous)

        self.next = QPushButton(Form)
        self.next.setObjectName(u"next")
        self.next.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout.addWidget(self.next)

        self.end = QPushButton(Form)
        self.end.setObjectName(u"end")
        self.end.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout.addWidget(self.end)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.add.setText(QCoreApplication.translate("Form", u"\u6dfb\u52a0", None))
        self.refreshBtn.setText(QCoreApplication.translate("Form", u"\u5237\u65b0", None))
        self.searchEdit.setPlaceholderText(QCoreApplication.translate("Form", u"\u641c\u7d22\u952e...", None))
        self.searchBtn.setText(QCoreApplication.translate("Form", u"\u641c\u7d22", None))
        self.clearBtn.setText(QCoreApplication.translate("Form", u"\u6e05\u9664", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"\u952e", None))
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"\u503c", None))
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"\u6570\u636e\u7c7b\u578b", None))
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"\u6570\u636e\u957f\u5ea6", None))
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"\u6709\u6548\u671f", None))
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"\u64cd\u4f5c", None))
        self.label.setText(QCoreApplication.translate("Form", u"/", None))
        self.total.setText(QCoreApplication.translate("Form", u"0", None))
        self.home.setText(QCoreApplication.translate("Form", u"<<", None))
        self.previous.setText(QCoreApplication.translate("Form", u"<", None))
        self.next.setText(QCoreApplication.translate("Form", u">", None))
        self.end.setText(QCoreApplication.translate("Form", u">>", None))
    # retranslateUi
