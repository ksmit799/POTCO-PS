from direct.gui.DirectGui import *
from panda3d.core import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.band import BandConstance
from pirates.piratesgui.RequestButton import RequestButton

class CrewInviteeButton(RequestButton):
    
    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(CrewInviteeButton)



class CrewInvitee(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('CrewInvitee')
    
    def __init__(self, avId, avName):
        guiMain = loader.loadModel('models/gui/gui_main')
        DirectFrame.__init__(self, relief = None, pos = (-0.59999999999999998, 0, 0.46999999999999997), image = guiMain.find('**/general_frame_e'), image_pos = (0.25, 0, 0.27500000000000002), image_scale = 0.25)
        guiMain.removeNode()
        self.initialiseoptions(CrewInvitee)
        self.avId = avId
        self.avName = avName
        if base.cr.avatarFriendsManager.checkIgnored(self.avId):
            self._CrewInvitee__handleNo()
            return None
        
        self.title = DirectLabel(parent = self, relief = None, text = PLocalizer.CrewInviteeTitle, text_scale = PiratesGuiGlobals.TextScaleExtraLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_font = PiratesGlobals.getPirateOutlineFont(), pos = (0.25, 0, 0.41999999999999998), image = None, image_scale = 0.25)
        nameArray = ('\x01CPOrangeHEAD\x01' + self.avName + '\x02', '\x01CPOrangeHEAD\x01' + self.avName + '\x02', '\x01CPOrangeOVER\x01' + self.avName + '\x02', '\x01CPOrangeHEAD\x01' + self.avName + '\x02')
        nameButton = DirectButton(parent = NodePath(), relief = None, text = nameArray, text_align = TextNode.ALeft, text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 0, command = self.handleAvatarPress, extraArgs = [
            avId,
            avName])
        (left, right, bottom, top) = nameButton.getBounds()
        nameGFX = TextGraphic(nameButton, left, right, 0, 1)
        buttonName = '\x05' + self.avName + '\x05'
        buttonText = PLocalizer.CrewInviteeInvitation % buttonName
        tpMgr = TextPropertiesManager.getGlobalPtr()
        tpMgr.setGraphic(self.avName, nameGFX)
        del tpMgr
        textRender = TextNode('textRender')
        textRender.setFont(PiratesGlobals.getInterfaceFont())
        textRender.setTextColor(PiratesGuiGlobals.TextFG2)
        textRender.setAlign(TextNode.ACenter)
        textRender.setShadowColor(PiratesGuiGlobals.TextShadow)
        textRender.setWordwrap(11)
        textRender.setTabWidth(1.0)
        textRender.setShadow(0.080000000000000002, 0.080000000000000002)
        textRender.setText(buttonText)
        textNode = self.attachNewNode(textRender.generate())
        textNode.setScale(PiratesGuiGlobals.TextScaleLarge)
        textNode.setPos(0.25, 0, 0.32500000000000001)
        self.bOk = CrewInviteeButton(text = PLocalizer.CrewInviteeOK, command = self._CrewInvitee__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.10000000000000001, 0, 0.050000000000000003)
        self.bNo = CrewInviteeButton(text = PLocalizer.CrewInviteeNo, command = self._CrewInvitee__handleNo)
        self.bNo.reparentTo(self)
        self.bNo.setPos(0.29999999999999999, 0, 0.050000000000000003)
        self.accept('BandRequestCancel-%s' % (self.avId,), self._CrewInvitee__handleCancelFromAbove)

    
    def destroy(self):
        if hasattr(self, 'destroyed'):
            return None
        
        self.destroyed = 1
        self.ignore('BandRequestCancel-%s' % (self.avId,))
        self.ignore('Esc')
        DirectFrame.destroy(self)

    
    def _CrewInvitee__handleOk(self):
        base.cr.PirateBandManager.d_invitationResponce(self.avId, self.avName, BandConstance.outcome_ok)
        self.destroy()

    
    def _CrewInvitee__handleNo(self):
        base.cr.PirateBandManager.d_invitationResponce(self.avId, self.avName, BandConstance.outcome_declined)
        self.destroy()

    
    def _CrewInvitee__handleCancelFromAbove(self):
        self.destroy()

    
    def handleAvatarPress(self, avId, avName):
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            base.localAvatar.guiMgr.handleAvatarDetails(avId, avName)
        


