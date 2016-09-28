# File: C (Python 2.4)

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.BorderFrame import BorderFrame

class CannonDefenseHelpPanel(NodePath):
    
    def __init__(self, headerTxt, bodyTxt, wordWrap, width, height):
        NodePath.__init__(self, 'Panel')
        self.setTransparency(TransparencyAttrib.MAlpha)
        self.background = BorderFrame(parent = self, frameSize = (-0.02, width, 0, height), pos = (0, 0, -height + 0.059999999999999998), state = DGG.DISABLED, frameColor = (0, 0, 0, 0), bgTransparency = 1)
        self._CannonDefenseHelpPanel__createHeaderText(self, headerTxt)
        self._CannonDefenseHelpPanel__createArrow()
        if bodyTxt:
            self._CannonDefenseHelpPanel__createBodyText(self, bodyTxt, wordWrap)
        

    
    def _CannonDefenseHelpPanel__createArrow(self):
        self.arrow = loader.loadModel('models/gui/pir_m_gui_helpArrow')
        self.arrow.setTransparency(TransparencyAttrib.MAlpha)
        self.arrow.setDepthTest(False)
        self.arrow.reparentTo(self.background)

    
    def _CannonDefenseHelpPanel__createHeaderText(self, parent, text):
        header = TextNode('Header')
        header.setFont(PiratesGlobals.getInterfaceFont())
        header.setTextColor(PiratesGuiGlobals.TextFG1)
        header.setAlign(TextNode.ALeft)
        header.setText(text)
        headerNode = parent.attachNewNode(header)
        headerNode.setScale(0.065000000000000002)
        headerNode.setZ(0.0)
        headerNode.setDepthTest(False)

    
    def _CannonDefenseHelpPanel__createBodyText(self, parent, text, wordWrap):
        body = TextNode('Body')
        body.setFont(PiratesGlobals.getInterfaceFont())
        body.setTextColor(PiratesGuiGlobals.TextFG2)
        body.setAlign(TextNode.ALeft)
        body.setWordwrap(wordWrap)
        body.setText(text)
        bodyNode = parent.attachNewNode(body)
        bodyNode.setScale(0.050000000000000003)
        bodyNode.setZ(-0.070000000000000007)
        bodyNode.setDepthTest(False)


