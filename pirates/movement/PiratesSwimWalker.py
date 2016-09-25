# File: P (Python 2.4)

from direct.showbase.InputStateGlobal import inputState
from direct.controls.SwimWalker import SwimWalker
from pandac.PandaModules import *
from direct.task.Task import Task

class PiratesSwimWalker(SwimWalker):
    
    def handleAvatarControls(self, task):
        if not self.lifter.hasContact():
            messenger.send('walkerIsOutOfWorld', [
                self.avatarNodePath])
        
        forward = inputState.isSet('forward')
        reverse = inputState.isSet('reverse')
        if not inputState.isSet('turnLeft'):
            pass
        turnLeft = inputState.isSet('slideLeft')
        if not inputState.isSet('turnRight'):
            pass
        turnRight = inputState.isSet('slideRight')
        slideLeft = inputState.isSet('slideLeft')
        slideRight = inputState.isSet('slideRight')
        if base.localAvatar.getAutoRun():
            forward = 1
            reverse = 0
        
        if (forward or self.avatarControlForwardSpeed) and reverse:
            pass
        self.speed = -(self.avatarControlReverseSpeed)
        if not reverse and slideLeft or -(self.avatarControlReverseSpeed) * 0.75:
            if not reverse and slideRight or self.avatarControlReverseSpeed * 0.75:
                if (slideLeft or -(self.avatarControlForwardSpeed) * 0.75) and slideRight:
                    pass
        self.slideSpeed = self.avatarControlForwardSpeed * 0.75
        if not slideLeft:
            pass
        if not slideRight:
            if (turnLeft or self.avatarControlRotateSpeed) and turnRight:
                pass
        self.rotationSpeed = -(self.avatarControlRotateSpeed)
        if self.wantDebugIndicator:
            self.displayDebugInfo()
        
        dt = ClockObject.getGlobalClock().getDt()
        if not self.speed and self.slideSpeed:
            pass
        self.moving = self.rotationSpeed
        if self.moving:
            if self.stopThisFrame:
                distance = 0.0
                slideDistance = 0.0
                rotation = 0.0
                self.stopThisFrame = 0
            else:
                distance = dt * self.speed
                slideDistance = dt * self.slideSpeed
                rotation = dt * self.rotationSpeed
            self.vel = Vec3(Vec3.forward() * distance + Vec3.right() * slideDistance)
            if self.vel != Vec3.zero():
                rotMat = Mat3.rotateMatNormaxis(self.avatarNodePath.getH(), Vec3.up())
                step = rotMat.xform(self.vel)
                self.avatarNodePath.setFluidPos(Point3(self.avatarNodePath.getPos() + step))
            
            self.avatarNodePath.setH(self.avatarNodePath.getH() + rotation)
            messenger.send('avatarMoving')
        else:
            self.vel.set(0.0, 0.0, 0.0)
        return task.cont


