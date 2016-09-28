# File: P (Python 2.4)

from direct.interval.IntervalGlobal import Sequence, Func
from direct.showbase.ShowBaseGlobal import *
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.showbase import DirectObject
from direct.actor import Actor
from direct.task import Task
from pandac.PandaModules import *
from pandac.PandaModules import CardMaker
from PotionBoardPiece import PotionBoardPiece
from pirates.piratesgui import GuiButton
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PLocalizer
import PotionGlobals

class PotionRecipe(DirectFrame):
    
    def __init__(self, potionGame, potionID, name, desc, ingredientData, level, isFree, questOnly):
        DirectFrame.__init__(self, parent = potionGame.background, relief = None)
        self.potionID = potionID
        self.name = name
        self.desc = desc
        self.potionGame = potionGame
        self.complete = False
        self.isFree = isFree
        self.level = level
        self.questOnly = questOnly
        self.available = False
        self.enabled = False
        self.haveMade = False
        self.ingredientData = ingredientData
        self.ingredients = []
        self.title = None
        self.subtitle1 = None
        self.subtitle2 = None
        self.subtitle3 = None
        self.ingredientCount = None
        self.ingredientLabel = None
        self.tileCount = None
        self.tileLabel = None
        self.soulCount = None
        self.soulLabel = None
        self.ingredientsMade = 0
        self.tilesUsed = 0
        self.soulsCleared = 0
        self._initGUI()

    
    def __cmp__(self, other):
        if other is None:
            return None
        
        if other.level != self.level:
            return cmp(self.level, other.level)
        
        return cmp(self.potionID, other.potionID)

    
    def _initGUI(self):
        pass

    
    def showDetails(self, event = None):
        self.unstash()

    
    def hideDetails(self, event = None):
        self.stash()

    
    def madeIngredients(self, count):
        self.ingredientsMade += count
        if self.ingredientCount is not None:
            self.ingredientCount['text'] = str(self.ingredientsMade)
        

    
    def clearedSouls(self, count):
        self.soulsCleared += count
        if self.soulCount is not None:
            self.soulCount['text'] = str(self.soulsCleared)
        

    
    def useTiles(self, count):
        self.tilesUsed += count
        if self.tileCount is not None:
            self.tileCount.stash()
            self.tileCount['text'] = str(self.tilesUsed)
            self.tileCount.unstash()
        

    
    def loadIngredients(self):
        cm = CardMaker('card')
        cm.setFrame(0, 0.80000000000000004, 0, 0.29999999999999999)
        self.background = self.attachNewNode(cm.generate())
        self.background.setTransparency(True)
        self.background.setColor(0.69999999999999996, 0.69999999999999996, 0.69999999999999996, 0)
        self.islandReq = 0
        if len(self.ingredientData) > 0:
            if False:
                self.nameText = PLocalizer.PotionGui['UnknownRecipeName']
                self.descText = PLocalizer.PotionGui['UnknownRecipe']
                if len(self.ingredients) > 0:
                    for ingredient in self.ingredients:
                        if ingredient.colorIndex > -1:
                            ingredient.setColor(-1, -1)
                            continue
                    
                else:
                    for ingredientData in self.ingredientData:
                        ingredient = PotionBoardPiece(self, -1, -1)
                        ingredient.setHiddenInfo(ingredientData['color'], ingredientData['level'])
                        if ingredientData['color'] > 2:
                            self.islandReq = ingredientData['color']
                        
                        ingredient.showName()
                        self.ingredients.append(ingredient)
                    
            else:
                self.nameText = self.name
                self.descText = self.desc
                if len(self.ingredients) > 0:
                    for ingredient in self.ingredients:
                        if ingredient.colorIndex < 0:
                            ingredient.setColor(ingredientData['color'], ingredientData['level'])
                        
                        if ingredient.colorIndex > 2:
                            self.islandReq = ingredient.colorIndex
                            continue
                    
                else:
                    for ingredientData in self.ingredientData:
                        ingredient = PotionBoardPiece(self, ingredientData['color'], ingredientData['level'])
                        if ingredientData['color'] > 2:
                            self.islandReq = ingredientData['color']
                        
                        ingredient.showName()
                        self.ingredients.append(ingredient)
                    
            for ingredient in self.ingredients:
                ingredient.setCompleted(False)
                ingredient.setBoardPos(0, (5.2999999999999998 - self.ingredients.index(ingredient)) * 1.05)
            
        else:
            self.nameText = self.name
            self.descText = self.desc
            if self.ingredientCount is not None:
                self.ingredientCount.removeNode()
            
            self.ingredientCount = DirectLabel(parent = self.background, relief = None, text = str(self.ingredientsMade), text_scale = PiratesGuiGlobals.TextScaleTitleSmall, text_align = TextNode.ARight, text_fg = PotionGlobals.TextColor, text_wordwrap = 30, pos = (0.17000000000000001, 0, 0.94999999999999996), textMayChange = 1)
            if self.ingredientLabel is not None:
                self.ingredientLabel.removeNode()
            
            self.ingredientLabel = DirectLabel(parent = self.background, relief = None, text = PLocalizer.PotionGui['IngredientCount'], text_scale = PiratesGuiGlobals.TextScaleTitleSmall, text_align = TextNode.ALeft, text_fg = PotionGlobals.TextColor, text_wordwrap = 30, pos = (0.25, 0, 0.94999999999999996), textMayChange = 1)
            if self.tileCount is not None:
                self.tileCount.removeNode()
            
            self.tileCount = DirectLabel(parent = self.background, relief = None, text = str(self.tilesUsed), text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ARight, text_fg = PotionGlobals.TextColor, text_wordwrap = 30, pos = (0.17000000000000001, 0, 0.75), textMayChange = 1)
            if self.tileLabel is not None:
                self.tileLabel.removeNode()
            
            self.tileLabel = DirectLabel(parent = self.background, relief = None, text = PLocalizer.PotionGui['TileCount'], text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ALeft, text_fg = PotionGlobals.TextColor, text_wordwrap = 30, pos = (0.25, 0, 0.75), textMayChange = 1)
            if self.soulCount is not None:
                self.soulCount.removeNode()
            
            self.soulCount = DirectLabel(parent = self.background, relief = None, text = str(self.soulsCleared), text_scale = PiratesGuiGlobals.TextScaleExtraLarge, text_align = TextNode.ARight, text_fg = PotionGlobals.TextColor, text_wordwrap = 30, pos = (0.17000000000000001, 0, 0.84999999999999998), textMayChange = 1)
            if self.soulLabel is not None:
                self.soulLabel.removeNode()
            
            self.soulLabel = DirectLabel(parent = self.background, relief = None, text = PLocalizer.PotionGui['SoulCount'], text_scale = PiratesGuiGlobals.TextScaleExtraLarge, text_align = TextNode.ALeft, text_fg = PotionGlobals.TextColor, text_wordwrap = 30, pos = (0.25, 0, 0.84999999999999998), textMayChange = 1)
        self.leveltext = PLocalizer.PotionGui['LevelLabel'] + str(self.level)
        if self.islandReq > 0:
            self.islandtext = PLocalizer.PotionGui['IslandName' + str(self.islandReq)]
        else:
            self.islandtext = PLocalizer.PotionGui['IslandName']
        if not self.enabled:
            self.levelColor = PiratesGuiGlobals.TextOV6
        elif not self.available:
            self.levelColor = PotionGlobals.TextColorDisabled
        else:
            self.levelColor = PotionGlobals.TextColor
        if not self.available:
            self.islandColor = PiratesGuiGlobals.TextOV6
        elif not self.enabled:
            self.islandColor = PotionGlobals.TextColorDisabled
        else:
            self.islandColor = PotionGlobals.TextColor
        if self.available and self.enabled:
            self.titleColor = PotionGlobals.TextColor
        else:
            self.titleColor = PotionGlobals.TextColorDisabled
        if self.title is not None:
            self.title.removeNode()
        
        self.title = DirectLabel(parent = self.background, relief = None, text = self.nameText, text_scale = PiratesGuiGlobals.TextScaleTitleSmall, text_align = TextNode.ACenter, text_fg = self.titleColor, text_wordwrap = 30, pos = (0.37, 0, 1.23), textMayChange = 0)
        if self.subtitle1 is not None:
            self.subtitle1.removeNode()
        
        self.subtitle1 = DirectLabel(parent = self.background, relief = None, text = self.leveltext, text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ARight, text_fg = self.levelColor, text_wordwrap = 30, pos = (0.34999999999999998, 0, 1.1799999999999999), textMayChange = 0)
        if self.subtitle2 is not None:
            self.subtitle2.removeNode()
        
        self.subtitle2 = DirectLabel(parent = self.background, relief = None, text = self.islandtext, text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ALeft, text_fg = self.islandColor, text_wordwrap = 30, pos = (0.39000000000000001, 0, 1.1799999999999999), textMayChange = 0)
        if self.subtitle3 is not None:
            self.subtitle3.removeNode()
        
        self.subtitle3 = DirectLabel(parent = self.background, relief = None, text = self.descText, text_scale = PiratesGuiGlobals.TextScaleMed, text_align = TextNode.ACenter, text_fg = self.titleColor, text_wordwrap = 30, pos = (0.37, 0, 1.1299999999999999), textMayChange = 0)
        self.stash()

    
    def reset(self):
        self.complete = False
        for ingredient in self.ingredients:
            ingredient.setCompleted(False)
        
        self.ingredientsMade = 0
        self.tilesUsed = 0
        self.soulsCleared = 0
        self.stash()

    
    def destroy(self):
        DirectFrame.destroy(self)
        for ingredient in self.ingredients:
            ingredient.destroy()
        
        del self.ingredients
        del self.potionGame


