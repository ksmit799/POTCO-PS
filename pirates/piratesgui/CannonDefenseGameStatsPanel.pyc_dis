# File: C (Python 2.4)

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui.CannonDefenseScorePanelBase import CannonDefenseScorePanelBase
from pirates.piratesgui.CannonDefenseScorePanelBase import RoundCompleteFlags
from pirates.piratesgui.GuiButton import GuiButton
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
import math

class CannonDefenseGameStatsPanel(CannonDefenseScorePanelBase):
    
    def __init__(self, roundComplete, panelNumber, numOfPanels, **kw):
        CannonDefenseScorePanelBase.__init__(self, panelNumber, numOfPanels, **None)
        self.prevButton = None
        self.nextButton = None
        self.timePlayedTotalslbl = []
        self.goldEarnedTotalslbl = []
        self.roundComplete = roundComplete
        self._createPanel()

    
    def _createPanel(self):
        startX = 0.77000000000000002
        widthX = 0.39000000000000001
        self._createHeader(self)
        self._createPlayerNames(self, self.playerLbls, startX, 0.96999999999999997, widthX)
        self._createStatsLabels(self, PLocalizer.CannonDefense['TimePlayed'], self.timePlayedTotalslbl, startX, 0.81999999999999995, widthX)
        self._createStatsLabels(self, PLocalizer.CannonDefense['ShipsSunkWave'], self.shipsSunkTotalslbl, startX, 0.71999999999999997, widthX)
        self._createStatsLabels(self, PLocalizer.CannonDefense['DamageDealtWave'], self.damageTotalslbl, startX, 0.62, widthX)
        self._createStatsLabels(self, PLocalizer.CannonDefense['AccuracyWave'], self.accuracyTotalslbl, startX, 0.52000000000000002, widthX)
        self._createStatsLabels(self, PLocalizer.CannonDefense['ShotsFiredWave'], self.shotsFiredTotalslbl, startX, 0.41999999999999998, widthX)
        self._createStatsLabels(self, PLocalizer.CannonDefense['GoldEarned'], self.goldEarnedTotalslbl, startX, 0.32000000000000001, widthX)
        self._createFooter(self)

    
    def _createHeader(self, myParent):
        headingTxtScale = PiratesGuiGlobals.TextScaleLarge * 3
        DirectLabel(parent = myParent, relief = None, state = DGG.DISABLED, text = PLocalizer.CannonDefense['Report'], text_scale = headingTxtScale, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_pos = (0, 0, 0), text_font = self.headingfont, textMayChange = 0, pos = (1.2, 0, 1.3700000000000001))

    
    def _createFooter(self, myParent):
        doWhatNextTxt = None
        txtScale = PiratesGuiGlobals.TextScaleLarge * 1.5
        DirectLabel(parent = myParent, relief = None, state = DGG.DISABLED, text = '%s/%s' % (self.panelNumber, self.numOfPanels), text_scale = txtScale, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_pos = (0, 0, 0), text_font = self.bodyfont, textMayChange = 0, pos = (2.1000000000000001, 0, 0.029999999999999999))
        self.prevButton = GuiButton(parent = self, pos = (1.8500000000000001, 0, -0.050000000000000003), text = PLocalizer.CannonDefense['Previous'])
        if self.roundComplete == RoundCompleteFlags.GAME_DEFEAT:
            doWhatNextTxt = PLocalizer.CannonDefense['Exit']
        else:
            doWhatNextTxt = PLocalizer.CannonDefense['Continue']
        self.nextButton = GuiButton(parent = self, pos = (2.1000000000000001, 0, -0.050000000000000003), text = doWhatNextTxt)

    
    def setTimePlayed(self, times, playerIndex):
        for index in range(0, len(times)):
            seconds = times[index]
            if seconds >= 60:
                minutes = int(math.ceil(float(seconds) / 60.0))
                text = '%s %s' % (minutes, PLocalizer.CannonDefense['Minutes'])
            else:
                text = '%s %s' % (seconds, PLocalizer.CannonDefense['Seconds'])
            self.timePlayedTotalslbl[index]['text'] = text
            if index == playerIndex:
                self.timePlayedTotalslbl[index]['text_fg'] = self.highlightPlayerColor
                self.timePlayedTotalslbl[index]['text_font'] = self.headingfont
                self.timePlayedTotalslbl[index]['text_shadow'] = PiratesGuiGlobals.TextShadow
                continue
        

    
    def setGoldEarned(self, goldEarned, playerIndex):
        for index in range(0, len(goldEarned)):
            self.goldEarnedTotalslbl[index]['text'] = str(goldEarned[index])
            if index == playerIndex:
                self.goldEarnedTotalslbl[index]['text_fg'] = self.highlightPlayerColor
                self.goldEarnedTotalslbl[index]['text_font'] = self.headingfont
                self.goldEarnedTotalslbl[index]['text_shadow'] = PiratesGuiGlobals.TextShadow
                continue
        


