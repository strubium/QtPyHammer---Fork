from PyQt5 import QtCore, QtGui, QtWidgets
from ..utilities import lang

class browser(QtWidgets.QDialog):
    def __init__(self, parent):
        super(browser, self).__init__(parent, QtCore.Qt.Tool)
        self.setWindowTitle("Properties")

        # Layout setup
        base_layout = QtWidgets.QVBoxLayout()
        bottom_row = QtWidgets.QHBoxLayout()
        bottom_row.addStretch(1)
        ok_button = QtWidgets.QPushButton(lang.langOk())
        ok_button.clicked.connect(self.accept)
        ok_button.setDefault(True)
        bottom_row.addWidget(ok_button)
        base_layout.addLayout(bottom_row)
        self.setLayout(base_layout)

        # Resize the dialog to fit the text
        self.adjustSize()
