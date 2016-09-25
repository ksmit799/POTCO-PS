# File: S (Python 2.4)

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.reputation import ReputationGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import InventoryItemList
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import GuiButton
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import GuiButton
from pirates.piratesgui import PurchaseList
from pirates.battle import WeaponGlobals
from pirates.uberdog.UberDogGlobals import *
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import *
from pirates.piratesgui.TabBar import LeftTab, TabBar
from pirates.inventory import ItemGlobals
from pirates.inventory.InventoryGlobals import *
from pirates.uberdog.TradableInventoryBase import InvItem

class StoreTab(LeftTab):
    
    def __init__(self, tabBar, name, **kw):
        optiondefs = (('modelName', 'general_frame_d', None), ('borderScale', 0.38, None), ('bgBuffer', 0.14999999999999999, None))
        self.defineoptions(kw, optiondefs)
        LeftTab.__init__(self, tabBar, name, **None)
        self.initialiseoptions(StoreTab)



class StoreTabBar(TabBar):
    
    def refreshTabs(self):
        for (x, name) in enumerate(self.tabOrder):
            tab = self.tabs[name]
            tab.reparentTo(self.bParent)
            tab.setPos(-0.070000000000000007, 0, 1.1000000000000001 - 0.10000000000000001 * (x + self.offset))
            (tab.setScale(0.20000000000000001, 1, 0.20000000000000001),)
        
        self.activeIndex = max(0, min(self.activeIndex, len(self.tabOrder) - 1))
        if len(self.tabOrder):
            name = self.tabOrder[self.activeIndex]
            tab = self.tabs[name]
            tab.reparentTo(self.fParent)
            tab.setX(-0.080000000000000002)
            tab.setScale(0.20000000000000001, 1, 0.22)
        

    
    def makeTab(self, name, **kw):
        return StoreTab(self, name, **None)



class StoreGUI(DirectFrame):
    notify = directNotify.newCategory('StoreGUI')
    width = (PiratesGuiGlobals.InventoryItemGuiWidth + PiratesGuiGlobals.ScrollbarSize + 0.059999999999999998) * 2
    height = 1.3500000000000001
    columnWidth = PiratesGuiGlobals.InventoryItemGuiWidth + PiratesGuiGlobals.ScrollbarSize + 0.050000000000000003
    CoinImage = None
    WeaponIcons = None
    SkillIcons = None
    FishingIcons = None
    
    def __init__(self, inventory, name, **kw):
        optiondefs = (('relief', None, None), ('framSize', (0, self.width, 0, self.height), None), ('sortOrder', 20, None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, None, **None)
        self.initialiseoptions(StoreGUI)
        if not StoreGUI.CoinImage:
            StoreGUI.CoinImage = loader.loadModel('models/gui/toplevel_gui').find('**/treasure_w_coin*')
        
        if not StoreGUI.WeaponIcons:
            StoreGUI.WeaponIcons = loader.loadModel('models/gui/gui_icons_weapon')
        
        if not StoreGUI.SkillIcons:
            StoreGUI.SkillIcons = loader.loadModel('models/textureCards/skillIcons')
        
        if not StoreGUI.FishingIcons:
            StoreGUI.FishingIcons = loader.loadModel('models/textureCards/fishing_icons')
        
        self.backTabParent = self.attachNewNode('backTabs', sort = 0)
        self.panel = GuiPanel.GuiPanel(name, self.width, self.height, parent = self)
        self.panel.closeButton['command'] = self.closePanel
        self.setPos(-1.1000000000000001, 0, -0.66000000000000003)
        self.balance = 0
        self.inventory = inventory
        self.storeInventory = InventoryItemList.InventoryItemList(self.inventory, self.height - 0.14999999999999999, buy = PiratesGuiGlobals.InventoryAdd)
        self.storeInventory.reparentTo(self.panel)
        self.storeInventory.setPos(0.029999999999999999, 0, 0.040000000000000001)
        self.storeInventory.sortByTypeAndLevel()
        self.cartWidth = self.columnWidth - 0.10000000000000001
        self.cartHeight = self.height - 0.25
        self.cartFrame = DirectFrame(parent = self.panel, relief = None, frameSize = (0, self.cartWidth, 0, self.cartHeight))
        self.cartFrame.setPos(self.columnWidth + 0.025000000000000001, 0, 0.080000000000000002)
        self.purchaseTitle = DirectFrame(parent = self.cartFrame, relief = None, text = PLocalizer.PurchaseCart, text_fg = PiratesGuiGlobals.TextFG1, text_align = TextNode.ACenter, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (0.0, -0.029999999999999999), textMayChange = 0, pos = (self.cartWidth / 2, 0, self.cartHeight))
        self.purchaseInventory = PurchaseList.PurchaseList([], self.cartHeight - 0.25, buy = PiratesGuiGlobals.InventoryRemove)
        self.purchaseInventory.reparentTo(self.cartFrame)
        self.purchaseInventory.setPos(0, 0, 0.20000000000000001)
        self.frontTabParent = self.panel.attachNewNode('frontTab', sort = 2)
        self.balanceTitle = DirectFrame(parent = self.cartFrame, relief = None, text = PLocalizer.Total, text_fg = PiratesGuiGlobals.TextFG2, text_align = TextNode.ALeft, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (0.0, 0.0), pos = (0.01, 0, 0.22500000000000001))
        self.balanceValue = DirectFrame(parent = self.cartFrame, relief = None, text = str(self.balance), text_fg = PiratesGuiGlobals.TextFG2, text_align = TextNode.ARight, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (-0.055, 0.0), textMayChange = 1, image = StoreGUI.CoinImage, image_scale = 0.14999999999999999, image_pos = (-0.025000000000000001, 0, 0.025000000000000001), pos = (self.cartWidth, 0, 0.22500000000000001))
        self.myGoldTitle = DirectFrame(parent = self.cartFrame, relief = None, text = PLocalizer.YourMoney, text_fg = PiratesGuiGlobals.TextFG2, text_align = TextNode.ALeft, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (0.0, 0.0), pos = (0.01, 0, 0.155))
        self.myGold = DirectFrame(parent = self.cartFrame, relief = None, text = str(localAvatar.getMoney()), text_fg = PiratesGuiGlobals.TextFG2, text_align = TextNode.ARight, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (-0.055, 0.0), textMayChange = 1, image = StoreGUI.CoinImage, image_scale = 0.14999999999999999, image_pos = (-0.025000000000000001, 0, 0.025000000000000001), pos = (self.cartWidth, 0, 0.155))
        self.commitButton = GuiButton.GuiButton(command = self.handleCommitPurchase, parent = self.cartFrame, text = PLocalizer.PurchaseCommit, text_fg = PiratesGuiGlobals.TextFG2, text_pos = (0, -(PiratesGuiGlobals.TextScaleLarge) * 0.25), text_scale = PiratesGuiGlobals.TextScaleLarge, pos = (self.width - 0.20000000000000001, 0, 0.074999999999999997))
        self.commitButton.setPos(self.cartWidth / 2, 0, 0.050000000000000003)
        self.initTabs()
        self.updateBalance()
        self.accept(getCategoryChangeMsg(localAvatar.getInventoryId(), InventoryType.ItemTypeMoney), self.updateBalance)
        self.accept(PiratesGuiGlobals.InventoryBuyEvent, self.handleBuyItem)
        base.localAvatar.guiMgr.setIgnoreEscapeHotKey(True)
        self.acceptOnce('escape', self.closePanel)

    
    def closePanel(self):
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr and base.localAvatar.guiMgr.mainMenu and not base.localAvatar.guiMgr.mainMenu.isHidden():
            base.localAvatar.guiMgr.toggleMainMenu()
        elif hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            base.localAvatar.guiMgr.setIgnoreEscapeHotKey(False)
            messenger.send('exitStore')
            self.ignoreAll()
        

    
    def handleBuyItem(self, data, useCode):
        itemId = data[0]
        if not itemId:
            return None
        
        itemType = EconomyGlobals.getItemType(itemId)
        if itemType <= ItemType.WAND or itemType == ItemType.POTION:
            data[1] = 1
        else:
            data[1] = EconomyGlobals.getItemQuantity(itemId)
        inventory = base.localAvatar.getInventory()
        if not inventory:
            return None
        
        itemQuantity = self.purchaseInventory.getItemQuantity(itemId)
        currStock = inventory.getStackQuantity(itemId)
        currStockLimit = inventory.getStackLimit(itemId)
        if useCode == PiratesGuiGlobals.InventoryAdd:
            itemTypeName = PLocalizer.InventoryItemClassNames.get(itemType)
            trainingReq = EconomyGlobals.getItemTrainingReq(itemId)
            if trainingReq:
                amt = inventory.getStackQuantity(trainingReq)
                if not amt:
                    base.localAvatar.guiMgr.createWarning(PLocalizer.NoTrainingWarning % itemTypeName, PiratesGuiGlobals.TextFG6)
                    return None
                
            
            itemType = EconomyGlobals.getItemType(itemId)
            if itemType != ItemType.POTION:
                minLvl = ItemGlobals.getWeaponRequirement(itemId)
            else:
                minLvl = 0
            repId = WeaponGlobals.getRepId(itemId)
            repAmt = inventory.getAccumulator(repId)
            if minLvl > ReputationGlobals.getLevelFromTotalReputation(repId, repAmt)[0]:
                base.localAvatar.guiMgr.createWarning(PLocalizer.LevelReqWarning % (minLvl, itemTypeName), PiratesGuiGlobals.TextFG6)
                return None
            
            if itemId in ItemGlobals.getAllWeaponIds():
                locatables = []
                for dataInfo in self.purchaseInventory.inventory:
                    dataId = dataInfo[0]
                    if dataId in ItemGlobals.getAllWeaponIds():
                        locatables.append(InvItem([
                            InventoryType.ItemTypeWeapon,
                            dataId,
                            0]))
                        continue
                
                locatables.append(InvItem([
                    InventoryType.ItemTypeWeapon,
                    itemId,
                    0]))
                locationIds = inventory.canAddLocatables(locatables)
                for locationId in locationIds:
                    if locationId in (Locations.INVALID_LOCATION, Locations.NON_LOCATION):
                        base.localAvatar.guiMgr.createWarning(PLocalizer.InventoryFullWarning, PiratesGuiGlobals.TextFG6)
                        return None
                        continue
                
            elif itemId in ItemGlobals.getAllConsumableIds():
                itemQuantity = self.purchaseInventory.getItemQuantity(itemId)
                currStock = inventory.getItemQuantity(InventoryType.ItemTypeConsumable, itemId)
                currStockLimit = inventory.getItemLimit(InventoryType.ItemTypeConsumable, itemId)
                if currStock + itemQuantity >= currStockLimit:
                    base.localAvatar.guiMgr.createWarning(PLocalizer.TradeItemFullWarning, PiratesGuiGlobals.TextFG6)
                    return None
                
                if currStock == 0:
                    locatables = []
                    dataIds = { }
                    for dataInfo in self.purchaseInventory.inventory:
                        dataId = dataInfo[0]
                        if dataId in ItemGlobals.getAllConsumableIds():
                            if dataIds.has_key(dataId):
                                dataIds[dataId] += 1
                            else:
                                dataIds[dataId] = 1
                        dataIds.has_key(dataId)
                    
                    if dataIds.has_key(itemId):
                        dataIds[itemId] += 1
                    else:
                        dataIds[itemId] = 1
                    for dataId in dataIds:
                        locatables.append(InvItem([
                            InventoryType.ItemTypeConsumable,
                            dataId,
                            0,
                            dataIds[dataId]]))
                    
                    locationIds = inventory.canAddLocatables(locatables)
                    for locationId in locationIds:
                        if locationId in (Locations.INVALID_LOCATION, Locations.NON_LOCATION):
                            base.localAvatar.guiMgr.createWarning(PLocalizer.InventoryFullWarning, PiratesGuiGlobals.TextFG6)
                            return None
                            continue
                    
                
            else:
                itemQuantity = self.purchaseInventory.getItemQuantity(itemId)
                currStock = inventory.getStackQuantity(itemId)
                currStockLimit = inventory.getStackLimit(itemId)
                itemCategory = EconomyGlobals.getItemCategory(itemId)
                if currStock + itemQuantity >= currStockLimit:
                    base.localAvatar.guiMgr.createWarning(PLocalizer.TradeItemFullWarning, PiratesGuiGlobals.TextFG6)
                    return None
                
            self.purchaseInventory.addPanel(data)
            self.purchaseInventory.inventory.append(data)
        elif useCode == PiratesGuiGlobals.InventoryRemove:
            self.purchaseInventory.removePanel(data)
        
        panel = self.storeInventory.getPanel(data)
        if panel:
            self.checkPanel(panel, inventory, itemId)
        
        self.updateBalance()

    
    def handleCommitPurchase(self):
        if self.purchaseInventory == []:
            base.localAvatar.guiMgr.createWarning(PLocalizer.EmptyPurchaseWarning, PiratesGuiGlobals.TextFG6)
            return None
        
        inventory = base.localAvatar.getInventory()
        if inventory:
            if inventory.getGoldInPocket() < self.balance:
                base.localAvatar.guiMgr.createWarning(PLocalizer.NotEnoughMoneyWarning, PiratesGuiGlobals.TextFG6)
                return None
            
            if self.balance < 0 and inventory.getGoldInPocket() + self.balance > GOLD_CAP:
                base.localAvatar.guiMgr.createWarning(PLocalizer.CannotHoldGoldWarning, PiratesGuiGlobals.TextFG6)
                return None
            
        
        StoreGUI.notify.debug('Make Purchase - Buying: %s' % self.purchaseInventory.inventory)
        messenger.send('makeSale', [
            self.purchaseInventory.inventory,
            []])

    
    def updateBalance(self, extraArgs = None):
        self.myGold['text'] = str(localAvatar.getMoney())
        self.balance = 0
        for item in self.purchaseInventory.panels:
            self.balance += max(item.price, 0)
        
        if self.balance > 0:
            self.balanceTitle['text'] = PLocalizer.Total
            self.balanceValue['text'] = str(abs(self.balance))
        elif self.balance < 0:
            self.balanceTitle['text'] = PLocalizer.Gain
            self.balanceValue['text'] = str(abs(self.balance))
        else:
            self.balanceTitle['text'] = PLocalizer.Total
            self.balanceValue['text'] = str(abs(self.balance))
        if self.balance > localAvatar.getMoney() or self.purchaseInventory.inventory == []:
            if self.balance > localAvatar.getMoney():
                self.balanceValue['text_fg'] = PiratesGuiGlobals.TextFG6
            
            self.commitButton['state'] = DGG.DISABLED
        else:
            self.balanceValue['text_fg'] = PiratesGuiGlobals.TextFG2
            self.commitButton['state'] = DGG.NORMAL
        inventory = base.localAvatar.getInventory()
        if inventory:
            if inventory.getGoldInPocket() < self.balance or self.purchaseInventory.inventory == []:
                self.commitButton['frameColor'] = PiratesGuiGlobals.ButtonColor3
            else:
                self.commitButton['frameColor'] = PiratesGuiGlobals.ButtonColor4
        

    
    def checkPanel(self, panel, inventory, itemId):
        purchaseQty = self.purchaseInventory.getItemQuantity(itemId)
        panel.checkPlayerInventory(itemId, purchaseQty)

    
    def initTabs(self):
        self.tabBar = StoreTabBar(parent = self, backParent = self.backTabParent, frontParent = self.frontTabParent, offset = 0)
        self.pageNames = []
        self.createTabs()
        if len(self.pageNames) > 0:
            self.setPage(self.pageNames[0])
        

    
    def createTabs(self):
        for item in self.inventory:
            if item == InventoryType.ShipRepairKit:
                if not base.config.GetBool('want-privateering', 1):
                    continue
                
            
            if not self.isPageAdded(getItemGroup(item)):
                self.addTab(getItemGroup(item), item)
                continue
        

    
    def addTab(self, itemGroup, item):
        newTab = self.tabBar.addTab(itemGroup, command = self.setPage, extraArgs = [
            itemGroup])
        repId = WeaponGlobals.getRepId(item)
        if repId:
            iconName = ReputationGlobals.RepIcons.get(repId)
            if repId == InventoryType.FishingRep:
                icon = StoreGUI.FishingIcons.find('**/%s' % iconName)
            else:
                icon = StoreGUI.WeaponIcons.find('**/%s' % iconName)
        elif InventoryType.begin_Consumables <= item:
            pass
        elif repId or ItemGlobals.getClass(item) == InventoryType.ItemTypeConsumable:
            iconName = EconomyGlobals.getItemIcons(item)
            icon = StoreGUI.SkillIcons.find('**/%s' % iconName)
        elif InventoryType.begin_WeaponCannonAmmo <= item:
            pass
        elif ItemGlobals.getClass(item) == InventoryType.ItemTypeConsumable:
            iconName = EconomyGlobals.getItemIcons(InventoryType.CannonL1)
            icon = StoreGUI.WeaponIcons.find('**/%s' % iconName)
        elif InventoryType.begin_WeaponGrenadeAmmo <= item:
            pass
        elif ItemGlobals.getClass(item) == InventoryType.ItemTypeConsumable:
            itemId = InventoryType.GrenadeWeaponL1
            iconName = EconomyGlobals.getItemIcons(itemId)
            icon = StoreGUI.WeaponIcons.find('**/%s' % iconName)
        elif InventoryType.begin_FishingLures <= item:
            pass
        elif ItemGlobals.getClass(item) == InventoryType.ItemTypeConsumable:
            icon = StoreGUI.FishingIcons.find('**/pir_t_gui_gen_fish_lure')
        else:
            icon = None
        newTab.nameTag = DirectLabel(parent = newTab, relief = None, state = DGG.DISABLED, image = icon, image_scale = 0.40000000000000002, image_pos = (0, 0, 0.040000000000000001), pos = (0.059999999999999998, 0, -0.035000000000000003))
        self.pageNames.append(itemGroup)

    
    def isPageAdded(self, pageName):
        return self.pageNames.count(pageName) > 0

    
    def setPage(self, pageName):
        self.tabBar.unstash()
        self.storeInventory.filterByItemGroup(pageName)


