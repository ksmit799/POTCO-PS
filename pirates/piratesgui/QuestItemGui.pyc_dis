# File: Q (Python 2.4)

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.uberdog import UberDogGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.InventoryItemGui import InventoryItemGui
from pirates.piratesbase import PLocalizer
from GuiButton import GuiButton

class QuestItemGui(InventoryItemGui):
    Width = PiratesGuiGlobals.InventoryPageWidth - PiratesGuiGlobals.GridSize
    Height = 0.20000000000000001
    
    def __init__(self, quest):
        self.loadGui()
        questScroll = self.topGui.find('**/main_gui_quest_scroll')
        data = (UberDogGlobals.InventoryCategory.QUESTS, quest.getDoId())
        self.quest = quest
        InventoryItemGui.__init__(self, data, image = questScroll, image_color = (0.69999999999999996, 0.69999999999999996, 0.69999999999999996, 1))
        self.initialiseoptions(QuestItemGui)
        self.accept(self.quest.getChangeEvent(), self._handleQuestChange)

    
    def destroy(self):
        self.destroyGui()
        DirectFrame.destroy(self)
        del self.quest
        self.ignoreAll()

    
    def createGui(self):
        reward = self.quest.getRewardText()
        if len(reward) > 1:
            if self.quest.isCompleteWithBonus():
                textFg = (0.10000000000000001, 0.80000000000000004, 0.10000000000000001, 1)
                text = PLocalizer.QuestItemGuiCompleteFormat % {
                    'desc': self.quest.getStatusText(),
                    'return': self.quest.getReturnText(),
                    'reward': reward }
            else:
                textFg = PiratesGuiGlobals.TextFG2
                text = PLocalizer.QuestItemGuiIncompleteFormat % {
                    'desc': self.quest.getStatusText(),
                    'reward': reward }
        elif self.quest.isCompleteWithBonus():
            textFg = (0.10000000000000001, 0.80000000000000004, 0.10000000000000001, 1)
            text = PLocalizer.QuestItemGuiCompleteFormatNoReward % {
                'desc': self.quest.getStatusText(),
                'return': self.quest.getReturnText() }
        else:
            textFg = PiratesGuiGlobals.TextFG2
            text = PLocalizer.QuestItemGuiIncompleteFormatNoReward % {
                'desc': self.quest.getStatusText() }
        self.descText = DirectLabel(parent = self, relief = None, text = text, text_align = TextNode.ALeft, text_scale = PiratesGuiGlobals.TextScaleLarge, text_fg = textFg, text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 1, pos = (-0.10000000000000001, 0, 0.10000000000000001))
        bWidth = 0.20000000000000001
        bHeight = 0.050000000000000003
        bBorder = 0.0050000000000000001
        if self.quest.isDroppable():
            self.dropButton = GuiButton(parent = self, text = PLocalizer.Drop, pos = (0.80000000000000004, 0, -0.02), command = self._dropQuest)
        else:
            self.dropButton = None
        self.shareButton = None

    
    def destroyGui(self):
        self.descText.destroy()
        del self.descText
        if self.dropButton:
            self.dropButton.destroy()
            del self.dropButton
        
        if self.shareButton:
            self.shareButton.destroy()
            del self.shareButton
        

    
    def _handleQuestChange(self):
        self.destroyGui()
        self.createGui()

    
    def _dropQuest(self):
        self.dropButton.hide()
        localAvatar.requestDropQuest(self.quest.getQuestId())

    
    def _shareQuest(self):
        localAvatar.requestShareQuest(self.quest.getQuestId())


