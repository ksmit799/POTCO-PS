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

class CrewRejoinButton(RequestButton):
    
    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(CrewRejoinButton)



class CrewRejoin(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('CrewRejoin')
    
    def __init__(self, avId, isManager, version):
        guiMain = loader.loadModel('models/gui/gui_main')
        DirectFrame.__init__(self, relief = None, pos = (-0.25, 0, -0.14999999999999999), image = guiMain.find('**/general_frame_e'), image_pos = (0.25, 0, 0.27500000000000002), image_scale = 0.25)
        self.initialiseoptions(CrewRejoin)
        self.avId = avId
        self.isManager = isManager
        self.version = version
        if base.cr.avatarFriendsManager.checkIgnored(self.avId):
            self._CrewRejoin__handleNo()
            return None
        
        titleUI = loader.loadModel('models/gui/ship_battle')
        guiMain = loader.loadModel('models/gui/gui_main')
        self.title = DirectLabel(parent = self, relief = None, text = PLocalizer.CrewRejoinTitle, text_scale = PiratesGuiGlobals.TextScaleExtraLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_font = PiratesGlobals.getPirateOutlineFont(), pos = (0.25, 0, 0.41999999999999998), image_scale = 0.25)
        if version == 2:
            text = PLocalizer.CrewRejoinParlorInvitation
        elif version == 1:
            text = PLocalizer.CrewRejoinPVPInvitation
        else:
            text = PLocalizer.CrewRejoinInvitation
        self.message = DirectLabel(parent = self, relief = None, text = text, text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 11, pos = (0.25, 0, 0.32500000000000001), textMayChange = 1)
        self.bOk = CrewRejoinButton(text = PLocalizer.CrewRejoinOK, command = self._CrewRejoin__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.10000000000000001, 0, 0.050000000000000003)
        self.bNo = CrewRejoinButton(text = PLocalizer.CrewRejoinNo, command = self._CrewRejoin__handleNo)
        self.bNo.reparentTo(self)
        self.bNo.setPos(0.29999999999999999, 0, 0.050000000000000003)
        self.accept('BandRejoinCancel-%s' % (self.avId,), self._CrewRejoin__handleCancelFromAbove)

    
    def destroy(self):
        if hasattr(self, 'destroyed'):
            return None
        
        self.destroyed = 1
        self.ignore('BandRejoinCancel-%s' % (self.avId,))
        self.ignore('Esc')
        DirectFrame.destroy(self)

    
    def _CrewRejoin__handleOk(self):
        if self.version == 2:
            base.localAvatar.d_setBandParlor(0)
        elif self.version == 1:
            base.localAvatar.d_setBandPvp(0)
        
        base.cr.PirateBandManager.d_rejoinResponce(self.avId, self.isManager, BandConstance.outcome_ok)
        self.destroy()

    
    def _CrewRejoin__handleNo(self):
        base.cr.PirateBandManager.d_rejoinResponce(self.avId, self.isManager, BandConstance.outcome_declined)
        self.destroy()

    
    def _CrewRejoin__handleCancelFromAbove(self):
        self.destroy()


