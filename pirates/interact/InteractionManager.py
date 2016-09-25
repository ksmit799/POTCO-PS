# File: I (Python 2.4)

from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.showbase import DirectObject
from direct.task import Task
from pirates.piratesbase import PiratesGlobals
import InteractiveBase

class InteractionManager(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('InteractionManager')
    Forward = Vec3(0, 1, 0)
    
    def __init__(self):
        self._InteractionManager__interactives = []
        self._InteractionManager__nearest = None
        self._InteractionManager__mouseOver = None
        self._InteractionManager__currentInteractive = None
        self._InteractionManager__updateDelay = 0.20000000000000001
        self._InteractionManager__updateTaskName = 'InteractionManagerUpdate'
        self._InteractionManager__locked = 0
        self.cTrav = None
        self.lifter = None
        self.cRayNode = None
        self.setupLifter()

    
    def delete(self):
        self.cleanupLifter()
        self.stop()

    
    def __str__(self):
        if self._InteractionManager__nearest:
            nearest = self._InteractionManager__nearest.getName()
        else:
            nearest = None
        if self._InteractionManager__currentInteractive:
            current = '%s(%s)' % (self._InteractionManager__currentInteractive.getName(), self._InteractionManager__currentInteractive.doId)
        else:
            current = None
        return 'InteractionMgr: N-%s, C-%s' % (nearest, current)

    
    def start(self):
        if self._InteractionManager__locked:
            return None
        
        taskMgr.remove(self._InteractionManager__updateTaskName)
        taskMgr.doMethodLater(self._InteractionManager__updateDelay, self.updateTextMessage, self._InteractionManager__updateTaskName)

    
    def stop(self, endCurrent = False):
        if self._InteractionManager__locked:
            return None
        
        if endCurrent:
            self.requestExitCurrent()
        
        taskMgr.remove(self._InteractionManager__updateTaskName)
        if self._InteractionManager__nearest:
            self._InteractionManager__nearest.hideProximityInfo()
            self._InteractionManager__nearest = None
        
        if self._InteractionManager__mouseOver:
            self._InteractionManager__mouseOver.hideMouseOverInfo()
            self._InteractionManager__mouseOver = None
        

    
    def lock(self):
        self._InteractionManager__locked = 1

    
    def unlock(self):
        self._InteractionManager__locked = 0

    
    def addInteractive(self, iObj, priority = InteractiveBase.PROXIMITY):
        if iObj.allowInteract:
            if (iObj, priority) in self._InteractionManager__interactives:
                raise HierarchyException(0, 'Redundant Interactive - %s(%d)' % (iObj.getName(), iObj.doId))
            
            self._InteractionManager__interactives.append((iObj, priority))
        

    
    def removeInteractive(self, iObj, priority = InteractiveBase.PROXIMITY):
        if (iObj, priority) in self._InteractionManager__interactives:
            self._InteractionManager__interactives.remove((iObj, priority))
        
        if iObj == self._InteractionManager__nearest:
            iObj.hideProximityInfo()
            self._InteractionManager__nearest = None
        
        if iObj == self._InteractionManager__mouseOver:
            iObj.hideMouseOverInfo()
            self._InteractionManager__mouseOver = None
        

    
    def sortInteractives(self):
        maxObj = None
        maxPri = 0
        for (iObj, pri) in self._InteractionManager__interactives:
            if pri > maxPri:
                maxObj = iObj
                maxPri = pri
                return (maxObj, maxPri)
                continue
        
        maxDot = -1
        maxPri = -1
        for (iObj, pri) in self._InteractionManager__interactives:
            if not iObj.isEmpty():
                vObj = iObj.getPosRelToAv()
                vObj.normalize()
                vDot = self.Forward.dot(vObj)
                if vDot > maxDot:
                    maxDot = vDot
                    maxObj = iObj
                    maxPri = pri
                
            vDot > maxDot
        
        return (maxObj, maxPri)

    
    def updateTextMessage(self, task):
        if not self._InteractionManager__interactives:
            return task.again
        
        newClosest = None
        (newObj, newPri) = self.sortInteractives()
        
        def popupInfo(newObj, newPri, self = self):
            if newObj:
                if newPri == InteractiveBase.PROXIMITY:
                    newObj.showProximityInfo()
                    self._InteractionManager__nearest = newObj
                elif newPri == InteractiveBase.MOUSE_OVER:
                    newObj.showMouseOverInfo()
                    self._InteractionManager__mouseOver = newObj
                
            

        if newObj is None:
            if self._InteractionManager__nearest:
                self._InteractionManager__nearest.hideProximityInfo()
                self._InteractionManager__nearest = None
            
            if self._InteractionManager__mouseOver:
                self._InteractionManager__mouseOver.hideMouseOverInfo()
                self._InteractionManager__mouseOver = None
            
            return task.again
        
        if newObj != self._InteractionManager__nearest and newObj != self._InteractionManager__mouseOver:
            if self._InteractionManager__nearest:
                self._InteractionManager__nearest.hideProximityInfo()
                self._InteractionManager__nearest = None
            
            if self._InteractionManager__mouseOver:
                self._InteractionManager__mouseOver.hideMouseOverInfo()
                self._InteractionManager__mouseOver = None
            
            popupInfo(newObj, newPri)
        
        return task.again

    
    def setCurrentInteractive(self, interactive):
        interactiveId = 0
        if interactive:
            interactiveId = interactive.doId
        
        self._InteractionManager__currentInteractive = interactive
        if self._InteractionManager__nearest:
            self._InteractionManager__nearest.hideProximityInfo()
            self._InteractionManager__nearest = None
        
        if self._InteractionManager__mouseOver:
            self._InteractionManager__mouseOver.hideMouseOverInfo()
            self._InteractionManager__mouseOver = None
        

    
    def getCurrentInteractive(self):
        return self._InteractionManager__currentInteractive

    
    def getCurrent(self):
        return self.getCurrentInteractive()

    
    def getInteractives(self):
        return self._InteractionManager__interactives

    
    def getNearest(self):
        return self._InteractionManager__nearest

    
    def getMouseOver(self):
        return self._InteractionManager__mouseOver

    
    def requestExitCurrent(self):
        if self._InteractionManager__currentInteractive:
            self._InteractionManager__currentInteractive.requestExit()
        

    
    def setupLifter(self):
        if not self.cTrav:
            self.cTrav = CollisionTraverser('InteractionMgr')
            cRay = CollisionRay(0.0, 0.0, 4000.0, 0.0, 0.0, -1.0)
            cRayNode = CollisionNode('InteractionMgr-cRay')
            cRayNode.addSolid(cRay)
            cRayNode.setFromCollideMask(PiratesGlobals.FloorBitmask | PiratesGlobals.ShipFloorBitmask)
            cRayNode.setIntoCollideMask(BitMask32.allOff())
            cRayNode.setBounds(BoundingSphere())
            cRayNode.setFinal(1)
            self.cRayNodePath = NodePath(cRayNode)
            self.lifter = CollisionHandlerFloor()
            self.lifter.setReach(8.0)
        

    
    def cleanupLifter(self):
        if self.cTrav:
            self.lifter.clearColliders()
            self.cTrav.clearColliders()
            self.cRayNode.removeNode()
            self.cTrav = None
            self.lifter = None
            self.cRayNode = None
        

    
    def useLifter(self, liftedNodePath, severity = 2):
        self.cRayNodePath.reparentTo(liftedNodePath)
        self.lifter.addCollider(self.cRayNodePath, liftedNodePath)
        self.cTrav.addCollider(self.cRayNodePath, self.lifter)
        self.cTrav.traverse(render)
        self.cTrav.removeCollider(self.cRayNodePath)
        self.lifter.removeCollider(self.cRayNodePath)
        self.cRayNodePath.detachNode()


