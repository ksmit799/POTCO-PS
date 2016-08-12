import math
import time
import os
import random
import sys
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.task.Task import Task
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.DirectObject import DirectObject
from direct.fsm.StateData import StateData
from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State
from direct.gui import DirectGuiGlobals
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import quickProfile
from otp.otpgui import OTPDialog
from otp.otpbase import OTPGlobals
from pirates.audio import SoundGlobals
from pirates.piratesgui.GameOptions import GameOptions
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import PDialog
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.piratesgui.ShardPanel import ShardPanel
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import TimeOfDayManager
from pirates.piratesbase import TODGlobals
from pirates.pirate import Pirate
from pirates.seapatch.SeaPatch import SeaPatch
from pirates.seapatch.Reflection import Reflection
from pirates.makeapirate import NameGUI
from pirates.piratesgui import NonPayerPanel
from pirates.piratesgui import TrialNonPayerPanel
from pirates.piratesbase import UserFunnel
from pirates.pirate import Human
from pirates.pirate import HumanDNA
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
APPROVED = 1
DENIED = 2

class AvatarChooser(DirectObject, StateData):
    notify = directNotify.newCategory('AvatarChooser')
    
    def __init__(self, parentFSM, doneEvent):
        StateData.__init__(self, doneEvent)
        self.choice = (0, 0)
        self.gameOptions = None
        self.av = None
        self.deleteConfirmDialog = None
        self.shareConfirmDialog = None
        self.firstAddDialog = None
        self.notQueueCompleteDialog = None
        self.notDownloadDialog = None
        self.notifications = { }
        self.subFrames = { }
        self.subAvButtons = { }
        self.handleDialogOnScreen = 0
        self.subIds = base.cr.avList.keys()
        if base.cr.isPaid() == OTPGlobals.AccessVelvetRope:
            for subId in base.cr.avList:
                avSet = base.cr.avList[subId]
                for avatar in avSet:
                    if type(avatar) != int:
                        avatar.dna.setTattooChest(0, 0, 0, 0, 0, 0)
                        avatar.dna.setTattooZone2(0, 0, 0, 0, 0, 0)
                        avatar.dna.setTattooZone3(0, 0, 0, 0, 0, 0)
                        avatar.dna.setTattooZone4(0, 0, 0, 0, 0, 0)
                        avatar.dna.setTattooZone5(0, 0, 0, 0, 0, 0)
                        avatar.dna.setTattooZone6(0, 0, 0, 0, 0, 0)
                        avatar.dna.setTattooZone7(0, 0, 0, 0, 0, 0)
                        avatar.dna.setJewelryZone1(0, 0, 0)
                        avatar.dna.setJewelryZone2(0, 0, 0)
                        avatar.dna.setJewelryZone3(0, 0, 0)
                        avatar.dna.setJewelryZone4(0, 0, 0)
                        avatar.dna.setJewelryZone5(0, 0, 0)
                        avatar.dna.setJewelryZone6(0, 0, 0)
                        avatar.dna.setJewelryZone7(0, 0, 0)
                        avatar.dna.setJewelryZone8(0, 0, 0)
                        continue
                
            
        
        self.subIds.sort()
        self.currentSubIndex = 0
        self.currentSubId = 0
        self.nonPayerPanel = None
        self.trialNonPayerPanel = None
        self.httpClient = None
        self.loginTask = None
        self.loginStatusRequest = None
        self.queueTask = None
        self.queueRequest = None
        self.queueComplete = False
        self.allPhasesComplete = False
        self.lastMousePos = (0, 0)
        base.avc = self
        self.forceQueueStr = ''
        self.finalizeConfirmDialog = None
        self.deniedConfirmDialog = None

    
    def enter(self):
        base.options.display.restrictToEmbedded(True)
        taskMgr.setupTaskChain('phasePost', threadPriority = TPHigh)
        if self.isLoaded == 0:
            self.load()
        
        base.disableMouse()
        self.quitButton.show()
        if base.cr.loginInterface.supportsRelogin():
            self.logoutButton.show()
        
        self.scene.reparentTo(render)
        camera.reparentTo(render)
        camera.setPosHpr(-29.018699999999999, 37.012500000000003, 24.75, 4.0899999999999999, 1.0, 0.0)
        loggedInSubId = base.cr.accountDetailRecord.playerAccountId
        if loggedInSubId in self.subIds:
            index = self.subIds.index(loggedInSubId)
        else:
            index = 0
        self.showSub(index)
        if self.ship:
            taskMgr.add(self._AvatarChooser__shipRockTask, 'avatarChooserShipRockTask')
        
        base.transitions.fadeScreen(1)
        base.transitions.fadeIn(3)
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()
        base.cr.loadingScreen.hide()
        globalClock.tick()
        base.graphicsEngine.renderFrame()
        base.playSfx(self.oceanSfx, looping = 1, volume = 0.59999999999999998)
        base.playSfx(self.woodCreaksSfx, looping = 1)
        base.musicMgr.request(SoundGlobals.MUSIC_AVATAR_CHOOSER, volume = 0.40000000000000002, priority = -2)
        self.accept('mouse1', self._startMouseReadTask)
        self.accept('mouse1-up', self._stopMouseReadTask)
        self.accept('mouse3', self._startMouseReadTask)
        self.accept('mouse3-up', self._stopMouseReadTask)
        if not self.disableOptions:
            self.accept(PiratesGlobals.OptionsHotkey, self._AvatarChooser__handleOptions)
        
        if base.launcher.getPhaseComplete(5):
            self._AvatarChooser__allPhasesComplete()
        else:
            self.accept('launcherAllPhasesComplete', self._AvatarChooser__allPhasesComplete)
        self._startLoginStatusTask()
        base.options.savePossibleWorking(base.options)
        if launcher.getValue('GAME_SHOW_FIRSTADD'):
            self.popupTrialPanel()
        

    
    def exit(self):
        if self.isLoaded == 0:
            return None
        
        base.musicMgr.requestFadeOut(SoundGlobals.MUSIC_AVATAR_CHOOSER)
        self.oceanSfx.stop()
        self.woodCreaksSfx.stop()
        if self.deleteConfirmDialog:
            self.deleteConfirmDialog.destroy()
            self.deleteConfirmDialog = None
        
        if self.shareConfirmDialog:
            self.shareConfirmDialog.destroy()
            self.shareConfirmDialog = None
        
        if self.notDownloadDialog:
            self.notDownloadDialog.destroy()
            self.notDownloadDialog = None
        
        self.avatarListFrame.hide()
        self.highlightFrame.hide()
        self.quitFrame.hide()
        self.renameButton.hide()
        self.scene.detachNode()
        if self.ship:
            taskMgr.remove('avatarChooserShipRockTask')
        
        self.ignore('mouse1')
        self.ignore('mouse1-up')
        self.ignore('mouse3')
        self.ignore('mouse3-up')
        self.ignore('f7')
        self.ignore('launcherPercentPhaseComplete')
        self.ignore('launcherAllPhasesComplete')
        self._stopMouseReadTask()
        self._stopQueueTask()
        base.options.saveWorking()
        self.ignoreAll()
        if hasattr(self, 'fadeInterval'):
            self.fadeInterval.pause()
            del self.fadeInterval
        
        if hasattr(self, 'fadeFrame'):
            self.fadeFrame.destroy()
        
        if self.doneStatus and self.doneStatus['mode'] == 'chose':
            base.options.display.restrictToEmbedded(False)
        
        taskMgr.setupTaskChain('phasePost', threadPriority = TPLow)

    
    def load(self):
        self.notify.debug('isPaid: %s' % str(base.cr.isPaid()))
        if self.isLoaded == 1:
            return None
        
        if not base.config.GetBool('disable-pirates-options', 0):
            pass
        self.disableOptions = base.config.GetBool('location-kiosk', 0)
        base.musicMgr.load('avchooser-theme')
        self.model = loader.loadModel('models/gui/avatar_chooser_rope')
        charGui = loader.loadModel('models/gui/char_gui')
        self.oceanSfx = loadSfx(SoundGlobals.SFX_FX_OCEAN_LOOP)
        self.woodCreaksSfx = loadSfx(SoundGlobals.SFX_SHIP_RIGGING)
        self.exclam = charGui.find('**/chargui_exclamation_mark')
        self.scene = NodePath('AvatarChooserScene')
        self.todManager = TimeOfDayManager.TimeOfDayManager()
        self.todManager.request('EnvironmentTOD')
        self.todManager.setEnvironment(TODGlobals.ENV_AVATARCHOOSER, { })
        self.todManager.doEndTimeOfDay()
        self.todManager.skyGroup.setSunTrueAngle(Vec3(260, 0, 15))
        self.todManager.skyGroup.setSunLock(1)
        self.todManager.skyGroup.dirLightSun.node().setColor(Vec4(0.90000000000000002, 0.69999999999999996, 0.80000000000000004, 1))
        pier = loader.loadModel('models/islands/pier_port_royal_2deck')
        pier.setPosHpr(-222.22999999999999, 360.07999999999998, 15.06, 251.56999999999999, 0.0, 0.0)
        pier.flattenStrong()
        pier.reparentTo(self.scene)
        pier2 = loader.loadModel('models/islands/pier_port_royal_1deck')
        pier2.setPosHpr(-35.0, 83.269999999999996, 19.260000000000002, 274.08999999999997, 0.0, 0.0)
        pier2.setScale(0.40000000000000002, 0.29999999999999999, 0.40000000000000002)
        pier2.flattenStrong()
        pier2.reparentTo(self.scene)
        self.water = SeaPatch(render, Reflection.getGlobalReflection(), todMgr = self.todManager)
        self.water.loadSeaPatchFile('out.spf')
        self.water.updateWater(2)
        self.water.ignore('grid-detail-changed')
        self.ship = None
        if base.launcher.getPhaseComplete(3):
            ShipGlobals = ShipGlobals
            import pirates.ship
            self.ship = base.shipFactory.getShip(ShipGlobals.INTERCEPTORL1)
            self.ship.modelRoot.setPosHpr(140.86000000000001, 538.97000000000003, -3.6200000000000001, -133.03999999999999, 0.0, 0.0)
            self.ship.modelRoot.reparentTo(self.scene)
            self.shipRoot = self.ship.modelRoot
            self.ship.playIdle()
            lodNode = self.ship.lod.node()
            self.ship.lod.node().forceSwitch(0)
        
        self.avatarListFrame = DirectFrame(parent = base.a2dTopLeft, relief = None)
        self.ropeFrame = DirectFrame(parent = self.avatarListFrame, relief = None, image = self.model.find('**/avatar_c_A_rope'), image_scale = 0.35999999999999999, pos = (0, 0, -0.014999999999999999))
        self.subFrame = BorderFrame(parent = self.avatarListFrame, frameSize = (-0.25, 0.25, -0.040000000000000001, 0.089999999999999997), borderScale = 0.20000000000000001, pos = (0, 0, -0.16), modelName = 'general_frame_f')
        triangleGui = loader.loadModel('models/gui/triangle')
        self.subLabel = DirectLabel(parent = self.subFrame, relief = None, text = '', text_scale = 0.044999999999999998, text_fg = (1, 0.90000000000000002, 0.69999999999999996, 0.90000000000000002), text_pos = (0, 0.035000000000000003), textMayChange = 1)
        if base.config.GetBool('allow-linked-accounts', 0):
            self.nextSubButton = DirectButton(parent = self.subFrame, relief = None, image = (triangleGui.find('**/triangle'), triangleGui.find('**/triangle_down'), triangleGui.find('**/triangle_over')), pos = (0.31, 0, 0.025000000000000001), scale = 0.080000000000000002, command = self.changeSub, extraArgs = [
                1])
            self.prevSubButton = DirectButton(parent = self.subFrame, relief = None, image = (triangleGui.find('**/triangle'), triangleGui.find('**/triangle_down'), triangleGui.find('**/triangle_over')), hpr = (0, 0, 180), pos = (-0.31, 0, 0.025000000000000001), scale = 0.080000000000000002, command = self.changeSub, extraArgs = [
                -1])
        
        self._AvatarChooser__createAvatarButtons()
        self.ropeFrame.reparentTo(self.avatarListFrame)
        self.subFrame.reparentTo(self.avatarListFrame)
        self.versionLabel = DirectLabel(parent = base.a2dTopRight, relief = None, text_scale = 0.040000000000000001, text_fg = (1, 1, 1, 0.5), text = '%s\n%s' % (base.cr.getServerVersion(), base.win.getPipe().getInterfaceName()), text_align = TextNode.ARight, pos = (-0.050000000000000003, 0, -0.050000000000000003))
        self.highlightFrame = DirectFrame(parent = base.a2dBottomCenter, relief = None, image = self.model.find('**/avatar_c_B_frame'), image_scale = 0.37, pos = (0, 0, 0.25), scale = 0.90000000000000002)
        self.highlightFrame.hide()
        if base.config.GetBool('allow-linked-accounts', 0):
            self.shareButton = DirectButton(parent = self.highlightFrame, relief = None, text_scale = 0.044999999999999998, text_fg = (1, 0.90000000000000002, 0.69999999999999996, 0.90000000000000002), text_shadow = PiratesGuiGlobals.TextShadow, text = ('', '', PLocalizer.AvatarChooserShared, ''), image = (self.model.find('**/avatar_c_B_unlock'), self.model.find('**/avatar_c_B_unlock'), self.model.find('**/avatar_c_B_unlock_over')), image_scale = 0.37, text_pos = (0, -0.10000000000000001), pos = (-0.51000000000000001, 0, -0.080000000000000002), scale = 1.3, command = self._AvatarChooser__handleShare)
        
        self.playButton = DirectButton(parent = self.highlightFrame, relief = None, text_scale = 0.050000000000000003, text_fg = (0.69999999999999996, 0.69999999999999996, 0.69999999999999996, 0.69999999999999996), text_shadow = PiratesGuiGlobals.TextShadow, text = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserLoading, image = (self.model.find('**/avatar_c_B_bottom'), self.model.find('**/avatar_c_B_bottom'), self.model.find('**/avatar_c_B_bottom_over')), image_scale = 0.37, text_pos = (0, -0.014999999999999999), pos = (0, 0, -0.080000000000000002), scale = 1.7, color = (0.69999999999999996, 0.69999999999999996, 0.69999999999999996, 0.69999999999999996), state = DGG.DISABLED, command = self._AvatarChooser__handlePlay)
        if not self.allPhasesComplete:
            self.playButton['text'] = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserLoading
        elif not self.queueComplete:
            self.playButton['text'] = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserInQueue
        else:
            self.playButton['text'] = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserPlay
            self.playButton.setColor(1, 1, 1, 1)
            self.playButton['text_fg'] = (1.0, 0.90000000000000002, 0.69999999999999996, 0.90000000000000002)
        self.accept('enter', self._AvatarChooser__handleEnter)
        self.accept('arrow_up', self._AvatarChooser__handleArrowUp)
        self.accept('arrow_down', self._AvatarChooser__handleArrowDown)
        self.deleteButton = DirectButton(parent = self.highlightFrame, relief = None, text_scale = 0.044999999999999998, text_fg = (1, 0.90000000000000002, 0.69999999999999996, 0.90000000000000002), text_shadow = PiratesGuiGlobals.TextShadow, text = ('', '', PLocalizer.AvatarChooserDelete, ''), image = (self.model.find('**/avatar_c_B_delete'), self.model.find('**/avatar_c_B_delete'), self.model.find('**/avatar_c_B_delete_over')), image_scale = 0.37, text_pos = (0, -0.10000000000000001), pos = (0.51000000000000001, 0, -0.080000000000000002), scale = 1.3, command = self._AvatarChooser__handleDelete)
        self.quitFrame = DirectFrame(parent = base.a2dBottomRight, relief = None, image = self.model.find('**/avatar_c_C_back'), image_scale = 0.37, pos = (-0.40000000000000002, 0, 0.20999999999999999), scale = 0.90000000000000002)
        self.quitFrameForeground = DirectFrame(parent = self.quitFrame, relief = None, image = self.model.find('**/avatar_c_C_frame'), image_scale = 0.37, pos = (0, 0, 0))
        self.logoutButton = DirectButton(parent = self.quitFrame, relief = None, text_scale = 0.044999999999999998, text_fg = (1, 0.90000000000000002, 0.69999999999999996, 0.90000000000000002), text_shadow = PiratesGuiGlobals.TextShadow, text = PLocalizer.OptionsPageLogout, image = (self.model.find('**/avatar_c_C_box'), self.model.find('**/avatar_c_C_box'), self.model.find('**/avatar_c_C_box_over')), image_scale = 0.37, text_pos = (0, -0.014999999999999999), pos = (0, 0, 0.20000000000000001), command = self._AvatarChooser__handleLogoutWithoutConfirm)
        self.logoutButton.hide()
        if self.disableOptions:
            optionsState = DGG.DISABLED
        else:
            optionsState = DGG.NORMAL
        self.optionsButton = DirectButton(parent = self.quitFrame, relief = None, text_scale = 0.050000000000000003, text_fg = (1, 0.90000000000000002, 0.69999999999999996, 0.90000000000000002), text_shadow = PiratesGuiGlobals.TextShadow, text = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserOptions, image = (self.model.find('**/avatar_c_C_box'), self.model.find('**/avatar_c_C_box'), self.model.find('**/avatar_c_C_box_over')), image_scale = 0.37, text_pos = (0, -0.014999999999999999), pos = (0, 0, 0.20999999999999999), command = self._AvatarChooser__handleOptions, state = optionsState)
        if self.disableOptions:
            self.optionsButton.setColorScale(Vec4(0.69999999999999996, 0.69999999999999996, 0.69999999999999996, 0.69999999999999996))
        
        self.upgradeButton = DirectButton(parent = self.quitFrame, relief = None, text_scale = 0.050000000000000003, text_fg = (1, 0.90000000000000002, 0.69999999999999996, 0.90000000000000002), text_shadow = PiratesGuiGlobals.TextShadow, text = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserUpgrade, image = (self.model.find('**/avatar_c_C_box'), self.model.find('**/avatar_c_C_box'), self.model.find('**/avatar_c_C_box_over')), image_scale = 0.37, text_pos = (0, -0.014999999999999999), pos = (0, 0, 0.070000000000000007), command = self._AvatarChooser__handleUpgrade)
        if base.cr.isPaid() == OTPGlobals.AccessFull:
            self.upgradeButton.hide()
            self.optionsButton.setPos(0, 0, 0.070000000000000007)
        
        self.disableQuit = base.config.GetBool('location-kiosk', 0)
        if self.disableQuit:
            quitState = DGG.DISABLED
        else:
            quitState = DGG.NORMAL
        self.quitButton = DirectButton(parent = self.quitFrame, state = quitState, relief = None, text_scale = 0.050000000000000003, text_fg = (1, 0.90000000000000002, 0.69999999999999996, 0.90000000000000002), text_shadow = PiratesGuiGlobals.TextShadow, text = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserQuit, image = (self.model.find('**/avatar_c_C_box'), self.model.find('**/avatar_c_C_box'), self.model.find('**/avatar_c_C_box_over')), image_scale = 0.37, text_pos = (0, -0.014999999999999999), pos = (0, 0, -0.070000000000000007), command = self._AvatarChooser__handleQuit)
        if self.disableQuit:
            self.quitButton.setColorScale(Vec4(0.69999999999999996, 0.69999999999999996, 0.69999999999999996, 0.69999999999999996))
        
        self.renameButton = DirectButton(parent = base.a2dTopRight, relief = None, text_scale = 0.050000000000000003, text_fg = (1, 0.90000000000000002, 0.69999999999999996, 0.90000000000000002), text_shadow = PiratesGuiGlobals.TextShadow, text = '\x01smallCaps\x01%s\x02' % 'rename', image = (self.model.find('**/avatar_c_C_box'), self.model.find('**/avatar_c_C_box'), self.model.find('**/avatar_c_C_box_over')), image_scale = 0.37, text_pos = (0, -0.014999999999999999), pos = (-0.29999999999999999, 0, -0.20000000000000001), command = self._AvatarChooser__handleRename)
        
        def shardSelected(shardId):
            base.cr.defaultShard = shardId

        self.shardPanel = ShardPanel(base.a2dBottomLeft, gear = NodePath('gear'), inverted = True, relief = None, scale = 0.84999999999999998, hpr = Vec3(0, 0, 180), pos = Vec3(0.41499999999999998, 0, 0.02), uppos = Vec3(0.41499999999999998, 0, 0.02), downpos = Vec3(0.41499999999999998, 0, 0.59999999999999998), shardSelected = shardSelected, buttonFont = PiratesGlobals.getInterfaceFont())
        self.shardPanel.setScissor(self.highlightFrame, Point3(-20, 0, -0.17999999999999999), Point3(20, 0, 1.0))
        self.shardPanelBottom = loader.loadModel('models/gui/general_frame_bottom')
        self.shardPanelBottom.setPos(0.41999999999999998, 0, 0.095000000000000001)
        self.shardPanelBottom.setScale(0.27300000000000002)
        self.shardPanelBottom.reparentTo(base.a2dBottomLeft)
        self.logo = loader.loadModel('models/gui/potcLogo')
        self.logo.reparentTo(self.avatarListFrame)
        self.logo.setPos(0, 0, 0.10000000000000001)
        self.logo.setScale(0.66000000000000003)
        charGui.removeNode()

    
    def _AvatarChooser__createAvatarButtons(self):
        subCard = loader.loadModel('models/gui/toplevel_gui')
        for subFrame in self.subFrames.values():
            subFrame.destroy()
        
        for buttonList in self.subAvButtons.values():
            for button in buttonList:
                button.destroy()
            
        
        self.subFrames = { }
        self.subAvButtons = { }
        i = 0
        for (subId, avData) in base.cr.avList.items():
            subFrame = DirectFrame(parent = self.avatarListFrame, relief = None, pos = (0, 0, -0.29999999999999999))
            self.subFrames[subId] = subFrame
            avatarButtons = []
            self.subAvButtons[subId] = avatarButtons
            spacing = -0.10000000000000001
            for (av, slot) in zip(avData, range(len(avData))):
                x = 0.0
                imageColor = Vec4(1, 1, 1, 1)
                textScale = 0.044999999999999998
                textFg = (1, 0.90000000000000002, 0.69999999999999996, 0.90000000000000002)
                if slot == 0:
                    z = -0.080000000000000002
                    textPos = (0, -0.02)
                    image = (self.model.find('**/avatar_c_A_top'), self.model.find('**/avatar_c_A_top'), self.model.find('**/avatar_c_A_top_over'), self.model.find('**/avatar_c_A_top'))
                elif slot == len(avData) - 1:
                    z = slot * spacing - 0.125
                    textPos = (0, 0.033000000000000002)
                    image = (self.model.find('**/avatar_c_A_bottom'), self.model.find('**/avatar_c_A_bottom'), self.model.find('**/avatar_c_A_bottom_over'), self.model.find('**/avatar_c_A_bottom'))
                else:
                    z = slot * spacing - 0.080000000000000002
                    textPos = (0, -0.014999999999999999)
                    image = (self.model.find('**/avatar_c_A_middle'), self.model.find('**/avatar_c_A_middle'), self.model.find('**/avatar_c_A_middle_over'), self.model.find('**/avatar_c_A_middle'))
                if av == OTPGlobals.AvatarSlotAvailable:
                    text = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserCreate
                    if -3 in avData:
                        command = self._AvatarChooser__handleCreate
                    else:
                        command = self.popupFeatureBrowser
                    state = DGG.NORMAL
                elif av == OTPGlobals.AvatarPendingCreate:
                    text = PLocalizer.AvatarChooserUnderConstruction
                    command = None
                    state = DGG.DISABLED
                    imageColor = Vec4(0.69999999999999996, 0.69999999999999996, 0.69999999999999996, 1)
                elif av == OTPGlobals.AvatarSlotUnavailable:
                    text = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserCreate
                    if -3 in avData:
                        command = self._AvatarChooser__handleCreate
                    else:
                        command = self.popupFeatureBrowser
                    state = DGG.NORMAL
                else:
                    avName = av.dna.getDNAName()
                    text = avName
                    command = self._AvatarChooser__handleHighlight
                    state = DGG.NORMAL
                dib = DirectButton(relief = None, parent = subFrame, state = state, text_fg = textFg, text_scale = textScale, text_shadow = PiratesGuiGlobals.TextShadow, text = text, image = image, image_color = imageColor, image_scale = 0.37, text_pos = textPos, pos = (x, 0, z), command = command, extraArgs = [
                    subId,
                    slot])
                avatarButtons.append(dib)
            
            i += 1
        
        subCard.removeNode()
        self.isLoaded = 1
        if self.queueComplete == False:
            self._AvatarChooser__deactivateCreateButtons()
        

    
    def unload(self):
        if self.isLoaded == 0:
            return None
        
        loader.unloadSfx(self.oceanSfx)
        loader.unloadSfx(self.woodCreaksSfx)
        del self.oceanSfx
        del self.woodCreaksSfx
        loader.unloadModel(self.model)
        self.model.removeNode()
        del self.model
        self.todManager.skyGroup.setSunLock(0)
        self.logo.removeNode()
        if self.av:
            self.av.delete()
            del self.av
        
        if self.ship:
            self.ship.destroy()
            self.ship = None
            taskMgr.remove('avatarChooserShipRockTask')
            self.shipRoot = None
        
        self.water.delete()
        del self.water
        self.scene.removeNode()
        del self.scene
        self.todManager.disable()
        self.todManager.delete()
        del self.todManager
        cleanupDialog('globalDialog')
        for subFrame in self.subFrames.values():
            subFrame.destroy()
        
        for buttonList in self.subAvButtons.values():
            for button in buttonList:
                button.destroy()
            
        
        del self.subFrames
        del self.subAvButtons
        self.avatarListFrame.destroy()
        self.highlightFrame.destroy()
        self.quitFrame.destroy()
        self.renameButton.destroy()
        if self.nonPayerPanel:
            self.nonPayerPanel.destroy()
        
        del self.nonPayerPanel
        if self.trialNonPayerPanel:
            self.trialNonPayerPanel.destroy()
        
        del self.trialNonPayerPanel
        if self.gameOptions is not None:
            base.options = self.gameOptions.options
            self.gameOptions.destroy()
            del self.gameOptions
        
        self.versionLabel.destroy()
        del self.versionLabel
        self.shardPanel.destroy()
        del self.shardPanel
        self.shardPanelBottom.removeNode()
        self.ignoreAll()
        self.isLoaded = 0
        if self.finalizeConfirmDialog:
            self.finalizeConfirmDialog.destroy()
            self.finalizeConfirmDialog = None
        
        if self.deniedConfirmDialog:
            self.deniedConfirmDialog.destroy()
            self.deniedConfirmDialog = None
        

    
    def getChoice(self):
        return self.choice

    
    def _AvatarChooser__showHighlightedAvatar(self):
        self.notify.debugCall()
        (subId, slot) = self.choice
        potAv = base.cr.avList[subId][slot]
        if self.av:
            self.av.cleanupHuman()
            self.av.delete()
        
        if self.deleteConfirmDialog:
            self.deleteConfirmDialog.destroy()
            self.deleteConfirmDialog = None
        
        if self.shareConfirmDialog:
            self.shareConfirmDialog.destroy()
            self.shareConfirmDialog = None
        
        self.av = Pirate.Pirate()
        self.av.setDNAString(potAv.dna)
        self.av.generateHuman(self.av.style.gender, base.cr.humanHigh)
        self.av.setPosHpr(-29.690000000000001, 46.350000000000001, 22.050000000000001, 180.0, 0.0, 0.0)
        self.av.reparentTo(self.scene)
        self.av.bindAnim('idle')
        self.av.loop('idle')
        self.av.useLOD(2000)
        self.highlightFrame.show()
        if base.config.GetBool('allow-linked-accounts', 0):
            if potAv.shared:
                self.shareButton['image'] = (self.model.find('**/avatar_c_B_unlock'), self.model.find('**/avatar_c_B_unlock'), self.model.find('**/avatar_c_B_unlock_over'))
                self.shareButton['text'] = ('', '', PLocalizer.AvatarChooserLocked, '')
            else:
                self.shareButton['image'] = (self.model.find('**/avatar_c_B_lock'), self.model.find('**/avatar_c_B_lock'), self.model.find('**/avatar_c_B_lock_over'))
                self.shareButton['text'] = ('', '', PLocalizer.AvatarChooserShared, '')
        
        if not (potAv.online):
            if potAv.creator or not base.config.GetBool('allow-linked-accounts', 0):
                self.deleteButton['state'] = DGG.NORMAL
                if base.config.GetBool('allow-linked-accounts', 0):
                    self.shareButton['state'] = DGG.NORMAL
                
            else:
                self.deleteButton['state'] = DGG.DISABLED
                if base.config.GetBool('allow-linked-accounts', 0):
                    self.shareButton['state'] = DGG.DISABLED
                
        if potAv.online:
            self.playButton['text'] = PLocalizer.AvatarChooserAlreadyOnline
            self.playButton['state'] = DGG.DISABLED
        elif potAv.shared and potAv.creator or not base.config.GetBool('allow-linked-accounts', 0):
            if not self.allPhasesComplete:
                self.playButton['text'] = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserLoading
            elif not self.queueComplete:
                self.playButton['text'] = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserInQueue
            else:
                self.playButton['text'] = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserPlay
            self.playButton['state'] = DGG.NORMAL
        else:
            self.playButton['text'] = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserLockedByOwner
            self.playButton['state'] = DGG.DISABLED
        self.renameButton.hide()
        if potAv.wishState == 'APPROVED':
            self.blockInput()
            self.finalizeConfirmDialog = PDialog.PDialog(text = PLocalizer.AvatarChooserNameAccepted, style = OTPDialog.Acknowledge, command = self._AvatarChooser__handleFinalize)
        elif potAv.wishState == 'DENIED' or potAv.wishState == 'OPEN':
            if self.notifications.get(slot, 0):
                self.blockInput()
                if not self.handleDialogOnScreen:
                    self.notify.info('deniedConfirmDialog on screen')
                    self.deniedConfirmDialog = PDialog.PDialog(text = PLocalizer.AvatarChooserPleaseRename, style = OTPDialog.Acknowledge, command = self._AvatarChooser__handleDenied)
                
                self.handleDialogOnScreen = 1
            
            self.renameButton.show()
        
        if not (potAv.lastLogout) or int(time.time() / 60) - potAv.lastLogout > 60:
            potAv.defaultShard = 0
            base.cr.avPlayedRecently = False
        else:
            base.cr.avPlayedRecently = True
        if base.cr.defaultShard == 0:
            self.shardPanel['preferredShard'] = potAv.defaultShard
        

    
    def _AvatarChooser__hideHighlightedAvatar(self):
        if self.av:
            self.av.delete()
            self.av = None
        
        self.highlightFrame.hide()
        self.renameButton.hide()

    
    def _AvatarChooser__handleRename(self):
        self.enterNameMode()

    
    def _AvatarChooser__handleHighlight(self, subId, slot):
        self.choice = (subId, slot)
        for button in self.subAvButtons[subId]:
            if button['text'] == PLocalizer.AvatarChooserSlotUnavailable:
                button['text_fg'] = (0.5, 0.5, 0.5, 1)
                continue
            button['text_fg'] = (1, 0.90000000000000002, 0.69999999999999996, 0.90000000000000002)
        
        self.subAvButtons[subId][slot]['text_fg'] = (1, 1, 1, 1)
        self._AvatarChooser__showHighlightedAvatar()

    
    def _AvatarChooser__rotateHighlightedAvatar(self, val):
        if self.av:
            self.av.setH(val)
        

    
    def _AvatarChooser__handleArrowUp(self):
        if self.gameOptions is not None and not self.gameOptions.isHidden():
            return None
        
        sub = self.choice[0]
        slot = self.choice[1]
        initialSlot = slot
        if not sub:
            return None
        
        numButtons = len(self.subAvButtons[sub])
        av = False
        for index in range(0, numButtons - 1):
            if base.cr.avList.get(sub)[index] not in (OTPGlobals.AvatarSlotUnavailable, OTPGlobals.AvatarSlotAvailable, OTPGlobals.AvatarPendingCreate):
                av = True
                break
                continue
        
        if not av:
            return None
        
        if slot == 0:
            slot = numButtons - 1
        else:
            slot = slot - 1
        while base.cr.avList.get(sub)[slot] in (OTPGlobals.AvatarSlotUnavailable, OTPGlobals.AvatarSlotAvailable, OTPGlobals.AvatarPendingCreate):
            if slot > 0:
                slot = slot - 1
                continue
            slot = numButtons - 1
        if self.subAvButtons[sub][slot]['state'] == DGG.NORMAL and initialSlot != slot:
            self._AvatarChooser__handleHighlight(sub, slot)
        

    
    def _AvatarChooser__handleArrowDown(self):
        if self.gameOptions is not None and not self.gameOptions.isHidden():
            return None
        
        sub = self.choice[0]
        slot = self.choice[1]
        initialSlot = slot
        if not sub:
            return None
        
        numButtons = len(self.subAvButtons[sub])
        av = False
        for index in range(0, numButtons - 1):
            if base.cr.avList.get(sub)[index] not in (OTPGlobals.AvatarSlotUnavailable, OTPGlobals.AvatarSlotAvailable, OTPGlobals.AvatarPendingCreate):
                av = True
                break
                continue
        
        if not av:
            return None
        
        if slot == numButtons - 1:
            slot = 0
        else:
            slot = slot + 1
        while base.cr.avList.get(sub)[slot] in (OTPGlobals.AvatarSlotUnavailable, OTPGlobals.AvatarSlotAvailable, OTPGlobals.AvatarPendingCreate):
            if slot < numButtons - 1:
                slot = slot + 1
                continue
            slot = 0
        if self.subAvButtons[sub][slot]['state'] == DGG.NORMAL and initialSlot != slot:
            self._AvatarChooser__handleHighlight(sub, slot)
        

    
    def _AvatarChooser__handleCreate(self, subId, slot):
        if not self.queueComplete:
            if not self.notQueueCompleteDialog:
                self.notQueueCompleteDialog = PDialog.PDialog(text = PLocalizer.AvatarChooserQueued, style = OTPDialog.Acknowledge, command = self._AvatarChooser__handleNotQueueComplete)
            
            self.notQueueCompleteDialog.show()
            return None
        
        self.choice = (subId, slot)
        self.accept('rejectAvatarSlot', self._AvatarChooser__rejectAvatarSlot)
        self.accept('avatarSlotResponse', self._AvatarChooser__avatarSlotResponse)
        base.cr.avatarManager.sendRequestAvatarSlot(subId, slot)
        base.cr.waitForDatabaseTimeout(requestName = 'WaitForCreateAvatarResponse')
        self.blockInput()

    
    def _AvatarChooser__rejectAvatarSlot(self, reasonId, subId, slot):
        self.notify.warning('rejectAvatarSlot: %s' % reasonId)
        self.ignore('rejectAvatarSlot')
        self.ignore('avatarSlotResponse')
        base.cr.cleanupWaitingForDatabase()
        self.allowInput()

    
    def _AvatarChooser__avatarSlotResponse(self, subId, slot):
        UserFunnel.loggingAvID('write', 'NEW')
        UserFunnel.loggingSubID('write', subId)
        self.ignore('rejectAvatarSlot')
        self.ignore('avatarSlotResponse')
        base.cr.cleanupWaitingForDatabase()
        self.doneStatus = {
            'mode': 'create' }
        self.acceptOnce(base.transitions.FadeOutEvent, lambda : messenger.send(self.doneEvent, [
self.doneStatus]))
        base.transitions.fadeOut()

    
    def _AvatarChooser__handleShare(self):
        if self.shareConfirmDialog:
            self.shareConfirmDialog.destroy()
        
        (subId, slot) = self.choice
        potAv = base.cr.avList[subId][slot]
        name = potAv.dna.getDNAName()
        self.blockInput()
        if potAv.shared:
            self.shareConfirmDialog = PDialog.PDialog(text = PLocalizer.AvatarChooserConfirmLock % name, style = OTPDialog.TwoChoice, command = self._AvatarChooser__handleShareConfirmation)
        else:
            self.shareConfirmDialog = PDialog.PDialog(text = PLocalizer.AvatarChooserConfirmShare % name, style = OTPDialog.TwoChoice, command = self._AvatarChooser__handleShareConfirmation)

    
    def _AvatarChooser__shareAvatarResponse(self, avatarId, subId, shared):
        base.cr.cleanupWaitingForDatabase()
        self.ignore('rejectShareAvatar')
        self.ignore('shareAvatarResponse')
        (subId, slot) = self.choice
        potAv = base.cr.avList[subId][slot]
        potAv.shared = shared
        if potAv.shared:
            self.shareButton['image'] = (self.model.find('**/avatar_c_B_unlock'), self.model.find('**/avatar_c_B_unlock'), self.model.find('**/avatar_c_B_unlock_over'))
            self.shareButton['text'] = ('', '', PLocalizer.AvatarChooserLocked, '')
        else:
            self.shareButton['image'] = (self.model.find('**/avatar_c_B_lock'), self.model.find('**/avatar_c_B_lock'), self.model.find('**/avatar_c_B_lock_over'))
            self.shareButton['text'] = ('', '', PLocalizer.AvatarChooserShared, '')
        self.allowInput()

    
    def _AvatarChooser__rejectShareAvatar(self, reasonId):
        self.notify.warning('rejectShareAvatar: %s' % reasonId)
        base.cr.cleanupWaitingForDatabase()
        self.ignore('rejectShareAvatar')
        self.ignore('shareAvatarResponse')
        self.allowInput()

    
    def _AvatarChooser__handleEnter(self):
        if self.playButton['state'] == DGG.NORMAL:
            self._AvatarChooser__handlePlay()
        

    
    def _AvatarChooser__handlePlay(self):
        if not self.queueComplete:
            if not self.notQueueCompleteDialog:
                self.notQueueCompleteDialog = PDialog.PDialog(text = PLocalizer.AvatarChooserQueued, style = OTPDialog.Acknowledge, command = self._AvatarChooser__handleNotQueueComplete)
            
            self.notQueueCompleteDialog.show()
            return None
        
        if not self.allPhasesComplete:
            if self.notDownloadDialog:
                self.notDownloadDialog.show()
            else:
                self.notDownloadDialog = PDialog.PDialog(text = PLocalizer.AvatarChooserNotDownload, style = OTPDialog.Acknowledge, command = self._AvatarChooser__handleNotDownload)
                base.cr.centralLogger.writeClientEvent('User encountered phase blocker at pick-a-pirate')
                self.notDownloadDialog.show()
            return None
        
        if (0, 0) == self.choice:
            self._AvatarChooser__handleCreate(self.currentSubId, 0)
            return None
        
        (subId, slot) = self.choice
        potAv = base.cr.avList[subId][slot]
        if potAv in (OTPGlobals.AvatarSlotUnavailable, OTPGlobals.AvatarSlotAvailable, OTPGlobals.AvatarPendingCreate):
            return None
        
        self.notify.info('AvatarChooser: wants to play slot: %s avId: %s subId: %s' % (slot, potAv.id, subId))
        self.accept('rejectPlayAvatar', self._AvatarChooser__rejectPlayAvatar)
        self.accept('playAvatarResponse', self._AvatarChooser__playAvatarResponse)
        winInfo = base.win.getProperties()
        x = winInfo.getXSize()
        y = winInfo.getYSize()
        ratio = float(x) / y
        self.fadeFrame = DirectFrame(parent = aspect2dp, frameSize = (-1.0 * ratio, 1.0 * ratio, -1.0, 1.0))
        self.fadeFrame.setTransparency(1)
        self.fadeInterval = Sequence(Func(self.blockInput), Func(self.fadeFrame.show), LerpColorScaleInterval(self.fadeFrame, 0.29999999999999999, Vec4(0.0, 0.0, 0.0, 1.0), Vec4(0.0, 0.0, 0.0, 0.0), blendType = 'easeInOut'), Func(base.transitions.fadeOut, t = 0), Func(base.cr.avatarManager.sendRequestPlayAvatar, potAv.id, subId), Func(base.cr.waitForDatabaseTimeout, requestName = 'WaitForPlayAvatarResponse'))
        self.fadeInterval.start()
        base.emoteGender = base.cr.avList[subId][slot].dna.gender

    
    def _AvatarChooser__rejectPlayAvatar(self, reasonId, avatarId):
        self.notify.warning('rejectPlayAvatar: %s' % reasonId)
        self.ignore('rejectPlayAvatar')
        self.ignore('playAvatarResponse')
        base.cr.cleanupWaitingForDatabase()
        self.rejectPlayAvatarDialog = PDialog.PDialog(text = PLocalizer.AvatarChooserRejectPlayAvatar, style = OTPDialog.Acknowledge, command = self._AvatarChooser__handleRejectPlayAvatar)

    
    def _AvatarChooser__handleRejectPlayAvatar(self, value):
        base.cr.loginFSM.request('shutdown')

    
    def _AvatarChooser__playAvatarResponse(self, avatarId, subId, access, founder):
        (subId, slot) = self.choice
        self.notify.info('AvatarChooser: acquired avatar slot: %s avId: %s subId: %s' % (slot, avatarId, subId))
        UserFunnel.loggingAvID('write', avatarId)
        UserFunnel.loggingSubID('write', subId)
        self.ignore('rejectPlayAvatar')
        self.ignore('playAvatarResponse')
        base.cr.cleanupWaitingForDatabase()
        self.doneStatus = {
            'mode': 'chose' }
        messenger.send(self.doneEvent, [
            self.doneStatus])
        messenger.send('destroyFeedbackPanel')

    
    def _AvatarChooser__activatePlayButton(self):
        if not self.allPhasesComplete:
            self.playButton['text'] = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserLoading
            return None
        
        if not self.queueComplete:
            self.playButton['text'] = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserInQueue
            return None
        
        self.playButton['state'] = DGG.NORMAL
        self.playButton['text'] = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserPlay
        self.playButton.setColor(1, 1, 1, 1)
        self.playButton['text_fg'] = (1.0, 0.90000000000000002, 0.69999999999999996, 0.90000000000000002)

    
    def _AvatarChooser__activateCreateButtons(self):
        if not self.allPhasesComplete:
            return None
        
        if not self.queueComplete:
            return None
        
        for (currSubId, currSubVal) in base.cr.avList.items():
            for currIdx in range(len(currSubVal)):
                if currSubVal[currIdx] == OTPGlobals.AvatarSlotAvailable:
                    button = self.subAvButtons[currSubId][currIdx]
                    button.setColorScale(1, 1, 1, 1)
                    button['text'] = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserCreate
                    continue
            
        

    
    def _AvatarChooser__deactivatePlayButton(self):
        self.playButton['text'] = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserInQueue
        self.playButton.setColor(0.69999999999999996, 0.69999999999999996, 0.69999999999999996, 0.69999999999999996)
        self.playButton['text_fg'] = (0.69999999999999996, 0.69999999999999996, 0.69999999999999996, 0.69999999999999996)

    
    def _AvatarChooser__deactivateCreateButtons(self):
        for (currSubId, currSubVal) in base.cr.avList.items():
            for currIdx in range(len(currSubVal)):
                if currSubVal[currIdx] == OTPGlobals.AvatarSlotAvailable:
                    button = self.subAvButtons[currSubId][currIdx]
                    button.setColorScale(0.69999999999999996, 0.69999999999999996, 0.69999999999999996, 0.69999999999999996)
                    button['text'] = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserInQueue
                    continue
            
        

    
    def _AvatarChooser__allPhasesComplete(self):
        self.allPhasesComplete = True
        self._AvatarChooser__activatePlayButton()
        self._AvatarChooser__activateCreateButtons()
        self.ignore('launcherAllPhasesComplete')

    
    def _startLoginStatusTask(self):
        if __dev__ or launcher.getValue('IS_DEV'):
            disableQueueDefault = 1
        else:
            disableQueueDefault = 0
        if config.GetBool('disable-server-queueing', disableQueueDefault):
            self._setQueueComplete()
            return None
        
        self.httpClient = HTTPClient()
        import urllib2 as urllib2
        proxies = urllib2.getproxies()
        if proxies and proxies.get('http'):
            self.notify.info('queuing proxy found')
            self.httpClient.setProxySpec(proxies.get('http'))
        else:
            self.notify.info('queuing proxy is none')
        loginTokenKey = config.GetString('queueing-token-1', 'SESSION_TOKEN')
        self.notify.info('using queueing token 1 of %s' % loginTokenKey)
        self.loginToken = launcher.getValue(loginTokenKey, None)
        self.queueComplete = False
        self.queueStatus = launcher.getValue('LOGIN_ACTION', None)
        if self.queueStatus and self.queueStatus == 'PLAY':
            self._setQueueComplete()
            return None
        
        self.queueFreqSeconds = launcher.getValue('QUEUE_FREQ_SECONDS', None)
        self.queueUrl = launcher.getValue('QUEUE_URL', None)
        if self.loginToken is not None and self.queueStatus == 'QUEUE' and self.queueFreqSeconds is not None and self.queueUrl is not None:
            self.queueFreqSeconds = int(self.queueFreqSeconds)
            self._startQueueTask()
            return None
        
        self.loginStatusRequest = None
        self.loginStatusTask = taskMgr.add(self._checkLoginStatus, 'AvatarChooser-CheckLoginStatus')
        self.loginStatusTask.delayTime = 0.10000000000000001

    
    def _checkLoginStatus(self, task):
        if not self.loginStatusRequest:
            loginStatusUrl = launcher.getValue('WEB_PAGE_LOGIN_RPC', 'https://piratesonline.go.com/auth/piratesLogin') + '?'
            if self.loginToken:
                loginStatusUrl += 'login_token=%s' % (self.loginToken,)
            elif __dev__ or launcher.getValue('IS_DEV'):
                testLogin = config.GetString('queueing-login', 'xx')
                testPass = config.GetString('queueing-pass', 'xx')
                loginStatusUrl += 'username=%s&password=%s' % (testLogin, testPass)
                if config.GetBool('server-queueing-force', 0):
                    self.forceQueueStr = '&wannaqueue=1'
                
                loginStatusUrl += self.forceQueueStr
            
            loginStatusUrl += '&fromGame=1'
            self.notify.info('Checking login status at: %s' % (loginStatusUrl,))
            self.statusRF = Ramfile()
            self.loginStatusRequest = self.httpClient.makeChannel(False)
            self.loginStatusRequest.beginGetDocument(DocumentSpec(loginStatusUrl))
            self.loginStatusRequest.downloadToRam(self.statusRF)
        
        if self.loginStatusRequest.run():
            return task.again
        
        requestData = ''
        if self.loginStatusRequest.isValid() and self.loginStatusRequest.isDownloadComplete():
            requestData = self.statusRF.getData()
            self.statusRF = None
        else:
            self.notify.info('LoginStatus check failed: %s' % (self.loginStatusRequest.getStatusString(),))
            self.loginStatusRequest = None
            return task.again
        results = { }
        for line in requestData.split('\n'):
            pair = line.split('=', 1)
            if len(pair) == 2:
                results[pair[0].strip()] = pair[1].strip()
                continue
        
        self.queueStatus = results.get('LOGIN_ACTION', None)
        if self.queueStatus == 'PLAY':
            self._setQueueComplete()
            return task.done
        
        if self.queueStatus != 'QUEUE':
            self.notify.warning('Received invalid LOGIN_ACTION: %s' % (self.queueStatus,))
            sys.exit(1)
        
        loginTokenKey = config.GetString('queueing-token-2', 'SESSION_TOKEN')
        self.notify.info('using queueing token 2 of %s' % loginTokenKey)
        self.loginToken = results.get(loginTokenKey, self.loginToken)
        self.queueFreqSeconds = int(results.get('QUEUE_FREQ_SECONDS', '10'))
        self.queueUrl = results.get('QUEUE_URL', None)
        if not (self.loginToken) or not (self.queueUrl):
            self.notify.warning('No login token or queueUrl, trying again:')
            self.loginStatusRequest = None
            return task.again
        
        if config.GetBool('server-queueing-force', 0):
            self.notify.info('forcing queue')
            self.forceQueueStr = '&wannaqueue=1'
            
            def clearForceQueue(task = None):
                if self.forceQueueStr:
                    self.notify.info('clearing force queue')
                    self.forceQueueStr = ''
                else:
                    self.notify.info('setting force queue')
                    self.forceQueueStr = '&wannaqueue=1'
                    self._setQueueNotComplete()

            self.accept('f1', clearForceQueue)
        else:
            self.forceQueueStr = ''
        self._startQueueTask()
        return task.done

    
    def _stopLoginStatusTask(self):
        self._stopQueueTask()
        self.httpClient = None
        self.loginStatusRequest = None
        if self.loginStatusTask:
            taskMgr.remove(self.loginStatusTask)
            self.loginStatusTask = None
        

    
    def _startQueueTask(self):
        self.notify.info('Checking queue status...')
        self.queueRequest = None
        self.queueTask = taskMgr.add(self._checkQueue, 'AvatarChooser-CheckQueue')

    
    def _checkQueue(self, task):
        if not self.queueRequest:
            self.notify.info('Checking queue status at: %s' % (self.queueUrl + self.forceQueueStr,))
            self.queueRequest = self.httpClient.makeChannel(False)
            self.queueRequest.beginGetDocument(DocumentSpec(self.queueUrl + self.forceQueueStr))
            self.statusRF = Ramfile()
            self.queueRequest.downloadToRam(self.statusRF)
            task.delayTime = 0.10000000000000001
        
        if self.queueRequest.run():
            return task.again
        
        requestData = ''
        if self.queueRequest.isValid() and self.queueRequest.isDownloadComplete():
            self.notify.info('CheckQueue download complete')
            requestData = self.statusRF.getData()
            self.statusRF = None
        else:
            self.notify.info('CheckQueue check failed: %s' % (self.loginStatusRequest.getStatusString(),))
            self.queueRequest = None
            return task.again
        task.delayTime = self.queueFreqSeconds
        results = { }
        for line in requestData.split('\n'):
            pair = line.split('=', 1)
            if len(pair) == 2:
                results[pair[0].strip()] = pair[1].strip()
                continue
        
        userError = results.get('USER_ERROR', None)
        if userError:
            self.notify.warning('Received USER_ERROR: %s fetching queue status' % (userError,))
            sys.exit(1)
        
        self.queueStatus = results.get('QUEUE_ACTION', None)
        if self.queueStatus == 'PLAY':
            self._setQueueComplete()
            return task.done
        
        if self.queueStatus != 'QUEUE':
            self.notify.warning('Received invalid QUEUE_ACTION: %s' % (self.queueStatus,))
            sys.exit(1)
        
        self.notify.info('Queue not ready.  Next check in %s seconds...' % (self.queueFreqSeconds,))
        self.queueRequest = None
        return task.again

    
    def _setQueueComplete(self):
        self.notify.info('Queueing is complete!')
        self.queueTask = None
        self.queueComplete = True
        self._AvatarChooser__activatePlayButton()
        self._AvatarChooser__activateCreateButtons()

    
    def _setQueueNotComplete(self):
        self.notify.info('Queueing is not complete!')
        self.queueComplete = False
        self._AvatarChooser__deactivatePlayButton()
        self._AvatarChooser__deactivateCreateButtons()
        if not taskMgr.hasTaskNamed('AvatarChooser-CheckQueue'):
            self._startQueueTask()
        

    
    def _stopQueueTask(self):
        self.queueRequest = None
        if self.queueTask:
            taskMgr.remove(self.queueTask)
            self.queueTask = None
        

    
    def _AvatarChooser__handleDelete(self):
        if self.deleteConfirmDialog:
            self.deleteConfirmDialog.destroy()
        
        (subId, slot) = self.choice
        potAv = base.cr.avList[subId][slot]
        name = potAv.dna.getDNAName()
        self.blockInput()
        self.deleteConfirmDialog = PDialog.PDialog(text = PLocalizer.AvatarChooserConfirmDelete % name, style = OTPDialog.YesNo, command = self._AvatarChooser__handleDeleteConfirmation)

    
    def _AvatarChooser__handleDeleteConfirmation(self, value):
        self.deleteConfirmDialog.destroy()
        self.deleteConfirmDialog = None
        if value == DGG.DIALOG_OK:
            (subId, slot) = self.choice
            potAv = base.cr.avList[subId][slot]
            self.notify.info('AvatarChooser: request delete slot: %s avId: %s subId: %s' % (slot, potAv.id, subId))
            self.accept('rejectRemoveAvatar', self._AvatarChooser__rejectRemoveAvatar)
            self.accept('removeAvatarResponse', self._AvatarChooser__removeAvatarResponse)
            base.cr.avatarManager.sendRequestRemoveAvatar(potAv.id, subId, 'delete')
            base.cr.waitForDatabaseTimeout(requestName = 'WaitForDeleteAvatarResponse')
            self.blockInput()
        else:
            self.allowInput()

    
    def _AvatarChooser__handleShareConfirmation(self, value):
        self.shareConfirmDialog.destroy()
        self.shareConfirmDialog = None
        if value == DGG.DIALOG_OK:
            (subId, slot) = self.choice
            potAv = base.cr.avList[subId][slot]
            self.notify.info('AvatarChooser: request share slot: %s avId: %s subId: %s' % (slot, potAv.id, subId))
            self.accept('rejectShareAvatar', self._AvatarChooser__rejectShareAvatar)
            self.accept('shareAvatarResponse', self._AvatarChooser__shareAvatarResponse)
            if potAv.shared:
                wantShared = 0
            else:
                wantShared = 1
            base.cr.avatarManager.sendRequestShareAvatar(potAv.id, subId, wantShared)
            base.cr.waitForDatabaseTimeout(requestName = 'WaitForShareAvatarResponse')
            self.blockInput()
        else:
            self.allowInput()

    
    def _AvatarChooser__removeAvatarResponse(self, avatarId, subId):
        self.ignore('rejectRemoveAvatar')
        self.ignore('removeAvatarResponse')
        base.cr.cleanupWaitingForDatabase()
        base.cr.sendGetAvatarsMsg()

    
    def _AvatarChooser__rejectRemoveAvatar(self, reasonId):
        self.notify.warning('rejectRemoveAvatar: %s' % reasonId)
        self.ignore('rejectRemoveAvatar')
        self.ignore('removeAvatarResponse')
        base.cr.cleanupWaitingForDatabase()
        self.allowInput()

    
    def updateAvatarList(self):
        self._AvatarChooser__hideHighlightedAvatar()
        self._AvatarChooser__createAvatarButtons()
        self.subIds = base.cr.avList.keys()
        self.subIds.sort()
        if self.currentSubId not in self.subIds:
            self.notify.warning('subId %s is no longer in family: %s' % (self.currentSubIndex, self.subIds))
            self.currentSubIndex = 0
        
        self.showSub(self.currentSubIndex)
        subAvs = base.cr.avList[self.currentSubId]
        if len(subAvs) > 0 and subAvs[0] not in (OTPGlobals.AvatarSlotUnavailable, OTPGlobals.AvatarSlotAvailable, OTPGlobals.AvatarPendingCreate):
            self._AvatarChooser__handleHighlight(self.currentSubId, 0)
        
        if not self.handleDialogOnScreen:
            self.allowInput()
        

    
    def _AvatarChooser__handleOptions(self):
        if self.gameOptions is not None:
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
        self.currentSubId = self.subIds[self.currentSubIndex]
        subAccess = base.cr.accountDetailRecord.subDetails[self.currentSubId].subAccess
        self.gameOptions = GameOptions('Game Options', x, y, width, height, base.options, access = subAccess, chooser = self)
        self.gameOptions.show()

    
    def _AvatarChooser__handleQuit(self):
        self.doneStatus = {
            'mode': 'exit' }
        messenger.send(self.doneEvent, [
            self.doneStatus])

    
    def _AvatarChooser__handleUpgrade(self):
        base.cr.centralLogger.writeClientEvent('Upgrade button pressed on Pick-A-Pirate screen')
        base.popupBrowser('http://piratesonline.go.com/#/account_services/membership_options.html', True)

    
    def _AvatarChooser__handleLogoutWithoutConfirm(self):
        base.cr.loginFSM.request('login')

    
    def _AvatarChooser__shipRockTask(self, task):
        h = self.shipRoot.getH()
        p = 1.5 * math.sin(task.time * 0.90000000000000002)
        r = 1.5 * math.cos(task.time * 1.1000000000000001) + 1.5 * math.cos(task.time * 1.8)
        self.shipRoot.setHpr(h, p, r)
        return Task.cont

    
    def blockInput(self):
        color = Vec4(0.69999999999999996, 0.69999999999999996, 0.69999999999999996, 0.69999999999999996)
        for subButtons in self.subAvButtons.values():
            for button in subButtons:
                button['state'] = DGG.DISABLED
                button.setColorScale(color)
            
        
        self.renameButton['state'] = DGG.DISABLED
        self.renameButton.setColorScale(color)
        self.quitButton['state'] = DGG.DISABLED
        self.quitButton.setColorScale(color)
        self.logoutButton['state'] = DGG.DISABLED
        self.logoutButton.setColorScale(color)
        self.playButton['state'] = DGG.DISABLED
        self.playButton.setColorScale(color)
        if base.config.GetBool('allow-linked-accounts', 0):
            self.shareButton['state'] = DGG.DISABLED
            self.shareButton.setColorScale(color)
        
        self.deleteButton['state'] = DGG.DISABLED
        self.deleteButton.setColorScale(color)
        self.optionsButton['state'] = DGG.DISABLED
        self.optionsButton.setColorScale(color)
        self.upgradeButton['state'] = DGG.DISABLED
        self.upgradeButton.setColorScale(color)
        if base.config.GetBool('allow-linked-accounts', 0):
            self.nextSubButton['state'] = DGG.DISABLED
            self.nextSubButton.setColorScale(color)
            self.prevSubButton['state'] = DGG.DISABLED
            self.prevSubButton.setColorScale(color)
        

    
    def allowInput(self):
        for subButtons in self.subAvButtons.values():
            for button in subButtons:
                if button['text']:
                    button['state'] = DGG.NORMAL
                else:
                    button['state'] = DGG.DISABLED
                button.clearColorScale()
            
        
        self.renameButton['state'] = DGG.NORMAL
        self.renameButton.clearColorScale()
        if not self.disableQuit:
            self.quitButton['state'] = DGG.NORMAL
            self.quitButton.clearColorScale()
        
        self.logoutButton['state'] = DGG.NORMAL
        self.logoutButton.clearColorScale()
        self.playButton['state'] = DGG.NORMAL
        self.playButton.clearColorScale()
        if base.config.GetBool('allow-linked-accounts', 0):
            self.shareButton['state'] = DGG.NORMAL
            self.shareButton.clearColorScale()
        
        self.deleteButton['state'] = DGG.NORMAL
        self.deleteButton.clearColorScale()
        self.upgradeButton['state'] = DGG.NORMAL
        self.upgradeButton.clearColorScale()
        if not self.disableOptions:
            self.optionsButton['state'] = DGG.NORMAL
            self.optionsButton.clearColorScale()
        
        if base.config.GetBool('allow-linked-accounts', 0):
            self.nextSubButton['state'] = DGG.NORMAL
            self.nextSubButton.clearColorScale()
            self.prevSubButton['state'] = DGG.NORMAL
            self.prevSubButton.clearColorScale()
        
        if self.choice == (0, 0):
            potAv = None
        else:
            (subId, slot) = self.choice
            potAv = base.cr.avList[subId][slot]
        if potAv and potAv not in (OTPGlobals.AvatarSlotUnavailable, OTPGlobals.AvatarSlotAvailable, OTPGlobals.AvatarPendingCreate):
            if not (potAv.online):
                if potAv.creator or not base.config.GetBool('allow-linked-accounts', 0):
                    self.deleteButton['state'] = DGG.NORMAL
                    if base.config.GetBool('allow-linked-accounts', 0):
                        self.shareButton['state'] = DGG.NORMAL
                    
                else:
                    self.deleteButton['state'] = DGG.DISABLED
                    if base.config.GetBool('allow-linked-accounts', 0):
                        self.shareButton['state'] = DGG.DISABLED
                    
            if potAv.online:
                self.playButton['state'] = DGG.DISABLED
            elif potAv.shared and potAv.creator or not base.config.GetBool('allow-linked-accounts', 0):
                self.playButton['state'] = DGG.NORMAL
            else:
                self.playButton['state'] = DGG.DISABLED
        
        if self.queueComplete == False:
            self._AvatarChooser__deactivatePlayButton()
            self._AvatarChooser__deactivateCreateButtons()
        

    
    def _AvatarChooser__handleFirstAdd(self, value):
        self.firstAddDialog.destroy()
        self.firstAddDialog = None
        self.allowInput()

    
    def _AvatarChooser__handleFinalize(self, value):
        (subId, slot) = self.choice
        self.notifications[slot].remove()
        del self.notifications[slot]
        self.finalizeConfirmDialog.destroy()
        self.finalizeConfirmDialog = None
        potAv = base.cr.avList[subId][slot]
        base.cr.avatarManager.sendRequestFinalize(potAv.id)
        potAv.name = potAv.wishName
        potAv.wishState = 'CLOSED'
        avButton = self.subAvButtons[subId][slot]
        avButton['text'] = potAv.name
        potAv.dna.setName(potAv.wishName)
        avButton.setText()
        self.allowInput()

    
    def _AvatarChooser__handleNotQueueComplete(self, value):
        self.notQueueCompleteDialog.destroy()
        self.notQueueCompleteDialog = None
        self.allowInput()

    
    def _AvatarChooser__handleNotDownload(self, value):
        self.notDownloadDialog.destroy()
        self.notDownloadDialog = None
        self.allowInput()

    
    def _AvatarChooser__handleDenied(self, value):
        (subId, slot) = self.choice
        self.notifications[slot].remove()
        del self.notifications[slot]
        self.deniedConfirmDialog.destroy()
        self.deniedConfirmDialog = None
        self.handleDialogOnScreen = 0
        self.allowInput()

    
    def enterNameMode(self):
        (subId, slot) = self.choice
        self.quitFrame.setColorScale(Vec4(1, 1, 1, 0))
        self.highlightFrame.setColorScale(Vec4(1, 1, 1, 0))
        self.avatarListFrame.setColorScale(Vec4(1, 1, 1, 0))
        base.camera.setX(-26)
        self.subFrame.hide()
        av = base.cr.avList[subId][slot]
        base.accept('q', self.exitNameMode)
        base.accept('NameGUIFinished', self.exitNameMode)
        self.renameButton.hide()
        self.nameGui = NameGUI.NameGUI(main = av, independent = True)
        self.nameGui.enter()

    
    def exitNameMode(self, value):
        (subId, slot) = self.choice
        if value == 1:
            if self.nameGui.customName:
                base.cr.avList[subId][slot].wishState = 'REQUESTED'
            else:
                potAv = base.cr.avList[subId][slot]
                potAv.name = self.nameGui._getName()
                potAv.wishState = 'CLOSED'
                avButton = self.subAvButtons[subId][slot]
                avButton['text'] = potAv.name
                potAv.dna.setName(potAv.name)
                avButton.setText()
            if self.notifications.get(slot, 0):
                self.notifications[slot].remove()
                del self.notifications[slot]
            
        else:
            self.renameButton.show()
        self.nameGui.unload()
        del self.nameGui
        base.ignore('q')
        base.ignore('NameGUIFinished')
        self.quitFrame.setColorScale(Vec4(1, 1, 1, 1))
        self.highlightFrame.setColorScale(Vec4(1, 1, 1, 1))
        self.avatarListFrame.setColorScale(Vec4(1, 1, 1, 1))
        base.camera.setX(-29)
        self.subFrame.show()

    
    def placeNotification(self, slot, pos, style):
        notification = self.exclam.copyTo(self.avatarListFrame)
        self.notifications[slot] = notification
        notification.setPos(pos[0], pos[1], pos[2])
        notification.setScale(0.14000000000000001)
        notification.setR(25)

    
    def changeSub(self, delta):
        self.showSub(self.currentSubIndex + delta)

    
    def showSub(self, index):
        if self.subIds[self.currentSubIndex]:
            numAvs = len(self.subAvButtons[self.subIds[self.currentSubIndex]])
            for slot in range(0, numAvs):
                if self.notifications.get(slot, 0):
                    self.notifications[slot].remove()
                    del self.notifications[slot]
                    continue
            
        
        self.currentSubIndex = index
        numSubs = len(self.subIds)
        if self.currentSubIndex <= 0:
            self.currentSubIndex = 0
            if base.config.GetBool('allow-linked-accounts', 0):
                self.prevSubButton.hide()
            
        elif base.config.GetBool('allow-linked-accounts', 0):
            self.prevSubButton.show()
        
        if self.currentSubIndex >= numSubs - 1:
            self.currentSubIndex = numSubs - 1
            if base.config.GetBool('allow-linked-accounts', 0):
                self.nextSubButton.hide()
            
        elif base.config.GetBool('allow-linked-accounts', 0):
            self.nextSubButton.show()
        
        self.currentSubId = self.subIds[self.currentSubIndex]
        subName = base.cr.accountDetailRecord.subDetails[self.currentSubId].subName
        subAccess = base.cr.accountDetailRecord.subDetails[self.currentSubId].subAccess
        subAccessStr = PLocalizer.AccessLevel[subAccess]
        subLabelText = '\x01white\x01%s\x02\n\x01smallCaps\x01%s\x02' % (subName, subAccessStr)
        self.subLabel['text'] = subLabelText
        for frame in self.subFrames.values():
            frame.hide()
        
        self.subFrames[self.currentSubId].show()
        anyAvatars = False
        for avList in base.cr.avList.values():
            for av in avList:
                if av not in (OTPGlobals.AvatarSlotUnavailable, OTPGlobals.AvatarSlotAvailable, OTPGlobals.AvatarPendingCreate):
                    anyAvatars = True
                    break
                    continue
            
            if anyAvatars:
                break
                continue
        
        avList = base.cr.avList[self.currentSubId]
        for avIdx in range(0, len(avList)):
            if avList[avIdx] not in (OTPGlobals.AvatarSlotUnavailable, OTPGlobals.AvatarSlotAvailable, OTPGlobals.AvatarPendingCreate):
                if avList[avIdx].wishState == 'APPROVED':
                    self.placeNotification(avIdx, (0.32000000000000001, 0, -0.37 - avIdx * 0.095000000000000001), APPROVED)
                elif avList[avIdx].wishState == 'DENIED' or avList[avIdx].wishState == 'OPEN':
                    self.placeNotification(avIdx, (0.32000000000000001, 0, -0.37 - avIdx * 0.095000000000000001), DENIED)
                
            avList[avIdx].wishState == 'OPEN'
        
        if anyAvatars:
            self.avatarListFrame.reparentTo(base.a2dTopLeft)
            self.avatarListFrame.setPosHprScale(0.41999999999999998, 0, -0.29999999999999999, 0, 0, 0, 1, 1, 1)
        else:
            self.avatarListFrame.reparentTo(base.a2dTopCenter)
            self.avatarListFrame.setPosHprScale(0, 0, -0.29999999999999999, 0, 0, 0, 1.1000000000000001, 1.1000000000000001, 1.1000000000000001)
            self.renameButton.hide()
            self.shardPanel.hide()
            self.shardPanelBottom.hide()
        subAvs = base.cr.avList[self.currentSubId]
        if len(subAvs) > 0 and subAvs[0] not in (OTPGlobals.AvatarSlotUnavailable, OTPGlobals.AvatarSlotAvailable, OTPGlobals.AvatarPendingCreate):
            self._AvatarChooser__handleHighlight(self.currentSubId, 0)
        else:
            self._AvatarChooser__hideHighlightedAvatar()

    
    def popupTrialPanel(self):
        if not self.trialNonPayerPanel:
            self.trialNonPayerPanel = TrialNonPayerPanel.TrialNonPayerPanel(trial = True)
        
        self.trialNonPayerPanel.show()

    
    def popupFeatureBrowser(self, subId, slot):
        if not self.nonPayerPanel:
            self.nonPayerPanel = TrialNonPayerPanel.TrialNonPayerPanel(trial = False)
            self.nonPayerPanel.fullText['text'] = PLocalizer.VR_FeaturePopLongTextAvatars
        
        self.nonPayerPanel.show()

    
    def _stopMouseReadTask(self):
        taskMgr.remove('AvatarChooser-MouseRead')

    
    def _startMouseReadTask(self):
        self._stopMouseReadTask()
        mouseData = base.win.getPointer(0)
        self.lastMousePos = (mouseData.getX(), mouseData.getY())
        taskMgr.add(self._mouseReadTask, 'AvatarChooser-MouseRead')

    
    def _mouseReadTask(self, task):
        if not base.mouseWatcherNode.hasMouse():
            pass
        1
        winSize = (base.win.getXSize(), base.win.getYSize())
        mouseData = base.win.getPointer(0)
        if mouseData.getX() > winSize[0] or mouseData.getY() > winSize[1]:
            pass
        1
        dx = mouseData.getX() - self.lastMousePos[0]
        mouseData = base.win.getPointer(0)
        self.lastMousePos = (mouseData.getX(), mouseData.getY())
        if self.av:
            value = self.av.getH()
            value = (value + dx * 0.69999999999999996) % 360
            self._AvatarChooser__rotateHighlightedAvatar(value)
        
        return Task.cont


