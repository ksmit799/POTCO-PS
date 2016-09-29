# File: S (Python 2.4)

from pandac.PandaModules import Point3, Vec3, Vec4, VBase3, CompassEffect, ModelNode, TransformState, NodePath, NodePathCollection
from direct.showbase import DirectObject
from pirates.piratesbase import PiratesGlobals
from direct.interval.AnimControlInterval import AnimControlInterval
from direct.interval.IntervalGlobal import Sequence, Func
from pirates.audio.SoundGlobals import loadSfx
from pirates.audio import SoundGlobals
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PLocalizer
from pirates.effects.ShipPowerRecharge import ShipPowerRecharge
from pirates.effects.ProtectionDome import ProtectionDome
from pirates.effects.WindBlurCone import WindBlurCone
from pirates.effects.FadingCard import FadingCard
from pirates.effects.DarkMaelstrom import DarkMaelstrom
from pirates.effects.Wind import Wind
from pirates.effects.Wake import Wake
from pirates.effects.WaterWakes import WaterWakes
from pirates.effects.WaterMist import WaterMist
from pirates.effects.ShipFire import ShipFire
from pirates.effects.ShipSmoke import ShipSmoke
from pirates.effects.DarkShipFog import DarkShipFog
from pirates.ship import ShipGlobals
from pirates.battle import Cannon
from pirates.shipparts import CannonPort
from direct.showutil.Rope import Rope
from pandac.PandaModules import RopeNode
import random

class Ship(DirectObject.DirectObject):
    notify = directNotify.newCategory('Ship')
    WantWake = config.GetBool('want-wake', 1)
    breakSfx1 = None
    breakSfx3 = None
    sinkingSfx1 = None
    sinkingSfx2 = None
    
    def __init__(self, shipClass, root, breakAnims, hitAnims, metaAnims, collisions, locators):
        self.modelRoot = root
        self.transRoot = NodePath('transRoot')
        self.modelRoot.reparentTo(self.transRoot)
        self.shipRoot = None
        self.shipClass = shipClass
        self.sailing = False
        self.sfxAlternativeStyle = False
        self.landedGrapples = []
        self.landedGrappleNodes = []
        self.breakAnims = breakAnims
        self.hitAnims = hitAnims
        self.metaAnims = metaAnims
        self.char = self.modelRoot.find('**/+Character')
        self.riggingControls = { }
        numBundles = self.char.node().getNumBundles()
        masts = self.breakAnims.keys()
        masts.sort()
        self.sinkTimeScale = 1.0
        if self.breakSfx1 is None:
            Ship.breakSfx1 = loadSfx(SoundGlobals.SFX_SHIP_MAST_BREAK_01)
        
        if self.breakSfx3 == None:
            Ship.breakSfx3 = loadSfx(SoundGlobals.SFX_MINIGAME_CANNON_MAST_BREAK)
        
        for (i, j) in enumerate(masts):
            bundle = self.char.node().getBundle(i + 1)
            ladderJoint = bundle.findChild('def_ladder_base')
            if ladderJoint:
                self.riggingControls[j] = ladderJoint
                continue
        
        self._Ship__breakIvals = { }
        for i in self.breakAnims:
            self._Ship__breakIvals[i] = Sequence(AnimControlInterval(self.breakAnims[i][0]), AnimControlInterval(self.breakAnims[i][1]))
        
        self._Ship__hitSailingIvals = { }
        for i in self.breakAnims:
            self._Ship__hitSailingIvals[i] = Sequence(AnimControlInterval(self.hitAnims[i][1]), Func(self.metaAnims['idle'].playAll))
        
        self.lod = self.modelRoot.find('**/+LODNode')
        self.modelCollisions = collisions
        self.mastStates = [
            1,
            1,
            1,
            1,
            1]
        self.mastsHidden = False
        self._Ship__targetableCollisions = []
        self.locators = locators
        self.center = None
        self.stern = None
        self.bow = None
        self.starboard = None
        self.port = None
        if self.sinkingSfx1 is None:
            Ship.sinkingSfx1 = loadSfx(SoundGlobals.SFX_SHIP_SINKING)
            Ship.sinkingSfx2 = loadSfx(SoundGlobals.SFX_MINIGAME_CANNON_SHIP_SINK)
        
        self.sinkEffectsRoot = None
        self.sinkEffects = []
        self.sinkTrack = None
        self.isSplit = False
        self.owner = None
        continue
        self.mastCollisions = _[1]([ (int(x.getTag('Mast Code')), x) for x in self.modelCollisions.findAllMatches('**/collision_masts') ])
        self.sailCollisions = self.modelCollisions.findAllMatches('**/collision_sails')
        self.disableSails()
        if self.metaAnims['rolldown'].getNumAnims():
            self._Ship__rollDownIval = AnimControlInterval(self.metaAnims['rolldown'])
            self.metaAnims['rolldown'].poseAll(0)
        else:
            self._Ship__rollDownIval = Interval('dummy', 0, 0)
        if self.metaAnims['rollup'].getNumAnims():
            self._Ship__rollUpIval = AnimControlInterval(self.metaAnims['rollup'])
        else:
            self._Ship__rollUpIval = Interval('dummy', 0, 0)
        self.sailStartIval = Sequence(Func(self.stopIvals), Func(self.enableSails), self._Ship__rollDownIval, Func(self.metaAnims['idle'].loopAll, 1))
        self.sailStopIval = Sequence(Func(self.stopIvals), self._Ship__rollUpIval, Func(self.disableSails), Func(self.metaAnims['tiedup'].playAll))
        self.windTunnelEffect1 = None
        self.windTunnelEffect2 = None
        self.windConeEffect = None
        self.powerRechargeEffect = None
        self.protectionEffect = None
        self.takeCoverEffect = None
        self.openFireEffect = None
        self.stormEffect = None
        self.wake = None
        self.fogEffect = None
        self.leftSideFire = None
        self.leftSideSmoke = None
        self.leftSideFire2 = None
        self.leftSideSmoke2 = None
        self.rightSideFire = None
        self.rightSideSmoke = None
        self.rightSideFire2 = None
        self.rightSideSmoke2 = None
        self.rearSideFire = None
        self.rearSideSmoke = None
        self.fader = None
        self.idleBounds = self.modelRoot.getTightBounds()
        self.setupCollisions()

    
    def setOwner(self, owner, ownerIsModelRoot = False):
        self.owner = owner
        if self.owner:
            if ownerIsModelRoot:
                self.shipRoot = self.owner.getParent()
                self.owner.reparentTo(self.shipRoot)
                self.transRoot.reparentTo(self.owner)
            else:
                self.shipRoot = self.owner.attachNewNode('ShipRoot')
                self.transRoot.reparentTo(self.shipRoot)
            self.modelRoot.setPythonTag('ship', owner)
        

    
    def setupCollisions(self):
        self.modelCollisions.setTag('objType', str(PiratesGlobals.COLL_NEWSHIP))
        self.floors = self.modelCollisions.find('**/collision_floors')
        self.deck = self.modelCollisions.find('**/collision_deck')
        self.planeBarriers = self.modelCollisions.find('**/collision_planes')
        self.planeBarriers.stash()
        self.walls = self.modelCollisions.find('**/collision_walls')
        self.shipCollWall = self.modelCollisions.find('**/collision_shiptoship')
        self.shipCollWall.setTag('objType', str(PiratesGlobals.COLL_NEWSHIP))
        if self.owner:
            self.shipCollWall.setTag('shipId', str(self.owner.doId))
        
        self.panels = self.modelCollisions.find('**/collision_panels')
        self.stashPlaneCollisions()

    
    def stashPlaneCollisions(self):
        self.planeBarriers.stash()

    
    def unstashPlaneCollisions(self):
        self.planeBarriers.unstash()

    
    def computeDimensions(self):
        if not self.center:
            self.center = self.modelRoot.attachNewNode('center')
        
        tb = self.idleBounds
        self.center.setPos((tb[0] + tb[1]) / 2.0)
        self.dimensions = tb[1] - tb[0]
        self.hullDimensions = tb[1] - tb[0]
        if not self.bow:
            self.bow = self.modelRoot.attachNewNode('bowPos')
        
        if not self.port:
            self.port = self.modelRoot.attachNewNode('portPos')
        
        if not self.starboard:
            self.starboard = self.modelRoot.attachNewNode('starboardPos')
        
        if not self.stern:
            self.stern = self.modelRoot.attachNewNode('sternPos')
        
        self.stern.setPos(Point3(0, tb[1][1], 0))
        self.bow.setPos(Point3(0, tb[0][1], 0))
        self.starboard.setPos(Point3(tb[1][0], 0, 0))
        self.port.setPos(Point3(tb[0][0], 0, 0))

    
    def getBoardingLocators(self):
        return self.locators.findAllMatches('**/boarding_spot_*;+s')

    
    def getPartNodes(self):
        if not self.center:
            self.computeDimensions()
        
        return (self.bow, self.port, self.starboard, self.stern)

    
    def disableOnDeckInteractions(self):
        pass

    
    def uniqueName(self, name):
        return name + '-%s' % id(self)

    
    def isInCrew(self, avId):
        if self.owner:
            return self.owner.isInCrew(avId)
        
        return False

    
    def dropMast(self, index):
        if index in self.breakAnims:
            self.breakAnims[index][1].playAll()
            self.dropRigging(index)
            self.mastCollisions[index].stash()
        
        self.mastStates[index] = 0

    
    def dropRigging(self, index):
        if index in self.riggingControls:
            self.riggingControls[index].applyFreeze(TransformState.makeScale((0, 0, 0)))
            self.char.node().forceUpdate()
        

    
    def restoreRigging(self, index):
        if index in self.riggingControls:
            self.riggingControls[index].applyFreeze(TransformState.makeMat(self.riggingControls[index].getDefaultValue()))
            self.char.node().forceUpdate()
        

    
    def hideMasts(self):
        self.mastsHidden = True
        for i in range(5):
            if i in self.breakAnims:
                if self.mastStates[i]:
                    self.breakAnims[i][1].playAll()
                    self.dropRigging(i)
                
            self.mastStates[i]
        

    
    def showMasts(self):
        self.mastsHidden = False
        for i in range(5):
            if i in self.breakAnims:
                if self.mastStates[i]:
                    self.breakAnims[i][0].poseAll(0)
                    self.restoreRigging(i)
                
            self.mastStates[i]
        

    
    def breakMast(self, index):
        breakSfx = self.breakSfx1
        if self.sfxAlternativeStyle:
            breakSfx = self.breakSfx3
        
        base.playSfx(breakSfx, node = self.modelRoot, cutoff = 3000)
        if index in self.breakAnims:
            self._Ship__hitSailingIvals[index].pause()
            self._Ship__breakIvals[index].pause()
            self._Ship__breakIvals[index].start()
            self.dropRigging(index)
            self.mastCollisions[index].stash()
        
        self.mastStates[index] = 0

    
    def restoreMast(self, index):
        if index in self.breakAnims:
            self._Ship__breakIvals[index].pause()
            self.breakAnims[index][0].poseAll(0)
            self.restoreRigging(index)
            self.mastCollisions[index].unstash()
        
        self.mastStates[index] = 1

    
    def mastHit(self, index):
        if index in self.hitAnims:
            if self.mastStates[index] and not (self.mastsHidden):
                if not self.sailing:
                    self.hitAnims[index][0].playAll()
                else:
                    self._Ship__hitSailingIvals[index].start()
            
        

    
    def stopIvals(self):
        self._Ship__rollDownIval.pause()
        self._Ship__rollUpIval.pause()
        for ival in self._Ship__hitSailingIvals.values():
            ival.pause()
        

    
    def playIdle(self):
        self.stopIvals()
        self.metaAnims['idle'].loopAll(1)

    
    def instantSailing(self):
        self.sailing = True
        self.enableSails()
        self.sailStopIval.pause()
        self.sailStartIval.pause()
        self.metaAnims['idle'].loopAll(1)

    
    def startSailing(self):
        self.stopIvals()
        if not self.sailing:
            self.sailing = True
            self.sailStopIval.pause()
            self.sailStartIval.pause()
            self.sailStartIval.start()
        

    
    def instantDocked(self):
        self.sailing = False
        self.disableSails()
        self.stopIvals()
        self.sailStopIval.pause()
        self.sailStartIval.pause()
        self.metaAnims['tiedup'].playAll()

    
    def stopSailing(self):
        if self.sailing:
            self.sailing = False
            self.sailStartIval.pause()
            self.sailStopIval.pause()
            self.sailStopIval.start()
        

    
    def playFullSailEffect(self):
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
            if not self.windTunnelEffect1:
                self.windTunnelEffect1 = Wind.getEffect()
            
            if self.windTunnelEffect1:
                self.windTunnelEffect1.reparentTo(self.center)
                self.windTunnelEffect1.fadeColor = Vec4(0.80000000000000004, 0.80000000000000004, 0.80000000000000004, 0.5)
                self.windTunnelEffect1.setScale(self.dimensions / 6.0)
                self.windTunnelEffect1.fadeTime = 2.0
                self.windTunnelEffect1.setH(180)
                self.windTunnelEffect1.play()
            
        

    
    def playComeAboutEffect(self):
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
            if not self.windTunnelEffect2:
                self.windTunnelEffect2 = Wind.getEffect()
            
            if self.windTunnelEffect2:
                self.windTunnelEffect2.reparentTo(self.center)
                self.windTunnelEffect2.fadeColor = Vec4(0.80000000000000004, 0.80000000000000004, 0.80000000000000004, 0.40000000000000002)
                self.windTunnelEffect2.setScale(self.dimensions / 10.0)
                self.windTunnelEffect2.fadeTime = 2.0
                self.windTunnelEffect2.setH(0)
                self.windTunnelEffect2.play()
            
        

    
    def playRamEffect(self):
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
            if not self.windConeEffect:
                self.windConeEffect = WindBlurCone.getEffect()
            
            if self.windConeEffect:
                self.windConeEffect.reparentTo(self.bow)
                self.windConeEffect.fadeColor = Vec4(0.80000000000000004, 0.80000000000000004, 0.80000000000000004, 0.5)
                self.windConeEffect.setScale(self.dimensions / 3.0)
                self.windConeEffect.setPos(0, self.dimensions[1] / 18.0, self.dimensions[2] / 4.0)
                self.windConeEffect.fadeTime = 2.0
                self.windConeEffect.startLoop()
            
        

    
    def playRechargeEffect(self):
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
            if not self.powerRechargeEffect:
                self.powerRechargeEffect = ShipPowerRecharge.getEffect()
            
            if self.powerRechargeEffect:
                self.powerRechargeEffect.reparentTo(self.char)
                self.powerRechargeEffect.setEffectColor(Vec4(0.5, 0.5, 1, 1))
                self.powerRechargeEffect.setScale(self.dimensions / 4.0)
                self.powerRechargeEffect.startLoop()
            
        

    
    def playSpawnEffect(self):
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
            self.protectionEffect = ProtectionDome.getEffect()
            if self.protectionEffect:
                self.protectionEffect.reparentTo(self.shipRoot)
                self.protectionEffect.setScale(self.dimensions[1] / 15.0)
                self.protectionEffect.startLoop()
            
        

    
    def playTakeCoverEffect(self):
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
            self.takeCoverEffect = FadingCard(loader.loadModel('models/textureCards/skillIcons').find('**/sail_take_cover'), color = Vec4(1, 1, 1, 1), fadeTime = 0.01, waitTime = 2.5, startScale = 0.94999999999999996, endScale = 1.0)
            if self.takeCoverEffect:
                self.takeCoverEffect.reparentTo(self.shipRoot)
                self.takeCoverEffect.setPos(0, 0, self.dimensions[2] * 1.25)
                self.takeCoverEffect.setScale(self.dimensions[1] / 4.0)
                self.takeCoverEffect.play()
                self.owner.playTextEffect(PLocalizer.CrewBuffTakeCoverString)
            
        

    
    def playOpenFireEffect(self):
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
            self.openFireEffect = FadingCard(loader.loadModel('models/textureCards/skillIcons').find('**/sail_openfire2'), color = Vec4(1, 1, 1, 1), fadeTime = 0.01, waitTime = 2.5, startScale = 0.94999999999999996, endScale = 1.0)
            if self.openFireEffect:
                self.openFireEffect.reparentTo(self.shipRoot)
                self.openFireEffect.setPos(0, 0, self.dimensions[2] * 1.25)
                self.openFireEffect.setScale(self.dimensions[1] / 4.0)
                self.openFireEffect.play()
                self.owner.playTextEffect(PLocalizer.CrewBuffOpenFireString)
            
        

    
    def stopRamEffect(self):
        if self.windConeEffect:
            self.windConeEffect.stopLoop()
        

    
    def stopRechargeEffect(self):
        if self.powerRechargeEffect:
            self.powerRechargeEffect.stopLoop()
        

    
    def stopSpawnEffect(self):
        if self.protectionEffect:
            self.protectionEffect.stopLoop()
        

    
    def stopTakeCoverEffect(self):
        if self.takeCoverEffect:
            self.takeCoverEffect.stop()
        

    
    def stopOpenFireEffect(self):
        if self.openFireEffect:
            self.openFireEffect.stop()
        

    
    def playStormEffect(self):
        if not self.stormEffect:
            self.stormEffect = DarkMaelstrom(self.shipRoot)
            self.stormEffect.setZ(50)
            self.stormEffect.loop()
            compassFX = CompassEffect.make(render)
            self.stormEffect.setEffect(compassFX)
        

    
    def stopStormEffect(self):
        if self.stormEffect:
            self.stormEffect.destroy()
            self.stormEffect = None
        

    
    def createWake(self):
        if self.owner:
            ownerId = self.owner.doId
        else:
            ownerId = None
        if not base.cr.activeWorld:
            self.notify.warning('Ship %s is trying to create a wake without an active world.' % (ownerId,))
            return None
        
        if not base.cr.activeWorld.getWater():
            self.notify.warning('Ship %s is trying to create a wake without an ocean. (world: %s)' % (ownerId, base.cr.activeWorld))
            return None
        
        if self.WantWake and base.cr.wantSpecialEffects and self.owner:
            self.removeWake()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                if not hasattr(base.cr.activeWorld.getWater(), 'patch'):
                    self.notify.error("Ship %s is in location %s,%s (%s[%s]).\nThis causes Attribute Error: 'NoneType' object has no attribute 'patch'\n" % (ownerId, self.getLocation()[0], self.getLocation()[1], type(self.getParentObj()), safeRepr(self.getParentObj())))
                
                self.wake = Wake.getEffect()
                if self.wake:
                    self.wake.attachToShip(self.owner)
                    compassFX = CompassEffect.make(render)
                    self.wake.setEffect(compassFX)
                    self.wake.startAnimate(self.owner)
                
            
        

    
    def removeWake(self):
        if self.wake:
            self.wake.cleanUpEffect()
            self.wake = None
        

    
    def hasWake(self):
        return self.wake != None

    
    def cleanup(self):
        self.sinkingEnd()
        self.modelRoot.clearPythonTag('ship')
        self.breakAnims = { }
        self.metaAnims = { }
        self.lod = None
        self.modelRoot.detachNode()
        self.modelRoot = None
        self.locators = None
        self.center = None
        self.stern = None
        self.bow = None
        self.starboard = None
        self.port = None
        self.removeLandedGrapples()
        self.cleanupCollisions()
        self.char = None
        loader.unloadSfx(self.sinkingSfx1)
        loader.unloadSfx(self.sinkingSfx2)
        self.sinkingSfx1 = None
        self.sinkingSfx2 = None
        self.sinkEffectsRoot = None
        self.sinkEffects = []
        self.owner = None
        self._Ship__rollDownIval.pause()
        self._Ship__rollDownIval = None
        self._Ship__rollUpIval.pause()
        self._Ship__rollUpIval = None
        self.sailStartIval.pause()
        self.sailStartIval = None
        self.sailStopIval.pause()
        self.sailStopIval = None
        for ival in self._Ship__breakIvals.values():
            ival.pause()
        
        self._Ship__breakIvals = { }
        self.windTunneldEffect1 = None
        self.windTunnelEffect2 = None
        self.windConeEffect = None
        self.powerRechargeEffect = None
        self.protectionEffect = None
        self.takeCoverEffect = None
        self.openFireEffect = None
        self.stopStormEffect()
        self.removeWake()
        self.cleanupDarkFog()
        if self.fader:
            self.fader.pause()
            self.fader = None
        

    
    def cleanupCollisions(self):
        self.mastCollisions = None
        self._Ship__targetableCollisions = []
        self.modelCollisions = None
        self.floors = None
        self.deck = None
        self.planeBarriers = None
        self.walls = None
        self.shipCollWall = None
        self.panels = None

    
    def demandMastStates(self, mastStates, maxHealth):
        for i in range(5):
            if maxHealth[i]:
                if mastStates[i]:
                    self.restoreMast(i)
                else:
                    self.dropMast(i)
            mastStates[i]
        

    
    def sinkingBegin(self):
        self.computeDimensions()
        self.disableOnDeckInteractions()
        self.removeWake()
        soundTrack = Sequence()
        sinkingSfx = self.sinkingSfx1
        if self.sfxAlternativeStyle:
            sinkingSfx = self.sinkingSfx2
        
        if sinkingSfx:
            soundTrack = Sequence(Func(base.playSfx, sinkingSfx, node = self.modelRoot, cutoff = 1000))
        
        self.sinkTrack = Sequence()
        sinkParallel = Parallel()
        if self.isInCrew(localAvatar.doId):
            sinkParallel.append(Func(base.localAvatar.b_setGameState, 'Cutscene', localArgs = [
                self.owner]))
            sinkParallel.append(self.getSinkCamIval())
        
        sinkParallel.append(Sequence(Func(self.startSinkEffects), soundTrack, self.getSinkShipIval()))
        self.sinkTrack.append(sinkParallel)
        self.sinkTrack.append(Func(self.endSinkEffects))
        if self.owner.isInCrew(localAvatar.doId):
            self.sinkTrack.append(Func(self.cleanupLocalSinking))
        
        self.sinkTrack.start()

    
    def sinkingEnd(self):
        if self.sinkTrack:
            self.sinkTrack.finish()
            self.sinkTrack = None
            self.endSinkEffects()
        

    
    def getSinkShipIval(self):
        return Parallel(LerpPosInterval(self.modelRoot, 18.0 * self.sinkTimeScale, Vec3(0, 0, -1.5 * self.dimensions[2])), LerpHprInterval(self.modelRoot, 12.0 * self.sinkTimeScale, VBase3(self.modelRoot.getH(), self.modelRoot.getP() + 75, self.modelRoot.getR())))

    
    def getSinkCamIval(self):
        camStartPos = Vec3(-4.0 * self.dimensions[0], -1.25 * self.dimensions[1], 40)
        camEndPos = Vec3(-4.0 * self.dimensions[0], self.dimensions[1], self.dimensions[2] / 2.0)
        if self.owner:
            self.owner.lookAtDummy.setPos(0, 0, self.center.getZ())
            
            def camLookAtDummy(t):
                camera.lookAt(self.owner.lookAtDummy)

            return Parallel(Func(camera.reparentTo, self.owner.attachNewNode('cameraDummy')), LerpPosInterval(camera, 16.0 * self.sinkTimeScale, camEndPos, startPos = camStartPos, blendType = 'easeInOut'), LerpPosInterval(self.owner.lookAtDummy, 18.0 * self.sinkTimeScale, Vec3(0, 80, 0)), LerpF