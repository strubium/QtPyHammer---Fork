from PyQt5 import QtCore, QtGui, QtWidgets
from ..utilities import lang

class browser(QtWidgets.QDialog):
    def __init__(self, parent):
        super(browser, self).__init__(parent, QtCore.Qt.Tool)
        self.setWindowTitle("Properties")
        
        self.box1 = QtWidgets.QLabel("Render Mode")
        self.render_mod_combo_box = QtWidgets.QComboBox()
        self.render_mod_combo_box.setGeometry(200, 150, 120, 40)
        self.render_mod_combo_box.addItem("Flat")
        self.render_mod_combo_box.addItem("Textured")
        self.render_mod_combo_box.addItem("Wireframe")
        self.render_mod_combo_box.setCurrentIndex(self.render_mod_combo_box.findText("Textured"))

        # Layout setup
        base_layout = QtWidgets.QVBoxLayout()
        base_layout.addWidget(self.box1)
        base_layout.addWidget(self.render_mod_combo_box)
        
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
