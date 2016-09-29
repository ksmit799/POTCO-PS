# File: P (Python 2.4)

from pirates.piratesgui.GuiPanel import *
from pirates.piratesgui.RequestButton import RequestButton
from pirates.piratesbase import PLocalizer

class PotionInstructionPanel(GuiPanel):
    
    def __init__(self):
        GuiPanel.__init__(self, PLocalizer.GypsyPotionCraftingTitle, 1, 0.40000000000000002, showClose = False, titleSize = 1.5)
        self.setPos((-0.5, 0, 0))
        self.bQuit = RequestButton(text = PLocalizer.GypsyPotionCraftingClose, command = self.quit)
        self.bQuit.reparentTo(self)
        self.bQuit.setPos(0.45000000000000001, 0, 0.029999999999999999)
        self.message = None
        self.callBack = None

    
    def show(self, onInstructionsComplete):
        if self.message is not None:
            self.message.removeNode()
        
        self.callBack = onInstructionsComplete
        self.messageText = PLocalizer.GypsyPotionCraftingMessage
        self.message = DirectLabel(parent = self, relief = None, text = self.messageText, text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 22, pos = (0.5, 0, 0.27000000000000002), textMayChange = 0)
        self.unstash()
        localAvatar.motionFSM.off()

    
    def quit(self):
        localAvatar.motionFSM.on()
        self.stash()
        if self.callBack is not None:
            self.callBack()
        


