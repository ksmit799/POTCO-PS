# File: P (Python 2.4)

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals
from pirates.piratesgui import PDialog
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.band import BandConstance
from pirates.piratesgui.RequestButton import RequestButton

class PiratesInfoButton(RequestButton):
    
    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(PiratesInfoButton)



class PiratesInfo(GuiPanel.GuiPanel):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesInfo')
    
    def __init__(self, title, messageList):
        GuiPanel.GuiPanel.__init__(self, title, 0.80000000000000004, 0.80000000000000004)
        self.initialiseoptions(PiratesInfo)
        self.messageList = messageList
        self.currentMessage = 0
        text = ' '
        base.me = self
        self.message = DirectLabel(parent = self, relief = None, text = self.messageList[self.currentMessage], text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ALeft, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 17, pos = (0.066699999999999995, 0, 0.59999999999999998), textMayChange = 1)
        self.bOk = PiratesInfoButton(text = PLocalizer.GenericConfirmOK, command = self._PiratesInfo__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.34999999999999998, 0, 0.050000000000000003)
        self.nextMessage()
        self.accept('clientLogout', self.destroy)

    
    def nextMessage(self):
        self.message['text'] = self.messageList[self.currentMessage]
        self.currentMessage += 1
        if self.currentMessage == len(self.messageList):
            self.bOk['text'] = PLocalizer.GenericConfirmDone
        else:
            self.bOk['text'] = PLocalizer.GenericConfirmNext

    
    def destroy(self):
        if hasattr(self, 'destroyed'):
            return None
        
        self.destroyed = 1
        self.ignore('Esc')
        GuiPanel.GuiPanel.destroy(self)

    
    def _PiratesInfo__handleOk(self):
        if self.currentMessage == len(self.messageList):
            self.destroy()
        else:
            self.nextMessage()

    
    def _PiratesInfo__handleCancelFromAbove(self):
        self.destroy()


