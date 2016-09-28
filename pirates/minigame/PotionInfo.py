# File: P (Python 2.4)

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui.GuiButton import GuiButton
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from PotionBoardPiece import PotionBoardPiece
import PotionGlobals

class PotionInfo(DirectFrame):
    
    def __init__(self, potionGame):
        self.potionGame = potionGame
        DirectFrame.__init__(self, parent = potionGame.dialogs, relief = None)
        self.setPos((-0.5, 0, 0.074999999999999997))
        guiAssets = loader.loadModel('models/minigames/pir_m_gui_pot_textureCard')
        parch = guiAssets.find('**/pir_t_gui_pot_potionIngredients')
        parch.setScale(3.4500000000000002, 1, 3.4500000000000002)
        parch.setPos(0.5, 0, -0.02)
        self.background = parch.copyTo(self)
        self.bQuit = GuiButton(image = (guiAssets.find('**/pir_t_gui_pot_exitIngredients'), guiAssets.find('**/pir_t_gui_pot_exitIngredientsOn'), guiAssets.find('**/pir_t_gui_pot_exitIngredientsOn'), guiAssets.find('**/pir_t_gui_pot_exitIngredients')), scale = (0.29999999999999999, 0.29999999999999999, 0.29999999999999999), command = self.quit)
        self.bQuit.reparentTo(self)
        self.bQuit.setPos(1.673, 0, 0.76700000000000002)
        self.messageText = PLocalizer.PotionGui['InfoText']
        self.message = DirectLabel(parent = self, relief = None, text = self.messageText, text_scale = PiratesGuiGlobals.TextScaleTitleSmall, text_align = TextNode.ARight, text_fg = PotionGlobals.TextColor, text_shadow = None, pos = (-0.17000000000000001, 0, 0.71999999999999997), textMayChange = 0)
        self.pieces = []
        self.pieceLabels = []
        for color in range(6):
            for level in range(6):
                piece = PotionBoardPiece(self, color, level + 1)
                piece.setPiecePosition(level * 0.112 - 0.27700000000000002, 0.17000000000000001 - color * 0.070900000000000005)
                piece.background.setDepthTest(False)
                piece.background.setDepthWrite(False)
                piece.setScale(0.34999999999999998)
                self.pieces.append(piece)
                piecelabel = DirectLabel(parent = self, relief = None, text = PLocalizer.PotionIngredients[color][level], text_scale = PiratesGuiGlobals.TextScaleMed, text_align = TextNode.ACenter, text_fg = PotionGlobals.TextColor, text_shadow = None, pos = (level * 0.38600000000000001 - 0.45200000000000001, 0, 0.438 - color * 0.245), textMayChange = 0)
                self.message = DirectLabel(parent = self, relief = None, text = PLocalizer.PotionIngredients[color][level], text_scale = PiratesGuiGlobals.TextScaleMed, text_align = TextNode.ACenter, text_fg = PotionGlobals.TextColor, text_shadow = None, pos = (level * 0.38600000000000001 - 0.45200000000000001, 0, 0.438 - color * 0.245), textMayChange = 0)
                self.pieceLabels.append(piecelabel)
            
        
        guiAssets.removeNode()

    
    def destroy(self):
        self.bQuit.destroy()
        DirectFrame.destroy(self)

    
    def show(self):
        if self.potionGame.closeCurrentDialog is not None:
            self.potionGame.closeCurrentDialog()
        
        self.potionGame.closeCurrentDialog = self.cleanUp
        self.potionGame.disableButtons()
        self.unstash()

    
    def toggle(self):
        if self.isStashed():
            self.show()
        else:
            self.quit()

    
    def cleanUp(self):
        self.potionGame.closeCurrentDialog = None
        self.potionGame.enableButtons()
        self.stash()

    
    def quit(self):
        self.cleanUp()
        if self.potionGame.gameFSM.gameStarted:
            self.potionGame.gameFSM.request('Eval')
        else:
            self.potionGame.gameFSM.request('RecipeSelect')


