# File: F (Python 2.4)

from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import StateData
import string
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from otp.uberdog import RejectCode
globalFriendSecret = None
AccountSecret = 0
AvatarSecret = 1
BothSecrets = 2

def showFriendSecret(secretType = AvatarSecret):
    global globalFriendSecret
    if not base.cr.isPaid():
        chatMgr = base.localAvatar.chatMgr
        chatMgr.fsm.request('trueFriendTeaserPanel')
    elif not base.cr.isParentPasswordSet():
        chatMgr = base.localAvatar.chatMgr
        if base.cr.productName in [
            'DisneyOnline-AP',
            'DisneyOnline-UK',
            'JP',
            'DE',
            'BR',
            'FR']:
            chatMgr = base.localAvatar.chatMgr
            if not base.cr.isPaid():
                chatMgr.fsm.request('unpaidChatWarning')
            else:
                chatMgr.paidNoParentPassword = 1
                chatMgr.fsm.request('unpaidChatWarning')
        else:
            chatMgr.paidNoParentPassword = 1
            chatMgr.fsm.request('noSecretChatAtAll')
    elif not base.cr.allowSecretChat():
        chatMgr = base.localAvatar.chatMgr
        if base.cr.productName in [
            'DisneyOnline-AP',
            'DisneyOnline-UK',
            'JP',
            'DE',
            'BR',
            'FR']:
            chatMgr = base.localAvatar.chatMgr
            if not base.cr.isPaid():
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
            guiButton = loader.loadModel('phase_3/models/gui/quit_button')
            buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
            nameBalloon = loader.loadModel('phase_3/models/props/chatbox_input')
            optionsButtonImage = (guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR'))
            okButtonImage = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
            cancelButtonImage = (buttons.find('**/CloseBtn_UP'), buttons.find('**/CloseBtn_DN'), buttons.find('**/CloseBtn_Rllvr'))
            withParentAccount = False
            
            try:
                withParentAccount = base.cr.withParentAccount
            except:
                self.notify.warning('withParentAccount not found in base.cr')

            if withParentAccount:
                okPos = (-0.22, 0.0, -0.5)
                textPos = (0, 0.25)
                okCommand = self._FriendSecretNeedsParentLogin__handleOKWithParentAccount
            elif base.cr.productName != 'Terra-DMC':
                okPos = (-0.22, 0.0, -0.5)
                textPos = (0, 0.25)
                okCommand = self._FriendSecretNeedsParentLogin__oldHandleOK
            else:
                self.passwordEntry = None
                okPos = (0, 0, -0.34999999999999998)
                textPos = (0, 0.125)
                okCommand = self._FriendSecretNeedsParentLogin__handleCancel
            self.dialog = DirectFrame(parent = aspect2dp, pos = (0.0, 0.10000000000000001, 0.20000000000000001), relief = None, image = DGG.getDefaultDialogGeom(), image_color = OTPGlobals.GlobalDialogColor, image_scale = (1.3999999999999999, 1.0, 1.25), image_pos = (0, 0, -0.10000000000000001), text = OTPLocalizer.FriendSecretNeedsParentLoginWarning, text_wordwrap = 21.5, text_scale = 0.055, text_pos = textPos, textMayChange = 1)
            DirectButton(self.dialog, image = okButtonImage, relief = None, text = OTPLocalizer.FriendSecretNeedsPasswordWarningOK, text_scale = 0.050000000000000003, text_pos = (0.0, -0.10000000000000001), textMayChange = 0, pos = okPos, command = okCommand)
            DirectLabel(parent = self.dialog, relief = None, pos = (0, 0, 0.34999999999999998), text = OTPLocalizer.FriendSecretNeedsPasswordWarningTitle, textMayChange = 0, text_scale = 0.080000000000000002)
            if base.cr.productName != 'Terra-DMC':
                self.usernameLabel = DirectLabel(parent = self.dialog, relief = None, pos = (-0.070000000000000007, 0.0, -0.10000000000000001), text = OTPLocalizer.ParentLogin, text_scale = 0.059999999999999998, text_align = TextNode.ARight, textMayChange = 0)
                self.usernameEntry = DirectEntry(parent = self.dialog, relief = None, image = nameBalloon, image1_color = (0.80000000000000004, 0.80000000000000004, 0.80000000000000004, 1.0), scale = 0.064000000000000001, pos = (0.0, 0.0, -0.10000000000000001), width = OTPGlobals.maxLoginWidth, numLines = 1, focus = 1, cursorKeys = 1, obscured = 1, command = self._FriendSecretNeedsParentLogin__handleUsername)
                self.passwordLabel = DirectLabel(parent = self.dialog, relief = None, pos = (-0.02, 0.0, -0.29999999999999999), text = OTPLocalizer.ParentPassword, text_scale = 0.059999999999999998, text_align = TextNode.ARight, textMayChange = 0)
                self.passwordEntry = DirectEntry(parent = self.dialog, relief = None, image = nameBalloon, image1_color = (0.80000000000000004, 0.80000000000000004, 0.80000000000000004, 1.0), scale = 0.064000000000000001, pos = (0.040000000000000001, 0.0, -0.29999999999999999), width = OTPGlobals.maxLoginWidth, numLines = 1, focus = 1, cursorKeys = 1, obscured = 1, command = okCommand)
                DirectButton(self.dialog, image = cancelButtonImage, relief = None, text = OTPLocalizer.FriendSecretNeedsPasswordWarningCancel, text_scale = 0.050000000000000003, text_pos = (0.0, -0.10000000000000001), textMayChange = 1, pos = (0.20000000000000001, 0.0, -0.5), command = self._FriendSecretNeedsParentLogin__handleCancel)
                if withParentAccount:
                    self.usernameEntry.enterText('')
                    self.usernameEntry['focus'] = 1
                    self.passwordEntry.enterText('')
                else:
                    self.usernameEntry.hide()
                    self.usernameLabel.hide()
                    self.passwordEntry['focus'] = 1
                    self.passwordEntry.enterText('')
            
            guiButton.removeNode()
            buttons.removeNode()
            nameBalloon.removeNode()
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
        

    
    def _FriendSecretNeedsParentLogin__handleOKWithParentAccount(self, *args):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        base.cr.parentUsername = username
        base.cr.parentPassword = password
        tt = base.cr.loginInterface
        
        try:
            DISLIdFromLogin = base.cr.DISLIdFromLogin
        except:
            DISLIdFromLogin = 0

        if DISLIdFromLogin and DISLIdFromLogin != localAvatar.DISLid:
            self.notify.error('Mismatched DISLIds, fromLogin=%s, localAvatar.dislId=%s' % (DISLIdFromLogin, localAvatar.DISLid))
        
        (okflag, message) = tt.authenticateParentUsernameAndPassword(localAvatar.DISLid, base.cr.password, username, password)
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

    
    def _FriendSecretNeedsParentLogin__oldHandleOK(self, *args):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        base.cr.parentUsername = username
        base.cr.parentPassword = password
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
        self.exit()

    
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



class FriendSecret(DirectFrame, StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('FriendSecret')
    
    def __init__(self, secretType):
        DirectFrame.__init__(self, parent = aspect2dp, pos = (0, 0, 0.29999999999999999), relief = None, image = DGG.getDefaultDialogGeom(), image_scale = (1.6000000000000001, 1, 1.3999999999999999), image_pos = (0, 0, -0.050000000000000003), image_color = OTPGlobals.GlobalDialogColor, borderWidth = (0.01, 0.01))
        StateData.StateData.__init__(self, 'friend-secret-done')
        self.initialiseoptions(FriendSecret)
        self.prefix = OTPGlobals.getDefaultProductPrefix()
        self.secretType = secretType
        self.notify.debug('### secretType = %s' % self.secretType)
        self.requestedSecretType = secretType
        self.notify.debug('### requestedSecretType = %s' % self.requestedSecretType)

    
    def unload(self):
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
        DirectFrame.destroy(self)
        self.ignore('clientCleanup')

    
    def load(self):
        if self.isLoaded == 1:
            return None
        
        self.isLoaded = 1
        self.introText = DirectLabel(parent = self, relief = None, pos = (0, 0, 0.40000000000000002), scale = 0.050000000000000003, text = OTPLocalizer.FriendSecretIntro, text_fg = (0, 0, 0, 1), text_wordwrap = 30)
        self.introText.hide()
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        self.getSecret = DirectButton(parent = self, relief = None, pos = (0, 0, -0.11), image = (guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale = OTPLocalizer.FSgetSecret, text = OTPLocalizer.FriendSecretGetSecret, text_scale = OTPLocalizer.FSgetSecretButton, text_pos = (0, -0.02), command = self._FriendSecret__determineSecret)
        self.getSecret.hide()
        self.enterSecretText = DirectLabel(parent = self, relief = None, pos = OTPLocalizer.FSenterSecretTextPos, scale = 0.050000000000000003, text = OTPLocalizer.FriendSecretEnterSecret, text_fg = (0, 0, 0, 1), text_wordwrap = 30)
        self.enterSecretText.hide()
        self.enterSecret = DirectEntry(parent = self, relief = DGG.SUNKEN, scale = 0.059999999999999998, pos = (-0.59999999999999998, 0, -0.38), frameColor = (0.80000000000000004, 0.80000000000000004, 0.5, 1), borderWidth = (0.10000000000000001, 0.10000000000000001), numLines = 1, width = 20, frameSize = (-0.40000000000000002, 20.399999999999999, -0.40000000000000002, 1.1000000000000001), command = self._FriendSecret__enterSecret)
        self.enterSecret.resetFrameSize()
        self.enterSecret.hide()
        self.ok1 = DirectButton(parent = self, relief = None, image = (guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale = OTPLocalizer.FSok1, text = OTPLocalizer.FriendSecretEnter, text_scale = 0.059999999999999998, text_pos = (0, -0.02), pos = (0, 0, -0.5), command = self._FriendSecret__ok1)
        self.ok1.hide()
        if base.cr.productName in [
            'JP',
            'DE',
            'BR',
            'FR']:
            
            class ShowHide:
                
                def show(self):
                    pass

                
                def hide(self):
                    pass


            self.changeOptions = ShowHide()
        
        self.ok2 = DirectButton(parent = self, relief = None, image = (guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale = OTPLocalizer.FSok2, text = OTPLocalizer.FriendSecretOK, text_scale = 0.059999999999999998, text_pos = (0, -0.02), pos = (0, 0, -0.56999999999999995), command = self._FriendSecret__ok2)
        self.ok2.hide()
        self.cancel = DirectButton(parent = self, relief = None, text = OTPLocalizer.FriendSecretCancel, image = (guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale = OTPLocalizer.FScancel, text_scale = 0.059999999999999998, text_pos = (0, -0.02), pos = (0, 0, -0.56999999999999995), command = self._FriendSecret__cancel)
        self.cancel.hide()
        self.nextText = DirectLabel(parent = self, relief = None, pos = (0, 0, 0.29999999999999999), scale = 0.059999999999999998, text = '', text_scale = OTPLocalizer.FSnextText, text_fg = (0, 0, 0, 1), text_wordwrap = 25.5)
        self.nextText.hide()
        self.secretText = DirectLabel(parent = self, relief = None, pos = (0, 0, -0.41999999999999998), scale = 0.10000000000000001, text = '', text_fg = (0, 0, 0, 1), text_wordwrap = 30)
        self.secretText.hide()
        guiButton.removeNode()
        self.makeFriendTypeButtons()
        self.accept('clientCleanup', self._FriendSecret__handleCleanup)
        self.accept('walkDone', self._FriendSecret__handleStop)

    
    def _FriendSecret__handleStop(self, message):
        self.exit()

    
    def _FriendSecret__handleCleanup(self):
        self.unload()

    
    def makeFriendTypeButtons(self):
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        self.avatarButton = DirectButton(self, image = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr')), relief = None, text = OTPLocalizer.FriendSecretDetermineSecretAvatar, text_scale = 0.070000000000000007, text_pos = (0.0, -0.10000000000000001), pos = (-0.34999999999999998, 0.0, -0.050000000000000003), command = self._FriendSecret__handleAvatar)
        avatarText = DirectLabel(parent = self, relief = None, pos = Vec3(0.34999999999999998, 0, -0.29999999999999999), text = OTPLocalizer.FriendSecretDetermineSecretAvatarRollover, text_fg = (0, 0, 0, 1), text_pos = (0, 0), text_scale = 0.055, text_align = TextNode.ACenter)
        avatarText.reparentTo(self.avatarButton.stateNodePath[2])
        self.avatarButton.hide()
        self.accountButton = DirectButton(self, image = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr')), relief = None, text = OTPLocalizer.FriendSecretDetermineSecretAccount, text_scale = 0.070000000000000007, text_pos = (0.0, -0.10000000000000001), pos = (0.34999999999999998, 0.0, -0.050000000000000003), command = self._FriendSecret__handleAccount)
        accountText = DirectLabel(parent = self, relief = None, pos = Vec3(-0.34999999999999998, 0, -0.29999999999999999), text = OTPLocalizer.FriendSecretDetermineSecretAccountRollover, text_fg = (0, 0, 0, 1), text_pos = (0, 0), text_scale = 0.055, text_align = TextNode.ACenter)
        accountText.reparentTo(self.accountButton.stateNodePath[2])
        self.accountButton.hide()
        buttons.removeNode()

    
    def enter(self):
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

    
    def exit(self):
        if self.isEntered == 0:
            return None
        
        self.isEntered = 0
        NametagGlobals.setOnscreenChatForced(0)
        self._FriendSecret__cleanupFirstPage()
        self.ignoreAll()
        self.accept('clientCleanup', self.unload)
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
        self.nextText.setPos(0, 0, 0.29999999999999999)
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
            self.notify.info('### requestLimitedSecret')
            base.cr.playerFriendsManager.sendRequestLimitedSecret(base.cr.parentUsername, base.cr.parentPassword)
        else:
            base.cr.playerFriendsManager.sendRequestUnlimitedSecret()
            self.notify.info('### requestUnlimitedSecret')
        self.accept(OTPGlobals.PlayerFriendNewSecretEvent, self._FriendSecret__gotAccountSecret)
        self.accept(OTPGlobals.PlayerFriendRejectNewSecretEvent, self._FriendSecret__rejectAccountSecret)

    
    def _FriendSecret__gotAvatarSecret(self, result, secret):
        self.ignore('requestSecretResponse')
        if result == 1:
            self.nextText['text'] = OTPLocalizer.FriendSecretGotSecret
            self.nextText.setPos(*OTPLocalizer.FSgotSecretPos)
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
        self.nextText.setPos(0, 0, 0.46999999999999997)
        self.secretText['text'] = secret
        self.nextText.show()
        self.secretText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()

    
    def _FriendSecret__rejectAccountSecret(self, reason):
        print '## rejectAccountSecret: reason = ', reason
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
        
        if not base.cr.friendManager:
            self.notify.warning('No FriendManager available.')
            self.exit()
            return None
        
        self._FriendSecret__cleanupFirstPage()
        if self.prefix:
            if secret[0:2] == self.prefix:
                secret = secret[3:]
                self.notify.info('### use TT secret')
                self.accept('submitSecretResponse', self._FriendSecret__enteredSecret)
                base.cr.friendManager.up_submitSecret(secret)
            else:
                self.accept(OTPGlobals.PlayerFriendUpdateEvent, self._FriendSecret__useAccountSecret)
                self.accept(OTPGlobals.PlayerFriendRejectUseSecretEvent, self._FriendSecret__rejectUseAccountSecret)
                if base.cr.needParentPasswordForSecretChat():
                    self.notify.info('### useLimitedSecret')
                    base.cr.playerFriendsManager.sendRequestUseLimitedSecret(secret, base.cr.parentUsername, base.cr.parentPassword)
                else:
                    self.notify.info('### useUnlimitedSecret')
                    base.cr.playerFriendsManager.sendRequestUseUnlimitedSecret(secret)
        
        self.nextText['text'] = OTPLocalizer.FriendSecretTryingSecret
        self.nextText.setPos(0, 0, 0.29999999999999999)
        self.nextText.show()
        self.ok1.hide()
        self.cancel.show()

    
    def _FriendSecret__enteredSecret(self, result, avId):
        self.ignore('submitSecretResponse')
        if result == 1:
            handle = base.cr.identifyAvatar(avId)
            if handle != None:
                self.nextText['text'] = OTPLocalizer.FriendSecretEnteredSecretSuccess % handle.getName()
            else:
                self.accept('friendsMapComplete', self._FriendSecret__nowFriends, [
                    avId])
                ready = base.cr.fillUpFriendsMap()
                if ready:
                    self._FriendSecret__nowFriends(avId)
                
                return None
        elif result == 0:
            self.nextText['text'] = OTPLocalizer.FriendSecretEnteredSecretUnknown
        elif result == 2:
            handle = base.cr.identifyAvatar(avId)
            if handle != None:
                self.nextText['text'] = OTPLocalizer.FriendSecretEnteredSecretFull % handle.getName()
            else:
                self.nextText['text'] = OTPLocalizer.FriendSecretEnteredSecretFullNoName
        elif result == 3:
            self.nextText['text'] = OTPLocalizer.FriendSecretEnteredSecretSelf
        elif result == 4:
            self.nextText['text'] = OTPLocalizer.FriendSecretEnteredSecretWrongProduct % self.prefix
        
        self.nextText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()

    
    def _FriendSecret__useAccountSecret(self, avId, friendInfo):
        self.ignore(OTPGlobals.PlayerFriendUpdateEvent)
        self.ignore(OTPGlobals.PlayerFriendRejectUseSecretEvent)
        self._FriendSecret__enteredSecret(1, 0)

    
    def _FriendSecret__rejectUseAccountSecret(self, reason):
        print '## rejectUseAccountSecret: reason = ', reason
        self.ignore(OTPGlobals.PlayerFriendUpdateEvent)
        self.ignore(OTPGlobals.PlayerFriendRejectUseSecretEvent)
        if reason == RejectCode.RejectCode.FRIENDS_LIST_FULL:
            self._FriendSecret__enteredSecret(2, 0)
        elif reason == RejectCode.RejectCode.ALREADY_FRIENDS_WITH_SELF:
            self._FriendSecret__enteredSecret(3, 0)
        else:
            self._FriendSecret__enteredSecret(0, 0)

    
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


