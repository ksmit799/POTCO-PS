# File: C (Python 2.4)

from pandac.PandaModules import *
from direct.showbase.InputStateGlobal import inputState
from direct.fsm import ClassicFSM, State
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import reduceAngle, fitSrcAngle2Dest
from direct.showbase.PythonUtil import clampScalar, getSetter
from direct.showbase.PythonUtil import ParamObj
from direct.task import Task
from otp.otpbase import OTPGlobals
from pirates.pirate import CameraMode
from pirates.piratesbase import PiratesGlobals

class CannonCamera(CameraMode.CameraMode, NodePath, ParamObj):
    notify = DirectNotifyGlobal.directNotify.newCategory('CannonCamera')
    
    class ParamSet(ParamObj.ParamSet):
        Params = {
            'minH': -60.0,
            'maxH': 60.0,
            'minP': -12.0,
            'maxP': 24,
            'sensitivityH': 0.070000000000000007,
            'sensitivityP': 0.029999999999999999 }

    CamParentPos = (Vec3(0, -6, 3), Vec3(0, -2, 0))
    
    def __init__(self, params = None):
        ParamObj.__init__(self)
        NodePath.__init__(self, self._getTopNodeName())
        CameraMode.CameraMode.__init__(self)
        self.camParent = self.attachNewNode('cannonCamParent')
        self.inputStateTokens = []
        self._paramStack = []
        self.keyboardDelta = (0, 0)
        self.keyboardRate = 1000
        if params is None:
            self.setDefaultParams()
        else:
            params.applyTo(self)

    
    def destroy(self):
        self._paramStack = None
        self.camParent = None
        self.cannonProp = None
        CameraMode.CameraMode.destroy(self)
        NodePath.removeNode(self)
        ParamObj.destroy(self)

    
    def _getTopNodeName(self):
        return 'CannonCam'

    
    def start(self, cannonProp):
        self.cannonProp = cannonProp
        CameraMode.CameraMode.start(self)

    
    def getName(self):
        return 'Cannon'

    
    def pushParams(self):
        self._paramStack.append(self.ParamSet(self))

    
    def popParams(self):
        if len(self._paramStack):
            self._paramStack.pop().applyTo(self)
        else:
            CannonCamera.notify.warning('param stack underflow')

    
    def getMinH(self):
        return self.minH

    
    def setMinH(self, minH):
        self.minH = minH

    
    def getMaxH(self):
        return self.maxH

    
    def setMaxH(self, maxH):
        self.maxH = maxH

    
    def getMinP(self):
        return self.minP

    
    def setMinP(self, minP):
        self.minP = minP

    
    def getMaxP(self):
        return self.maxP

    
    def setMaxP(self, maxP):
        self.maxP = maxP

    
    def getSensitivityH(self):
        return self.sensitivityH

    
    def setSensitivityH(self, sensitivityH):
        self.sensitivityH = sensitivityH

    
    def getSensitivityP(self):
        return self.sensitivityP

    
    def setSensitivityP(self, sensitivityP):
        self.sensitivityP = sensitivityP

    
    def enterActive(self):
        CameraMode.CameraMode.enterActive(self)
        base.camLens.setMinFov(PiratesGlobals.CannonCameraFov)
        base.camNode.setLodCenter(self)
        if base.wantEnviroDR:
            base.enviroCamNode.setLodCenter(self)
        
        if self.cannonProp.ship:
            self.reparentTo(self.cannonProp.ship.avCannonView)
        else:
            self.reparentTo(self.cannonProp.hNode)
        camera.reparentTo(self.camParent)
        self.camParent.clearTransform()
        self.clearTransform()
        camera.clearTransform()
        self.camParent.setPosHpr(*self.CamParentPos)
        self.camParent.setR(render, 0.0)

    
    def _startKeyboardUpdateTask(self):
        self._stopKeyboardUpdateTask()
        self.inputStateTokens = []
        ist = self.inputStateTokens
        ist.append(inputState.watchWithModifiers('forward', 'arrow_up', inputSource = inputState.ArrowKeys))
        ist.append(inputState.watchWithModifiers('reverse', 'arrow_down', inputSource = inputState.ArrowKeys))
   