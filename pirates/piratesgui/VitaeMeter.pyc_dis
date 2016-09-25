# File: V (Python 2.4)

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui.DialMeter import DialMeter
from pirates.piratesgui.BorderFrame import BorderFrame

class VitaeMeter(DirectFrame):
    
    def __init__(self, parent, **kw):
        DirectFrame.__init__(self, parent, **None)
        self.initialiseoptions(VitaeMeter)
        toplevel_gui = loader.loadModel('models/gui/toplevel_gui')
        self.vitaeDial = DialMeter(parent = self, meterColor = Vec4(0.80000000000000004, 0.20000000000000001, 0.20000000000000001, 1), baseColor = Vec4(0, 0, 0, 1), scale = 0.28000000000000003)
        icon = toplevel_gui.find('**/morale_skull*')
        self.vitaeIcon = DirectFrame(parent = self, state = DGG.NORMAL, relief = None, image = icon, image_scale = 0.625)
        detailLabel = DirectLabel(relief = None, state = DGG.DISABLED, text = PLocalizer.VitaeDesc, text_align = TextNode.ALeft, text_scale = PiratesGuiGlobals.TextScaleExtraLarge, text_fg = PiratesGuiGlobals.TextFG1, text_wordwrap = 15, text_shadow = (0, 0, 0, 1), pos = (0.0, 0, -0.025000000000000001), textMayChange = 0, sortOrder = 91)
        height = -(detailLabel.getHeight() + 0.01)
        width = max(0.25, detailLabel.getWidth() + 0.040000000000000001)
        self.helpBox = BorderFrame(parent = self, state = DGG.DISABLED, modelName = 'general_frame_f', frameSize = (-0.040000000000000001, width, height, 0.050000000000000003), pos = (0.050000000000000003, 0, -0.050000000000000003), sortOrder = 90)
        detailLabel.reparentTo(self.helpBox)
        self.helpBox.hide()
        self.helpBox.setClipPlaneOff()
        self.meterLabel = DirectLabel(parent = self.vitaeDial, relief = None, pos = (0, 0, -0.45000000000000001), text = PLocalizer.Vitae, text_scale = 0.20000000000000001, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_font = PiratesGlobals.getPirateOutlineFont(), textMayChange = 1)
        self.vitaeIcon.bind(DGG.WITHIN, self.showDetails)
        self.vitaeIcon.bind(DGG.WITHOUT, self.hideDetails)

    
    def showDetails(self, event):
        self.helpBox.show()

    
    def hideDetails(self, event):
        self.helpBox.hide()

    
    def update(self, level, range, val):
        self.vitaeDial.hide()
        Range = range * 1.0009999999999999
        if level > 0:
            self.vitaeDial.update(val, Range)
            self.vitaeDial.show()
        


