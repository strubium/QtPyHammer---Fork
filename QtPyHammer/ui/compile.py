from PyQt5 import QtCore, QtGui, QtWidgets

class browser(QtWidgets.QDialog):
    def __init__(self, parent):
        super(browser, self).__init__(parent, QtCore.Qt.Tool)
        self.setWindowTitle("Run Map")

        # Add QLabel to display text
        self.text_label = QtWidgets.QLabel("The Compile Menu is not implemented yet")
        self.text_label.setAlignment(QtCore.Qt.AlignCenter)  # Center align text
        self.text_label.setWordWrap(True)  # Enable word wrap
        self.text_label.setMargin(10)  # Add margin to the label
        self.text_label.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)

        # Add QLabel widgets
        self.box1 = QtWidgets.QLabel("Run BSP")
        bsp_combo_box = QtWidgets.QComboBox() 
        bsp_combo_box.setGeometry(200, 150, 120, 40) 
        bsp_combo_box.addItem("No") 
        bsp_combo_box.addItem("Normal") 
        bsp_combo_box.addItem("Only Entities")

        self.box2 = QtWidgets.QLabel("Run VIS")
        vis_combo_box = QtWidgets.QComboBox() 
        vis_combo_box.setGeometry(200, 150, 120, 40) 
        vis_combo_box.addItem("No") 
        vis_combo_box.addItem("Normal") 
        vis_combo_box.addItem("Fast")

        self.box3 = QtWidgets.QLabel("Run RAD")
        rad_combo_box = QtWidgets.QComboBox() 
        rad_combo_box.setGeometry(200, 150, 120, 40) 
        rad_combo_box.addItem("No") 
        rad_combo_box.addItem("Normal") 
        rad_combo_box.addItem("Fast")

        # Layout setup
        base_layout = QtWidgets.QVBoxLayout()
        base_layout.addWidget(self.text_label)
        base_layout.addWidget(self.box1)
        base_layout.addWidget(self.bsp_combo_box)
        base_layout.addWidget(self.box2)
        base_layout.addWidget(self.vis_combo_box)
        base_layout.addWidget(self.box3)
        base_layout.addWidget(self.rad_combo_box)
        bottom_row = QtWidgets.QHBoxLayout()
        bottom_row.addStretch(1)
        ok_button = QtWidgets.QPushButton("Ok")
        ok_button.clicked.connect(self.accept)
        ok_button.setDefault(True)
        bottom_row.addWidget(ok_button)    
        base_layout.addLayout(bottom_row)
        self.setLayout(base_layout)

        # Resize the dialog to fit the text
        self.adjustSize()
