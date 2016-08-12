# File: A (Python 2.4)

from direct.interval.IntervalGlobal import *
from direct.interval.ActorInterval import ActorInterval
from direct.directnotify import DirectNotifyGlobal
from direct.actor.Actor import Actor
from direct.distributed.ClockDelta import *
from direct.showbase.PythonUtil import lerp, report
import types

class MixerType(type):
    
    def __init__(cls, name, bases, dct):
        super(MixerType, cls).__init__(name, bases, dct)
        cls.sectionNameIds = dict(zip(cls.sectionNames, range(len(cls.sectionNames))))
        if set(cls.partNameLists.keys()) != set(cls.sectionNames):
            cls.partNameLists = {section: section for section in cls.sectionNames}
        
class AnimationChannel:
    notify = DirectNotifyGlobal.directNotify.newCategory('AnimationChannel')
    
    def __init__(self, chanId, loop, actor, partName, checkInFunc):
        self.chanId = chanId
        self.actor = actor
        self.partName = partName
        self.checkInFunc = checkInFunc
        self.loop = loop
        self.active = False
        self.upAnimName = None
        self.upAnimWeight = 0.0
        self.savedUpAnimWeight = 0.0
        self.downAnimName = None
        self.downAnimWeight = 0.0
        self.savedDownAnimWeight = 0.0
        self._animCount = 0
        self.animSpanId = 0

    
    def __str__(self):
        return '(AnimationChannel: id=%d loop=%d controlId=%04d active=%d)           downAnim(%1.2f)=%-15s    upAnim(%1.2f)=%-15s' % (self.getId(), self.isLoopChannel(), self.animSpanId, self.isActive(), self.getDownAnimWeight(), str(self.getDownAnimName()), self.getUpAnimWeight(), str(self.getUpAnimName()))

    
    def cleanup(self, checkInFunc):
        self._animCount = 0
        self.animSpanId = 0
        if self.actor and self.getDownAnimName():
            self.actor.setControlEffect(self.getDownAnimName(), 0.0, self.partName)
        
        if self.actor and self.getUpAnimName():
            self.actor.setControlEffect(self.getUpAnimName(), 0.0, self.partName)
        
        self.clearUpAnim(0)
        self.clearDownAnim(0)
        self.checkInFunc = checkInFunc
        self.active = False
        self.looping = False

    
    def delete(self):
        self.cleanup(None)
        self.actor = None
        self.partName = None
        self.checkInFunc = None

    
    def clearUpAnim(self, animSpanId):
        self.setUpAnimName(None, animSpanId)
        self.setUpAnimWeight(0.0, animSpanId)

    
    def clearDownAnim(self, animSpanId):
        if self.actor and self.animSpanId == animSpanId and self.getDownAnimName():
            self.actor.setControlEffect(self.getDownAnimName(), 0.0, self.partName)
            Actor.stop(self.actor, self.getDownAnimName(), self.partName)
        
        self.setDownAnimName(None, animSpanId)
        self.setDownAnimWeight(0.0, animSpanId)

    
    def getId(self):
        return self.chanId

    
    def setUpAnimName(self, name, animSpanId):
        if self.animSpanId == animSpanId:
            self.upAnimName = name
        

    
    def setUpAnimWeight(self, weight, animSpanId):
        if self.animSpanId == animSpanId:
            if self.upAnimName:
                self.upAnimWeight = weight
            else:
                self.upAnimWeight = 0.0
        

    
    def setDownAnimName(self, name, animSpanId):
        if self.animSpanId == animSpanId:
            self.downAnimName = name
        

    
    def setDownAnimWeight(self, weight, animSpanId):
        if self.animSpanId == animSpanId:
            if self.downAnimName:
                self.downAnimWeight = weight
            else:
                self.downAnimWeight = 0.0
        

    
    def getUpAnimName(self):
        return self.upAnimName

    
    def getUpAnimWeight(self):
        return self.upAnimWeight

    
    def getDownAnimName(self):
        return self.downAnimName

    
    def getDownAnimWeight(self):
        return self.downAnimWeight

    
    def setActive(self, active, animSpanId):
        if self.animSpanId == animSpanId:
            self.active = active
        

    
    def isActive(self):
        return self.active

    
    def isLoopChannel(self):
        return self.loop

    
    def getNewAnimSpanId(self):
        self._animCount = self._animCount % 65535 + 1
        return self._animCount

    
    def moveUpToDown(self, newAnim, animSpanId):
        if newAnim == self.getUpAnimName():
            self.saveWeightState(animSpanId)
        elif newAnim == self.getDownAnimName():
            weight = self.getDownAnimWeight()
            self.setDownAnimName(self.getUpAnimName(), animSpanId)
            self.setDownAnimWeight(self.getUpAnimWeight(), animSpanId)
            self.setUpAnimName(newAnim, animSpanId)
            self.setUpAnimWeight(weight, animSpanId)
            self.saveWeightState(animSpanId)
        else:
            self.clearDownAnim(animSpanId)
            self.setDownAnimName(self.getUpAnimName(), animSpanId)
            self.setDownAnimWeight(self.getUpAnimWeight(), animSpanId)
            self.setUpAnimName(newAnim, animSpanId)
            self.setUpAnimWeight(0.0, animSpanId)
            self.saveWeightState(animSpanId)

    
    def saveWeightState(self, animSpanId):
        if self.animSpanId == animSpanId:
            self.savedDownAnimWeight = max(self.getDownAnimWeight(), 0.001)
            self.savedUpAnimWeight = max(self.getUpAnimWeight(), 0.001)
        

    
    def lerpUpAnimWeight(self, t, animSpanId, finalVal = 1.0):
        self.setUpAnimWeight(lerp(self.savedUpAnimWeight, finalVal, t), animSpanId)

    
    def lerpDownAnimWeight(self, t, animSpanId, finalVal = 0.0):
        self.setDownAnimWeight(lerp(self.savedDownAnimWeight, finalVal, t), animSpanId)

    
    def checkInWrapper(self, t, animSpanId):
        if self.animSpanId == animSpanId and self.checkInFunc:
            
            try:
                self.checkInFunc()
            except TypeError:
                e = None
                self.notify.warning(str(e))
                if self.actor:
                    self.notify.warning(self.actor.getName() + ' invalid AnimationChannel state with animSpanId = ' + str(animSpanId))
                
                self.notify.warning('chanId = ' + str(self.getId()))
                self.notify.warning('upAnimName = ' + str(self.getUpAnimName()))
                self.notify.warning('downAnimName = ' + str(self.getUpAnimName()))
            


    
    def assertControl(self, animSpanId):
        self.animSpanId = animSpanId

    
    def applyWeightToUpAnim(self, channelWeight):
        if self.actor and self.upAnimName:
            finalWeight = min(channelWeight, self.getUpAnimWeight())
            self.actor.setControlEffect(self.upAnimName, finalWeight, self.partName)
            return finalWeight
        
        return 0.0

    
    def applyWeightToDownAnim(self, channelWeight):
        if self.actor and self.downAnimName:
            finalWeight = min(channelWeight, self.getDownAnimWeight())
            self.actor.setControlEffect(self.downAnimName, finalWeight, self.partName)
            return finalWeight
        
        return 0.0

    
    def distributeWeightToChannel(self, channelWeight):
        downWeight = self.applyWeightToDownAnim(channelWeight)
        upWeight = self.applyWeightToUpAnim(channelWeight)
        return channelWeight * (downWeight + upWeight)

    
    def getAnimTransIval(self, blendTime, animSpanId, finalUpVal = 1.0, finalDownVal = 0.0):
        return Parallel(LerpFunc(self.lerpDownAnimWeight, duration = blendTime, extraArgs = [
            animSpanId,
            finalDownVal]), LerpFunc(self.lerpUpAnimWeight, duration = blendTime, extraArgs = [
            animSpanId,
            finalUpVal]), LerpFunc(self.checkInWrapper, duration = blendTime, extraArgs = [
            animSpanId]))

    
    def getLoopIval(self, animName, blendInT, blendDelay):
        animSpanId = self.getNewAnimSpanId()
        animSpan = Sequence(Func(self.assertControl, animSpanId, name = Func.makeUniqueName(self.assertControl, animName)), Wait(blendDelay), Func(self.moveUpToDown, animName, animSpanId, name = Func.makeUniqueName(self.moveUpToDown, animName)), Func(self.setActive, True, animSpanId, name = Func.makeUniqueName(self.setActive, animName)), self.getAnimTransIval(blendInT, animSpanId), Func(self.clearDownAnim, animSpanId, name = Func.makeUniqueName(self.clearDownAnim, animName)), Func(self.setActive, bool(animName), animSpanId, name = Func.makeUniqueName(self.setActive, animName)))
        return animSpan

    
    def getPlayIval(self, animName, animTime, blendInT, blendOutT, blendInto):
        animSpanId = self.getNewAnimSpanId()
        blendIn = Sequence(self.getAnimTransIval(blendInT, animSpanId), Func(self.clearDownAnim, animSpanId))
        if animName == None:
            wait = Wait(0)
        else:
            wait = Wait(animTime - blendInT + blendOutT)
        if animName == None:
            blendOut = Sequence(Func(self.setActive, False, animSpanId))
        else:
            blendOut = Sequence(Func(self.moveUpToDown, blendInto, animSpanId), self.getAnimTransIval(blendOutT, animSpanId), Func(self.clearDownAnim, animSpanId), Func(self.setActive, bool(blendInto), animSpanId))
        animSpan = Sequence(Func(self.assertControl, animSpanId, name = Func.makeUniqueName(self.assertControl, animName)), Func(self.moveUpToDown, animName, animSpanId, name = Func.makeUniqueName(self.moveUpToDown, animName)), Func(self.setActive, True, animSpanId, name = Func.makeUniqueName(self.setActive, animName)), blendIn, wait, blendOut)
        return animSpan

    
    def distributeWeight(self, channelWeight):
        return channelWeight - self.distributeWeightToChannel(channelWeight)



class PartMixer:
    notify = DirectNotifyGlobal.directNotify.newCategory('PartMixer')
    
    def __init__(self, mixer, channelCount, actor, partNameList):
        self.actor = actor
        self.partNameList = partNameList
        self.channels = [ AnimationChannel(x, x in mixer.LOOP.values(), actor, partNameList, self.distributeWeight) for x in range(channelCount) ]

    
    def __str__(self):
        outStr = '(PartMixer: parts = %s)\n' % `self.partNameList`
        for chanNum in range(len(self.channels) - 1, -1, -1):
            outStr += '%s\n' % str(self.channels[chanNum])
        
        return outStr

    
    def distributeWeight(self):
        if self.actor and not self.actor.isMixing():
            remainingWeight = 0
        
        remainingWeight = 1.0
        for chanNum in range(len(self.channels) - 1, -1, -1):
            chan = self.channels[chanNum]
            if chan.isActive():
                remainingWeight = chan.distributeWeight(remainingWeight)
        

    
    def getLoopIval(self, chanId, animName, blendInT, blendDelay):
        outIval = Parallel()
        for channel in self.channels:
            if chanId == channel.getId():
                outIval.append(channel.getLoopIval(animName, blendInT, blendDelay))
            if channel.isLoopChannel():
                outIval.append(channel.getLoopIval(None, blendInT, blendDelay))
        
        if len(outIval):
            return outIval
        

    
    def getPlayIval(self, chanId, animName, animTime, blendInT, blendOutT, blendInto):
        return self.channels[chanId].getPlayIval(animName, animTime, blendInT, blendOutT, blendInto)

    
    def cleanup(self):
        for chan in self.channels:
            chan.cleanup(self.distributeWeight)
        

    
    def delete(self):
        self.cleanup()
        for channel in self.channels:
            channel.delete()
        
        self.actor = None
        self.partNameList = None
        self.channels = []



class AnimationMixer:
    __metaclass__ = MixerType
    notify = DirectNotifyGlobal.directNotify.newCategory('AnimationMixer')
    NA_INDEX = -1
    LOOP_INDEX = 0
    ACTION_INDEX = 1
    LOOP = {
        'NA': NA_INDEX,
        'LOOP': LOOP_INDEX }
    ACTION = {
        'NA': NA_INDEX,
        'ACTION': ACTION_INDEX }
    sectionNames = [
        None]
    partNameLists = {
        None: [] }
    AnimRankings = { }
    defaultBlendT = 0.14999999999999999
    
    def __init__(self, actor):
        self.actor = actor
        channelCount = [](_[1])
        self.partMixers = self.sectionNames([](_[1], [ PartMixer(self, channelCount, actor, self.getPartsNameList(part)) for part in self.sectionNames ]))
        self.ownedIvals = []

    
    def __str__(self):
        outStr = '(%s: %s)\n' % (self.__class__.__name__, `self.actor`)
        for sectionName in self.partMixers:
            outStr += '%s\n' % str(self.partMixers[sectionName])
        
        outStr += '\nOwned Intervals\n-------------------------------\n'
        for ival in self.ownedIvals:
            outStr += `ival` + ': isPlaying = ' + `ival.isPlaying()` + '\n'
        
        return outStr

    
    def getPartsNameList(self, sectionName):
        outList = []
        if sectionName is None or set(sectionName) == set(self.sectionNames):
            return None
        elif isinstance(sectionName, types.StringType):
            sectionNames = [
                sectionName]
        elif isinstance(sectionName, types.ListType):
            sectionNames = sectionName
        else:
            sectionNames = []
        for section in sectionNames:
            partList = self.partNameLists.get(section)
            if partList:
                outList.extend(partList)
        
        return outList

    
    def getSectionList(self, sectionName):
        if not sectionName:
            return self.sectionNames
        elif isinstance(sectionName, types.StringType):
            return [
                sectionName]
        elif isinstance(sectionName, types.ListType):
            return sectionName
        else:
            return []

    
    def addIvalToOwnedList(self, ival):
        self.ownedIvals = _[1]
        self.ownedIvals.append(ival)

    
    def __getPlayIval(self, newAnim, partName = None, fromFrame = None, toFrame = None, blendInT = defaultBlendT, blendOutT = defaultBlendT, duration = 0.0, blendInto = None):
        sectionNames = self.getSectionList(partName)
        rankings = self.AnimRankings.get(newAnim)
        if rankings:
            loopRanks = self.LOOP.values()
            ival = Parallel()
            for section in sectionNames:
                rank = rankings[self.sectionNameIds[section]]
                if rank in loopRanks:
                    pass
                1
                if rank > self.NA_INDEX:
                    pDuration = duration
                    partNames = self.getPartsNameList(section)
                    if not pDuration:
                        pDuration = Actor.getDuration(self.actor, newAnim, partNames, fromFrame, toFrame)
                    
                    if pDuration == None:
                        continue
                    
                    if pDuration == 0.0:
                        continue
                    
                    playRate = Actor.getPlayRate(self.actor, newAnim, partNames)
                    if playRate:
                        pDuration /= abs(playRate)
                    
                    if pDuration < blendInT + blendOutT:
                        blendInT = pDuration / 2
                        blendOutT = pDuration / 2
                    
                    ival.append(self.partMixers[section].getPlayIval(rank, newAnim, pDuration, blendInT = blendInT, blendOutT = blendOutT, blendInto = blendInto))
            
            if len(ival):
                return ival
            
        

    _AnimationMixer__getPlayIval = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'animmixer')(__getPlayIval)
    
    def __getLoopIval(self, newAnim, rate = 1.0, partName = None, fromFrame = None, toFrame = None, blendT = defaultBlendT, blendDelay = 0):
        sectionNames = self.getSectionList(partName)
        rankings = self.AnimRankings.get(newAnim)
        if rankings:
            loopRanks = self.LOOP.values()
            loopRanks.sort(reverse = True)
            ival = Parallel()
            for section in sectionNames:
                rank = rankings[self.sectionNameIds[section]]
                if rank not in loopRanks:
                    for loopRank in loopRanks:
                        if loopRank < rank:
                            break
                            continue
                    
                    rank = loopRank
                
                if rank > self.NA_INDEX:
                    loopIval = self.partMixers[section].getLoopIval(rank, newAnim, blendT, blendDelay)
                    if loopIval:
                        ival.append(loopIval)
                    
            
            if len(ival):
                return ival
            
        

    _AnimationMixer__getLoopIval = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'animmixer')(__getLoopIval)
    
    def __getPoseIval(self, newAnim, partName = None, frame = 0, blendT = defaultBlendT):
        sectionNames = self.getSectionList(partName)
        rankings = self.AnimRankings.get(newAnim)
        if rankings:
            loopIndices = self.LOOP.values()
            loopIndices.sort()
            ival = Parallel()
            for section in sectionNames:
                rank = rankings[self.sectionNameIds[section]]
                loopRank = loopIndices[0]
                for loopIndex in loopIndices:
                    if rank >= loopIndex:
                        loopRank = loopIndex
                        continue
                
                rank = loopRank
                if rank > self.NA_INDEX:
                    loopIval = self.partMixers[section].getLoopIval(rank, newAnim, blendT, blendDelay = 0)
                    if loopIval:
                        ival.append(loopIval)
                    
            
            if len(ival):
                return ival
            
        

    _AnimationMixer__getPoseIval = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'animmixer')(__getPoseIval)
    
    def _AnimationMixer__processActorInterval(self, actorInterval, partName, blendInT, blendOutT, blendInto):
        if not isinstance(actorInterval, ActorInterval) and self.actor is not actorInterval.actor or hasattr(actorInterval, 'animMixed'):
            return actorInterval
        
        newAnim = actorInterval.animName
        sectionName = self.getSectionList(partName)
        partName = self.getPartsNameList(sectionName)
        fromFrame = actorInterval.startFrame
        toFrame = actorInterval.endFrame
        duration = actorInterval.duration
        ival = self._AnimationMixer__getPlayIval(newAnim, sectionName, fromFrame, toFrame, blendInT, blendOutT, duration, blendInto)
        if ival:
            actorInterval.resetControls(partName)
            actorInterval = Parallel(ival, actorInterval)
            actorInterval.animMixed = True
        
        return actorInterval

    
    def loop(self, newAnim, rate = 1.0, restart = True, partName = None, fromFrame = None, toFrame = None, blendT = defaultBlendT, blendDelay = 0):
        ival = self._AnimationMixer__getLoopIval(newAnim, rate, partName, fromFrame, toFrame, blendT, blendDelay)
        if ival:
            partName = self.getPartsNameList(self.getSectionList(partName))
            self.actor.setPlayRate(rate, newAnim, partName)
            Actor.loop(self.actor, newAnim, restart = restart, partName = partName, fromFrame = fromFrame, toFrame = toFrame)
            ival.start()
            ival.setT(0.01)
            self.addIvalToOwnedList(ival)
        

    loop = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'animmixer')(loop)
    
    def play(self, newAnim, partName = None, fromFrame = None, toFrame = None, blendInT = defaultBlendT, blendOutT = defaultBlendT, blendInto = None):
        partNames = self.getPartsNameList(self.getSectionList(partName))
        ival = self._AnimationMixer__getPlayIval(newAnim, partName, fromFrame, toFrame, blendInT, blendOutT, blendInto = blendInto)
        if ival:
            Actor.play(self.actor, newAnim, partName = partNames, fromFrame = fromFrame, toFrame = toFrame)
            ival.start()
            ival.setT(0.01)
            self.addIvalToOwnedList(ival)
        

    play = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'animmixer')(play)
    
    def pingpong(self, newAnim, rate = 1.0, partName = None, fromFrame = None, toFrame = None, blendT = defaultBlendT):
        ival = self._AnimationMixer__getLoopIval(newAnim, rate, partName, fromFrame, toFrame, blendT)
        if ival:
            partName = self.getPartsNameList(self.getSectionList(partName))
            self.actor.setPlayRate(rate, newAnim, partName)
            Actor.pingpong(self.actor, newAnim, partName = partName, fromFrame = fromFrame, toFrame = toFrame)
            ival.start()
            ival.setT(0.01)
            self.addIvalToOwnedList(ival)
        

    pingpong = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'animmixer')(pingpong)
    
    def pose(self, newAnim, frame, partName = None, blendT = defaultBlendT):
        ival = self._AnimationMixer__getPoseIval(newAnim, partName, frame, blendT)
        if ival:
            partName = self.getPartsNameList(self.getSectionList(partName))
            Actor.pose(self.actor, newAnim, frame = frame, partName = partName)
            ival.start()
            ival.setT(0.01)
            self.addIvalToOwnedList(ival)
        

    pose = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'animmixer')(pose)
    
    def actorInterval(self, actorInterval, partName, blendInT = defaultBlendT, blendOutT = defaultBlendT, blendInto = None):
        return self._AnimationMixer__processActorInterval(actorInterval, partName, blendInT, blendOutT, blendInto)

    actorInterval = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'animmixer')(actorInterval)
    
    def stop(self, animName = None, partName = None):
        Actor.stop(self.actor, animName, partName)

    stop = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'animmixer')(stop)
    
    def cleanup(self):
        for ival in self.ownedIvals:
            ival.finish()
        
        self.ownedIvals = []
        for sectionName in self.partMixers:
            self.partMixers[sectionName].cleanup()
        
        Actor.stop(self.actor)
        Actor.setControlEffect(self.actor, None, 0.0)

    cleanup = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'animmixer')(cleanup)
    
    def delete(self):
        self.cleanup()
        for sectionName in self.partMixers:
            self.partMixers[sectionName].delete()
        
        self.actor = None
        self.partMixers = { }



class ReducedAnimationMixer(AnimationMixer):
    
    def __init__(self, actor):
        AnimationMixer.__init__(self, actor)
        self.actionAnim = None
        self.loopAnim = None
        self.loopOp = None
        self.loopArgs = ()
        self.loopKw = { }
        self._ReducedAnimationMixer__actionContext = 0

    __init__ = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'animmixer')(__init__)
    
    def __str__(self):
        outStr = '(%s: %s)\n' % (self.__class__.__name__, `self.actor`)
        outStr += 'actionAnim: %s\n' % (self.actionAnim,)
        if self.loopOp:
            outStr += 'loopStatus: %s(%s, %s, %s)\n' % (self.loopOp.__name__, self.loopAnim, self.loopArgs, self.loopKw)
        else:
            outStr += 'loopStatus: None\n'
        outStr += '\nOwned Intervals\n-------------------------------\n'
        for ival in self.ownedIvals:
            outStr += `ival` + ': isPlaying = ' + `ival.isPlaying()` + '\n'
        
        return outStr

    
    def nextActionContext(self):
        self._ReducedAnimationMixer__actionContext += 1
        return self._ReducedAnimationMixer__actionContext

    
    def setAction(self, anim, context):
        if context >= self._ReducedAnimationMixer__actionContext:
            self.actionAnim = anim
            self.actor.setControlEffect(anim, 1)
        

    setAction = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'animmixer')(setAction)
    
    def clearAction(self, context):
        if context >= self._ReducedAnimationMixer__actionContext:
            if self.actionAnim:
                self.stop(self.actionAnim)
            
            self.actionAnim = None
            self._ReducedAnimationMixer__startLoopIfAble()
        

    clearAction = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'animmixer')(clearAction)
    
    def setLoop(self, loopOp, anim, *args, **kw):
        self.clearLoop()
        self.loopOp = loopOp
        self.loopAnim = anim
        self.loopArgs = args
        self.loopKw = kw
        self._ReducedAnimationMixer__startLoopIfAble()
        self.actor.setControlEffect(anim, 1)

    setLoop = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'animmixer')(setLoop)
    
    def __startLoopIfAble(self):
        if not (self.actionAnim) and self.loopOp:
            self.loopOp(self.actor, self.loopAnim, *self.loopArgs, **self.loopArgs)
        

    _ReducedAnimationMixer__startLoopIfAble = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'animmixer')(__startLoopIfAble)
    
    def clearLoop(self):
        if self.loopAnim:
            self.loopAnim = None
            self.loopOp = None
        

    clearLoop = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'animmixer')(clearLoop)
    
    def __getPlayIval(self, newAnim, fromFrame, toFrame, duration = 0):
        pDuration = duration
        if not pDuration:
            pDuration = Actor.getDuration(self.actor, newAnim, None, fromFrame, toFrame)
        
        if pDuration == None:
            return Sequence()
        
        if pDuration == 0.0:
            return Sequence()
        
        playRate = Actor.getPlayRate(self.actor, newAnim)
        if playRate:
            pDuration /= abs(playRate)
        
        context = self.nextActionContext()
        return Sequence(Func(self.setAction, newAnim, context), Wait(pDuration + 1), Func(self.clearAction, context))

    _ReducedAnimationMixer__getPlayIval = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'animmixer')(__getPlayIval)
    
    def __processActorInterval(self, actorInterval):
        actorInterval.resetControls(None)
        context = self.nextActionContext()
        return Sequence(Func(self.setAction, actorInterval.animName, context), actorInterval, Func(self.clearAction, context))

    _ReducedAnimationMixer__processActorInterval = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'animmixer')(__processActorInterval)
    
    def play(self, newAnim, fromFrame = None, toFrame = None, blendInT = 0, blendOutT = 0, blendInto = None):
        ival = self._ReducedAnimationMixer__getPlayIval(newAnim, fromFrame, toFrame)
        if ival:
            Actor.play(self.actor, newAnim, fromFrame = fromFrame, toFrame = toFrame)
            ival.start()
            ival.setT(0.01)
            self.addIvalToOwnedList(ival)
        

    play = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'animmixer')(play)
    
    def loop(self, newAnim, rate = 1.0, restart = True, fromFrame = None, toFrame = None, blendT = 0, blendDelay = 0):
        self.setLoop(Actor.loop, newAnim, restart = restart, fromFrame = fromFrame, toFrame = toFrame)
        Actor.loop(self.actor, newAnim, restart = restart, fromFrame = fromFrame, toFrame = toFrame)
        self.actor.setPlayRate(rate, newAnim)

    loop = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'animmixer')(loop)
    
    def pingpong(self, newAnim, rate = 1.0, fromFrame = None, toFrame = None, blendT = 0):
        self.setLoop(Actor.pingpong, newAnim, fromFrame = fromFrame, toFrame = toFrame)
        Actor.pingpong(self.actor, newAnim, fromFrame = fromFrame, toFrame = toFrame)
        self.actor.setPlayRate(rate, newAnim)

    pingpong = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'animmixer')(pingpong)
    
    def pose(self, newAnim, frame, partName = None, blendT = 0):
        self.setLoop(Actor.pose, newAnim, frame)
        Actor.pose(self.actor, newAnim, frame)

    pose = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'animmixer')(pose)
    
    def actorInterval(self, actorInterval, partName = None, blendInT = 0, blendOutT = 0, blendInto = None):
        return self._ReducedAnimationMixer__processActorInterval(actorInterval)

    actorInterval = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'animmixer')(actorInterval)
    
    def cleanup(self):
        self.clearAction(self.nextActionContext())
        self.clearLoop()
        AnimationMixer.cleanup(self)
        Actor.setControlEffect(self.actor, None, 1.0)

    cleanup = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'animmixer')(cleanup)

