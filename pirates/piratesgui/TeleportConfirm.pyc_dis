# File: T (Python 2.4)

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals
from pirates.piratesgui import PDialog
from pirates.piratesgui import SocialPage
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.band import BandConstance
from pirates.piratesgui.RequestButton import RequestButton

class TeleportConfirmButton(RequestButton):
    
    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(TeleportConfirmButton)



class TeleportConfirm(SocialPage.SocialPage):
    notify = DirectNotifyGlobal.directNotify.newCategory('TeleportConfirm')
    
    def __init__(self, avId, avName):
        SocialPage.SocialPage.__init__(self, 'TeleportConfirm')
        self.initialiseoptions(TeleportConfirm)
        self.setPos(-0.25, 0, -0.14999999999999999)
        self.avId = avId
        self.avName = avName
        if base.cr.avatarFriendsManager.checkIgnored(self.avId):
            self._TeleportConfirm__handleNo()
            return None
        
        guiMain = loader.loadModel('models/gui/gui_main')
        self.box = OnscreenImage(parent = self, pos = (0.25, 0, 0.27500000000000002), image = guiMain.find('**/general_frame_e'), scale = 0.25)
        self.title = DirectLabel(parent = self, relief = None, text = PLocalizer.TeleportConfirmTitle, text_scale = PiratesGuiGlobals.TextScaleExtraLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_font = PiratesGlobals.getPirateOutlineFont(), pos = (0.25, 0, 0.41999999999999998))
        text = PLocalizer.TeleportConfirmMessage % self.avName
        self.message = DirectLabel(parent = self, relief = None, text = text, text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 11, pos = (0.25, 0, 0.32500000000000001), textMayChange = 1)
        self.bOk = TeleportConfirmButton(text = PLocalizer.TeleportConfirmOK, command = self._TeleportConfirm__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.10000000000000001, 0, 0.050000000000000003)
        self.bNo = TeleportConfirmButton(text = PLocalizer.TeleportConfirmNo, command = self._TeleportConfirm__handleNo)
        self.bNo.reparentTo(self)
        self.bNo.setPos(0.29999999999999999, 0, 0.050000000000000003)
        av = base.cr.getDo(avId)
        if av:
            self.accept(av.getDisableEvent(), self._TeleportConfirm__handleAvatarLeft)
        

    
    def destroy(self):
        if hasattr(self, 'destroyed'):
            return None
        
        self.destroyed = 1
        self.ignore('BandRequestCancel-%s' % (self.avId,))
        self.ignore('BandRejoinCancel-%s' % (self.avId,))
        self.ignore('Esc')
        SocialPage.SocialPage.destroy(self)

    
    def _TeleportConfirm__handleOk(self):
        base.localAvatar.guiMgr.handleGotoAvatar(self.avId, self.avName)
        self.destroy()

    
    def _TeleportConfirm__handleNo(self):
        self.destroy()

    
    def _TeleportConfirm__handleAvatarLeft(self):
        if not base.cr.identifyAvatar(self.avId):
            self.destroy()
        


