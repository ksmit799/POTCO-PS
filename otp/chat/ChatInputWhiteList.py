from direct.fsm import FSM
from otp.otpbase import OTPGlobals
import sys
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from otp.otpbase import OTPLocalizer
from direct.task import Task
from otp.chat.ChatInputTyped import ChatInputTyped

class ChatInputWhiteList(FSM.FSM, DirectEntry):
    notify = DirectNotifyGlobal.directNotify.newCategory('ChatInputWhiteList')
    ExecNamespace = None
    
    def __init__(self, parent = None, **kw):
        FSM.FSM.__init__(self, 'ChatInputWhiteList')
        optiondefs = (('parent', parent, None), ('relief', DGG.SUNKEN, None), ('text_scale', 0.029999999999999999, None), ('frameSize', (-0.20000000000000001, 25.300000000000001, -0.5, 1.2), None), ('borderWidth', (0.0030000000000000001, 0.0030000000000000001), None), ('frameColor', (0.90000000000000002, 0.90000000000000002, 0.84999999999999998, 0.80000000000000004), None), ('entryFont', OTPGlobals.getInterfaceFont(), None), ('width', 25, None), ('numLines', 1, None), ('cursorKeys', 1, None), ('backgroundFocus', 0, None), ('suppressKeys', 1, None), ('suppressMouse', 1, None), ('command', self.sendChat, None), ('failedCommand', self.sendFailed, None), ('focus', 0, None), ('text', '', None))
        self.defineoptions(kw, optiondefs)
        DirectEntry.__init__(self, parent = parent, **None)
        self.initialiseoptions(ChatInputWhiteList)
        self.whisperId = None
        wantHistory = 0
        if __dev__:
            wantHistory = 1
        
        self.wantHistory = base.config.GetBool('want-chat-history', wantHistory)
        self.history = [
            '']
        self.historySize = base.config.GetInt('chat-history-size', 10)
        self.historyIndex = 0
        self.whiteList = None
        self.active = 0
        self.autoOff = 0
        self.alwaysSubmit = False
        DirectGuiGlobals = DirectGuiGlobals
        import direct.gui
        self.bind(DirectGuiGlobals.TYPE, self.applyFilter)
        self.bind(DirectGuiGlobals.ERASE, self.applyFilter)
        tpMgr = TextPropertiesManager.getGlobalPtr()
        Red = tpMgr.getProperties('red')
        Red.setTextColor(1.0, 0.0, 0.0, 1)
        tpMgr.setProperties('WLRed', Red)
        del tpMgr
        self.origFrameColor = self['frameColor']
        self.origTextScale = self['text_scale']
        self.origFrameSize = self['frameSize']

    
    def delete(self):
        self.ignore('arrow_up-up')
        self.ignore('arrow_down-up')

    
    def requestMode(self, mode, *args):
        self.request(mode, *args)

    
    def defaultFilter(self, request, *args):
        if request == 'AllChat':
            pass
        1
        if request == 'PlayerWhisper':
            if not base.talkAssistant.checkWhisperSpeedChatPlayer(self.whisperId):
                messenger.send('Chat-Failed player typed chat test')
                return None
            
        elif request == 'AvatarWhisper':
            if not base.talkAssistant.checkWhisperSpeedChatAvatar(self.whisperId):
                messenger.send('Chat-Failed avatar typed chat test')
                return None
            
        
        return FSM.FSM.defaultFilter(self, request, *args)

    
    def enterOff(self):
        self.deactivate()

    
    def exitOff(self):
        self.activate()

    
    def enterAllChat(self):
        self['focus'] = 1
        self.show()

    
    def exitAllChat(self):
        pass

    
    def enterGuildChat(self):
        self['focus'] = 1
        self.show()

    
    def exitGuildChat(self):
        pass

    
    def enterCrewChat(self):
        self['focus'] = 1
        self.show()

    
    def exitCrewChat(self):
        pass

    
    def enterShipPVPChat(self):
        self['focus'] = 1
        self.show()

    
    def exitShipPVPChat(self):
        pass

    
    def enterPlayerWhisper(self, whisperId):
        self.tempText = self.get()
        self.activate()
        self.whisperId = whisperId

    
    def exitPlayerWhisper(self):
        self.set(self.tempText)
        self.whisperId = None

    
    def enterAvatarWhisper(self, whisperId):
        self.tempText = self.get()
        self.activate()
        self.whisperId = whisperId

    
    def exitAvatarWhisper(self):
        self.set(self.tempText)
        self.whisperId = None

    
    def activate(self):
        self.set('')
        self['focus'] = 1
        self.show()
        self.active = 1
        self.guiItem.setAcceptEnabled(True)
        self.accept('uber-escape', self.handleEscape)
        if self.wantHistory:
            self.accept('arrow_up-up', self.getPrevHistory)
            self.accept('arrow_down-up', self.getNextHistory)
        

    
    def deactivate(self):
        self.ignore('uber-escape')
        self.set('')
        self['focus'] = 0
        self.hide()
        self.active = 0
        self.ignore('arrow_up-up')
        self.ignore('arrow_down-up')

    
    def handleEscape(self):
        localAvatar.chatMgr.deactivateChat()

    
    def isActive(self):
        return self.active

    
    def _checkShouldFilter(self, text):
        if len(text) > 0 and text[0] in [
            '/']:
            return False
        else:
            return True

    
    def sendChat(self, text, overflow = False):
        text = self.get(plain = True)
        if text:
            self.set('')
            if base.config.GetBool('exec-chat', 0) and text[0] == '>':
                if text[1:]:
                    ext = base.talkAssistant.execMessage(text[1:])
                    base.talkAssistant.receiveDeveloperMessage(text)
                    base.talkAssistant.receiveDeveloperMessage(ext)
                    base.localAvatar.setChatAbsolute(ext, CFSpeech | CFTimeout)
                    if self.wantHistory:
                        self.addToHistory(text)
                    
                    localAvatar.chatMgr.deactivateChat()
                    localAvatar.chatMgr.activateChat()
                    self.set('>')
                    self.setCursorPosition(1)
                    return None
                else:
                    localAvatar.chatMgr.deactivateChat()
            elif base.config.GetBool('want-slash-commands', 1) and text[0] == '/':
                base.talkAssistant.executeSlashCommand(text)
            elif (localAvatar.isGM() or base.cr.wantMagicWords) and text[0] == '`':
                base.talkAssistant.executeGMCommand(text)
            else:
                self.sendChatByMode(text)
            if self.wantHistory:
                self.addToHistory(text)
            
        else:
            localAvatar.chatMgr.deactivateChat()
        if not overflow:
            self.hide()
            if self.autoOff:
                self.requestMode('Off')
            
            localAvatar.chatMgr.messageSent()
        

    
    def sendChatByMode(self, text):
        state = self.getCurrentOrNextState()
        messenger.send('sentRegularChat')
        if state == 'PlayerWhisper':
            base.talkAssistant.sendAccountTalk(text, self.whisperId)
        elif state == 'AvatarWhisper':
            base.talkAssistant.sendWhisperTalk(text, self.whisperId)
        else:
            base.talkAssistant.sendOpenTalk(text)

    
    def sendFailed(self, text):
        self['frameColor'] = (0.90000000000000002, 0.0, 0.0, 0.80000000000000004)
        
        def resetFrameColor(task = None):
            self['frameColor'] = self.origFrameColor
            return Task.done

        taskMgr.doMethodLater(0.10000000000000001, resetFrameColor, 'resetFrameColor')
        self.applyFilter(keyArgs = None, strict = False)
        self.guiItem.setAcceptEnabled(True)

    
    def chatOverflow(self, overflowText):
        self.sendChat(self.get(plain = True), overflow = True)

    
    def addToHistory(self, text):
        self.history = [
            text] + self.history[:self.historySize - 1]
        self.historyIndex = 0

    
    def getPrevHistory(self):
        self.set(self.history[self.historyIndex])
        self.historyIndex += 1
        self.historyIndex %= len(self.history)
        self.setCursorPosition(len(self.get()))

    
    def getNextHistory(self):
        self.set(self.history[self.historyIndex])
        self.historyIndex -= 1
        self.historyIndex %= len(self.history)
        self.setCursorPosition(len(self.get()))

    
    def importExecNamespace(self):
        pass

    
    def _ChatInputWhiteList__execMessage(self, message):
        print '_execMessage %s' % message
        if not ChatInputTyped.ExecNamespace:
            ChatInputTyped.ExecNamespace = { }
            exec 'from panda3d.core import *' in globals(), self.ExecNamespace
            self.importExecNamespace()

        try:
            return str(eval(message, globals(), ChatInputTyped.ExecNamespace))
        except SyntaxError:
            #TODO
            pass
    
    def applyFilter(self, keyArgs, strict = False):
        text = self.get(plain = True)
        if len(text) > 0:
            if text[0] == '/':
                self.guiItem.setAcceptEnabled(True)
                return None
            elif text[0] == '>' and base.config.GetBool('exec-chat', 0):
                self.guiItem.setAcceptEnabled(True)
                return None
            elif text[0] == '~' and base.cr.wantMagicWords:
                self.guiItem.setAcceptEnabled(True)
                return None
            
        
        words = text.split(' ')
        newwords = []
        self.notify.debug('%s' % words)
        okayToSubmit = True
        for word in words:
            if word == '' or self.whiteList.isWord(word):
                newwords.append(word)
                continue
            okayToSubmit = False
            newwords.append('\x01WLEnter\x01' + word + '\x02')
        
        if not strict:
            lastword = words[-1]
            if lastword == '' or self.whiteList.isPrefix(lastword):
                newwords[-1] = lastword
            else:
                newwords[-1] = '\x01WLEnter\x01' + lastword + '\x02'
        
        if not okayToSubmit:
            pass
        self.guiItem.setAcceptEnabled(self.alwaysSubmit)
        newtext = ' '.join(newwords)
        self.set(newtext)


