"""QtPyHammer MainWindow class & other core ui classes"""
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon

from .. import ops
from ..ui import entity, popup, texture_browser, compile, properties
from ..ui import workspace
from ..utilities import lang


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(QtWidgets.QMainWindow, self).__init__(parent)
        global current_dir
        self.setWindowIcon(QtGui.QIcon('HammerLogo.png'))
        self.setWindowTitle("QtPyHammer - Fork")
        self.setMinimumSize(640, 480)
        self.setTabPosition(QtCore.Qt.TopDockWidgetArea, QtWidgets.QTabWidget.North)
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.tabs.removeTab)
        self.setCentralWidget(self.tabs)
        # NOTE: some actions should be disabled when no maptabs are open
        # TODO: add a method to connect self.actions to the active tab
        # & connect this method to self.tabs.currentChanged(...)

        # Child dialogs
        self.map_browser = ops.MapFileBrowser(self)

        self.actions = {}
        # ^ {"identifier": action}
        self.main_menu = QtWidgets.QMenuBar()
        file_menu = self.main_menu.addMenu(lang.langFile())
        self.actions["File/New"] = file_menu.addAction("&New")

        def new_file():
            ops.new_file(self)

        self.actions["File/New"].triggered.connect(new_file)
        self.actions["File/Open"] = file_menu.addAction("&Open")

        def open_files():
            ops.open_files(self, self.map_browser)

        self.actions["File/Open"].triggered.connect(open_files)
        self.actions["File/Save"] = file_menu.addAction("&Save")

        def save_file():
            ops.save_file(self, self.map_browser)

        self.actions["File/Save"].triggered.connect(save_file)
        self.actions["File/Save As"] = file_menu.addAction("Save &As")

        def save_file_as():
            ops.save_file_as(self, self.map_browser)

        self.actions["File/Save As"].triggered.connect(save_file_as)
        file_menu.addSeparator()
        # self.import_menu = file_menu.addMenu("Import")
        # self.import_menu.addAction(".obj")
        # export_menu = file_menu.addMenu("Export")
        # export_menu.addAction("Prefab")
        # export_menu.addAction(".qph") # grayed out if active tab is a .qph
        # export_menu.addAction(".obj")
        # export_menu.addAction(".smd")
        file_menu.addSeparator()
        self.actions["File/Options"] = file_menu.addAction("&Options")
        properties_menu = properties.browser(parent=self)
        self.actions["File/Options"].triggered.connect(properties_menu.show)
        file_menu.addSeparator()
        self.actions["File/Compile"] = file_menu.addAction(lang.langCompile())
        compile_menu = compile.browser(parent=self)
        self.actions["File/Compile"].triggered.connect(compile_menu.show)
        file_menu.addSeparator()
        self.actions["File/Exit"] = file_menu.addAction(lang.langExit())
        self.actions["File/Exit"].triggered.connect(QtCore.QCoreApplication.quit)

        edit_menu = self.main_menu.addMenu(lang.langEdit())
        self.actions["Edit/Undo"] = edit_menu.addAction(lang.langUndo())
        self.actions["Edit/Undo"].setEnabled(False)
        # self.actions["Edit/Undo"].triggered.connect( # edit timeline
        self.actions["Edit/Redo"] = edit_menu.addAction(lang.langRedo())
        self.actions["Edit/Redo"].setEnabled(False)
        # self.actions["Edit/Redo"].triggered.connect( # edit timeline
        self.actions["Edit/History"] = edit_menu.addMenu("&History...")
        self.actions["Edit/History"].setEnabled(False)
        # self.actions["Edit/History"].triggered.connect(ui.edit_timeline)
        edit_menu.addSeparator()
        self.actions["Edit/Find"] = edit_menu.addAction("Find &Entites")
        self.actions["Edit/Find"].setEnabled(False)
        # self.actions["Edit/Find"].triggered.connect(ops.vmf.search)
        self.actions["Edit/Replace"] = edit_menu.addAction("&Replace")
        self.actions["Edit/Replace"].setEnabled(False)
        # self.actions["Edit/Replace"].triggered.connect(ops.vmf.search_replace)
        edit_menu.addSeparator()
        self.actions["Edit/Cut"] = edit_menu.addAction("Cu&t")
        self.actions["Edit/Cut"].setEnabled(False)
        # self.actions["Edit/Cut"].triggered.connect(
        self.actions["Edit/Copy"] = edit_menu.addAction("&Copy")
        self.actions["Edit/Copy"].setEnabled(False)
        # self.actions["Edit/Copy"].triggered.connect(
        self.actions["Edit/Paste"] = edit_menu.addAction("&Paste")
        self.actions["Edit/Paste"].setEnabled(False)
        # self.actions["Edit/Paste"].triggered.connect(
        self.actions["Edit/Paste Special"] = edit_menu.addAction("Paste &Special")
        self.actions["Edit/Paste Special"].setEnabled(False)
        # self.actions["Edit/Paste Special"].triggered.connect(
        self.actions["Edit/Delete"] = edit_menu.addAction("&Delete")
        self.actions["Edit/Delete"].setEnabled(False)
        # self.actions["Edit/Delete"].triggered.connect(
        edit_menu.addSeparator()
        self.actions["Edit/Properties"] = edit_menu.addAction("P&roperties")
        self.actions["Edit/Properties"].setEnabled(False)
        # self.actions["Edit/Properties"].triggered.connect(

        tools_menu = self.main_menu.addMenu(lang.langTools())
        self.actions["Tools/Group"] = tools_menu.addAction("&Group")
        self.actions["Tools/Group"].setEnabled(False)
        # self.actions["Tools/Group"].triggered.connect(
        self.actions["Tools/Ungroup"] = tools_menu.addAction("&Ungroup")
        self.actions["Tools/Ungroup"].setEnabled(False)
        # self.actions["Tools/Ungroup"].triggered.connect(
        tools_menu.addSeparator()
        self.actions["Tools/Brush to Entity"] = tools_menu.addAction("&Tie to Entitiy")
        try:
            ent_browser = entity.browser(parent=self)
            self.actions["Tools/Brush to Entity"].triggered.connect(ent_browser.show)
        except Exception as exc:
            error_popup = popup.browser(parent=self, popuptext="Error", msgtext="Failed to load .fgds!")
            self.actions["Tools/Brush to Entity"].triggered.connect(error_popup.show)
            self.actions["Tools/Brush to Entity"].setEnabled(False)
            raise exc
        self.actions["Tools/Entity to Brush"] = tools_menu.addAction("&Move to World")
        self.actions["Tools/Entity to Brush"].setEnabled(False)
        # self.actions["Tools/Entity to Brush"].triggered.connect(
        tools_menu.addSeparator()
        self.actions["Tools/Apply Texture"] = tools_menu.addAction("&Apply Texture")
        self.actions["Tools/Apply Texture"].setEnabled(False)
        # self.actions["Tools/Apply Texture"].triggered.connect(ops.texture.apply)
        self.actions["Tools/Replace Texture"] = tools_menu.addAction("&Replace Textures")
        self.actions["Tools/Replace Texture"].setEnabled(False)
        # self.actions["Tools/Replace Texture"].triggered.connect(ops.texture.replace)
        self.actions["Tools/Texture Lock"] = tools_menu.addAction("Texture &Lock")
        self.actions["Tools/Texture Lock"].setCheckable(True)
        self.actions["Tools/Texture Lock"].setEnabled(False)
        # self.actions["Tools/Texture Lock"].triggered.connect(
        tools_menu.addSeparator()
        self.actions["Tools/Sound Browser"] = tools_menu.addAction("&Sound Browser")
        self.actions["Tools/Sound Browser"].setEnabled(False)
        # self.actions["Tools/Sound Browser"].triggered.connect(ui.sound_browser)
        tools_menu.addSeparator()
        self.actions["Tools/Transform"] = tools_menu.addAction("Transform")
        self.actions["Tools/Transform"].setEnabled(False)
        # self.actions["Tools/Transform"].triggered.connect(
        self.actions["Tools/Snap to Grid"] = tools_menu.addAction("Snap Selection to Grid")
        self.actions["Tools/Snap to Grid"].setEnabled(False)
        # self.actions["Tools/Snap to Grid"].triggered.connect(
        tools_menu.addSeparator()
        self.actions["Tools/Flip Horizontally"] = tools_menu.addAction("Flip Horizontally")
        self.actions["Tools/Flip Horizontally"].setEnabled(False)
        # self.actions["Tools/Flip Horizontally"].triggered.connect(
        self.actions["Tools/Flip Vertically"] = tools_menu.addAction("Flip Vertically")
        self.actions["Tools/Flip Vertically"].setEnabled(False)
        # self.actions["Tools/Flip Vertically"].triggered.connect(
        tools_menu.addSeparator()
        self.actions["Tools/Create Prefab"] = tools_menu.addAction("Create &Prefab")
        self.actions["Tools/Create Prefab"].setEnabled(False)
        # self.actions["Tools/Create Prefab"].triggered.connect(

        map_menu = self.main_menu.addMenu("&Map")
        self.actions["Map/Snap to Grid"] = map_menu.addAction("&Snap to Grid")
        self.actions["Map/Snap to Grid"].setCheckable(True)
        self.actions["Map/Snap to Grid"].setChecked(True)
        self.actions["Map/Snap to Grid"].setEnabled(False)
        # self.actions["Map/Snap to Grid"].triggered.connect(
        self.actions["Map/Show Grid"] = map_menu.addAction("Sho&w Grid")
        self.actions["Map/Show Grid"].setCheckable(True)
        self.actions["Map/Show Grid"].setChecked(True)
        self.actions["Map/Show Grid"].setEnabled(False)
        # self.actions["Map/Show Grid"].triggered.connect(
        grid_settings = map_menu.addMenu("&Grid Settings")
        # Grid+ [
        # Grid- ]
        grid_settings.setEnabled(False)
        map_menu.addSeparator()
        self.actions["Map/Entity Report"] = map_menu.addAction("&Entity Report")
        self.actions["Map/Entity Report"].setEnabled(False)
        # self.actions["Map/Entity Report"].triggered.connect(ui.entity_report)
        # self.actions["Map/Zooify"] map_menu.addAction("&Zooify")
        # make an asset zoo / texture pallets from the currently open vmf
        self.actions["Map/Debug"] = map_menu.addAction("&Check for Problems")
        self.actions["Map/Debug"].setEnabled(False)
        # self.actions["Map/Debug"].triggered.connect(ui.map.debug)
        # map_menu.addAction("&Diff Map File")
        map_menu.addSeparator()
        self.actions["Map/Pointfile"] = map_menu.addAction("Pointfile / Find Leak (.lin)")
        self.actions["Map/Pointfile"].setEnabled(False)
        # self.actions["Map/Pointfile"].triggered.connect(
        self.actions["Map/Portal File"] = map_menu.addAction("Portal file (.prt)")
        self.actions["Map/Portal File"].setEnabled(False)
        # self.actions["Map/Portal File"].triggered.connect(
        map_menu.addSeparator()
        # map_menu.addAction("Show &Information")
        self.actions["Map/Properties"] = map_menu.addAction("&Map Properties")
        self.actions["Map/Properties"].setEnabled(False)
        # self.actions["Map/Properties"].triggered.connect(ui.map.properties)

        search_menu = self.main_menu.addMenu("&Search")
        self.actions["Search/Entity"] = search_menu.addAction("Find &Entity")
        self.actions["Search/Entity"].setEnabled(False)
        # self.actions["Search/Entity"].triggered.connect(ui.search.entity)
        self.actions["Search/Logic"] = search_menu.addAction("Find &IO")
        self.actions["Search/Logic"].setEnabled(False)
        # self.actions["Search/Logic"].triggered.connect(ui.search.logic)
        self.actions["Search/Replace Logic"] = search_menu.addAction("Find + &Replace IO")
        self.actions["Search/Replace Logic"].setEnabled(False)
        # self.actions["Search/Replace Logic"].triggered.connect(ui.search.logic)
        search_menu.addSeparator()
        self.actions["Search/Coords"] = search_menu.addAction("Go to &Coordinates")
        self.actions["Search/Coords"].setEnabled(False)
        # self.actions["Search/Coords"].triggered.connect(ui.search.coords)
        self.actions["Search/Brush"] = search_menu.addAction("Go to &Brush Number")
        self.actions["Search/Brush"].setEnabled(False)
        # self.actions["Search/Brush"].triggered.connect(ui.search.brush)

        view_menu = self.main_menu.addMenu("&View")
        self.actions["View/Center 2D"] = view_menu.addAction("Center 2D Views on selection")
        self.actions["View/Center 2D"].setEnabled(False)
        # self.actions["View/Center 2D"].triggered.connect(
        self.actions["View/Center 3D"] = view_menu.addAction("Center 3D Views on selection")
        self.actions["View/Center 3D"].setEnabled(False)
        # self.actions["View/Center 3D"].triggered.connect(
        view_menu.addAction(self.actions["Search/Coords"])
        view_menu.addSeparator()
        # self.actions["View/Logic"] = view_menu.addAction("Show &Logic Connections")
        # self.actions["View/Logic"].setCheckable(True)
        self.actions["View/Models"] = view_menu.addAction("Show &Models in 2D")
        self.actions["View/Models"].setCheckable(True)
        self.actions["View/Models"].setChecked(True)
        self.actions["View/Models"].setEnabled(False)
        # self.actions["View/Models"].triggered.connect(
        self.actions["View/Entity Names"] = view_menu.addAction("Entity &Names")
        self.actions["View/Entity Names"].setCheckable(True)
        self.actions["View/Entity Names"].setChecked(True)
        self.actions["View/Entity Names"].setEnabled(False)
        # self.actions["View/Entity Names"].triggered.connect(
        view_menu.addSeparator()
        self.actions["View/Hide"] = view_menu.addAction("&Hide")
        self.actions["View/Hide"].setEnabled(False)
        # self.actions["View/Hide"].triggered.connect(
        self.actions["View/Hide Unselected"] = view_menu.addAction("&Hide Unselected")
        self.actions["View/Hide Unselected"].setEnabled(False)
        # self.actions["View/Hide Unselected"].triggered.connect(
        self.actions["View/Unhide"] = view_menu.addAction("&Unhide")
        self.actions["View/Unhide"].setEnabled(False)
        # self.actions["View/Unhide"].triggered.connect(
        view_menu.addSeparator()
        self.actions["View/Visgroups"] = view_menu.addAction("Move Selection to Visgroup")
        self.actions["View/Visgroups"].setEnabled(False)
        # self.actions["View/Visgroups"].triggered.connect(ui.
        view_menu.addSeparator()
        self.actions["View/Settings"] = view_menu.addAction("&OpenGL Settings")
        self.actions["View/Settings"].setEnabled(False)
        # self.actions["View/Settings"].triggered.connect(ui.
        open_url = QtGui.QDesktopServices.openUrl
        help_menu = self.main_menu.addMenu("&Help")
        self.actions["Help/Offline"] = help_menu.addAction("Offline Help")
        self.actions["Help/Offline"].setEnabled(False)
        # self.actions["Help/Offline"].triggered.connect(ui.
        help_menu.addSeparator()
        self.actions["Help/About QPH"] = help_menu.addAction("About QtPyHammer")
        about_popup = popup.browser(parent=self, popuptext="About",
                                    msgtext="A Python alternative to Valve Hammer Editor 4.x, forked from QtPyHammer\n\nVersion: v0.0.5forked")
        self.actions["Help/About QPH"].triggered.connect(about_popup.show)
        self.actions["Help/About Qt"] = help_menu.addAction("About Qt")
        self.actions["Help/About Qt"].triggered.connect(lambda: open_url(QtCore.QUrl(
            "https://github.com/spyder-ide/qtpy")))
        # self.actions["Help/About Qt"].triggered.connect(ui. #QDialog
        self.actions["Help/License"] = help_menu.addAction("License")
        self.actions["Help/License"].triggered.connect(lambda: open_url(QtCore.QUrl(
            "https://github.com/strubium/QtPyHammer/blob/master/LICENSE")))
        # self.actions["Help/License"].triggered.connect(ui. #QDialog
        self.actions["Help/Contributors"] = help_menu.addAction("Contributors")
        self.actions["Help/Contributors"].triggered.connect(
            lambda: open_url(QtCore.QUrl("https://github.com/QtPyHammer-devs/QtPyHammer/graphs/contributors")))
        self.actions["Help/QPH Wiki"] = help_menu.addAction("QtPyHammer Wiki")
        self.actions["Help/QPH Wiki"].triggered.connect(lambda: open_url(QtCore.QUrl(
            "https://github.com/snake-biscuits/QtPyHammer/wiki")))
        help_menu.addSeparator()
        self.actions["Help/VDC"] = help_menu.addAction("Valve Developer Community")
        self.actions["Help/VDC"].triggered.connect(lambda: open_url(QtCore.QUrl(
            "https://developer.valvesoftware.com/wiki/Main_Page")))

        # attach all actions to hotkeys
        app = QtWidgets.QApplication.instance()
        for action in app.hotkeys.allKeys():
            if not action.startswith("Menu."):
                continue  # TODO: filter w/ some QSettings feature? [not .allKeys()]
            action_name = action[5:]  # remove leading "Menu."
            if action_name not in self.actions:
                continue
            shortcut = app.hotkeys.value(action)
            self.actions[action_name].setShortcut(shortcut)

        self.setMenuBar(self.main_menu)

        # TOOLBARS
        key_tools = QtWidgets.QToolBar("Tools")
        key_tools.setMovable(True)
        button_1 = QtWidgets.QToolButton()  # need icons (.png)
        button_1.setToolTip("Toggle 2D grid visibility")
        button_1.setIcon(QIcon("icons/2dHammerIcon"))
        button_1.setEnabled(False)
        key_tools.addWidget(button_1)
        button_2 = QtWidgets.QToolButton()
        button_2.setToolTip("Toggle 3D grid visibility")
        button_2.setIcon(QIcon("icons/3dHammerIcon"))
        button_2.setEnabled(False)
        key_tools.addWidget(button_2)
        button_3 = QtWidgets.QToolButton()
        button_3.setToolTip("Smaller Grid")
        button_3.setEnabled(False)
        key_tools.addWidget(button_3)
        button_4 = QtWidgets.QToolButton()
        button_4.setToolTip("Larger Grid")
        button_4.setIcon(QIcon("icons/LargeGridIcon"))
        button_4.setEnabled(False)
        key_tools.addWidget(button_4)
        key_tools.addSeparator()
        button_5 = QtWidgets.QToolButton()
        button_5.setToolTip("Load Window State")
        button_5.setEnabled(False)
        key_tools.addWidget(button_5)
        button_6 = QtWidgets.QToolButton()
        button_6.setToolTip("Save Window State")
        button_6.setEnabled(False)
        key_tools.addWidget(button_6)
        key_tools.addSeparator()
        button_7 = QtWidgets.QToolButton()
        button_7.setToolTip("Undo")
        button_7.setEnabled(False)
        key_tools.addWidget(button_7)
        button_8 = QtWidgets.QToolButton()
        button_8.setToolTip("Redo")
        button_8.setEnabled(False)
        key_tools.addWidget(button_8)
        key_tools.addSeparator()

        self.addToolBar(QtCore.Qt.TopToolBarArea, key_tools)
        # undo redo | carve | group ungroup ignore | hide unhide alt-hide |
        # cut copy paste | cordon | TL <TL> | DD 3D DW DA |
        # compile helpers 2D_models fade CM prop_detail NO_DRAW

        right_toolbar = QtWidgets.QToolBar("Sidebar")
        right_toolbar.setFixedWidth(115)
        label_1 = QtWidgets.QLabel("Select:")
        right_toolbar.addWidget(label_1)
        right_toolbar.setMovable(True)
        button_1 = QtWidgets.QPushButton("Groups")
        button_1.setFixedSize(100, 25)
        button_1.setEnabled(False)
        right_toolbar.addWidget(button_1)
        button_2 = QtWidgets.QPushButton("Objects")
        button_2.setFixedSize(100, 25)
        button_2.setEnabled(False)
        right_toolbar.addWidget(button_2)
        button_3 = QtWidgets.QPushButton("Solids")
        button_3.setFixedSize(100, 25)
        button_3.setEnabled(False)
        right_toolbar.addWidget(button_3)
        right_toolbar.addSeparator()

        label_2 = QtWidgets.QLabel("Texture Selection:")
        right_toolbar.addWidget(label_2)
        button_4 = QtWidgets.QPushButton("Browse")
        button_4.setFixedSize(100, 25)
        texture_popup = texture_browser.TextureBrowser(parent=self)
        button_4.clicked.connect(texture_popup.show)
        right_toolbar.addWidget(button_4)

        self.addToolBar(QtCore.Qt.RightToolBarArea, right_toolbar)

    def open(self, filename):  # allows loading via drag & drop
        raw_filename, extension = os.path.splitext(filename)
        short_filename = os.path.basename(filename)
        if extension == ".vmf":
            tab = workspace.VmfTab(filename, new=False, parent=self)
        elif extension == ".qph":
            raise NotImplementedError("No .qph viewport tabs yet")
            # tab = workspace.QphTab(filename, new=False, parent=self)
        else:
            raise RuntimeError(f"{filename} is not a .vmf file")
        self.tabs.addTab(tab, short_filename)
        self.tabs.setCurrentIndex(self.tabs.count() - 1)
