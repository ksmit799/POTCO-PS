from panda3d.core import *
from pirates.util.PythonUtilPOD import clampScalar
from pirates.util.PythonUtil import lerp
from direct.gui.DirectGui import DGG, DirectFrame, DirectLabel, DirectSlider, DirectEntry, DirectButton
from direct.gui.OnscreenText import OnscreenText
import sys

class RangeSlider(DirectFrame):
    
    def __init__(self, label = '', range = (0, 1), command = None, value = 0.0, orientation = DGG.HORIZONTAL, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **args)
        self.initialiseoptions(self.__class__)
        self.setup(label, range, value, orientation, *args, **args)
        self['command'] = command

    
    def __setitem__(self, key, value):
        if key == 'command':
            
            def finalCommand():
                val = self.slider['value']
                self.slider['text'] = '%1.3f' % val
                if value:
                    value(val)
                

            self.slider['command'] = finalCommand
        elif key == 'value':
            self.slider['value'] = value
        elif key == 'range':
            self.slider['range'] = value
        else:
            super(self.__class__, self).__setitem__(key, value)

    
    def __getitem__(self, key):
        if key == 'command':
            return self.slider['command']
        elif key == 'value':
            return self.slider['value']
        elif key == 'range':
            return self.slider['range']
        else:
            return super(self.__class__, self).__getitem__(key)

    
    def setup(self, label, range, value, orientation, *args, **kwargs):
        
        def updateField(widget, field, value):
            widget[field] = value

        
        def finalCommand():
            val = self.slider['value']
            updateField(self.slider, 'text', '%1.3f' % val)

        self.slider = DirectSlider(parent = self, relief = DGG.FLAT, range = range, value = value, orientation = orientation, scale = 0.25, thumb_relief = DGG.FLAT, thumb_color = (0, 1, 1, 1), pos = (0, 0, 0), text = '0.0', text_scale = 0.20000000000000001, text_pos = (0, 0.10000000000000001, 0))
        updateField(self.slider, 'command', finalCommand)
        width = 3
        if orientation == DGG.HORIZONTAL:
            pos = (-0.27500000000000002 - width * 0.050000000000000003, 0, -0.02)
        else:
            pos = (-0.025000000000000001 * width, 0, -0.34999999999999998)
        self.min = DirectEntry(parent = self, initialText = `float(self.slider['range'][0])`, scale = 0.050000000000000003, width = width, pos = pos)
        updateField(self.min, 'command', lambda x: updateField(self.slider, 'range', (float(x), self.slider['range'][1])))
        if orientation == DGG.HORIZONTAL:
            pos = (0.27500000000000002, 0, -0.02)
        else:
            pos = (-0.025000000000000001 * width, 0, 0.29999999999999999)
        self.max = DirectEntry(parent = self, initialText = `float(self.slider['range'][1])`, scale = 0.050000000000000003, width = width, pos = pos)
        updateField(self.max, 'command', lambda x: updateField(self.slider, 'range', (self.slider['range'][0], float(x))))
        self.label = DirectLabel(parent = self, relief = None, text = label, text_scale = 0.050000000000000003, text_pos = (0.029999999999999999 - 0.39500000000000002, 0.34999999999999998 - 0.23999999999999999, 0), text_align = TextNode.ALeft)



class MapConfig(DirectFrame):
    
    def __init__(self, *args, **kwargs):
        kwargs['suppressMouse'] = 0
        super(self.__class__, self).__init__(*args, **args)
        self.initialiseoptions(self.__class__)
        self.setTransparency(1)
        self.setup()

    
    def setup(self):
        if hasattr(self, 'mainFrame'):
            self.mainFrame.destroy()
        
        self.mainFrame = DirectFrame(parent = self, relief = None)
        
        def setVisibility():
            value = self.visSlider['value']
            self.setColorScale(Vec4(1, 1, 1, value))

        self.visSlider = DirectSlider(guiId = 'visSlider', parent = self.mainFrame, scale = 0.40000000000000002, thumb_relief = DGG.FLAT, thumb_color = (0.25, 1.0, 0.25, 1), pos = (0.40000000000000002, 0, -0.84999999999999998), text = 'Visibility', text_scale = 0.20000000000000001, text_pos = (0, 0.10000000000000001, 0), text_bg = (0.80000000000000004, 0.80000000000000004, 0.80000000000000004, 1), value = 1.0, command = setVisibility)
        self.visSlider.getChild(0).setTransparency(0)
        self.camFrame = DirectFrame(guiId = 'camFrame', parent = self.mainFrame, relief = DGG.RIDGE, frameSize = (0.0, 0.80000000000000004, 0.0, 0.32000000000000001), frameColor = (1, 1, 0.75, 1), borderWidth = (0.0050000000000000001, 0.0050000000000000001), pos = (0, 0, 0.59999999999999998), text = 'Camera', text_fg = (0, 0, 0, 1), text_scale = 0.050000000000000003, text_pos = (0.10000000000000001, 0.26000000000000001, 0))
        self.camSlider = RangeSlider(guiId = 'zoom', label = 'Zoom (Y-axis)', range = (-0.75, 0.25), value = 0, parent = self.camFrame, pos = (0.39500000000000002, 0, 0.070000000000000007))
        self.worldFrame = DirectFrame(guiId = 'worldFrame', parent = self.mainFrame, relief = DGG.RIDGE, frameSize = (0.0, 0.80000000000000004, -0.55000000000000004, 0.5), frameColor = (1, 0.75, 0.75, 1), borderWidth = (0.0050000000000000001, 0.0050000000000000001), pos = (0.0, 0, 0), text = 'World', text_fg = (0, 0, 0, 1), text_scale = 0.050000000000000003, text_pos = (0.10000000000000001, 0.42999999999999999, 0))
        self.worldPSlider = RangeSlider(guiId = 'worldP', label = 'World P', range = (-90, 0), value = 0.0, parent = self.worldFrame, pos = (0.39500000000000002, 0, 0.23999999999999999))
        self.worldDecorScaleSlider = RangeSlider(guiId = 'worldP', label = 'World Decor Scale', range = (0.20000000000000001, 0.29999999999999999), value = 0.25, parent = self.worldFrame, pos = (0.39500000000000002, 0, 0.0))
        self.finalSlider = RangeSlider(guiId = 'final', label = 'Final', range = (0, 1), value = 0, parent = self.worldFrame, pos = (0.39500000000000002, 0, -0.47999999999999998))
        self.saveState0Button = DirectButton(guiId = 'save0Button', parent = self.mainFrame, scale = 0.10000000000000001, pos = (0.20000000000000001, 0, -0.65000000000000002), borderWidth = (0.10000000000000001, 0.10000000000000001), text = 'save pt0')
        self.saveState1Button = DirectButton(guiId = 'save1Button', parent = self.mainFrame, scale = 0.10000000000000001, pos = (0.59999999999999998, 0, -0.65000000000000002), borderWidth = (0.10000000000000001, 0.10000000000000001), text = 'save pt1')


