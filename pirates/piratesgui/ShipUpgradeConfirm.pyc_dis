# File: S (Python 2.4)

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui.RequestButton import RequestButton

class PiratesConfirmButton(RequestButton):
    
    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(PiratesConfirmButton)



class ShipUpgradeConfirm(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesConfirm')
    
    def __init__(self, title, message, commandOkay, commandCancel, titleScale = PiratesGuiGlobals.TextScaleExtraLarge):
        guiMain = loader.loadModel('models/gui/gui_main')
        DirectFrame.__init__(self, relief = None, pos = (-0.59999999999999998, 0, 0.46999999999999997), image = guiMain.find('**/general_frame_e'), image_pos = (0.25, 0, 0.27500000000000002), image_scale = 0.25)
        self.initialiseoptions(ShipUpgradeConfirm)
        self.setBin('gui-fixed', 0)
        self.commandOkay = commandOkay
        self.commandCancel = commandCancel
        self.title = DirectLabel(parent = self, relief = None, text = title, text_scale = titleScale, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_font = PiratesGlobals.getPirateOutlineFont(), pos = (0.25, 0, 0.41999999999999998), image = None, image_scale = 0.25)
        text = message
        self.message = DirectLabel(parent = self, relief = None, text = message, text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 11, pos = (0.25, 0, 0.32500000000000001), textMayChange = 1)
        self.bOk = PiratesConfirmButton(text = PLocalizer.GenericConfirmOK, command = self._ShipUpgradeConfirm__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.10000000000000001, 0, 0.050000000000000003)
        self.bNo = PiratesConfirmButton(text = PLocalizer.GenericConfirmNo, command = self._ShipUpgradeConfirm__handleNo)
        self.bNo.reparentTo(self)
        self.bNo.setPos(0.29999999999999999, 0, 0.050000000000000003)

    
    def destroy(self):
        if hasattr(self, 'destroyed'):
            return None
        
        self.destroyed = 1
        self.ignore('Esc')
        DirectFrame.destroy(self)

    
    def _ShipUpgradeConfirm__handleOk(self):
        if self.commandOkay:
            self.commandOkay()
        
        self.destroy()

    
    def _ShipUpgradeConfirm__handleNo(self):
        if self.commandCancel:
            self.commandCancel()
        
        self.destroy()


