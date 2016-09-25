# File: D (Python 2.4)

from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.effects.ProjectileEffect import ProjectileEffect
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesbase import PiratesGlobals
from pirates.effects.SmokeCloud import SmokeCloud
from pirates.effects.ShipSplintersA import ShipSplintersA
from pirates.effects.LightSmoke import LightSmoke
from pirates.effects.ExplosionFlip import ExplosionFlip
from pirates.effects.ShockwaveRing import ShockwaveRing
from pirates.effects.CameraShaker import CameraShaker
from pirates.effects.Fire import Fire
from pirates.effects.MuzzleFlash import MuzzleFlash
from pirates.effects.DustRing import DustRing
from pirates.effects.Sparks import Sparks
from pirates.effects.SmokeBomb import SmokeBomb
from pirates.effects.SmokePillar import SmokePillar
from pirates.effects.FlamingDebris import FlamingDebris
from pirates.effects.ShipDebris import ShipDebris
from pirates.effects.RockDebris import RockDebris
from pirates.effects.Explosion import Explosion
from pirates.effects.ExplosionTip import ExplosionTip
from pirates.effects.LightningStrike import LightningStrike
from pirates.effects.MuzzleFlame import MuzzleFlame
from pirates.effects.SmallRockShower import SmallRockShower
from pirates.effects.SimpleSmokeCloud import SimpleSmokeCloud
from pirates.effects.FlashEffect import FlashEffect
from pirates.effects.WaterMist import WaterMist
from pirates.effects.EruptionSmoke import EruptionSmoke
from pirates.effects.BulletEffect import BulletEffect
from pirates.effects.FireStormRingEffect import FireStormRingEffect
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
import random

class DefenseCannonballProjectileEffect(ProjectileEffect):
    
    def __init__(self, cr, attackerId, hitObject, objType, pos, skillId, ammoSkillId, normal = None):
        ProjectileEffect.__init__(self, cr, attackerId, hitObject, objType, pos, skillId, ammoSkillId, normal)

    
    def basicHitEffect(self, hitObject, pos, skillId, ammoSkillId):
        WeaponGlobals = WeaponGlobals
        import pirates.battle
        if self.cr:
            attacker = self.cr.doId2do.get(self.attackerId)
            aoeRadius = self.cr.battleMgr.getModifiedAttackAreaRadius(attacker, skillId, ammoSkillId)
        else:
            attacker = None
            aoeRadius = 0
        if attacker:
            pass
        unlimited = bool(attacker.isLocal())
        if config.GetBool('show-aoe-radius', 0):
            s = loader.loadModel('models/misc/smiley')
            s.reparentTo(render)
            s.setPos(hitObject, pos)
            s.setScale(aoeRadius)
            s.setTransparency(1)
            s.setColorScale(1.0, 0.5, 0.5, 0.40000000000000002)
        
        if ammoSkillId in [
            InventoryType.DefenseCannonRoundShot,
            InventoryType.DefenseCannonHotShot,
            InventoryType.DefenseCannonBomb,
            InventoryType.DefenseCannonScatterShot,
            InventoryType.DefenseCannonPowderKeg,
            InventoryType.DefenseCannonMine,
            InventoryType.DefenseCannonTargetedShot]:
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                explosionEffect = ExplosionFlip.getEffect(unlimited)
                if explosionEffect:
                    explosionEffect.reparentTo(base.effectsRoot)
                    self.setEffectPos(explosionEffect, hitObject, pos)
                    explosionEffect.setScale(0.80000000000000004)
                    explosionEffect.play()
                
            
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                smokeCloudEffect = SimpleSmokeCloud.getEffect(unlimited)
                if smokeCloudEffect:
                    smokeCloudEffect.reparentTo(hitObject)
                    self.setEffectPos(smokeCloudEffect, hitObject, pos)
                    smokeCloudEffect.setEffectScale(1.0)
                    smokeCloudEffect.play()
                
                if localAvatar.ship and hitObject == localAvatar.ship:
                    cameraShakerEffect = CameraShaker()
                    cameraShakerEffect.wrtReparentTo(hitObject)
                    cameraShakerEffect.setPos(hitObject, pos)
                    cameraShakerEffect.shakeSpeed = 0.040000000000000001
                    cameraShakerEffect.shakePower = 6.0
                    cameraShakerEffect.numShakes = 2
                    cameraShakerEffect.scalePower = 1
                    cameraShakerEffect.play(120.0)
                
            
        
        if ammoSkillId in [
            InventoryType.DefenseCannonBomb,
            InventoryType.DefenseCannonMineInWater]:
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                effect = Explosion.getEffect(unlimited)
                if effect:
                    effect.wrtReparentTo(hitObject)
                    self.setEffectPos(effect, hitObject, pos)
                    effect.setEffectScale(1.0)
                    effect.setEffectRadius(aoeRadius / 3.0)
                    effect.play()
                
            
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                for i in range(2):
                    effect = FlamingDebris.getEffect(unlimited)
                    if effect:
                        effect.wrtReparentTo(base.effectsRoot)
                        self.setEffectPos(effect, hitObject, pos)
                        effect.duration = 4
                        effect.velocityX = self.projVelocity[i][0]
                        effect.velocityY = self.projVelocity[i][1]
                        effect.play()
                        continue
                
                if localAvatar.ship and hitObject == localAvatar.ship:
                    cameraShakerEffect = CameraShaker()
                    cameraShakerEffect.wrtReparentTo(hitObject)
                    cameraShakerEffect.setPos(hitObject, pos)
                    cameraShakerEffect.shakeSpeed = 0.040000000000000001
                    cameraShakerEffect.shakePower = 6.0
                    cameraShakerEffect.numShakes = 2
                    cameraShakerEffect.scalePower = 1
                    cameraShakerEffect.play(300.0)
                
            
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = FlamingDebris.getEffect(unlimited)
                if effect:
                    effect.wrtReparentTo(base.effectsRoot)
                    self.setEffectPos(effect, hitObject, pos)
                    effect.duration = 4
                    effect.velocityX = self.projVelocity[i][0]
                    effect.velocityY = self.projVelocity[i][1]
                    effect.play()
                
            
        
        if ammoSkillId == InventoryType.DefenseCannonFireStorm:
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                for i in range(2):
                    effect = FlamingDebris.getEffect(unlimited)
                    if effect:
                        effect.wrtReparentTo(base.effectsRoot)
                        self.setEffectPos(effect, hitObject, pos)
                        effect.duration = 4
                        effect.velocityX = self.projVelocity[i][0] * random.choice([
                            -1,
                            1])
                        effect.velocityY = self.projVelocity[i][1] * random.choice([
                            -1,
                            1])
                        effect.play()
                        continue
                
            
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                for i in range(3):
                    effect = FlamingDebris.getEffect(unlimited)
                    if effect:
                        effect.wrtReparentTo(base.effectsRoot)
                        self.setEffectPos(effect, hitObject, pos)
                        effect.duration = 4
                        effect.velocityX = self.projVelocity[i][0] * 2 * random.choice([
                            -1,
                            1])
                        effect.velocityY = self.projVelocity[i][1] * 3 * random.choice([
                            -1,
                            1])
                        effect.play()
                        continue
                
                effect = FireStormRingEffect.getEffect(unlimited)
                if effect:
                    effect.wrtReparentTo(base.effectsRoot)
                    self.setEffectPos(effect, hitObject, pos)
                    effect.setEffectScale(1.5)
                    effect.setRadius(30.0)
                    effect.setEffectColor(Vec4(0.80000000000000004, 0.40000000000000002, 0.20000000000000001, 1.0))
                    effect.play()
                
            
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                for i in range(4):
                    effect = FlamingDebris.getEffect(unlimited)
                    if effect:
                        effect.wrtReparentTo(base.effectsRoot)
                        self.setEffectPos(effect, hitObject, pos)
                        effect.duration = 4
                        effect.velocityX = self.projVelocity[i][0] * 3 * random.choice([
                            -1,
                            1])
                        effect.velocityY = self.projVelocity[i][1] * 4 * random.choice([
                            -1,
                            1])
                        effect.play()
                        continue
                
            
        
        if ammoSkillId == InventoryType.DefenseCannonBullet:
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                shipDebris = BulletEffect.getEffect()
                if shipDebris:
                    shipDebris.reparentTo(base.effectsRoot)
                    shipDebris.setPos(hitObject, pos)
                    shipDebris.setScale(1.0)
                    shipDebris.loadObjects(6)
                    shipDebris.play()
                
            
        

    
    def setEffectPos(self, effect, hitObject, pos):
        objType = hitObject.getNetTag('objType')
        if objType and int(objType) == PiratesGlobals.COLL_DEFENSE_AMMO:
            ammo = hitObject.getPythonTag('ammo')
            if ammo:
                effect.reparentTo(render)
                effect.setPos(ammo.getPos())
                return None
            
        
        effect.setPos(hitObject, pos)


