# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'list.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.add = QPushButton(Form)
        self.add.setObjectName(u"add")

        self.horizontalLayout_2.addWidget(self.add)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


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
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"\u952e", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"\u503c", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"\u6570\u636e\u7c7b\u578b", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"\u6570\u636e\u957f\u5ea6", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"\u6709\u6548\u671f", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"\u64cd\u4f5c", None));
        self.label.setText(QCoreApplication.translate("Form", u"/", None))
        self.total.setText(QCoreApplication.translate("Form", u"0", None))
#if QT_CONFIG(statustip)
        self.home.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.home.setText(QCoreApplication.translate("Form", u"<<", None))
#if QT_CONFIG(statustip)
        self.previous.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.previous.setText(QCoreApplication.translate("Form", u"<", None))
#if QT_CONFIG(statustip)
        self.next.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.next.setText(QCoreApplication.translate("Form", u">", None))
#if QT_CONFIG(statustip)
        self.end.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.end.setText(QCoreApplication.translate("Form", u">>", None))
    # retranslateUi

