# File: M (Python 2.4)

from direct.fsm.FSM import FSM
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import Enum
from pirates.piratesbase import PiratesGlobals
from pirates.pirate import Human
import random
import types
from direct.distributed.ClockDelta import *
from direct.showbase.InputStateGlobal import inputState
from pirates.battle import EnemyGlobals
from pirates.effects.WaterRipple import WaterRipple
from pirates.inventory import ItemGlobals
WALK_CUTOFF = 0.5
NPC_WALK_CUTOFF = 0.5
RUN_CUTOFF = PiratesGlobals.ToonForwardSpeed
NPC_RUN_CUTOFF = 17.0
STATE_MOTION = {
    'Idle': PiratesGlobals.STAND_INDEX,
    'Run': PiratesGlobals.RUN_INDEX,
    'WalkForward': PiratesGlobals.WALK_INDEX,
    'WalkReverse': PiratesGlobals.REVERSE_INDEX,
    'SpinLeft': PiratesGlobals.SPIN_LEFT_INDEX,
    'SpinRight': PiratesGlobals.SPIN_RIGHT_INDEX,
    'StrafeLeft': PiratesGlobals.STRAFE_LEFT_INDEX,
    'StrafeRight': PiratesGlobals.STRAFE_RIGHT_INDEX,
    'StrafeLeftDiag': PiratesGlobals.STRAFE_LEFT_DIAG_INDEX,
    'StrafeRightDiag': PiratesGlobals.STRAFE_RIGHT_DIAG_INDEX,
    'StrafeLeftDiagReverse': PiratesGlobals.STRAFE_LEFT_DIAG_REV_INDEX,
    'StrafeRightDiagReverse': PiratesGlobals.STRAFE_RIGHT_DIAG_REV_INDEX,
    'Airborne': PiratesGlobals.OVER_SOLID_INDEX }
IDLE_SPLASH_ANIMS = [
    ('idle_head_scratch_side', 1.3999999999999999),
    ('idle_head_scratch', 1.0)]
IDLE_SPLASH_PLAY = config.GetBool('want-splash-anims', 1)
IDLE_SPLASH_DELAY = config.GetInt('splash-anims-delay', 60)

class MotionAnimFSM(FSM):
    BLENDAMT = 0.40000000000000002
    GROUNDSTATE = Enum('OverSolid, OverWater')
    ANIMSTATE = Enum('Land, Jump')
    notify = directNotify.newCategory('MotionAnimFSM')
    
    def __init__(self, av):
        FSM.__init__(self, 'MotionAnimFSM')
        self.av = av
        self.groundState = self.GROUNDSTATE.OverSolid
        self.airborneState = False
        self.setAllowAirborne(True)
        self.landIval = None
        self.landRunIval = None
        self.idleJumpIval = None
        self.lastMoveSpeed = 0
        self.zeroSpeedTimer = 0
        self.motionFSMLag = base.config.GetBool('motionfsm-lag', 1)
        self.currentSplash = None
        self.splashAnims = None
        self.splashAnimDelay = None

    
    def cleanup(self):
        if not self.isInTransition():
            FSM.cleanup(self)
        
        self.landIval = None
        self.landRunIval = None
        self.idleJumpIval = None
        if hasattr(self, 'av'):
            self.ignoreAll()
            del self.av
        

    
    def setAnimInfo(self, animInfo, reset = True):
        self.fsmLock.acquire()
        
        try:
            self.animInfo = animInfo
            if reset:
                self.request(self.state)
        finally:
            self.fsmLock.release()


    
    def trackAnimToSpeed(self, task = None):
        self.fsmLock.acquire()
        
        try:
            if self.airborneState != self.av.controlManager.getIsAirborne():
                self.av.b_setAirborneState(not (self.airborneState))
            
            speeds = self.av.controlManager.getSpeeds()
            if speeds:
                if self.av == localAvatar:
                    speeds = (speeds[0], speeds[1], speeds[2], self.av.getTrackedRotation())
                
                self.updateAnimState(*speeds)
            
            if task:
                return task.cont
        finally:
            self.fsmLock.release()


    
    def adjustAnimScale(self, state, moveSpeed, slideSpeed = 0):
        self.fsmLock.acquire()
        
        try:
            currAnimName = self.av.getCurrentAnim()
            if (self.av.isNpc == False or currAnimName != 'walk') and currAnimName != 'run' and currAnimName != 'bayonet_walk' and currAnimName != 'bayonet_run':
                return None
            
            style = self.av.style
            scale = None
            if hasattr(self.av, 'walkAnimScale'):
                scale = self.av.walkAnimScale
            
            if self.av is not localAvatar or style or scale:
                if scale:
                    newScale = moveSpeed * scale
                elif type(style) is not types.StringType:
                    style = style.getBodyShape()
                
                animFileName = self.av.getAnimFilename(self.av.getCurrentAnim())
                animSpeedScale = PiratesGlobals.GetAnimScale(animFileName)
                if animSpeedScale == None:
                    if currAnimName == 'walk' or currAnimName == 'bayonet_walk':
                        animSpeedScale = 0.24399999999999999
                    else:
                        animSpeedScale = 0.029999999999999999
                
                newScale = moveSpeed * animSpeedScale
                avScale = EnemyGlobals.getEnemyScale(self.av)
                if avScale:
                    newScale /= avScale
                
                newScale = max(newScale, 0.25)
                if currAnimName == 'walk' or currAnimName == 'bayonet_walk':
                    animIdx = PiratesGlobals.WALK_INDEX
                else:
                    animIdx = PiratesGlobals.RUN_INDEX
                currPlayRate = self.av.getPlayRate(self.animInfo[animIdx][0])
                if currPlayRate == None or abs(currPlayRate - newScale) < 0.074999999999999997:
                    return None
                
                if animIdx == PiratesGlobals.WALK_INDEX:
                    newAnimInfo = ((self.animInfo[PiratesGlobals.STAND_INDEX][0], self.animInfo[PiratesGlobals.STAND_INDEX][1]), (self.animInfo[PiratesGlobals.WALK_INDEX][0], newScale)) + self.animInfo[2:]
                else:
                    newAnimInfo = ((self.animInfo[PiratesGlobals.STAND_INDEX][0], self.animInfo[PiratesGlobals.STAND_INDEX][1]), (self.animInfo[PiratesGlobals.WALK_INDEX][0], self.animInfo[PiratesGlobals.WALK_INDEX][1]), (self.animInfo[PiratesGlobals.RUN_INDEX][0], newScale)) + self.animInfo[3:]
                if slideSpeed:
                    slideSpeed = max(slideSpeed, 0.45000000000000001)
                    newAnimInfo = ((self.animInfo[PiratesGlobals.STAND_INDEX][0], self.animInfo[PiratesGlobals.STAND_INDEX][1]), (self.animInfo[PiratesGlobals.WALK_INDEX][0], self.animInfo[PiratesGlobals.WALK_INDEX][1]), (self.animInfo[PiratesGlobals.RUN_INDEX][0], self.animInfo[PiratesGlobals.RUN_INDEX][1]), (self.animInfo[PiratesGlobals.REVERSE_INDEX][0], self.animInfo[PiratesGlobals.REVERSE_INDEX][1]), (self.animInfo[PiratesGlobals.STRAFE_LEFT_INDEX][0], slideSpeed), (self.animInfo[PiratesGlobals.STRAFE_RIGHT_INDEX][0], slideSpeed)) + self.animInfo[6:]
                
                self.av.motionFSM.setAnimInfo(newAnimInfo, reset = False)
                self.av.setPlayRate(newScale, self.animInfo[animIdx][0])
        finally:
            self.fsmLock.release()


    
    def updateNPCAnimState(self, forwardSpeed, rotateSpeed = 0, slideSpeed = 0):
        self.fsmLock.acquire()
        
        try:
            animScaleAdjust = False
            if self.canBeAirborne and self.airborneState:
                state = 'Airborne'
            elif slideSpeed >= WALK_CUTOFF:
                if self.av.getAnimFilename('strafe_right'):
                    state = 'StrafeRight'
                else:
                    state = 'WalkForward'
            elif slideSpeed <= -WALK_CUTOFF:
                if self.av.getAnimFilename('strafe_left'):
                    state = 'StrafeLeft'
                else:
                    state = 'WalkForward'
            elif forwardSpeed >= NPC_RUN_CUTOFF:
                state = 'Run'
                animScaleAdjust = True
            elif forwardSpeed > NPC_WALK_CUTOFF:
                state = 'WalkForward'
                animScaleAdjust = True
            elif rotateSpeed > 0.0:
                if self.av.getAnimFilename('spin_left'):
                    state = 'SpinLeft'
                else:
                    state = 'WalkForward'
            elif rotateSpeed < 0.0:
                if self.av.getAnimFilename('spin_right'):
                    state = 'SpinRight'
                else:
                    state = 'WalkForward'
            else:
                state = 'Idle'
            zeroSpeedLimit = 0.10000000000000001
            if globalClock.getFrameTime() - self.zeroSpeedTimer < zeroSpeedLimit and self.motionFSMLag:
                if state != self.state and self.state != 'Idle':
                    return None
                
            
            if animScaleAdjust:
                self.adjustAnimScale(state, forwardSpeed, slideSpeed)
            
            if self.state != state:
                if self.isInTransition():
                    self.demand(state)
                else:
                    self.request(state)
            
            self.lastMoveSpeed = forwardSpeed
            self.zeroSpeedTimer = globalClock.getFrameTime()
        finally:
            self.fsmLock.release()


    
    def updateAnimState(self, forwardSpeed, rotateSpeed, slideSpeed = 0.0, trackedRotation = 0.0):
        if self.av.getGameState() == 'Fishing':
            return None
        
        self.fsmLock.acquire()
        
        try:
            if self.canBeAirborne and self.airborneState:
                state = 'Airborne'
            elif forwardSpeed >= WALK_CUTOFF and slideSpeed >= WALK_CUTOFF:
                state = 'StrafeRightDiag'
            elif forwardSpeed >= WALK_CUTOFF and slideSpeed <= -WALK_CUTOFF:
                state = 'StrafeLeftDiag'
            elif forwardSpeed >= WALK_CUTOFF and trackedRotation > 1:
                state = 'StrafeRightDiag'
            elif forwardSpeed >= WALK_CUTOFF and trackedRotation < -1:
                state = 'StrafeLeftDiag'
            elif forwardSpeed >= RUN_CUTOFF:
                state = 'Run'
            elif forwardSpeed >= WALK_CUTOFF:
                state = 'WalkForward'
                self.adjustAnimScale(state, forwardSpeed)
            elif forwardSpeed <= -WALK_CUTOFF and slideSpeed >= WALK_CUTOFF:
                state = 'StrafeRightDiagReverse'
            elif forwardSpeed <= -WALK_CUTOFF and slideSpeed <= -WALK_CUTOFF:
                state = 'StrafeLeftDiagReverse'
            elif forwardSpeed <= -WALK_CUTOFF:
                state = 'WalkReverse'
            elif slideSpeed >= WALK_CUTOFF:
                state = 'StrafeRight'
            elif slideSpeed <= -WALK_CUTOFF:
                state = 'StrafeLeft'
            elif rotateSpeed > 0.0 or trackedRotation < 0:
                state = 'SpinLeft'
            elif rotateSpeed < 0.0 or trackedRotation > 0:
                state = 'SpinRight'
            else:
                state = 'Idle'
            if self.state != state:
                if self.av.doId < 300000000:
                    pass
                1
                if self.isInTransition():
                    self.demand(state)
                else:
                    self.request(state)
                if self.av.isLocal() and self.av.getGameState() == 'Emote':
                    messenger.send('localAvatarExitEmote')
                
                if not self.av.isLocal() and self.av.getGameState() == 'Emote':
                    self.av.playEmote(self.av.emoteId)
                
        finally:
            self.fsmLock.release()


    
    def setAllowAirborne(self, allow):
        self.canBeAirborne = allow

    
    def handleAirborneEvent(self, event):
        if event == 'Jump':
            self.av.b_playMotionAnim(self.ANIMSTATE.Jump)
        
        if event == 'Land':
            self.av.b_playMotionAnim(self.ANIMSTATE.Land)
        

    handleAirborneEvent = report(types = [
        'args',
        'deltaStamp'], dConfigParam = [
        'jump'])(handleAirborneEvent)
    
    def playMotionAnim(self, anim, local = True):
        if anim == self.ANIMSTATE.Jump:
            if local:
                self.jump()
            else:
                self.jump()
        elif anim == self.ANIMSTATE.Land:
            if local:
                speeds = self.av.controlManager.getSpeeds()
                if speeds[0] == 0.0:
                    self.land()
                else:
                    self.landRun()
            else:
                self.land()
        

    playMotionAnim = report(types = [
        'args',
        'deltaStamp'], dConfigParam = [
        'jump'])(playMotionAnim)
    
    def jump(self):
        self.fsmLock.acquire()
        
        try:
            animInfo = ItemGlobals.getJumpAnimInfo(self.av.getCurrentWeapon())
            if self.state == 'Idle':
                startFrame = animInfo[1]
                endFrame = animInfo[3]
                if self.idleJumpIval:
                    self.idleJumpIval.finish()
                
                self.idleJumpIval = self.av.actorInterval(animInfo[0], startFrame = startFrame, endFrame = endFrame, playRate = 1.5, blendInT = 0.0, blendOutT = self.BLENDAMT * 0.5)
                self.idleJumpIval.start()
            else:
                startFrame = animInfo[2]
                endFrame = animInfo[3]
                self.av.play(animInfo[0], fromFrame = startFrame, toFrame = endFrame, blendInT = self.BLENDAMT * 0.5, blendOutT = self.BLENDAMT * 0.5)
        finally:
            self.fsmLock.release()


    jump = report(types = [
        'args',
        'deltaStamp'], dConfigParam = [
        'jump'])(jump)
    
    def land(self):
        self.fsmLock.acquire()
        
        try:
            animInfo = ItemGlobals.getJumpAnimInfo(self.av.getCurrentWeapon())
            if self.landIval:
                self.landIval.finish()
            
            startFrame = animInfo[3]
            endFrame = animInfo[4]
            self.landIval = self.av.actorInterval(animInfo[0], startFrame = startFrame, endFrame = endFrame, blendInT = 0.0, blendOutT = self.BLENDAMT * 0.5)
            self.landIval.start()
        finally:
            self.fsmLock.release()


    land = report(types = [
        'args',
        'deltaStamp'], dConfigParam = [
        'jump'])(land)
    
    def landRun(self):
        self.fsmLock.acquire()
        
        try:
            if not self.landRunIval:
                animInfo = ItemGlobals.getJumpAnimInfo(self.av.getCurrentWeapon())
                startFrame = animInfo[3] + 1
                endFrame = startFrame + 5
                self.landRunIval = self.av.actorInterval(animInfo[0], startFrame = startFrame, endFrame = endFrame, blendInT = 0.0, blendOutT = 0.14999999999999999)
            
            self.landRunIval.start()
        finally:
            self.fsmLock.release()


    landRun = report(types = [
        'args',
        'deltaStamp'], dConfigParam = [
        'jump'])(landRun)
    
    def setAirborneState(self, airborneState):
        self.airborneState = airborneState

    setAirborneState = report(types = [
        'args',
        'deltaStamp'], dConfigParam = [
        'jump'])(setAirborneState)
    
    def getAirborneState(self):
        return self.airborneState

    getAirborneState = report(types = [
        'args',
        'deltaStamp'], dConfigParam = [
        'jump'])(getAirborneState)
    
    def isAirborne(self):
        return self.airborneState

    isAirborne = report(types = [
        'args',
        'deltaStamp'], dConfigParam = [
        'jump'])(isAirborne)
    
    def setGroundState(self, groundState):
        self.fsmLock.acquire()
        
        try:
            if self.groundState != groundState:
                self.groundState = groundState
                if self.state == 'Airborne':
                    self.request('Airborne')
                
        finally:
            self.fsmLock.release()


    setGroundState = report(types = [
        'args',
        'deltaStamp'], dConfigParam = [
        'jump'])(setGroundState)
    
    def startTrackAnimToSpeed(self):
        taskName = self.av.taskName('trackAnimToSpeed')
        taskMgr.remove(taskName)
        self.trackAnimToSpeed(None)
        taskMgr.add(self.trackAnimToSpeed, taskName)

    
    def stopTrackAnimToSpeed(self):
        taskName = self.av.taskName('trackAnimToSpeed')
        taskMgr.remove(taskName)

    
    def enterOff(self):
        if self.landIval:
            self.landIval.finish()
        
        if self.landRunIval:
            self.landRunIval.finish()
        
        if self.idleJumpIval:
            self.idleJumpIval.finish()
        
        if self.av.isLocal():
            self.ignore('jumpStart')
            self.ignore('jumpLand')
            self.ignore('jumpLandHard')
        
        if self.av.isLocal():
            self.av.setMovementIndex(-1)
        

    
    def exitOff(self):
        if self.av.isLocal():
            self.accept('jumpStart', self.handleAirborneEvent, [
                'Jump'])
            self.accept('jumpLand', self.handleAirborneEvent, [
                'Land'])
            self.accept('jumpLandHard', self.handleAirborneEvent, [
                'Land'])
        

    
    def enterIdle(self):
        (anim, rate) = self.animInfo[PiratesGlobals.STAND_INDEX]
        blendT = self.BLENDAMT * 0.5
        if anim and rate:
            if not hasattr(self.av, 'animIval') or not (self.av.animIval):
                self.av.loop(anim, rate, blendT = blendT)
            
        
        self.av.motionFSMEnterState(self.newState)
        if self.av.isLocal():
            self.av.setMovementIndex(PiratesGlobals.STAND_INDEX)
        
        self.setupSplash()

    enterIdle = report(types = [
        'args',
        'deltaStamp'], dConfigParam = [
        'jump'])(enterIdle)
    
    def exitIdle(self):
        self.av.stopLookAroundTask()
        self.av.motionFSMExitState(self.oldState)
        self.cleanupSplash()

    
    def setupSplash(self):
        if not IDLE_SPLASH_PLAY or not self.av.canIdleSplashEver():
            return None
        
        self.cleanupSplash()
        if self.splashAnimDelay:
            splashDelay = self.splashAnimDelay
        else:
            splashDelay = IDLE_SPLASH_DELAY
        
        def idleOneShot(task = None):
            if self.av.canIdleSplash():
                if self.splashAnims:
                    animChoice = random.choice(self.splashAnims)
                else:
                    animChoice = random.choice(IDLE_SPLASH_ANIMS)
                self.av.setPlayRate(animChoice[1], animChoice[0])
                self.av.play(animChoice[0])
                if not self.av.getDuration(animChoice[0]):
                    pass
                offset = max(5, 5)
                self.currentSplash = animChoice[0]
            elif not self.av.getDuration():
                pass
            offset = max(5, 5)
            task.delayTime = random.random() * max(0, splashDelay - offset) + offset
            return task.again

        delay = random.random() * splashDelay + 15
        taskMgr.doMethodLater(delay, idleOneShot, self.av.uniqueName('idleOneShot'))

    
    def cleanupSplash(self):
        taskMgr.remove(self.av.uniqueName('idleOneShot'))
        self.interruptSplash()

    
    def interruptSplash(self):
        if self.currentSplash:
            animCtrl = self.av.getAnimControl(self.currentSplash, 'head')
            if animCtrl:
                nextFrame = animCtrl.getNextFrame()
                fromFrame = max(0, nextFrame - 1)
                self.av.play(self.currentSplash, fromFrame = fromFrame, toFrame = fromFrame + 1)
            
            self.currentSplash = None
        

    
    def setupSplashAnimOverride(self, splashAnims):
        self.splashAnims = splashAnims

    
    def setupSplashAnimOverrideDelay(self, delay):
        self.splashAnimDelay = delay

    
    def enterWalkForward(self):
        (anim, rate) = self.animInfo[PiratesGlobals.WALK_INDEX]
        blendT = self.BLENDAMT * 0.5
        if anim and rate and self.av.canMove:
            self.av.loop(anim, rate, blendT = blendT)
        
        if self.av.isLocal():
            self.av.setMovementIndex(PiratesGlobals.WALK_INDEX)
            if self.av.cameraFSM.currentCamera:
                self.av.cameraFSM.currentCamera.avFaceCamera()
            
        

    enterWalkForward = report(types = [
        'args',
        'deltaStamp'], dConfigParam = [
        'jump'])(enterWalkForward)
    
    def exitWalkForward(self):
        pass

    
    def enterWalkReverse(self):
        (anim, rate) = self.animInfo[PiratesGlobals.REVERSE_INDEX]
        if anim and rate:
            self.av.loop(anim, rate, blendT = self.BLENDAMT)
        
        if self.av.isLocal():
            self.av.setMovementIndex(PiratesGlobals.REVERSE_INDEX)
            if self.av.cameraFSM.currentCamera:
                self.av.cameraFSM.currentCamera.avFaceCamera()
            
        

    
    def exitWalkReverse(self):
        pass

    
    def enterSpinLeft(self):
        (anim, rate) = self.animInfo[PiratesGlobals.SPIN_LEFT_INDEX]
        if anim and rate:
            self.av.loop(anim, rate, blendT = self.BLENDAMT)
        
        if self.av.isLocal():
            self.av.setMovementIndex(PiratesGlobals.SPIN_LEFT_INDEX)
            if self.av.cameraFSM.currentCamera:
                self.av.cameraFSM.currentCamera.avFaceCamera()
            
        

    
    def exitSpinLeft(self):
        pass

    
    def enterSpinRight(self):
        (anim, rate) = self.animInfo[PiratesGlobals.SPIN_RIGHT_INDEX]
        if anim and rate:
            self.av.loop(anim, rate, blendT = self.BLENDAMT)
        
        if self.av.isLocal():
            self.av.setMovementIndex(PiratesGlobals.SPIN_RIGHT_INDEX)
            if self.av.cameraFSM.currentCamera:
                self.av.cameraFSM.currentCamera.avFaceCamera()
            
        

    
    def exitSpinRight(self):
        pass

    
    def enterStrafeRight(self):
        (anim, rate) = self.animInfo[PiratesGlobals.STRAFE_RIGHT_INDEX]
        if anim and rate:
            self.av.loop(anim, rate, blendT = self.BLENDAMT)
        
        if self.av.isLocal():
            self.av.setMovementIndex(PiratesGlobals.STRAFE_RIGHT_INDEX)
            if self.av.cameraFSM.currentCamera:
                self.av.cameraFSM.currentCamera.avFaceCamera()
            
        

    
    def exitStrafeRight(self):
        pass

    
    def enterStrafeLeft(self):
        (anim, rate) = self.animInfo[PiratesGlobals.STRAFE_LEFT_INDEX]
        if anim and rate:
            self.av.loop(anim, rate, blendT = self.BLENDAMT)
        
        if self.av.isLocal():
            self.av.setMovementIndex(PiratesGlobals.STRAFE_LEFT_INDEX)
            if self.av.cameraFSM.currentCamera:
                self.av.cameraFSM.currentCamera.avFaceCamera()
            
        

    
    def exitStrafeLeft(self):
        pass

    
    def enterStrafeRightDiag(self):
        (anim, rate) = self.animInfo[PiratesGlobals.STRAFE_RIGHT_DIAG_INDEX]
        if anim and rate:
            self.av.loop(anim, rate, blendT = self.BLENDAMT)
        
        if self.av.isLocal():
            self.av.setMovementIndex(PiratesGlobals.STRAFE_RIGHT_DIAG_INDEX)
            if self.av.cameraFSM.currentCamera:
                self.av.cameraFSM.currentCamera.avFaceCamera()
            
        

    
    def exitStrafeRightDiag(self):
        pass

    
    def enterStrafeLeftDiag(self):
        (anim, rate) = self.animInfo[PiratesGlobals.STRAFE_LEFT_DIAG_INDEX]
        if anim and rate:
            self.av.loop(anim, rate, blendT = self.BLENDAMT)
        
        if self.av.isLocal():
            self.av.setMovementIndex(PiratesGlobals.STRAFE_LEFT_DIAG_INDEX)
            if self.av.cameraFSM.currentCamera:
                self.av.cameraFSM.currentCamera.avFaceCamera()
            
        

    
    def exitStrafeLeftDiag(self):
        pass

    
    def enterStrafeRightDiagReverse(self):
        (anim, rate) = self.animInfo[PiratesGlobals.STRAFE_RIGHT_DIAG_REV_INDEX]
        if anim and rate:
            self.av.loop(anim, rate, blendT = self.BLENDAMT)
        
        if self.av.isLocal():
            self.av.setMovementIndex(PiratesGlobals.STRAFE_RIGHT_DIAG_REV_INDEX)
            if self.av.cameraFSM.currentCamera:
                self.av.cameraFSM.currentCamera.avFaceCamera()
            
        

    
    def exitStrafeRightDiagReverse(self):
        pass

    
    def enterStrafeLeftDiagReverse(self):
        (anim, rate) = self.animInfo[PiratesGlobals.STRAFE_LEFT_DIAG_REV_INDEX]
        if anim and rate:
            self.av.loop(anim, rate, blendT = self.BLENDAMT)
        
        if self.av.isLocal():
            self.av.setMovementIndex(PiratesGlobals.STRAFE_LEFT_DIAG_REV_INDEX)
            if self.av.cameraFSM.currentCamera:
                self.av.cameraFSM.currentCamera.avFaceCamera()
            
        

    
    def exitStrafeLeftDiagReverse(self):
        pass

    
    def enterAdvance(self):
        (anim, rate) = self.animInfo[PiratesGlobals.ADVANCE_INDEX]
        if anim and rate:
            self.av.loop(anim, rate, blendT = self.BLENDAMT)
            if self.av.cameraFSM.currentCamera:
                self.av.cameraFSM.currentCamera.avFaceCamera()
            
        

    
    def exitAdvance(self):
        pass

    
    def enterRetreat(self):
        (anim, rate) = self.animInfo[PiratesGlobals.RETREAT_INDEX]
        if anim and rate:
            self.av.loop(anim, rate, blendT = self.BLENDAMT)
            if self.av.cameraFSM.currentCamera:
                self.av.cameraFSM.currentCamera.avFaceCamera()
            
        

    
    def exitRetreat(self):
        pass

    
    def enterRun(self):
        (anim, rate) = self.animInfo[PiratesGlobals.RUN_INDEX]
        blendT = self.BLENDAMT * 0.5
        if anim and rate and self.av.canMove:
            self.av.loop(anim, rate, blendT = blendT)
        
        if self.av.isLocal():
            self.av.setMovementIndex(PiratesGlobals.RUN_INDEX)
            if self.av.cameraFSM.currentCamera:
                self.av.cameraFSM.currentCamera.avFaceCamera()
            
        

    
    def exitRun(self):
        pass

    
    def enterAirborne(self):
        if self.groundState == self.GROUNDSTATE.OverSolid:
            idleAnim = self.animInfo[PiratesGlobals.OVER_SOLID_INDEX][0]
            self.av.loop(idleAnim, blendT = 0.0)
        elif self.groundState == self.GROUNDSTATE.OverWater:
            idleAnim = self.animInfo[PiratesGlobals.OVER_WATER_INDEX][0]
            self.av.loop(idleAnim, blendT = 0.0)
        
        if self.av.isLocal():
            self.av.setMovementIndex(-1)
        

    enterAirborne = report(types = [
        'args',
        'deltaStamp'], dConfigParam = [
        'jump'])(enterAirborne)
    
    def exitAirborne(self):
        pass

    exitAirborne = report(types = [
        'args',
        'deltaStamp'], dConfigParam = [
        'jump'])(exitAirborne)
    
    def request(self, *args, **kwargs):
        FSM.request(self, *args, **args)

    request = report(types = [
        'args',
        'deltaStamp'], dConfigParam = [
        'jump'])(request)


class MotionFSM(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('MotionFSM')
    BLENDAMT = 0.25
    
    def __init__(self, av):
        FSM.__init__(self, 'MotionFSM')
        self.av = av
        self.avHeight = 5
        self.cannotFloat = 0
        self._MotionFSM__submerged = None
        self._MotionFSM__overwater = None
        self._MotionFSM__inwater = None
        self.motionAnimFSM = MotionAnimFSM(self.av)
        if hasattr(self.av, 'getAnimInfo'):
            self.setAnimInfo(self.av.getAnimInfo('LandRoam'))
        
        self.lifterDelayFrames = 0
        self._MotionFSM__locked = 0
        self.movementKeys = { }
        keys = ('arrow_up', 'arrow_down', 'arrow_left', 'arrow_right', 'w', 's', 'a', 'd', 'q', 'e')
        for key in keys:
            self.movementKeys[key] = 0
            self.accept(key, self.setMovementTrack, extraArgs = [
                key,
                1])
            self.accept(key + '-up', self.setMovementTrack, extraArgs = [
                key,
                0])
        

    
    def setMovementTrack(self, track, value):
        if self.movementKeys:
            self.movementKeys[track] = value
        

    
    def setAvatar(self, av):
        self.av = av
        self.motionAnimFSM.av = av

    
    def cleanup(self):
        FSM.cleanup(self)
        if hasattr(self, 'av'):
            self.ignoreAll()
            self.motionAnimFSM.cleanup()
            del self.motionAnimFSM
            del self.av
            self.movementKeys = { }
        

    
    def off(self, lock = False):
        if self._MotionFSM__locked:
            return None
        
        self.request('Off')
        if lock:
            self.lock()
        

    
    def on(self, unlock = False):
        if unlock:
            self.unlock()
        
        if self._MotionFSM__locked:
            return None
        
        self.request('On')

    
    def moveLockIfOn(self):
        if self.state == 'On':
            self.moveLock()
        

    
    def onIfMoveLock(self):
        if self.state == 'MoveLock':
            self.on()
        

    
    def moveLock(self):
        if self._MotionFSM__locked:
            return None
        
        self.request('MoveLock')

    
    def lock(self):
        self._MotionFSM__locked = 1

    
    def unlock(self):
        self._MotionFSM__locked = 0

    
    def isLocked(self):
        return self._MotionFSM__locked

    
    def setAnimInfo(self, animInfo, reset = True):
        self.animInfo = animInfo
        self.motionAnimFSM.setAnimInfo(animInfo, reset)

    
    def setAllowAirborne(self, allow):
        self.motionAnimFSM.setAllowAirborne(allow)

    
    def filterOff(self, request, args):
        return self.defaultFilter(request, args)

    
    def defaultFilter(self, request, args):
        if self.av.isLocal():
            if localAvatar.gameFSM and localAvatar.gameFSM.state == 'Cutscene':
                return None
            
        
        return FSM.defaultFilter(self, request, args)

    
    def enterOff(self):
        idleAnim = self.animInfo[PiratesGlobals.STAND_INDEX][0]
        if idleAnim:
            self.av.loop(idleAnim, blendT = self.BLENDAMT)
        
        self.av.stopLookAroundTask()
        if hasattr(self.av, 'loadAnimatedHead'):
            if self.av.loadAnimatedHead == False:
                self.av.headNode.setHpr(self.av.headFudgeHpr)
            
        

    
    def exitOff(self):
        pass

    
    def fix(self):
        (anim, rate) = self.animInfo[STATE_MOTION.get(self.state, PiratesGlobals.STAND_INDEX)]
        self.av.loop(anim, rate, blendT = 0.0)

    
    def enterOn(self):
        if self.av.canMove:
            self.av.startSmooth()
        
        if self.av.isLocal():
            self.av.startPosHprBroadcast()
            self.av.collisionsOn()
            self.motionAnimFSM.startTrackAnimToSpeed()
            self.av.enableAvatarControls()
            for key in self.movementKeys:
                if self.movementKeys[key]:
                    messenger.send(key)
                    continue
            
            if not self.av.ship:
                self.startCheckUnderWater()
            
        

    
    def exitOn(self):
        if self.av.isLocal():
            self.av.stopLookAroundTask()
            if self.av.loadAnimatedHead == False:
                self.av.headNode.setHpr(self.av.headFudgeHpr)
            
            self.av.stopPosHprBroadcast()
            self.av.collisionsOff()
            self.motionAnimFSM.stopTrackAnimToSpeed()
            self.av.disableAvatarControls()
            self.stopCheckUnderWater()
            self.av.setActiveShadow(0)
            self.motionAnimFSM.request('Off')
        

    
    def enterMoveLock(self):
        idleAnim = self.animInfo[PiratesGlobals.STAND_INDEX][0]
        if idleAnim:
            self.av.loop(idleAnim, blendT = self.BLENDAMT)
        
        self.av.startSmooth()
        if self.av.isLocal():
            self.av.startPosHprBroadcast()
            self.av.collisionsOn()
            self.startCheckUnderWater()
        

    
    def exitMoveLock(self):
        self.av.stopSmooth()
        if self.av.isLocal():
            self.av.stopLookAroundTask()
            if self.av.loadAnimatedHead == False:
                self.av.headNode.setHpr(self.av.headFudgeHpr)
            
            self.av.stopPosHprBroadcast()
            self.stopCheckUnderWater()
            self.av.collisionsOff()
            self.av.setActiveShadow(0)
            self.motionAnimFSM.request('Off')
        

    
    def startCheckUnderWater(self):
        if self.cannotFloat:
            return None
        
        self.stopCheckUnderWater()
        if self.getCurrentOrNextState() is not 'Off':
            task = taskMgr.add(self._MotionFSM__checkUnderWater, 'localAvatarCheckUnderWater', priority = 34)
            task.oldParent = self.av.getParent()
        

    
    def stopCheckUnderWater(self):
        if self.cannotFloat:
            return None
        
        taskMgr.remove('localAvatarCheckUnderWater')
        self._MotionFSM__submerged = None
        self._MotionFSM__overwater = None
        self._MotionFSM__inwater = None
        self.av.disableWaterEffect()

    
    def _MotionFSM__checkUnderWater(self, task):
        if not hasattr(self.av.controlManager.currentControls, 'lifter') and base.cr.isOceanEnabled():
            return task.cont
        
        if self.lifterDelayFrames:
            self.lifterDelayFrames -= 1
            return task.cont
        
        waterZ = base.cr.getWaterHeight(self.av)
        avZ = self.av.getZ(render)
        if avZ <= waterZ and not (self._MotionFSM__inwater):
            self._MotionFSM__inwater = True
            self.av.enableWaterEffect()
        
        if avZ > waterZ and self._MotionFSM__inwater:
            self._MotionFSM__inwater = False
            self.av.disableWaterEffect()
        
        if self._MotionFSM__inwater:
            offset = (waterZ - avZ) + 0.14999999999999999
            speeds = self.av.controlManager.getSpeeds()
            self.av.adjustWaterEffect(offset, *speeds)
        
        curControls = self.av.controlManager.currentControls
        if curControls.lifter.hasContact():
            avAirborneHeight = curControls.lifter.getAirborneHeight()
            if self._MotionFSM__submerged:
                if avAirborneHeight < self.avHeight and not (self.av.bobbing):
                    self._MotionFSM__submerged = False
                    self._MotionFSM__overwater = False
                    if task.oldParent == self.av.getParent():
                        self.av.setZ(avZ - avAirborneHeight)
                    
                    self.av.cameraFSM.fpsCamera.lerpFromZOffset(avAirborneHeight, PiratesGlobals.SWIM_WALK_TRANSITION_TIME)
                    self.av.controlManager.currentControls.oneTimeCollide()
                    messenger.send('localAvatarExitWater')
                    self.av.b_setGroundState(self.motionAnimFSM.GROUNDSTATE.OverSolid)
                
            elif avZ + self.avHeight - avAirborneHeight <= waterZ and not (self._MotionFSM__overwater):
                self._MotionFSM__overwater = True
                self.av.b_setGroundState(self.motionAnimFSM.GROUNDSTATE.OverWater)
            
            if avZ + self.avHeight <= waterZ:
                self._MotionFSM__submerged = True
                messenger.send('localAvatarEnterWater')
                self.av.controlManager.currentControls.isAirborne = 0
                curControls.abortJump()
            
            if avZ == waterZ and avAirborneHeight > self.avHeight:
                self._MotionFSM__submerged = True
                self._MotionFSM__overwater = True
            
        elif self._MotionFSM__submerged != True:
            self._MotionFSM__submerged = True
            self._MotionFSM__overwater = True
            messenger.send('localAvatarEnterWater')
        
        task.oldParent = self.av.getParent()
        return task.cont

    
    def isAirborne(self):
        if not (self._MotionFSM__submerged):
            pass
        return self.motionAnimFSM.airborneState

    
    def setWaterState(self, overWater, submerged):
        self._MotionFSM__submerged = submerged
        self._MotionFSM__overWater = overWater

    
    def setLifterDelayFrames(self, frames):
        self.lifterDelayFrames = frames


