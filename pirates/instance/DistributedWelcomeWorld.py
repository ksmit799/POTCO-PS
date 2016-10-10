# File: D (Python 2.4)

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.PythonUtil import report
from pirates.instance import DistributedInstanceBase
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import TODGlobals
from pirates.battle import EnemyGlobals
from pirates.pvp import PVPGlobals

class DistributedWelcomeWorld(DistributedInstanceBase.DistributedInstanceBase):
    notify = directNotify.newCategory('DistributedWelcomeWorld')
    
    def handleOnStage(self):
        DistributedInstanceBase.DistributedInstanceBase.handleOnStage(self)
        base.cr.timeOfDayManager.setEnvironment(TODGlobals.ENV_DEFAULT)

    handleOnStage = report(types = [
        'args'], dConfigParam = [
        'dteleport'])(handleOnStage)
    
    def getWorldPos(self, node):
        if not node.isEmpty() and self.isOnStage():
            return node.getPos(self)
        

    
    def getAggroRadius(self):
        return EnemyGlobals.MAX_SEARCH_RADIUS

    
    def localAvEnterDeath(self, av):
        DistributedInstanceBase.DistributedInstanceBase.localAvEnterDeath(self, av)
        self.d_localAvatarDied()

    localAvEnterDeath = report(types = [
        'frameCount'], dConfigParam = 'jail')(localAvEnterDeath)

