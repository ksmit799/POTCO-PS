# File: Q (Python 2.4)

from pandac.PandaModules import TransformState
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.PythonUtil import report
from pirates.pirate import AvatarType, AvatarTypes
from pirates.piratesbase import PiratesGlobals
from pirates.quest import QuestConstants
from pirates.piratesbase import TeamUtils
from pirates.world import LocationConstants
import types
import copy

class QuestGoal:
    Type_Uid = 0
    Type_Custom = 1
    LEVEL_IDX = 0
    TYPE_IDX = 1
    FACTION_IDX = 2
    HULL_IDX = 3
    FLAGSHIP_IDX = 4
    LOCATION_IDX = 5
    MAX_IDX = 6
    GOAL_TYPE_DINGHY = 'dinghy'
    GOAL_TYPE_SHIP = 'ship'
    GOAL_TYPES_OCEAN = [
        GOAL_TYPE_SHIP]
    
    def __init__(self, typeInfo):
        self._QuestGoal__goalDataStr = None
        if typeInfo == None:
            self._QuestGoal__goalType = types.ListType
            self._QuestGoal__goalData = []
            return None
        
        if type(typeInfo) == types.StringType:
            typeInfo = [
                typeInfo]
        
        self._QuestGoal__goalData = typeInfo
        self._QuestGoal__goalType = type(self._QuestGoal__goalData)

    
    def getType(self):
        if self._QuestGoal__goalType == types.DictType:
            return self.Type_Custom
        
        return self.Type_Uid

    
    def getTargetType(self):
        if self._QuestGoal__goalType == types.DictType:
            return self._QuestGoal__goalData.get(self.TYPE_IDX)
        
        return (0, 0, 0, 0)

    
    def getTargetTypeOnlyOnOcean(self):
        return self.getTargetType() in self.GOAL_TYPES_OCEAN

    
    def getLocation(self):
        if self._QuestGoal__goalType == types.DictType:
            return self._QuestGoal__goalData.get(self.LOCATION_IDX)
        

    
    def compareTo(self, object, goalOwner = None):
        if self._QuestGoal__goalType == types.DictType:
            goalLevel = self._QuestGoal__goalData.get(self.LEVEL_IDX, 0)
            if goalLevel > 0 and goalLevel > object.getLevel():
                return 1
            
            hasIsShip = hasattr(object, '_isShip')
            if game.process == 'ai' and not hasIsShip:
                return -1
            
            goalLocation = self._QuestGoal__goalData.get(self.LOCATION_IDX, None)
            objectLocation = object.getParentObj()
            if goalLocation and objectLocation and hasattr(objectLocation, 'getUniqueId') and not (goalLocation == LocationConstants.LocationIds.ANY_LOCATION) and not LocationConstants.isInArea(goalLocation, objectLocation.getUniqueId())[0]:
                return 1
            
            if hasIsShip and object._isShip():
                if self.getTargetTypeOnlyOnOcean():
                    goalFaction = self._QuestGoal__goalData.get(self.FACTION_IDX, None)
                    if goalFaction:
                        isEnemy = False
                        if goalOwner:
                            isEnemy = TeamUtils.friendOrFoe(goalOwner, object) == PiratesGlobals.ENEMY
                        
                        objFaction = object.getFaction()
                        if goalFaction != None and objFaction != None or goalFaction.getFaction() != objFaction.getFaction() or not isEnemy:
                            return 1
                        
                    
                    goalHull = self._QuestGoal__goalData.get(self.HULL_IDX, None)
                    if goalHull != None:
                        shipClassList = QuestConstants.getShipList(goalHull)
                        if shipClassList == None:
                            shipClassList = [
                                goalHull]
                        
                        if object.shipClass not in shipClassList:
                            return 1
                        
                    
                    goalFlagship = self._QuestGoal__goalData.get(self.FLAGSHIP_IDX, False)
                    if goalFlagship != object.isFlagship:
                        return 1
                    
                    if object.getTeam() == PiratesGlobals.PLAYER_TEAM:
                        return 1
                    
                    return 0
                
            elif not self.getTargetTypeOnlyOnOcean():
                if self._QuestGoal__goalData.get(self.TYPE_IDX) == AvatarTypes.AnyAvatar and goalOwner:
                    if TeamUtils.friendOrFoe(goalOwner, object) == PiratesGlobals.ENEMY:
                        return 0
                    
                elif object.getAvatarType().isA(self._QuestGoal__goalData.get(self.TYPE_IDX)):
                    return 0
                
            
        elif self._QuestGoal__goalData and object.getUniqueId() in self._QuestGoal__goalData:
            return 0
        
        return 1

    
    def getGoalIds(self, uidMgr = None, all = True):
        if all:
            results = [
                (0, '')]
        else:
            results = ''
        if self._QuestGoal__goalType == types.ListType:
            if all:
                uidData = self._QuestGoal__goalData
            else:
                uidData = self._QuestGoal__goalData[:1]
            if uidMgr:
                results = zip(map(lambda x: uidMgr.getDoId(x, None), uidData), uidData)
            elif len(uidData) == 0:
                results = ''
            else:
                results = uidData[0]
        
        return results

    
    def _asString(self):
        if self._QuestGoal__goalDataStr != None:
            return self._QuestGoal__goalDataStr
        
        if self._QuestGoal__goalData == None:
            resultStr = ''
        
        if self._QuestGoal__goalType == types.ListType:
            resultStr = str(self._QuestGoal__goalData)
        else:
            strRep = ''
            for currField in range(self.MAX_IDX):
                strRep += str(self._QuestGoal__goalData.get(currField, None))
                strRep += '-'
            
            resultStr = strRep
        self._QuestGoal__goalDataStr = resultStr
        return resultStr

    
    def __repr__(self):
        return self._asString()

    
    def __str__(self):
        return self._asString()

    
    def __cmp__(self, other):
        strRep = self._asString()
        otherStrRep = other._asString()
        if strRep < otherStrRep:
            return -1
        elif strRep > otherStrRep:
            return 1
        
        return 0

    
    def __hash__(self):
        result = hash(self._asString())
        return result



class QuestStep:
    STNPC = 1
    STItem = 2
    STArea = 3
    STTunnel = 4
    STExteriorDoor = 5
    STInteriorDoor = 6
    STDinghy = 7
    STShip = 8
    STNPCArea = 9
    STQuestNode = 10
    STNPCEnemy = 11
    STQuestProp = 12
    NullStep = None
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestStep')
    
    def __init__(self, originDoId, stepDoId, stepType, posH = (0, 0, 0, 0), islandUid = '', targetAreaUid = '', targetAvatarType = None, nodeSizes = (0, 0), nearOffset = (0, 0, 0), nearVis = (0, 0, 0)):
        self.originDoId = originDoId
        self.stepDoId = stepDoId
        self.stepType = stepType
        self.posH = posH
        self.islandUid = islandUid
        self.targetAreaUid = targetAreaUid
        self.targetAvatarType = targetAvatarType
        self.nodeSizes = nodeSizes
        self.nearOffset = nearOffset
        self.nearVis = nearVis

    
    def __repr__(self):
        return 'QuestStep(%d, %d, %d, %s, %s, %s, %s, %s, %s, %s)' % (self.getOriginDoId(), self.getStepDoId(), self.getStepType(), `self.getPosH()`, self.getIsland(), self.getTargetArea(), self.targetAvatarType, self.nodeSizes, self.nearOffset, self.nearVis)

    
    def __cmp__(self, other):
        if not not isinstance(other, QuestStep) and cmp(self.originDoId, other.originDoId) and cmp(self.stepDoId, other.stepDoId) and cmp(self.stepType, other.stepType) and cmp(self.posH, other.posH) and cmp(self.islandUid, other.islandUid) and cmp(self.targetAreaUid, other.targetAreaUid) and cmp(self.targetAvatarType, other.targetAvatarType) and cmp(self.nodeSizes, other.nodeSizes) and cmp(self.nearOffset, other.nearOffset):
            pass
        return cmp(self.nearVis, other.nearVis)

    
    def compareTarget(self, other):
        
        try:
            if not not isinstance(other, QuestStep) and cmp(self.originDoId, other.originDoId) and cmp(self.stepDoId, other.stepDoId) and cmp(self.stepType, other.stepType) and cmp(self.islandId, other.islandId) and cmp(self.targetAreaId, other.targetAreaId) and cmp(self.targetAvatarType, other.targetAvatarType) and cmp(self.nodeSizes, other.nodeSizes) and cmp(self.nearOffset, other.nearOffset):
                pass
            return cmp(self.nearVis, other.nearVis)
        except:
            self.notify.warning('error encountered when comparing queststeps %s and %s' % (self, other))
            return 0


    
    def getOriginDoId(self):
        return self.originDoId

    
    def getStepDoId(self):
        return self.stepDoId

    
    def getStepType(self):
        return self.stepType

    
    def getPosH(self):
        return self.posH

    
    def setIsland(self, islandUid = ''):
        self.islandUid = islandUid

    
    def getIsland(self):
        return self.islandUid

    
    def setTargetArea(self, targetUid = ''):
        self.targetAreaUid = targetUid

    
    def getTargetArea(self):
        return self.targetAreaUid

    
    def getNodeSizes(self):
        return self.nodeSizes

    
    def getNearOffset(self):
        return self.nearOffset

    
    def getNearVis(self):
        return self.nearVis

    
    def getNullStep():
        if QuestStep.NullStep:
            pass
        1
        QuestStep.NullStep = QuestStep(0, 0, 0)
        return QuestStep.NullStep

    getNullStep = staticmethod(getNullStep)
    
    def showIndicator(self):
        targetLocation = self.getTargetArea()
        parentObj = localAvatar.getParentObj()
        if config.GetBool('dynamic-rayoflight-area-only', True) and parentObj and hasattr(parentObj, 'uniqueId') and parentObj.uniqueId == targetLocation:
            return False
        
        return True



class QuestPath:
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestPath')
    
    def __init__(self, air):
        self.world = None
        self.posH = (0, 0, 0, 0)
        self.questSteps = { }
        self.islandStep = None
        self.islandDoId = None
        self.preferredStepUids = set()
        if __dev__:
            pass
        1

    
    def delete(self):
        self.islandDoId = None
        self.islandStep = None
        self.questSteps = { }
        self.world = None

    
    def setWorld(self, world):
        self.world = world

    
    def setQuestStepPosH(self, x, y, z, h):
        self.posH = (x, y, z, h)

    
    def getIslandDoId(self):
        if self.islandDoId:
            pass
        1
        if self._isIsland():
            self.islandDoId = self.doId
        
        return self.islandDoId

    
    def getQuestStepIsland(self):
        if self._isIsland():
            return QuestStep(0, self.getIslandDoId(), self._getQuestStepType())
        

    getQuestStepIsland = report(types = [
        'frameCount',
        'args'], dConfigParam = 'quest-indicator')(getQuestStepIsland)
    
    def getQuestStep(self, questDestUid, islandDoId, avId):
        if not self.getIslandDoId():
            self.getExitIslandStep()
        
        questIslandDoId = islandDoId
        questIsland = None
        isPrivate = False
        goalType = questDestUid.getType()
        if goalType != QuestGoal.Type_Custom:
            if islandDoId == None:
                questIslandDoId = self.world.getObjectIslandDoId(questDestUid)
            
            isPrivate = self.world.getObjectIsPrivate(questDestUid)
            if not questIslandDoId:
                return None
            
            questIsland = self.air.doId2do.get(questIslandDoId)
            if not questIsland:
                return None
            
        
        if questIslandDoId or goalType == QuestGoal.Type_Custom:
            if (self.getIslandDoId() == questIslandDoId or goalType == QuestGoal.Type_Custom) and not questDestUid.getTargetTypeOnlyOnOcean():
                islandObj = self.getIsland()
                if islandObj and goalType == QuestGoal.Type_Custom and islandObj.notHasQuestGoal(questDestUid):
                    return QuestStep.NullStep
                
                islandSearchResult = self.getIntoIslandStep(questDestUid, isPrivate, avId)
                if islandObj:
                    if islandSearchResult == None or islandSearchResult == QuestStep.NullStep:
                        islandObj.setNotHasQuestGoal(questDestUid)
                    else:
                        searchArea = self._checkNeedDinghyStep(avId, islandSearchResult.getOriginDoId())
                        if searchArea:
                            return self._getLocalDinghy(avId, questDestUid, searchArea = searchArea)
                        
                
                return islandSearchResult
            else:
                step = self.getExitIslandStep()
                if step:
                    return step
                else:
                    dinghyStep = self._getLocalDinghy(avId, questDestUid)
                    if dinghyStep:
                        return dinghyStep
                    else:
                        destIsland = self.air.doId2do.get(questIslandDoId)
                        if destIsland:
                            return QuestStep(self.doId, questIslandDoId, questIsland._getQuestStepType())
                        
        

    getQuestStep = report(types = [
        'frameCount',
        'args'], dConfigParam = 'quest-indicator')(getQuestStep)
    
    def _checkNeedDinghyStep(self, avId, goalOriginId):
        avObj = self.air.doId2do.get(avId)
        if avObj:
            avParent = avObj.getParentObj()
            avIsland = avParent.getIsland()
            if avParent is avIsland:
                if goalOriginId != avParent.doId:
                    return avParent
                
            
        

    
    def _getLocalDinghy(self, avId, questDestUid, searchArea = None):
        avObj = self.air.doId2do.get(avId)
        if avObj:
            avZone = avObj.zoneId
            if searchArea == None:
                searchArea = self
            
            dinghyId = self.world.queryGoalByObjectType(QuestGoal.GOAL_TYPE_DINGHY, avObj, questDestUid, searchArea)
            dinghyObj = self.air.doId2do.get(dinghyId)
            if dinghyObj:
                dinghyPos = dinghyObj.getPos(searchArea)
                return QuestStep(searchArea.doId, dinghyId, dinghyObj._getQuestStepType(), posH = (dinghyPos[0], dinghyPos[1], dinghyPos[2], dinghyObj.getH()), islandUid = self.getUniqueId())
            
        

    
    def getExitIslandStep(self):
        if self._isIsland() or self._isShip():
            return None
        
        if not self.islandStep:
            self._getIslandPath([], [], { })
        
        returnStep = copy.copy(self.islandStep)
        return returnStep

    getExitIslandStep = report(types = [
        'frameCount',
        'args'], dConfigParam = 'quest-indicator')(getExitIslandStep)
    
    def getIntoIslandStep(self, questDestUid, isPrivate, avId = None):
        questStep = self.questSteps.get(questDestUid)
        if not questStep or config.GetBool('cache-quest-step', 1) == 0:
            path = self._getQuestPath(questDestUid, isPrivate, [], [], { }, avId)
            if path:
                targetAreaUid = self.air.doId2do[path[len(path) - 1]].getParentObj().uniqueId
                questStep = self.questSteps.get(questDestUid)
                if questStep:
                    questStep.setTargetArea(targetAreaUid)
                
            
        
        if questDestUid.getType() == QuestGoal.Type_Custom:
            self.questSteps.pop(questDestUid, None)
        
        return questStep

    getIntoIslandStep = report(types = [
        'frameCount',
        'args'], dConfigParam = 'quest-indicator')(getIntoIslandStep)
    
    def getOntoOceanStep(self, questDestUid, avId):
        questIds = self.world.queryGoal(questDestUid, self, avId)
        for (questDoId, questUid) in questIds:
            questGoalObj = self.air.doId2do.get(questDoId)
            if questGoalObj:
                questDest = QuestStep(self.world.worldGrid.doId, questDoId, questGoalObj._getQuestStepType(), questGoalObj._getQuestStepPosH())
                avObj = self.air.doId2do.get(avId)
                if avObj:
                    avObj.setQuestGoalDoId(questGoalObj)
                
                return questDest
                continue
        
        return QuestStep.NullStep

    
    def _getExitLinkDoIds(self, questGoalUid):
        if __dev__:
            pass
        1
        return []

    
    def _getQuestStepType(self):
        if __dev__:
            pass
        1
        return 0

    
    def _isIsland(self):
        if __dev__:
            pass
        1
        return False

    
    def _isShip(self):
        return False

    
    def _getQuestStepPosH(self):
        return self.posH

    
    def _getIslandPath(self, alreadyVisited, needToVisit, pathDict):
        islandPath = []
        needToStore = False
        if not islandPath:
            if self._isIsland():
                islandPath = alreadyVisited + [
                    self.doId]
            
        
        if islandPath:
            finalPath = [
                islandPath[-1]]
            next = pathDict.get(finalPath[-1])
            while next:
                finalPath.append(next)
                next = pathDict.get(finalPath[-1])
            finalPath.reverse()
        
        exitLinks = islandPath
        for link in exitLinks:
            pathDict[link] = self.doId
        
        needToVisit += exitLinks
        if needToVisit:
            nextDoId = needToVisit.pop(0)
            nextStep = self.air.doId2do[nextDoId]
            finalPath = nextStep._getIslandPath(alreadyVisited + [
                self.doId], needToVisit, pathDict)
            needToStore = True
        else:
            finalPath = []
        if needToStore and self.doId in finalPath:
            self._storeIslandStep(finalPath)
        
        return finalPath

    _getIslandPath = report(types = [
        'frameCount',
        'args'], dConfigParam = 'quest-indicator')(_getIslandPath)
    
    def _storeIslandStep(self, path):
        stepDoId = path[path.index(self.doId) + 1]
        step = self.air.doId2do[stepDoId]
        if __dev__:
            pass
        1
        self.islandStep = QuestStep(self.doId, stepDoId, step._getQuestStepType(), step._getQuestStepPosH())
        self.islandDoId = step.islandDoId

    _storeIslandStep = report(types = [
        'frameCount',
        'args'], dConfigParam = 'quest-indicator')(_storeIslandStep)
    
    def _getQuestPath(self, questDestUid, isPrivate, alreadyVisited, needToVisit, pathDict, avId):
        questDest = None
        questPath = []
        needToStore = False
        if not isPrivate:
            if not questPath:
                questIds = self.world.queryGoal(questDestUid, self, avId)
                for (questDoId, questUid) in questIds:
                    questGoalObj = self.air.doId2do.get(questDoId)
                    if questGoalObj:
                        if questGoalObj.getParentObj() is self or questGoalObj is self:
                            if questDoId != self.doId:
                                pathDict.setdefault(questDoId, self.doId)
                                newIds = [
                                    self.doId,
                                    questDoId]
                            else:
                                newIds = [
                                    self.doId]
                            questPath = alreadyVisited + [
                                self.doId,
                                questDoId]
                            questDest = QuestStep(self.doId, questDoId, questGoalObj._getQuestStepType(), questGoalObj._getQuestStepPosH())
                            needToStore = True
                            avObj = self.air.doId2do.get(avId)
                            if avObj:
                                avObj.setQuestGoalDoId(questGoalObj)
                            
                            break
                        
                    elif questDoId != None:
                        pass
                    
                    if questDestUid.getType() != QuestGoal.Type_Custom and questUid:
                        
                        try:
                            objInfo = self.air.worldCreator.getObjectDataFromFileByUid(questUid, self.getFileName())
                            if objInfo:
                                if objInfo.get('Type') == 'Dinghy':
                                    pos = objInfo['Pos']
                                    hpr = objInfo['Hpr']
                                    questPath = alreadyVisited + [
                                        self.doId]
                                    questDest = QuestStep(self.doId, 0, QuestStep.STQuestNode, (pos[0], pos[1], pos[2], hpr[0]))
                                    needToStore = True
                                    break
                                elif objInfo.get('Type') == 'Quest Node':
                                    pos = objInfo['Pos']
                                    nodePos = None
                                    parentUid = self.air.worldCreator.getObjectDataFromFileByUid(questUid, self.getFileName(), getParentUid = True)
                                    if parentUid:
                                        parentObj = self.world.uidMgr.justGetMeMeObject(parentUid)
                                        if parentObj:
                                            tform = TransformState.makePosHpr(parentObj.getPos(self), parentObj.getHpr(self))
                                            nodePos = tform.getMat().xformPoint(pos)
                                        
                                    
                                    if nodePos == None:
                                        nodePos = pos
                                    
                                    hpr = objInfo['Hpr']
                                    at = int(float(objInfo['At']))
                                    near = int(float(objInfo['Near']))
                                    nearOffset = (int(objInfo['NearOffsetX']), int(objInfo['NearOffsetY']), int(objInfo['NearOffsetZ']))
                                    nearVis = (int(objInfo['NearVisX']), int(objInfo['NearVisY']), int(objInfo['NearVisZ']))
                                    questPath = alreadyVisited + [
                                        self.doId]
                                    questDest = QuestStep(self.doId, 0, QuestStep.STQuestNode, (nodePos[0], nodePos[1], nodePos[2], hpr[0]), nodeSizes = [
                                        at,
                                        near], nearOffset = nearOffset, nearVis = nearVis)
                                    needToStore = True
                                    break
                                elif objInfo.get('Type') == 'Object Spawn Node':
                                    pos = objInfo['Pos']
                                    hpr = objInfo['Hpr']
                                    questPath = alreadyVisited + [
                                        self.doId]
                                    questDest = QuestStep(self.doId, 0, QuestStep.STArea, (pos[0], pos[1], pos[2], hpr[0]))
                                    needToStore = True
                                    break
                                
                        except AttributeError:
                            pass
                        

                
            
        elif not questPath:
            if self.air.worldCreator.isObjectDefined(questDestUid.getGoalIds(all = False), self.world.getFileName() + '.py'):
                questPath = alreadyVisited + [
                    self.doId]
                needToStore = False
            
        
        if questPath:
            finalPath = [
                questPath[-1]]
            next = pathDict.get(finalPath[-1])
            while next:
                finalPath.append(next)
                next = pathDict.get(finalPath[-1])
            finalPath.reverse()
        
        exitLinks = questPath
        for link in exitLinks:
            pathDict[link] = self.doId
        
        needToVisit += exitLinks
        if needToVisit:
            nextDoId = needToVisit.pop(0)
            nextStep = self.air.doId2do[nextDoId]
            finalPath = nextStep._getQuestPath(questDestUid, isPrivate, alreadyVisited + [
                self.doId], needToVisit, pathDict, avId)
            if questDestUid.getType() == QuestGoal.Type_Custom:
                nextStep.questSteps.pop(questDestUid, None)
            
            needToStore = True
        else:
            finalPath = []
            needToStore = True
        if needToStore and self.doId in finalPath:
            self._storeQuestStep(finalPath, questDestUid, questDest)
        
        if not finalPath:
            self._storeQuestStep(finalPath, questDestUid, questStep = QuestStep.getNullStep())
        
        return finalPath

    _getQuestPath = report(types = [
        'frameCount',
        'args'], dConfigParam = 'quest-indicator')(_getQuestPath)
    
    def _storeQuestStep(self, path, questDestUid, questStep = None):
        if not questStep:
            stepDoId = path[path.index(self.doId) + 1]
            step = self.air.doId2do[stepDoId]
            if __dev__:
                pass
            1
            questStep = QuestStep(self.doId, stepDoId, step._getQuestStepType(), step._getQuestStepPosH())
        
        self.questSteps[questDestUid] = questStep

    _storeQuestStep = report(types = [
        'frameCount',
        'args'], dConfigParam = 'quest-indicator')(_storeQuestStep)
    
    def setAsPreferredStepFor(self, questGoalUid):
        self.preferredStepUids.add(questGoalUid)

    
    def isPreferredStep(self, questGoalUid):
        return questGoalUid in self.preferredStepUids


