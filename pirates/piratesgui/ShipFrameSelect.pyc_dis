# File: S (Python 2.4)

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.ShipFrame import ShipFrame
from pirates.piratesgui.GuiButton import GuiButton
from pirates.piratesgui.ShipSnapshot import ShipSnapshot

class ShipFrameSelect(ShipFrame):
    STOwn = 0
    STFriend = 1
    STBand = 2
    STGuild = 3
    STPublic = 4
    
    def __init__(self, parent, **kw):
        gui = loader.loadModel('models/gui/toplevel_gui')
        image = (gui.find('**/generic_button'), gui.find('**/generic_button_down'), gui.find('**/generic_button_over'), gui.find('**/generic_button_disabled'))
        optiondefs = (('relief', 0, None), ('frameSize', (0.0, 0.90000000000000002, 0.0, 0.41999999999999998), None), ('image', image[3], None), ('image_pos', (0.45000000000000001, 0.0, 0.20799999999999999), None), ('image_scale', (0.93999999999999995, 1, 1.1000000000000001), None), ('image_color', (0.80000000000000004, 0.80000000000000004, 0.80000000000000004, 1), None), ('frameColor', (1, 1, 1, 0.90000000000000002), None), ('snapShotPos', (-0.040000000000000001, 0, -0.080000000000000002), None), ('shipPos', VBase3(0.76000000000000001, 0, 0.14999999999999999), None), ('shipHpr', VBase3(-70, 6, 15), None), ('shipScale', VBase3(0.55000000000000004), None), ('shipType', ShipFrameSelect.STOwn, None), ('command', None, None), ('extraArgs', [], None))
        self.nameLabel = None
        self.classLabel = None
        self.typeLabel = None
        self.stateLabel = None
        self.button = None
        self.snapShot = None
        self.defineoptions(kw, optiondefs)
        ShipFrame.__init__(self, parent, **None)
        self.initialiseoptions(ShipFrameSelect)

    
    def destroy(self):
        self.nameLabel = None
        self.classLabel = None
        self.typeLabel = None
        self.stateLabel = None
        self.button = None
        self.snapShot = None
        ShipFrame.destroy(self)

    
    def createGui(self):
        ShipFrame.createGui(self)
        self.nameLabel = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, text = PLocalizer.makeHeadingString(self['shipName'], 2), text_align = TextNode.ALeft, text_scale = 0.050000000000000003, text_pos = (0.059999999999999998, 0.014999999999999999), text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 1, frameColor = PiratesGuiGlobals.ButtonColor1[3], frameSize = (self['frameSize'][0] + 0.040000000000000001, self['frameSize'][1] - 0.029999999999999999, -0.0, 0.050000000000000003), pos = (0, 0, self['frameSize'][3] - 0.089999999999999997))
        self.classLabel = DirectLabel(parent = self.nameLabel, relief = None, state = DGG.DISABLED, text = PLocalizer.makeHeadingString(PLocalizer.ShipClassNames.get(self['shipClass']), 1), text_font = PiratesGlobals.getInterfaceFont(), text_scale = PiratesGuiGlobals.TextScaleMed, text_align = TextNode.ALeft, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = (0, 0, 0, 1), textMayChange = 1, text_pos = (self.nameLabel['frameSize'][0] + 0.02, -0.029999999999999999))
        self.typeLabel = DirectLabel(parent = self.nameLabel, relief = None, state = DGG.DISABLED, text = '', text_pos = (0.59999999999999998, -0.029999999999999999), text_font = PiratesGlobals.getInterfaceFont(), text_scale = 0.032000000000000001, text_align = TextNode.ARight, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = (0, 0, 0, 1), textMayChange = 0)
        self.stateLabel = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, text = '', text_font = PiratesGlobals.getInterfaceFont(), text_align = TextNode.ALeft, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = (0, 0, 0, 1), text_pos = (0.19, 0.070000000000000007), text_scale = PiratesGuiGlobals.TextScaleLarge, textMayChange = 0)
        gui = loader.loadModel('models/gui/toplevel_gui')
        geomCheck = gui.find('**/generic_check')
        self.button = GuiButton(parent = self, pos = (0.73999999999999999, 0, 0.080000000000000002), text = PLocalizer.SelectShip, text_scale = PiratesGuiGlobals.TextScaleLarge, text_font = PiratesGlobals.getInterfaceFont(), text_pos = (0.035000000000000003, -0.014), geom = (geomCheck,) * 4, geom_pos = (-0.059999999999999998, 0, 0), geom_scale = 0.5, geom0_color = PiratesGuiGlobals.ButtonColor6[0], geom1_color = PiratesGuiGlobals.ButtonColor6[1], geom2_color = PiratesGuiGlobals.ButtonColor6[2], geom3_color = PiratesGuiGlobals.ButtonColor6[3], image3_color = (0.80000000000000004, 0.80000000000000004, 0.80000000000000004, 1), helpPos = (-0.40000000000000002, 0, 0.029999999999999999), helpDelay = 0.29999999999999999, command = self['command'], extraArgs = self['extraArgs'])

    
    def enableStatsOV(self, shipOV):
        self.snapShot = ShipSnapshot(self, shipOV, pos = self['snapShotPos'])
        typeStr = ''
        if shipOV.Hp <= 0:
            self.button['state'] = DGG.DISABLED
            stateStr = '\x1Ired\x1%s\x2' % PLocalizer.ShipSunk
            self['shipColorScale'] = VBase4(1, 0.40000000000000002, 0.40000000000000002, 1)
        elif shipOV.state in 'Off':
            self.button['state'] = DGG.NORMAL
            stateStr = PLocalizer.ShipInBottle
        else:
            self.button['state'] = DGG.NORMAL
            stateStr = PLocalizer.ShipAtSea
        self.typeLabel['text'] = '\x1smallCaps\x1(%s)\x2' % typeStr


