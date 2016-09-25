# File: B (Python 2.4)

from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class BlockShield(PooledEffect, EffectController):
    
    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.effectModel = loader.loadModel('models/effects/pir_m_efx_chr_blockShield')
        self.effectModel.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.effectColor = Vec4(0.40000000000000002, 0.59999999999999998, 1, 1)
        self.effectModel.setBillboardPointWorld(2)
        self.effectModel.setDepthWrite(0)
        self.effectModel.setColorScaleOff()
        self.effectModel.setTwoSided(1)
        self.effectModel.setLightOff()
        self.effectModel.setTransparency(1)
        self.effectModel.reparentTo(self)
        self.effectModel.setColorScale(0, 0, 0, 0)

    
    def createTrack(self):
        self.effectModel.setColorScale(self.effectColor)
        textureStage = self.effectModel.findAllTextureStages()[0]
        fadeOut = LerpColorScaleInterval(self.effectModel, 0.20000000000000001, Vec4(0, 0, 0, 0), startColorScale = self.effectColor, blendType = 'easeIn')
        scaleIval = LerpScaleInterval(self.effectModel, 0.20000000000000001, Vec3(1, 1, 1.2), startScale = Vec3(1, 1, 0.5))
        uvScroll = LerpFunctionInterval(self.setNewUVs, 0.40000000000000002, toData = 0.5, fromData = 0.0, extraArgs = [
            self.effectModel,
            textureStage])
        self.startEffect = Parallel(Sequence(Wait(0.20000000000000001), fadeOut), scaleIval, uvScroll)
        self.endEffect = Sequence(Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, self.endEffect)

    
    def setEffectColor(self, color):
        self.effectColor = color

    
    def setNewUVs(self, offset, part, ts):
        part.setTexOffset(ts, 0.0, offset)

    
    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    
    def destroy(self):
        self.stop()
        if self.track:
            self.track = None
        
        self.removeNode()
        EffectController.destroy(self)
        PooledEffect.destroy(self)


