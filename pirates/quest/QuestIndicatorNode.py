# File: Q (Python 2.4)

from pandac.PandaModules import *
from pirates.world.ZoneLOD import ZoneLOD
from direct.fsm.FSM import FSM
from direct.interval.IntervalGlobal import Parallel
from direct.showbase.PythonUtil import report
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.effects.RayOfLight import RayOfLight
from pirates.map.MinimapObject import DynamicMinimapObject
from pirates.world.LocationConstants import LocationIds
from pirates.world.DistributedGameArea import DistributedGameArea

class QuestIndicatorNode(NodePath, FSM, ZoneLOD):
    notify = directNotify.newCategory('QuestIndicatorNode')
    
    def __init__(self, name, zoneRadii, questStep):
        zoneRadii += [
            1000000]
        NodePath.__init__(self, name)
        FSM.__init__(self, '%sFSM' % name)
        ZoneLOD.__init__(self, self._QuestIndicatorNode__uniqueName, zoneRadii)
        self.questStep = questStep
        self.pendingOriginObj = None
        self.muted = False
        self.farEffect = None
        self.wantBottomEffect = True
        self.minimapObject = None
        self.minimap = None
        
        def originObjHere(originObj):
            self.pendingOriginObj = None
            self.setZoneRadii(zoneRadii)
            self.placeInWorld()

        self._selfRefreshTask = None
        self._refreshTargetInfo = None
        if self.questStep.getOriginDoId():
            self.pendingOriginObj = base.cr.relatedObjectMgr.requestObjects([
                self.questStep.getOriginDoId()], eachCallback = originObjHere)
        else:
            originObjHere(None)

    
    def delete(self):
        if self.minimapObject:
            self.minimapObject.removeFromMap()
            self.minimapObject = None
        
        self.stopTargetRefresh()
        if self.pendingOriginObj:
            base.cr.relatedObjectMgr.abortRequest(self.pendingOriginObj)
            self.pendingOriginObj = None
        
        self._QuestIndicatorNode__cleanup()
        ZoneLOD.delete(self)
        self.remove()
        self.minimapObject = None
        self.minimap = None
        self.questStep = None
        if self.farEffect:
            self.farEffect.stopLoop()
            self.farEffect.destroy()
        
        self.farEffect = None

    delete = report(types = [
        'args'], dConfigParam = 'quest-indicator')(delete)
    
    def cleanup(self):
        pass

    cleanup = report(types = [
        'args'], dConfigParam = 'quest-indicator')(cleanup)
    
    def __cleanup(self):
        ZoneLOD.cleanup(self)
        FSM.cleanup(self)

    _QuestIndicatorNode__cleanup = report(types = [
        'args'], dConfigParam = 'quest-indicator')(__cleanup)
    
    def _QuestIndicatorNode__uniqueName(self, idString):
        return '%s-QuestNodeIndicator-%s' % (idString, id(self.questStep))

    
    def placeInWorld(self):
        pass

    placeInWorld = report(types = [
        'args'], dConfigParam = 'quest-indicator')(placeInWorld)
    
    def loadZoneLevel(self, level):
        self.notify.debug('LoadZoneLevel: %s' % level)

    
    def unloadZoneLevel(self, level, cacheObs = False):
        self.notify.debug('UnloadZoneLevel: %s' % level)

    
    def defaultFilter(self, request, args):
        if request != self.state:
            return FSM.defaultFilter(self, request, args)
        

    
    def getMinimapObject(self):
        if not self.minimapObject:
            self.minimapObject = MinimapQuest(self)
        
        return self.minimapObject

    
    def exitOff(self):
        self.accept('transferMinimapObjects', self.transferMinimapObject)
        if hasattr(localAvatar, 'guiMgr') and localAvatar.guiMgr:
            self.minimap = localAvatar.guiMgr.getMinimap()
            if self.minimap and self.getMinimapObject():
                self.minimap.addObject(self.getMinimapObject())
            
            self.updateGuiHints(localAvatar.activeQuestId)
        

    exitOff = report(types = [
        'args'], dConfigParam = 'quest-indicator')(exitOff)
    
    def transferMinimapObject(self, guiMgr):
        guiMgr.transferMinimapObject(self.getMinimapObject())

    
    def enterOff(self):
        self.ignore('transferMinimapObjects')
        self.stopFarEffect()
        if self.minimap and self.minimapObject:
            self.minimap.removeObject(self.minimapObject)
        
        if hasattr(localAvatar, 'guiMgr') and localAvatar.guiMgr:
            localAvatar.guiMgr.setQuestHintText('')
        
        self.minimap = None

    enterOff = report(types = [
        'frameCount',
        'args'], dConfigParam = 'quest-indicator')(enterOff)
    
    def enterFar(self):
        self.notify.debug('Enter: Far')
        self.startFarEffect()

    enterFar = report(types = [
        'args'], dConfigParam = 'quest-indicator')(enterFar)
    
    def exitFar(self):
        self.notify.debug('Exit: Far')
        self.stopFarEffect()

    exitFar = report(types = [
        'args'], dConfigParam = 'quest-indicator')(exitFar)
    
    def enterNear(self):
        self.notify.debug('Enter: Near')

    
    def exitNear(self):
        self.notify.debug('Exit: Near')

    
    def enterAt(self):
        self.notify.debug('Enter: At')

    
    def exitAt(self):
        self.notify.debug('Exit: At')

    
    def startFarEffect(self):
        if self.muted:
            return None
        
        if not self.farEffect:
            self.farEffect = RayOfLight()
            self.farEffect.setBottomRayEnabled(self.wantBottomEffect)
            self.farEffect.reparentTo(self)
            self.farEffect.startLoop()
        

    startFarEffect = report(types = [
        'args'], dConfigParam = 'quest-indicator')(startFarEffect)
    
    def stopFarEffect(self):
        if self.farEffect:
            self.farEffect.stopLoop()
            self.farEffect.destroy()
            self.farEffect = None
        

    stopFarEffect = report(types = [
        'args'], dConfigParam = 'quest-indicator')(stopFarEffect)
    
    def showEffect(self):
        self.notify.debug('ShowEffect')
        self.muted = False
        self.startFarEffect()

    showEffect = report(types = [
        'args'], dConfigParam = 'quest-indicator')(showEffect)
    
    def hideEffect(self):
        self.notify.debug('HideEffect')
        self.muted = True
        self.stopFarEffect()

    hideEffect = report(types = [
        'args'], dConfigParam = 'quest-indicator')(hideEffect)
    
    def requestTargetRefresh(self, refreshDelay = 10):
        self.stopTargetRefresh()
        
        def tryRefresh(task):
            if localAvatar.ship:
                avLoc = localAvatar.ship.getLocation()
            else:
                avLoc = localAvatar.getLocation()
            currTime = globalClock.getFrameTime()
            if (self._refreshTargetInfo == None or self._refreshTargetInfo[0] != avLoc) and currTime - self._refreshTargetInfo[1] > 10:
                localAvatar.refreshActiveQuestStep(False, True)
                self._refreshTargetInfo = [
                    avLoc,
                    currTime]
            
            if refreshDelay == 0:
                return task.done
            else:
                return task.again

        if localAvatar.questStepAutoRefresh():
            self._selfRefreshTask = taskMgr.doMethodLater(refreshDelay, tryRefresh, 'indicatorNodeRefresh-%s' % localAvatar.doId)
        

    
    def stopTargetRefresh(self):
        if self._selfRefreshTask:
            taskMgr.remove(self._selfRefreshTask)
            self._selfRefreshTask = None
            self._refreshTargetInfo = None
        

    
    def updateGuiHints(self, questId):
        if not hasattr(localAvatar, 'guiMgr') or not (localAvatar.guiMgr):
            return None
        
        hintText = ''
        quest = localAvatar.getQuestById(questId)
        if quest and hasattr(quest.getTasks()[0], 'getEnemyType') and not quest.isComplete():
            if quest.getTasks()[0].getLocation() != LocationIds.ANY_LOCATION:
                pass
            elif localAvatar.questStep and localAvatar.questStep.getTargetArea():
                targetLocation = localAvatar.questStep.getTargetArea()
                localAvatar.guiMgr.radarGui.hideGlowRing()
                targetLocationName = PLocalizer.LocationNamesNotIsland.get(targetLocation)
                if not targetLocationName:
                    targetLocationName = PLocalizer.LocationNames.get(targetLocation)
                
                if targetLocationName:
                    hintText = PLocalizer.TargetsInThere % targetLocationName
                
            elif localAvatar.questStep:
                localAvatar.guiMgr.radarGui.hideGlowRing()
                targetLocation = localAvatar.questStep.getIsland()
                targetLocationName = PLocalizer.LocationNames.get(targetLocation)
                if targetLocationName:
                    hintText = PLocalizer.TargetsInThere % targetLocationName
                
            
        
        localAvatar.guiMgr.setQuestHintText(hintText)

    
    def setZoneLODOffset(self, zone, offset):
        if zone == -1:
            for currSphere in self.zoneSphere:
                sphereSolid = currSphere.node().modifySolid(0)
                sphereSolid.setCenter(offset)
            
        else:
            sphereSolid = self.zoneSphere[zone].node().modifySolid(0)
            sphereSolid.setCenter(offset)



class MinimapQuest(DynamicMinimapObject):
    SORT = 3
    ICON = None
    ARROW = None
    
    def __init__(self, worldNode):
        if not MinimapQuest.ICON:
            model = loader.loadModel('models/gui/compass_main')
            MinimapQuest.ICON = model.find('**/icon_objective_grey')
            MinimapQuest.ICON.clearTransform()
            MinimapQuest.ICON.setHpr(0, 90, 0)
            MinimapQuest.ICON.setColorScale(1, 1, 0, 1, 1)
            MinimapQuest.ICON.setScale(250)
            MinimapQuest.ICON.flattenStrong()
        
        if not MinimapQuest.ARROW:
            model = loader.loadModel('models/gui/compass_arrow')
            MinimapQuest.ARROW = model.getChild(0).getChild(0).copyTo(NodePath())
            MinimapQuest.ARROW.setScale(0.75)
            MinimapQuest.ARROW.setColorScale(1, 1, 0, 1, 1)
            MinimapQuest.ARROW.flattenStrong()
        
        DynamicMinimapObject.__init__(self, 'quest', worldNode, MinimapQuest.ICON)
        self.outOfRangeGeom = NodePath('outOfRange')
        arrow = MinimapQuest.ARROW.copyTo(self.outOfRangeGeom)
        arrow.setPosHpr(1.1000000000000001, 0, 0, 0, 0, 90)

    
    def _updateOnMap(self, map):
        localAvatar.guiMgr.radarGui.updateOutOfRange(map, self, self.outOfRangeGeom)
        if localAvatar.guiMgr.invasionScoreboard:
            self.mapGeom.hide()
        else:
            self.mapGeom.show()

    
    def _removedFromMap(self, map):
        self.outOfRangeGeom.detachNode()

    
    def _zoomChanged(self, radius):
        self.mapGeom.setScale((radius / 1000.0) * 4)


