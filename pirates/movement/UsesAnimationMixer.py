from direct.interval.IntervalGlobal import ActorInterval
from direct.actor.Actor import Actor
from direct.fsm.FSM import FSM
from direct.showbase.PythonUtil import report
from pirates.movement.AnimationMixer import ReducedAnimationMixer

class UsesAnimationMixer:
    
    def __init__(self, animationMixerType = None):
        if hasattr(self, 'animationMixer') and self.animationMixer:
            if not isinstance(self.animationMixer, animationMixerType):
                pass
            1
            return None
        
        self._UsesAnimationMixer__mixer = None
        if animationMixerType:
            self.animationMixer = animationMixerType(self)
        else:
            self.animationMixer = None
        self.reducedMixer = None

    
    def delete(self):
        if self.animationMixer:
            self.animationMixer.delete()
            self.animationMixer = None
        
        if self.reducedMixer:
            self.reducedMixer.delete()
            self.reducedMixer = None
        

    
    def play(self, *args, **kwargs):
        if self._UsesAnimationMixer__mixer:
            defaultBlendT = self._UsesAnimationMixer__mixer.defaultBlendT
        else:
            defaultBlendT = 0
        blendInT = kwargs.pop('blendInT', defaultBlendT)
        blendOutT = kwargs.pop('blendOutT', defaultBlendT)
        blendInto = kwargs.pop('blendInto', None)
        if self._UsesAnimationMixer__mixer:
            self._UsesAnimationMixer__mixer.play(blendInT = blendInT, blendOutT = blendOutT, blendInto = blendInto, *args, **args)
        else:
            Actor.play(self, *args, **args)

    play = report(types = [
        'args',
        'deltaStamp'], dConfigParam = [
        'animmixer',
        'jump'])(play)
    
    def loop(self, *args, **kwargs):
        if self._UsesAnimationMixer__mixer:
            defaultBlendT = self._UsesAnimationMixer__mixer.defaultBlendT
        else:
            defaultBlendT = 0
        blendT = kwargs.pop('blendT', defaultBlendT)
        blendDelay = kwargs.pop('blendDelay', 0)
        if self._UsesAnimationMixer__mixer:
            self._UsesAnimationMixer__mixer.loop(blendT = blendT, blendDelay = blendDelay, *args, **args)
        elif 'rate' in kwargs:
            rate = kwargs.pop('rate')
            Actor.loop(self, *args, **args)
            self.setPlayRate(rate, args[0])
        else:
            Actor.loop(self, *args, **args)

    loop = report(types = [
        'args',
        'deltaStamp'], dConfigParam = [
        'animmixer',
        'jump'])(loop)
    
    def pingpong(self, *args, **kwargs):
        if self._UsesAnimationMixer__mixer:
            defaultBlendT = self._UsesAnimationMixer__mixer.defaultBlendT
        else:
            defaultBlendT = 0
        blendT = kwargs.pop('blendT', defaultBlendT)
        if self._UsesAnimationMixer__mixer:
            self._UsesAnimationMixer__mixer.pingpong(blendT = blendT, *args, **args)
        else:
            Actor.pingpong(self, *args, **args)

    pingpong = report(types = [
        'args',
        'deltaStamp'], dConfigParam = [
        'animmixer',
        'jump'])(pingpong)
    
    def pose(self, *args, **kwargs):
        if self._UsesAnimationMixer__mixer:
            defaultBlendT = self._UsesAnimationMixer__mixer.defaultBlendT
        else:
            defaultBlendT = 0
        blendT = kwargs.pop('blendT', defaultBlendT)
        if self._UsesAnimationMixer__mixer:
            self._UsesAnimationMixer__mixer.pose(blendT = blendT, *args, **args)
        else:
            Actor.pose(self, *args, **args)

    pose = report(types = [
        'args',
        'deltaStamp'], dConfigParam = [
        'animmixer',
        'jump'])(pose)
    
    def stop(self, *args, **kwargs):
        if self._UsesAnimationMixer__mixer:
            self._UsesAnimationMixer__mixer.stop(*args, **args)
        else:
            Actor.stop(self, *args, **args)

    stop = report(types = [
        'args',
        'deltaStamp'], dConfigParam = [
        'animmixer',
        'jump'])(stop)
    
    def actorInterval(self, *args, **kwargs):
        mixingWanted = kwargs.pop('mixingWanted', bool(self._UsesAnimationMixer__mixer))
        if mixingWanted and self._UsesAnimationMixer__mixer:
            defaultBlendT = self._UsesAnimationMixer__mixer.defaultBlendT
        elif mixingWanted and self.animationMixer:
            defaultBlendT = self.animationMixer.defaultBlendT
        else:
            defaultBlendT = 0
        blendInT = kwargs.pop('blendInT', defaultBlendT)
        blendOutT = kwargs.pop('blendOutT', defaultBlendT)
        blendInto = kwargs.pop('blendInto', None)
        if mixingWanted:
            partName = kwargs.get('partName', None)
            return self._UsesAnimationMixer__mixer.actorInterval(ActorInterval(self, *args, **args), partName, blendInT, blendOutT, blendInto)
        else:
            return ActorInterval(self, *args, **args)

    actorInterval = report(types = [
        'args',
        'deltaStamp'], dConfigParam = [
        'animmixer',
        'jump'])(actorInterval)
    
    def disableMixing(self):
        if self._UsesAnimationMixer__mixer:
            self._UsesAnimationMixer__mixer.cleanup()
            self._UsesAnimationMixer__mixer = None
        
        Actor.disableBlend(self)
        Actor.stop(self)

    disableMixing = report(types = [
        'args',
        'deltaStamp'], dConfigParam = [
        'animmixer',
        'jump'])(disableMixing)
    
    def enableMixing(self):
        if self._UsesAnimationMixer__mixer != self.animationMixer:
            self.disableMixing()
        
        self._UsesAnimationMixer__mixer = self.animationMixer
        if self._UsesAnimationMixer__mixer:
            Actor.enableBlend(self)
            self._UsesAnimationMixer__mixer.cleanup()
        

    enableMixing = report(types = [
        'args',
        'deltaStamp'], dConfigParam = [
        'animmixer',
        'jump'])(enableMixing)
    
    def enableReducedMixing(self):
        if not self.reducedMixer:
            self.reducedMixer = ReducedAnimationMixer(self)
        
        if self._UsesAnimationMixer__mixer != self.reducedMixer:
            self.disableMixing()
        
        self._UsesAnimationMixer__mixer = self.reducedMixer
        self._UsesAnimationMixer__mixer.cleanup()

    enableReducedMixing = report(types = [
        'args',
        'deltaStamp'], dConfigParam = [
        'animmixer',
        'jump'])(enableReducedMixing)
    
    def isMixing(self):
        return self._UsesAnimationMixer__mixer is not None

    
    def printMixer(self):
        print self._UsesAnimationMixer__mixer


