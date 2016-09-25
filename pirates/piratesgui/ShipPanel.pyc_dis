# File: S (Python 2.4)

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.ShipFrameBottle import ShipFrameBottle
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesTimer
from pirates.ship import ShipUpgradeGlobals
from pirates.battle import WeaponGlobals
from pirates.uberdog.UberDogGlobals import InventoryType

class ShipPanel(DirectFrame):
    Width = PiratesGuiGlobals.ShipPanelWidth
    Height = PiratesGuiGlobals.ShipPanelHeight
    
    def __init__(self, shipPage, shipId, **kwargs):
        self.shipPage = shipPage
        self.emptyBottle = True
        self.setShipId(shipId)
        self.timer = None
        self.lBroadsideLimit = 0
        self.rBroadsideLimit = 0
        kwargs.setdefault('relief', None)
        kwargs.setdefault('frameSize', (0, self.Width, 0, self.Height))
        DirectFrame.__init__(self, **None)
        self.initialiseoptions(ShipPanel)
        gui = loader.loadModel('models/gui/toplevel_gui')
        inventoryGui = loader.loadModel('models/gui/gui_icons_inventory')
        chestIcon = inventoryGui.find('**/pir_t_ico_trs_chest_01*')
        cannonIcon = gui.find('**/topgui_icon_ship_cannon_single')
        skillIcons = loader.loadModel('models/textureCards/skillIcons')
        broadsideId = InventoryType.CannonRoundShot
        ammoIconName = WeaponGlobals.getSkillIcon(broadsideId)
        broadsideIcon = skillIcons.find('**/%s' % ammoIconName)
        crewIcon = (gui.find('**/pir_t_gui_gen_friends_pirates'),)
        self.bottleFrame = ShipFrameBottle(parent = self, shipId = shipId, relief = None, state = DGG.DISABLED, pos = (0.074999999999999997, 0, 0.75), scale = 0.83499999999999996)
        gui = loader.loadModel('models/gui/gui_ship_window')
        bottleImage = gui.find('**/ship_bottle')
        self.shipBottle = DirectLabel(parent = self.bottleFrame, relief = None, state = DGG.DISABLED, geom = bottleImage, geom_scale = 0.29999999999999999, geom_pos = (0, 0, 0), pos = (0.5, 0, -0.0))
        self.nameLabel = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, text = PLocalizer.makeHeadingString(PLocalizer.EmptyBottle, 2), text_fg = PiratesGuiGlobals.TextFG1, text_scale = PiratesGuiGlobals.TextScaleTitleSmall, text_align = TextNode.ACenter, text_shadow = (0, 0, 0, 1), text_wordwrap = 30, textMayChange = 1, text_font = PiratesGlobals.getPirateFont(), pos = (0.55000000000000004, 0, 1.22))
        self.classLabel = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, text = PLocalizer.makeHeadingString(PLocalizer.EmptyBottleDesc, 1), text_scale = PiratesGuiGlobals.TextScaleMed, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = (0, 0, 0, 1), text_wordwrap = 30, textMayChange = 1, text_font = PiratesGlobals.getInterfaceFont(), pos = (0.55000000000000004, 0, 1.1799999999999999))
        self.timer = PiratesTimer.PiratesTimer(showMinutes = True, mode = None, titleText = '', titleFg = '', infoText = '', cancelText = '', cancelCallback = None)
        self.timer.setFontColor(PiratesGuiGlobals.TextFG2)
        self.timer.reparentTo(self)
        self.timer.setPos(0.45000000000000001, 0, 0.93999999999999995)
        self.timer.setScale(0.59999999999999998)
        self.timer.stash()
        self.hpMeter = DirectWaitBar(parent = self, relief = DGG.RAISED, state = DGG.DISABLED, range = 1, value = 0, frameColor = (0.0, 0.0, 0.0, 0.0), barColor = (0.10000000000000001, 0.69999999999999996, 0.10000000000000001, 1), frameSize = (0, 0.31, 0, 0.018599999999999998), text = '', text_align = TextNode.ARight, text_scale = 0.029999999999999999, text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1), text_pos = (0.29999999999999999, 0.029999999999999999), pos = (0.55000000000000004, 0.0, 0.45000000000000001), scale = 1.2)
        hpLabel = DirectLabel(parent = self.hpMeter, relief = None, state = DGG.DISABLED, text = PLocalizer.HP, text_scale = 0.029999999999999999, text_align = TextNode.ALeft, text_pos = (0.014999999999999999, 0.029999999999999999), text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1))
        self.speedMeter = DirectWaitBar(parent = self, relief = DGG.RAISED, state = DGG.DISABLED, range = 1, value = 0, frameColor = (0.0, 0.0, 0.0, 0.0), barColor = (0.69999999999999996, 0.69999999999999996, 0.10000000000000001, 1), frameSize = (0, 0.31, 0, 0.018599999999999998), text = '', text_align = TextNode.ARight, text_scale = 0.029999999999999999, text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1), text_pos = (0.29999999999999999, 0.029999999999999999), pos = (0.55000000000000004, 0.0, 0.34999999999999998), scale = 1.2)
        speedLabel = DirectLabel(parent = self.speedMeter, relief = None, state = DGG.DISABLED, text = PLocalizer.Sails, text_scale = 0.029999999999999999, text_align = TextNode.ALeft, text_pos = (0.014999999999999999, 0.029999999999999999), text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1))
        self.customHullLabel = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, geom = chestIcon, geom_scale = 0.14999999999999999, geom_pos = (0, 0, 0), text = '', text_scale = 0.044999999999999998, text_align = TextNode.ACenter, text_pos = (0, -0.070000000000000007), text_fg = PiratesGuiGlobals.TextFG1, text_shadow = (0, 0, 0, 1), textMayChange = 1, text_font = PiratesGlobals.getInterfaceOutlineFont(), pos = (0.34999999999999998, 0, 0.68000000000000005))
        self.customHullLabel.hide()
        self.customRiggingLabel = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, geom = chestIcon, geom_scale = 0.14999999999999999, geom_pos = (0, 0, 0), text = '', text_scale = 0.044999999999999998, text_align = TextNode.ACenter, text_pos = (0, -0.070000000000000007), text_fg = PiratesGuiGlobals.TextFG1, text_shadow = (0, 0, 0, 1), textMayChange = 1, text_font = PiratesGlobals.getInterfaceOutlineFont(), pos = (0.75, 0, 0.68000000000000005))
        self.customRiggingLabel.hide()
        textPos = (0.0, -0.16)
        self.plunderLimit = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, geom = chestIcon, geom_scale = 0.10000000000000001, geom_pos = (0, 0, -0.050000000000000003), text = '', text_scale = 0.044999999999999998, text_align = TextNode.ACenter, text_pos = textPos, text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1), textMayChange = 1, text_font = PiratesGlobals.getInterfaceOutlineFont(), pos = (0.20000000000000001, 0, 0.20000000000000001))
        plunderLabel = DirectLabel(parent = self.plunderLimit, relief = None, state = DGG.DISABLED, text = PLocalizer.Cargo, text_scale = 0.035999999999999997, text_align = TextNode.ACenter, text_pos = (0, 0.040000000000000001), text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1))
        self.cannonLimit = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, geom = cannonIcon, geom_scale = 0.45000000000000001, geom_pos = (0, 0, -0.050000000000000003), text = '', text_scale = 0.044999999999999998, text_align = TextNode.ACenter, text_pos = textPos, text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1), textMayChange = 1, text_font = PiratesGlobals.getInterfaceOutlineFont(), pos = (0.37, 0, 0.20000000000000001))
        cannonLabel = DirectLabel(parent = self.cannonLimit, relief = None, state = DGG.DISABLED, text = PLocalizer.Cannon, text_scale = 0.035999999999999997, text_align = TextNode.ACenter, text_pos = (0, 0.040000000000000001), text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1))
        self.cannonLabel = cannonLabel
        self.broadsideLimit = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, geom = broadsideIcon, geom_scale = 0.14999999999999999, geom_pos = (0, 0, -0.050000000000000003), text = '', text_scale = 0.044999999999999998, text_align = TextNode.ACenter, text_pos = textPos, text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1), textMayChange = 1, text_font = PiratesGlobals.getInterfaceOutlineFont(), pos = (0.81000000000000005, 0, 0.20000000000000001))
        broadsideLabel = DirectLabel(parent = self.broadsideLimit, relief = None, state = DGG.DISABLED, text = PLocalizer.Broadsides, text_scale = 0.035999999999999997, text_align = TextNode.ACenter, text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1), text_pos = (0.0, 0.040000000000000001))
        self.broadsideLabel = broadsideLabel
        self.crewLimit = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, geom = crewIcon, geom_scale = 0.40000000000000002, geom_pos = (0, 0, 0.10000000000000001), text = '', text_scale = 0.044999999999999998, text_align = TextNode.ACenter, text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1), textMayChange = 1, text_font = PiratesGlobals.getInterfaceOutlineFont(), pos = (0.56000000000000005, 0, 0.040000000000000001))
        crewLabel = DirectLabel(parent = self.crewLimit, relief = None, state = DGG.DISABLED, text = PLocalizer.Crew, text_scale = 0.035999999999999997, text_align = TextNode.ACenter, text_pos = (0.0, 0.20000000000000001), text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1))
        self.crewLabel = crewLabel
        shipOV = base.cr.getOwnerView(self.shipId)
        if shipOV:
            self.setShipName(shipOV.name)
            self.setShipClass(shipOV.shipClass)
            self.setShipHp(shipOV.Hp, shipOV.maxHp)
            self.setShipSp(shipOV.Sp, shipOV.maxSp)
            self.setShipCrew(shipOV.crew, shipOV.maxCrew)
            self.setShipCargo([], shipOV.maxCargo)
            if hasattr(shipOV, 'cannonConfig'):
                self.setShipMaxCannons(shipOV.cannonConfig)
                self.setShipMaxBroadside(shipOV.lBroadsideConfig, shipOV.rBroadsideConfig)
            
            self.updateIcons()
        
        if self.emptyBottle:
            self.hpMeter.hide()
            self.speedMeter.hide()
            self.plunderLimit.hide()
            self.cannonLimit.hide()
            self.broadsideLimit.hide()
            self.crewLimit.hide()
        
        self.accept('setName-%s' % self.shipId, self.setShipName)
        self.accept('setShipClass-%s' % self.shipId, self.setShipClass)
        self.accept('setShipHp-%s' % self.shipId, self.setShipHp)
        self.accept('setShipSp-%s' % self.shipId, self.setShipSp)
        self.accept('setShipCargo-%s' % self.shipId, self.setShipCargo)
        self.accept('setShipCrew-%s' % self.shipId, self.setShipCrew)
        self.accept('setShipTimer-%s' % self.shipId, self.setShipTimer)
        self.accept('setHullCannonConfig-%s' % self.shipId, self.setShipMaxCannons)
        self.accept('setHullLeftBroadsideConfig-%s' % self.shipId, self.setShipMaxLeftBroadside)
        self.accept('setHullRightBroadsideConfig-%s' % self.shipId, self.setShipMaxRightBroadside)
        self.accept('ShipChanged-%s' % self.shipId, self.handleShipChanged)
        if base.config.GetBool('want-deploy-button', 0):
            pass
        1

    
    def handleShipChanged(self, task = None):
        self.updateIcons()

    
    def updateIcons(self):
        shipOV = base.cr.getOwnerView(self.shipId)
        if shipOV:
            shipHullInfo = ShipUpgradeGlobals.HULL_TYPES.get(shipOV.customHull)
            shipRiggingInfo = ShipUpgradeGlobals.RIGGING_TYPES.get(shipOV.customRigging)
            UpgradeIcons = loader.loadModel('models/textureCards/shipUpgradeIcons', okMissing = True)
            skillIcons = loader.loadModel('models/textureCards/skillIcons')
            if shipHullInfo and shipHullInfo['Icon']:
                if UpgradeIcons:
                    hullImage = UpgradeIcons.find('**/%s' % shipHullInfo['Icon'])
                    self.customHullLabel['geom'] = hullImage
                
                self.customHullLabel['text'] = shipHullInfo['Name'] + '\n' + PLocalizer.HullLabel
                self.customHullLabel.show()
                self.setShipHp(shipOV.Hp, shipOV.maxHp)
                self.setShipCargo(shipOV.cargo, shipOV.maxCargo)
                if shipHullInfo['BroadsideType']:
                    broadsideId = shipHullInfo['BroadsideType']
                    ammoIconName = WeaponGlobals.getSkillIcon(broadsideId)
                    broadsideIcon = skillIcons.find('**/%s' % ammoIconName)
                    self.broadsideLimit['geom'] = broadsideIcon
                    self.broadsideLimit['geom_scale'] = 0.14999999999999999
                else:
                    broadsideId = InventoryType.CannonRoundShot
                    ammoIconName = WeaponGlobals.getSkillIcon(broadsideId)
                    broadsideIcon = skillIcons.find('**/%s' % ammoIconName)
                    self.broadsideLimit['geom'] = broadsideIcon
                    self.broadsideLimit['geom_scale'] = 0.14999999999999999
            
            if shipRiggingInfo and shipRiggingInfo['Icon']:
                riggingImage = skillIcons.find('**/%s' % shipRiggingInfo['Icon'])
                self.customRiggingLabel['geom'] = riggingImage
                self.customRiggingLabel['text'] = shipRiggingInfo['Name'] + '\n' + PLocalizer.RiggingLabel
                self.customRiggingLabel.show()
            
        

    
    def destroy(self):
        self.hpMeter = None
        self.speedMeter = None
        self.plunderLimit = None
        self.cannonLimit = None
        self.broadsideLimit = None
        self.crewLimit = None
        self.ignoreAll()
        self.hullCards = []
        DirectFrame.destroy(self)

    
    def setShipId(self, shipId):
        self.shipId = shipId
        if shipId <= 2:
            self.emptyBottle = True
        else:
            self.emptyBottle = False

    
    def getShipId(self):
        return self.shipId

    
    def setShipName(self, name, team = None):
        self.nameLabel['text'] = PLocalizer.makeHeadingString(name, 2)

    
    def setShipClass(self, shipClass):
        self.classLabel['text'] = PLocalizer.makeHeadingString(PLocalizer.ShipClassNames.get(shipClass), 1)

    
    def setShipHp(self, hp, maxHp):
        self.hpMeter['text'] = '%d/%d' % (hp, maxHp)
        self.hpMeter['range'] = maxHp
        self.hpMeter['value'] = hp

    
    def setShipSp(self, sp, maxSp):
        self.speedMeter['text'] = '%d/%d' % (sp, maxSp)
        self.speedMeter['range'] = maxSp
        self.speedMeter['value'] = sp

    
    def setShipPlunderLimit(self, current, limit):
        self.plunderLimit['text'] = str(limit)

    
    def setShipCrew(self, crewArray, maxCrewCount):
        crewCount = len(crewArray)
        self.crewLimit['text'] = '%d/%d' % (crewCount, maxCrewCount)

    
    def setShipCargo(self, cargo, maxCargo):
        self.plunderLimit['text'] = str(maxCargo)

    
    def setShipTimer(self, timeLeft):
        if timeLeft:
            self.timer.unstash()
            self.timer.countdown(timeLeft)
        else:
            self.timer.timerExpired()
            self.timer.stop()
            self.timer.stash()

    
    def setShipMaxCannons(self, cannonConfig):
        self.cannonLimit['text'] = str(len(cannonConfig) - cannonConfig.count(0))

    
    def setShipMaxLeftBroadside(self, broadsideConfig):
        self.lBroadsideLimit = len(broadsideConfig)
        self.broadsideLeftLimit['text'] = '%d' % (self.lBroadsideLimit - broadsideConfig.count(0))

    
    def setShipMaxRightBroadside(self, broadsideConfig):
        self.rBroadsideLimit = len(broadsideConfig)

    
    def setShipMaxBroadside(self, broadsideConfigL, broadsideConfigR):
        self.lBroadsideLimit = len(broadsideConfigL)
        self.rBroadsideLimit = len(broadsideConfigR)
        numBS = (self.lBroadsideLimit - broadsideConfigL.count(0)) + (self.rBroadsideLimit - broadsideConfigR.count(0))
        self.broadsideLimit['text'] = '%d' % numBS


