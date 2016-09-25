# File: P (Python 2.4)

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.band import BandConstance
from pirates.piratesgui.RequestButton import RequestButton

class PiratesConfirmButton(RequestButton):
    
    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(PiratesConfirmButton)



class PiratesConfirm(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesConfirm')
    
    def __init__(self, title, message, command, avId = None, tattoo = None, barber = None, titleScale = PiratesGuiGlobals.TextScaleExtraLarge):
        guiMain = loader.loadModel('models/gui/gui_main')
        DirectFrame.__init__(self, relief = None, pos = (-0.59999999999999998, 0, 0.46999999999999997), image = guiMain.find('**/general_frame_e'), image_pos = (0.25, 0, 0.27500000000000002), image_scale = 0.25)
        self.initialiseoptions(PiratesConfirm)
        self.command = command
        self.avId = avId
        self.tattoo = tattoo
        self.barber = barber
        if avId is not None and base.cr.avatarFriendsManager.checkIgnored(self.avId):
            self._PiratesConfirm__handleNo()
            return None
        
        self.title = DirectLabel(parent = self, relief = None, text = title, text_scale = titleScale, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_font = PiratesGlobals.getPirateOutlineFont(), pos = (0.25, 0, 0.41999999999999998), image = None, image_scale = 0.25)
        text = message
        self.message = DirectLabel(parent = self, relief = None, text = message, text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 11, pos = (0.25, 0, 0.32500000000000001), textMayChange = 1)
        self.bOk = PiratesConfirmButton(text = PLocalizer.GenericConfirmOK, command = self._PiratesConfirm__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.10000000000000001, 0, 0.050000000000000003)
        self.bNo = PiratesConfirmButton(text = PLocalizer.GenericConfirmNo, command = self._PiratesConfirm__handleNo)
        self.bNo.reparentTo(self)
        self.bNo.setPos(0.29999999999999999, 0, 0.050000000000000003)
        self.accept('clientLogout', self.destroy)

    
    def destroy(self):
        if hasattr(self, 'destroyed'):
            return None
        
        self.destroyed = 1
        self.ignore('BandRequestCancel-%s' % (self.avId,))
        self.ignore('BandRejoinCancel-%s' % (self.avId,))
        self.ignore('Esc')
        DirectFrame.destroy(self)

    
    def _PiratesConfirm__handleOk(self):
        if self.avId:
            self.command(self.avId)
        elif self.tattoo:
            self.command(self.tattoo[0], self.tattoo[1], self.tattoo[2])
        elif self.barber:
            self.command(self.barber[0], self.barber[1], self.barber[2])
        else:
            self.command()
        self.destroy()

    
    def _PiratesConfirm__handleNo(self):
        self.destroy()

    
    def _PiratesConfirm__handleCancelFromAbove(self):
        self.destroy()


