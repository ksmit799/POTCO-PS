# File: S (Python 2.4)

from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import sys
import gc

class SceneBuffer(DirectObject):
    
    def __init__(self, name, size = Vec2(512, 512) * 2.0, camAspectRatio = 1.0, clearColor = Vec4(0.84999999999999998, 0.84999999999999998, 0.84999999999999998, 1.0), sceneGraph = None):
        DirectObject.__init__(self)
        self.name = name
        self.size = size
        if not sceneGraph:
            self._SceneBuffer__sceneGraph = NodePath(self.name + '-render')
        else:
            self._SceneBuffer__sceneGraph = sceneGraph
        self.camera = self._SceneBuffer__sceneGraph.attachNewNode(Camera(self.name + 'camera'))
        self.camNode = self.camera.node()
        self.camLens = PerspectiveLens()
        self.camLens.setFov(30, 30)
        self.camNode.setLens(self.camLens)
        self._SceneBuffer__texture = Texture(self.name)
        self._SceneBuffer__buffer = None
        self._SceneBuffer__createBuffer()
        self.accept('close_main_window', self._SceneBuffer__destroyBuffer)
        self.accept('open_main_window', self._SceneBuffer__createBuffer)

    
    def _SceneBuffer__destroyBuffer(self):
        if self._SceneBuffer__buffer:
            base.graphicsEngine.removeWindow(self._SceneBuffer__buffer)
            self._SceneBuffer__buffer = None
        

    
    def _SceneBuffer__createBuffer(self):
        self._SceneBuffer__destroyBuffer()
        self._SceneBuffer__buffer = base.win.makeTextureBuffer(self.name, self.size[0], self.size[1], tex = self._SceneBuffer__texture)
        dr = self._SceneBuffer__buffer.makeDisplayRegion()
        dr.setCamera(self.camera)

    
    def getSceneRoot(self):
        return self._SceneBuffer__sceneGraph

    
    def getTexture(self):
        return self._SceneBuffer__texture

    
    def getTextureCard(self):
        if self._SceneBuffer__buffer:
            return self._SceneBuffer__buffer.getTextureCard()
        
        return NodePath('empty')

    
    def destroy(self):
        self.disable()
        self.camera = None
        self.camLens = None
        self._SceneBuffer__sceneGraph = None
        self._SceneBuffer__texture = None
        self._SceneBuffer__destroyBuffer()
        self.ignore('close_main_window')
        self.ignore('open_main_window')

    
    def enable(self):
        if self._SceneBuffer__buffer:
            self._SceneBuffer__createBuffer()
            self._SceneBuffer__buffer.setActive(True)
        

    
    def disable(self):
        if self._SceneBuffer__buffer:
            self._SceneBuffer__buffer.setActive(False)
        


