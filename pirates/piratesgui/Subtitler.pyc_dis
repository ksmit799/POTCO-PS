# File: S (Python 2.4)

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase import DirectObject
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui.GuiButton import GuiButton
from pirates.piratesgui.DialogButton import DialogButton

class Subtitler(DirectObject.DirectObject):
    
    def __init__(self):
        DirectObject.DirectObject.__init__(self)
        self.event = None
        self.sfx = None
        self.text = DirectLabel(parent = render2d, relief = None, text = '', text_align = TextNode.ACenter, text_scale = 0.055, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 1, text_font = PiratesGlobals.getPirateFont(), pos = (0, 0, -0.90000000000000002), sortOrder = 80)
        self.confirmButton = DialogButton(parent = base.a2dBottomRight, pos = (-0.14999999999999999, 0, 0.095000000000000001), text = PLocalizer.MakeAPirateNext, text_scale = 0.050000000000000003, text_pos = (0.040000000000000001, -0.017999999999999999), text_fg = PiratesGuiGlobals.TextFG2, textMayChange = 1, command = self.advancePageNumber, sortOrder = 90, buttonStyle = DialogButton.YES)
        self.EscText = DirectLabel(parent = render2d, relief = None, text = '', text_align = TextNode.ALeft, text_scale = 0.055, text_fg = PiratesGuiGlobals.TextFG9, text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 1, text_font = PiratesGlobals.getPirateFont(), pos = (-0.92000000000000004, 0, 0.88), sortOrder = 80)
        base.transitions.loadLetterbox()
        self.text.setScale(aspect2d, 1)
        self.accept('aspectRatioChanged', self.text.setScale, [
            aspect2d,
            1])
        self.text.hide()
        self.confirmButton.hide()
        self.EscText.hide()
        self.fader = None
        self.subtitleParent = render2d.attachNewNode(PGTop('subtitleParent'))
        self.subtitleParent.node().setMouseWatcher(base.mouseWatcherNode)
        self._Subtitler__chatPageNumber = None
        self._Subtitler__chatPages = None
        self._Subtitler__chatMessage = None
        self._Subtitler__chatPages = []
        self._Subtitler__optionButtons = []
        self.specialButtonImage = None
        self.clearTextOverride = False

    
    def destroy(self):
        self.ignoreAll()
        if self.fader:
            self.fader.finish()
            self.fader = None
        
        if self.sfx:
            self.sfx.stop()
            self.sfx = None
        
        self.text.destroy()
        del self.text
        self.confirmButton.destroy()
        del self.confirmButton
        self.EscText.destroy()
        del self.EscText
        self.subtitleParent.removeNode()
        self._Subtitler__destroyOptionButtons()
        taskMgr.remove('clearSubtitleTask')

    
    def clearText(self, resetOverride = False):
        if resetOverride:
            self.clearTextOverride = False
        
        if self.clearTextOverride:
            return None
        
        taskMgr.remove('clearSubtitleTask')
        self.event = None
        self.text['text'] = ''
        self.text['text_fg'] = PiratesGuiGlobals.TextFG2
        self.text.hide()
        self.confirmButton.hide()
        if self.sfx:
            self.sfx.stop()
            self.sfx = None
        
        self.ignore('enter')
        self.ignore('mouse1')
        self.ignore('letterboxOff')
        self._Subtitler__clearChatMessage()
        self._Subtitler__destroyOptionButtons()
        self._Subtitler__optionButtons = []

    
    def _Subtitler__processChatMessage(self, message):
        self._Subtitler__chatPages = message.split('\x7')
        self._Subtitler__chatMessage = message
        self._Subtitler__chatSet = 0
        self._Subtitler__chatPageNumber = 0

    
    def _Subtitler__clearChatMessage(self):
        self._Subtitler__chatPageNumber = None
        self._Subtitler__chatPages = None
        self._Subtitler__chatMessage = None
        self._Subtitler__chatPages = []

    
    def setPageChat(self, message, timeout = False, confirm = False, options = None, callback = None, extraArgs = []):
        if options != None:
            self._Subtitler__loadOptionButtons(options, callback, extraArgs)
        
        self._Subtitler__processChatMessage(message)
        self._Subtitler__updatePageChat(timeout, confirm)

    
    def _Subtitler__loadOptionButtons(self, options, callback, extraArgs):
        
        def optionCallback(*args):
            self.advancePageNumber()
            callback(*args)

        for i in xrange(len(options)):
            optionButton = GuiButton(parent = base.a2dBottomRight, pos = (-0.14999999999999999 - (len(options) - 1 - i) * 0.25, 0, 0.095000000000000001), text = str(options[i]), text_pos = (0, -0.012500000000000001), text_scale = 0.050000000000000003, text_fg = PiratesGuiGlobals.TextFG2, textMayChange = 1, command = optionCallback, extraArgs = [
                options[i]] + extraArgs, sortOrder = 90)
            if self.specialButtonImage:
                optionButton['image'] = self.specialButtonImage
                optionButton['image_scale'] = (0.59999999999999998, 0.59999999999999998, 0.59999999999999998)
            
            optionButton.hide()
            self._Subtitler__optionButtons.append(optionButton)
        

    
    def _Subtitler__destroyOptionButtons(self):
        for optionButton in self._Subtitler__optionButtons:
            optionButton.destroy()
            del optionButton
        
        self._Subtitler__optionButtons = None

    
    def _Subtitler__updatePageChat(self, timeout = False, confirm = False):
        if self._Subtitler__chatPageNumber >= 0:
            message = self._Subtitler__chatPages[self._Subtitler__chatPageNumber]
            self.showText(message, timeout = timeout, confirm = confirm)
        

    
    def getNumChatPages(self):
        if self._Subtitler__chatPageNumber != None:
            return len(self._Subtitler__chatPages)
        
        return 0

    
    def advancePageNumber(self):
        if self._Subtitler__chatPageNumber != None:
            if self._Subtitler__chatPageNumber >= 0:
                self._Subtitler__chatPageNumber += 1
                if self._Subtitler__chatPageNumber >= len(self._Subtitler__chatPages):
                    self._Subtitler__chatPageNumber = -1
                
                self._Subtitler__updatePageChat()
                if self._Subtitler__chatPageNumber >= 0:
                    messenger.send('nextChatPage', [
                        self._Subtitler__chatPageNumber,
                        0])
                else:
                    messenger.send('doneChatPage', [
                        0])
                    self.confirmCallback()
            
        

    
    def showText(self, text, color = None, sfx = None, timeout = 0, confirm = False):
        taskMgr.remove('clearSubtitleTask')
        self.text['text'] = text
        self.text.show()
        self.accept('letterboxOff', self.clearText)
        if self.getNumChatPages() > 1 and self._Subtitler__optionButtons or confirm:
            self.confirmButton.show()
            if self._Subtitler__chatPageNumber == len(self._Subtitler__chatPages) - 1:
                messenger.send('lastSubtitlePage')
                if self._Subtitler__optionButtons:
                    for optionButton in self._Subtitler__optionButtons:
                        optionButton.show()
                    
                    self.confirmButton.hide()
                else:
                    self.confirmButton['text'] = PLocalizer.GenericConfirmOK
            else:
                self.confirmButton['text'] = PLocalizer.GenericConfirmNext
        else:
            self.confirmButton.hide()
        self.event = None
        if color:
            self.text['text_fg'] = color
        
        if sfx:
            if self.sfx:
                self.sfx.stop()
            
            self.sfx = sfx
            base.playSfx(sfx)
        
        if timeout:
            taskMgr.doMethodLater(timeout, self.clearText, 'clearSubtitleTask', extraArgs = [
                True])
        

    
    def fadeInText(self, text, color = None, sfx = None):
        self.text['text'] = text
        self.text.show()
        self.confirmButton.hide()
        self.event = None
        if sfx:
            if self.sfx:
                self.sfx.stop()
            
            self.sfx = sfx
            base.playSfx(sfx)
        
        if self.fader:
            self.fader.finish()
            self.fader = None
        
        if color:
            self.text['text_fg'] = color
        
        self.fader = LerpFunctionInterval(self.text.setAlphaScale, fromData = 0, toData = 1, duration = 1.0)
        self.fader.start()

    
    def fadeOutText(self):
        self.event = None
        self.confirmButton.hide()
        if self.sfx:
            self.sfx.stop()
            self.sfx = None
        
        self.ignore('enter')
        self.ignore('mouse1')
        if self.fader:
            self.fader.finish()
            self.fader = None
        
        fadeOut = LerpFunctionInterval(self.text.setAlphaScale, fromData = 1, toData = 0, duration = 1.0)
        
        def restoreColor():
            self.text['text_fg'] = PiratesGuiGlobals.TextFG2

        
        def resetPos():
            self.text.setPos(Vec3(0.0, 0.0, 0.0))

        self.fader = Sequence(fadeOut, Func(self.text.hide), Func(restoreColor), Func(resetPos))
        self.fader.start()

    
    def confirmText(self, text, event, color = None, sfx = None):
        self.text['text'] = text
        if color:
            self.text['text_fg'] = color
        
        self.text.show()
        self.confirmButton.show()
        self.event = event
        if sfx:
            if self.sfx:
                self.sfx.stop()
            
            self.sfx = sfx
            base.playSfx(sfx)
        
        self.confirmButton['command'] = self.confirmCallback

    
    def confirmCallback(self):
        if self.event:
            messenger.send(self.event)
            self.event = None
        
        self.clearText()
        self.hideEscapeText()
        self.confirmButton['command'] = self.advancePageNumber

    
    def showEscapeText(self, text):
        self.EscText['text'] = text
        self.EscText.show()

    
    def hideEscapeText(self):
        self.EscText['text'] = ''
        self.EscText.hide()


