# File: C (Python 2.4)

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.band import BandConstance
from pirates.piratesgui.RequestButton import RequestButton

class CrewBootButton(RequestButton):
    
    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(CrewBootButton)



class CrewBoot(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('CrewBoot')
    
    def __init__(self, avId, avName):
        guiMain = loader.loadModel('models/gui/gui_main')
        DirectFrame.__init__(self, relief = None, pos = (-0.59999999999999998, 0, 0.46999999999999997), image = guiMain.find('**/general_frame_e'), image_pos = (0.25, 0, 0.27500000000000002), image_scale = 0.25)
        self.initialiseoptions(CrewBoot)
        self.avId = avId
        self.avName = avName
        self.title = DirectLabel(parent = self, relief = None, text = PLocalizer.CrewBootTitle, text_scale = PiratesGuiGlobals.TextScaleExtraLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_font = PiratesGlobals.getPirateOutlineFont(), pos = (0.25, 0, 0.41999999999999998))
        text = PLocalizer.CrewBootMessage % self.avName
        self.message = DirectLabel(parent = self, relief = None, text = text, text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 11, pos = (0.25, 0, 0.32500000000000001), textMayChange = 1)
        self.bOk = CrewBootButton(text = PLocalizer.CrewBootOK, command = self._CrewBoot__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.10000000000000001, 0, 0.050000000000000003)
        self.bNo = CrewBootButton(text = PLocalizer.CrewBootNo, command = self._CrewBoot__handleNo)
        self.bNo.reparentTo(self)
        self.bNo.setPos(0.29999999999999999, 0, 0.050000000000000003)

    
    def destroy(self):
        if hasattr(self, 'destroyed'):
            return None
        
        self.destroyed = 1
        self.ignore('Esc')
        DirectFrame.destroy(self)

    
    def _CrewBoot__handleOk(self):
        base.cr.PirateBandManager.d_requestBoot(self.avId)
        self.destroy()

    
    def _CrewBoot__handleNo(self):
        self.destroy()

    
    def _CrewBoot__handleCancelFromAbove(self):
        self.destroy()


