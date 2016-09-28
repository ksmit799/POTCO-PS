from direct.gui.DirectGui import *
from panda3d.core import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPLocalizer
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui.RequestButton import RequestButton

class GuildInviteeButton(RequestButton):
    
    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(GuildInviteeButton)



class GuildInvitee(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('GuildInvitee')
    
    def __init__(self, avId, avName, guildId, guildName):
        guiMain = loader.loadModel('models/gui/gui_main')
        DirectFrame.__init__(self, relief = None, pos = (-0.59999999999999998, 0, 0.46999999999999997), image = guiMain.find('**/general_frame_e'), image_pos = (0.25, 0, 0.27500000000000002), image_scale = (0.28000000000000003, 1, 0.28000000000000003))
        self.initialiseoptions(GuildInvitee)
        self.avId = avId
        self.avName = avName
        self.guildId = guildId
        if base.cr.avatarFriendsManager.checkIgnored(self.avId):
            self._GuildInvitee__handleNo()
            return None
        
        if guildName == 0 and guildName == '' or guildName == '0':
            self.guildName = PLocalizer.GuildDefaultName % self.guildId
        else:
            self.guildName = guildName
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
        text = OTPLocalizer.GuildInviteeInvitation % (buttonName, self.guildName)
        guiMain = loader.loadModel('models/gui/gui_main')
        self.box = OnscreenImage(parent = self, pos = (0.25, 0, 0.27500000000000002), image = guiMain.find('**/general_frame_e'), scale = 0.28000000000000003)
        self.title = DirectLabel(parent = self, relief = None, text = PLocalizer.GuildInviteeTitle, text_scale = PiratesGuiGlobals.TextScaleExtraLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_font = PiratesGlobals.getPirateOutlineFont(), pos = (0.25, 0, 0.41999999999999998), image = None, image_scale = 0.25)
        self.message = DirectLabel(parent = self, relief = None, text = text, text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 11, pos = (0.25, 0, 0.32500000000000001), textMayChange = 1)
        self.bOk = GuildInviteeButton(text = OTPLocalizer.GuildInviteeOK, command = self._GuildInvitee__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.10000000000000001, 0, 0.14999999999999999)
        self.bNo = GuildInviteeButton(text = OTPLocalizer.GuildInviteeNo, command = self._GuildInvitee__handleNo)
        self.bNo.reparentTo(self)
        self.bNo.setPos(0.29999999999999999, 0, 0.14999999999999999)
        self.bIgnore = GuildInviteeButton(text = PLocalizer.GuildInviteeIgnore, command = self._GuildInvitee__handleIgnore)
        self.bIgnore.reparentTo(self)
        self.bIgnore['image_scale'] = (0.65000000000000002, 1, 0.5)
        self.bIgnore.setPos(0.20000000000000001, 0, 0.050000000000000003)
        self.bIgnore['text_pos'] = (0.040000000000000001, 0.040000000000000001)
        if hasattr(base, 'localAvatar'):
            if not base.localAvatar.isPopulated():
                self._GuildInvitee__handleNo()
                return None
            
        
        self.accept('declineGuildInvitation', self._GuildInvitee__handleNo)
        self.accept('cancelGuildInvitation', self._GuildInvitee__handleCancelFromAbove)
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            if base.localAvatar.guiMgr.ignoreGuildInvites:
                self._GuildInvitee__handleNo()
            
        

    
    def destroy(self):
        if hasattr(self, 'destroyed'):
            return None
        
        self.destroyed = 1
        self.ignore('cancelGuildInvitation')
        DirectFrame.destroy(self)

    
    def _GuildInvitee__handleOk(self):
        base.cr.guildManager.sendAcceptInvite()
        self.destroy()

    
    def _GuildInvitee__handleNo(self):
        base.cr.guildManager.sendDeclineInvite()
        self.destroy()

    
    def _GuildInvitee__handleIgnore(self):
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            base.localAvatar.guiMgr.handleIgnoreGuildInvites()
        
        self.destroy()

    
    def _GuildInvitee__handleCancelFromAbove(self):
        self.destroy()

    
    def handleAvatarPress(self, avId, avName):
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            base.localAvatar.guiMgr.handleAvatarDetails(avId, avName)
        


