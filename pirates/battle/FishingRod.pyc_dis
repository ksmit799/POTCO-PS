# File: F (Python 2.4)

import Weapon
import WeaponGlobals
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesbase import PLocalizer
from pirates.effects import PolyTrail
import random

class FishingRod(Weapon.Weapon):
    modelTypes = [
        'models/handheld/pir_m_hnd_tol_fishingPole',
        'models/handheld/pir_m_hnd_tol_fishingPoleMed',
        'models/handheld/pir_m_hnd_tol_fishingPoleLarge']
    models = { }
    icons = { }
    vertex_list = [
        Vec4(0.0, 0.40000000000000002, 0.0, 1.0),
        Vec4(0.0, 2.0, 0.0, 1.0),
        Vec4(-0.55000000000000004, 2.9500000000000002, 0.0, 1.0)]
    motion_color = {
        InventoryType.CutlassWeaponL1: [
            Vec4(0.29999999999999999, 0.40000000000000002, 0.10000000000000001, 0.5),
            Vec4(0.29999999999999999, 0.29999999999999999, 0.29999999999999999, 0.5),
            Vec4(0.59999999999999998, 0.59999999999999998, 0.59999999999999998, 0.5)],
        InventoryType.CutlassWeaponL2: [
            Vec4(0.10000000000000001, 0.20000000000000001, 0.40000000000000002, 0.5),
            Vec4(0.40000000000000002, 0.5, 0.69999999999999996, 0.5),
            Vec4(0.5, 0.5, 0.90000000000000002, 0.75)],
        InventoryType.CutlassWeaponL3: [
            Vec4(1, 1, 0.40000000000000002, 0.5),
            Vec4(0.40000000000000002, 0.5, 0.59999999999999998, 0.5),
            Vec4(0.69999999999999996, 0.69999999999999996, 0.80000000000000004, 0.75)],
        InventoryType.CutlassWeaponL4: [
            Vec4(0.59999999999999998, 0.59999999999999998, 0.75, 1),
            Vec4(0.59999999999999998, 0.5, 0.20000000000000001, 1),
            Vec4(0.59999999999999998, 0.59999999999999998, 0.40000000000000002, 1)],
        InventoryType.CutlassWeaponL5: [
            Vec4(1, 0.20000000000000001, 0.20000000000000001, 0.5),
            Vec4(0.5, 0.5, 0.5, 0.75),
            Vec4(0.69999999999999996, 0.69999999999999996, 0.90000000000000002, 1)],
        InventoryType.CutlassWeaponL6: [
            Vec4(1, 1, 0, 0.5),
            Vec4(0.29999999999999999, 0.29999999999999999, 0.29999999999999999, 1),
            Vec4(0.10000000000000001, 0.10000000000000001, 0.10000000000000001, 1)] }
    
    def __init__(self, itemId):
        Weapon.Weapon.__init__(self, itemId, 'fishingRod')

    
    def loadModel(self):
        self.prop = self.getModel(self.itemId)
        self.prop.reparentTo(self)

    
    def delete(self):
        self.endAttack(None)
        self.removeTrail()
        Weapon.Weapon.delete(self)

    
    def getDrawIval(self, av, ammoSkillId = 0, blendInT = 0.10000000000000001, blendOutT = 0):
        track = Parallel(Func(base.playSfx, self.drawSfx, node = av, cutoff = 60), av.actorInterval('sword_draw', playRate = 1.5, endFrame = 15, blendInT = blendInT, blendOutT = blendOutT), Sequence(Wait(0.187), Func(self.attachTo, av)))
        return track

    
    def getReturnIval(self, av, blendInT = 0, blendOutT = 0.10000000000000001):
        track = Parallel(Func(base.playSfx, self.returnSfx, node = av, cutoff = 60), av.actorInterval('sword_putaway', playRate = 2, endFrame = 35, blendInT = blendInT, blendOutT = blendOutT), Sequence(Wait(0.56000000000000005), Func(self.detachFrom, av)))
        return track

    
    def attachTo(self, av):
        Weapon.Weapon.attachTo(self, av)
        if hasattr(av, 'isGhost') and av.isGhost:
            return None
        
        self.createTrail(av)

    
    def detachFrom(self, av):
        Weapon.Weapon.detachFrom(self, av)
        self.removeTrail()

    
    def createTrail(self, target):
        if self.isEmpty():
            return None
        
        if not self.motion_trail:
            self.motion_trail = PolyTrail.PolyTrail(target, self.vertex_list, self.motion_color.get(self.itemId))
            self.motion_trail.reparentTo(self)
            self.motion_trail.setUseNurbs(1)
            card = loader.loadModel('models/effects/swordtrail_effects')
            tex = card.find('**/swordtrail_lines').findTexture('*')
            self.motion_trail.setTexture(tex)
            self.motion_trail.setBlendModeOn()
            if self.itemId == InventoryType.CutlassWeaponL6:
                self.motion_trail.setBlendModeOff()
            
            card.removeNode()
        

    
    def removeTrail(self):
        if self.motion_trail:
            self.motion_trail.destroy()
            self.motion_trail = None
        

    
    def getBlurColor(self):
        return self.motion_color.get(self.itemId)[2]

    
    def beginAttack(self, av):
        Weapon.Weapon.beginAttack(self, av)

    
    def setupSounds(cls):
        FishingRod.hitSfxs = (loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_CLASHCLANG), loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SWIPECLANG_01), loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SWIPECLANG_02), loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SWIPECLANG_03))
        FishingRod.missSfxs = (loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SWOOSH_01), loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SWOOSH_02))
        FishingRod.skillSfxs = {
            InventoryType.FishingRodStall: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_HACK),
            InventoryType.FishingRodPull: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_HACK),
            InventoryType.FishingRodHeal: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_HACK),
            InventoryType.FishingRodTug: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_HACK),
            InventoryType.FishingRodSink: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_HACK),
            InventoryType.FishingRodOceanEye: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SLASH) }
        FishingRod.drawSfx = loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_REEL_END)
        FishingRod.returnSfx = loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_ROD_OUT)

    setupSounds = classmethod(setupSounds)


def getHitSfx():
    return FishingRod.hitSfxs


def getMissSfx():
    return FishingRod.missSfxs

