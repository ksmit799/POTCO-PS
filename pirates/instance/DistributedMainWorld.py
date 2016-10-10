# File: D (Python 2.4)

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.PythonUtil import report
from pirates.instance.DistributedInstanceBase import DistributedInstanceBase
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import TODGlobals
from pirates.battle import EnemyGlobals
from pirates.pvp import PVPGlobals
from pirates.effects.FireworkGlobals import *
from pirates.effects.FireworkShowManager import FireworkShowManager

class DistributedMainWorld(DistributedInstanceBase):
    notify = directNotify.newCategory('DistributedMainWorld')
    
    def __init__(self, cr):
        DistributedInstanceBase.__init__(self, cr)
        self.setName('MainWorld')
        self.pvpRespawnCall = None

    
    def disable(self):
        if self.pvpRespawnCall:
            self.pvpRespawnCall.destroy()
            self.pvpRespawnCall = None
        
        DistributedInstanceBase.disable(self)

    
    def delete(self):
        self.ignore('sendingLocalAvatarToJail')
        DistributedInstanceBase.delete(self)

    
    def handleOffStage(self, cacheAreas = []):
        self.disableFireworkShow()
        DistributedInstanceBase.handleOffStage(self, cacheAreas)

    handleOffStage = report(types = [
        'args'], dConfigParam = [
        'dteleport'])(handleOffStage)
    
    def handleOnStage(self):
        DistributedInstanceBase.handleOnStage(self)
        base.cr.timeOfDayManager.setEnvironment(TODGlobals.ENV_DEFAULT)

    handleOnStage = report(types = [
        'args'], dConfigParam = [
        'dteleport'])(handleOnStage)
    
    def localAvEnterDeath(self, av):
        DistributedInstanceBase.localAvEnterDeath(self, av)
        self.d_localAvatarDied()
        if av.getSiegeTeam():
            self._startPvpRespawn(PVPGlobals.MainWorldAvRespawnDelay)
        

    localAvEnterDeath = report(types = [
        'frameCount'], dConfigParam = 'jail')(localAvEnterDeath)
    
    def _startPvpRespawn(self, delay):
        self.pvpRespawnCall = DelayedCall(self._doPvpRespawn, name = 'PVPrespawn', delay = delay)

    
    def _doPvpRespawn(self):
        
        try:
            pass
        except:
            return None

        if hasattr(localAvatar, 'ship') and localAvatar.ship and not localAvatar.ship.isSailable():
            self._startPvpRespawn(0.20000000000000001)
            return None
        
        self.hideDeathLoadingScreen(localAvatar)
        localAvatar.b_setGameState('LandRoam')

    
    def localAvExitDeath(self, av):
        DistributedInstanceBase.localAvExitDeath(self, av)

    localAvExitDeath = report(types = [
        'frameCount'], dConfigParam = 'jail')(localAvExitDeath)
    
    def getWorldPos(self, node):
        if not node.isEmpty() and self.isOnStage():
            return node.getPos(self)
        

    
    def getAggroRadius(self):
        return EnemyGlobals.MAX_SEARCH_RADIUS

    
    def enableFireworkShow(self, timestamp = 0.0, showType = None):
        if showType != None:
            if not self.fireworkShowMgr:
                self.fireworkShowMgr = FireworkShowManager()
                self.fireworkShowMgr.enable(showType, timestamp)
            
        elif base.fourthOfJuly:
            if not self.fireworkShowMgr:
                self.fireworkShowMgr = FireworkShowManager()
                self.fireworkShowMgr.enable(FireworkShowType.FourthOfJuly, timestamp)
            
        

    
    def disableFireworkShow(self):
        if self.fireworkShowMgr:
            self.fireworkShowMgr.disable()
            self.fireworkShowMgr = None
        

    if __dev__:
        
        def printIslands(self):
            for (doId, island) in self.islands.iteritems():
                print doId, `island`
            

    

