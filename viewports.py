# try qopengl to keep dependecies simple & multi-platform
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
from OpenGL.GLU import *
from PyQt5 import QtCore, QtGui, QtWidgets

import sys
sys.path.insert(0, 'utilities') # there has to be a better way to load these
import camera
import physics
import vmf_tool
import vector
import solid_tool # must be loaded AFTER vmf_tool (how do dependencies work?)

view_modes = ['flat', 'textured', 'wireframe']
# "silhouette" view mode, lights on black brushwork & props

class Viewport2D(QtWidgets.QOpenGLWidget):
    def __init__(self, fps=30, parent=None):
        super(Viewport2D, self).__init__(parent)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000 / fps)
        self.dt = 1 / fps # will desynchronise
        self.fps = fps
##        self.drawcalls = {}
##        # buffer: {shader: [[index_start, index_len], ...]}
##        # all GL_TRIANGLES
        # set render resolution?
        self.camera = camera.freecam(None, None, 128)
        ### BUFFERS ###
        # HELPER MODELS: (static draw)
        # shared app-wide
        # modelname: index(start, len)
        # BRUSHES: (dynamic draw)
        # brush index: vertex(start, len), index(start, len)
        # vertex buffer len
        # index buffer len
        # MODELS: (dynamic draw)
        # modelname: vertex(start, len), index(start, len)

    def executeGL(self, func, *args, **kwargs):
        """Execute func(self, *args, **kwargs) in this viewport's glContext"""
        self.makeCurrent()
        func(self, *args, **kwargs)
        self.doneCurrent()

    def resizeGL(self, width, height):
        x_scale = width / height
        glLoadIdentity()
        glOrtho(-x_scale, x_scale, -1, 1, 0, 1024)

    def initializeGL(self):
        glClearColor(0, 0, 0, 0)
        # glEnables
        glColor(.75, .75, .75)
        if self.fps != 30: # for 2d
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def sharedGLsetup(self): # call manually in one viewport once all are made
        """Sets up buffers, textures & shaders shared across many viewports"""
        self.makeCurrent()
        glEnable(GL_TEXTURE_2D)
        black = b'\xFF\xAF\x00\x00'
        purple = b'\x00\xFF\xAF\x00'
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 2, 2, 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, black + purple + purple + black)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glColor(1, 1, 1)
        self.doneCurrent()
##        return buffer_handles, shader_handles, texture_handles

    def paintGL(self): # how do we use Qt OpenGL functions?
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glRotate(self.dt * 90, 0, 0, 1)
        glBegin(GL_TRIANGLES)
        glTexCoord(1, 0)
        glVertex(1, 0, 0)
        glTexCoord(-1, 0)
        glVertex(-1, 0, 0)
        glTexCoord(0, 1)
        glVertex(0, 1, 0)
        glEnd()

        glEnableClientState(GL_VERTEX_ARRAY)
        a = [[-.5, .5], [.5, .5], [.5, -.5], [-.5, -.5]]
        glVertexPointerf(a)
        glDrawArrays(GL_POLYGON, 0, len(a))
        glFlush()

    def update(self):
        super(Viewport2D, self).update()
        # update animations (TICKS)
        # just to keep logic seperate
        # super().update() calls paintGL


class Viewport3D(Viewport2D):
    def __init__(self, fps=30, view_mode='flat', parent=None):
        super(Viewport3D, self).__init__(fps=fps, parent=parent)
        self.view_mode = view_mode
        self.fov = 90 # how do users change this?
        self.camera_moving = False
        self.camera_keys = list()
    
    def changeViewMode(self, view_mode): # overlay viewmode button
        if self.view_mode == view_mode:
            return # exit, no changes needed
        if self.view_mode == 'wireframe':
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        if view_mode == 'textured':
            glEnable(GL_TEXTURE_2D)
        else:
            glDisable(GL_TEXTURE_2D)
        if view_mode == 'wireframe':
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            return # polygon mode, shaders off, textures off
        # change shader to flat (flat / wireframe)
        # or to complex (textured)

    def keyPressEvent(self, event):
        self.keys += event.key()
        if event.key() == QtCore.Qt.Key_Z:
            self.camera_moving = False if self.camera_moving else True
            if self.camera_moving == True:
                print('camera moving')
            else:
                print('camera stopped')

    def initializeGL(self):
        glClearColor(0, 0, 0, 0)
        # find width & height before calling
        gluPerspective(90, self.width() / self.height(), 0.1, 4096 * 4)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glFrontFace(GL_CW)
        glPointSize(4)

    def paintGL(self):
        # gluPerspective
        # rotate camera
        # draw skybox
        # translate
        glPushMatrix()
        glLineWidth(1)
        glBegin(GL_LINES)
        glColor(1, 0, 0)
        glVertex(0, 0, 0)
        glVertex(128, 0, 0)
        glColor(0, 1, 0)
        glVertex(0, 0, 0)
        glVertex(0, 128, 0)
        glColor(0, 0, 1)
        glVertex(0, 0, 0)
        glVertex(0, 0, 128)
        glEnd()
        glPopMatrix()

    def resizeGL(self, width, height):
        self.makeCurrent()
        gluPerspective(self.fov, width / height, 0.1, 1024)
        self.doneCurrent()

    def update(self):
        if self.camera_moving:
            # need to sample mouse vector (relative updates)
            self.camera.update(self.mouse, self.keys, self.dt)


# dock widget containing grid?
# docked tabs?
# QTabWidget.addTab(MapDock)
def class MapDock(QtWidgets.QDockWidget):
    def __init__(self, parent):
        super(QuadView, self).__init__(parent)
        quad_layout = QtWidgets.QGridLayout()
        for y in range(2):
            for x in range(2):
                if x == 0 and y == 0:
                    quad_layout.addWidget(Viewport3D(30), x, y)
                else:
                    quad_layout.addWidget(Viewport2D(15), x, y)
        self.setLayout(quad_layout)
    # 4 viewports
    # .vmf
    # buffers
    # camera(s)
    # shaders
    ,,,

if __name__ == "__main__":
    import sys

    def except_hook(cls, exception, traceback):
        sys.__excepthook__(cls, exception, traceback)

    sys.excepthook = except_hook
    # ^^^ for python debugging inside Qt ^^^ #
    
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    window.setGeometry(256, 256, 512, 512)
    quad_view = QtWidgets.QGridLayout()
    for y in range(2):
        for x in range(2):
            if x == 0 and y == 0:
                quad_view.addWidget(Viewport3D(30), x, y)
            else:
                quad_view.addWidget(Viewport2D(15), x, y)
    window.setLayout(quad_view)
    window.show()
    # need initializeGL called by the viewport we setup
    # so the window must be shown FIRST to call initGL
    quad_view.itemAtPosition(0, 0).widget().sharedGLsetup()
    
    sys.exit(app.exec_())