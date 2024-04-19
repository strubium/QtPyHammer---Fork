from PyQt5 import QtCore, QtGui, QtWidgets

class browser(QtWidgets.QDialog):
    def __init__(self, parent):
        super(browser, self).__init__(parent, QtCore.Qt.Tool)
        self.setWindowTitle("Popup")
        # self.setWindowIcon(parent.entity_icon)
        self.setGeometry(780, 220, 360, 640)
        app = QtWidgets.QApplication.instance()
        self.base_widget = QtWidgets.QTabWidget()
        base_layout = QtWidgets.QVBoxLayout()
        base_layout.addWidget(self.base_widget)
        bottom_row = QtWidgets.QHBoxLayout()
        bottom_row.addStretch(1)
        ok_button = QtWidgets.QPushButton("Ok")
        ok_button.clicked.connect(self.accept)
        ok_button.setDefault(True)
        bottom_row.addWidget(ok_button)
        base_layout.addLayout(bottom_row)
        self.setLayout(base_layout)