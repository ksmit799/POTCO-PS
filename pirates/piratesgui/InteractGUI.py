# File: I (Python 2.4)

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.distributed import InteractGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals

class InteractGUI(DirectFrame):
    
    def __init__(self):
        DirectFrame.__init__(self, relief = None, sortOrder = 3, pos = (-0.5, 0, -0.40000000000000002))
        self.optionButtons = []
        self.initialiseoptions(InteractGUI)

    
    def destroy(self):
        self.destroyOptionButtons()
        DirectFrame.destroy(self)

    
    def destroyOptionButtons(self):
        for optionButton in self.optionButtons:
            optionButton.destroy()
        
        if hasattr(self, 'title'):
            self.title.destroy()
            del self.title
        
        self.optionButtons = []

    
    def setOptions(self, title, optionIds, statusCodes, optionCallback, bribeType):
        z = 1.0
        self.destroyOptionButtons()
        self.title = DirectLabel(parent = self, relief = None, text = title, text_align = TextNode.ACenter, text_scale = 0.070000000000000007, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 1, pos = (0, 0, z - 0.080000000000000002), text_font = PiratesGlobals.getPirateOutlineFont())
        gui = loader.loadModel('models/gui/avatar_chooser_rope')
        topPanel = gui.find('**/avatar_c_A_top')
        topPanelOver = gui.find('**/avatar_c_A_top_over')
        middlePanel = gui.find('**/avatar_c_A_middle')
        middlePanelOver = gui.find('**/avatar_c_A_middle_over')
        bottomPanel = gui.find('**/avatar_c_A_bottom')
        bottomPanelOver = gui.find('**/avatar_c_A_bottom_over')
        for (i, optionId, statusCode) in zip(range(len(optionIds)), optionIds, statusCodes):
            optionName = InteractGlobals.InteractOptionNames.get(optionId, 'Error')
            optionHelp = InteractGlobals.InteractOptionHelpText.get(optionId, 'Error')
            print 'DEBUG: InteractGUI.optionName = %s' % optionName
            if (optionName == 'Bribe') & (bribeType == 1):
                optionName = PLocalizer.InteractBribeAlt
            
            if i == 0:
                image = (topPanel, topPanel, topPanelOver, topPanel)
                textPos = (0, -0.029999999999999999)
                z -= 0.19
            elif i == len(optionIds) - 1:
                image = (bottomPanel, bottomPanel, bottomPanelOver, bottomPanel)
                textPos = (0, 0.033000000000000002)
                if i == 1:
                    z -= 0.16500000000000001
                else:
                    z -= 0.155
            else:
                image = (middlePanel, middlePanel, middlePanelOver, middlePanel)
                textPos = (0, -0.014999999999999999)
                if i == 1:
                    z -= 0.11
                else:
                    z -= 0.105
            if statusCode == InteractGlobals.NORMAL:
                state = DGG.NORMAL
                textFg = PiratesGuiGlobals.TextFG1
                imageColor = (1, 1, 1, 1)
            elif statusCode == InteractGlobals.DISABLED:
                state = DGG.DISABLED
                textFg = (0.29999999999999999, 0.25, 0.20000000000000001, 1)
                imageColor = (0.80000000000000004, 0.80000000000000004, 0.80000000000000004, 1)
            elif statusCode == InteractGlobals.HIGHLIGHT:
                state = DGG.NORMAL
                textFg = PiratesGuiGlobals.TextFG2
                imageColor = (1, 1, 1, 1)
            
            optionButton = DirectButton(parent = self, relief = None, state = state, pressEffect = 0, text = optionName, text_fg = textFg, text_shadow = PiratesGuiGlobals.TextShadow, text_align = TextNode.ACenter, text_scale = 0.050000000000000003, text_pos = textPos, image = image, image_scale = 0.40000000000000002, image_color = imageColor, pos = (0, 0, z), command = optionCallback, extraArgs = [
                optionId])
            self.optionButtons.append(optionButton)
        
        gui.removeNode()


