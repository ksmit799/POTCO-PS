# File: P (Python 2.4)

from direct.controls.GravityWalker import GravityWalker
from direct.showbase.InputStateGlobal import inputState
from pandac.PandaModules import *
from direct.task.Task import Task

class PiratesGravityWalker(GravityWalker):
    notify = directNotify.newCategory('PiratesGravityWalker')
    
    def __init__(self, *args, **kwargs):
        GravityWalker.__init__(self, *args, **args)
        self.predicting = 0

    
    def handleAvatarControls(self, task):
        run = inputState.isSet('run')
        forward = inputState.isSet('forward')
        reverse = inputState.isSet('reverse')
        turnLeft = inputState.isSet('turnLeft')
        turnRight = inputState.isSet('turnRight')
        slideLeft = inputState.isSet('slideLeft')
        slideRight = inputState.isSet('slideRight')
        jump = inputState.isSet('jump')
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
        if (turnLeft or self.avatarControlRotateSpeed) and turnRight:
            pass
        self.rotationSpeed = -(self.avatarControlRotateSpeed)
        if self.speed and self.slideSpeed:
            self.speed *= GravityWalker.DiagonalFactor
            self.slideSpeed *= GravityWalker.DiagonalFactor
        
        debugRunning = inputState.isSet('debugRunning')
        if debugRunning:
            self.speed *= base.debugRunningMultiplier
            self.slideSpeed *= base.debugRunningMultiplier
            self.rotationSpeed *= 1.25
        
        if self.needToDeltaPos:
            self.setPriorParentVector()
            self.needToDeltaPos = 0
        
        if self.wantDebugIndicator:
            self.displayDebugInfo()
        
        
        def sendLandMessage(impact):
            if impact > -15.0:
                messenger.send('jumpEnd')
            elif -15.0 >= impact:
                pass
            elif impact > -15.0:
                messenger.send('jumpLand')
                self.startJumpDelay(0.5)
            else:
                messenger.send('jumpLandHard')
                self.startJumpDelay(0.5)

        
        def predictHeightAndVelocity(aheadFrames):
            dt = globalClock.getDt()
            vel = self.lifter.getVelocity()
            height = self.getAirborneHeight()
            grav = self.lifter.getGravity()
            dtt = dt * aheadFrames
            futureHeight = height + vel * dtt + 0.5 * grav * dtt * dtt
            futureVel = vel - grav * dtt
            return (futureHeight, futureVel)

        if self.lifter.isOnGround():
            if self.isAirborne:
                self.isAirborne = 0
                self.predicting = 0
                impact = self.lifter.getImpactVelocity()
                sendLandMessage(impact)
            
            self.priorParent = Vec3.zero()
            if jump and self.mayJump:
                
                def doJump(task):
                    self.lifter.addVelocity(self.avatarControlJumpForce)
                    self.isAirborne = 1
                    self.predicting = 1

                if not taskMgr.hasTaskNamed('jumpWait'):
                    taskMgr.doMethodLater(0.20000000000000001, doJump, 'jumpWait')
                    messenger.send('jumpStart')
                
            
        elif self.isAirborne and self.predicting:
            (futureHeight, futureVel) = predictHeightAndVelocity(2)
            if futureHeight <= 0.0:
                self.isAirborne = 0
                self.predicting = 0
                sendLandMessage(futureVel)
            
        elif self.getAirborneHeight() > 2.0:
            self.isAirborne = 1
            self.predicting = 1
        
        self._PiratesGravityWalker__oldPosDelta = self.avatarNodePath.getPosDelta(render)
        self._PiratesGravityWalker__oldDt = ClockObject.getGlobalClock().getDt()
        dt = self._PiratesGravityWalker__oldDt
        if not self.speed and self.slideSpeed and self.rotationSpeed:
            pass
        self.moving = self.priorParent != Vec3.zero()
        if self.moving:
            distance = dt * self.speed
            slideDistance = dt * self.slideSpeed
            rotation = dt * self.rotationSpeed
            if distance and slideDistance or self.priorParent != Vec3.zero():
                rotMat = Mat3.rotateMatNormaxis(self.avatarNodePath.getH(), Vec3.up())
                if self.isAirborne:
                    forward = Vec3.forward()
                else:
                    contact = self.lifter.getContactNormal()
                    forward = contact.cross(Vec3.right())
                    forward.normalize()
                self.vel = Vec3(forward * distance)
                if slideDistance:
                    if self.isAirborne:
                        right = Vec3.right()
                    else:
                        right = forward.cross(contact)
                        right.normalize()
                    self.vel = Vec3(self.vel + right * slideDistance)
                
                self.vel = Vec3(rotMat.xform(self.vel))
                step = self.vel + self.priorParent * dt
                self.avatarNodePath.setFluidPos(Point3(self.avatarNodePath.getPos() + step))
                self.vel /= dt
            
            self.avatarNodePath.setH(self.avatarNodePath.getH() + rotation)
        else:
            self.vel.set(0.0, 0.0, 0.0)
        if self.moving or jump:
            messenger.send('avatarMoving')
        
        return task.cont

    
    def disableJump(self):
        if base.localAvatar.controlManager.forceAvJumpToken is None:
            base.localAvatar.controlManager.disableAvatarJump()
        

    
    def enableJump(self):
        if base.localAvatar.controlManager.forceAvJumpToken is not None:
            base.localAvatar.controlManager.enableAvatarJump()
        

    
    def abortJump(self):
        taskMgr.remove('jumpWait')

    
    def reset(self):
        GravityWalker.reset(self)
        self.abortJump()

    
    def disableAvatarControls(self):
        GravityWalker.disableAvatarControls(self)
        self.abortJump()


