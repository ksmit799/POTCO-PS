# File: C (Python 2.4)

from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.piratesgui.CannonDefenseHelpPanel import CannonDefenseHelpPanel
from pirates.piratesbase import PLocalizer

class CannonDefenseHelpManager:
    
    def __init__(self, fadeLength):
        self.ammo = None
        self.mine = None
        self.ammoPanel = None
        self.wave = None
        self.exit = None
        self.help = None
        self._CannonDefenseHelpManager__createPanels()
        self._CannonDefenseHelpManager__createIntervals(fadeLength)

    
    def _CannonDefenseHelpManager__createPanels(self):
        self.ammo = CannonDefenseHelpPanel(PLocalizer.CannonDefenseHelp['AmmoHeader'], PLocalizer.CannonDefenseHelp['AmmoBody'], 13, 0.60999999999999999, 0.55000000000000004)
        self.ammo.setPos(-0.10000000000000001, 0, 1)
        self.ammo.arrow.setHpr(0, 0, 90)
        self.ammo.arrow.setPos(0.10000000000000001, 0, -0.111)
        self.mine = CannonDefenseHelpPanel(PLocalizer.CannonDefenseHelp['MineHeader'], PLocalizer.CannonDefenseHelp['MineBody'], 12, 0.54000000000000004, 0.20000000000000001)
        self.mine.setPos(0.31, 0, -0.25)
        self.mine.arrow.setHpr(0, 0, -90)
        self.mine.arrow.setPos(0.040000000000000001, 0, 0.311)
        self.ammoPanel = CannonDefenseHelpPanel(PLocalizer.CannonDefenseHelp['AmmoPanelHeader'], PLocalizer.CannonDefenseHelp['AmmoPanelBody'], 9, 0.45000000000000001, 0.51000000000000001)
        self.ammoPanel.setPos(0.20000000000000001, 0, 0.059999999999999998)
        self.ammoPanel.arrow.setHpr(0, 0, -180)
        self.ammoPanel.arrow.setPos(-0.127, 0, 0.25)
        self.wave = CannonDefenseHelpPanel(PLocalizer.CannonDefenseHelp['WaveHeader'], PLocalizer.CannonDefenseHelp['WaveBody'], 13, 0.59999999999999998, 0.25)
        self.wave.setPos(-1.55, -0.20999999999999999, -0.29999999999999999)
        self.wave.arrow.setPos(0.70999999999999996, 0, 0.19)
        self.exit = CannonDefenseHelpPanel(PLocalizer.CannonDefenseHelp['ExitHeader'], None, 0, 0.44, 0.080000000000000002)
        self.exit.setPos(-0.45000000000000001, 0, 0.45000000000000001)
        self.exit.arrow.setScale(0.59999999999999998, 1.0, 0.59999999999999998)
        self.exit.arrow.setHpr(0, 0, 90)
        self.exit.arrow.setPos(0.23000000000000001, 0, -0.065000000000000002)
        self.help = CannonDefenseHelpPanel(PLocalizer.CannonDefenseHelp['HelpHeader'], None, 0, 0.51000000000000001, 0.085000000000000006)
        self.help.setPos(-0.81999999999999995, 0, 0.28000000000000003)
        self.help.arrow.setScale(0.29999999999999999, 1.0, 0.29999999999999999)
        self.help.arrow.setHpr(0, 0, 90)
        self.help.arrow.setPos(0.40999999999999998, 0, -0.029999999999999999)

    
    def destroy(self):
        if self.mine:
            self.mine.removeNode()
            self.mine = None
        
        if self.ammoPanel:
            self.ammoPanel.removeNode()
            self.ammoPanel = None
        
        if self.ammo:
            self.ammo.removeNode()
            self.ammo = None
        
        if self.wave:
            self.wave.removeNode()
            self.wave = None
        
        if self.exit:
            self.exit.removeNode()
            self.exit = None
        
        if self.help:
            self.help.removeNode()
            self.help = None
        

    
    def _CannonDefenseHelpManager__createIntervals(self, length):
        opaque = Vec4(1, 1, 1, 1)
        transparent = Vec4(1, 1, 1, 0)
        self.fadeIn = Parallel(self.ammo.colorScaleInterval(length, opaque, transparent), self.mine.colorScaleInterval(length, opaque, transparent), self.ammoPanel.colorScaleInterval(length, opaque, transparent), self.wave.colorScaleInterval(length, opaque, transparent), self.exit.colorScaleInterval(length, opaque, transparent), self.help.colorScaleInterval(length, opaque, transparent))
        self.fadeOut = Parallel(self.ammo.colorScaleInterval(length, transparent), self.mine.colorScaleInterval(length, transparent), self.ammoPanel.colorScaleInterval(length, transparent), self.wave.colorScaleInterval(length, transparent), self.exit.colorScaleInterval(length, transparent), self.help.colorScaleInterval(length, transparent))


