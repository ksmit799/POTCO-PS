# File: S (Python 2.4)

from pandac.PandaModules import HashVal, hashPrcVariables
from direct.fsm.FSM import FSM
from direct.task.Task import Task
from direct.distributed import DistributedSmoothNode
from otp.ai.GarbageLeakServerEventAggregator import GarbageLeakServerEventAggregator
from pirates.piratesbase import PiratesGlobals
from pirates.world.LocationConstants import LocationIds

class ShardFSM(FSM):
    
    def __init__(self, cr):
        FSM.__init__(self, 'ShardFSM')
        self.cr = cr
        self.shardInterestHandle = None
        self.request('NoShard')

    
    def enterOff(self):
        self.cr.uidMgr.reset()
        if self.cr.distributedDistrict:
            self.cr.distributedDistrict.worldCreator.cleanupAllAreas()
        
        if config.GetDouble('want-dev-hotkeys', 0):
            self.ignore(PiratesGlobals.LogoutHotkey)
        
        self.cr._removeAllOV()
        self.cr.cache.turnOff()
        self.cr.doDataCache.flush()
        self.cr.handler = self.cr.handleMessageType
        self.cr.cleanupWaitAllInterestsComplete()

    
    def enterNoShard(self):
        locUID = localAvatar.getReturnLocation()
        if locUID:
            self.cr.loadingScreen.showTarget(locUID)
            self.cr.loadingScreen.showHint(locUID)
        else:
            locUID = LocationIds.PORT_ROYAL_ISLAND
            localAvatar.setReturnLocation(locUID)
            self.cr.loadingScreen.showTarget(jail = True)
        base.graphicsEngine.renderFrame()
        
        def logout():
            if hasattr(base, 'localAvatar') and localAvatar.getCanLogout():
                self.cr.logout()
            

        self.cr._userLoggingOut = False
        self.cr.accept(PiratesGlobals.LogoutHotkey, self.cr.logout)

    enterNoShard = report(types = [
        'args'], dConfigParam = [
        'dteleport'])(enterNoShard)
    
    def filterNoShard(self, request, args):
        if request == 'OpenShard':
            pass
        1
        if request == 'ShardReady':
            return None
        
        return self.defaultFilter(request, args)

    filterNoShard = report(types = [
        'args'], dConfigParam = [
        'dteleport'])(filterNoShard)
    
    def exitNoShard(self):
        pass

    exitNoShard = report(types = [
        'args'], dConfigParam = [
        'dteleport'])(exitNoShard)
    
    def enterOpenShard(self):
        shardId = self.cr.getShardId()
        self.cr.handler = self.cr.handleWaitOnEnterResponses
        self.cr.cache.turnOn()
        self.acceptOnce('shardInterestComplete', self.request, extraArgs = [
            'PrepareShard',
            shardId])
        self.shardInterestHandle = self.cr.addTaggedInterest(shardId, PiratesGlobals.ShardInterestZone, self.cr.ITAG_SHARD, 'shardInterest', event = 'shardInterestComplete')

    enterOpenShard = report(types = [
        'args'], dConfigParam = [
        'dteleport'])(enterOpenShard)
    
    def exitOpenShard(self):
        pass

    exitOpenShard = report(types = [
        'args'], dConfigParam = [
        'dteleport'])(exitOpenShard)
    
    def fromOpenShardToOff(self):
        self.exitOpenShard()
        self.ignore('shardInterestComplete')
        self.cr.removeTaggedInterest(self.shardInterestHandle)
        self.shardInterestHandle = None
        self.enterOff()

    fromOpenShardToOff = report(types = [
        'args'], dConfigParam = [
        'dteleport'])(fromOpenShardToOff)
    
    def enterPrepareShard(self, shardId):
        self.cr.distributedDistrict = self.cr.getDo(shardId)
        DistributedSmoothNode.globalActivateSmoothing(1, 0)
        h = HashVal()
        hashPrcVariables(h)
        pyc = HashVal()
        if not __dev__:
            self.cr.hashFiles(pyc)
        
        self.cr.timeManager.d_setSignature(self.cr.userSignature, h.asBin(), pyc.asBin())
        if self.cr.timeManager.synchronize('startup'):
            self.acceptOnce('gotTimeSync', self.request, extraArgs = [
                'ShardReady',
                shardId])
        else:
            self.demand('ShardReady', shardId)

    enterPrepareShard = report(types = [
        'args'], dConfigParam = [
        'dteleport'])(enterPrepareShard)
    
    def exitPrepareShard(self):
        self.cr.removeTaggedInterest(self.shardInterestHandle)
        self.shardInterestHandle = None
        self.ignore('gotTimeSync')
        if self.cr.timeManager:
            self.cr.timeManager.setDisconnectReason(PiratesGlobals.DisconnectSwitchShards)
        

    exitPrepareShard = report(types = [
        'args'], dConfigParam = [
        'dteleport'])(exitPrepareShard)
    
    def fromPrepareShardToShardReady(self, shardId):
        self.ignore('gotTimeSync')
        self.enterShardReady(shardId)

    fromPrepareShardToShardReady = report(types = [
        'args'], dConfigParam = [
        'dteleport'])(fromPrepareShardToShardReady)
    
    def enterShardReady(self, shardId):
        self.garbageLeakLogger = GarbageLeakServerEventAggregator(self)
        self.cr.handler = self.cr.handlePlayGame
        base.transitions.noFade()
        
        def checkScale(task):
            return Task.cont

        messenger.send('shardReady-%s' % (shardId,))

    enterShardReady = report(types = [
        'args'], dConfigParam = [
        'dteleport'])(enterShardReady)
    
    def exitShardReady(self):
        self.cr.cache.turnOff()
        self.cr.removeInterestTag(self.cr.ITAG_GAME)
        self.cr.setWorldStack([])
        self.cr.removeInterestTag(self.cr.ITAG_WORLD)
        self.cr.removeTaggedInterest(self.shardInterestHandle)
        self.shardInterestHandle = None
        self.cr.removeInterestTag(self.cr.ITAG_SHARD)
        if self.cr.timeManager:
            self.cr.timeManager.setDisconnectReason(PiratesGlobals.DisconnectSwitchShards)
        
        taskMgr.remove('globalScaleCheck')
        self.handler = None
        self.garbageLeakLogger.destroy()
        del self.garbageLeakLogger


