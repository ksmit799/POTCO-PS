from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from panda3d.core import *
from pirates.battle.DistributedBattleNPC import DistributedBattleNPC
from pirates.piratesbase import PLocalizer
from pirates.pirate import AvatarTypes
from pirates.piratesbase import PiratesGlobals
from pirates.creature.Alligator import Alligator
from pirates.creature.Bat import Bat
from pirates.creature.Chicken import Chicken
from pirates.creature.Crab import Crab
from pirates.creature.Dog import Dog
from pirates.creature.FlyTrap import FlyTrap
from pirates.creature.Monkey import Monkey
from pirates.creature.Pig import Pig
from pirates.creature.Rooster import Rooster
from pirates.creature.Scorpion import Scorpion
from pirates.creature.Seagull import Seagull
from pirates.creature.Raven import Raven
from pirates.creature.Stump import Stump
from pirates.creature.Wasp import Wasp
from pirates.kraken.Grabber import Grabber
from pirates.kraken.Holder import Holder
from pirates.kraken.KrakenBody import KrakenBody
from pirates.kraken.Head import Head as KrakenHead
from pirates.pirate import AvatarTypes
from pirates.battle import EnemyGlobals
from pirates.effects.Immolate import Immolate
from pirates.effects.JRDeathBlast import JRDeathBlast
from pirates.effects.JRDeath import JRDeath
from pirates.effects.ExplosionFlip import ExplosionFlip
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
import random
CreatureTypes = {
    AvatarTypes.Crab: Crab,
    AvatarTypes.RockCrab: Crab,
    AvatarTypes.StoneCrab: Crab,
    AvatarTypes.GiantCrab: Crab,
    AvatarTypes.CrusherCrab: Crab,
    AvatarTypes.Chicken: Chicken,
    AvatarTypes.Rooster: Rooster,
    AvatarTypes.Pig: Pig,
    AvatarTypes.Dog: Dog,
    AvatarTypes.Seagull: Seagull,
    AvatarTypes.Raven: Raven,
    AvatarTypes.Stump: Stump,
    AvatarTypes.TwistedStump: Stump,
    AvatarTypes.FlyTrap: FlyTrap,
    AvatarTypes.RancidFlyTrap: FlyTrap,
    AvatarTypes.AncientFlyTrap: FlyTrap,
    AvatarTypes.Scorpion: Scorpion,
    AvatarTypes.DireScorpion: Scorpion,
    AvatarTypes.DreadScorpion: Scorpion,
    AvatarTypes.Alligator: Alligator,
    AvatarTypes.BayouGator: Alligator,
    AvatarTypes.BigGator: Alligator,
    AvatarTypes.HugeGator: Alligator,
    AvatarTypes.Bat: Bat,
    AvatarTypes.RabidBat: Bat,
    AvatarTypes.VampireBat: Bat,
    AvatarTypes.FireBat: Bat,
    AvatarTypes.Wasp: Wasp,
    AvatarTypes.KillerWasp: Wasp,
    AvatarTypes.AngryWasp: Wasp,
    AvatarTypes.SoldierWasp: Wasp,
    AvatarTypes.Monkey: Monkey,
    AvatarTypes.GrabberTentacle: Grabber,
    AvatarTypes.HolderTentacle: Holder,
    AvatarTypes.Kraken: KrakenBody,
    AvatarTypes.KrakenHead: KrakenHead }

class DistributedCreature(DistributedBattleNPC):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCreature')
    
    def __init__(self, cr):
        DistributedBattleNPC.__init__(self, cr)
        self.creature = None
        self.creatureTypeEffect = None
        self.needNoticeGroundTracking = 1
        self.sfxList = []

    
    def generate(self):
        DistributedBattleNPC.generate(self)
        self.customInteractOptions()

    
    def announceGenerate(self):
        DistributedBattleNPC.announceGenerate(self)
        self.addActive()

    
    def disable(self):
        self.removeActive()
        DistributedBattleNPC.disable(self)

    
    def delete(self):
        if self.creature and self.creatureTypeEffect:
            self.creatureTypeEffect.stopLoop()
        
        if self.creature:
            self.creature.detachNode()
            self.creature.delete()
            self.creature = None
        
        self.sfxList = []
        DistributedBattleNPC.delete(self)

    
    def setupCreature(self, avatarType):
        if not self.creature:
            self.creature = CreatureTypes[avatarType.getNonBossType()]()
            self.creature.setAvatarType(avatarType)
            self.creature.reparentTo(self.getGeomNode())
            self.motionFSM.setAnimInfo(self.getAnimInfo('LandRoam'))
            self.nametag3d.setName('empty_use_self_dot_creature_dot_nametag3d_instead')
            self.creature.nametag3d.reparentTo(self.nametag3d)
            if base.options.getCharacterDetailSetting() == 0:
                if self.creature.hasLOD():
                    self.creature.getLODNode().forceSwitch(2)
                
            
            if self.avatarType.isA(AvatarTypes.FireBat):
                geom = self.creature.getGeomNode()
                geom.setTransparency(1)
                geom.setBin('pre-additive', 4)
                geom.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                geom.setColorScale(VBase4(1.0, 0.29999999999999999, 0.29999999999999999, 1))
                FireBat = FireBat
                import pirates.effects.FireBat
                self.creatureTypeEffect = FireBat.getEffect()
                if self.creatureTypeEffect:
                    self.creatureTypeEffect.reparentTo(geom)
                    self.creatureTypeEffect.setPos(0, 0.0, 4.5)
                    self.creatureTypeEffect.startLoop()
                
                self.creature.nametagOffset = 5.0
                self.adjustNametag3d()
            
        

    
    def loop(self, *args, **kw):
        if self.creature:
            pass
        return self.creature.loop(*args, **args)

    
    def play(self, *args, **kw):
        if self.creature:
            pass
        return self.creature.play(*args, **args)

    
    def pingpong(self, *args, **kw):
        if self.creature:
            pass
        return self.creature.pingpong(*args, **args)

    
    def pose(self, *args, **kw):
        if self.creature:
            pass
        return self.creature.pose(*args, **args)

    
    def stop(self, *args, **kw):
        if self.creature:
            pass
        return self.creature.stop(*args, **args)

    
    def setPlayRate(self, *args, **kw):
        if self.creature:
            pass
        return self.creature.setPlayRate(*args, **args)

    
    def getPlayRate(self, *args, **kw):
        if self.creature:
            pass
        return self.creature.getPlayRate(*args, **args)

    
    def getDuration(self, *args, **kw):
        if self.creature:
            pass
        return self.creature.getDuration(*args, **args)

    
    def actorInterval(self, *args, **kw):
        if self.creature:
            pass
        return self.creature.actorInterval(*args, **args)

    
    def getAnimControl(self, *args, **kw):
        if self.creature:
            pass
        return self.creature.getAnimControl(*args, **args)

    
    def getOuchSfx(self):
        if self.creature:
            pass
        return self.creature.sfx.get('pain')

    
    def getSfx(self, *args, **kw):
        if self.creature:
            pass
        return self.creature.getSfx(*args, **args)

    
    def initializeNametag3d(self):
        if self.creature:
            pass
        return self.creature.initializeNametag3d()

    initializeNametag3d = report(types = [
        'module',
        'args'], dConfigParam = 'nametag')(initializeNametag3d)
    
    def getNameText(self):
        if self.creature:
            pass
        return self.creature.getNameText()

    getNameText = report(types = [
        'module',
        'args'], dConfigParam = 'nametag')(getNameText)
    
    def setName(self, name):
        DistributedBattleNPC.setName(self, name)
        self.refreshStatusTray()
        self.creature.nametag.setDisplayName('        ')
        nameText = self.getNameText()
        if nameText:
            if self.isNpc:
                self.accept('weaponChange', self.setMonsterNameTag)
                self.setMonsterNameTag()
                EnemyGlobals = EnemyGlobals
                import pirates.battle
                color2 = EnemyGlobals.getNametagColor(self.avatarType)
                if self.isBoss():
                    color2 = (0.94999999999999996, 0.10000000000000001, 0.10000000000000001, 1)
                
                nameText['fg'] = color2
            
        

    setName = report(types = [
        'module',
        'args'], dConfigParam = 'nametag')(setName)
    
    def setMonsterNameTag(self):
        PLocalizer = PLocalizer
        import pirates.piratesbase
        if self.isInInvasion():
            name = self.name
        elif self.level:
            color = self.cr.battleMgr.getExperienceColor(base.localAvatar, self)
            name = '%s  %s\x01smallCaps\x01%s%s\x02\x02' % (self.name, color, PLocalizer.Lv, self.level)
        else:
            name = self.name
        self.getNameText()['text'] = name

    setMonsterNameTag = report(types = [
        'module',
        'args'], dConfigParam = 'nametag')(setMonsterNameTag)
    
    def addActive(self):
        if self.creature:
            self.creature.addActive()
            self.creature.nametag.setName(' ')
        

    addActive = report(types = [
        'module',
        'args'], dConfigParam = 'nametag')(addActive)
    
    def removeActive(self):
        if self.creature:
            self.creature.removeActive()
        

    
    def customInteractOptions(self):
        self.setInteractOptions(isTarget = False, allowInteract = False)

    
    def setAvatarType(self, avatarType):
        DistributedBattleNPC.setAvatarType(self, avatarType)
        self.setupCreature(avatarType)

    setAvatarType = report(types = [
        'module',
        'args'], dConfigParam = 'nametag')(setAvatarType)
    
    def setLevel(self, level):
        DistributedBattleNPC.setLevel(self, level)
        self.creature.setLevel(level)

    
    def getAnimInfo(self, *args, **kw):
        if self.creature:
            pass
        return self.creature.getAnimInfo(*args, **args)

    
    def freezeShadow(self, *args, **kw):
        self.creature.shadowPlacer.off()
        self.freezeTask = None

    
    def setHeight(self, height):
        self.height = height
        self.creature.adjustNametag3d(self.scale)
        if self.collTube:
            self.collTube.setPointB(0, 0, height)
            if self.collNodePath:
                self.collNodePath.forceRecomputeBounds()
            
        
        if self.battleTube:
            self.battleTube.setPointB(0, 0, max(5.0, height))
        

    
    def shouldNotice(self):
        return self.creature.shouldNotice()

    
    def endShuffle(self):
        self.creature.endShuffle()

    
    def disableMixing(self):
        self.creature.disableMixing()

    
    def enableReducedMixing(self):
        self.creature.enableReducedMixing()

    
    def enableMixing(self):
        self.creature.enableMixing()

    
    def getDeathTrack(self):
        if self.avatarType.isA(AvatarTypes.FireBat):
            av = self.creature
            animName = av.getDeathAnimName()
            duration = av.getDuration(animName)
            frames = av.getNumFrames(animName)
            delay = 0.0
            
            def startSFX():
                sfx = loadSfx(SoundGlobals.SFX_SKILL_HELLFIRE_HIT)
                pitchRate = 0.80000000000000004 + random.random() * 0.40000000000000002
                sfx.setPlayRate(pitchRate)
                si = SoundInterval(sfx, node = self, volume = 1.0, seamlessLoop = False, cutOff = 150.0)
                self.sfxList.append(si)
                si.start()

            
            def stopSmooth():
                if self.smoothStarted:
                    taskName = self.taskName('smooth')
                    taskMgr.remove(taskName)
                
                self.smoothStarted = 0

            
            def startVFX():
                offset = Vec3(0.0, 2.0, 5.0)
                root = av
                explosionEffect = ExplosionFlip.getEffect()
                if explosionEffect:
                    explosionEffect.reparentTo(render)
                    explosionEffect.setPos(root, offset)
                    explosionEffect.setScale(0.5)
                    explosionEffect.play()
                
                if self.creatureTypeEffect:
                    self.creatureTypeEffect.stopLoop()
                    self.creatureTypeEffect = None
                

            
            def startVFX2():
                effectScale = EnemyGlobals.getEffectScale(self)
                offset = Vec3(0.0, 2.0, 5.0)
                root = av
                deathBlast = Immolate.getEffect()
                if deathBlast:
                    deathBlast.reparentTo(render)
                    deathBlast.setPos(root, offset)
                    deathBlast.setScale(effectScale)
                    deathBlast.play()
                

            deathIval = Parallel(Func(stopSmooth), Func(self.setTransparency, 1), Sequence(Func(startVFX), Wait(0.20000000000000001), Func(startVFX2)), Sequence(Func(startSFX), Wait(0.25), Func(startSFX)), av.actorInterval(animName, blendOutT = 0.0), Sequence(Wait(duration / 2.0), LerpColorScaleInterval(av, duration / 2.0, Vec4(1, 1, 1, 0), startColorScale = Vec4(1)), Func(self.hide, 0, PiratesGlobals.INVIS_DEATH), Func(self.clearColorScale), Func(self.clearTransparency)))
            return deathIval
        else:
            return DistributedBattleNPC.getDeathTrack(self)

    
    def getSpawnTrack(self):
        if self.avatarType.isA(AvatarTypes.FireBat):
            if self.getAnimControl('intro'):
                introIval = self.actorInterval('intro')
            else:
                fadeIn = LerpFunctionInterval(self.setAlphaScale, 2.0, fromData = 0.0, toData = 1.0)
                introIval = Sequence(Func(self.setTransparency, 1), fadeIn, Func(self.clearTransparency), Func(self.clearColorScale))
                introIval.append(Func(self.ambushIntroDone))
                return introIval
        else:
            DistributedBattleNPC.getSpawnTrack(self)


