# File: D (Python 2.4)

from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import *
from otp.otpgui import OTPDialog
from pirates.battle.CannonGUI import CannonGUI
from pirates.battle import CannonGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.PDialog import PDialog
from pirates.piratesgui.ReputationMeter import ReputationMeter
from pirates.battle import CannonGlobals
from pirates.battle import WeaponGlobals
from pirates.reputation import ReputationGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.minigame.CannonDefenseHUD import CannonDefenseHUD
from pirates.piratesgui.CannonDefenseHelpManager import CannonDefenseHelpManager
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
import pirates.minigame.AmmoPanel as pirates
import random
import math

class DefenseCannonGUI(CannonGUI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DefenseCannonGUI')
    
    def __init__(self, cannon):
        CannonGUI.__init__(self, cannon)
        self.exitEvent = None
        self._DefenseCannonGUI__dialog = None
        self.helpButton = None
        self.helpUI = None
        self.flashHelp = None
        self.ammoFade = None
        self._DefenseCannonGUI__ammoCountersHidden = False
        self.setupExtraButtons()
        self.exitCannon['command'] = self.showExitDialog
        self.volleyLabel.setPos(-0.28000000000000003, 0, 0.089999999999999997)
        self.reloadBar.setPos(-0.13, 0, 0.080000000000000002)
        self.ammoImage.setPos(-0.38, 0, 0.059999999999999998)
        self.repMeter = ReputationMeter(InventoryType.DefenseCannonRep, width = 0.69999999999999996)
        self.repMeter.reparentTo(base.a2dBottomCenter)
        self.repMeter.setPos(0.0, 0.0, 0.025000000000000001)
        self.hud = CannonDefenseHUD()
        self.hud.create()
        self._exp = 0
        self.lastLevel = 1
        self.accept('incDefenseCannonExp', self.increaseExp)
        if __dev__:
            base.dcg = self
        

    
    def destroy(self):
        if self.ammoFade:
            self.ammoFade.finish()
            self.ammoFade = None
        
        if self.flashHelp:
            self.flashHelp.finish()
            self.flashHelp = None
        
        if self.helpButton:
            self.helpButton.destroy()
            self.helpButton = None
        
        if self.helpUI:
            self.helpUI.destroy()
            self.helpUI = None
        
        if self.hud:
            self.hud.destroy()
            self.hud = None
        
        base.musicMgr.requestFadeOut(SoundGlobals.MUSIC_MINIGAME_CANNON)
        self.repMeter.destroy()
        self.ignore('incDefenseCannonExp')
        CannonGUI.destroy(self)

    
    def setupExtraButtons(self):
        weaponIcons = loader.loadModel('models/gui/gui_icons_weapon')
        self.helpButton = DirectButton(parent = base.a2dBottomRight, relief = None, pos = (-0.59999999999999998, 0, 0.089999999999999997), scale = 0.5, text = '?', text_pos = (0, -0.055), text_scale = 0.20999999999999999, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_font = PiratesGlobals.getPirateBoldOutlineFont(), sortOrder = 2, command = self.toggleHelpUI)
        DirectLabel(parent = self.helpButton, text = PLocalizer.CannonDefense['Help'], text_pos = (0, -0.14999999999999999), text_scale = 0.080000000000000002, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_font = PiratesGlobals.getPirateBoldOutlineFont(), frameColor = (1, 1, 1, 0))

    
    def increaseExp(self, amt, total):
        self._exp += amt
        if self._exp > total:
            return None
        
        (level, leftoverValue) = ReputationGlobals.getLevelFromTotalReputation(InventoryType.DefenseCannonRep, self._exp)
        self.repMeter.update(self._exp)
        if level > self.lastLevel:
            base.localAvatar.levelUpMsg(InventoryType.DefenseCannonRep, level, 0)
            self.lastLevel = level
        

    
    def toggleHelpUI(self):
        if self.helpUI == None:
            self._DefenseCannonGUI__createHelpUI()
            self.fadeOutAmmoCounters()
            if self.cannon.ammoPanel.state == pirates.minigame.AmmoPanel.CLOSED:
                self.cannon.ammoPanel.onTabClick()
            
        else:
            self._DefenseCannonGUI__destroyHelpUI()
            self.fadeInAmmoCounters()
            if self.cannon.ammoPanel.state == pirates.minigame.AmmoPanel.OPENED:
                self.cannon.ammoPanel.onTabClick()
            

    
    def _DefenseCannonGUI__createHelpUI(self):
        self.helpUI = CannonDefenseHelpManager(0.5)
        self.helpUI.exit.reparentTo(self.exitCannon)
        self.helpUI.exit.setScale(2.0)
        self.helpUI.help.reparentTo(self.helpButton)
        self.helpUI.help.setScale(2.0)
        self.helpUI.ammoPanel.reparentTo(self.cannon.ammoPanel.panel)
        self.helpUI.ammoPanel.setScale(1.0 / 3.0)
        self.helpUI.ammo.reparentTo(base.a2dBottomCenter)
        self.helpUI.mine.reparentTo(self.hud.goldRemainingUI.mineCounter)
        self.helpUI.mine.setScale(2.0 / 3.0)
        self.helpUI.wave.reparentTo(self.hud.timeRemainingUI.timeRemaining)
        self.helpUI.wave.setScale(1.0 / 0.75)
        self.helpUI.fadeIn.start()

    
    def _DefenseCannonGUI__destroyHelpUI(self):
        cleanup = Sequence(Func(self.helpUI.fadeIn.pause), self.helpUI.fadeOut, Func(self.helpUI.destroy), name = self.cannon.uniqueName('HelpUI_FadeIn'))
        cleanup.start()
        self.helpUI = None

    
    def isHelpUIVisible(self):
        return self.helpUI != None

    
    def flashHelpButton(self, delay = 0.20000000000000001, length = 5):
        if self.flashHelp:
            self.flashHelp.finish()
            self.flashHelp = None
        
        self.flashHelp = Sequence(name = self.cannon.uniqueName('HelpButton_Flash'))
        
        def setColor(key, value):
            self.helpButton[key] = value

        for i in range(0, length):
            self.flashHelp.append(Wait(delay))
            self.flashHelp.append(Func(setColor, 'text_fg', PiratesGuiGlobals.TextFG19))
            self.flashHelp.append(Wait(delay))
            self.flashHelp.append(Func(setColor, 'text_fg', PiratesGuiGlobals.TextFG2))
        
        self.flashHelp.start()

    
    def fadeOutAmmoCounters(self, length = 0.5):
        if self._DefenseCannonGUI__ammoCountersHidden:
            return None
        
        transparent = Vec4(1, 1, 1, 0)
        if self.ammoFade:
            self.ammoFade.finish()
        
        self.ammoFade = Parallel(self.volleyLabel.colorScaleInterval(length, transparent), self.reloadBar.colorScaleInterval(length, transparent), self.ammoImage.colorScaleInterval(length, transparent))
        self.ammoFade.start()
        self._DefenseCannonGUI__ammoCountersHidden = True

    
    def fadeInAmmoCounters(self, length = 0.5):
        if self._DefenseCannonGUI__ammoCountersHidden == False:
            return None
        
        opaque = Vec4(1, 1, 1, 1)
        transparent = Vec4(1, 1, 1, 0)
        if self.ammoFade:
            self.ammoFade.finish()
        
        self.ammoFade = Parallel(self.volleyLabel.colorScaleInterval(length, opaque, transparent), self.reloadBar.colorScaleInterval(length, opaque, transparent), self.ammoImage.colorScaleInterval(length, opaque, transparent))
        self.ammoFade.start()
        self._DefenseCannonGUI__ammoCountersHidden = False

    
    def showExitDialog(self):
        if self._DefenseCannonGUI__dialog == None:
            self._DefenseCannonGUI__dialog = PDialog(text = PLocalizer.CannonDefense['ExitCannon'], style = OTPDialog.YesNo, giveMouse = False, command = self._DefenseCannonGUI__onDialogItemSelected)
        else:
            self._DefenseCannonGUI__dialog.cleanup()
            self._DefenseCannonGUI__dialog = None

    
    def _DefenseCannonGUI__onDialogItemSelected(self, value):
        if value == 1:
            if self.exitEvent:
                self.exitEvent()
            
        
        self._DefenseCannonGUI__dialog.cleanup()
        self._DefenseCannonGUI__dialog = None


