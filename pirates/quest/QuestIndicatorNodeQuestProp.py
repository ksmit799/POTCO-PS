# File: Q (Python 2.4)

from pirates.effects.RayOfLight import RayOfLight
from pirates.quest.QuestIndicatorGridNode import QuestIndicatorGridNode
from direct.showbase.PythonUtil import report

class QuestIndicatorNodeQuestProp(QuestIndicatorGridNode):
    
    def __init__(self, questStep):
        self.nearEffect = None
        QuestIndicatorGridNode.__init__(self, 'QuestPropIndicator', [
            30,
            150], questStep)

    
    def delete(self):
        QuestIndicatorGridNode.delete(self)
        if self.nearEffect:
            self.nearEffect.destroy()
        
        self.nearEffect = None

    delete = report(types = [
        'frameCount',
        'args'], dConfigParam = 'quest-indicator')(delete)
    
    def enterOff(self):
        QuestIndicatorGridNode.enterOff(self)

    enterOff = report(types = [
        'frameCount',
        'args'], dConfigParam = 'quest-indicator')(enterOff)
    
    def enterFar(self):
        QuestIndicatorGridNode.enterFar(self)
        self.requestTargetRefresh()

    
    def exitFar(self):
        QuestIndicatorGridNode.exitFar(self)
        self.stopTargetRefresh()

    
    def enterNear(self):
        QuestIndicatorGridNode.enterNear(self)
        self.startNearEffect()

    enterNear = report(types = [
        'frameCount',
        'args'], dConfigParam = 'quest-indicator')(enterNear)
    
    def exitNear(self):
        self.stopNearEffect()
        QuestIndicatorGridNode.exitNear(self)

    exitNear = report(types = [
        'frameCount',
        'args'], dConfigParam = 'quest-indicator')(exitNear)
    
    def enterAt(self):
        QuestIndicatorGridNode.enterAt(self)

    enterAt = report(types = [
        'frameCount',
        'args'], dConfigParam = 'quest-indicator')(enterAt)
    
    def exitAt(self):
        QuestIndicatorGridNode.exitAt(self)

    exitAt = report(types = [
        'frameCount',
        'args'], dConfigParam = 'quest-indicator')(exitAt)
    
    def stepObjArrived(self, stepObj):
        QuestIndicatorGridNode.stepObjArrived(self, stepObj)
        if self.getCurrentOrNextState() in ('Near',):
            self.startNearEffect()
        

    stepObjArrived = report(types = [
        'frameCount',
        'args'], dConfigParam = 'quest-indicator')(stepObjArrived)
    
    def stepObjLeft(self):
        self.stopNearEffect()
        QuestIndicatorGridNode.stepObjLeft(self)

    
    def showEffect(self):
        QuestIndicatorGridNode.showEffect(self)
        self.startNearEffect()

    
    def hideEffect(self):
        QuestIndicatorGridNode.hideEffect(self)
        self.stopNearEffect()

    
    def startNearEffect(self):
        if self.muted:
            return None
        
        if not self.nearEffect:
            self.nearEffect = RayOfLight()
            self.nearEffect.setBottomRayEnabled(self.wantBottomEffect)
            self.nearEffect.startLoop()
        
        if self.stepObj:
            self.nearEffect.reparentTo(self.stepObj)
        

    startNearEffect = report(types = [
        'frameCount',
        'args'], dConfigParam = 'quest-indicator')(startNearEffect)
    
    def stopNearEffect(self):
        if self.nearEffect:
            self.nearEffect.stopLoop()
            self.nearEffect = None
        

    stopNearEffect = report(types = [
        'frameCount',
        'args'], dConfigParam = 'quest-indicator')(stopNearEffect)

