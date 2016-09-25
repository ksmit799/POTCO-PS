# File: Q (Python 2.4)

from direct.directnotify import DirectNotifyGlobal
from pirates.quest import QuestLadderDB
from pirates.uberdog import DistributedInventoryBase
from pirates.piratesbase.PLocalizer import NPCNames

class QuestStatus:
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestStatus')
    
    def __init__(self, av):
        self.av = av
        self.ladders = { }
        self.choiceContainers = { }
        self.invRequest = DistributedInventoryBase.DistributedInventoryBase.getInventory(self.av.inventoryId, self.createLadders)
        self.NPCInteractMode = False
        self.cacheHistoryMode = False
        self.ladderDeleteList = []
        self.initialized = False

    
    def delete(self):
        
        try:
            pass
        except:
            self.QuestStatus_deleted = 1
            self.choiceContainers = { }
            for ladder in self.ladders.values():
                ladder.destroy()
            
            self.ladders = { }
            self.ladderDeleteList = []
            self.av = None
            DistributedInventoryBase.DistributedInventoryBase.cancelGetInventory(self.invRequest)


    
    def forceInit(self):
        if not self.initialized:
            inv = localAvatar.getInventory()
            if inv:
                self.createLadders(inv)
                self.initialized = True
            else:
                self.notify.warning('inventory not available yet!')
        

    
    def createLadders(self, inventory):
        if inventory:
            for quest in inventory.getQuestList():
                self.assignQuest(quest)
            
            ladderChoiceContainers = []
            for ladder in self.ladders.values():
                ladder.getChoiceContainers(ladderChoiceContainers)
            
            choiceInts = self.av.getCurrentQuestChoiceContainers()
            for container in ladderChoiceContainers:
                containerInt = container.getQuestInt()
                if containerInt in choiceInts:
                    self.choiceContainers[container.getName()] = container
                    continue
            
        

    
    def assignQuest(self, quest, populateHistory = False):
        questId = quest.getQuestId()
        for (ladderId, ladderDNA) in QuestLadderDB.FameQuestLadderDict.items():
            if ladderDNA.hasQuest(questId):
                if not self.ladders.has_key(ladderId):
                    self.ladders[ladderId] = ladderDNA.constructDynamicCopy(self.av)
                
                ladder = self.ladders[ladderId]
                if ladder.linkQuest(quest):
                    if populateHistory:
                        questStub = ladder.getQuestStub(questId)
                        self.cacheHistoryMode = True
                        questStub.completePreviousContainers()
                        self.cacheHistoryMode = False
                    
                
            ladder.linkQuest(quest)
        
        for (ladderId, ladderDNA) in QuestLadderDB.FortuneQuestLadderDict.items():
            if ladderDNA.hasQuest(questId):
                if not self.ladders.has_key(ladderId):
                    self.ladders[ladderId] = ladderDNA.constructDynamicCopy(self.av)
                
                ladder = self.ladders[ladderId]
                if ladder.linkQuest(quest):
                    if populateHistory:
                        questStub = ladder.getQuestStub(questId)
                        self.cacheHistoryMode = True
                        questStub.completePreviousContainers()
                        self.cacheHistoryMode = False
                    
                
            ladder.linkQuest(quest)
        
        if populateHistory:
            self.writeHistory()
        

    
    def handleQuestDropped(self, droppedQuestId):
        for ladder in self.ladders.values():
            if ladder.hasQuest(droppedQuestId):
                self.clearLadderFromHistory(ladder)
                self.deleteLadder(ladder.getName())
                continue
        

    
    def handleLadderComplete(self, ladder):
        ladderName = ladder.getName()
        if not self.ladders.has_key(ladderName):
            self.notify.warning('%s not in ladders dict!' % ladderName)
            ladder.destroy()
        else:
            self.ladderDeleteList.append(ladderName)

    
    def deleteLadder(self, ladderName):
        if self.ladders.has_key(ladderName):
            self.ladders[ladderName].destroy()
            del self.ladders[ladderName]
        else:
            self.notify.warning('%s not in ladders dict!' % ladderName)

    
    def getCurrentQuests(self):
        inventory = self.av.getInventory()
        if not inventory:
            self.notify.warning('av: %s has no inventory!' % self.av.getDoId())
            return []
        
        quests = inventory.getQuestList()
        if len(quests) == 0:
            self.notify.warning('av: %s has no active quests!' % self.av.getDoId())
            return []
        
        return quests

    
    def getCurrentQuest(self, questId):
        quests = self.getCurrentQuests()
        for q in quests:
            if q.questId == questId:
                return q
                continue
        

    
    def addCurrentQuestChoiceContainer(self, container):
        nameInt = container.getQuestInt()
        containers = self.av.getCurrentQuestChoiceContainers()
        if nameInt in containers:
            self.notify.warning('%d already in choice container list!' % nameInt)
            return None
        
        containers.append(nameInt)
        if self.cacheHistoryMode == False:
            self.av.b_setCurrentQuestChoiceContainers(containers)
        else:
            self.av.setCurrentQuestChoiceContainers(containers)
        self.choiceContainers[container.getName()] = container

    
    def removeCurrentQuestChoiceContainer(self, container):
        nameInt = container.getQuestInt()
        containers = self.av.getCurrentQuestChoiceContainers()
        if nameInt in containers:
            containers.remove(nameInt)
        
        if self.cacheHistoryMode == False:
            self.av.b_setCurrentQuestChoiceContainers(containers)
        else:
            self.av.setCurrentQuestChoiceContainers(containers)
        name = container.getName()
        if self.choiceContainers.has_key(name):
            del self.choiceContainers[name]
        

    
    def clearHistory(self):
        ladderHistory = self.av.getQuestLadderHistory()
        if len(ladderHistory):
            self.av.b_setQuestLadderHistory([])
        

    
    def writeHistory(self):
        ladderHistory = self.av.getQuestLadderHistory()
        self.av.b_setQuestLadderHistory(ladderHistory)
        choiceContainers = self.av.getCurrentQuestChoiceContainers()
        self.av.b_setCurrentQuestChoiceContainers(choiceContainers)

    
    def removeFromHistory(self, ladder):
        ladderHistory = self.av.getQuestLadderHistory()
        ladderInt = ladder.getQuestInt()
        if ladderInt in ladderHistory:
            ladderHistory.remove(ladderInt)
        
        self.av.setQuestLadderHistory(ladderHistory)

    
    def getClearedLadderFromHistory(self, ladder, ladderHistory):
        ladderInt = ladder.getQuestInt()
        if ladderInt in ladderHistory:
            ladderHistory.remove(ladderInt)
        
        for container in ladder.getContainers():
            ladderHistory = self.getClearedLadderFromHistory(container, ladderHistory)
        
        return ladderHistory

    
    def clearLadderFromHistory(self, ladder):
        ladderHistory = self.av.getQuestLadderHistory()
        ladderHistory = self.getClearedLadderFromHistory(ladder, ladderHistory)
        self.av.setQuestLadderHistory(ladderHistory)

    
    def updateHistory(self, completedContainer):
        if completedContainer.isChoice():
            self.removeCurrentQuestChoiceContainer(completedContainer)
        
        ladderHistory = self.av.getQuestLadderHistory()
        downstreamContainers = []
        completedContainer.getDownstreamContainers(downstreamContainers)
        for container in downstreamContainers:
            questInt = container.getQuestInt()
            if questInt in ladderHistory:
                self.notify.warning('For avatar: %s; Purging child questInt: %s' % (self.av.doId, questInt))
                ladderHistory.remove(questInt)
                continue
        
        newQuestInt = completedContainer.getQuestInt()
        if newQuestInt not in ladderHistory:
            ladderHistory.append(newQuestInt)
        else:
            self.notify.warning('%d already in ladder history' % newQuestInt)
        if self.cacheHistoryMode == False:
            self.av.b_setQuestLadderHistory(ladderHistory)
        else:
            self.av.setQuestLadderHistory(ladderHistory)

    
    def _QuestStatus__getDeepestChoiceContainerWithGiver(self, giverId):
        deepestContainer = None
        for container in self.choiceContainers.values():
            if giverId == container.getGiverId():
                deepestContainer = container
                continue
        
        return deepestContainer

    
    def getQuestOffersFromGiver(self, giverId):
        quests = self.getCurrentQuests()
        if not quests:
            return (None, None, 0)
        
        container = self._QuestStatus__getDeepestChoiceContainerWithGiver(giverId)
        if not container:
            return (None, None, 0)
        
        offers = container.getValidContainers()
        finalOffers = []
        completedLadders = self.av.getQuestLadderHistory()
        for offer in offers:
            if offer.getQuestInt() not in completedLadders:
                finalOffers = [
                    offer] + finalOffers
                continue
        
        totalOffers = container.getContainers()
        numIncomplete = 0
        for offer in totalOffers:
            if offer.getQuestInt() not in completedLadders:
                numIncomplete = numIncomplete + 1
                continue
        
        numAssignedIncomplete = numIncomplete - len(finalOffers)
        if len(finalOffers) == 0:
            pass
        1
        return (finalOffers, container, numAssignedIncomplete)

    
    def hasLadderQuest(self, quest):
        return self.hasLadderQuestId(quest.getQuestId())

    
    def hasLadderQuestId(self, questId):
        for currLadder in self.ladders.values():
            if currLadder.hasQuest(questId):
                return True
                continue
        
        return False

    
    def getContainer(self, name):
        for ladder in self.ladders.values():
            ctr = ladder.getContainer(name)
            if ctr:
                return ctr
                continue
        

    
    def getLadderIdWithQuestId(self, questId):
        for ladder in self.ladders.values():
            if ladder.hasQuest(questId):
                return ladder.getName()
                continue
        

    
    def hasQuestIdLadderId(self, questId, ladderId):
        ladder = self.ladders.get(ladderId)
        if ladder:
            return ladder.hasQuest(questId)
        else:
            self.notify.warning('%s not in ladder list!' % ladderId)
            return False

    
    def getQuestStub(self, questId):
        for currLadder in self.ladders.values():
            stub = currLadder.getQuestStub(questId)
            if stub:
                return stub
                continue
        

    
    def getNextQuestId(self, questId):
        for currLadder in self.ladders.values():
            if currLadder.hasQuest(questId):
                return currLadder.getNextQuestId(questId)
                continue
        

    
    def getSiblingQuestIds(self, questId):
        for currLadder in self.ladders.values():
            if currLadder.hasQuest(questId):
                return currLadder.getSiblingQuestIds(questId)
                continue
        
        return []

    
    def getCompletedContainer(self, questId, completedStubCount):
        ladderId = self.av.questStatus.getLadderIdWithQuestId(questId)
        container = self.ladders[ladderId].getContainer(questId)
        lastCompleted = container
        while lastCompleted.isComplete():
            if lastCompleted.parent and lastCompleted.parent.isComplete():
                lastCompleted = lastCompleted.parent
                continue
            return lastCompleted
        ladderHistory = self.av.getQuestLadderHistory()
        for containerInt in ladderHistory:
            for ladder in self.ladders.values():
                container = ladder.getContainerInt(containerInt)
                if container:
                    includeSelf = True
                    if completedStubCount > 1:
                        if questId == container.getName():
                            self.notify.debug('getCompletedContainer().questId Excluded: %s' % questId)
                            self.notify.debug('getCompletedContainer().completedStubCount: %s' % completedStubCount)
                            includeSelf = False
                        
                    
                    if container and container.hasQuest(questId) and includeSelf:
                        ladderName = ladder.getName()
                        if ladderName in self.ladderDeleteList:
                            self.deleteLadder(ladderName)
                            self.ladderDeleteList.remove(ladderName)
                        
                        self.notify.debug('getCompletedContainer().container.getName() Returned: %s' % container.getName())
                        return container
                    
            
        

    
    def dropSameLadderQuests(self, questId):
        droppedQuests = []
        for (ladderId, ladderDNA) in QuestLadderDB.FameQuestLadderDict.items():
            if ladderDNA.hasQuest(questId):
                currQuests = self.av.getInventory().getQuestList()
                for quest in currQuests:
                    if ladderDNA.hasQuest(quest.getQuestId()):
                        droppedQuests.append(quest.getDeletedEventString())
                        simbase.air.questMgr.dropQuest(self.av, quest)
                        continue
                
        
        for (ladderId, ladderDNA) in QuestLadderDB.FortuneQuestLadderDict.items():
            if ladderDNA.hasQuest(questId):
                currQuests = self.av.getInventory().getQuestList()
                for quest in currQuests:
                    if ladderDNA.hasQuest(quest.getQuestId()):
                        droppedQuests.append(quest.getDeletedEventString())
                        simbase.air.questMgr.dropQuest(self.av, quest)
                        continue
                
        
        return droppedQuests

    
    def setNPCInteractMode(self, mode):
        self.NPCInteractMode = mode

    
    def getNPCInteractMode(self):
        return self.NPCInteractMode

    
    def getFortuneOffers(self, giverId):
        offers = []
        for ladder in QuestLadderDB.FortuneQuestLadderDict.values():
            if giverId == ladder.getGiverId():
                offers.append(ladder)
                continue
        
        return offers


