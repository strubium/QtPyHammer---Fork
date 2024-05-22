import os
import sys

import valvefgd
from PyQt5 import QtCore, QtWidgets

from QtPyHammer.ui.core import MainWindow
from QtPyHammer.ui.user_preferences.theme import load_theme

def load_ini(ini):
    # Perhaps return an encapsulated QSettings
    # with more direct access to variables (convert from default string etc.)
    # It would also be handy to have defaults saved in the code, so we can restore
    return QtCore.QSettings(ini, QtCore.QSettings.IniFormat)

def get_theme():
    return theme

def load_theme():
    self.themes = dict()
    # ^ {theme_name: theme}
    for filename in os.listdir("configs/themes/"):
        theme_name = filename.rpartition(".")[0]  # Filename without extension
        self.themes[theme_name] = load_theme(f"configs/themes/{filename}")
    theme = self.preferences.value("Theme", "default")
    if theme not in self.themes:
        theme = "default"
    self.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
    self.setPalette(self.themes[theme])
    if sys.platform == "win32":
        reg = QtCore.QSettings(r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
                              QtCore.QSettings.NativeFormat)
        if reg.value("AppsUseLightTheme") == 0:  # Windows system dark mode
            dark_theme = f"{theme}_dark"
            if dark_theme not in self.themes:
                dark_theme = "default_dark"
            self.setPalette(self.themes[dark_theme])
            self.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
            # ^ TODO: Allow themes to include .css files
            # -- and have them locked to individual widgets?

def load_fgd():
    fgd_file = self.game_config.value("Hammer/GameData0")
    self.fgd = valvefgd.parser.FgdParse(fgd_file)

def load_configs():
    self.folder = os.path.dirname(__file__)
    self.preferences = load_ini("configs/preferences.ini")
    game = self.preferences.value("Game", "Team Fortress 2")
    self.game_config = load_ini(f"configs/game_{game}.ini")
    self.hotkeys = load_ini("configs/controls/hammer.ini")

def __init__(self, argv):
    load_configs()
    load_fgd()
    load_theme()
    
