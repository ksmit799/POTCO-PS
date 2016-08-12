import math
import random
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.task import Task
from direct.showbase.DirectObject import DirectObject
from otp.otpbase import OTPRender

class DependencyArray:
    
    def __init__(self, createCallback):
        self.state = False
        self.createCallback = createCallback
        self.array = []

    
    def enable(self, enable):
        self.state = enable

    
    def addDependency(self, item):
        self.array.append(item)

    
    def removeDependency(self, item):
        if item and item in self.array:
            self.array.remove(item)
        

    
    def checkDependencies(self):
        state = False
        if self.array:
            state = True
            length = len(self.array)
            for i in range(length):
                item = self.array[i]
                if item.created == False:
                    state = False
                    break
                    continue
            
            if state and self.state:
                self.createCallback()
            
        
        return state

    
    def delete(self):
        if self.array:
            length = len(self.array)
            for i in range(length):
                item = self.array[i]
                if item:
                    self.array[i] = None
                    item = None
                    continue
            
            self.array = None
        



class RenderToTexture(DirectObject):
    
    def __init__(self, rtt_name, width = 512, height = 512, order = 0, format = 0, clear_color = Vec4(0.0, 0.0, 0.0, 1.0), dependency_array = None):
        self.rtt_name = rtt_name
        self.width = width
        self.height = height
        self.order = order
        self.format = format
        self.clear_color = clear_color
        self.texture_buffer = None
        self.camera_node_path = None
        self.card = None
        self.card_parent = None
        self.card_shader = None
        self.created = False
        self.dependency_arrays = []
        if dependency_array:
            self.dependency_arrays.append(dependency_array)
            dependency_array.addDependency(self)
        
        if self._RenderToTexture__createBuffer():
            self.accept('close_main_window', self._RenderToTexture__destroyBuffer)
            self.accept('open_main_window', self._RenderToTexture__createBuffer)
        

    
    def addDependencyArray(self, array):
        if array:
            self.dependency_arrays.append(array)
        

    
    def removeDependencyArray(self, array):
        if array and array in self.dependency_arrays:
            self.dependency_arrays.remove(array)
        

    
    def enable(self, enable):
        if enable:
            if self.texture_buffer:
                self.texture_buffer.setActive(1)
            
        elif self.texture_buffer:
            self.texture_buffer.setActive(0)
        

    
    def getTextureBuffer(self):
        return self.texture_buffer

    
    def saveCamera(self, camera):
        self.camera_node_path = camera

    
    def saveCard(self, card):
        self.card = card

    
    def _RenderToTexture__destroyBuffer(self):
        if self.camera_node_path:
            self.camera_node_path.removeNode()
            self.camera_node_path = None
        
        if self.card:
            self.card.removeNode()
            self.card = None
        
        if self.texture_buffer:
            self.texture_buffer.setActive(False)
            base.graphicsEngine.removeWindow(self.texture_buffer)
        
        self.texture_buffer = None
        self.created = False

    
    def _RenderToTexture__createBuffer(self):
        state = False
        self._RenderToTexture__destroyBuffer()
        texture_buffer = base.win.makeTextureBuffer(self.rtt_name, self.width, self.height)
        if texture_buffer:
            texture_buffer.setClearColor(self.clear_color)
            texture_buffer.setSort(self.order)
            if self.format:
                texture = texture_buffer.getTe