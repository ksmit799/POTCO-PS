# File: I (Python 2.4)

from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.inventory import InventoryUIItem
from pirates.inventory import InventoryUIContainer
from pirates.inventory.InventoryUIGlobals import *

class InventoryUIBagbar(DirectFrame):
    
    def __init__(self, manager, cellSizeX = 0.10000000000000001, cellSizeZ = 0.10000000000000001):
        self.cellSizeX = cellSizeX
        self.cellSizeZ = cellSizeZ
        self.sizeX = cellSizeX
        self.sizeZ = cellSizeZ
        self.manager = manager
        optiondefs = (('relief', DGG.FLAT, None), ('state', DGG.NORMAL, self.setState), ('frameSize', (-0.0, self.cellSizeX, -0.0, self.cellSizeZ), None), ('frameColor', (0.0, 0.0, 0.0, 1.0), None))
        self.defineoptions({ }, optiondefs)
        DirectFrame.__init__(self, parent = NodePath())
        self.initialiseoptions(InventoryUIBagbar)
        self.bagButtonList = []
        self.containerList = []
        self.lastOpened = None

    
    def destroy(self):
        self.containerList = []
        for bag in self.bagButtonList:
            bag.unbind(DGG.WITHIN)
            bag.unbind(DGG.WITHOUT)
            bag.bar = None
            bag.destroy()
        
        self.bagButtonList = []
        DirectFrame.destroy(self)

    
    def setup(self):
        gui = loader.loadModel('models/gui/toplevel_gui')
        chestButtonClosed = gui.find('**/treasure_chest_closed_over')
        chestButtonOpen = gui.find('**/treasure_chest_open_over')
        textScale = 0.040000000000000001
        bagCount = 0
        for container in self.containerList:
            bagButton = DirectButton(parent = self, relief = DGG.SUNKEN, borderWidth = (self.cellSizeX * 0.050000000000000003, self.cellSizeX * 0.050000000000000003), frameSize = (-(self.cellSizeX) * 0.45000000000000001, self.cellSizeX * 0.45000000000000001, -(self.cellSizeZ) * 0.45000000000000001, self.cellSizeZ * 0.45000000000000001), frameColor = CELL_COLOR_NORMAL, textMayChange = 1, geom = chestButtonClosed, geom_scale = 0.80000000000000004 * self.cellSizeX, text = '', text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_scale = textScale, text_pos = (0.0, self.cellSizeZ * -0.27000000000000002), pos = (self.cellSizeX * (float(bagCount) + 0.5), 0.0, self.cellSizeZ * 0.5), command = self.bagClicked, extraArgs = [
                None])
            bagButton.bind(DGG.WITHIN, self.manager.setWithinBag, extraArgs = [
                bagButton,
                0])
            bagButton.bind(DGG.WITHOUT, self.manager.setWithinBag, extraArgs = [
                bagButton,
                1])
            bagButton['extraArgs'] = [
                bagButton]
            bagButton.container = container
            bagButton.bar = self
            bagCount += 1
            self.bagButtonList.append(bagButton)
        
        self['frameSize'] = (-0.0, self.cellSizeX * bagCount, -0.0, self.cellSizeZ)
        self.sizeX = bagCount * self.cellSizeX

    
    def cleanup(self):
        for bag in self.bagButtonList:
            bag.destroy()
        
        self.bagButtonList = []

    
    def addContainer(self, container):
        container.hide()
        self.containerList.append(container)
        self.cleanup()
        self.setup()

    
    def bagClicked(self, bagButton):
        if self.manager.locked:
            return None
        
        self.openBag(bagButton)

    
    def openBag(self, bagButton):
        print 'BagBar Open Bag'
        gui = loader.loadModel('models/gui/toplevel_gui')
        chestButtonClosed = gui.find('**/treasure_chest_closed_over')
        chestButtonOpen = gui.find('**/treasure_chest_open_over')
        if self.lastOpened:
            self.lastOpened['geom'] = chestButtonClosed
        
        for container in self.containerList:
            container.hide()
        
        bagButton['geom'] = chestButtonOpen
        bagButton.container.takeOut()
        bagButton.container.show()
        self.lastOpened = bagButton

    
    def openDefault(self):
        if not self.lastOpened:
            self.openBag(self.bagButtonList[0])
        


