# File: E (Python 2.4)

from pandac.PandaModules import *

class EffectController:
    particleDummy = None
    
    def __init__(self):
        self.track = None
        self.startEffect = None
        self.endEffect = None
        self.f = None
        self.p0 = None

    
    def createTrack(self):
        pass

    
    def destroy(self):
        self.finish()
        if self.f:
            self.f.cleanup()
        
        self.f = None
        self.p0 = None
        self.removeNode()

    destroy = report(types = [
        'args'], dConfigParam = 'quest-indicator')(destroy)
    
    def cleanUpEffect(self):
        self.setPosHpr(0, 0, 0, 0, 0, 0)
        if self.f:
            self.f.disable()
        
        self.detachNode()

    cleanUpEffect = report(types = [
        'args'], dConfigParam = 'quest-indicator')(cleanUpEffect)
    
    def reallyCleanUpEffect(self):
        self.cleanUpEffect()
        self.finish()

    reallyCleanUpEffect = report(types = [
        'args'], dConfigParam = 'quest-indicator')(reallyCleanUpEffect)
    
    def play(self, lod = None):
        if lod != None:
            
            try:
                self.createTrack(lod)
            except TypeError:
                e = None
                raise TypeError('Error loading %s effect.' % self.__class__.__name__)
            

        self.createTrack()
        self.track.start()

    play = report(types = [
        'args'], dConfigParam = 'quest-indicator')(play)
    
    def stop(self):
        if self.track:
            self.track.pause()
            self.track = None
        
        if self.startEffect:
            self.startEffect.pause()
            self.startEffect = None
        
        if self.endEffect:
            self.endEffect.pause()
            self.endEffect = None
        
        self.cleanUpEffect()

    stop = report(types = [
        'args'], dConfigParam = 'quest-indicator')(stop)
    
    def finish(self):
        if self.track:
            self.track.pause()
            self.track = None
        
        if self.startEffect:
            self.startEffect.pause()
            self.startEffect = None
        
        if self.endEffect:
            self.endEffect.pause()
            self.endEffect = None
        

    finish = report(types = [
        'args'], dConfigParam = 'quest-indicator')(finish)
    
    def startLoop(self, lod = None):
        if lod != None:
            
            try:
                self.createTrack(lod)
            except TypeError:
                e = None
                raise TypeError('Error loading %s effect.' % self.__class__.__name__)
            

        self.createTrack()
        if self.startEffect:
            self.startEffect.start()
        

    startLoop = report(types = [
        'args'], dConfigParam = 'quest-indicator')(startLoop)
    
    def stopLoop(self):
        if self.startEffect:
            self.startEffect.pause()
            self.startEffect = None
        
        if self.endEffect and not self.endEffect.isPlaying():
            self.endEffect.start()
        

    stopLoop = report(types = [
        'args'], dConfigParam = 'quest-indicator')(stopLoop)
    
    def getTrack(self):
        if not self.track:
            self.createTrack()
        
        return self.track

    getTrack = report(types = [
        'args'], dConfigParam = 'quest-indicator')(getTrack)
    
    def enableEffect(self):
        if self.f and self.particleDummy:
            self.f.start(self, self.particleDummy)
        elif self.f:
            self.f.start(self, self)
        

    enableEffect = report(types = [
        'args'], dConfigParam = 'quest-indicator')(enableEffect)
    
    def disableEffect(self):
        if self.f:
            self.f.disable()
        

    disableEffect = report(types = [
        'args'], dConfigParam = 'quest-indicator')(disableEffect)

