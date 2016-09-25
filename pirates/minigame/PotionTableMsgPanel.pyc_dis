# File: P (Python 2.4)

from pirates.piratesgui.GuiPanel import *
from pirates.piratesgui.RequestButton import RequestButton
from pirates.piratesbase import PLocalizer

class PotionTableMsgPanel(GuiPanel):
    
    def __init__(self):
        GuiPanel.__init__(self, 'Training needed', 1, 0.40000000000000002, showClose = False, titleSize = 1.5)
        self.setPos((-0.5, 0, 0))
        self.bQuit = RequestButton(text = 'OK', command = self.quit)
        self.bQuit.reparentTo(self)
        self.bQuit.setPos(0.45000000000000001, 0, 0.050000000000000003)
        self.message = None

    
    def show(self):
        if self.message is not None:
            self.message.removeNode()
        
        self.messageText = 'Please visit the gypsy before crafting potions.'
        self.message = DirectLabel(parent = self, relief = None, text = self.messageText, text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 17, pos = (0.5, 0, 0.20000000000000001), textMayChange = 0)
        self.unstash()
        localAvatar.motionFSM.off()

    
    def quit(self):
        localAvatar.motionFSM.on()
        self.stash()


