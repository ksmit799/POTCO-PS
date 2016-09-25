# File: G (Python 2.4)

from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.battle.ProjectileAmmo import ProjectileAmmo
import random

class GrenadeProjectile(ProjectileAmmo):
    
    def __init__(self, cr, ammoSkillId, event):
        ProjectileAmmo.__init__(self, cr, ammoSkillId, event)
        self.splashScale = 1.5
        self.explosionScale = 1.0

    
    def removeNode(self):
        ProjectileAmmo.removeNode(self)

    
    def loadModel(self):
        if not base.config.GetBool('want-special-effects', 1):
            grenade = loader.loadModel('models/ammunition/cannonball')
            grenade.setScale(0.59999999999999998)
        elif self.ammoSkillId == InventoryType.GrenadeExplosion:
            grenade = loader.loadModel('models/ammunition/cannonball')
            grenade.setScale(0.59999999999999998)
        else:
            grenade = loader.loadModel('models/ammunition/cannonball')
            if self.ammoSkillId == InventoryType.GrenadeShockBomb:
                grenade.setColorScale(0.20000000000000001, 1, 0.20000000000000001, 1)
                grenade.setScale(0.59999999999999998)
            elif self.ammoSkillId == InventoryType.GrenadeFireBomb:
                grenade.setColorScale(1, 0.20000000000000001, 0.20000000000000001, 1)
                grenade.setScale(0.59999999999999998)
            elif self.ammoSkillId == InventoryType.GrenadeSmokeCloud:
                grenade.setColorScale(0.5, 0.5, 0.5, 1)
                grenade.setScale(0.59999999999999998)
            elif self.ammoSkillId == InventoryType.GrenadeSiege:
                grenade.setColorScale(0.20000000000000001, 0.20000000000000001, 1, 1)
                grenade.setScale(1.5)
            
        return grenade


