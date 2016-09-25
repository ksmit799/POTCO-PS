# File: L (Python 2.4)

from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui.GameOptions import Options
from PooledEffect import PooledEffect
from EffectController import EffectController

class LanternGlow(PooledEffect, EffectController):
    
    def __init__(self, effectParent = None, billboardOffset = 1.0):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        if effectParent:
            self.reparentTo(effectParent)
        
        self.glow = loader.loadModel('models/effects/lanternGlow')
        self.glow.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingColor, ColorBlendAttrib.OOneMinusIncomingAlpha))
        self.glow.setBillboardPointEye(billboardOffset)
        self.glow.setColorScaleOff()
        self.glow.setLightOff()
        self.glow.setFogOff()
        self.glow.reparentTo(self)
        self.glow.setScale(1.0)
        self.glow.setPos(Vec3(0, 0, -0.14999999999999999))
        self.glowHalo = loader.loadModel('models/effects/gypsyBallGlow').find('**/glow_aura')
        self.glowHalo.reparentTo(self.glow)
        self.glowHalo.setColorScale(0.80000000000000004, 0.69999999999999996, 0.29999999999999999, 0.10000000000000001)
        self.glowHalo.setScale(0.5)
        self.fadeIval = None
        self.scaleIval = None

    
    def createTrack(self, lod = None):
        scaleUpHalo = self.glow.scaleInterval(0.14999999999999999, 1.0, startScale = 0.90000000000000002, blendType = 'easeInOut', name = 'LanternGlow')
        scaleDownHalo = self.glow.scaleInterval(0.14999999999999999, 0.90000000000000002, startScale = 1.0, blendType = 'easeInOut', name = 'LanternGlow')
        self.scaleIval = Sequence(scaleDownHalo, scaleUpHalo)
        self.startEffect = Sequence(Func(self.scaleIval.loop))
        self.endEffect = Sequence(Func(self.scaleIval.finish))
        self.track = Sequence(self.startEffect, Wait(2.0), self.endEffect)

    
    def enableEffect(self):
        if self.scaleIval:
            self.scaleIval.loop()
        

    
    def disableEffect(self):
        if self.scaleIval:
            self.scaleIval.pause()
        

    
    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    
    def destroy(self):
        if self.scaleIval:
            self.scaleIval.finish()
        
        self.glow.removeNode()
        EffectController.destroy(self)
        PooledEffect.destroy(self)


