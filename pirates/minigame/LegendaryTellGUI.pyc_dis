# File: L (Python 2.4)

import math
from pandac.PandaModules import NodePath
from panda3d.core import TextNode
from pirates.piratesgui.GuiButton import GuiButton
from direct.gui.DirectGui import *
from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import TransparencyAttrib
import FishingGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesgui import PiratesGuiGlobals
from pirates.world.LocationConstants import LocationIds
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import CollectionMap
from pirates.piratesgui import GuiPanel

class LegendaryTellGUI(GuiPanel.GuiPanel):
    
    def __init__(self, w, h, locationId = LocationIds.PORT_ROYAL_ISLAND):
        GuiPanel.GuiPanel.__init__(self, '', w, h, True)
        self.card = loader.loadModel('models/gui/pir_m_gui_fsh_legendaryScreen')
        self.storyImageCard = loader.loadModel('models/minigames/pir_m_gam_fsh_legendaryGui')
        self.UICompoments = { }
        self.setPos(-1.1499999999999999, 0.0, -0.59999999999999998)
        self['geom'] = self.card.find('**/background')
        self['geom_pos'] = (0.57999999999999996, 0.0, 0.63)
        self['geom_scale'] = (0.94999999999999996, 0.0, 0.84999999999999998)
        self.coinImage = OnscreenImage(parent = self, image = self.card.find('**/coin'), scale = 0.90000000000000002, hpr = (0, 0, 0), pos = (0.84999999999999998, 0, 0.84999999999999998))
        self.titleTextNode = TextNode('legendPanelTitle')
        self.titleTextNode.setText(PLocalizer.LegendSelectionGui['panelTitle'])
        self.titleTextNode.setFont(PiratesGlobals.getPirateFont())
        self.titleTextNode.setTextColor(0.87, 0.81999999999999995, 0.54000000000000004, 0.90000000000000002)
        self.titleTextNodePath = NodePath(self.titleTextNode)
        self.titleTextNodePath.setPos(0.65000000000000002, 0.0, 1.2)
        self.titleTextNodePath.setScale(0.070000000000000007)
        self.titleTextNodePath.reparentTo(self)
        self.introTextNode = TextNode('legendaryIntroTextNode')
        self.introTextNode.setText(PLocalizer.LegendSelectionGui['legendIntro'])
        self.introTextNode.setWordwrap(14.0)
        self.introTextNode.setTextColor(0.90000000000000002, 0.80000000000000004, 0.46999999999999997, 0.90000000000000002)
        self.introTextNodePath = NodePath(self.introTextNode)
        self.introTextNodePath.setPos(0.59999999999999998, 0.0, 0.5)
        self.introTextNodePath.setScale(0.042000000000000003)
        self.introTextNodePath.reparentTo(self)
        self.buttonRootNode = NodePath('button_RootNode')
        self.buttonRootNode.reparentTo(self)
        self.buttonRootNode.setPos(-0.080000000000000002, 0.0, 1.1499999999999999)
        self.iconCard = loader.loadModel('models/gui/treasure_gui')
        self.legendSelectionButtons = { }
        btnGeom = (self.card.find('**/fishButton/idle'), self.card.find('**/fishButton/idle'), self.card.find('**/fishButton/over'))
        for i in range(len(FishingGlobals.legendaryFishData)):
            fishName = FishingGlobals.legendaryFishData[i]['name']
            fishId = FishingGlobals.legendaryFishData[i]['id']
            assetsKey = CollectionMap.Assets[fishId]
            pos_x = 0.29999999999999999
            pos_z = 0.0 - i * 0.25
            button = GuiButton(parent = self.buttonRootNode, text = (fishName, fishName, fishName, fishName), text0_fg = (0.42999999999999999, 0.28999999999999998, 0.19, 1.0), text1_fg = (0.42999999999999999, 0.28999999999999998, 0.19, 1.0), text2_fg = (0.42999999999999999, 0.28999999999999998, 0.19, 1.0), text3_fg = (0.42999999999999999, 0.28999999999999998, 0.19, 1.0), text_scale = 0.035000000000000003, text_pos = (0.037999999999999999, -0.0050000000000000001), pos = (pos_x, 0, pos_z), hpr = (0, 0, 0), scale = 1.5, image = btnGeom, image_pos = (0, 0, 0), image_scale = 0.69999999999999996, sortOrder = 2, command = self.buttonClickHandle, extraArgs = [
                fishId,
                assetsKey,
                locationId])
            button.icon = OnscreenImage(parent = button, image = self.iconCard.find('**/%s*' % assetsKey), scale = 0.34999999999999998, hpr = (0, 0, 0), pos = (-0.123, 0, 0.0050000000000000001))
        
        self.legendPanel = GuiPanel.GuiPanel('', 2.6000000000000001, 1.8999999999999999, True)
        self.legendPanel.setPos(-1.3, 0.0, -0.94999999999999996)
        self.legendPanel.background = OnscreenImage(parent = self.legendPanel, scale = (2.3999999999999999, 0, 1.8), image = self.storyImageCard.find('**/pir_t_gui_fsh_posterBackground'), hpr = (0, 0, 0), pos = (1.3, 0, 0.94999999999999996))
        self.legendPanel.storyImage = OnscreenImage(parent = self.legendPanel, scale = 1, image = self.card.find('**/coin'), hpr = (0, 0, 0), pos = (1.8, 0, 1))
        self.storyTextNode = TextNode('storyTextNode')
        self.storyTextNode.setText('')
        self.storyTextNode.setWordwrap(19.0)
        self.storyTextNode.setTextColor(0.23000000000000001, 0.089999999999999997, 0.029999999999999999, 1.0)
        self.storyTextNodePath = NodePath(self.storyTextNode)
        self.storyTextNodePath.setPos(0.33000000000000002, 0.0, 1.6699999999999999)
        self.storyTextNodePath.setScale(0.050000000000000003)
        self.storyTextNodePath.reparentTo(self.legendPanel)
        self.callBack = None
        self.legendPanel.hide()

    
    def destroy(self):
        self.legendPanel.destroy()
        GuiPanel.GuiPanel.destroy(self)

    
    def buttonClickHandle(self, fishId, imgKey, locationId):
        result = imgKey.split('_')
        temp = str(result[1]).capitalize()
        imgName = 'pir_t_gui_fsh_poster%s' % temp
        self.legendPanel.storyImage.setImage(self.storyImageCard.find('**/%s*' % imgName))
        self.storyTextNode.setText(PLocalizer.LegendSelectionGui['shortStory'][fishId][locationId])
        self.legendPanel.show()

    
    def setCallBack(self, callback):
        self.callBack = callback

    
    def closePanel(self):
        GuiPanel.GuiPanel.closePanel(self)
        if self.callBack is not None:
            self.callBack()
        


