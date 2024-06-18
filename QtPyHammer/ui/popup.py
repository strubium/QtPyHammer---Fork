from PyQt5 import QtCore, QtGui, QtWidgets
from ..utilities import lang


class browser(QtWidgets.QDialog):
    def __init__(self, parent, popuptext="Error", msgtext="Something's wrong, but we don't know what"):
        super(browser, self).__init__(parent, QtCore.Qt.Tool)
        self.setWindowTitle(popuptext)

        # Add QLabel to display text
        self.text_label = QtWidgets.QLabel(msgtext)
        self.text_label.setAlignment(QtCore.Qt.AlignCenter)  # Center align text
        self.text_label.setWordWrap(True)  # Enable word wrap
        self.text_label.setMargin(15)  # Add margin to the label
        self.text_label.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)

        # Layout setup
        base_layout = QtWidgets.QVBoxLayout()
        base_layout.addWidget(self.text_label)
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
