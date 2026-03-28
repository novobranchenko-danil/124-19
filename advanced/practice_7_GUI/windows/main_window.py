# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QApplication, QFrame, QGroupBox, QLabel,
    QLayout, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(500, 754)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMinimumSize(QSize(500, 700))
        self.centralwidget.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.verticalLayout_2.addItem(self.horizontalSpacer_2)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(19)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setScaledContents(False)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.verticalLayout_2.addItem(self.horizontalSpacer)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        font1 = QFont()
        font1.setPointSize(14)
        self.groupBox.setFont(font1)
        self.groupBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(-1, 5, -1, 5)
        self.login_register_button = QPushButton(self.groupBox)
        self.login_register_button.setObjectName(u"login_register_button")
        self.login_register_button.setAutoExclusive(False)

        self.verticalLayout.addWidget(self.login_register_button)

        self.all_market_button = QPushButton(self.groupBox)
        self.all_market_button.setObjectName(u"all_market_button")
        self.all_market_button.setAutoExclusive(False)

        self.verticalLayout.addWidget(self.all_market_button)

        self.search_button = QPushButton(self.groupBox)
        self.search_button.setObjectName(u"search_button")
        self.search_button.setAutoExclusive(False)

        self.verticalLayout.addWidget(self.search_button)

        self.search_nearby_button = QPushButton(self.groupBox)
        self.search_nearby_button.setObjectName(u"search_nearby_button")
        self.search_nearby_button.setAutoExclusive(False)

        self.verticalLayout.addWidget(self.search_nearby_button)

        self.help_button = QPushButton(self.groupBox)
        self.help_button.setObjectName(u"help_button")
        self.help_button.setAutoExclusive(False)

        self.verticalLayout.addWidget(self.help_button)

        self.line = QFrame(self.groupBox)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.quit_button = QPushButton(self.groupBox)
        self.quit_button.setObjectName(u"quit_button")
        self.quit_button.setAutoExclusive(False)

        self.verticalLayout.addWidget(self.quit_button)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 1)
        self.verticalLayout.setStretch(4, 1)
        self.verticalLayout.setStretch(6, 1)

        self.verticalLayout_2.addWidget(self.groupBox)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 500, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\U0001f33d\U0001f9fa Farmers Market Base \U0001f955\U0001f33b", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Menu", None))
        self.login_register_button.setText(QCoreApplication.translate("MainWindow", u"Login/Register", None))
        self.all_market_button.setText(QCoreApplication.translate("MainWindow", u"View All Markets", None))
        self.search_button.setText(QCoreApplication.translate("MainWindow", u"Search Market", None))
        self.search_nearby_button.setText(QCoreApplication.translate("MainWindow", u"Search Market Nearby", None))
        self.help_button.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.quit_button.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
    # retranslateUi

