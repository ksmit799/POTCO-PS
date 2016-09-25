# File: C (Python 2.4)

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui.CannonDefenseScorePanelBase import CannonDefenseScorePanelBase
from pirates.piratesgui.CannonDefenseScorePanelBase import RoundCompleteFlags
from pirates.piratesgui.GuiButton import GuiButton
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer

class CannonDefenseEndOfWavePanel(CannonDefenseScorePanelBase):
    
    def __init__(self, waveNumber, roundComplete, panelNumber, numOfPanels, **kw):
        CannonDefenseScorePanelBase.__init__(self, panelNumber, numOfPanels, **None)
        self.lblCountDown = None
        self.lblTreasureStolen = None
        self.lblTreasureLeft = None
        self.roundComplete = roundComplete
        self.waveNumber = waveNumber
        self._createPanel()

    
    def _createPanel(self):
        startX = 0.77000000000000002
        widthX = 0.39000000000000001
        self._createHeader(self, self.waveNumber, self.roundComplete)
        self._createTreasureLabels(self, 1.2150000000000001)
        self._createWaveResultsLabel(self, 0.96999999999999997)
        self._createPlayerNames(self, self.playerLbls, startX, 0.96999999999999997, widthX)
        self._createStatsLabels(self, PLocalizer.CannonDefense['ShipsSunkWave'], self.shipsSunkTotalslbl, startX, 0.81999999999999995, widthX)
        self._createStatsLabels(self, PLocalizer.CannonDefense['DamageDealtWave'], self.damageTotalslbl, startX, 0.71999999999999997, widthX)
        self._createStatsLabels(self, PLocalizer.CannonDefense['AccuracyWave'], self.accuracyTotalslbl, startX, 0.62, widthX)
        self._createStatsLabels(self, PLocalizer.CannonDefense['ShotsFiredWave'], self.shotsFiredTotalslbl, startX, 0.52000000000000002, widthX)
        self._createGoldAwardedLabel(self, 0.22)
        self._createFooter(self)

    
    def _createHeader(self, myParent, waveNumber, roundComplete):
        textColor = PiratesGuiGlobals.TextFG1
        if roundComplete == RoundCompleteFlags.GAME_DEFEAT:
            waveCompleteTxt = PLocalizer.CannonDefense['GameOver']
            textColor = PiratesGuiGlobals.TextOV6
        else:
            waveCompleteTxt = PLocalizer.CannonDefense['WaveComplete'] % waveNumber
            if roundComplete == RoundCompleteFlags.GAME_VICTORY:
                textColor = PiratesGuiGlobals.TextFG25
            
        headingTxtScale = PiratesGuiGlobals.TextScaleLarge * 4
        DirectLabel(parent = myParent, relief = None, state = DGG.DISABLED, text = waveCompleteTxt, text_scale = headingTxtScale, text_align = TextNode.ACenter, text_fg = textColor, text_shadow = PiratesGuiGlobals.TextShadow, text_pos = (0, 0, 0), text_font = self.headingfont, textMayChange = 0, pos = (1.2, 0, 1.3500000000000001))

    
    def _createFooter(self, myParent):
        txtScale = PiratesGuiGlobals.TextScaleLarge * 1.5
        if self.roundComplete == RoundCompleteFlags.WAVE_COMPLETE:
            nextWaveTxt = PLocalizer.CannonDefense['NextWave'] % '?'
            self.lblCountDown = DirectLabel(parent = myParent, relief = None, state = DGG.DISABLED, text = nextWaveTxt, text_scale = txtScale, text_align = TextNode.ARight, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_pos = (0, 0, 0), text_font = self.bodyfont, textMayChange = 1, pos = (2.25, 0, -0.059999999999999998))
            self.lblCountDown.hide()
        else:
            DirectLabel(parent = myParent, relief = None, state = DGG.DISABLED, text = '%s/%s' % (self.panelNumber, self.numOfPanels), text_scale = txtScale, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_pos = (0, 0, 0), text_font = self.bodyfont, textMayChange = 0, pos = (2.1000000000000001, 0, 0.029999999999999999))
            self.nextButton = GuiButton(parent = self, pos = (2.1000000000000001, 0, -0.050000000000000003), text = PLocalizer.CannonDefense['Next'])

    
    def _createTreasureLabels(self, myParent, startY):
        txtScale = PiratesGuiGlobals.TextScaleLarge * 1.45
        self.lblTreasureStolen = DirectLabel(parent = myParent, relief = None, state = DGG.DISABLED, text = '', text_scale = txtScale, text_align = TextNode.ALeft, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_pos = (0, 0, 0), text_font = self.headingfont, textMayChange = 1, pos = (0.29999999999999999, 0, startY))
        self.lblTreasureLeft = DirectLabel(parent = myParent, relief = None, state = DGG.DISABLED, text = '', text_scale = txtScale, text_align = TextNode.ARight, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_pos = (0, 0, 0), text_font = self.bodyfont, textMayChange = 1, pos = (2.1000000000000001, 0, startY))

    
    def _createWaveResultsLabel(self, myParent, startY):
        DirectLabel(parent = myParent, relief = None, state = DGG.DISABLED, text = PLocalizer.CannonDefense['WaveResults'], text_scale = PiratesGuiGlobals.TextScaleLarge * 1.5, text_align = TextNode.ALeft, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_pos = (0, 0, 0), text_font = self.headingfont, textMayChange = 1, pos = (0.22, 0, startY))

    
    def _createGoldAwardedLabel(self, myParent, startY):
        txtScale = PiratesGuiGlobals.TextScaleLarge * 1.5
        self.lblGoldAwarded = DirectLabel(parent = myParent, relief = None, state = DGG.DISABLED, text = '', text_scale = txtScale, text_align = TextNode.ARight, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_pos = (0, 0, 0), text_font = self.headingfont, textMayChange = 1, pos = (2.1899999999999999, 0, startY - 0.074999999999999997))
        self.lblTreasureEarned = DirectLabel(parent = myParent, relief = None, state = DGG.DISABLED, text = '', text_scale = txtScale, text_align = TextNode.ARight, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_pos = (0, 0, 0), text_font = self.headingfont, textMayChange = 1, pos = (2.1899999999999999, 0, startY))
        self.lblTreasureEarned.hide()

    
    def setGoldAwarded(self, gold, goldBonus = 0):
        if goldBonus:
            self.lblGoldAwarded['text'] = PLocalizer.CannonDefense['PayShareBonus'] % (str(gold), str(goldBonus))
        else:
            self.lblGoldAwarded['text'] = PLocalizer.CannonDefense['PayShare'] % str(gold)

    
    def setTreasureAwarded(self, amount):
        if amount == 0:
            return None
        
        self.lblTreasureEarned['text'] = PLocalizer.CannonDefense['TreasureEarned'] % amount
        self.lblTreasureEarned.show()

    
    def updateCountDown(self, timeLeft):
        self.lblCountDown['text'] = PLocalizer.CannonDefense['NextWave'] % timeLeft
        if self.lblCountDown.isHidden():
            self.lblCountDown.show()
        

    
    def setTreasureStats(self, treasureStolen, treasureRemaining):
        self.lblTreasureStolen['text'] = '%s %s %s' % (PLocalizer.CannonDefense['TreasureStolen'], treasureStolen, PLocalizer.CannonDefense['Treasure'])
        self.lblTreasureLeft['text'] = '%s %s %s' % (PLocalizer.CannonDefense['TreasureRemaining'], treasureRemaining, PLocalizer.CannonDefense['Treasure'])


