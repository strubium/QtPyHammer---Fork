from PyQt5 import QtCore, QtGui, QtWidgets

from ..utilities import lang
from ..ui import popup
import subprocess

class browser(QtWidgets.QDialog):
    def __init__(self, parent):
        super(browser, self).__init__(parent, QtCore.Qt.Tool)

        self.setWindowTitle("Run Map")

        # Add QLabel widgets
        self.box1 = QtWidgets.QLabel("Run BSP:")
        self.bsp_combo_box = QtWidgets.QComboBox()
        self.bsp_combo_box.setGeometry(200, 150, 120, 40)
        self.bsp_combo_box.addItem(lang.langNo())
        self.bsp_combo_box.addItem(lang.langNormal())
        self.bsp_combo_box.addItem("Only Entities")
        self.bsp_combo_box.setCurrentIndex(self.bsp_combo_box.findText(lang.langNormal()))

        self.box2 = QtWidgets.QLabel("Run VIS:")
        self.vis_combo_box = QtWidgets.QComboBox()
        self.vis_combo_box.setGeometry(200, 150, 120, 40)
        self.vis_combo_box.addItem(lang.langNo())
        self.vis_combo_box.addItem(lang.langNormal())
        self.vis_combo_box.addItem(lang.langFast())
        self.vis_combo_box.setCurrentIndex(self.vis_combo_box.findText(lang.langNormal()))

        self.box3 = QtWidgets.QLabel("Run RAD:")
        self.rad_combo_box = QtWidgets.QComboBox()
        self.rad_combo_box.setGeometry(200, 150, 120, 40)
        self.rad_combo_box.addItem(lang.langNo())
        self.rad_combo_box.addItem(lang.langNormal())
        self.rad_combo_box.addItem(lang.langFast())
        self.rad_combo_box.setCurrentIndex(self.rad_combo_box.findText(lang.langFast()))
        
        self.box4 = QtWidgets.QLabel("Path to VMF")
        self.textbox = QtWidgets.QLineEdit(self)
        self.textbox.resize(280,40)

        # Layout setup
        base_layout = QtWidgets.QVBoxLayout()
        base_layout.addWidget(self.box1)
        base_layout.addWidget(self.bsp_combo_box)
        base_layout.addWidget(self.box2)
        base_layout.addWidget(self.vis_combo_box)
        base_layout.addWidget(self.box3)
        base_layout.addWidget(self.rad_combo_box)
        base_layout.addWidget(self.box4)
        base_layout.addWidget(self.textbox)
        bottom_row = QtWidgets.QHBoxLayout()
        bottom_row.addStretch(1)
        cancel_button = QtWidgets.QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        bottom_row.addWidget(cancel_button)
        ok_button = QtWidgets.QPushButton(lang.langOk())
        ok_button.clicked.connect(self.on_ok_clicked)
        ok_button.setDefault(True)
        bottom_row.addWidget(ok_button)
        base_layout.addLayout(bottom_row)
        self.setLayout(base_layout)

        # Resize the dialog to fit the text
        self.adjustSize()

    def on_ok_clicked(self):
        preferences = QtWidgets.QApplication.instance().game_config
        vbsp_path = preferences.value("Hammer/BSP", r"C:/Program Files (x86)/Steam/steamapps/common/Team Fortress 2/bin/vbsp.exe")
        vvis_path = preferences.value("Hammer/Vis", r"C:/Program Files (x86)/Steam/steamapps/common/Team Fortress 2/bin/vvis.exe")
        vrad_path = preferences.value("Hammer/Light", r"C:/Program Files (x86)/Steam/steamapps/common/Team Fortress 2/bin/vrad.exe")

        game_path = preferences.value("General/GameDir", r"C:\Program Files (x86)\Steam\steamapps\common\Team Fortress 2\tf")
        file_path = self.textbox.text()

        if not file_path:
            no_text_popup = popup.browser(parent=self, popuptext="Error", msgtext="File path cannot be empty")
            no_text_popup.show()
            return
        bsp_index = self.bsp_combo_box.currentIndex()
        vis_index = self.vis_combo_box.currentIndex()
        rad_index = self.rad_combo_box.currentIndex()

        vbsp_arguments = ['-game', game_path]
        vvis_arguments = ['-game', game_path]
        vrad_arguments = ['-game', game_path]

        if bsp_index == 0:
            vbsp_arguments += ['-leaktest', file_path]
        elif bsp_index == 1:
            vbsp_arguments += ['-leaktest', file_path]
        elif bsp_index == 2:
            vbsp_arguments += ['-leaktest', '-onlyents', file_path]

        if vis_index == 0:
            vvis_arguments += [file_path]
        elif vis_index == 1:
            vvis_arguments += [file_path]
        elif vis_index == 2:
            vvis_arguments += ['-fast', file_path]

        if rad_index == 0:
            vrad_arguments += [file_path]
        elif rad_index == 1:
            vrad_arguments += [file_path]
        elif rad_index == 2:
            vrad_arguments += ['-fast', file_path]

        vbsp_command = [vbsp_path] + vbsp_arguments
        vvis_command = [vvis_path] + vvis_arguments
        vrad_command = [vrad_path] + vrad_arguments

        subprocess.run(vbsp_command, check=True)
        subprocess.run(vvis_command, check=True)
        subprocess.run(vrad_command, check=True)
        self.accept()
