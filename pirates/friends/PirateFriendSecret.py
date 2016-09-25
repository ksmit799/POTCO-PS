# File: P (Python 2.4)

from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import StateData
import string
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PLocalizer
globalFriendSecret = None
AccountSecret = 0
AvatarSecret = 1
BothSecrets = 2
offX = 0.80000000000000004
offZ = 0.59999999999999998

def showFriendSecret(secretType = AccountSecret):
    global globalFriendSecret
    if not Freebooter.getPaidStatus(localAvatar.getDoId()) and base.cr.productName == 'DisneyOnline-US':
        chatMgr = base.localAvatar.chatMgr
        chatMgr.fsm.request('unpaidChatWarning')
    elif not base.cr.allowSecretChat():
        chatMgr = base.localAvatar.chatMgr
        if base.cr.productName in [
            'DisneyOnline-AP',
            'DisneyOnline-UK',
            'ES',
            'Wanadoo',
            'T-Online',
            'JP']:
            chatMgr = base.localAvatar.chatMgr
            if not Freebooter.getPaidStatus(localAvatar.getDoId()):
                chatMgr.fsm.request('unpaidChatWarning')
            else:
                chatMgr.paidNoParentPassword = 1
                chatMgr.fsm.request('unpaidChatWarning')
        else:
            chatMgr.fsm.request('noSecretChatAtAll')
    elif base.cr.needParentPasswordForSecretChat():
        unloadFriendSecret()
        globalFriendSecret = FriendSecretNeedsParentLogin(secretType)
        globalFriendSecret.enter()
    else:
        openFriendSecret(secretType)


def openFriendSecret(secretType):
    global globalFriendSecret
    if globalFriendSecret != None:
        globalFriendSecret.unload()
    
    globalFriendSecret = FriendSecret(secretType)
    globalFriendSecret.setPos(-0.75, 0, -0.45000000000000001)
    globalFriendSecret.enter()


def hideFriendSecret():
    if globalFriendSecret != None:
        globalFriendSecret.exit()
    


def unloadFriendSecret():
    global globalFriendSecret
    if globalFriendSecret != None:
        globalFriendSecret.unload()
        globalFriendSecret = None
    


class FriendSecretNeedsParentLogin(StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('FriendSecretNeedsParentLogin')
    
    def __init__(self, secretType):
        StateData.StateData.__init__(self, 'friend-secret-needs-parent-login-done')
        self.dialog = None
        self.secretType = secretType

    
    def enter(self):
        StateData.StateData.enter(self)
        base.localAvatar.chatMgr.fsm.request('otherDialog')
        if self.dialog == None:
            charGui = loader.loadModel('models/gui/char_gui')
            buttonImage = (charGui.find('**/chargui_text_block_large'), charGui.find('**/chargui_text_block_large_down'), charGui.find('**/chargui_text_block_large_over'))
            self.dialog = GuiPanel.GuiPanel('Secret Codes!!! Arg!!', 1.6000000000000001, 1.2, False)
            offX = -0.75
            offZ = -0.45000000000000001
            self.dialog.setPos(offX, 0, offZ)
            okPos = (-0.22 - offX, 0.0, -0.29999999999999999 - offZ)
            cancelPos = (0.20000000000000001 - offX, 0.0, -0.29999999999999999 - offZ)
            textPos = (0, 0.25)
            okCommand = self._FriendSecretNeedsParentLogin__handleOK
            DirectButton(self.dialog, image = buttonImage, image_scale = (0.40000000000000002, 1, 0.40000000000000002), relief = None, text = OTPLocalizer.FriendSecretNeedsPasswordWarningOK, text_fg = PiratesGuiGlobals.TextFG2, text_scale = 0.050000000000000003, text_pos = (0.0, -0.01), textMayChange = 0, pos = okPos, command = okCommand)
            DirectLabel(parent = self.dialog, relief = None, pos = (0 - offX, 0, 0.55000000000000004 - offZ), text = OTPLocalizer.FriendSecretNeedsPasswordWarningTitle, text_fg = PiratesGuiGlobals.TextFG2, textMayChange = 0, text_scale = 0.080000000000000002)
            if base.cr.productName != 'Terra-DMC':
                self.usernameLabel = DirectLabel(parent = self.dialog, relief = None, pos = (-0.070000000000000007 - offX, 0.0, 0.10000000000000001 - offZ), text = OTPLocalizer.ParentLogin, text_fg = PiratesGuiGlobals.TextFG2, text_scale = 0.059999999999999998, text_align = TextNode.ARight, textMayChange = 0)
                self.usernameEntry = DirectEntry(parent = self.dialog, relief = None, text_fg = PiratesGuiGlobals.TextFG2, scale = 0.064000000000000001, pos = (0.0 - offX, 0.0, 0.10000000000000001 - offZ), width = OTPGlobals.maxLoginWidth, numLines = 1, focus = 1, cursorKeys = 1, obscured = 1, suppressKeys = 1, command = self._FriendSecretNeedsParentLogin__handleUsername)
                self.passwordLabel = DirectLabel(parent = self.dialog, relief = None, pos = (-0.070000000000000007 - offX, 0.0, -0.10000000000000001 - offZ), text = OTPLocalizer.ParentPassword, text_fg = PiratesGuiGlobals.TextFG2, text_scale = 0.059999999999999998, text_align = TextNode.ARight, textMayChange = 0)
                self.passwordEntry = DirectEntry(parent = self.dialog, relief = None, text_fg = PiratesGuiGlobals.TextFG2, scale = 0.064000000000000001, pos = (0.0 - offX, 0.0, -0.10000000000000001 - offZ), width = OTPGlobals.maxLoginWidth, numLines = 1, focus = 1, cursorKeys = 1, obscured = 1, suppressKeys = 1, command = self._FriendSecretNeedsParentLogin__handleOK)
                DirectButton(self.dialog, image = buttonImage, image_scale = (0.40000000000000002, 1, 0.40000000000000002), relief = None, text = OTPLocalizer.FriendSecretNeedsPasswordWarningCancel, text_scale = 0.050000000000000003, text_pos = (0.0, -0.01), textMayChange = 1, text_fg = PiratesGuiGlobals.TextFG2, pos = cancelPos, command = self._FriendSecretNeedsParentLogin__handleCancel)
                self.usernameEntry['focus'] = 1
                self.usernameEntry.enterText('')
                charGui.removeNode()
            
        else:
            self.dialog['text'] = OTPLocalizer.FriendSecretNeedsParentLoginWarning
            if self.usernameEntry:
                self.usernameEntry['focus'] = 1
                self.usernameEntry.enterText('')
            elif self.passwordEntry:
                self.passwordEntry['focus'] = 1
                self.passwordEntry.enterText('')
            
        self.dialog.show()

    
    def exit(self):
        print 'exit'
        self.ignoreAll()
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None
        
        if self.isEntered:
            base.localAvatar.chatMgr.fsm.request('mainMenu')
            StateData.StateData.exit(self)
        

    
    def _FriendSecretNeedsParentLogin__handleUsername(self, *args):
        if self.passwordEntry:
            self.passwordEntry['focus'] = 1
            self.passwordEntry.enterText('')
        

    
    def _FriendSecretNeedsParentLogin__oldHandleOK(self, *args):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        tt = base.cr.loginInterface
        (okflag, message) = tt.authenticateParentPassword(base.cr.userName, base.cr.password, password)
        if okflag:
            self.exit()
            openFriendSecret(self.secretType)
        elif message:
            base.localAvatar.chatMgr.fsm.request('problemActivatingChat')
            base.localAvatar.chatMgr.problemActivatingChat['text'] = OTPLocalizer.ProblemActivatingChat % message
        else:
            self.dialog['text'] = OTPLocalizer.FriendSecretNeedsPasswordWarningWrongPassword
            self.passwordEntry['focus'] = 1
            self.passwordEntry.enterText('')

    
    def _FriendSecretNeedsParentLogin__handleOK(self, *args):
        base.cr.parentUsername = self.usernameEntry.get()
        base.cr.parentPassword = self.passwordEntry.get()
        base.cr.playerFriendsManager.sendRequestUseLimitedSecret('', base.cr.parentUsername, base.cr.parentPassword)
        self.accept(OTPGlobals.PlayerFriendRejectUseSecretEvent, self._FriendSecretNeedsParentLogin__handleParentLogin)
        self._FriendSecretNeedsParentLogin__handleParentLogin(0)

    
    def _FriendSecretNeedsParentLogin__handleParentLogin(self, reason):
        if reason == 0:
            self.exit()
            openFriendSecret(self.secretType)
        elif reason == 1:
            self.dialog['text'] = OTPLocalizer.FriendSecretNeedsPasswordWarningWrongUsername
            self.usernameEntry['focus'] = 1
            self.usernameEntry.enterText('')
        elif reason == 2:
            self.dialog['text'] = OTPLocalizer.FriendSecretNeedsPasswordWarningWrongPassword
            self.passwordEntry['focus'] = 1
            self.passwordEntry.enterText('')
        else:
            base.localAvatar.chatMgr.fsm.request('problemActivatingChat')
            base.localAvatar.chatMgr.problemActivatingChat['text'] = OTPLocalizer.ProblemActivatingChat % message

    
    def _FriendSecretNeedsParentLogin__handleCancel(self):
        self.exit()



class FriendSecret(GuiPanel.GuiPanel, StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('FriendSecret')
    
    def __init__(self, secretType):
        GuiPanel.GuiPanel.__init__(self, 'Secret Codes!!! Arg!!', 1.6000000000000001, 1.2)
        StateData.StateData.__init__(self, 'friend-secret-done')
        self.initialiseoptions(FriendSecret)
        self.prefix = OTPGlobals.getDefaultProductPrefix()
        self.secretType = secretType
        self.notify.debug('### secretType = %s' % self.secretType)
        self.requestedSecretType = secretType
        self.notify.debug('### requestedSecretType = %s' % self.requestedSecretType)

    
    def unload(self):
        print 'unload'
        if self.isLoaded == 0:
            return None
        
        self.isLoaded = 0
        self.exit()
        del self.introText
        del self.getSecret
        del self.enterSecretText
        del self.enterSecret
        del self.ok1
        del self.ok2
        del self.cancel
        del self.secretText
        del self.avatarButton
        del self.accountButton
        GuiPanel.GuiPanel.destroy(self)

    
    def load(self):
        print 'load'
        if self.isLoaded == 1:
            return None
        
        self.isLoaded = 1
        charGui = loader.loadModel('models/gui/char_gui')
        buttonImage = (charGui.find('**/chargui_text_block_large'), charGui.find('**/chargui_text_block_large_down'), charGui.find('**/chargui_text_block_large_over'))
        self.introText = DirectLabel(parent = self, relief = None, pos = (0 + offX, 0, 0.40000000000000002 + offZ), scale = 0.050000000000000003, text = PLocalizer.FriendSecretIntro, text_fg = PiratesGuiGlobals.TextFG2, text_wordwrap = 30)
        self.introText.hide()
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        self.getSecret = DirectButton(parent = self, relief = None, pos = (0 + offX, 0, -0.11 + offZ), image = buttonImage, image_scale = (0.84999999999999998, 1, 0.40000000000000002), text = OTPLocalizer.FriendSecretGetSecret, text_fg = PiratesGuiGlobals.TextFG2, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (0, -0.02), command = self._FriendSecret__determineSecret)
        self.getSecret.hide()
        self.enterSecretText = DirectLabel(parent = self, relief = None, pos = (0 + offX, 0, -0.25 + offZ), text = OTPLocalizer.FriendSecretEnterSecret, text_scale = PiratesGuiGlobals.TextScaleLarge, text_fg = PiratesGuiGlobals.TextFG2, text_wordwrap = 30)
        self.enterSecretText.hide()
        self.enterSecret = DirectEntry(parent = self, relief = DGG.SUNKEN, scale = 0.059999999999999998, pos = (-0.59999999999999998 + offX, 0, -0.38 + offZ), frameColor = (0.80000000000000004, 0.80000000000000004, 0.5, 1), borderWidth = (0.10000000000000001, 0.10000000000000001), numLines = 1, width = 20, frameSize = (-0.40000000000000002, 20.399999999999999, -0.40000000000000002, 1.1000000000000001), command = self._FriendSecret__enterSecret, suppressKeys = 1)
        self.enterSecret.resetFrameSize()
        self.enterSecret.hide()
        self.ok1 = DirectButton(parent = self, relief = None, image = buttonImage, image_scale = (0.84999999999999998, 1, 0.40000000000000002), text = OTPLocalizer.FriendSecretEnter, text_fg = PiratesGuiGlobals.TextFG2, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (0, -0.02), pos = (0 + offX, 0, -0.5 + offZ), command = self._FriendSecret__ok1)
        self.ok1.hide()
        self.ok2 = DirectButton(parent = self, relief = None, image = buttonImage, image_scale = (0.40000000000000002, 1, 0.40000000000000002), text = OTPLocalizer.FriendSecretOK, text_fg = PiratesGuiGlobals.TextFG2, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (0, -0.02), pos = (0 + offX, 0, -0.5 + offZ), command = self._FriendSecret__ok2)
        self.ok2.hide()
        self.cancel = DirectButton(parent = self, relief = None, text = OTPLocalizer.FriendSecretCancel, image = buttonImage, image_scale = (0.40000000000000002, 1, 0.40000000000000002), text_fg = PiratesGuiGlobals.TextFG2, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (0, -0.02), pos = (0 + offX, 0, -0.5 + offZ), command = self._FriendSecret__cancel)
        self.cancel.hide()
        self.nextText = DirectLabel(parent = self, relief = None, pos = (0 + offX, 0, 0.29999999999999999 + offZ), scale = 0.059999999999999998, text = '', text_fg = PiratesGuiGlobals.TextFG2, text_wordwrap = 25.5)
        self.nextText.hide()
        self.secretText = DirectLabel(parent = self, relief = None, pos = (0 + offX, 0, -0.35999999999999999 + offZ), scale = 0.10000000000000001, text = '', text_fg = PiratesGuiGlobals.TextFG2, text_wordwrap = 30)
        self.secretText.hide()
        charGui.removeNode()
        self.makeFriendTypeButtons()

    
    def makeFriendTypeButtons(self):
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        self.avatarButton = DirectButton(self, relief = None, text = OTPLocalizer.FriendSecretDetermineSecretAvatar, text_scale = 0.070000000000000007, text_pos = (0.0, -0.10000000000000001), pos = (-0.34999999999999998 + offX, 0.0, -0.050000000000000003 + offZ), command = self._FriendSecret__handleAvatar)
        avatarText = DirectLabel(parent = self, relief = None, pos = Vec3(0.34999999999999998, 0, -0.29999999999999999), text = OTPLocalizer.FriendSecretDetermineSecretAvatarRollover, text_fg = PiratesGuiGlobals.TextFG2, text_pos = (0, 0), text_scale = 0.055, text_align = TextNode.ACenter)
        avatarText.reparentTo(self.avatarButton.stateNodePath[2])
        self.avatarButton.hide()
        self.accountButton = DirectButton(self, relief = None, text = OTPLocalizer.FriendSecretDetermineSecretAccount, text_scale = 0.070000000000000007, text_pos = (0.0, -0.10000000000000001), pos = (0.34999999999999998 + offX, 0.0, -0.050000000000000003 + offZ), command = self._FriendSecret__handleAccount)
        accountText = DirectLabel(parent = self, relief = None, pos = Vec3(-0.34999999999999998 + offX, 0, -0.29999999999999999 + offZ), text = OTPLocalizer.FriendSecretDetermineSecretAccountRollover, text_fg = PiratesGuiGlobals.TextFG2, text_pos = (0, 0), text_scale = 0.055, text_align = TextNode.ACenter)
        accountText.reparentTo(self.accountButton.stateNodePath[2])
        self.accountButton.hide()

    
    def enter(self):
        print 'enter'
        if self.isEntered == 1:
            return None
        
        self.isEntered = 1
        if self.isLoaded == 0:
            self.load()
        
        self.show()
        self.introText.show()
        self.getSecret.show()
        self.enterSecretText.show()
        self.enterSecret.show()
        self.ok1.show()
        self.ok2.hide()
        self.cancel.hide()
        self.nextText.hide()
        self.secretText.hide()
        base.localAvatar.chatMgr.fsm.request('otherDialog')
        self.enterSecret['focus'] = 1
        NametagGlobals.setOnscreenChatForced(1)

    
    def closePanel(self):
        print 'closePanel'
        self.exit()

    
    def exit(self):
        print 'exit'
        if self.isEntered == 0:
            return None
        
        self.isEntered = 0
        NametagGlobals.setOnscreenChatForced(0)
        self._FriendSecret__cleanupFirstPage()
        self.ignoreAll()
        self.hide()

    
    def _FriendSecret__determineSecret(self):
        if self.secretType == BothSecrets:
            self._FriendSecret__cleanupFirstPage()
            self.ok1.hide()
            self.nextText['text'] = OTPLocalizer.FriendSecretDetermineSecret
            self.nextText.setPos(0, 0, 0.29999999999999999)
            self.nextText.show()
            self.avatarButton.show()
            self.accountButton.show()
            self.cancel.show()
        else:
            self._FriendSecret__getSecret()

    
    def _FriendSecret__handleAvatar(self):
        self.requestedSecretType = AvatarSecret
        self._FriendSecret__getSecret()

    
    def _FriendSecret__handleAccount(self):
        self.requestedSecretType = AccountSecret
        self._FriendSecret__getSecret()

    
    def _FriendSecret__handleCancel(self):
        self.exit()

    
    def _FriendSecret__getSecret(self):
        self._FriendSecret__cleanupFirstPage()
        self.nextText['text'] = OTPLocalizer.FriendSecretGettingSecret
        self.nextText.setPos(0 + offX, 0, 0.29999999999999999 + offZ)
        self.nextText.show()
        self.avatarButton.hide()
        self.accountButton.hide()
        self.ok1.hide()
        self.cancel.show()
        if self.requestedSecretType == AvatarSecret:
            if not base.cr.friendManager:
                self.notify.warning('No FriendManager available.')
                self.exit()
                return None
            
            base.cr.friendManager.up_requestSecret()
            self.accept('requestSecretResponse', self._FriendSecret__gotAvatarSecret)
        elif base.cr.needParentPasswordForSecretChat():
            base.cr.playerFriendsManager.sendRequestLimitedSecret(base.cr.parentUsername, base.cr.parentPassword)
        else:
            base.cr.playerFriendsManager.sendRequestUnlimitedSecret()
        self.accept(OTPGlobals.PlayerFriendNewSecretEvent, self._FriendSecret__gotAccountSecret)
        self.accept(OTPGlobals.PlayerFriendRejectNewSecretEvent, self._FriendSecret__rejectAccountSecret)

    
    def _FriendSecret__gotAvatarSecret(self, result, secret):
        self.ignore('requestSecretResponse')
        if result == 1:
            self.nextText['text'] = OTPLocalizer.FriendSecretGotSecret
            self.nextText.setPos(0 + offX, 0, 0.46999999999999997 + offZ)
            if self.prefix:
                self.secretText['text'] = self.prefix + ' ' + secret
            else:
                self.secretText['text'] = secret
        else:
            self.nextText['text'] = OTPLocalizer.FriendSecretTooMany
        self.nextText.show()
        self.secretText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()

    
    def _FriendSecret__gotAccountSecret(self, secret):
        self.ignore(OTPGlobals.PlayerFriendNewSecretEvent)
        self.ignore(OTPGlobals.PlayerFriendRejectNewSecretEvent)
        self.nextText['text'] = OTPLocalizer.FriendSecretGotSecret
        self.nextText.setPos(0 + offX, 0, 0.46999999999999997 + offZ)
        self.secretText['text'] = secret
        self.nextText.show()
        self.secretText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()

    
    def _FriendSecret__rejectAccountSecret(self, reason):
        self.ignore(OTPGlobals.PlayerFriendNewSecretEvent)
        self.ignore(OTPGlobals.PlayerFriendRejectNewSecretEvent)
        self.nextText['text'] = OTPLocalizer.FriendSecretTooMany
        self.nextText.show()
        self.secretText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()

    
    def _FriendSecret__enterSecret(self, secret):
        self.enterSecret.set('')
        secret = string.strip(secret)
        if not secret:
            self.exit()
            return None
        
        if self.requestedSecretType == AvatarSecret:
            if not base.cr.friendManager:
                self.notify.warning('No FriendManager available.')
                self.exit()
                return None
            
            self._FriendSecret__cleanupFirstPage()
            if self.prefix:
                if secret[0:2] == self.prefix:
                    secret = secret[3:]
                else:
                    self._FriendSecret__enteredSecret(4, 0)
                    return None
            
            base.cr.friendManager.up_submitSecret(secret)
        else:
            self._FriendSecret__cleanupFirstPage()
            if base.cr.needParentPasswordForSecretChat():
                base.cr.playerFriendsManager.sendRequestUseLimitedSecret(secret, base.cr.parentUsername, base.cr.parentPassword)
            else:
                base.cr.playerFriendsManager.sendRequestUseUnlimitedSecret(secret)
        self.nextText['text'] = OTPLocalizer.FriendSecretTryingSecret
        self.nextText.setPos(0 + offX, 0, 0.29999999999999999 + offZ)
        self.nextText.show()
        self.ok1.hide()
        self.cancel.show()
        self.accept(OTPGlobals.PlayerFriendAddEvent, self._FriendSecret__secretResponseOkay)
        self.accept(OTPGlobals.PlayerFriendRejectUseSecretEvent, self._FriendSecret__secretResponseReject)
        taskMgr.doMethodLater(10.0, self._FriendSecret__secretTimeout, 'timeoutSecretResponse')

    
    def _FriendSecret__secretTimeout(self, caller = None):
        print '__secretTimeout'
        self.ignore(OTPGlobals.PlayerFriendAddEvent)
        self.ignore(OTPGlobals.PlayerFriendRejectUseSecretEvent)
        self.nextText['text'] = OTPLocalizer.FriendSecretTimeOut
        return None
        self.nextText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()

    
    def _FriendSecret__secretResponseOkay(self, avId, info):
        print '__secretResponseOkay'
        taskMgr.remove('timeoutSecretResponse')
        self.ignore(OTPGlobals.PlayerFriendAddEvent)
        self.ignore(OTPGlobals.PlayerFriendRejectUseSecretEvent)
        self.nextText['text'] = OTPLocalizer.FriendSecretEnteredSecretSuccess % info.playerName
        self.nextText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()

    
    def _FriendSecret__secretResponseReject(self, reason):
        print '__secretResponseReject'
        taskMgr.remove('timeoutSecretResponse')
        self.ignore(OTPGlobals.PlayerFriendAddEvent)
        self.ignore(OTPGlobals.PlayerFriendRejectUseSecretEvent)
        self.nextText['text'] = OTPLocalizer.FriendSecretEnteredSecretUnknown
        self.nextText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()

    
    def _FriendSecret__nowFriends(self, avId):
        self.ignore('friendsMapComplete')
        handle = base.cr.identifyAvatar(avId)
        if handle != None:
            self.nextText['text'] = OTPLocalizer.FriendSecretNowFriends % handle.getName()
        else:
            self.nextText['text'] = OTPLocalizer.FriendSecretNowFriendsNoName
        self.nextText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()

    
    def _FriendSecret__ok1(self):
        secret = self.enterSecret.get()
        self._FriendSecret__enterSecret(secret)

    
    def _FriendSecret__ok2(self):
        self.exit()

    
    def _FriendSecret__cancel(self):
        self.exit()

    
    def _FriendSecret__cleanupFirstPage(self):
        self.introText.hide()
        self.getSecret.hide()
        self.enterSecretText.hide()
        self.enterSecret.hide()
        base.localAvatar.chatMgr.fsm.request('mainMenu')


