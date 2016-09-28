# File: P (Python 2.4)

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from pirates.piratesgui import PDialog
from pirates.piratesgui import SocialPage
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui.RequestButton import RequestButton

class PVPInviteeButton(RequestButton):
    
    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(PVPInviteeButton)



class PVPInvitee(SocialPage.SocialPage):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPInvitee')
    
    def __init__(self, avId, avName):
        SocialPage.SocialPage.__init__(self, 'PVPInvitee')
        self.initialiseoptions(PVPInvitee)
        self.setPos(-0.59999999999999998, 0, 0.46999999999999997)
        self.avId = avId
        self.avName = avName
        guiMain = loader.loadModel('models/gui/gui_main')
        self.box = OnscreenImage(parent = self, pos = (0.25, 0, 0.27500000000000002), image = guiMain.find('**/general_frame_e'), scale = 0.25)
        self.title = DirectLabel(parent = self, relief = None, text = PLocalizer.PVPInviteeTitle, text_scale = PiratesGuiGlobals.TextScaleExtraLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_font = PiratesGlobals.getPirateOutlineFont(), pos = (0.25, 0, 0.41999999999999998), image = None, image_scale = 0.25)
        text = PLocalizer.PVPInviteeInvitation % self.avName
        self.message = DirectLabel(parent = self, relief = None, text = text, text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 11, pos = (0.25, 0, 0.32500000000000001), textMayChange = 1)
        self.bOk = PVPInviteeButton(text = OTPLocalizer.DialogOK, command = self._PVPInvitee__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.10000000000000001, 0, 0.10000000000000001)
        self.bNo = PVPInviteeButton(text = OTPLocalizer.DialogNo, command = self._PVPInvitee__handleNo)
        self.bNo.reparentTo(self)
        self.bNo.setPos(0.29999999999999999, 0, 0.10000000000000001)
        self.accept('cancelChallengeInvitation', self._PVPInvitee__handleCancelFromAbove)

    
    def destroy(self):
        if hasattr(self, 'destroyed'):
            return None
        
        self.destroyed = 1
        self.ignore('cancelChallengeInvitation')
        GuiPanel.GuiPanel.destroy(self)

    
    def _PVPInvitee__handleOk(self):
        base.cr.pvpManager.sendAcceptChallenge(self.avId)
        self.destroy()

    
    def _PVPInvitee__handleNo(self):
        self.destroy()

    
    def _PVPInvitee__handleCancelFromAbove(self):
        self.destroy()


