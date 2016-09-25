# File: G (Python 2.4)

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from pirates.piratesgui import PDialog
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui.RequestButton import RequestButton
GUILDRANK_VETERAN = 4
GUILDRANK_GM = 3
GUILDRANK_OFFICER = 2
GUILDRANK_MEMBER = 1

class GuildMemberButton(RequestButton):
    
    def __init__(self, text, command):
        RequestButton.__init__(self, text, command, 2.0)
        self.initialiseoptions(GuildMemberButton)
        self['text_pos'] = (0.050000000000000003, 0.025000000000000001)



class GuildMemberButtonYesNo(RequestButton):
    
    def __init__(self, text, command):
        RequestButton.__init__(self, text, command, 1.0)
        self.initialiseoptions(GuildMemberButtonYesNo)
        self['text_pos'] = (0.050000000000000003, 0.025000000000000001)



class GuildMember(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('GuildMember')
    
    def __init__(self, avId, avName, guildId, canpromote, candemote, cankick):
        guiMain = loader.loadModel('models/gui/gui_main')
        DirectFrame.__init__(self, relief = None, pos = (-0.59999999999999998, 0, 0.41999999999999998), image = guiMain.find('**/general_frame_e'), image_pos = (0.25, 0, 0.23999999999999999), image_scale = (0.29999999999999999, 0.0, 0.34000000000000002))
        self.initialiseoptions(GuildMember)
        self.avId = avId
        self.avName = avName
        self.guildId = guildId
        self.canpromote = canpromote
        self.candemote = candemote
        self.cankick = cankick
        rank = base.cr.guildManager.getRank(avId)
        self.title = None
        self.message = None
        self.avocateMessage = None
        self.bTopEditButton = None
        self.bBottomEditButton = None
        self.bKick = None
        self.bAvocateConfrim = None
        self.bAvocateCancel = None
        self.bAvocate = None
        guiMain = loader.loadModel('models/gui/gui_main')
        self.title = DirectLabel(parent = self, relief = None, text = OTPLocalizer.GuildMemberTitle, text_scale = PiratesGuiGlobals.TextScaleTitleSmall, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_font = PiratesGlobals.getPirateOutlineFont(), pos = (0.25, 0, 0.44))
        self.message = DirectLabel(parent = self, relief = None, text = avName, text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_fg = (0.90000000000000002, 1, 0.90000000000000002, 1), text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 11, pos = (0.25, 0, 0.34499999999999997), textMayChange = 1)
        self.avocateMessage = DirectLabel(parent = self, relief = None, text = OTPLocalizer.GuildMemberGMMessage % avName, text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ALeft, text_fg = (0.90000000000000002, 1, 0.90000000000000002, 1), text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 11, pos = (0.050000000000000003, 0, 0.34499999999999997), textMayChange = 1)
        self.avocateMessage.hide()
        if rank in (GUILDRANK_MEMBER, GUILDRANK_VETERAN):
            topButtonText = OTPLocalizer.GuildMemberPromote
            topButtonCommand = self._GuildMember__handleMakeOfficer
        else:
            topButtonText = OTPLocalizer.GuildMemberDemoteInvite
            topButtonCommand = self._GuildMember__handleMakeVeteran
        if rank in (GUILDRANK_OFFICER, GUILDRANK_VETERAN):
            bottomButtonText = OTPLocalizer.GuildMemberDemote
            bottomButtonCommand = self._GuildMember__handleMakeMember
        else:
            bottomButtonText = OTPLocalizer.GuildMemberPromoteInvite
            bottomButtonCommand = self._GuildMember__handleMakeVeteran
        self.bTopEditButton = GuildMemberButton(text = topButtonText, command = topButtonCommand)
        self.bTopEditButton.reparentTo(self)
        self.bTopEditButton.setPos(0.20000000000000001, 0, 0.26000000000000001)
        self.bBottomEditButton = GuildMemberButton(text = bottomButtonText, command = bottomButtonCommand)
        self.bBottomEditButton.reparentTo(self)
        self.bBottomEditButton.setPos(0.20000000000000001, 0, 0.19)
        if self.canpromote:
            self.bTopEditButton.show()
            self.bBottomEditButton.show()
        else:
            self.bTopEditButton.hide()
            self.bBottomEditButton.hide()
        self.bKick = GuildMemberButton(text = OTPLocalizer.GuildMemberKick, command = self._GuildMember__handleKick)
        self.bKick.reparentTo(self)
        self.bKick.setPos(0.20000000000000001, 0, 0.12)
        if not self.cankick:
            self.bKick.hide()
        
        self.bCancel = GuildMemberButton(text = OTPLocalizer.GuildMemberCancel, command = self._GuildMember__handleCancel)
        self.bCancel.reparentTo(self)
        self.bCancel.setPos(0.20000000000000001, 0, -0.080000000000000002)
        self.bAvocate = GuildMemberButton(text = OTPLocalizer.GuildMemberGM, command = self._GuildMember__handleAvocatePopup)
        self.bAvocate.reparentTo(self)
        self.bAvocate.setPos(0.20000000000000001, 0, 0.02)
        if localAvatar.getGuildRank() == GUILDRANK_GM:
            self.bAvocate.show()
        else:
            self.bAvocate.hide()
        self.bAvocateConfrim = GuildMemberButtonYesNo(text = OTPLocalizer.GuildMemberGMConfirm, command = self._GuildMember__handleAvocate)
        self.bAvocateConfrim.reparentTo(self)
        self.bAvocateConfrim.setPos(0.050000000000000003, 0, -0.080000000000000002)
        self.bAvocateConfrim.hide()
        self.bAvocateCancel = GuildMemberButtonYesNo(text = OTPLocalizer.GuildMemberCancel, command = self._GuildMember__handleAvocateCancel)
        self.bAvocateCancel.reparentTo(self)
        self.bAvocateCancel.setPos(0.34999999999999998, 0, -0.080000000000000002)
        self.bAvocateCancel.hide()
        self.accept('guildMemberUpdated', self.determineOptions)

    
    def destroy(self):
        if hasattr(self, 'destroyed'):
            return None
        
        self.destroyed = 1
        self.ignoreAll()
        DirectFrame.destroy(self)

    
    def _GuildMember__handleMakeOfficer(self):
        base.cr.guildManager.changeRank(self.avId, GUILDRANK_OFFICER)

    
    def _GuildMember__handleMakeVeteran(self):
        base.cr.guildManager.changeRank(self.avId, GUILDRANK_VETERAN)

    
    def _GuildMember__handleMakeMember(self):
        base.cr.guildManager.changeRank(self.avId, GUILDRANK_MEMBER)

    
    def _GuildMember__handleKick(self):
        base.cr.guildManager.removeMember(self.avId)
        self.destroy()

    
    def _GuildMember__handleCancel(self):
        self.destroy()

    
    def _GuildMember__handleAvocatePopup(self):
        self.bTopEditButton.hide()
        self.bBottomEditButton.hide()
        self.bKick.hide()
        self.bCancel.hide()
        self.bAvocate.hide()
        self.bAvocateConfrim.show()
        self.bAvocateCancel.show()
        self.avocateMessage.show()
        self.message.hide()

    
    def _GuildMember__handleAvocateCancel(self):
        if self.canpromote:
            self.bTopEditButton.show()
            self.bBottomEditButton.show()
        else:
            self.bTopEditButton.hide()
            self.bBottomEditButton.hide()
        self.bKick.show()
        self.bCancel.show()
        if base.cr.guildManager.getRank(localAvatar.doId) == GUILDRANK_GM:
            self.bAvocate.show()
        else:
            self.bAvocate.hide()
        self.bAvocateConfrim.hide()
        self.bAvocateCancel.hide()
        self.avocateMessage.hide()
        self.message.show()

    
    def _GuildMember__handleAvocate(self):
        base.cr.guildManager.changeRankAvocate(self.avId)
        self.destroy()

    
    def determineOptions(self, avId):
        if avId != self.avId and avId != localAvatar.doId:
            return None
        
        if not base.cr.guildManager.isInGuild(avId):
            self.destroy()
            return None
        
        (self.canpromote, self.candemote, self.cankick) = base.cr.guildManager.getOptionsFor(avId)
        rank = base.cr.guildManager.getRank(self.avId)
        self._GuildMember__handleAvocateCancel()
        if self.canpromote:
            if rank in (GUILDRANK_MEMBER, GUILDRANK_VETERAN):
                topButtonText = OTPLocalizer.GuildMemberPromote
                topButtonCommand = self._GuildMember__handleMakeOfficer
            else:
                topButtonText = OTPLocalizer.GuildMemberDemoteInvite
                topButtonCommand = self._GuildMember__handleMakeVeteran
            if rank in (GUILDRANK_OFFICER, GUILDRANK_VETERAN):
                bottomButtonText = OTPLocalizer.GuildMemberDemote
                bottomButtonCommand = self._GuildMember__handleMakeMember
            else:
                bottomButtonText = OTPLocalizer.GuildMemberPromoteInvite
                bottomButtonCommand = self._GuildMember__handleMakeVeteran
            self.bTopEditButton.configure(text = topButtonText, command = topButtonCommand)
            self.bBottomEditButton.configure(text = bottomButtonText, command = bottomButtonCommand)
        
        if self.canpromote:
            self.bTopEditButton.show()
            self.bBottomEditButton.show()
        else:
            self.bTopEditButton.hide()
            self.bBottomEditButton.hide()
        if self.cankick:
            self.bKick.show()
        else:
            self.bKick.hide()


