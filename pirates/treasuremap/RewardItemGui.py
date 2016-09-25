# File: R (Python 2.4)

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals

class RewardItemGui(DirectFrame):
    Width = PiratesGuiGlobals.TMCompletePanelWidth - PiratesGuiGlobals.GridSize
    Height = PiratesGuiGlobals.TMCompletePageHeight / 7
    
    def __init__(self, item, parent = None, textScale = None, itemHeight = None, **kw):
        if itemHeight == None:
            itemHeight = RewardItemGui.Height
        
        optiondefs = (('state', DGG.NORMAL, None), ('frameColor', (0.10000000000000001, 0.10000000000000001, 1, 0.080000000000000002), None), ('borderWidth', PiratesGuiGlobals.BorderWidth, None), ('frameSize', (0.0, RewardItemGui.Width, 0.0, itemHeight), None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent)
        self.initialiseoptions(RewardItemGui)
        self.textScale = 0.059999999999999998
        if textScale:
            self.textScale = textScale
        
        self.item = item

    
    def setup(self):
        self._createIface()

    
    def destroy(self):
        self._destroyIface()
        DirectFrame.destroy(self)
        self.ignoreAll()

    
    def _createIface(self):
        textFg = PiratesGuiGlobals.TextFG1
        self.descText = DirectLabel(parent = self, relief = None, text = self.item[0], text_align = TextNode.ALeft, text_scale = self.textScale, text_fg = textFg, text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 1, pos = (0.59999999999999998, 0, self.getHeight() / 2))
        self.valueText = DirectLabel(parent = self, relief = None, text = str(self.item[1]), text_align = TextNode.ARight, text_scale = self.textScale, text_fg = textFg, text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 1, pos = (1.8, 0, self.getHeight() / 2))

    
    def _destroyIface(self):
        self.descText.destroy()
        del self.descText
        self.valueText.destroy()
        del self.valueText

    
    def _handleItemChange(self):
        self._destroyIface()
        self._createIface()


