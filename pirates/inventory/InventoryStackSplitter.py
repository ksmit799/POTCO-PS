# File: I (Python 2.4)

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.inventory.InventoryUIGlobals import *

class InventoryStackSplitter(BorderFrame):
    
    def __init__(self, cell, manager):
        self.sizeX = 0.80000000000000004
        self.sizeZ = 0.59999999999999998
        textScale = PiratesGuiGlobals.TextScaleTitleSmall
        optiondefs = (('state', DGG.DISABLED, None), ('frameSize', (-0.0 * self.sizeX, 1.0 * self.sizeX, -0.0 * self.sizeZ, 1.0 * self.sizeZ), None), ('text', PLocalizer.InventorySplitterTitle, None), ('text_align', TextNode.ACenter, None), ('text_font', PiratesGlobals.getPirateBoldOutlineFont(), None), ('text_fg', (1, 1, 1, 1), None), ('text_shadow', PiratesGuiGlobals.TextShadow, None), ('textMayChange', 1, None), ('text_scale', textScale, None), ('text_pos', (self.sizeX * 0.5, self.sizeZ - textScale), None))
        self.defineoptions({ }, optiondefs)
        BorderFrame.__init__(self, parent = NodePath())
        self.initialiseoptions(InventoryStackSplitter)
        self.fromCell = cell
        self.manager = manager
        self.setup()

    
    def setup(self):
        self.setBin('gui-fixed', 1)
        self.itemLabel = DirectLabel(parent = self, relief = None, text = '%s' % self.fromCell.inventoryItem.getName(), text_font = PiratesGlobals.getPirateBoldOutlineFont(), text_align = TextNode.ACenter, text_scale = PiratesGuiGlobals.TextScaleLarge, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, image = self.fromCell.inventoryItem['image'], image_scale = self.fromCell.inventoryItem['image_scale'], text_pos = (0.0, 0.066000000000000003), pos = (self.sizeX * 0.5, 0.0, self.sizeZ * 0.65000000000000002))
        Gui = loader.loadModel('models/gui/toplevel_gui')
        buttonImage = (Gui.find('**/generic_button'), Gui.find('**/generic_button_down'), Gui.find('**/generic_button_over'), Gui.find('**/generic_button_disabled'))
        self.confirmButton = DirectButton(parent = self, relief = None, image = buttonImage, image_scale = (0.22, 1.0, 0.22), image0_color = VBase4(0.65000000000000002, 0.65000000000000002, 0.65000000000000002, 1), image1_color = VBase4(0.40000000000000002, 0.40000000000000002, 0.40000000000000002, 1), image2_color = VBase4(0.90000000000000002, 0.90000000000000002, 0.90000000000000002, 1), image3_color = VBase4(0.40999999999999998, 0.40000000000000002, 0.40000000000000002, 1), text = PLocalizer.InventorySplitterConfirm, text_font = PiratesGlobals.getPirateBoldOutlineFont(), text_align = TextNode.ACenter, text_pos = (0, -0.01), text_scale = PiratesGuiGlobals.TextScaleLarge, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, pos = (self.sizeX * 0.5, 0, 0.050000000000000003), command = self.manager.closeSplitter)
        self.allButton = DirectButton(parent = self, relief = None, image = buttonImage, image_scale = (0.13, 1.0, 0.17999999999999999), image0_color = VBase4(0.65000000000000002, 0.65000000000000002, 0.65000000000000002, 1), image1_color = VBase4(0.40000000000000002, 0.40000000000000002, 0.40000000000000002, 1), image2_color = VBase4(0.90000000000000002, 0.90000000000000002, 0.90000000000000002, 1), image3_color = VBase4(0.40999999999999998, 0.40000000000000002, 0.40000000000000002, 1), text = PLocalizer.InventorySplitterAll, text_font = PiratesGlobals.getPirateBoldOutlineFont(), text_align = TextNode.ACenter, text_pos = (0, -0.01), text_scale = PiratesGuiGlobals.TextScaleLarge, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, pos = (self.sizeX * 0.75, 0, self.sizeZ * 0.25), command = self.setAll)
        self.noneButton = DirectButton(parent = self, relief = None, image = buttonImage, image_scale = (0.13, 1.0, 0.17999999999999999), image0_color = VBase4(0.65000000000000002, 0.65000000000000002, 0.65000000000000002, 1), image1_color = VBase4(0.40000000000000002, 0.40000000000000002, 0.40000000000000002, 1), image2_color = VBase4(0.90000000000000002, 0.90000000000000002, 0.90000000000000002, 1), image3_color = VBase4(0.40999999999999998, 0.40000000000000002, 0.40000000000000002, 1), text = PLocalizer.InventorySplitterNone, text_font = PiratesGlobals.getPirateBoldOutlineFont(), text_align = TextNode.ACenter, text_pos = (0, -0.01), text_scale = PiratesGuiGlobals.TextScaleLarge, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, pos = (self.sizeX * 0.25, 0, self.sizeZ * 0.25), command = self.setNone)
        generic_x = Gui.find('**/generic_x')
        generic_box = Gui.find('**/generic_box')
        generic_box_over = Gui.find('**/generic_box_over')
        self.closeButton = DirectButton(parent = self, relief = None, pos = (self.sizeX - 0.035000000000000003, 0, self.sizeZ - 0.035000000000000003), scale = 0.28000000000000003, geom = generic_x, image = (generic_box, generic_box, generic_box_over, generic_box), image_scale = 0.69999999999999996, text = '', textMayChange = 1, command = self.manager.closeSplitter)
        charGui = loader.loadModel('models/gui/char_gui')
        incImage = (charGui.find('**/chargui_forward'), charGui.find('**/chargui_forward_down'), charGui.find('**/chargui_forward_over'))
        decImage = (charGui.find('**/chargui_back'), charGui.find('**/chargui_back_down'), charGui.find('**/chargui_back_over'))
        amount = self.fromCell.inventoryItem.getAmount()
        self.slider = DirectSlider(parent = self, relief = None, command = self.updateSlider, image = charGui.find('**/chargui_slider_small'), image_scale = (2.1499999999999999, 2.1499999999999999, 1.5), thumb_relief = None, thumb_image = (charGui.find('**/chargui_slider_node'), charGui.find('**/chargui_slider_node_down'), charGui.find('**/chargui_slider_node_over')), pos = (self.sizeX * 0.5, 0.0, self.sizeZ * 0.38), text_align = TextNode.ACenter, text_scale = (0.10000000000000001, 0.10000000000000001), text_pos = (0.0, 0.10000000000000001), text_fg = PiratesGuiGlobals.TextFG1, scale = 0.38, pageSize = 1.0, scrollSize = 1.0, text = 'default', value = 0, range = (0, amount))
        self.incButton = DirectButton(parent = self, relief = None, pos = (self.sizeX * 0.55000000000000004, 0, self.sizeZ * 0.25), image = incImage, image_scale = 0.34999999999999998, text = '', textMayChange = 1)
        self.decButton = DirectButton(parent = self, relief = None, pos = (self.sizeX * 0.45000000000000001, 0, self.sizeZ * 0.25), image = decImage, image_scale = 0.34999999999999998, text = '', textMayChange = 1)
        self.slider.guiItem.setLeftButton(self.decButton.guiItem)
        self.slider.guiItem.setRightButton(self.incButton.guiItem)

    
    def updateSlider(self):
        amount = self.fromCell.inventoryItem.getAmount()
        amountSplit = int(self.slider['value'])
        self.slider['text'] = '%s/%s' % (amountSplit, amount)

    
    def setAll(self):
        self.slider['value'] = self.slider['range'][1]

    
    def setNone(self):
        self.slider['value'] = self.slider['range'][0]


