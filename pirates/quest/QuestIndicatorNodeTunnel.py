# File: Q (Python 2.4)

from pandac.PandaModules import Point3
from pirates.piratesgui.RadarGui import *
from pirates.quest.QuestIndicatorNode import QuestIndicatorNode
from pirates.piratesgui.RadarGui import RADAR_OBJ_TYPE_QUEST
from direct.showbase.PythonUtil import report, StackTrace

class QuestIndicatorNodeTunnel(QuestIndicatorNode):
    LOD_CENTER_OFFSET_X = 30
    
    def __init__(self, questStep):
        self.pendingStepObj = None
        QuestIndicatorNode.__init__(self, 'TunnelIndicator', [
            self.LOD_CENTER_OFFSET_X], questStep)

    
    def delete(self):
        if self.pendingStepObj:
            base.cr.relatedObjectMgr.abortRequest(self.pendingStepObj)
            self.pendingStepObj = None
        
        self.ignore('tunnelSetLinks')
        QuestIndicatorNode.delete(self)

    delete = report(types = [
        'frameCount',
        'args'], dConfigParam = 'quest-indicator')(delete)
    
    def placeInWorld(self):
        
        def stepObjHere(tunnelObj):
            self.pendingStepObj = None
            area = base.cr.getDo(self.questStep.getOriginDoId())
            areaUid = area.getUniqueId()
            areaNodeName = tunnelObj.getAreaNodeNameFromAreaUid(areaUid)
            areaNode = area.getConnectorNodeNamed(areaNodeName)
            self.reparentTo(areaNode)
            self.setPosHpr(0, 0, 0, 0, 0, 0)
            self.setPos(self, self.LOD_CENTER_OFFSET_X, 0, 5)
            self.wrtReparentTo(area)

        stepObjHere = report(types = [
            'frameCount',
            'args'], dConfigParam = 'quest-indicator')(stepObjHere)
        if self.pendingStepObj:
            base.cr.relatedObjectMgr.abortRequest(self.pendingStepObj)
            self.pendingStepObj = None
        
        self.pendingStepObj = base.cr.relatedObjectMgr.requestObjects([
            self.questStep.getStepDoId()], eachCallback = stepObjHere)

    placeInWorld = report(types = [
        'frameCount',
        'args'], dConfigParam = 'quest-indicator')(placeInWorld)
    
    def loadZoneLevel(self, level):
        QuestIndicatorNode.loadZoneLevel(self, level)
        if level == 0:
            self.request('At')
        elif level == 1:
            self.request('Far')
        

    loadZoneLevel = report(types = [
        'frameCount',
        'args'], dConfigParam = 'quest-indicator')(loadZoneLevel)
    
    def unloadZoneLevel(self, level):
        QuestIndicatorNode.unloadZoneLevel(self, level)
        if level == 0:
            self.request('Far')
        elif level == 1:
            self.request('Off')
        

    unloadZoneLevel = report(types = [
        'frameCount',
        'args'], dConfigParam = 'quest-indicator')(unloadZoneLevel)
    
    def enterAt(self):
        QuestIndicatorNode.enterAt(self)
        self.pendingStepObj = None

    enterAt = report(types = [
        'frameCount',
        'args'], dConfigParam = 'quest-indicator')(enterAt)
    
    def exitAt(self):
        QuestIndicatorNode.exitAt(self)

    exitAt = report(types = [
        'frameCount',
        'args'], dConfigParam = 'quest-indicator')(exitAt)
    
    def startFarEffect(self):
        QuestIndicatorNode.startFarEffect(self)
        if self.farEffect:
            self.farEffect.setPos(0, 0, -5)
        

    startFarEffect = report(types = [
        'frameCount',
        'args'], dConfigParam = 'quest-indicator')(startFarEffect)
    
    def setZoneRadii(self, zoneRadii, zoneCenter = [
        0,
        0]):
        QuestIndicatorNode.setZoneRadii(self, zoneRadii, zoneCenter)
        self.setZoneLODOffset(-1, Point3(-(self.LOD_CENTER_OFFSET_X), 0, 0))


