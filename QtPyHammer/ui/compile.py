from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess

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
        bsp_combo_box.setCurrentIndex(bsp_combo_box.findText("Normal"))

        self.box2 = QtWidgets.QLabel("Run VIS")
        vis_combo_box = QtWidgets.QComboBox()
        vis_combo_box.setGeometry(200, 150, 120, 40)
        vis_combo_box.addItem("No")
        vis_combo_box.addItem("Normal")
        vis_combo_box.addItem("Fast")
        vis_combo_box.setCurrentIndex(vis_combo_box.findText("Normal"))

        self.box3 = QtWidgets.QLabel("Run RAD")
        rad_combo_box = QtWidgets.QComboBox()
        rad_combo_box.setGeometry(200, 150, 120, 40)
        rad_combo_box.addItem("No")
        rad_combo_box.addItem("Normal")
        rad_combo_box.addItem("Fast")
        rad_combo_box.setCurrentIndex(rad_combo_box.findText("Fast"))

        # Layout setup
        base_layout = QtWidgets.QVBoxLayout()
        base_layout.addWidget(self.text_label)
        base_layout.addWidget(self.box1)
        base_layout.addWidget(bsp_combo_box)
        base_layout.addWidget(self.box2)
        base_layout.addWidget(vis_combo_box)
        base_layout.addWidget(self.box3)
        base_layout.addWidget(rad_combo_box)
        bottom_row = QtWidgets.QHBoxLayout()
        bottom_row.addStretch(1)
        cancel_button = QtWidgets.QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        bottom_row.addWidget(cancel_button)  
        ok_button = QtWidgets.QPushButton("Ok")
        ok_button.clicked.connect(self.on_ok_clicked)
        ok_button.setDefault(True)
        bottom_row.addWidget(ok_button)    
        base_layout.addLayout(bottom_row)
        self.setLayout(base_layout)

        # Resize the dialog to fit the text
        self.adjustSize()
    def on_ok_clicked(self):
        vbsp_path = r'C:\Program Files (x86)\Steam\steamapps\common\Team Fortress 2\bin\vbsp.exe'
        vvis_path = r'C:\Program Files (x86)\Steam\steamapps\common\Team Fortress 2\bin\vvis.exe'
        vrad_path = r'C:\Program Files (x86)\Steam\steamapps\common\Team Fortress 2\bin\vrad.exe'

        game_path = r'C:\Program Files (x86)\Steam\steamapps\common\Team Fortress 2\tf'
        file_path = r'C:\Users\hudso\OneDrive\Desktop\SCP Maps\Slammin Test.vmf'

        bsp_index = self.bsp_combo_box.currentIndex()
        vis_index = self.vis_combo_box.currentIndex()
        rad_index = self.rad_combo_box.currentIndex()

        vbsp_arguments = ['-game', game_path, file_path, '-leaktest']
        vvis_arguments = ['-game', game_path, file_path]
        vrad_arguments = ['-game', game_path, file_path]

        if bsp_index == 0:
            vbsp_arguments += []
        elif bsp_index == 1:
            vbsp_arguments += []
        elif bsp_index == 2:
            vbsp_arguments += ['-onlyents']

        if vis_index == 0:
            vvis_arguments += []
        elif vis_index == 1:
            vvis_arguments += []
        elif vis_index == 2:
            vvis_arguments += ['-fast']

        if rad_index == 0:
            vrad_arguments += []
        elif rad_index == 1:
            vrad_arguments += []
        elif rad_index == 2:
            vrad_arguments += ['-fast']

        vbsp_command = [vbsp_path] + vbsp_arguments
        vvis_command = [vvis_path] + vvis_arguments
        vrad_command = [vrad_path] + vrad_arguments

        subprocess.run(vbsp_command, check=True)
        subprocess.run(vvis_command, check=True)
        subprocess.run(vrad_command, check=True)
        self.accept()