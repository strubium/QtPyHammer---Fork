"""QtPyHammer Workspace that holds and manages an open .vmf file"""
import enum
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QMouseEvent
from . import viewport, popup
from ..utilities import raycast
from ..ops.vmf import VmfInterface


class SELECTION_MODE(enum.Enum):
    SOLID = 0
    OBJECT = 1
    GROUP = 2
    FACE = 3


class VmfTab(QtWidgets.QWidget):
    """Holds the .vmf data and viewport(s)"""
    def __init__(self, vmf_path, new=True, parent=None):
        super(VmfTab, self).__init__(parent)
        self.filename = vmf_path
        self.never_saved = True if new else False
        self.selection_mode = SELECTION_MODE.GROUP
        self.selection = set()
        # ^ ("type", major_id, minor_id) e.g. ("brush", brush.id, face.id)
        # UI
        layout = QtWidgets.QVBoxLayout()  # holds the viewport
        # ^ 2 QSplitter(s) will be used for quad viewports
        self.viewport = viewport.MapViewport3D(self)
        # self.viewport.setViewMode.connect(...)
        self.viewport.setFocus()  # not working as intended
        layout.addWidget(self.viewport)
        self.setLayout(layout)
        # TODO: viewport splitter(s), toolbar (grid controls etc.),
        # selection mode widget, hotkeys (defined in settings)
        self.map_file = VmfInterface(self, self.filename)
        # ^ define the VmfInterface last so it can connect to everything
        # undo & redo is tied directly to the VmfInterface

    def mousePressEvent(self, event: QMouseEvent):
        """Override the mouse press event to handle selection"""
        if event.button() == QtCore.Qt.LeftButton:
            # Convert the mouse position to normalized device coordinates
            ndc_x = (2.0 * event.x()) / self.viewport.width() - 1.0
            ndc_y = 1.0 - (2.0 * event.y()) / self.viewport.height()

            # Use a raycasting method to find the selection
            ray_origin, ray_direction = viewport.MapViewport3D.do_raycast(self, ndc_x, ndc_y)
            self.select(ray_origin, ray_direction)

    def select(self, ray_origin, ray_direction):
        """Get the object hit by ray"""
        ray_length = self.viewport.render_manager.draw_distance
        ray = raycast.Ray(ray_origin, ray_direction, ray_length)
        objects = self.map_file.get_objects()  # Access objects from VmfInterface
        selection = raycast(ray, objects)
        if selection:
            self.selection.add(selection)
            # TODO: highlight selection in renderer

    def save_to_file(self):
        print(f"Saving {self.filename}... ", end="")
        try:
            # shutil.copy a backup.vmx before saving
            # but not if saving as another filename
            # update self.map_file with:
            # - the camera's location
            # - hidden state of objects (visgroups included)
            self.map_file.save(self.filename)
        except Exception as exc:
            error_popup = popup.browser(parent=self, popuptext="Error", msgtext="Error when saving")
            error_popup.show()
            raise exc
        saved_popup = popup.browser(parent=self, popuptext="Status", msgtext="Saved")
        saved_popup.show()
        self.never_saved = False

    def close(self):
        # TODO: ask the user if they want to save first
        # release used memory eg. self.viewport.render_manager buffers
        super(VmfTab, self).close()
