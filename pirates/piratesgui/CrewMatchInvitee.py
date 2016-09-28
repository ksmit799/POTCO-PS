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

class CrewMatchInviteeButton(RequestButton):
    
    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(CrewMatchInviteeButton)



class CrewMatchInvitee(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('CrewMatchInvitee')
    
    def __init__(self, avId, avName, location, initialRequest = False, crewType = 1):
        guiMain = loader.loadModel('models/gui/gui_main')
        DirectFrame.__init__(self, relief = None, pos = (-0.59999999999999998, 0, 0.46999999999999997), image = guiMain.find('**/general_frame_e'), image_pos = (0.25, 0, 0.27500000000000002), image_scale = 0.25)
        self.initialiseoptions(CrewMatchInvitee)
        self.avId = avId
        self.avName = avName
        self.initialRequest = initialRequest
        self.location = location
        self.crewType = crewType
        self.title = DirectLabel(parent = self, relief = None, text = PLocalizer.CrewMatchCrewLookout, text_scale = PiratesGuiGlobals.TextScaleExtraLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_font = PiratesGlobals.getPirateOutlineFont(), pos = (0.25, 0, 0.41999999999999998), image = None, image_scale = 0.25)
        nameArray = ('\x1CPOrangeHEAD\x1' + self.avName + '\x2', '\x1CPOrangeHEAD\x1' + self.avName + '\x2', '\x1CPOrangeOVER\x1' + self.avName + '\x2', '\x1CPOrangeHEAD\x1' + self.avName + '\x2')
        nameButton = DirectButton(parent = NodePath(), relief = None, text = nameArray, text_align = TextNode.ALeft, text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 0, command = self.handleAvatarPress, extraArgs = [
            avId,
            avName])
        (left, right, bottom, top) = nameButton.getBounds()
        nameGFX = TextGraphic(nameButton, left, right, 0, 1)
        buttonName = '\x5' + self.avName + '\x5'
        if location != '':
            buttonText = PLocalizer.CrewMatchInviteeInvitation % (buttonName, self.location)
        else:
            buttonText = PLocalizer.CrewMatchInviteeInvitationNoLocation % buttonName
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
        self.bOk = CrewMatchInviteeButton(text = PLocalizer.CrewInviteeOK, command = self._CrewMatchInvitee__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.10000000000000001, 0, 0.050000000000000003)
        self.bNo = CrewMatchInviteeButton(text = PLocalizer.CrewInviteeNo, command = self._CrewMatchInvitee__handleNo)
        self.bNo.reparentTo(self)
        self.bNo.setPos(0.29999999999999999, 0, 0.050000000000000003)
        self.accept('clientLogout', self.destroy)
        self.accept('destroyCrewMatchInvite', self.destroy)

    
    def destroy(self):
        if hasattr(self, 'destroyed'):
            return None
        
        self.destroyed = 1
        self.ignore('Esc')
        DirectFrame.destroy(self)

    
    def _CrewMatchInvitee__handleOk(self):
        if self.initialRequest:
            base.cr.crewMatchManager.acceptInitialInviteGUI()
        else:
            base.cr.crewMatchManager.acceptInvite()
            base.cr.crewMatchManager.offerCurrentlyOnScreen = False
        self.destroy()

    
    def _CrewMatchInvitee__handleNo(self):
        if self.initialRequest:
            base.cr.crewMatchManager.initialAvatarAddResponse(2)
        else:
            base.cr.crewMatchManager.offerCurrentlyOnScreen = False
            base.cr.crewMatchManager.checkOfferCache()
        self.destroy()

    
    def _CrewMatchInvitee__handleCancelFromAbove(self):
        self.destroy()

    
    def handleAvatarPress(self, avId, avName):
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            base.localAvatar.guiMgr.handleAvatarDetails(avId, avName)
        


