# File: L (Python 2.4)

import math
import copy
import types
import random
from direct.showbase.ShowBaseGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase.PythonUtil import *
from direct.directnotify import DirectNotifyGlobal
from direct.controls import ControlManager
from direct.interval.IntervalGlobal import *
from direct.controls import BattleWalker
from direct.actor import Actor
from direct.showbase.InputStateGlobal import inputState
from direct.distributed.ClockDelta import *
from direct.showbase.ShadowPlacer import ShadowPlacer
from direct.fsm.StatePush import StateVar
from otp.avatar.LocalAvatar import LocalAvatar
from otp.avatar import PositionExaminer
from otp.otpbase import OTPGlobals
from otp.speedchat import SCDecoders
from otp.otpgui import OTPDialog
from pirates.audio import SoundGlobals
from pirates.piratesgui import PDialog
from pirates.battle import WeaponGlobals
from pirates.battle import DistributedBattleAvatar
from pirates.chat.PiratesChatManager import PiratesChatManager
from pirates.chat.PTalkAssistant import PTalkAssistant
from pirates.ship import ShipGlobals
from pirates.piratesgui import GuiManager
from pirates.piratesgui import PiratesGuiGlobals
from pirates.tutorial import ChatTutorial
from pirates.tutorial import ChatTutorialAlt
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import EmoteGlobals
from pirates.reputation import ReputationGlobals
from pirates.battle import RangeDetector
from pirates.battle import BattleSkillDiary
from pirates.movement.CameraFSM import CameraFSM
from pirates.economy.EconomyGlobals import *
from pirates.economy import EconomyGlobals
from pirates.piratesbase import TeamUtils
from pirates.piratesbase import UserFunnel
from pirates.ship import DistributedSimpleShip
from pirates.instance import DistributedMainWorld
from pirates.world import DistributedGameArea
from pirates.world import OceanZone
from pirates.interact import InteractiveBase
from pirates.effects.CloudScud import CloudScud
from pirates.effects.ProtectionSpiral import ProtectionSpiral
from pirates.battle.EnemySkills import EnemySkills
from pirates.inventory import InventoryGlobals
from pirates.inventory.InventoryGlobals import Locations
from direct.controls.GhostWalker import GhostWalker
from direct.controls.PhysicsWalker import PhysicsWalker
from direct.controls.ObserverWalker import ObserverWalker
from pirates.movement.PiratesGravityWalker import PiratesGravityWalker
from pirates.movement.PiratesSwimWalker import PiratesSwimWalker
from pirates.quest import QuestDB
from pirates.quest import QuestStatus
from pirates.world.LocationConstants import LocationIds, getParentIsland
from pirates.world import WorldGlobals
from pirates.map.MinimapObject import GridMinimapObject
from pirates.pirate import TitleGlobals
from pirates.uberdog.UberDogGlobals import InventoryCategory, InventoryType
from pirates.uberdog.DistributedInventoryBase import DistributedInventoryBase
import Pirate
import LocalPirateGameFSM
from DistributedPlayerPirate import DistributedPlayerPirate
from pirates.pirate import PlayerStateGlobals
from pirates.pirate import AvatarTypes
from pirates.makeapirate import ClothingGlobals
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from pirates.inventory import ItemGlobals
from direct.task.Task import Task
from pirates.effects.PooledEffect import PooledEffect
from pirates.piratesgui.GameOptions import Options
from pirates.piratesgui import MessageGlobals
from pirates.piratesbase import TODGlobals
from direct.gui import OnscreenText
globalClock = ClockObject.getGlobalClock()
if base.config.GetBool('want-pstats', 0):
    import profile
    import pstats


class bp:
    loginCfg = bpdb.bpGroup(iff = False, cfg = 'loginCfg', static = 1)

from direct.controls.ControlManager import ControlManager
if base.config.GetBool('want-custom-keys', 0):
    ControlManager.wantCustomKeys = 1
    ControlManager.wantWASD = 0
else:
    ControlManager.wantCustomKeys = 0
    ControlManager.wantWASD = 1

class LocalPirate(DistributedPlayerPirate, LocalAvatar):
    notify = DirectNotifyGlobal.directNotify.newCategory('LocalPirate')
    neverDisable = 1
    
    def __init__(self, cr):
        
        try:
            pass
        except:
            self.LocalPirate_initialized = 1
            DistributedPlayerPirate.__init__(self, cr)
            self.masterHuman = base.cr.humanHigh
            chatMgr = PiratesChatManager()
            talkAssistant = PTalkAssistant()
            LocalAvatar.__init__(self, cr, chatMgr, talkAssistant = talkAssistant)
            self.gameFSM = None
            self.equippedWeapons = []
            self.monstrousTarget = None
            self.distanceToTarget = 0
            self._LocalPirate__lootUIEnabled = True
            self.missedLootInformation = []
            self.setLocalAvatarUsingWeapon(1)
            self.cameraFSM = CameraFSM(self)
            self.guiMgr = GuiManager.GuiManager(self)
            self.interestHandles = []
            if base.config.GetBool('debug-local-animMixer', 0):
                self.animMixer.setVerbose(True)
            
            self.currentMouseOver = None
            self.currentAimOver = None
            self.currentSelection = None
            self.tutObject = None
            self.currentDialogMovie = None
            self.ship = None
            self.shipList = set()
            self.cannon = None
            self._LocalPirate__turboOn = 0
            self._LocalPirate__marioOn = 0
            self.speedIndex = 0
            self.curMoveSound = None
            self.setupMovementSounds()
            self.rangeDetector = RangeDetector.RangeDetector()
            self.rangeDetector.detachNode()
            self.showQuest = True
            self.currentOcean = 0
            self.soundWhisper = loadSfx(SoundGlobals.SFX_GUI_WHISPER)
            self.positionExaminer = PositionExaminer.PositionExaminer()
            self.skillDiary = BattleSkillDiary.BattleSkillDiary(self.cr, self)
            self.lookAtTarget = None
            self.lookAtTimer = None
            self.lookAtDummy = self.attachNewNode('lookAtDummy')
            self.lookFromNode = self.attachNewNode('lookFromTargetHelper')
            self.lookFromNode.setZ(self.getHeight())
            self.lookToNode = NodePath('lookToTargetHelper')
            if base.config.GetBool('want-dev', False):
                self.accept('shift-f12', self.toggleAvVis)
            
            self.money = 0
            self.firstMoneyQuieted = 0
            self.enableAutoRun = 0
            self.kickEvents = None
            self.battleTeleportFlagTask = None
            self.openJailDoorTrack = None
            self.currentStoryQuests = []
            self.cloudScudEffect = None
            self.soloInteraction = False
            self.emoteAccess = []
            self.AFKDelay = base.config.GetInt('afk-delay', 600)
            self.playRewardAnimation = None
            self.localProjectiles = []
            self._cannonAmmoSkillId = InventoryType.CannonRoundShot
            self._siegeTeamSV = StateVar(0)
            self.guildPopupDialog = None
            self.moralePopupDialog = None
            self.gmNameTagEnabledLocal = 0
            self.gmNameTagStringLocal = ''
            self.gmNameTagColorLocal = ''
            soundEffects = [
                SoundGlobals.SFX_MONSTER_JR_LAUGH_01,
                SoundGlobals.SFX_MONSTER_JR_LAUGH_02,
                SoundGlobals.SFX_MONSTER_JR_ENJOY,
                SoundGlobals.SFX_MONSTER_JR_SUBMIT,
                SoundGlobals.SFX_MONSTER_JR_JOIN]
            self.jollySfx = loadSfx(random.choice(soundEffects))
            self.currCombatMusic = None
            self.clothingUpdateTaskName = 'inventoryClothingUpdate'
            self.clothingUpdatePending = 0
            self.sailHit = 0
            self.playersNearby = { }
            self.trackedRotation = []
            self.trackedTurning = 0
            self.lastCannonShot = globalClock.getFrameTime()
            self.pendingInitQuest = None
            self.inInvasion = False
            self.levelFootStep = None
            self.wobbleList = []
            self.fovIval = None
            self.lockRegenFlag = 0
            self.everBeenGhost = 0
            self.mistimedAttack = 0
            if base.config.GetBool('want-easy-combos', 1):
                self.wantComboTiming = 0
            else:
                self.wantComboTiming = 1
            self.zombieEffect = None
            self.zombieIval = None
            self.defenceEffects = { }
            self.skillSfxIval = None
            self.currentWeaponSlotId = 1
            if base.config.GetBool('want-pstats', 0):
                self.pstatsGen = PStatCollector('Battle Avatars:Avatar Generating')
                self.pstatsLoad = PStatCollector('Battle Avatars:Loading Asset')
                self.pstatsFPS = PStatCollector('Battle Avatars:fps')
                self.lastTime = None
                taskMgr.add(self.logPStats, 'avatarPstats')
            
            self.fishingGameHook = None
            self.accept('shipRemoved', self.checkHaveShip)
            self.rocketOn = 0
            if base.config.GetBool('want-rocketman', 0):
                self.startRocketJumpMode()
            
            self.dialogProp = None
            self.duringDialog = False
            self.efficiency = False
            self.boardedShip = False
            self.shipLookAhead = 1


    
    def setShipLookAhead(self, value):
        self.shipLookAhead = value

    
    def startRocketJumpMode(self):
        self.oldGravity = None
        self.accept('space', self.moveUpStart)
        self.accept('space-up', self.moveUpEnd)
        self.rocketOn = 1

    
    def endRocketJumpMode(self):
        self.moveUpEnd()
        self.ignore('space')
        self.ignore('space-up')
        self.rocketOn = 0

    
    def moveUpEnd(self):
        taskMgr.remove('rocketDelayTask')
        if self.oldGravity != None:
            if self.oldGravity and 0:
                self.controlManager.get('walk').lifter.setGravity(self.oldGravity)
            else:
                self.controlManager.get('walk').lifter.setGravity(32.173999999999999 * 2.0)
            self.oldGravity = None
        

    
    def moveUpStart(self):
        self.lastJumpTime = None
        self.jumpStartTime = globalClock.getFrameTime()
        self.oldGravity = self.controlManager.get('walk').lifter.getGravity()
        if self.controlManager.get('walk').lifter.isOnGround():
            taskMgr.doMethodLater(0.5, self.rocketGrav, 'rocketDelayTask')
        else:
            self.rocketGrav()

    
    def rocketGrav(self, task = None):
        self.controlManager.get('walk').lifter.setGravity(-32.173999999999999)
        if task:
            return task.done
        

    
    def sendUpdate(self, *args, **kw):
        if self.isGenerated():
            return DistributedPlayerPirate.sendUpdate(self, *args, **args)
        

    
    def logPStats(self, task):
        self.pstatsGen.setLevel(taskMgr.mgr.findTaskChain('background').getNumTasks() + 0)
        self.pstatsLoad.setLevel(taskMgr.mgr.findTaskChain('loader').getNumTasks() + 0)
        if self.lastTime == None:
            self.lastTime = globalClock.getRealTime()
        
        timeDelta = globalClock.getRealTime() - self.lastTime
        self.lastTime = globalClock.getRealTime()
        if timeDelta <= 0.0:
            fps = 0.0
        else:
            fps = 1.0 / timeDelta
        self.pstatsFPS.setLevel(fps)
        return task.cont

    
    def setupWalkControls(self, avatarRadius = 1.3999999999999999, floorOffset = OTPGlobals.FloorOffset, reach = 4.0, wallBitmask = OTPGlobals.WallBitmask, floorBitmask = OTPGlobals.FloorBitmask, ghostBitmask = OTPGlobals.GhostBitmask):
        walkControls = PiratesGravityWalker(gravity = 32.173999999999999 * 2.0)
        walkControls.setWallBitMask(wallBitmask)
        walkControls.setFloorBitMask(floorBitmask)
        walkControls.initializeCollisions(self.cTrav, self, avatarRadius, floorOffset, reach)
        walkControls.setAirborneHeightFunc(self.getAirborneHeight)
        self.controlManager.add(walkControls, 'walk')
        self.physControls = walkControls
        swimControls = PiratesSwimWalker()
        swimControls.setWallBitMask(wallBitmask)
        swimControls.setFloorBitMask(floorBitmask)
        swimControls.initializeCollisions(self.cTrav, self, avatarRadius, floorOffset, 4.0)
        swimControls.setAirborneHeightFunc(self.getAirborneHeight)
        self.controlManager.add(swimControls, 'swim')
        ghostControls = GhostWalker()
        ghostControls.setWallBitMask(ghostBitmask)
        ghostControls.setFloorBitMask(floorBitmask)
        ghostControls.initializeCollisions(self.cTrav, self, avatarRadius, floorOffset, reach)
        ghostControls.setAirborneHeightFunc(self.getAirborneHeight)
        self.controlManager.add(ghostControls, 'ghost')
        observerControls = ObserverWalker()
        observerControls.setWallBitMask(ghostBitmask)
        observerControls.setFloorBitMask(floorBitmask)
        observerControls.initializeCollisions(self.cTrav, self, avatarRadius, floorOffset, reach)
        observerControls.setAirborneHeightFunc(self.getAirborneHeight)
        self.controlManager.add(observerControls, 'observer')
        self.controlManager.use('walk', self)
        self.controlManager.disable()

    
    def respondShipUpgrade(self, shipId, retCode):
        if retCode:
            messenger.send('ShipUpgraded', [
                shipId,
                retCode])
            base.localAvatar.guiMgr.queueInstructionMessageFront(PLocalizer.ShipUpgradeComplete, [], None, 1.0, messageCategory = MessageGlobals.MSG_CAT_PURCHASE)
        else:
            messenger.send('ShipUpgraded', [
                shipId,
                retCode])
            base.localAvatar.guiMgr.queueInstructionMessageFront(PLocalizer.ShipUpgradeFailed, [], None, 1.0, messageCategory = MessageGlobals.MSG_CAT_PURCHASE_FAILED)

    
    def createGameFSM(self):
        self.gameFSM = LocalPirateGameFSM.LocalPirateGameFSM(self)

    
    def updateReputation(self, category, value):
        DistributedPlayerPirate.updateReputation(self, category, value)
        self.guiMgr.updateReputation(category, value)

    
    def playSkillMovie(self, skillId, ammoSkillId, skillResult, charge = 0, targetId = 0, areaIdList = []):
        if WeaponGlobals.getSkillTrack(skillId) == WeaponGlobals.BREAK_ATTACK_SKILL_INDEX:
            self.skillDiary.clearHits(skillId)
            self.guiMgr.combatTray.clearSkillCharge(skillId)
        else:
            self.skillDiary.startRecharging(skillId, ammoSkillId)
        if WeaponGlobals.getSkillTrack(skillId) == WeaponGlobals.DEFENSE_SKILL_INDEX:
            if skillId == EnemySkills.MISC_VOODOO_REFLECT:
                self.showEffectString(PLocalizer.AttackReflected)
            else:
                self.showEffectString(PLocalizer.AttackBlocked)
            self.guiMgr.combatTray.startSkillRecharge(skillId)
        
        if skillId in (EnemySkills.STAFF_TOGGLE_AURA_WARDING, EnemySkills.STAFF_TOGGLE_AURA_NATURE, EnemySkills.STAFF_TOGGLE_AURA_DARK):
            if self.getAuraActivated():
                skillId = EnemySkills.STAFF_TOGGLE_AURA_OFF
            
        
        DistributedPlayerPirate.playSkillMovie(self, skillId, ammoSkillId, skillResult, charge, targetId, areaIdList)

    
    def sendRequestMAPClothes(self, clothes):
        self.sendUpdate('requestMAPClothes', [
            clothes])

    
    def lockRegen(self):
        self.lockRegenFlag = 1

    
    def unlockAndRegen(self, force = True):
        self.lockRegenFlag = 0
        if self.needRegenFlag or force:
            self.cueRegenerate(force = 1)
        

    
    def cueRegenerate(self, force = 0):
        if (self.clothingUpdatePending or self.lockRegenFlag) and not force:
            self.needRegenFlag = 1
            return None
        
        DistributedPlayerPirate.cueRegenerate(self)

    
    def doRegeneration(self):
        if not self.lockRegenFlag:
            DistributedPlayerPirate.doRegeneration(self)
            messenger.send('localAv-regenerate')
        

    
    def wearJewelry(self, itemToWear, location, remove = None):
        if remove:
            self.tryOnJewelry(None, location)
        else:
            self.tryOnJewelry(itemToWear, location)
        taskMgr.remove(self.clothingUpdateTaskName)
        task = taskMgr.doMethodLater(5.0, self.sendClothingUpdate, self.clothingUpdateTaskName)
        self.clothingUpdatePending = 1

    
    def wearItem(self, itemToWear, location, remove = None):
        if remove:
            self.removeClothes(location)
        else:
            self.tryOnClothes(location, itemToWear.itemTuple)
        taskMgr.remove(self.clothingUpdateTaskName)
        task = taskMgr.doMethodLater(5.0, self.sendClothingUpdate, self.clothingUpdateTaskName)
        self.clothingUpdatePending = 1

    
    def wearTattoo(self, itemToWear, location, remove = None):
        if remove:
            self.tryOnTattoo(None, location)
        else:
            self.tryOnTattoo(itemToWear, location)
        taskMgr.remove(self.clothingUpdateTaskName)
        task = taskMgr.doMethodLater(5.0, self.sendClothingUpdate, self.clothingUpdateTaskName)
        self.clothingUpdatePending = 1

    
    def sendClothingUpdate(self, args = None):
        self.sendUpdate('requestChangeClothes', [])
        self.clothingUpdatePending = 0

    
    def checkForWeaponInSlot(self, weaponId, slot):
        inventory = localAvatar.getInventory()
        if slot == -1:
            return 1
        
        if inventory:
            weaponInSlot = inventory.getLocatables().get(slot)
            if weaponInSlot and weaponInSlot[1] == weaponId:
                return weaponInSlot[1]
            else:
                return None
        

    
    def getWeaponFromSlot(self, slot):
        inventory = localAvatar.getInventory()
        if inventory:
            weaponInSlot = inventory.getLocatables().get(slot)
            if weaponInSlot and weaponInSlot[1]:
                return weaponInSlot[1]
            else:
                return None
        

    
    def toggleWeapon(self, newWeaponId, slotId, fromWheel = 0):
        switchWeaponStates = [
            'LandRoam',
            'Battle',
            'WaterRoam',
            'Dialog']
        if self.getGameState() not in switchWeaponStates:
            return None
        
        if self.belongsInJail():
            return None
        
        if self.guiMgr.mainMenu and not self.guiMgr.mainMenu.isHidden():
            return None
        
        if not self.checkForWeaponInSlot(newWeaponId, slotId):
            return None
        
        newSlot = self.currentWeaponSlotId != slotId
        self.currentWeaponSlotId = slotId
        if (newWeaponId != self.currentWeaponId or newSlot) and self.isWeaponDrawn:
            self.d_requestCurrentWeapon(newWeaponId, 1)
            self.l_setCurrentWeapon(newWeaponId, 1, slotId)
            self.b_setGameState('Battle')
        elif not (self.isWeaponDrawn) and fromWheel:
            self.d_requestCurrentWeapon(newWeaponId, 1)
            self.l_setCurrentWeapon(newWeaponId, 1, slotId)
            self.b_setGameState('Battle')
        elif not self.isWeaponDrawn:
            self.d_requestCurrentWeapon(newWeaponId, 1)
            self.l_setCurrentWeapon(newWeaponId, 1, slotId)
            self.b_setGameState('Battle')
            messenger.send('weaponEquipped')
        else:
            self.d_requestCurrentWeapon(newWeaponId, 0)
            self.l_setCurrentWeapon(newWeaponId, 0, slotId)
            self.b_setGameState('LandRoam')
            messenger.send('weaponSheathed')

    
    def putWeaponAway(self):
        if self.isWeaponDrawn:
            self.d_requestCurrentWeapon(self.currentWeaponId, 0)
            self.l_setCurrentWeapon(self.currentWeaponId, 0, self.currentWeaponSlotId)
            self.b_setGameState('LandRoam')
            messenger.send('weaponSheathed')
        

    
    def setCurrentWeapon(self, currentWeaponId, isWeaponDrawn):
        pass

    
    def l_setCurrentWeapon(self, currentWeaponId, isWeaponDrawn, slotId):
        if not self.gameFSM.isInTransition() and self.getGameState() in [
            'WaterRoam',
            'WaterTreasureRoam']:
            return None
        
        if self.currentWeaponId != currentWeaponId or self.isWeaponDrawn != isWeaponDrawn:
            DistributedPlayerPirate.sendRequestRemoveEffects(self, self.stickyTargets)
            self.setStickyTargets([])
            taskMgr.remove(self.uniqueName('runAuraDetection'))
        
        subtype = ItemGlobals.getSubtype(currentWeaponId)
        if WeaponGlobals.getWeaponCategory(currentWeaponId) == WeaponGlobals.VOODOO and isWeaponDrawn == True:
            self.guiMgr.attuneSelection.show()
        else:
            self.guiMgr.attuneSelection.hide()
        specialAttack = ItemGlobals.getSpecialAttack(self.currentWeaponId)
        if self.curAttackAnim:
            if specialAttack == EnemySkills.CUTLASS_ROLLTHRUST:
                self.curAttackAnim.pause()
            else:
                self.curAttackAnim.finish()
            self.curAttackAnim = None
        
        if self.secondWeapon:
            self.secondWeapon.removeNode()
            self.secondWeapon = None
        
        if ItemGlobals.getSubtype(currentWeaponId) == ItemGlobals.QUEST_PROP_POWDER_KEG and not isWeaponDrawn:
            currentWeaponId = 0
        
        self.checkWeaponSwitch(currentWeaponId, isWeaponDrawn)
        self.guiMgr.setCurrentWeapon(currentWeaponId, isWeaponDrawn, slotId)
        specialAttack = ItemGlobals.getSpecialAttack(currentWeaponId)
        if specialAttack and isWeaponDrawn:
            if WeaponGlobals.getSkillTrack(specialAttack) == WeaponGlobals.BREAK_ATTACK_SKILL_INDEX:
                self.skillDiary.clearHits(specialAttack)
                self.guiMgr.combatTray.clearSkillCharge(specialAttack)
            else:
                self.skillDiary.startRecharging(specialAttack, 0)
                self.guiMgr.combatTray.startSkillRecharge(specialAttack)
        

    
    def d_requestCurrentWeapon(self, currentWeaponId, isWeaponDrawn):
        self.sendUpdate('requestCurrentWeapon', [
            currentWeaponId,
            isWeaponDrawn])

    
    def d_requestCurrentAmmo(self, currentAmmoId):
        self.sendUpdate('requestCurrentAmmo', [
            currentAmmoId])

    
    def d_requestCurrentCharm(self, currentCharmId):
        self.sendUpdate('requestCurrentCharm', [
            currentCharmId])

    
    def setCurrentCharm(self, currentCharm):
        DistributedPlayerPirate.setCurrentCharm(self, currentCharm)
        self.guiMgr.combatTray.skillTray.updateCharmSkills()

    
    def _LocalPirate__drawWeapon(self):
        self.guiMgr.combatTray.toggleWeapon(self.currentWeaponId, self.currentWeaponSlotId)

    
    def _LocalPirate__drawWeaponIfTarget(self):
        if self.isWeaponDrawn:
            return None
        
        if self.cr.targetMgr:
            target = self.cr.targetMgr.pickObject()
            if target and TeamUtils.damageAllowed(target, self):
                self.guiMgr.combatTray.toggleWeapon(self.currentWeaponId, self.currentWeaponSlotId)
            
        

    
    def enableMouseWeaponDraw(self):
        self.accept('control', self._LocalPirate__drawWeapon)
        self.accept('mouse1', self._LocalPirate__drawWeaponIfTarget)
        self.accept('mouse2', self._LocalPirate__drawWeapon)

    
    def disableMouseWeaponDraw(self):
        self.ignore('control')
        self.ignore('mouse1')
        self.ignore('mouse2')

    
    def runAuraDetection(self, task):
        targets = []
        self.areaAuraSphere.reparentTo(self)
        self.areaAuraTrav.addCollider(self.areaAuraSphere, self.areaAuraQueue)
        self.areaAuraTrav.traverse(self.getRender())
        self.areaAuraTrav.removeCollider(self.areaAuraSphere)
        self.areaAuraSphere.detachNode()
        numEntries = self.areaAuraQueue.getNumEntries()
        if numEntries == 0:
            pass
        1
        for i in range(numEntries):
            entry = self.areaAuraQueue.getEntry(i)
            potentialTargetColl = entry.getIntoNodePath()
            potentialTarget = self.repository.targetMgr.getObjectFromNodepath(potentialTargetColl)
            if potentialTarget:
                if not TeamUtils.damageAllowed(potentialTarget, self):
                    potentialTargetId = potentialTarget.getDoId()
                    targets.append(potentialTargetId)
                
            TeamUtils.damageAllowed(potentialTarget, self)
        
        DistributedPlayerPirate.sendRequestAuraDetection(self, targets)
        return Task.again

    
    def setMoney(self, money, quiet = 0):
        if money == None:
            inv = self.getInventory()
            if inv:
                money = inv.getGoldInPocket()
            else:
                return None
        
        self.guiMgr.setMoney(money)
        if money != 0:
            gain = money - self.money
            if gain > 0 and self._LocalPirate__lootUIEnabled:
                if quiet and self.firstMoneyQuieted == 0 and self.gameFSM.getCurrentOrNextState() == 'ParlorGame' and localAvatar.guiMgr.scoreboard and not localAvatar.guiMgr.scoreboard.isEmpty():
                    self.firstMoneyQuieted = 1
                else:
                    self.guiMgr.messageStack.showLoot([], gold = gain)
            
        
        self.money = money
        inv = self.getInventory()
        if inv:
            if not self.money >= 300 and inv.getStackQuantity(InventoryType.BuyNewShip) == 0:
                if not self.money >= 800 and inv.getStackQuantity(InventoryType.BuyNewShip) == 1:
                    if not self.money >= 1000 and inv.getStackQuantity(InventoryType.BuyNewShip) == 2:
                        if not self.money >= 3500 and inv.getStackQuantity(InventoryType.BuyNewShip) == 3:
                            if not self.money >= 5000 and inv.getStackQuantity(InventoryType.BuyNewShip) == 4:
                                if not self.money >= 20000 and inv.getStackQuantity(InventoryType.BuyNewShip) == 5:
                                    if self.money >= 40000 and inv.getStackQuantity(InventoryType.BuyNewShip) == 6 and self.money >= 60000 and inv.getStackQuantity(InventoryType.BuyNewShip) == 7:
                                        self.sendRequestContext(InventoryType.BuyNewShip)
                                    
                                

    
    def _setCrewShip(self, ship):
        crewShip = self.crewShip
        if crewShip is not None and crewShip != ship:
            crewShip.hideStatusDisplay()
            if self.guiMgr and self.guiMgr.mapPage:
                self.guiMgr.mapPage.removeShip(crewShip.doId)
            
            mapObj = crewShip.getMinimapObject()
            if mapObj:
                mapObj.setAsLocalAvShip(False)
            
        
        DistributedPlayerPirate._setCrewShip(self, ship)
        if ship:
            ship.showStatusDisplay()
            self.d_requestCurrentIsland(0)
            if self.guiMgr and self.guiMgr.mapPage:
                pos = base.cr.activeWorld.getWorldPos(ship)
                self.guiMgr.mapPage.addShip(ship.getShipInfo(), pos)
            
            mapObj = ship.getMinimapObject()
            if mapObj:
                mapObj.setAsLocalAvShip(True)
            
        else:
            self.b_clearTeleportFlag(PiratesGlobals.TFOnShip)
            self.b_clearTeleportFlag(PiratesGlobals.TFNotSameCrew)
            self.b_clearTeleportFlag(PiratesGlobals.TFSiegeCaptain)

    _setCrewShip = report(types = [
        'args',
        'deltaStamp',
        'module'], dConfigParam = 'shipboard')(_setCrewShip)
    
    def setActiveShipId(self, shipId):
        DistributedPlayerPirate.setActiveShipId(self, shipId)
        messenger.send('activeShipChange', sentArgs = [
            shipId])

    setActiveShipId = report(types = [
        'args',
        'deltaStamp',
        'module'], dConfigParam = 'shipboard')(setActiveShipId)
    
    def setReturnLocation(self, returnLocation):
        if returnLocation == '1142018473.22dxschafe':
            returnLocation = LocationIds.DEL_FUEGO_ISLAND
        
        DistributedPlayerPirate.setReturnLocation(self, returnLocation)
        
        def setIt(inventory, returnLocation = returnLocation):
            if inventory:
                if __dev__ and not getBase().config.GetBool('login-location-used-setIt', False):
                    bp.loginCfg()
                    ConfigVariableBool('login-location-used-setRetIt').setValue(True)
                    config_location = getBase().config.GetString('login-location', '').lower()
                    config_location_uid = PLocalizer.LocationUids.get(config_location)
                    if config_location and config_location_uid:
                        self.guiMgr.mapPage.setReturnIsland(config_location_uid)
                        return None
                    
                
                if inventory.getShipDoIdList():
                    self.guiMgr.mapPage.setReturnIsland(returnLocation)
                else:
                    self.guiMgr.mapPage.setReturnIsland(LocationIds.PORT_ROYAL_ISLAND)
            else:
                DistributedInventoryBase.getInventory(self.inventoryId, setIt)

        DistributedInventoryBase.getInventory(self.inventoryId, setIt)

    
    def setCurrentIsland(self, islandUid):
        DistributedPlayerPirate.setCurrentIsland(self, islandUid)
        if self.guiMgr:
            if self.guiMgr.mapPage:
                self.guiMgr.mapPage.setCurrentIsland(islandUid)
            
        

    setCurrentIsland = report(types = [
        'frameCount',
        'args'], dConfigParam = 'map')(setCurrentIsland)
    
    def setJailCellIndex(self, index):
        DistributedPlayerPirate.setJailCellIndex(self, index)
        messenger.send('localAvatar-setJailCellIndex', [
            index])

    
    def setCurrentTarget(self, targetId):
        target = self.cr.doId2do.get(targetId)
        if target == self.currentTarget:
            if TeamUtils.damageAllowed(target, self):
                self.requestCombatMusic()
            
            return None
        
        if self.currentTarget:
            self.currentTarget.setLocalTarget(0)
            if self.currentTarget.state == 'Use':
                self.currentTarget.request('Idle')
            
        
        self.currentTarget = target
        if target:
            if (not hasattr(target, 'currentDialogMovie') or target.currentDialogMovie == None) and target.hideHpMeterFlag == 0:
                target.showHpMeter()
            
            target.setLocalTarget(1)
            target.request('Use')
        
        self.cr.interactionMgr.start()
        if self.currentTarget and TeamUtils.damageAllowed(self.currentTarget, self):
            self.requestCombatMusic()
        
        DistributedPlayerPirate.setCurrentTarget(self, targetId)

    
    def delete(self):
        
        try:
            pass
        except:
            self.LocalPirate_deleted = 1
            self.guiMgr.delete()
            del self.guiMgr
            self.cameraFSM.cleanup()
            del self.cameraFSM
            del self.currentMouseOver
            self.currentAimOver = None
            del self.currentSelection
            del self.skillDiary
            self.ignore('shipRemoved')
            self.cr.avatarFriendsManager.reset()
            DistributedPlayerPirate.delete(self)
            taskMgr.remove(self.uniqueName('questShow'))
            taskMgr.remove(self.uniqueName('oceanCheck'))
            taskMgr.remove(self.uniqueName('runAuraDetection'))
            self.currentStoryQuests = []
            LocalAvatar.delete(self)
            self.stopAllDefenceEffects()
            if self.cloudScudEffect:
                self.cloudScudEffect.stopLoop()
                self.cloudScudEffect = None
            
            self.questStatus.delete()
            del self.questStatus
            self._LocalPirate__cleanupGuildDialog()
            self._LocalPirate__cleanupMoraleDialog()
            del base.localAvatar
            del __builtins__['localAvatar']
            if __dev__:
                del __builtins__['av']
            


    
    def generateHuman(self, *args, **kwargs):
        DistributedPlayerPirate.generateHuman(self, *args, **args)
        self.deleteWeaponJoints()
        lod2000 = self.getLOD('2000')
        if lod2000:
            lod2000.flattenStrong()
        
        lod1000 = self.getLOD('1000')
        if lod1000:
            lod1000.flattenStrong()
        
        self.getWeaponJoints()
        self.setLODAnimation(1000, 1000, 0.001)

    
    def generate(self):
        base.localAvatar = self
        __builtins__['localAvatar'] = self
        if __dev__:
            __builtins__['av'] = self
        
        DistributedPlayerPirate.generate(self)

    
    def addInvInterest(self):
        self.invInterest = self.cr.addTaggedInterest(self.doId, PiratesGlobals.InventoryZone, self.cr.ITAG_AVATAR, 'inventory')

    
    def announceGenerate(self):
        base.loadingScreen.tick()
        invInterestDelay = base.config.GetInt('delay-inv-interest', 10)
        if invInterestDelay > 0:
            DelayedCall(self.addInvInterest, delay = invInterestDelay)
        else:
            self.addInvInterest()
        if self.guildId:
            self.guildInterest = self.cr.addTaggedInterest(self.cr.guildManager.doId, self.guildId, self.cr.ITAG_AVATAR, 'guild')
        else:
            self.guildInterest = None
        self.nametag.manage(base.marginManager)
        self.controlManager.setTag('avId', str(self.getDoId()))
        pe = PolylightEffect.make()
        brightness = 1.25
        darkness = 0.80000000000000004
        pe.setWeight(brightness)
        self.node().setEffect(pe)
        DistributedPlayerPirate.announceGenerate(self)
        self.questStatus = QuestStatus.QuestStatus(self)
        posHpr = (0, 0, 0, 0, 0, 0)
        self.setPosHpr(*posHpr)
        if base.config.GetBool('osd-anim-blends', 0):
            self.toggleOsdAnimBlends(True)
        
        self.acceptOnce('generate-%s' % self.getInventoryId(), self.initInventoryGui)
        for weaponId in WeaponGlobals.getHumanWeaponTypes():
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), weaponId), self.refreshInventoryWeapons)
        
        for skillId in range(InventoryType.begin_WeaponSkillMelee, InventoryType.end_WeaponSkillMelee):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs = [
                skillId])
        
        for skillId in range(InventoryType.begin_WeaponSkillCutlass, InventoryType.end_WeaponSkillCutlass):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs = [
                skillId])
        
        for skillId in range(InventoryType.begin_WeaponSkillPistol, InventoryType.end_WeaponSkillPistol):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs = [
                skillId])
        
        for skillId in range(InventoryType.begin_WeaponSkillMusket, InventoryType.end_WeaponSkillMusket):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs = [
                skillId])
        
        for skillId in range(InventoryType.begin_WeaponSkillBayonet, InventoryType.end_WeaponSkillBayonet):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs = [
                skillId])
        
        for skillId in range(InventoryType.begin_WeaponSkillDagger, InventoryType.end_WeaponSkillDagger):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs = [
                skillId])
        
        for skillId in range(InventoryType.begin_SkillSailing, InventoryType.end_SkillSailing):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs = [
                skillId])
        
        for skillId in range(InventoryType.begin_WeaponSkillCannon, InventoryType.end_ExtendedWeaponSkillCannon):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs = [
                skillId])
        
        for skillId in range(InventoryType.begin_WeaponSkillDoll, InventoryType.end_WeaponSkillDoll):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs = [
                skillId])
        
        for skillId in range(InventoryType.begin_WeaponSkillWand, InventoryType.end_WeaponSkillWand):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs = [
                skillId])
        
        for teleportTokenId in range(InventoryType.begin_TeleportToken, InventoryType.end_TeleportToken):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), teleportTokenId), self.guiMgr.mapPage.updateTeleportIsland, extraArgs = [
                teleportTokenId])
        
        self.accept('inventoryAccumulator-%s-%s' % (self.getInventoryId(), InventoryType.OverallRep), self.updateReputation, extraArgs = [
            InventoryType.OverallRep])
        for repCategory in ReputationGlobals.getReputationCategories():
            self.accept('inventoryAccumulator-%s-%s' % (self.getInventoryId(), repCategory), self.updateReputation, extraArgs = [
                repCategory])
        
        for unCat in ReputationGlobals.getUnspentCategories():
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), unCat), self.guiMgr.updateUnspent, extraArgs = [
                unCat])
        
        self.accept(InventoryGlobals.getCategoryQuantChangeMsg(self.getInventoryId(), InventoryType.ItemTypeConsumable), self.guiMgr.updateTonic)
        self.guiMgr.combatTray.updateBestTonic()
        self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), InventoryType.ShipRepairKit), self.guiMgr.updateShipRepairKit)
        self.guiMgr.combatTray.updateShipRepairKits()
        taskMgr.add(self.shadowReach, 'shadowReach', priority = 40)
        self.accept('enterWater', self.handleWaterIn)
        self.accept('againWater', self.handleWaterAgain)
        self.accept('exitWater', self.handleWaterOut)
        if self.style.getTutorial() < PiratesGlobals.TUT_GOT_COMPASS and not base.config.GetBool('teleport-all', 0):
            self.b_setTeleportFlag(PiratesGlobals.TFNoCompass)
        
        if self.style.getTutorial() == PiratesGlobals.TUT_CHAPTER3_STARTED:
            if self.chatMgr.noChat:
                ct = ChatTutorialAlt.ChatTutorialAlt()
            else:
                ct = ChatTutorial.ChatTutorial()
        
        if not (self.inPvp):
            if self.style.getTutorial() >= PiratesGlobals.TUT_MET_JOLLY_ROGER or self.guiMgr.forceLookout:
                self.guiMgr.crewHUD.setHUDOn()
                self.guiMgr.crewHUDTurnedOff = False
            
        if not base.launcher.getPhaseComplete(5):
            self.b_setTeleportFlag(PiratesGlobals.TFPhaseIncomplete)
            self.accept('phaseComplete-5', self.handlePhaseComplete, extraArgs = [
                5])
        
        self.accept('InputState-forward', self.checkInputState)
        self.accept('InputState-reverse', self.checkInputState)
        self.accept('InputState-turnLeft', self.checkInputState)
        self.accept('InputState-turnRight', self.checkInputState)
        self.accept(WeaponGlobals.LocalAvatarUseItem, self.checkAction)
        self.accept(WeaponGlobals.LocalAvatarUseProjectileSkill, self.checkAction)
        self.accept(WeaponGlobals.LocalAvatarUseShipSkill, self.checkAction)
        self.accept(WeaponGlobals.LocalAvatarUseTargetedSkill, self.checkAction)
        self.accept(WeaponGlobals.LocalAvatarUseTargetedSkill, self.checkAction)
        self.accept('action', self.checkAction)
        self.accept('moustacheFlip', self.handleMoustache)
        self.bindAnim([
            'idle',
            'run',
            'walk',
            'spin_right',
            'spin_left'])
        self.ignore('localAvatarVisZoneChanged')
        if base.options.getCharacterDetailSetting() in (0, 1):
            self.getLODNode().forceSwitch(1)
        
        messenger.send('localPirate-created', [])
        DistributedInventoryBase.getInventory(base.localAvatar.inventoryId, self.inventoryArrived)
        self.guiMgr.initQuestPage()

    
    def disable(self):
        if base.config.GetBool('want-pstats', 0):
            taskMgr.remove('avatarPstats')
        
        self.ignore('generate-%s' % self.getInventoryId())
        self.ignore(InventoryGlobals.getCategoryQuantChangeMsg(self.getInventoryId(), InventoryType.ItemTypeMoney))
        self.ignore('inventoryQuantity-%s-%s' % (self.getInventoryId(), InventoryType.Dinghy))
        self.ignore('inventoryAddDoId-%s-%s' % (self.getInventoryId(), InventoryCategory.SHIPS))
        self.ignore('inventoryRemoveDoId-%s-%s' % (self.getInventoryId(), InventoryCategory.SHIPS))
        self.ignore('control-f3')
        self.ignore('shift-f12')
        self.ignore('enterWater')
        self.ignore('againWater')
        self.ignore('exitWater')
        self.ignore('phaseComplete-5')
        self.ignore(self.cr.getAllInterestsCompleteEvent())
        self.ignore('moustacheFlip')
        self.cr.removeTaggedInterest(self.invInterest)
        self.invInterest = None
        if self.guildInterest:
            self.cr.removeTaggedInterest(self.guildInterest)
            self.guildInterest = None
        
        taskMgr.remove(self.taskName('irisIn'))
        self.stopCombatMusic()
        self.clearBattleTeleportFlag(send = False)
        self.shipList = set()
        self.nametag.unmanage(base.marginManager)
        del self.invInterest
        if self.pendingInitQuest:
            DistributedInventoryBase.cancelGetInventory(self.pendingInitQuest)
            self.pendingInitQuest = None
        
        if self.openJailDoorTrack:
            self.openJailDoorTrack.pause()
            self.openJailDoorTrack = None
        
        taskMgr.remove(self.uniqueName('monitorStickyTargets'))
        taskMgr.remove('localAvLookAtTarget')
        taskMgr.remove(self.uniqueName('setZombie'))
        base.talkAssistant.clearHistory()
        base.chatPanel.updateDisplay()
        self.ignore('InputState-forward')
        self.ignore('InputState-backward')
        self.ignore('uber-enter')
        taskMgr.remove('autoAFK')
        self.cleanupLocalProjectiles()
        messenger.send('localPirateDisabled')
        DistributedPlayerPirate.disable(self)

    
    def inventoryArrived(self, inventory):
        self.accept(InventoryGlobals.getCategoryQuantChangeMsg(localAvatar.getInventoryId(), InventoryType.PVPTotalInfamyLand), self.infamyUpdate)
        self.accept(InventoryGlobals.getCategoryQuantChangeMsg(localAvatar.getInventoryId(), InventoryType.PVPTotalInfamySea), self.infamyUpdate)

    
    def setBadgeIcon(self, titleId, rank):
        DistributedPlayerPirate.setBadgeIcon(self, titleId, rank)
        messenger.send('LocalBadgeChanged')

    
    def setShipBadgeIcon(self, titleId, rank):
        DistributedPlayerPirate.setShipBadgeIcon(self, titleId, rank)
        messenger.send('LocalShipBadgeChanged')

    
    def infamyUpdate(self, task = None):
        if localAvatar.badge and len(localAvatar.badge) == 2:
            titleId = localAvatar.badge[0]
            inventoryType = TitleGlobals.getInventoryType(titleId)
            if inventoryType:
                exp = localAvatar.getInventory().getStackQuantity(TitleGlobals.getInventoryType(titleId))
                realRank = TitleGlobals.getRank(titleId, exp)
                if realRank != localAvatar.badge[1]:
                    localAvatar.sendRequestSetBadgeIcon(titleId, realRank)
                
            
        
        if localAvatar.shipBadge and len(localAvatar.shipBadge) == 2:
            titleId = localAvatar.shipBadge[0]
            inventoryType = TitleGlobals.getInventoryType(titleId)
            if inventoryType:
                exp = localAvatar.getInventory().getStackQuantity(TitleGlobals.getInventoryType(titleId))
                realRank = TitleGlobals.getRank(titleId, exp)
                if realRank != localAvatar.shipBadge[1]:
                    localAvatar.sendRequestSetShipBadgeIcon(titleId, realRank)
                
            
        
        messenger.send('LocalAvatarInfamyUpdated')

    
    def clearInventoryInterest(self):
        self.removeInterest(self.invInterest, event = self.uniqueName('localAvatar-close-inventory'))

    
    def handlePhaseComplete(self, phase):
        DistributedPlayerPirate.handlePhaseComplete(self, phase)
        if phase == 5:
            self.b_clearTeleportFlag(PiratesGlobals.TFPhaseIncomplete)
        

    
    def handleMoustache(self, moustache = 0):
        self.sendClothingUpdate()

    
    def initInventoryGui(self, inventory):
        gold = inventory.getGoldInPocket()
        self.setMoney(gold, quiet = 1)
        self.accept(InventoryGlobals.getCategoryQuantChangeMsg(inventory.doId, InventoryType.ItemTypeMoney), self.setMoney)
        self.refreshInventoryWeapons()

    
    def refreshInventoryWeapons(self, args = None):
        self.equipSavedWeapons()
        self.guiMgr.refreshInventoryWeapons()

    
    def equipSavedWeapons(self):
        inventory = self.getInventory()
        if not inventory:
            return None
        
        self.equippedWeapons = [
            0,
            0,
            0,
            0,
            0,
            0]
        inventory.getEquippedWeapons(self.equippedWeapons)
        if not self.currentWeaponId:
            self.currentWeaponId = self.equippedWeapons[0]
            if self.currentWeaponId:
                self.currentWeaponSlotId = 1
            
            self.l_setCurrentWeapon(self.currentWeaponId, self.isWeaponDrawn, 1)
            self.d_requestCurrentWeapon(self.currentWeaponId, self.isWeaponDrawn)
        
        self.guiMgr.setEquippedWeapons(self.equippedWeapons)

    
    def died(self):
        pass

    
    def setupControls(self):
        floorOffset = OTPGlobals.FloorOffset
        reach = 8.0
        avatarRadius = 1.3999999999999999
        controls = BattleWalker.BattleWalker()
        controls.setWallBitMask(OTPGlobals.WallBitmask | PiratesGlobals.GoldBitmask)
        controls.setFloorBitMask(OTPGlobals.FloorBitmask)
        controls.initializeCollisions(self.cTrav, self, avatarRadius, floorOffset, reach)
        controls.setAirborneHeightFunc(self.getAirborneHeight)
        self.controlManager.add(controls, 'battle')
        self.setupWalkControls(avatarRadius = 1.3999999999999999, floorOffset = OTPGlobals.FloorOffset, reach = reach, wallBitmask = OTPGlobals.WallBitmask | PiratesGlobals.GoldBitmask, floorBitmask = OTPGlobals.FloorBitmask, ghostBitmask = OTPGlobals.GhostBitmask)
        self.enableRun()
        self.startListenAutoRun()

    
    def startListenAutoRun(self):
        self.accept('shift-r', self.startAutoRun)
        self.accept('r', self.toggleAutoRun)
        self.accept('mouse4', self.toggleAutoRun)

    
    def stopListenAutoRun(self):
        self.ignore('shift-r')
        self.ignore('r')
        self.ignore('mouse4')

    
    def toggleAutoRun(self):
        if self.enableAutoRun:
            self.stopAutoRun()
        else:
            self.startAutoRun()
            self.removeContext(InventoryType.DockCommands, 6)

    
    def toggleTurbo(self):
        if self._LocalPirate__turboOn:
            self._LocalPirate__turboOn = 0
        else:
            self._LocalPirate__turboOn = 1

    
    def getTurbo(self):
        return self._LocalPirate__turboOn

    
    def toggleMario(self):
        if self._LocalPirate__marioOn:
            self._LocalPirate__marioOn = 0
            self.setSwiftness(1.0)
        else:
            self._LocalPirate__marioOn = 1
            self.setSwiftness(6.0)

    
    def getMario(self):
        return self._LocalPirate__marioOn

    
    def initializeCollisions(self):
        LocalAvatar.initializeCollisions(self)
        cRay = CollisionRay(0.0, 0.0, 8.0, 0.0, 0.0, -1.0)
        cRayNode = CollisionNode('LP.cRayNode')
        cRayNode.addSolid(cRay)
        cRayNode.setFromCollideMask(OTPGlobals.FloorBitmask)
        cRayNode.setIntoCollideMask(BitMask32.allOff())
        self.cFloorNodePath = self.attachNewNode(cRayNode)
        self.floorEventHandler = CollisionHandlerEvent()
        self.floorEventHandler.addInPattern('enterFloor%in')
        self.floorEventHandler.addOutPattern('exitFloor%in')
        cRay = CollisionRay(0.0, 0.0, 8.0, 0.0, 0.0, -1.0)
        cRayNode2 = CollisionNode('LP.cRayNode2')
        cRayNode2.addSolid(cRay)
        cRayNode2.setFromCollideMask(PiratesGlobals.WaterBitmask)
        cRayNode2.setIntoCollideMask(BitMask32.allOff())
        self.cWaterNodePath = self.attachNewNode(cRayNode2)
        self.waterEventHandler = CollisionHandlerEvent()
        self.waterEventHandler.addInPattern('enterWater')
        self.waterEventHandler.addAgainPattern('againWater')
        self.waterEventHandler.addOutPattern('exitWater')
        zoneSphere = CollisionSphere(0, 0, 0, 1)
        zoneNode = CollisionNode('LP.zoneLOD')
        zoneNode.setFromCollideMask(PiratesGlobals.ZoneLODBitmask)
        zoneNode.setIntoCollideMask(BitMask32.allOff())
        zoneNode.addSolid(zoneSphere)
        self.cZoneLODNodePath = self.attachNewNode(zoneNode)
        base.lodTrav.addCollider(self.cZoneLODNodePath, base.zoneLODEventHandler)
        auraSphere = CollisionSphere(0, 0, 0, WeaponGlobals.AURA_RADIUS)
        node = CollisionNode('areaTargetAuraSphere')
        node.addSolid(auraSphere)
        node.setFromCollideMask(PiratesGlobals.BattleAimBitmask)
        node.setIntoCollideMask(BitMask32.allOff())
        self.areaAuraSphere = NodePath(node)
        self.areaAuraSphere.setName('LocalPirate.auraSphere')
        self.areaAuraQueue = CollisionHandlerQueue()
        self.areaAuraHandler = CollisionHandlerEvent()
        self.areaAuraTrav = CollisionTraverser('LocalPirate.auraTrav')

    
    def deleteCollisions(self):
        LocalAvatar.deleteCollisions(self)
        self.cFloorNodePath.removeNode()
        self.cWaterNodePath.removeNode()
        del self.floorEventHandler
        del self.waterEventHandler
        base.lodTrav.removeCollider(self.cZoneLODNodePath)
        self.cZoneLODNodePath.removeNode()
        self.cZoneLODNodePath = None

    
    def collisionGhost(self):
        LocalAvatar.collisionsOff(self)

    
    def collisionUnghost(self):
        LocalAvatar.collisionsOn(self)

    
    def collisionsOn(self):
        LocalAvatar.collisionsOn(self)
        self.cTrav.addCollider(self.cFloorNodePath, self.floorEventHandler)
        self.cTrav.addCollider(self.cWaterNodePath, self.waterEventHandler)

    
    def collisionsOff(self):
        LocalAvatar.collisionsOff(self)
        self.cTrav.removeCollider(self.cFloorNodePath)
        self.cTrav.removeCollider(self.cWaterNodePath)

    
    def initializeBattleCollisions(self):
        if self.aimTubeNodePaths:
            return None
        
        self.aimTubeEvent = self.uniqueName('aimTube')
        aimTube = CollisionTube(0, 0, 0, 0, 0, self.height, self.battleTubeRadius * 1.5)
        aimTube.setTangible(0)
        aimTubeNode = CollisionNode(self.aimTubeEvent)
        aimTubeNode.addSolid(aimTube)
        aimTubeNode.setIntoCollideMask(PiratesGlobals.BattleAimBitmask)
        aimTubeNodePath = self.attachNewNode(aimTubeNode)
        aimTubeNodePath.setTag('objType', str(PiratesGlobals.COLL_AV))
        aimTubeNodePath.setTag('avId', str(self.doId))
        self.aimTubeNodePaths.append(aimTubeNodePath)

    
    def setupAnimationEvents(self):
        pass

    
    def clearPageUpDown(self):
        if self.isPageDown or self.isPageUp:
            self.lerpCameraFov(PiratesGlobals.DefaultCameraFov, 0.59999999999999998)
            self.isPageDown = 0
            self.isPageUp = 0
            self.setCameraPositionByIndex(self.cameraIndex)
        

    
    def getClampedAvatarHeight(self):
        return max(self.getHeight(), 3.0)

    
    def isLocal(self):
        return 1

    
    def canChat(self):
        if self.cr.allowOpenChat():
            return 1
        
        if self.commonChatFlags & (OTPGlobals.CommonChat | OTPGlobals.SuperChat):
            return 1
        
        return 0

    
    def startChat(self):
        LocalAvatar.startChat(self)
        self.accept('chatUpdateSCQuest', self.b_setSpeedChatQuest)
        self.ignore(PiratesGlobals.ThinkPosHotkey)
        self.accept(PiratesGlobals.ThinkPosHotkey, self.thinkPos)
        self.ignore(PiratesGlobals.SpeedChatHotkey)
        self.accept(PiratesGlobals.SpeedChatHotkey, self.openSpeedChat)

    
    def stopChat(self):
        LocalAvatar.stopChat(self)
        self.ignore('chatUpdateSCQuest')
        self.ignore(PiratesGlobals.ThinkPosHotkey)
        self.ignore(PiratesGlobals.SpeedChatHotkey)

    
    def isMap(self):
        return self.name == 'map'

    
    def thinkPos(self):
        pos = self.getPos(render)
        hpr = self.getHpr(render)
        serverVersion = base.cr.getServerVersion()
        districtName = base.cr.getShardName(self.defaultShard)
        parentId = self.parentId
        zoneId = self.zoneId
        parent = self.cr.doId2do.get(parentId)
        model = None
        if parent:
            pos = self.getPos(parent)
            hpr = self.getHpr(parent)
            if isinstance(parent, DistributedSimpleShip.DistributedSimpleShip):
                model = PLocalizer.ShipClassNames[parent.shipClass]
            elif isinstance(parent, DistributedGameArea.DistributedGameArea):
                model = parent.modelPath
                model = model.split('/')[-1]
            
        
        strPos = '\nMaya Pos: \n%.1f, %.1f, %.1f' % (pos[0], pos[2], -pos[1]) + '\nPanda Pos: \n%.1f, %.1f, %.1f' % (pos[0], pos[1], pos[2]) + '\nH: %.1f' % hpr[0] + '\nModel: %s' % model + '\nTexture: %s, Terrain: %s, Avatar: %s' % (base.options.getTextureScaleString(), base.options.getGameOptionString(base.options.getTerrainDetailSetting()), base.options.getGameOptionString(base.options.getCharacterDetailSetting())) + '\nLoc: (%s, %s)' % (str(parentId), str(zoneId)) + ',\nVer: %s, ' % serverVersion + '\nDistrict: %s' % districtName
        print 'Current position=', strPos.replace('\n', ', ')
        self.setChatAbsolute(strPos, CFThought | CFTimeout)

    
    def openSpeedChat(self):
        pass

    
    def setSwiftness(self, swiftness):
        DistributedPlayerPirate.setSwiftness(self, swiftness)
        self.updatePlayerSpeed()

    
    def setSwiftnessMod(self, swiftness):
        DistributedPlayerPirate.setSwiftnessMod(self, swiftness)
        self.notify.debug('LocalPirate: setSwiftnessMod %s' % swiftness)
        self.updatePlayerSpeed()

    
    def setStunMod(self, stun):
        DistributedPlayerPirate.setStunMod(self, stun)
        self.notify.debug('LocalPirate: setStunMod %s' % stun)
        self.updatePlayerSpeed()

    
    def setHasteMod(self, haste):
        DistributedPlayerPirate.setHasteMod(self, haste)
        self.notify.debug('LocalPirate: setHasteMod %s' % haste)
        self.updatePlayerSpeed()

    
    def setAimMod(self, stun):
        DistributedPlayerPirate.setAimMod(self, stun)
        self.updatePlayerSpeed()

    
    def setTireMod(self, tire):
        DistributedPlayerPirate.setTireMod(self, tire)
        self.notify.debug('LocalPirate: setTireMod %s' % tire)
        self.updatePlayerSpeed()

    
    def attackTire(self, seconds = 1.2):
        if base.cr.gameStatManager.aggroModelIndex == 1:
            self.setTireMod(-0.40000000000000002)
            taskMgr.remove(self.uniqueName('tireTask'))
            taskMgr.doMethodLater(seconds, self.untire, self.uniqueName('tireTask'))
        

    
    def untire(self, task = None):
        self.setTireMod(0.0)
        if task:
            return task.done
        

    
    def targetedWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, attacker, pos, charge = 0, delay = None, multihit = 0, itemEffects = []):
        DistributedPlayerPirate.targetedWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, attacker, pos, delay)
        attacker.respondedToLocalAttack = 1

    
    def updatePlayerSpeed(self):
        speedMult = self.swiftness + self.hasteMod + self.stunMod + self.tireMod
        speedMult = max(speedMult, -1.0)
        if self.swiftness + self.swiftnessMod <= 0.0:
            speedMult = 0.0
        
        if speedMult > 0.5:
            speedMult += self.aimMod
        
        self.notify.debug('speedMult = %s' % speedMult)
        oldSpeeds = PiratesGlobals.PirateSpeeds[self.speedIndex]
        newSpeeds = map(lambda x: speedMult * x, oldSpeeds)
        self.controlManager.setSpeeds(*newSpeeds)

    
    def setWalkForWeapon(self):
        DistributedPlayerPirate.setWalkForWeapon(self)
        self.updatePlayerSpeed()

    
    def requestEnterBattle(self):
        if self.getGameState() == 'LandRoam':
            self.b_setGameState('Battle')
        elif self.getGameState() == 'Battle':
            self.notify.debug('You are already in battle!')
        else:
            self.notify.debug('You cannot use weapons now.')

    
    def requestExitBattle(self):
        if localAvatar.curAttackAnim:
            timeToLock = localAvatar.curAttackAnim.getDuration() - localAvatar.curAttackAnim.getT()
            self.guiMgr.combatTray.noAttackForTime(timeToLock)
        
        if self.guiMgr.mainMenu and not self.guiMgr.mainMenu.isHidden():
            self.guiMgr.toggleMainMenu()
            return None
        
        if self.getGameState() == 'Battle':
            if self.gameFSM.defaultState == 'Battle':
                self.b_setGameState('LandRoam')
            elif self.gameFSM.defaultState in ('Injured', 'Dying'):
                return None
            else:
                self.b_setGameState(self.gameFSM.defaultState)
        
        messenger.send('weaponSheathed')

    
    def requestEmote(self, emoteId):
        if localAvatar.curAttackAnim:
            timeToLock = localAvatar.curAttackAnim.getDuration() - localAvatar.curAttackAnim.getT()
            self.guiMgr.combatTray.noAttackForTime(timeToLock)
        
        return DistributedPlayerPirate.requestEmote(self, emoteId)

    
    def togglePrintAnimBlends(self, enable = None):
        if not hasattr(self, '_printAnimBlends'):
            self._printAnimBlends = False
        
        if enable is None:
            enable = not (self._printAnimBlends)
        
        self._printAnimBlends = enable
        if enable:
            
            def doPrint(task, self = self):
                print 'AnimBlends:'
                self.printAnimBlends()
                print ''
                return task.cont

            taskMgr.add(doPrint, 'printAnimBlends')
            print 'togglePrintAnimBlends ON'
        else:
            taskMgr.remove('printAnimBlends')
            print 'togglePrintAnimBlends OFF'

    
    def toggleOsdAnimBlends(self, enable = None):
        if not hasattr(self, '_osdAnimBlends'):
            self._osdAnimBlends = False
        
        if enable is None:
            enable = not (self._osdAnimBlends)
        
        self._osdAnimBlends = enable
        if enable:
            
            def doOsd(task, self = self):
                self.osdAnimBlends()
                return task.cont

            taskMgr.add(doOsd, 'osdAnimBlends')
            print 'toggleOsdAnimBlends ON'
        else:
            taskMgr.remove('osdAnimBlends')
            print 'toggleOsdAnimBlends OFF'

    
    def toggleAvVis(self):
        self.getLOD('2000').toggleVis()
        self.find('**/drop_shadow*').toggleVis()

    
    def getAddInterestEventName(self):
        return self.uniqueName('addInterest')

    
    def getRemoveInterestEventName(self):
        return self.uniqueName('removeInterest')

    
    def setInterest(self, parentId, zone, interestTags, event = None):
        context = self.cr.addInterest(parentId, zone, interestTags[0], event)
        if context:
            self.notify.debug('adding interest %d: %d %d' % (context.asInt(), parentId, zone))
            self.interestHandles.append([
                interestTags,
                context])
        else:
            self.notify.warning('Tried to set interest when shard was closed')
			
  setInterest = report(types = [
        'args',
        'deltaStamp',
        'module'], dConfigParam = 'teleport')(setInterest)

    def clearInterest(self, event):
        if len(self.interestHandles) > 0:
            contextInfo = self.interestHandles[0]
            self.notify.debug('removing interest %d' % contextInfo[1])
            self.cr.removeInterest(contextInfo[1], event)
            self.interestHandles.remove(contextInfo)

  clearInterest = report(types = ['args', 'deltaStamp', 'module'], dConfigParam = 'teleport')(clearInterest)

    def clearInterestNamed(self, callback, interestTags):
        toBeRemoved = []
        numInterests = 0
        for currContext in self.interestHandles:
            matchFound = False
            for currTag in interestTags:
                if currTag in currContext[0]:
                    matchFound = True
                    break
                    continue

            if matchFound:
                context = currContext[1]
                self.notify.debug('removing interest %s' % context)
                self.cr.removeInterest(context, callback)
                toBeRemoved.append(currContext)
                numInterests += 1
                continue

        for currToBeRemoved in toBeRemoved:
            self.interestHandles.remove(currToBeRemoved)

        if numInterests == 0 and callback:
            messenger.send(callback)

        return numInterests

    def replaceInterestTag(self, oldTag, newTag):
        for i in xrange(len(self.interestHandles)):
            tags, ctx = self.interestHandles.pop(0)
            newTags = [tag if tag != oldTag else newTag for tag in tags]
            self.interestHandles.append([newTags, ctx])

    #def d_setLocation(self, parentId, zoneId, teleport=0):
    #    self.sendUpdate('setLocation', [parentId, zoneId, teleport])

    #def b_setLocation(self, parentId, zoneId, teleport=0):
    #    self.d_setLocation(parentId, zoneId, teleport)
    #    setLocation(parentId, zoneId, teleport)

    #def setLocation(self, parentId, zoneId, teleport=0):
    #    pass
        #if zoneId and parentId:
        #    DistributedBattleAvatar.setLocation(self, parentId, zoneId, teleport)

    def teleportToShard(self, shardId, zoneId, callbackEvent):
        messenger.send(callbackEvent)

    def handleTeleportToShardDone(self):
        pass

    def setLootCarried(self, *args, **kw):
        pass

    def printState(self, *args, **kw):
        pass

    def playOuch(self, *args, **kw):
        pass

    def getGetupTrack(self, *args, **kw):
        pass

    def hasEffect(self, *args, **kw):
        pass

    def setBattleTeleportFlag(self, *args, **kw):
        pass

    def clearBattleTeleportFlag(self, *args, **kw):
        pass

    def setupMovementSounds(self, *args, **kw):
        pass

    def _setShip(self, *args, **kw):
        pass

    def setShipId(self, *args, **kw):
        pass

    def setAreaFootstep(self, *args, **kw):
        pass

    def setSurfaceIndexFromLevelDefault(self, *args, **kw):
        pass

    def setSurfaceIndex(self, *args, **kw):
        pass

    def setMovementIndex(self, *args, **kw):
        pass

    def getTrackedRotation(self, *args, **kw):
        pass

    def _changeMoveSound(self, *args, **kw):
        pass

    def stopSound(self, *args, **kw):
        pass

    def refreshStatusTray(self, *args, **kw):
        pass

    def getConeOriginNode(self, *args, **kw):
        pass

    def composeRequestProjectileSkill(self, *args, **kw):
        pass

    def composeRequestShipSkill(self, *args, **kw):
        pass

    def initCombatTray(self, *args, **kw):
        pass

    def setStickyTargets(self, *args, **kw):
        pass

    def startMonitorStickyTargets(self, *args, **kw):
        pass

    def monitorStickyTargets(self, *args, **kw):
        pass

    def openJailDoor(self, *args, **kw):
        pass

    def beginTrackTarget(self, *args, **kw):
        pass

    def endTrackTarget(self, *args, **kw):
        pass

    def startLookAtTarget(self, *args, **kw):
        pass

    def __lookAtTarget(self, *args, **kw):
        pass

    def stopLookingAtTarget(self, *args, **kw):
        pass

    def testFacing(self, *args, **kw):
        pass

    def findLegalTargets(self, *args, **kw):
        pass

    def checkViewingArc(self, *args, **kw):
        pass

    def addWobbleId(self, *args, **kw):
        pass

    def removeWobbleId(self, *args, **kw):
        pass

    def startFovWobble(self, *args, **kw):
        pass

    def doFovWobble(self, *args, **kw):
        pass

    def setCamFov(self, *args, **kw):
        pass

    def setCamRoll(self, *args, **kw):
        pass

    def stopFovWobble(self, *args, **kw):
        pass

    def _setCreatureTransformation(self, *args, **kw):
        pass

    def setCreatureTransformation(self, *args, **kw):
        pass

    def setHasGhostPowers(self, *args, **kw):
        pass

    def startGhostGM(self, *args, **kw):
        pass

    def stopGhostGM(self, *args, **kw):
        pass

    def requestKill(self, *args, **kw):
        pass

    def requestGhost(self, *args, **kw):
        pass

    def setAvatarViewTarget(self, *args, **kw):
        pass

    def acknowledgeViewTarget(self, *args, **kw):
        pass

    def displayWhisper(self, *args, **kw):
        pass

    def displayTalkWhisper(self, *args, **kw):
        pass

    def displayTalkAccount(self, *args, **kw):
        pass

    def whisperTo(self, *args, **kw):
        pass

    def setKickEvents(self, *args, **kw):
        pass

    def spendSkillPoint(self, *args, **kw):
        pass

    def checkForAutoTrigger(self, *args, **kw):
        pass

    def swapFloorCollideMask(self, *args, **kw):
        pass

    def handleShipArrive(self, *args, **kw):
        pass

    def handleShipLeave(self, *args, **kw):
        pass

    def placeOnShip(self, *args, **kw):
        pass

    def removeFromShip(self, *args, **kw):
        pass

    def startAutoRun(self, *args, **kw):
        pass

    def stopAutoRun(self, *args, **kw):
        pass

    def getName(self, *args, **kw):
        pass

    def soShowReset(self, *args, **kw):
        pass

    def resetQuestShow(self, *args, **kw):
        pass

    def setGuildId(self, *args, **kw):
        pass

    def setBandId(self, *args, **kw):
        pass

    def setSiegeTeam(self, *args, **kw):
        pass

    def setTutorial(self, *args, **kw):
        pass

    def startOceanCheck(self, *args, **kw):
        pass

    def checkCurrentOcean(self, *args, **kw):
        pass

    def l_setActiveQuest(self, *args, **kw):
        pass

    def wrtReparentTo(self, *args, **kw):
        pass

    def enableWaterEffect(self, *args, **kw):
        pass

    def disableWaterEffect(self, *args, **kw):
        pass

    def adjustWaterEffect(self, *args, **kw):
        pass

    def handleWaterIn(self, *args, **kw):
        pass

    def handleWaterAgain(self, *args, **kw):
        pass

    def handleWaterOut(self, *args, **kw):
        pass

    def spawnWiggle(self, *args, **kw):
        pass

    def setLifterDelayFrames(self, *args, **kw):
        pass

    def queueStoryQuest(self, *args, **kw):
        pass

    def resetStoryQuest(self):
        self.currentStoryQuests = []

    def triggerNPCInteract(self, *args, **kw):
        pass

    def leaveZoneLOD(self, LODObj):
        pass

    def enterZoneLOD(self, LODObj):
        pass

    def b_setGameState(self, *args, **kw):
        pass

    def printTS(self, *args, **kw):
        pass

    def printIZL(self, *args, **kw):
        pass

    def addStatusEffect(self, *args, **kw):
        pass

    def removeStatusEffect(self, *args, **kw):
        pass

    def setDefaultShard(self, *args, **kw):
        pass

    def logDefaultShard(self, *args, **kw):
        pass

    def enableCloudScudEffect(self, *args, **kw):
        pass

    def disableCloudScudEffect(self, *args, **kw):
        pass

    def teleportCleanupComplete(self, *args, **kw):
        pass

    def doFadeIn(self, *args, **kw):
        pass

    def setSoloInteraction(self, solo):
        self.soloInteraction = solo

    def getSoloInteraction(self):
        return self.soloInteraction

    def initVisibleToCamera(self):
        pass

    def isStateAIProtected(self):
        pass

    def setGameState(self, gameState, timestamp = None, localArgs = [], localChange = 0):
        pass

    def motionFSMEnterState(self, *args, **kw):
        pass

    def motionFSMExitState(self, *args, **kw):
        pass

    def updatePaidStatus(self, *args, **kw):
        pass

    def goAFK(self, task):
        if not self.isAFK:
            self.toggleAFK()
        return task.done

    def checkInputState(self, message):
        pass

    def checkAction(self, *args, **kw):
        pass

    def delayAFK(self, message=None):
        pass

    def toggleAFK(self):
        pass

    def gotSpecialReward(self, *args, **kw):
        pass

    def addLocalProjectile(self, *args, **kw):
        pass

    def clearLocalProjectile(self, *args, **kw):
        pass

    def cleanupLocalProjectiles(self, *args, **kw):
        pass

    def addShipTarget(self, *args, **kw):
        pass

    def setCannonAmmoSkillId(self, *args, **kw):
        pass

    def getCannonAmmoSkillId(self):
        pass

    def getShortName(self):
        pass

    def getLevel(self):
        pass

    def setAsGM(self, state):
        pass

    def setBadgeIcon(self, titleId, rank):
        pass

    def setShipBadgeIcon(self, titleId, rank):
        pass

    def changeBodyType(self):
        if self.gameFSM.getCurrentOrNextState() == 'Battle':
            self.b_setGameState('LandRoam')
        DistributedPlayerPirate.changeBodyType(self)

    def setAvatarSkinCrazy(self, *args, **kw):
        pass

    def playCurse(self, *args, **kw):
        pass

    def setZombie(self, *args, **kw):
        pass

    def setCurseStatus(self, status):
        
        def valid_value(val, states):
            return (val >= 0 and val <= len(states))

        states = [[6, None], [5, self.jollySfx], [4, None]]
        if not valid_value(status, states):
            return

        state = states[status]
        base.cr.newsManager.displayMessage(state[0])
        if state[1]:
            base.playSfx(state[1])

    def getAllowSocialPanel(self):
        allowed = False
        if not self.config.GetBool('want-tutorial', 0) and __dev__:
            allowed = True
        else:
            if hasattr(self, 'allowSocialPanel'):
                allowed = self.allowSocialPanel
        return allowed

    def setAllowSocialPanel(self, allow):
        self.allowSocialPanel = allow

    def displayMoraleMessage(self):
        pass

    def __cleanupMoraleDialog(self):
        if self.moralePopupDialog:
            self.moralePopupDialog.destroy()
            self.moralePopupDialog = None

    def __destroyedMoraleDialog(self):
        self.moralePopupDialog = None

    def guildStatusUpdate(self, *args, **kw):
        pass

    def guildNameRequest(self):
        pass

    def guildNameReject(self, guildId):
        pass

    def guildNameChange(self, guildName, name):
        pass

    def __cleanupGuildDialog(self):
        if self.guildPopupDialog:
            self.guildPopupDialog.destroy()
            self.guildPopupDialog = None

    def __destroyedGuildDialog(self):
        self.guildPopupDialog = None

    def getCanLogout(self):
        if not base.config.GetBool('location-kiosk', 0) and self.currentDialogMovie:
            return self.getGameState() != 'Cutscene'

    def teleportQuery(self, requesterId, requesterBandMgrId, requesterBandId, requesterGuildId, requesterShardId):
        pass

    def teleportResponse(self, avId, available, shardId, instanceDoId, areaDoId):
        pass

    def requestCombatMusic(self):
        pass

    def stopCombatMusic(self):
        pass

    def setEfficiency(self, *args, **kw):
        pass

    def setBoardedShip(self, *args, **kw):
        pass

    def putOnBoat(self, *args, **kw):
        pass

    def gotBoat(self, *args, **kw):
        pass

    def arrivedOnShip(self, *args, **kw):
        pass

    def leftShip(self, *args, **kw):
        pass

    def getMinimapObject(self,):
        return None #TODO

    def getGridMinimapObject(self):
        return self.getMinimapObject()

    def setVisZone(self, zone):
        pass

    def handleZoneChanged(self, avObj, parentId, zoneId):
        if avObj is self:
            self.b_setLocation(parentId, zoneId)

    def skipTutorial(self, *args, **kw):
        pass

    def handleBackToMain(self, *args, **kw):
        pass

    def refreshInventoryUI(self):
        pass

    def setDefenceEffect(self, skillId):
        pass

    def stopAllDefenceEffects(self):
        pass

    def testProtection(self):
        pass

    def testBlock(self):
        pass

    def disableLootUI(self):
        self._LocalPirate__lootUIEnabled = True

    def enableLootUI(self):
        self._LocalPirate__lootUIEnabled = True

    def checkHaveShip(self):
        pass

    def enterDialogMode(self):
        pass

    def exitDialogMode(self):
        pass