# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FrmConexao.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFormLayout, QLabel, QLineEdit, QSizePolicy,
    QWidget)

class Ui_dlgConexao(object):
    def setupUi(self, dlgConexao):
        if not dlgConexao.objectName():
            dlgConexao.setObjectName(u"dlgConexao")
        dlgConexao.resize(437, 164)
        font = QFont()
        font.setPointSize(11)
        dlgConexao.setFont(font)
        self.formLayout = QFormLayout(dlgConexao)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(dlgConexao)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.edServidor = QLineEdit(dlgConexao)
        self.edServidor.setObjectName(u"edServidor")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.edServidor)

        self.label_2 = QLabel(dlgConexao)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.edBancoDeDados = QLineEdit(dlgConexao)
        self.edBancoDeDados.setObjectName(u"edBancoDeDados")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.edBancoDeDados)

        self.label_3 = QLabel(dlgConexao)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.edUsuario = QLineEdit(dlgConexao)
        self.edUsuario.setObjectName(u"edUsuario")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.edUsuario)

        self.label_4 = QLabel(dlgConexao)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.edSenha = QLineEdit(dlgConexao)
        self.edSenha.setObjectName(u"edSenha")
        self.edSenha.setEchoMode(QLineEdit.Password)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.edSenha)

        self.buttonBox = QDialogButtonBox(dlgConexao)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.buttonBox)


        self.retranslateUi(dlgConexao)
        self.buttonBox.accepted.connect(dlgConexao.accept)
        self.buttonBox.rejected.connect(dlgConexao.reject)

        QMetaObject.connectSlotsByName(dlgConexao)
    # setupUi

    def retranslateUi(self, dlgConexao):
        dlgConexao.setWindowTitle(QCoreApplication.translate("dlgConexao", u"Conex\u00e3o ao servidor de Banco de Dados", None))
        self.label.setText(QCoreApplication.translate("dlgConexao", u"URL do servidor:", None))
        self.edServidor.setText(QCoreApplication.translate("dlgConexao", u"regulus.cotuca.unicamp.br", None))
        self.label_2.setText(QCoreApplication.translate("dlgConexao", u"Nome do banco de dados:", None))
        self.edBancoDeDados.setText(QCoreApplication.translate("dlgConexao", u"chico", None))
        self.edBancoDeDados.setPlaceholderText(QCoreApplication.translate("dlgConexao", u"BDseuRA", None))
        self.label_3.setText(QCoreApplication.translate("dlgConexao", u"Nome do usu\u00e1rio:", None))
        self.edUsuario.setText(QCoreApplication.translate("dlgConexao", u"chico", None))
        self.edUsuario.setPlaceholderText(QCoreApplication.translate("dlgConexao", u"BDseuRA", None))
        self.label_4.setText(QCoreApplication.translate("dlgConexao", u"Senha:", None))
    # retranslateUi

