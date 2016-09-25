# File: C (Python 2.4)

from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.fsm.FSM import FSM
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesgui.ChatBar import ChatBar
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import EmoteGlobals
from otp.chat.TalkGlobals import *
from pirates.chat.PiratesTalkGlobals import *
from otp.speedchat import SCDecoders
from otp.otpbase import OTPLocalizer
import string
import random

class ChatPanel(DirectFrame, FSM):
    NumVisible = 10
    WrapWidth = 22
    WrapWidthSmall = 28
    TextScale = 0.035000000000000003
    TextScaleSmall = 0.028000000000000001
    FadeTime = 0.29999999999999999
    TextFadeDelay = 120
    TextFadeTime = 5
    widthBase = 21.25
    widthVarience = 12.0
    
    def __init__(self, chatManager, whiteListEntry):
        optiondefs = (('relief', None, None), ('state', DGG.NORMAL, self.setState), ('frameSize', (0, 0.90000000000000002, 0, 0.59999999999999998), None), ('frameColor', (1, 0, 1, 0.20000000000000001), None))
        self.defineoptions({ }, optiondefs)
        DirectFrame.__init__(self, parent = NodePath())
        self.initialiseoptions(ChatPanel)
        FSM.__init__(self, 'ChatPanel')
        base.chatPanel = self
        self.chatManager = chatManager
        self.index = 0
        self.runningLineCount = 0
        self.runningLineCountLastId = -1
        self.lineCountList = [
            0]
        self.wrappedText = []
        self.chatFont = PiratesGlobals.getInterfaceFont()
        self.nameFont = PiratesGlobals.getInterfaceFont()
        self.shadowOffset = (0.089999999999999997, 0.089999999999999997)
        self.shadowColor = (0.0, 0.0, 0.0, 1.0)
        self.fontColorStyle = 1
        if base.config.GetBool('want-random-chatStyle', 0):
            self.chatFont = random.choice([
                PiratesGlobals.getInterfaceFont(),
                PiratesGlobals.getInterfaceOutlineFont()])
            self.nameFont = random.choice([
                PiratesGlobals.getInterfaceFont(),
                PiratesGlobals.getInterfaceOutlineFont()])
            self.shadowOffset = random.choice([
                (0.089999999999999997, 0.089999999999999997),
                (0.0, 0.0)])
            self.fontColorStyle = random.choice([
                0,
                1,
                2])
        
        self.lineDict = { }
        self.renderedLineDict = { }
        self.renderedLines = []
        self.wordWrapper = TextNode('wrapper')
        self.wordWrapper.setFont(self.chatFont)
        self.wordWrapper.setWordwrap(self.WrapWidth)
        self.wordWrapper.setTabWidth(1.0)
        self.fadeIval = None
        self.fadeTextIval = None
        self.preferredMode = 'Short'
        self.linesShown = True
        self.holdLinesShown = None
        self.wantSmallFont = 0
        self.currentFontSize = self.TextScale
        self.currentWordWrap = self.WrapWidth
        self.resizeDelayTaskName = 'ChatPanel_Resize'
        self.sCloseButton = None
        self.tCloseButton = None
        self.minButton = None
        self.maxButton = None
        self.setupGui()
        self.chatBar = ChatBar(parent = self, chatMgr = chatManager, whiteListEntry = whiteListEntry)
        self.setBoxWidth(base.options.chatbox_scale)
        self.checkEmotes()
        self.needSlider = 0
        self.reparentTo(base.a2dBottomLeft)
        self.accept('NewOpenMessage', self._ChatPanel__handleOpenMessage)
        self.accept('SetChatBoxWidth', self.setBoxWidth)
        self.accept('SetChatBoxStyle', self.setChatStyle)
        self.accept('GUIHidden', self._ChatPanel__handleGlobalGuiHide)
        self.accept('GUIShown', self._ChatPanel__handleGlobalGuiShow)

    
    def setChatStyle(self, value):
        pass

    
    def setBoxWidth(self, scale):
        self.currentWordWrap = self.widthBase + scale * self.widthVarience
        wordWrapWithBias = self.widthBase + 1.22 * scale * self.widthVarience
        percentage = float(self.currentWordWrap) / float(self.widthBase)
        self.shortBorder.setScale(percentage, 1.0, 1.0)
        self.shortBg.setScale(percentage, 1.0, 1.0)
        self.tallBorder.setScale(percentage, 1.0, 1.0)
        self.tallBg.setScale(percentage, 1.0, 1.0)
        self.wordWrapper.setWordwrap(wordWrapWithBias)
        self.chatDisplayNP.setScale(self.currentFontSize)
        messenger.send('SetChatBoxPercentage', [
            percentage])
        self.chatBar.setBoxWidth(percentage)
        while taskMgr.hasTaskNamed(self.resizeDelayTaskName):
            taskMgr.remove(self.resizeDelayTaskName)
        task = taskMgr.doMethodLater(0.5, self.regenAfterResize, self.resizeDelayTaskName)

    
    def regenAfterResize(self, task):
        self.regenText()
        return task.done

    
    def toggleFontSize(self):
        if self.wantSmallFont == 0:
            self.wantSmallFont = 1
        elif self.wantSmallFont == 1:
            self.wantSmallFont = 0
        
        self.setFontSize(self.wantSmallFont)

    
    def setFontSize(self, size):
        self.wantSmallFont = size
        if self.wantSmallFont == 1:
            self.currentFontSize = self.TextScaleSmall
            self.currentWordWrap = self.WrapWidthSmall
        elif self.wantSmallFont == 0:
            self.currentFontSize = self.TextScale
            self.currentWordWrap = self.WrapWidth
        
        self.wordWrapper.setWordwrap(self.currentWordWrap)
        self.chatDisplayNP.setScale(self.currentFontSize)
        self.regenText()
        self.request('Standby')
        self.request(self.preferredMode)

    
    def setupGui(self):
        self.cleanupGui()
        if hasattr(self, 'chatBar'):
            self.chatBar.detachNode()
        
        self.removeChildren()
        guib = loader.loadModel('models/gui/chat_frame_b')
        guic = loader.loadModel('models/gui/chat_frame_c')
        charGui = loader.loadModelOnce('models/gui/char_gui')
        tGui = loader.loadModel('models/gui/triangle')
        self.hideNode = self.attachNewNode('hideNode')
        cm = CardMaker('shortBg')
        cm.setColor(0, 0, 0, 1)
        cm.setFrame(0.0050000000000000001, 0.89500000000000002, 0.089999999999999997, 0.59499999999999997)
        self.shortBg = self.hideNode.attachNewNode(cm.generate())
        self.shortBg.setTransparency(1)
        self.shortBg.setColor(0, 0, 0, 1)
        self.shortBg.flattenStrong()
        self.shortBg.setColorScale(1, 1, 1, 0)
        self.shortBorder = self.hideNode.attachNewNode('shortBorder')
        top = guib.find('**/pPlane8').copyTo(self.shortBorder)
        top.setZ(-0.75)
        mid = guib.find('**/pPlane9').copyTo(self.shortBorder)
        mid.setScale(1, 1, 0.68000000000000005)
        mid.setZ(-0.40000000000000002)
        guib.find('**/pPlane10').copyTo(self.shortBorder)
        top = guib.find('**/pPlane26').copyTo(self.shortBorder)
        top.setZ(-0.75)
        mid = guib.find('**/pPlane27').copyTo(self.shortBorder)
        mid.setScale(1, 1, 0.68000000000000005)
        mid.setZ(-0.40000000000000002)
        self.shortBorder.setScale(0.20000000000000001)
        self.shortBorder.setPos(0.5, 0, 0.375)
        self.shortBorder.flattenStrong()
        buttonGeom = NodePath('Close')
        guib.find('**/pPlane30').copyTo(buttonGeom)
        guib.find('**/pPlane31').copyTo(buttonGeom)
        guib.find('**/pPlane32').copyTo(buttonGeom)
        buttonGeom.flattenStrong()
        self.sCloseButton = DirectButton(parent = self.shortBorder, relief = None, frameColor = (1, 1, 1, 1), pad = (-0.02, -0.02), borderWidth = (0, 0), geom = buttonGeom, pos = (0.5, 0, 0.22500000000000001), scale = 0.20000000000000001, rolloverSound = None, command = self.chatManager.deactivateChat)
        buttonGeom = NodePath('Max')
        guib.find('**/pPlane22').copyTo(buttonGeom)
        guib.find('**/pPlane23').copyTo(buttonGeom)
        buttonGeom.flattenStrong()
        self.maxButton = DirectButton(parent = self.shortBorder, relief = None, frameColor = (1, 1, 1, 1), pad = (-0.02, -0.02), borderWidth = (0, 0), geom = buttonGeom, pos = (0.5, 0, 0.22500000000000001), scale = 0.20000000000000001, rolloverSound = None, command = self.request, extraArgs = [
            'Tall'])
        cm.setName('tallBg')
        cm.setFrame(0.0050000000000000001, 0.89500000000000002, 0.089999999999999997, 1.3600000000000001)
        self.tallBg = self.hideNode.attachNewNode(cm.generate())
        self.tallBg.setColor(0, 0, 0, 1)
        self.tallBg.setTransparency(1)
        self.tallBg.flattenStrong()
        self.tallBg.setColorScale(1, 1, 1, 0)
        self.tallBorder = self.hideNode.attachNewNode('tallBorder')
        guic.find('**/pPlane8').copyTo(self.tallBorder)
        guic.find('**/pPlane9').copyTo(self.tallBorder)
        guic.find('**/pPlane10').copyTo(self.tallBorder)
        guic.find('**/pPlane26').copyTo(self.tallBorder)
        guic.find('**/pPlane27').copyTo(self.tallBorder)
        self.tallBorder.setScale(0.20000000000000001)
        self.tallBorder.setPos(0.5, 0, 0.375)
        self.tallBorder.flattenStrong()
        buttonGeom = NodePath('Close')
        guic.find('**/pPlane30').copyTo(buttonGeom)
        guic.find('**/pPlane31').copyTo(buttonGeom)
        guic.find('**/pPlane32').copyTo(buttonGeom)
        buttonGeom.flattenStrong()
        self.tCloseButton = DirectButton(parent = self.tallBorder, relief = None, frameColor = (1, 1, 1, 1), pad = (-0.02, -0.02), borderWidth = (0, 0), geom = buttonGeom, pos = (0.5, 0, 0.375), scale = 0.20000000000000001, rolloverSound = None, command = self.chatManager.deactivateChat)
        buttonGeom = NodePath('Min')
        guic.find('**/pPlane28').copyTo(buttonGeom)
        guic.find('**/pPlane29').copyTo(buttonGeom)
        buttonGeom.flattenStrong()
        self.minButton = DirectButton(parent = self.tallBorder, relief = None, frameColor = (1, 1, 1, 1), pad = (-0.02, -0.02), borderWidth = (0, 0), geom = buttonGeom, pos = (0.54800000000000004, 0, 0.375), scale = 0.20000000000000001, rolloverSound = None, command = self.request, extraArgs = [
            'Short'])
        self.chatTextRender = TextNode('chatTextRender')
        self.chatTextRender.setFont(self.chatFont)
        self.chatTextRender.setShadowColor(self.shadowColor)
        self.chatTextRender.setShadow(self.shadowOffset)
        self.chatDisplayNP = self.hideNode.attachNewNode('chatDisplay')
        self.chatDisplayNP.setScale(self.TextScale)
        self.chatDisplayNP.setColorScale(1, 1, 1, 1)
        self.chatDisplayNP.showThrough()
        self._ChatPanel__showLines()
        self.slider = DirectScrollBar(parent = self, relief = None, manageButtons = 0, resizeThumb = 0, frameSize = (-0.0060000000000000001, 0.0060000000000000001, -0.080000000000000002, 0.080000000000000002), image = charGui.find('**/chargui_slider_small'), image_scale = (0.17999999999999999, 0.035000000000000003, 0.070000000000000007), image_hpr = (0, 0, 90), thumb_image = (charGui.find('**/chargui_slider_node'), charGui.find('**/chargui_slider_node_down'), charGui.find('**/chargui_slider_node_over')), thumb_image_scale = 0.074999999999999997, thumb_relief = None, decButton_pos = Vec3(0, 0, -0.082500000000000004), decButton_image = (tGui.find('**/triangle'), tGui.find('**/triangle_down'), tGui.find('**/triangle_over')), decButton_image_hpr = (0, 0, 90), decButton_scale = (0.080000000000000002, 1.0, 0.125), decButton_image_scale = 0.074999999999999997, decButton_relief = None, incButton_pos = Vec3(0.00025000000000000001, 0, 0.082500000000000004), incButton_image = (tGui.find('**/triangle'), tGui.find('**/triangle_down'), tGui.find('**/triangle_over')), incButton_image_hpr = (0, 0, -90), incButton_scale = (0.080000000000000002, 1.0, 0.125), incButton_image_scale = 0.074999999999999997, incButton_relief = None, scale = 5.7000000000000002, pos = (0.051999999999999998, 0, 0.69999999999999996), value = 0, range = (0, self.NumVisible), scrollSize = 1, pageSize = 1, orientation = DGG.VERTICAL_INVERTED, command = self.scrollList)
        self.slider.hide()
        self.slider.setName('chatPanel.slider')
        if hasattr(self, 'chatBar'):
            self.chatBar.reparentTo(self)
        
        self.request('Standby')
        self.updateDisplay()

    
    def cleanupGui(self):
        if self.sCloseButton:
            self.sCloseButton.detachNode()
            self.sCloseButton.destroy()
        
        if self.tCloseButton:
            self.tCloseButton.detachNode()
            self.tCloseButton.destroy()
        
        if self.minButton:
            self.minButton.detachNode()
            self.minButton.destroy()
        
        if self.maxButton:
            self.maxButton.detachNode()
            self.maxButton.destroy()
        
        self.wrappedText = []
        self.lineDict = { }
        self.renderedLineDict = { }
        self.renderedLines = []
        self.shortBg = None
        self.shortBorder = None
        self.tallBg = None
        self.tallBorder = None
        self.sCloseButton = None
        self.maxButton = None
        self.tCloseButton = None
        self.minButton = None
        self.chatTextRender = None
        self.chatDisplayNP = None
        self.slider = None

    
    def destroy(self):
        self.chatFont = None
        self.nameFont = None
        self.ignore('NewOpenMessage')
        self.ignore(PiratesGlobals.HideGuiHotkey)
        self.stopFadeIval()
        self.stopFadeTextIval()
        self.stopFadeTextTimer()
        self.slider.destroy()
        self.cleanupGui()
        DirectFrame.destroy(self)
        self.chatManager = None
        base.chatPanel = None

    
    def activateAllChat(self):
        self.requestPreferredMode()
        self.chatBar.request('All')

    
    def activateCrewChat(self):
        self.requestPreferredMode()
        self.chatBar.request('Crew')

    
    def activateGuildChat(self):
        self.requestPreferredMode()
        self.chatBar.request('Guild')

    
    def activateShipPVPChat(self):
        self.requestPreferredMode()
        self.chatBar.request('ShipPVP')

    
    def activateWhisperChat(self, whisperId, toPlayer = False):
        self.requestPreferredMode()
        name = base.talkAssistant.findName(whisperId, toPlayer)
        self.chatBar.request('Whisper', name, whisperId)

    
    def deactivateChat(self):
        self.request('Standby')
        self.chatBar.request('Hidden')

    
    def updateState(self, state):
        self['state'] = state

    
    def setState(self):
        DirectFrame.setState(self)
        if hasattr(self, 'sCloseButton'):
            self.sCloseButton['state'] = self['state']
            self.maxButton['state'] = self['state']
            self.tCloseButton['state'] = self['state']
            self.minButton['state'] = self['state']
            self.slider['state'] = self['state']
        

    
    def startFadeInIval(self):
        self.stopFadeIval()
        self.fadeIval = Parallel(Func(self.updateState, DGG.NORMAL), Func(self.hideNode.show), self.shortBg.colorScaleInterval(self.FadeTime, Vec4(1, 1, 1, 0.75), blendType = 'easeOut'), self.shortBorder.colorScaleInterval(self.FadeTime, Vec4(1, 1, 1, 1), blendType = 'easeOut'), self.tallBg.colorScaleInterval(self.FadeTime, Vec4(1, 1, 1, 0.75), blendType = 'easeOut'), self.tallBorder.colorScaleInterval(self.FadeTime, Vec4(1, 1, 1, 1), blendType = 'easeOut'), self.slider.colorScaleInterval(self.FadeTime, Vec4(1, 1, 1, 1), blendType = 'easeOut'))
        self.fadeIval.start()

    
    def startFadeOutIval(self):
        self.stopFadeIval()
        self.fadeIval = Parallel(Func(self.updateState, DGG.DISABLED), self.shortBg.colorScaleInterval(self.FadeTime, Vec4(1, 1, 1, 0), blendType = 'easeIn'), self.shortBorder.colorScaleInterval(self.FadeTime, Vec4(1, 1, 1, 0), blendType = 'easeIn'), self.tallBg.colorScaleInterval(self.FadeTime, Vec4(1, 1, 1, 0), blendType = 'easeIn'), self.tallBorder.colorScaleInterval(self.FadeTime, Vec4(1, 1, 1, 0), blendType = 'easeIn'), self.slider.colorScaleInterval(self.FadeTime, Vec4(1, 1, 1, 0), blendType = 'easeIn'), Sequence(Wait(self.FadeTime), Func(self.hideNode.hide)))
        self.fadeIval.start()

    
    def stopFadeIval(self):
        if self.fadeIval:
            self.fadeIval.pause()
        
        self.fadeIval = None

    
    def startFadeTextIval(self):
        self.stopFadeTextIval()
        self.fadeTextIval = Sequence()
        self.fadeTextIval.append(self.chatDisplayNP.colorScaleInterval(self.TextFadeTime, Vec4(1, 1, 1, 0)))
        self.fadeTextIval.append(Func(self._ChatPanel__hideLines))
        self.fadeTextIval.start()

    
    def stopFadeTextIval(self):
        if self.fadeTextIval:
            self.fadeTextIval.pause()
        
        self.fadeTextIval = None

    
    def unfadeText(self):
        self.stopFadeTextIval()
        self.chatDisplayNP.setColorScale(1, 1, 1, 1)
        self._ChatPanel__showLines()

    
    def startFadeTextTimer(self):
        self.stopFadeTextTimer()
        taskMgr.doMethodLater(self.TextFadeDelay, self.startFadeTextIval, 'ChatPanel-fadeText', [])

    
    def stopFadeTextTimer(self):
        taskMgr.remove('ChatPanel-fadeText')

    
    def requestPreferredMode(self):
        self.request(self.preferredMode)

    
    def defaultFilter(self, request, args):
        if self.getCurrentOrNextState() == request:
            return None
        else:
            return FSM.defaultFilter(self, request, args)

    
    def enterStandby(self):
        messenger.send('chatPanelClose')
        self.startFadeOutIval()
        self.startFadeTextTimer()
        self.NumVisible = 10
        (self.chatDisplayNP.setPos(0.089999999999999997, 0, 0.20000000000000001 + 9.1430000000000007 * self.currentFontSize),)
        self.index = 0
        self.slider['value'] = self.index
        self.updateDisplay()

    
    def exitStandby(self):
        messenger.send('chatPanelOpen')
        self.startFadeInIval()
        self.stopFadeTextTimer()
        self.unfadeText()

    
    def enterShort(self):
        messenger.send('chatPanelMin')
        self.slider.hide()
        self.shortBg.show()
        self.shortBorder.show()
        self.tallBg.hide()
        self.tallBorder.hide()
        (self.chatDisplayNP.setPos(0.089999999999999997, 0, 0.20000000000000001 + 9.1430000000000007 * self.currentFontSize),)
        self.preferredMode = 'Short'
        self.NumVisible = 10
        self.index = 0
        self.slider['value'] = self.index
        self.updateDisplay()

    
    def exitShort(self):
        pass

    
    def enterTall(self):
        messenger.send('chatPanelMax')
        self.tallBg.show()
        self.tallBorder.show()
        self.shortBg.hide()
        self.shortBorder.hide()
        self.slider.show()
        (self.chatDisplayNP.setPos(0.089999999999999997, 0, 0.20000000000000001 + 31.143000000000001 * self.currentFontSize),)
        self.preferredMode = 'Tall'
        self.NumVisible = 32
        self.index = 0
        self.slider['value'] = self.index
        self.updateDisplay()
        localAvatar.guiMgr.messageStackParent.setPos(0, 0, 0.75)

    
    def exitTall(self):
        localAvatar.guiMgr.messageStackParent.setPos(0, 0, 0.0)

    
    def getMessageTagText(self, message, wantReceiver = False):
        chatString = ''
        plainName = ''
        tag = ''
        extraInfo = ''
        divider = ':'
        seperator = '.'
        annouceMark = ' '
        isAnnounce = 0
        if message.getExtraInfo():
            extraInfo = message.getExtraInfo()
        
        if wantReceiver and message.getReceiverAvatarName():
            plainName = message.getReceiverAvatarName()
        elif message.getSenderAvatarName():
            plainName = message.getSenderAvatarName()
        elif message.getSenderAccountName():
            plainName = message.getSenderAccountName()
        
        if message.getTalkType() in (INFO_SYSTEM, INFO_GAME, UPDATE_FRIEND, CANNON_DEFENSE, INFO_GUILD):
            if wantReceiver:
                useName = plainName
            else:
                useName = '\x1Super\x1.\x2 ' + plainName
        elif message.getTalkType() == INFO_OPEN:
            if message.getSenderAvatarId() == localAvatar.doId:
                useName = ''
            else:
                useName = plainName
        elif message.getTalkType() == INFO_DEV:
            useName = ''
        elif message.getTalkType() in (TALK_OPEN, TALK_WHISPER, TALK_ACCOUNT, AVATAR_THOUGHT):
            if message.getTalkType() == TALK_WHISPER:
                if message.getSenderAvatarId() == localAvatar.doId:
                    plainName = OTPLocalizer.WhisperToFormatName % message.getReceiverAvatarName()
                else:
                    plainName = OTPLocalizer.WhisperFromFormatName % message.getSenderAvatarName()
            elif message.getTalkType() == TALK_ACCOUNT:
                if message.getSenderAccountId() == base.cr.accountDetailRecord.playerAccountId:
                    plainName = OTPLocalizer.WhisperToFormatName % message.getReceiverAccountName()
                else:
                    plainName = OTPLocalizer.WhisperFromFormatName % message.getSenderAccountName()
            
            if message.getTalkType() == AVATAR_THOUGHT:
                if message.getSenderAvatarId() == localAvatar.doId:
                    plainName = OTPLocalizer.ThoughtSelfFormatName
                else:
                    plainName = OTPLocalizer.ThoughtOtherFormatName % message.getSenderAvatarName()
            
            useName = plainName + divider
        elif message.getTalkType() == TALK_GM:
            useName = '[' + PLocalizer.TalkGMLabel + '] ' + plainName + divider
        elif message.getTalkType() == TALK_GUILD:
            useName = '[' + PLocalizer.TalkGuildLabel + '] ' + plainName + divider
        elif message.getTalkType() == UPDATE_GUILD:
            useName = '\x1Super\x1.\x2 [' + PLocalizer.TalkGuildLabel + '] ' + plainName
        elif message.getTalkType() == TALK_PARTY:
            useName = '[' + PLocalizer.TalkCrewLabel + '] ' + plainName + divider
        elif message.getTalkType() == UPDATE_PARTY:
            useName = '\x1Super\x1.\x2 [' + PLocalizer.TalkCrewLabel + '] ' + plainName
        elif message.getTalkType() == TALK_PVP:
            useName = '[' + extraInfo + '] ' + plainName + divider
        elif message.getTalkType() == UPDATE_PVP:
            useName = '\x1Super\x1.\x2 [' + extraInfo + '] ' + plainName
        
        return useName

    
    def decodeOpenMessage(self, message):
        nameButton = None
        extraInfo = message.getExtraInfo()
        useName = self.getMessageTagText(message)
        if message.getTalkType() == INFO_GUILD:
            useName2 = self.getMessageTagText(message, wantReceiver = True)
        
        tpMgr = TextPropertiesManager.getGlobalPtr()
        buttonCommand = None
        buttonArgs = None
        buttonCommand2 = None
        buttonArgs2 = None
        if message.getSenderAvatarId() == localAvatar.doId:
            if message.getTalkType() == TALK_WHISPER:
                buttonCommand = self.handleAvatarPress
                buttonArgs = [
                    message.getReceiverAvatarId(),
                    useName]
            else:
                buttonCommand = self.handleAvatarPress
                buttonArgs = [
                    message.getSenderAvatarId(),
                    useName]
        elif message.getTalkType() == TALK_ACCOUNT and message.getSenderAccountId():
            if message.getSenderAccountId() == base.cr.accountDetailRecord.playerAccountId:
                buttonCommand = self.handlePlayerPress
                buttonArgs = [
                    message.getReceiverAccountId(),
                    useName]
            else:
                buttonCommand = self.handlePlayerPress
                buttonArgs = [
                    message.getSenderAccountId(),
                    useName]
        elif message.getSenderAvatarId():
            buttonCommand = self.handleAvatarPress
            buttonArgs = [
                message.getSenderAvatarId(),
                useName]
        elif message.getSenderAccountId():
            buttonCommand = self.handlePlayerPress
            buttonArgs = [
                message.getSenderAccountId(),
                useName]
        
        if message.getTalkType() == INFO_GUILD and message.getReceiverAvatarId():
            wantTwoNames = True
        else:
            wantTwoNames = False
        if wantTwoNames:
            buttonCommand2 = self.handleAvatarPress
            buttonArgs2 = [
                message.getReceiverAvatarId(),
                useName2]
        
        nameArray = ('\x1' + MESSAGE_COLOR_TABLE[message.getTalkType()][self.fontColorStyle] + '\x1' + useName + '\x2', '\x1' + MESSAGE_COLOR_TABLE[message.getTalkType()][self.fontColorStyle] + '\x1' + useName + '\x2', '\x1' + MESSAGE_OVER_TABLE[message.getTalkType()][self.fontColorStyle] + '\x1' + useName + '\x2', '\x1' + MESSAGE_COLOR_TABLE[message.getTalkType()][self.fontColorStyle] + '\x1' + useName + '\x2')
        nameButton = DirectButton(parent = NodePath(), relief = None, text = nameArray, text_align = TextNode.ALeft, text_pos = (0.0, 0.0), text_shadow = self.shadowColor, text_shadowOffset = self.shadowOffset, text_font = self.nameFont, textMayChange = 0, command = buttonCommand, extraArgs = buttonArgs)
        (left, right, bottom, top) = nameButton.getBounds()
        nameGFX = TextGraphic(nameButton, left, right, 0, 1)
        buttonName = '%s%s' % (message.getTalkType(), useName)
        tpMgr.setGraphic(buttonName, nameGFX)
        if wantTwoNames:
            nameArray2 = ('\x1' + MESSAGE_COLOR_TABLE[message.getTalkType()][self.fontColorStyle] + '\x1' + useName2 + '\x2', '\x1' + MESSAGE_COLOR_TABLE[message.getTalkType()][self.fontColorStyle] + '\x1' + useName2 + '\x2', '\x1' + MESSAGE_OVER_TABLE[message.getTalkType()][self.fontColorStyle] + '\x1' + useName2 + '\x2', '\x1' + MESSAGE_COLOR_TABLE[message.getTalkType()][self.fontColorStyle] + '\x1' + useName2 + '\x2')
            nameButton2 = DirectButton(parent = NodePath(), relief = None, text = nameArray2, text_align = TextNode.ALeft, text_pos = (0.0, 0.0), text_shadow = self.shadowColor, text_shadowOffset = self.shadowOffset, text_font = self.nameFont, textMayChange = 0, command = buttonCommand2, extraArgs = buttonArgs2)
            (left, right, bottom, top) = nameButton2.getBounds()
            nameGFX2 = TextGraphic(nameButton2, left, right, 0, 1)
            buttonName2 = '%s%s' % (message.getTalkType(), useName2)
            tpMgr.setGraphic(buttonName2, nameGFX2)
        
        del tpMgr
        self.lineDict[message.getMessageId()] = (message, nameButton, buttonName)
        if nameButton:
            messageName = '\x5' + buttonName + '\x5'
            if wantTwoNames:
                messageName2 = '\x5' + buttonName2 + '\x5'
            
        else:
            messageName = message.getSenderAvatarName() + ': '
        messageBody = message.getBody()
        chatString = ''
        if '%s' in message.getBody() and message.getTalkType() == INFO_OPEN:
            someMessage = message.getBody() % messageName
        elif '%s' in message.getBody() and message.getTalkType() == INFO_GUILD:
            if wantTwoNames:
                if extraInfo:
                    someMessage = message.getBody() % (messageName, messageName2, extraInfo[0])
                else:
                    someMessage = message.getBody() % (messageName, messageName2)
            elif extraInfo:
                someMessage = message.getBody() % (messageName, extraInfo[0])
            else:
                someMessage = message.getBody() % messageName
        else:
            someMessage = messageName + message.getBody()
        chatCode = MESSAGE_STYLE_TABLE[message.getTalkType()][self.fontColorStyle]
        self.wordWrapper.setText(someMessage)
        wrappedText = self.wordWrapper.getWordwrappedText().split('\n')
        tab = '    '
        for i in range(len(wrappedText)):
            if i == 0:
                if chatCode:
                    wrappedText[i] = '\x1' + chatCode + '\x1' + wrappedText[i] + '\x2'
                
            elif i > 0:
                wrappedText[i] = '    ' + '\x1' + chatCode + '\x1' + wrappedText[i] + '\x2'
            
            if i < len(wrappedText) - 1:
                wrappedText[i] += '\n'
                continue
        
        for text in wrappedText:
            chatString += text
        
        return chatString

    
    def clearText(self):
        tpMgr = TextPropertiesManager.getGlobalPtr()
        for key in self.lineDict:
            (message, nameButton, buttonName) = self.lineDict[key]
            nameButton.destroy()
            tpMgr.clearGraphic(buttonName)
        
        self.renderedLineDict = { }
        self.lineDict = { }
        del tpMgr

    
    def regenText(self):
        self.clearText()
        self.updateDisplay()

    
    def regenLineCountList(self):
        self.runningLineCount = 0
        self.runningLineCountLastId = -1
        self.lineCountList = [
            0]
        allMessages = base.talkAssistant.getAllCompleteText()
        for message in allMessages:
            self.wordWrapper.setText(self.getMessageTagText(message) + message.getBody())
            wrappedText = self.wordWrapper.getWordwrappedText()
            if message.getMessageId() > self.runningLineCountLastId:
                self.runningLineCountLastId = message.getMessageId()
            
            for mline in wrappedText.split('\n'):
                self.lineCountList.append(message.getMessageId())
                self.runningLineCount += 1
            
        

    
    def putText(self, startLine, numLines):
        startMessage = self.lineCountList[startLine]
        messageList = base.talkAssistant.getCompleteTextFromRecent(self.NumVisible, startMessage)
        displayText = []
        tpMgr = TextPropertiesManager.getGlobalPtr()
        lineHeight = self.chatFont.getLineHeight()
        self.renderedLines = []
        messageIdList = []
        for message in messageList:
            if base.cr.avatarFriendsManager.checkIgnored(message.getSenderAvatarId()):
                continue
            
            messageIdList.append(message.getMessageId())
            if not self.renderedLineDict.get(message):
                msg = self.decodeOpenMessage(message)
                messageRenderedLines = []
                self.renderedLineDict[message] = messageRenderedLines
                for mline in msg.split('\n'):
                    self.chatTextRender.setText(mline)
                    newLine = self.chatTextRender.generate()
                    messageRenderedLines.append(newLine)
                
            
            self.renderedLines = self.renderedLineDict[message] + self.renderedLines
            if len(self.renderedLines) >= self.NumVisible:
                break
                continue
        
        removeIds = []
        removeRendered = []
        for key in self.lineDict:
            if key not in messageIdList:
                (message, nameButton, buttonName) = self.lineDict[key]
                nameButton.destroy()
                tpMgr.clearGraphic(buttonName)
                removeIds.append(key)
                removeRendered.append(message)
                continue
        
        for message in removeRendered:
            self.renderedLineDict.pop(message)
        
        for key in removeIds:
            self.lineDict.pop(key)
        
        self.renderedLines = self.renderedLines[-(self.NumVisible):]
        self.chatDisplayNP.getChildren().detach()
        z = -lineHeight * (self.NumVisible - len(self.renderedLines))
        for rline in self.renderedLines:
            np = self.chatDisplayNP.attachNewNode(rline)
            np.setZ(z)
            z -= lineHeight
        
        del tpMgr
        self.updateRange()

    
    def _ChatPanel__handleOpenMessage(self, message):
        self.index = 0
        if message.getMessageId() > self.runningLineCountLastId:
            self.runningLineCountLastId = message.getMessageId()
            self.wordWrapper.setText(self.getMessageTagText(message) + message.getBody())
            wrappedText = self.wordWrapper.getWordwrappedText()
            for mline in wrappedText.split('\n'):
                self.lineCountList.append(message.getMessageId())
                self.runningLineCount += 1
            
        
        self.updateDisplay()
        self.unfadeText()
        if self.getCurrentOrNextState() == 'Standby':
            self.startFadeTextTimer()
        

    
    def _ChatPanel__handleGlobalGuiShow(self):
        if self._ChatPanel__showLines:
            self.chatDisplayNP.showThrough()
        

    
    def _ChatPanel__handleGlobalGuiHide(self):
        if self.linesShown:
            self.chatDisplayNP.show()
        

    
    def _ChatPanel__showLines(self):
        self.linesShown = True
        if base.showGui:
            self.chatDisplayNP.showThrough()
        else:
            self.chatDisplayNP.show()

    
    def _ChatPanel__hideLines(self):
        self.linesShown = False
        self.chatDisplayNP.hide()

    
    def updateDisplay(self):
        if hasattr(base, 'talkAssistant'):
            self.putText(self.index, self.NumVisible)
        

    
    def updateRange(self):
        numLines = self.runningLineCount
        if self.getCurrentOrNextState() != 'Tall':
            self.index = 0
            return None
        
        maxRange = self.runningLineCount - int(self.NumVisible * 0.66000000000000003)
        maxRange = max(maxRange, 0)
        if maxRange:
            if self.getCurrentOrNextState() == 'Tall':
                self.slider.show()
            
            self.slider['range'] = (0, maxRange)
            self.index = min(self.index, self.slider['range'][1])
            self.index = max(self.index, self.slider['range'][0])
        else:
            self.slider.hide()
            self.index = 0

    
    def scrollList(self):
        index = int(self.slider.getValue())
        if self.index != index:
            self.index = index
            self.updateDisplay()
        

    
    def enableCrewChat(self):
        self.chatBar.refreshTabStates()

    
    def disableCrewChat(self):
        self.chatBar.refreshTabStates()

    
    def enableGuildChat(self):
        self.chatBar.refreshTabStates()

    
    def disableGuildChat(self):
        self.chatBar.refreshTabStates()

    
    def disableShipPVPChat(self):
        self.chatBar.refreshTabStates()

    
    def enableShipPVPChat(self):
        self.chatBar.refreshTabStates()

    
    def enableWhiteListChat(self):
        self.chatBar.enableWhiteListChat()

    
    def disableWhiteListChat(self):
        self.chatBar.disableWhiteListChat()

    
    def checkEmotes(self):
        for id in PLocalizer.EmoteCommands.values():
            if type(id) == type((0,)):
                continue
        

    
    def hide(self):
        self.holdLinesShown = self.linesShown
        NodePath.hide(self)
        self._ChatPanel__hideLines()

    
    def show(self):
        DirectFrame.show(self)
        if self.holdLinesShown:
            self._ChatPanel__showLines()
        

    
    def handleAvatarPress(self, avId, avName):
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            base.localAvatar.guiMgr.handleAvatarDetails(avId, avName)
        

    
    def handlePlayerPress(self, pId, pName):
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            base.localAvatar.guiMgr.handlePlayerDetails(pId, pName)
        


