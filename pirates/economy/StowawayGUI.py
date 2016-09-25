# File: S (Python 2.4)

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.audio import SoundGlobals
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
from pirates.piratesgui.StowawayItemGui import StowawayItemGui
from pirates.audio.SoundGlobals import loadSfx

class StowawayGUI(DirectFrame):
    notify = directNotify.newCategory('StowawayGUI')
    width = PiratesGuiGlobals.InventoryItemGuiWidth + PiratesGuiGlobals.ScrollbarSize + 0.059999999999999998
    height = 1.3500000000000001
    columnWidth = PiratesGuiGlobals.InventoryItemGuiWidth + PiratesGuiGlobals.ScrollbarSize + 0.050000000000000003
    CoinImage = None
    CrateShutSound = None
    
    def __init__(self, inventory, name, **kw):
        optiondefs = (('relief', None, None), ('framSize', (0, self.width, 0, self.height), None), ('sortOrder', 20, None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, None, **None)
        self.initialiseoptions(StowawayGUI)
        if not StowawayGUI.CoinImage:
            StowawayGUI.CoinImage = loader.loadModel('models/gui/toplevel_gui').find('**/treasure_w_coin*')
        
        if not StowawayGUI.CrateShutSound:
            StowawayGUI.CrateShutSound = loadSfx(SoundGlobals.SFX_STOWAWAY_CRATE_SHUT)
        
        self.panel = GuiPanel.GuiPanel(name, self.width, self.height, parent = self)
        self.panel.closeButton['command'] = self.closePanel
        self.setPos(-0.80000000000000004, 0, -0.66000000000000003)
        self.balance = 0
        self.inventory = inventory
        self.storeInventory = InventoryItemList.InventoryItemList(self.inventory, self.height - 0.14999999999999999, buy = PiratesGuiGlobals.InventoryAdd, listItemClass = StowawayItemGui)
        self.storeInventory.reparentTo(self.panel)
        self.storeInventory.setPos(0.029999999999999999, 0, 0.040000000000000001)
        self.myGoldTitle = DirectFrame(parent = self.panel, relief = None, text = PLocalizer.YourMoney, text_fg = PiratesGuiGlobals.TextFG2, text_align = TextNode.ALeft, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (0.0, 0.0), pos = (0.10000000000000001, 0, 0.155))
        self.myGold = DirectFrame(parent = self.myGoldTitle, relief = None, text = str(localAvatar.getMoney()), text_fg = PiratesGuiGlobals.TextFG2, text_align = TextNode.ARight, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (-0.055, 0.0), textMayChange = 1, image = StowawayGUI.CoinImage, image_scale = 0.14999999999999999, image_pos = (-0.025000000000000001, 0, 0.025000000000000001), pos = (0.40000000000000002, 0, 0))
        self.accept(PiratesGuiGlobals.InventoryBuyEvent, self.handleBuyItem)
        self.acceptOnce('escape', self.closePanel)

    
    def closePanel(self):
        messenger.send('exitStore')
        self.ignoreAll()

    
    def handleBuyItem(self, data, useCode):
        itemId = data[0]
        if not itemId:
            return None
        
        inventory = base.localAvatar.getInventory()
        if not inventory:
            return None
        
        if useCode == PiratesGuiGlobals.InventoryAdd:
            if inventory.getGoldInPocket() < EconomyGlobals.StowawayCost[itemId]:
                base.localAvatar.guiMgr.createWarning(PLocalizer.NotEnoughMoneyWarning, PiratesGuiGlobals.TextFG6)
                return None
            
            messenger.send('requestStowaway', [
                itemId])
        elif useCode == PiratesGuiGlobals.InventoryRemove:
            raise 
        


