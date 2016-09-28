# File: S (Python 2.4)

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from pirates.piratesgui import InventoryPage
from pirates.reputation import ReputationGlobals
from pirates.uberdog.UberDogGlobals import InventoryCategory, InventoryType, InventoryId
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import RadialMenu
from pirates.piratesgui.ReputationMeter import ReputationMeter
from pirates.piratesgui import SkillpageGuiButton
from pirates.piratesgui import PiratesGuiGlobals
from pirates.battle import WeaponGlobals
from pirates.piratesbase import Freebooter
from pirates.piratesgui.SkillButton import SkillButton
from pirates.piratesgui import PDialog
from otp.otpgui import OTPDialog
from pirates.inventory import ItemGlobals
MAX_REP = 6

class SkillPage(InventoryPage.InventoryPage):
    MAX_UPGRADE_DOTS = 5
    EXCLUDED_SKILLS = [
        InventoryType.CannonGrappleHook]
    notify = DirectNotifyGlobal.directNotify.newCategory('SkillPage')
    SkillIcons = None
    WeaponIcons = None
    TopGui = None
    DotTex = None
    FrameTex = None
    
    def __init__(self):
        if not SkillPage.SkillIcons:
            SkillPage.SkillIcons = loader.loadModel('models/textureCards/skillIcons')
            SkillPage.WeaponIcons = loader.loadModel('models/gui/gui_icons_weapon')
            SkillPage.DotTex = SkillPage.SkillIcons.find('**/skill_tree_level_dot')
            SkillPage.FrameTex = SkillPage.SkillIcons.find('**/skill_tree_level_ring')
        
        InventoryPage.InventoryPage.__init__(self)
        self.initialiseoptions(SkillPage)
        self.tabBar = None
        self.currentRep = InventoryType.CannonRep
        self.skillFrames = { }
        self.boostDisplays = { }
        self.backFrames = { }
        self.lastUserSelectedTab = None
        self.dataChanged = True
        self.spentDialog = None
        self.localMods = { }
        self.demo = False
        self.demoSeq = None
        self.blinkSeqs = []
        self.blinkSeqs2 = []
        ornament = loader.loadModel('models/gui/gui_skill_window')
        ornament.find('**/pPlane81').detachNode()
        ornament.find('**/pPlane83').detachNode()
        ornament.find('**/pPlane84').detachNode()
        ornament.find('**/pPlane93').detachNode()
        ornament.setScale(0.32500000000000001, 0, 0.32000000000000001)
        ornament.setPos(0.54000000000000004, 0, 0.71999999999999997)
        ornament.flattenStrong()
        ornament.reparentTo(self)
        self.box = loader.loadModel('models/gui/gui_title_box').find('**/gui_title_box_top')
        box = loader.loadModel('models/gui/gui_title_box').find('**/gui_title_box_top')
        box.setPos(0.55000000000000004, 0, 1.26)
        box.setScale(0.32500000000000001, 0.0, 0.25)
        box.reparentTo(ornament)
        ornament.flattenStrong()
        self.repMeter = ReputationMeter(self.getRep(), width = 0.69999999999999996)
        self.repMeter.reparentTo(self)
        self.repMeter.setPos(0.55000000000000004, 0, 1.24)
        self.unspent = DirectLabel(parent = self, relief = None, text = PLocalizer.SkillPageUnspentPoints % 0, text_scale = 0.040000000000000001, text_align = TextNode.ACenter, text_pos = (0, -0.01), text_fg = (1, 1, 1, 1), pos = (0.80000000000000004, 0, 0.02))

    
    def destroy(self):
        for spot in self.skillFrames.keys():
            self.skillFrames[spot].destroy()
        
        if self.tabBar:
            self.tabBar.destroy()
            self.tabBar = None
        
        self._SkillPage__handleFreeDialog()
        InventoryPage.InventoryPage.destroy(self)
        if self.demoSeq:
            self.demoSeq.pause()
            self.demoSeq = None
        
        for blinkSeq in self.blinkSeqs:
            blinkSeq.pause()
            blinkSeq = None
        
        self.blinkSeqs = []
        for blinkSeq in self.blinkSeqs2:
            blinkSeq.pause()
            blinkSeq = None
        
      