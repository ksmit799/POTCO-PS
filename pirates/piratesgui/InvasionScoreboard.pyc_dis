# File: I (Python 2.4)

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import Scoreboard
from pirates.piratesgui import DialogButton
from pirates.piratesgui import GuiButton
from pirates.uberdog.UberDogGlobals import *
from pirates.invasion import InvasionGlobals
from pirates.ai import HolidayGlobals
from pirates.world.LocationConstants import LocationIds
import time

class InvasionScoreboard(DirectFrame):
    width = PiratesGuiGlobals.PortPanelWidth / 2.0
    height = PiratesGuiGlobals.PortPanelHeight * 3.0 / 5.0
    titleHeight = PiratesGuiGlobals.PortTitleHeight
    buffer = 0.050000000000000003
    
    def __init__(self, holidayId, wonInvasion, reputationEarned, enemiesKilled, barricadesSaved, wavesCleared):
        DirectFrame.__init__(self, relief = None, parent = base.aspect2d, image = None, pos = (0.0, 0.0, 0.5))
        self.holidayId = holidayId
        self.wonInvasion = wonInvasion
        self.reputationEarned = reputationEarned
        self.enemiesKilled = enemiesKilled
        self.barricadesSaved = barricadesSaved
        self.wavesCleared = wavesCleared
        self.panel = None
        self.onIsland = False
        if localAvatar.getParentObj() and localAvatar.getParentObj().getUniqueId() == InvasionGlobals.getIslandId(self.holidayId) and localAvatar.getParentObj().minimap:
            self.onIsland = True
        
        self.firePaths = []
        top_gui = loader.loadModel('models/gui/toplevel_gui')
        general_frame_gui = loader.loadModel('models/gui/general_frame')
        main_gui = loader.loadModel('models/gui/gui_main')
        background = general_frame_gui.find('**/middle')
        side_bar = main_gui.find('**/boarder_side')
        top_left = general_frame_gui.find('**/topLeft')
        top_right = general_frame_gui.find('**/topRight')
        bottom_left = general_frame_gui.find('**/bottomLeft')
        bottom_right = general_frame_gui.find('**/bottomRight')
        generic_x = main_gui.find('**/x2')
        generic_box = main_gui.find('**/exit_button')
        generic_box_over = main_gui.find('**/exit_button_over')
        parchment = top_gui.find('**/pir_t_gui_gen_parchment')
        wax_seal = top_gui.find('**/pir_t_gui_gen_waxSeal')
        fires = [
            top_gui.find('**/pir_t_gui_gen_fire0'),
            top_gui.find('**/pir_t_gui_gen_fire1'),
            top_gui.find('**/pir_t_gui_gen_fire2')]
        top_gui.removeNode()
        general_frame_gui.removeNode()
        main_gui.removeNode()
        if self.onIsland:
            topLeftBackground = OnscreenImage(parent = self, image = background, scale = 0.75, pos = (0.75, 0.0, 0.0), color = (0.29999999999999999, 0.29999999999999999, 0.29999999999999999, 1.0))
            topRightBackground = OnscreenImage(parent = self, image = background, scale = 0.75, pos = (1.5, 0.0, 0.0), color = (0.29999999999999999, 0.29999999999999999, 0.29999999999999999, 1.0))
            bottomLeftBackground = OnscreenImage(parent = self, image = background, scale = 0.75, pos = (0.75, 0.0, -0.75), color = (0.29999999999999999, 0.29999999999999999, 0.29999999999999999, 1.0))
            bottomRightBackground = OnscreenImage(parent = self, image = background, scale = 0.75, pos = (1.5, 0.0, -0.75), color = (0.29999999999999999, 0.29999999999999999, 0.29999999999999999, 1.0))
            leftBorder1 = OnscreenImage(parent = self, image = side_bar, scale = 0.25, pos = (-0.26000000000000001, 0.0, -0.53000000000000003))
            leftBorder2 = OnscreenImage(parent = self, image = side_bar, scale = 0.25, pos = (-0.26000000000000001, 0.0, -1.1499999999999999))
            rightBorder1 = OnscreenImage(parent = self, image = side_bar, scale = 0.25, pos = (1.2350000000000001, 0.0, -0.53000000000000003))
            rightBorder2 = OnscreenImage(parent = self, image = side_bar, scale = 0.25, pos = (1.2350000000000001, 0.0, -1.1499999999999999))
            topBorder1 = OnscreenImage(parent = self, image = side_bar, scale = 0.25, pos = (0.53000000000000003, 0.0, -0.26000000000000001), hpr = (0, 0, -90))
            topBorder2 = OnscreenImage(parent = self, image = side_bar, scale = 0.25, pos = (1.1499999999999999, 0.0, -0.26000000000000001), hpr = (0, 0, -90))
            bottomBorder1 = OnscreenImage(parent = self, image = side_bar, scale = 0.25, pos = (0.53000000000000003, 0.0, -1.7649999999999999), hpr = (0, 0, -90))
            bottomBorder2 = OnscreenImage(parent = self, image = side_bar, scale = 0.25, pos = (1.1499999999999999, 0.0, -1.7649999999999999), hpr = (0, 0, -90))
            topLeftCorner = OnscreenImage(parent = self, image = top_left, scale = 1.0, pos = (0.12, 0.0, -0.11))
            topRightCorner = OnscreenImage(parent = self, image = top_right, scale = 1.0, pos = (1.3799999999999999, 0.0, -0.11))
            bottomLeftCorner = OnscreenImage(parent = self, image = bottom_left, scale = 1.0, pos = (0.12, 0.0, -1.3899999999999999))
            bottomRightCorner = OnscreenImage(parent = self, image = bottom_right, scale = 1.0, pos = (1.3799999999999999, 0.0, -1.3899999999999999))
            titlePos = (0.75, 0, -0.080000000000000002)
            resultPos = (0.75, 0, -0.17000000000000001)
            scoreboardPos = (0.20000000000000001, 0, -1.3500000000000001)
            closePos = (1.8100000000000001, 0, -1.21)
        else:
            leftBackground = OnscreenImage(parent = self, image = background, scale = 0.75, pos = (0.75, 0.0, -0.375), color = (0.29999999999999999, 0.29999999999999999, 0.29999999999999999, 1.0))
            rightBackground = OnscreenImage(parent = self, image = background, scale = 0.75, pos = (1.5, 0.0, -0.375), color = (0.29999999999999999, 0.29999999999999999, 0.29999999999999999, 1.0))
            leftBorder = OnscreenImage(parent = self, image = side_bar, scale = 0.25, pos = (-0.26000000000000001, 0.0, -0.83999999999999997))
            rightBorder = OnscreenImage(parent = self, image = side_bar, scale = 0.25, pos = (1.2350000000000001, 0.0, -0.83999999999999997))
            topBorder1 = OnscreenImage(parent = self, image = side_bar, scale = 0.25, pos = (0.53000000000000003, 0.0, -0.63500000000000001), hpr = (0, 0, -90))
            topBorder2 = OnscreenImage(parent = self, image = side_bar, scale = 0.25, pos = (1.1499999999999999, 0.0, -0.63500000000000001), hpr = (0, 0, -90))
            bottomBorder1 = OnscreenImage(parent = self, image = side_bar, scale = 0.25, pos = (0.53000000000000003, 0.0, -1.3899999999999999), hpr = (0, 0, -90))
            bottomBorder2 = OnscreenImage(parent = self, image = side_bar, scale = 0.25, pos = (1.1499999999999999, 0.0, -1.3899999999999999), hpr = (0, 0, -90))
            topLeftCorner = OnscreenImage(parent = self, image = top_left, scale = 1.0, pos = (0.12, 0.0, -0.48499999999999999))
            topRightCorner = OnscreenImage(parent = self, image = top_right, scale = 1.0, pos = (1.3799999999999999, 0.0, -0.48499999999999999))
            bottomLeftCorner = OnscreenImage(parent = self, image = bottom_left, scale = 1.0, pos = (0.12, 0.0, -1.0149999999999999))
            bottomRightCorner = OnscreenImage(parent = self, image = bottom_right, scale = 1.0, pos = (1.3799999999999999, 0.0, -1.0149999999999999))
            titlePos = (0.75, 0, -0.5)
            resultPos = (0.75, 0, -0.58999999999999997)
            scoreboardPos = (0.20000000000000001, 0, -0.90000000000000002)
            closePos = (1.8100000000000001, 0, -1.585)
        titleTxt = PLocalizer.InvasionScoreboardTitle % PLocalizer.LocationNames[InvasionGlobals.getIslandId(self.holidayId)]
        title = DirectLabel(parent = self, relief = None, text = titleTxt, text_align = TextNode.ACenter, text_scale = 0.070000000000000007, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, pos = titlePos, text_font = PiratesGlobals.getPirateOutlineFont())
        if self.wonInvasion:
            resultText = PLocalizer.InvasionWon
        else:
            resultText = PLocalizer.InvasionLost % PLocalizer.getInvasionMainZoneName(HolidayGlobals.getHolidayName(self.holidayId))
        result = DirectLabel(parent = self, relief = None, text = resultText, text_align = TextNode.ACenter, text_scale = PiratesGuiGlobals.TextScaleTitleMed, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, pos = resultPos, text_font = PiratesGlobals.getPirateOutlineFont())
        self.screenNode = None
        self.screenNodeScale = None
        if self.onIsland:
            parchmentImage = OnscreenImage(parent = self, image = parchment, scale = (0.80000000000000004, 0, 0.94999999999999996), pos = (0.75, 0, -0.69999999999999996))
            self.screenNode = localAvatar.getParentObj().minimap.getScreenNode()
        
        if self.screenNode:
            self.screenNode.reparentTo(self)
            screenInfo = InvasionGlobals.getScreenInfo(self.holidayId)
            self.screenNode.setPos(screenInfo[0])
            self.screenNodeScale = self.screenNode.getScale()
            self.screenNode.setScale(screenInfo[1])
            self.screenNode.show()
        
        if self.onIsland:
            if self.wonInvasion:
                waxSealImage = OnscreenImage(parent = self, image = wax_seal, pos = (1.27, 0, -0.94999999999999996), scale = 1.0)
                self.fireSeq = None
            else:
                for fireInfo in InvasionGlobals.getLossFires(self.holidayId):
                    firePath = NodePath(SequenceNode('SeqNode'))
                    for fireCard in fires:
                        firePath.node().addChild(fireCard.node())
                    
                    firePath.node().setFrameRate(10)
                    firePath.node().loop(False)
                    firePath.reparentTo(self)
                    firePath.setPos(fireInfo[0])
                    firePath.setScale(fireInfo[1])
                    self.firePaths.append(firePath)
                
        
        closeButton = GuiButton.GuiButton(parent = self, relief = None, pos = closePos, image = (generic_box, generic_box, generic_box_over, generic_box), image_scale = 0.59999999999999998, command = localAvatar.guiMgr.removeInvasionScoreboard)
        xButton = OnscreenImage(parent = closeButton, image = generic_x, scale = 0.29999999999999999, pos = (-0.38200000000000001, 0, 1.1499999999999999))
        self.createScoreboard(scoreboardPos)

    
    def destroy(self):
        if self.onIsland and localAvatar.getParentObj() and localAvatar.getParentObj().getUniqueId() == InvasionGlobals.getIslandId(self.holidayId) and localAvatar.getParentObj().minimap:
            localAvatar.getParentObj().minimap.handleHolidayEnded(localAvatar.getParentObj(), HolidayGlobals.getHolidayName(self.holidayId), True)
        
        if self.screenNode:
            self.screenNode.reparentTo(localAvatar.guiMgr.minimapRoot)
            self.screenNode.setPos(0, 0, 0)
            self.screenNode.setScale(self.screenNodeScale)
            self.screenNode.hide()
        
        if self.panel:
            self.panel.destroy()
        
        self.panel = None
        for firePath in self.firePaths:
            firePath.removeNode()
            del firePath
        
        self.firePaths = []
        DirectFrame.destroy(self)

    
    def getInvasionResults(self):
        self.results = []
        mainZoneBonus = int(self.reputationEarned * InvasionGlobals.MAIN_ZONE_BONUS)
        enemyBonus = int(self.reputationEarned * InvasionGlobals.ENEMY_BONUS)
        waveBonus = self.wavesCleared * InvasionGlobals.WAVE_BONUS
        barricadeBonus = int(self.reputationEarned * self.barricadesSaved * InvasionGlobals.BARRICADE_BONUS)
        if self.wonInvasion:
            totalBonus = int((mainZoneBonus + enemyBonus + barricadeBonus) * (waveBonus + 1.0))
            self.results.append({
                'Type': 'Entry',
                'Text': PLocalizer.InvasionMainZoneSaved % PLocalizer.getInvasionMainZoneName(HolidayGlobals.getHolidayName(self.holidayId)),
                'Value1': PLocalizer.InvasionNotoriety % mainZoneBonus })
        else:
            totalBonus = int((enemyBonus + barricadeBonus) * (waveBonus + 1.0))
        self.results.append({
            'Type': 'Entry',
            'Text': PLocalizer.InvasionBarricadesSaved % self.barricadesSaved,
            'Value1': PLocalizer.InvasionNotoriety % barricadeBonus })
        if self.enemiesKilled == 1:
            self.results.append({
                'Type': 'Entry',
                'Text': PLocalizer.InvasionEnemyKilled,
                'Value1': PLocalizer.InvasionNotoriety % enemyBonus })
        else:
            self.results.append({
                'Type': 'Entry',
                'Text': PLocalizer.InvasionEnemiesKilled % self.enemiesKilled,
                'Value1': PLocalizer.InvasionNotoriety % enemyBonus })
        self.results.append({
            'Type': 'Entry',
            'Text': PLocalizer.InvasionWavesCleared % self.wavesCleared,
            'Value1': PLocalizer.InvasionNotorietyBonus % int(waveBonus * 100) })
        self.results.append({
            'Type': 'Entry',
            'Text': PLocalizer.InvasionTotalBonus,
            'Value1': PLocalizer.InvasionNotoriety % totalBonus })
        return self.results

    
    def createScoreboard(self, scoreboardPos):
        invasionResults = self.getInvasionResults()
        self.panel = Scoreboard.Scoreboard('', self.width, self.height - 0.71499999999999997, invasionResults, self.titleHeight)
        self.panel.reparentTo(self)
        self.panel.setPos(scoreboardPos)
        for item in self.panel.list.items:
            item.descText['text_font'] = PiratesGlobals.getPirateOutlineFont()
            item.valueText['text_font'] = PiratesGlobals.getPirateOutlineFont()
        
        lenItems = len(self.panel.list.items)
        self.panel.list.items[0].descText.configure(text_fg = PiratesGuiGlobals.TextFG4)
        self.panel.list.items[0].valueText.configure(text_fg = PiratesGuiGlobals.TextFG4)

    
    def closePanel(self):
        GuiPanel.GuiPanel.closePanel(self)
        self.destroy()
        messenger.send('invasionScoreBoardClose')


