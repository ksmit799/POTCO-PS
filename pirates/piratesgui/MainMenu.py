import copy
import string
import os
from direct.gui.DirectGui import *
from panda3d.core import *
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.GuiButton import GuiButton
from pirates.piratesbase import PLocalizer
from direct.directnotify import DirectNotifyGlobal
from pirates.piratesgui import PDialog
from pirates.piratesgui import FeedbackPanel
from pirates.piratesgui import MainMenuConfirm
from pirates.piratesgui.GameOptions import GameOptions
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from otp.otpgui import OTPDialog

class MainMenu(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('MainMenu')
    
    def __init__(self, title, x, y, width, height):
        self.popupDialog = None
        self.feedbackPanel = None
        self.gameOptions = None
        DirectFrame.__init__(self, relief = None, image = loader.loadModel('models/misc/fade'), image_scale = (5, 2, 2), image_color = (0, 0, 0, 0.29999999999999999), image_pos = (0.5, 0, 0.80000000000000004), state = DGG.NORMAL, pos = (x, 0.0, y), sortOrder = 20)
        self.initialiseoptions(MainMenu)
        self.setBin('gui-fixed', 5)
        self.model = loader.loadModel('models/gui/avatar_chooser_rope')
        self.parentFrame = DirectFrame(parent = self, pos = (0, 0, 1.2))
        self.ropeFrame = DirectFrame(parent = self.parentFrame, relief = None, image = self.model.find('**/avatar_c_A_rope'), image_scale = 0.35999999999999999, pos = (0.51800000000000002, 0, 1.5800000000000001))
        self.ropeFrame2 = DirectFrame(parent = self.parentFrame, relief = None, image = self.model.find('**/avatar_c_A_rope'), image_scale = 0.35999999999999999, pos = (1.0760000000000001, 0, 1.5800000000000001))
        self.logo = loader.loadModel('models/gui/potcLogo')
        self.logo.reparentTo(self.parentFrame)
        self.logo.setPos(width / 2.0, 0, height - 0.14999999999999999)
        self.logo.setScale(0.90000000000000002)
        self.buttons = []
        hotkeys = [
            '']
        hotkeyConfig = getBase().config.GetString('want-menu-hotkeys', '')
        if hotkeyConfig and '%' not in hotkeyConfig:
            hotkeyConfig = 'f%s'
        
        buttonCount = 0
        if hotkeyConfig:
            hotkeys = [
                'esc']
            buttonCount += 1
        
        self.returnButton = GuiButton(parent = self.logo, relief = None, text_scale = PiratesGuiGlobals.TextScaleExtraLarge, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text = PLocalizer.MainMenuReturn, image = (self.model.find('**/avatar_c_A_top'), self.model.find('**/avatar_c_A_top'), self.model.find('**/avatar_c_A_top_over')), image_scale = 0.40000000000000002, text_pos = (0, -0.02), pos = (0, 0, -0.45000000000000001), command = self._MainMenu__handleReturn, hotkeys = hotkeys, hotkeyLabel = hotkeys[0], hotkeyLabelX = 0.20000000000000001, hotkeyArgs = False)
        self.buttons.append(self.returnButton)
        if hotkeyConfig:
            hotkeys = [
                hotkeyConfig % (buttonCount,)]
            buttonCount += 1
        
        self.optionsButton = GuiButton(parent = self.logo, relief = None, text_scale = PiratesGuiGlobals.TextScaleExtraLarge, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text = PLocalizer.MainMenuOptions, image = (self.model.find('**/avatar_c_A_middle'), self.model.find('**/avatar_c_A_middle'), self.model.find('**/avatar_c_A_middle_over')), image_scale = 0.40000000000000002, text_pos = (0, -0.014999999999999999), pos = (0, 0, -0.56399999999999995), command = self._MainMenu__handleOptions, hotkeys = hotkeys, hotkeyLabel = hotkeys[0], hotkeyLabelX = 0.20000000000000001, hotkeyArgs = False)
        self.buttons.append(self.optionsButton)
        if hotkeyConfig:
            hotkeys = [
                hotkeyConfig % (buttonCount,)]
            buttonCount += 1
        
        self.feedbackButton = GuiButton(parent = self.logo, relief = None, text_scale = PiratesGuiGlobals.TextScaleExtraLarge, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text = PLocalizer.MainMenuFeedback, image = (self.model.find('**/avatar_c_A_middle'), self.model.find('**/avatar_c_A_middle'), self.model.find('**/avatar_c_A_middle_over')), image_scale = 0.40000000000000002, text_pos = (0, -0.014999999999999999), pos = (0, 0, -0.67000000000000004), command = self._MainMenu__loadFeedbackPanel, hotkeys = hotkeys, hotkeyLabel = hotkeys[0], hotkeyLabelX = 0.20000000000000001, hotkeyArgs = False)
        self.buttons.append(self.feedbackButton)
        self.buttonZ = -0.67000000000000004
        magicWordConfig = getBase().config.GetString('want-menu-magic', '')
        if magicWordConfig:
            self.magicButtons = []
            magicWords = _[1]
            magicWords = [ choice(mw[0] == '~', mw, '~%s' % mw) for mw in magicWords ]
            for mw in magicWords:
                if hotkeyConfig:
                    hotkeys = [
                        hotkeyConfig % (buttonCount,)]
                    buttonCount += 1
                
                self.buttonZ = self.buttonZ - 0.106
                self.magicButtons.append(GuiButton(parent = self.logo, relief = None, text_scale = PiratesGuiGlobals.TextScaleExtraLarge, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text = mw, image = (self.model.find('**/avatar_c_A_middle'), self.model.find('**/avatar_c_A_middle'), self.model.find('**/avatar_c_A_middle_over')), image_scale = 0.40000000000000002, text_pos = (0, -0.014999999999999999), pos = (0, 0, self.buttonZ), command = lambda mw = mw: self._MainMenu__handleMagic(mw), hotkeys = hotkeys, hotkeyLabel = hotkeys[0], hotkeyLabelX = 0.20000000000000001, hotkeyArgs = False))
            
            self.buttons.extend(self.magicButtons)
        
        if hotkeyConfig:
            hotkeys = [
                hotkeyConfig % (buttonCount,)]
            buttonCount += 1
        
        self.buttonZ = self.buttonZ - 0.106
        self.logoutButton = GuiButton(parent = self.logo, relief = None, text_scale = PiratesGuiGlobals.TextScaleExtraLarge, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text = PLocalizer.MainMenuLogout, image = (self.model.find('**/avatar_c_A_middle'), self.model.find('**/avatar_c_A_middle'), self.model.find('**/avatar_c_A_middle_over')), image_scale = 0.40000000000000002, text_pos = (0, -0.014999999999999999), pos = (0, 0, self.buttonZ), command = self._MainMenu__handleLogout, hotkeys = hotkeys, hotkeyLabel = hotkeys[0], hotkeyLabelX = 0.20000000000000001, hotkeyArgs = False)
        self.buttons.append(self.logoutButton)
        if hotkeyConfig:
            hotkeys = [
                hotkeyConfig % (buttonCount,)]
            buttonCount += 1
        
        self.buttonZ = self.buttonZ - 0.157
        self.quitButton = GuiButton(parent = self.logo, relief = None, text_scale = PiratesGuiGlobals.TextScaleExtraLarge, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text = PLocalizer.MainMenuQuit, image = (self.model.find('**/avatar_c_A_bottom'), self.model.find('**/avatar_c_A_bottom'), self.model.find('**/avatar_c_A_bottom_over')), image_scale = 0.40000000000000002, text_pos = (0, 0.035000000000000003), pos = (0, 0, self.buttonZ), command = self._MainMenu__handleQuit, hotkeys = hotkeys, hotkeyLabel = hotkeys[0], hotkeyLabelX = 0.20000000000000001, hotkeyArgs = False)
        self.buttons.append(self.quitButton)
        self.barFrame = DirectFrame(parent = self.logo, relief = None, image = self.model.find('**/avatar_c_B_frame'), image_scale = 0.34999999999999998, pos = (0, 0, -0.34999999999999998))
        self.showMenuIval = None
        self.hideMenuIval = None
        self.buildShowHideMenuIvals()
        self.menuSfx = loadSfx(SoundGlobals.SFX_GUI_SHOW_PANEL)
        self.menuSfx.setVolume(0.40000000000000002)

    
    def destroy(self):
        self.ignoreAll()
        self.delete_dialogs()
        loader.unloadSfx(self.menuSfx)
        del self.menuSfx
        if self.showMenuIval:
            self.showMenuIval.pause()
        
        self.showMenuIval = None
        if self.hideMenuIval:
            self.hideMenuIval.pause()
        
        self.hideMenuIval = None
        self.buttons = []
        DirectFrame.destroy(self)

    
    def delete_dialogs(self):
        if self.popupDialog:
            self.popupDialog.destroy()
            del self.popupDialog
            self.popupDialog = None
        
        if self.feedbackPanel:
            self.feedbackPanel.destroy()
            del self.feedbackPanel
            self.feedbackPanel = None
        
        if self.gameOptions:
            self.gameOptions.destroy()
            del self.gameOptions
            self.gameOptions = None
        

    
    def _MainMenu__handleReturn(self):
        base.localAvatar.guiMgr.toggleMainMenu()

    
    def _MainMenu__handleOptions(self):
        if self.gameOptions:
            if self.gameOptions.isHidden():
                self.gameOptions.show()
            else:
                self.gameOptions.hide()
        elif base.config.GetBool('want-custom-keys', 0):
            width = 1.8
        else:
            width = 1.6000000000000001
        height = 1.6000000000000001
        x = -width / 2
        y = -height / 2
        self.gameOptions = GameOptions('Game Options', x, y, width, height, base.options)
        self.gameOptions.show()
        base.options = self.gameOptions.options

    
    def _MainMenu__loadFeedbackPanel(self):
        if base.localAvatar.guiMgr.feedbackFormActive:
            return None
        
        self.feedbackPanel = FeedbackPanel.FeedbackPanel()
        self.feedbackPanel.setBin('gui-popup', -5)

    
    def _MainMenu__handleLogout(self):
        if self.popupDialog:
            self.popupDialog.destroy()
        
        self.popupDialog = MainMenuConfirm.MainMenuConfirm('logout')
        self.popupDialog.setBin('gui-popup', -5)

    
    def _MainMenu__handleQuit(self):
        if self.popupDialog:
            self.popupDialog.destroy()
        
        self.popupDialog = MainMenuConfirm.MainMenuConfirm('quit')
        self.popupDialog.setBin('gui-popup', -5)

    
    def _MainMenu__handleMagic(self, mw):
        messenger.send('magicWord', [
            mw])

    
    def logout_dialog_command(self, value):
        self.delete_dialogs()
        if value == 1:
            
            try:
                if base.cr.tutorialObject and base.cr.tutorialObject.map:
                    base.cr.tutorialObject.map.handleCancel()
                elif localAvatar.getCanLogout():
                    if localAvatar.guiMgr.crewHUD.crew:
                        localAvatar.guiMgr.crewHUD.leaveCrew()
                    
                    self.hideMenuIval.start()
                    base.cr.logout()
            except:
                pass
					
    def buildShowHideMenuIvals(self):
        showSequence = Sequence(Func(self.show), ProjectileInterval(self.parentFrame, duration = 0.20000000000000001, endPos = Point3(0, 0, -0.10000000000000001)), ProjectileInterval(self.parentFrame, duration = 0.14999999999999999, endPos = Point3(0, 0, -0.050000000000000003), gravityMult = -1), ProjectileInterval(self.parentFrame, duration = 0.14999999999999999, endPos = Point3(0, 0, -0.10000000000000001)))
        self.showMenuIval = showSequence
        hideParallel = Parallel(ProjectileInterval(self.parentFrame, duration = 0.20000000000000001, endPos = Point3(0, 0, 1.2), gravityMult = -1))
        hideSequence = Sequence(hideParallel, Func(self.hide))
        self.hideMenuIval = hideSequence

    
    def showMenu(self):
        self.menuSfx.play()
        self.showMenuIval.start()

    
    def show(self):
        DirectFrame.show(self)
        for button in self.buttons:
            button.acceptHotkeys()
        
        messenger.send('MainMenuShown')

    
    def hideMenu(self):
        self.menuSfx.play()
        self.hideMenuIval.start()

    
    def hide(self):
        for button in self.buttons:
            button.ignoreHotkeys()
        
        DirectFrame.hide(self)
        messenger.send('MainMenuHidden')

    
    def abruptHide(self):
        self.showMenuIval.finish()
        self.parentFrame.setPos(0, 0, 1.2)
        self.hide()


