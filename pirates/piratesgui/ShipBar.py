# File: S (Python 2.4)

from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.fsm.FSM import FSM
from direct.showbase.PythonUtil import Functor
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.TabBar import TopTab, TabBar

class ShipTab(TopTab):
    
    def __init__(self, tabBar, name, **kw):
        optiondefs = (('modelName', 'general_frame_c', None), ('frameSize', (0, 0.20499999999999999, 0.0, 0.10000000000000001), None), ('borderScale', 0.13500000000000001, None), ('bgBuffer', 0.14000000000000001, None), ('showBackground', True, None), ('bgColorScale', VBase4(0, 0, 0, 1), None), ('flatten', 0, None), ('label', '', None), ('textMayChange', 0, None), ('textpos', (0.10000000000000001, 0.025000000000000001, 0), None))
        self.defineoptions(kw, optiondefs)
        TopTab.__init__(self, tabBar, name, **None)
        self.initialiseoptions(ShipTab)
        self.guiComponents['background'].setTransparency(0, 1)
        self.label = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, text = name, text_pos = self['textpos'], text_scale = 0.050000000000000003, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_font = PiratesGlobals.getInterfaceFont(), textMayChange = 1)

    
    def setTextBright(self, bright):
        if bright:
            self.label['text_fg'] = PiratesGuiGlobals.TextFG1
        else:
            self.label['text_fg'] = PiratesGuiGlobals.TextFG9



class ShipTabBar(TabBar):
    
    def __init__(self, backParent, frontParent, parent, *args, **kw):
        optiondefs = (('relief', None, None), ('state', DGG.DISABLED, None), ('offset', 0.5, None))
        self.defineoptions(kw, optiondefs)
        TabBar.__init__(self, backParent, frontParent, parent, *args, **args)
        self.initialiseoptions(ShipTabBar)

    
    def makeTab(self, name, **kw):
        return ShipTab(self, name, **None)

    
    def refreshTabs(self):
        for (x, name) in enumerate(self.tabOrder):
            tab = self.tabs[name]
            tab.setPos(0.080000000000000002 + 0.17999999999999999 * (x + self.offset), 0, 0.059999999999999998)
            if tab.getParent() != self.bParent:
                tab.reparentTo(self.bParent)
                continue
        
        self.activeIndex = max(0, min(self.activeIndex, len(self.tabOrder) - 1))
        if len(self.tabOrder):
            name = self.tabOrder[self.activeIndex]
            tab = self.tabs[name]
            tab.reparentTo(self.fParent)
            tab.setZ(0.076999999999999999)
        


