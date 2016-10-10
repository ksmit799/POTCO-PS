# File: D (Python 2.4)

from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from pirates.piratesbase import PiratesGlobals

class DistributedTravelAgent(DistributedObjectGlobal):
    notify = directNotify.newCategory('DistributedTravelAgent')
    
    def d_requestTutorialTeleport(self):
        self.sendUpdate('requestTutorialTeleport')

    d_requestTutorialTeleport = report(types = [
        'args'], dConfigParam = 'dteleport')(d_requestTutorialTeleport)
    
    def d_requestWelcomeWorldTeleport(self):
        self.sendUpdate('requestWelcomeWorldTeleport')

    d_requestWelcomeWorldTeleport = report(types = [
        'args'], dConfigParam = 'dteleport')(d_requestWelcomeWorldTeleport)
    
    def d_requestLoginTeleport(self, shardId = 0):
        self.sendUpdate('requestLoginTeleport', [
            shardId])

    d_requestLoginTeleport = report(types = [
        'args'], dConfigParam = 'dteleport')(d_requestLoginTeleport)
    
    def d_requestInstanceTeleport(self, shardId = 0):
        self.sendUpdate('requestInstanceTeleport', [
            shardId])

    d_requestInstanceTeleport = report(types = [
        'args'], dConfigParam = 'dteleport')(d_requestInstanceTeleport)

