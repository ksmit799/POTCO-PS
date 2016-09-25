# File: B (Python 2.4)

from pandac.PandaModules import *
from direct.gui.DirectGui import DGG
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.piratesgui.GuiPanel import GuiPanel
from pirates.piratesgui.GuiButton import GuiButton
from pirates.piratesgui.DialogButton import DialogButton
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.CheckButton import CheckButton
from pirates.piratesbase import PiratesGlobals

class BoardingPermissionPanel(GuiPanel):
    
    def __init__(self, parent, *args, **kw):
        self.guiSetup = False
        optiondefs = (('parent', parent, None), ('pos', (-0.57999999999999996, 0, -0.089999999999999997), None), ('command', None, None), ('extraArgs', [], None), ('ownShip', 0, None))
        self.defineoptions(kw, optiondefs)
        GuiPanel.__init__(self, title = PLocalizer.BoardPermTitle, h = 0.80000000000000004, w = 0.5, titleSize = 1.5, showClose = False, **None)
        self.initialiseoptions(BoardingPermissionPanel)
        self.titleLabel['text_align'] = TextNode.ACenter
        self.titleLabel.setPos(0.23000000000000001, 0, 0.71999999999999997)
        self.setupGui()

    
    def destroy(self):
        self.button = None
        self.background = None
        self.friendsButton = None
        self.crewButton = None
        self.guildButton = None
        self.publicButton = None
        GuiPanel.destroy(self)

    
    def setupGui(self):
        self.destroyGui()
        if not self.guiSetup:
            self.button = DialogButton(parent = self, buttonStyle = DialogButton.NO, pos = (0.25, 0, 0.080000000000000002), text = PLocalizer.lClose, helpPos = (-0.40000000000000002, 0, 0.029999999999999999), helpDelay = 0.29999999999999999, command = self['command'], extraArgs = self['extraArgs'])
            self.background = BorderFrame(parent = self, pos = (0.050000000000000003, 0, 0.050000000000000003), frameSize = [
                0.0,
                0.40000000000000002,
                0.10000000000000001,
                0.59999999999999998], bgColorScale = VBase4(0, 0, 0, 0.75), bgTransparency = 1, flatten = 0)
            if self['ownShip']:
                state = DGG.NORMAL
            else:
                state = DGG.DISABLED
            ship = localAvatar.getShip()
            if ship:
                friendState = ship.getAllowFriendState()
                crewState = ship.getAllowCrewState()
                guildState = ship.getAllowGuildState()
                publicState = ship.getAllowPublicState()
            else:
                friendState = 0
                crewState = 0
                guildState = 0
                publicState = 0
            buttonOptions = {
                'parent': self.background,
                'state': state,
                'relief': None,
                'pos': (0.059999999999999998, 0, 0.53000000000000003),
                'scale': 0.29999999999999999,
                'text': PLocalizer.CrewBoardingAccessAllowFriends,
                'value': friendState,
                'text_pos': (0.16700000000000001, -0.059999999999999998, 0),
                'text0_fg': PiratesGuiGlobals.TextFG1,
                'text1_fg': PiratesGuiGlobals.TextFG1,
                'text2_fg': PiratesGuiGlobals.TextFG1,
                'text3_fg': PiratesGuiGlobals.TextFG9,
                'text_font': PiratesGlobals.getInterfaceFont(),
                'text_scale': 0.14999999999999999,
                'text_shadow': (0, 0, 0, 1),
                'text_align': TextNode.ALeft,
                'command': self.allowFriends }
            self.friendsButton = CheckButton(**None)
            buttonOptions['text'] = PLocalizer.CrewBoardingAccessAllowCrew
            buttonOptions['pos'] = (buttonOptions['pos'][0], buttonOptions['pos'][1], buttonOptions['pos'][2] - 0.12)
            buttonOptions['command'] = self.allowCrew
            buttonOptions['value'] = crewState
            self.crewButton = CheckButton(**None)
            buttonOptions['text'] = PLocalizer.CrewBoardingAccessAllowGuild
            buttonOptions['pos'] = (buttonOptions['pos'][0], buttonOptions['pos'][1], buttonOptions['pos'][2] - 0.12)
            buttonOptions['command'] = self.allowGuild
            buttonOptions['value'] = guildState
            self.guildButton = CheckButton(**None)
            buttonOptions['text'] = PLocalizer.CrewBoardingAccessAllowPublic
            buttonOptions['pos'] = (buttonOptions['pos'][0], buttonOptions['pos'][1], buttonOptions['pos'][2] - 0.12)
            buttonOptions['command'] = self.allowPublic
            buttonOptions['value'] = publicState
            self.publicButton = CheckButton(**None)
            self.guiSetup = True
        

    
    def destroyGui(self):
        if self.guiSetup:
            self.background.destroy()
            self.background = None
            self.friendsButton.destroy()
            self.friendsButton = None
            self.crewButton.destroy()
            self.crewButton = None
            self.guildButton.destroy()
            self.guildButton = None
            self.publicButton.destroy()
            self.publicButton = None
            self.button.destroy()
            self.button = None
            self.guiSetup = False
        

    
    def allowFriends(self, allow):
        if self['ownShip']:
            ship = localAvatar.getShip()
            if ship:
                ship.b_setAllowFriendState(allow)
            
        

    
    def allowCrew(self, allow):
        if self['ownShip']:
            ship = localAvatar.getShip()
            if ship:
                ship.b_setAllowCrewState(allow)
            
        

    
    def allowGuild(self, allow):
        if self['ownShip']:
            ship = localAvatar.getShip()
            if ship:
                ship.b_setAllowGuildState(allow)
            
        

    
    def allowPublic(self, allow):
        if self['ownShip']:
            ship = localAvatar.getShip()
            if ship:
                ship.b_setAllowPublicState(allow)
            
        

    
    def setAllowFriends(self, allow):
        self.friendsButton['value'] = allow

    
    def setAllowCrew(self, allow):
        self.crewButton['value'] = allow

    
    def setAllowGuild(self, allow):
        self.guildButton['value'] = allow

    
    def setAllowPublic(self, allow):
        self.publicButton['value'] = allow


