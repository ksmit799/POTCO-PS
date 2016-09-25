# File: C (Python 2.4)

from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.piratesgui.TabBar import LeftTab, TabBar
from pirates.piratesbase import PLocalizer

class ChestTab(LeftTab):
    
    def __init__(self, tabBar, name, **kw):
        optiondefs = (('modelName', 'general_frame_d', None), ('borderScale', 0.38, None), ('bgBuffer', 0.14999999999999999, None), ('frameSize', (-0.125, 0.125, -0.10000000000000001, 0.10000000000000001), None), ('unfocusSize', (0, 0, 0, 0), None), ('focusSize', (-0.125, 0.125, -0.11, 0.11), None), ('heightFactor', 0.59999999999999998, None), ('mouseEntered', None, None), ('mouseLeft', None, None))
        self.defineoptions(kw, optiondefs)
        LeftTab.__init__(self, tabBar, name, **None)
        self.initialiseoptions(ChestTab)
        self['unfocusSize'] = self['frameSize']



class ChestTabBar(TabBar):
    
    def refreshTabs(self):
        zOffset = 0.0
        for name in self.tabOrder:
            tab = self.tabs[name]
            tab.reparentTo(self.bParent)
            tab.setPos(-0.62, 0, 0.37 - self.offset - zOffset)
            tab['frameSize'] = tab['unfocusSize']
            zOffset += tab.getHeight() * tab['heightFactor']
        
        self.activeIndex = max(0, min(self.activeIndex, len(self.tabOrder) - 1))
        if len(self.tabOrder):
            name = self.tabOrder[self.activeIndex]
            tab = self.tabs[name]
            tab.reparentTo(self.fParent)
            tab.setX(-0.64000000000000001)
            tab['frameSize'] = tab['focusSize']
        

    
    def makeTab(self, name, **kw):
        return ChestTab(self, name, **None)



class ChestPanel(DirectFrame):
    
    def __init__(self, parent, **kw):
        optiondefs = (('relief', None, None), ('state', DGG.NORMAL, None), ('frameSize', (-0.55000000000000004, 0.55000000000000004, -0.81999999999999995, 0.71999999999999997), None), ('pos', (-0.55000000000000004, 0, 0.80000000000000004), None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent = NodePath(), **None)
        self.initialiseoptions(ChestPanel)
        self.setBin('gui-fixed', 0)
        self.setupLayers()
        self.hideIval = None
        self.showIval = None
        self.destZ = 0.80000000000000004
        self.active = False
        self.currPageIndex = None
        self.pages = []
        self.pageTabs = []
        self.accept('page_down', self._ChestPanel__pageChange, [
            1])
        self.accept('page_up', self._ChestPanel__pageChange, [
            -1])
        self.hide()
        if not parent:
            pass
        self.reparentTo(aspect2d)
        self.beenOpen = 0

    
    def destroy(self):
        self.cancelIval()
        del self.hideIval
        del self.showIval
        for page in self.pages:
            page.destroy()
        
        del self.pages
        del self.pageTabs
        self.ignoreAll()
        DirectFrame.destroy(self)

    
    def setupLayers(self):
        if hasattr(self, 'border'):
            self.border.destroy()
            self.sideTentacle.removeNode()
            self.background.removeNode()
            self.backTabParent.removeNode()
            self.frontTabParent.removeNode()
            self.b.removeNode()
        
        gui = loader.loadModel('models/gui/gui_sea_chest')
        scale = 0.32000000000000001
        self.sideTentacle = self.attachNewNode('sideTentacle')
        self.sideTentacle.setScale(scale)
        gui.find('**/side_tentacle').copyTo(self.sideTentacle)
        self.sideTentacle.flattenStrong()
        self.sideTentacle.show()
        self.backTabParent = self.attachNewNode('backTabs')
        self.background = self.attachNewNode('background')
        self.background.setScale(scale)
        gui.find('**/background').copyTo(self.background)
        self.background.flattenStrong()
        border = self.attachNewNode('border', sort = 1)
        geom = gui.find('**/border').copyTo(border)
        geom.flattenStrong()
        geom.setScale(scale)
        self.frontTabParent = self.attachNewNode('frontTab', sort = 2)
        mainGui = loader.loadModel('models/gui/gui_main')
        self.titleLabel = DirectFrame(relief = None, parent = self, textMayChange = 1, image = mainGui.find('**/title_bar_08'), image_scale = 0.20000000000000001, image_pos = (0, 0, -0.315), text = PLocalizer.InventoryPageTitle, text_fg = (1, 1, 1, 1), text_font = PiratesGlobals.getPirateBoldOutlineFont(), text_scale = 0.070000000000000007, text_align = TextNode.ACenter, text_shadow = PiratesGuiGlobals.TextShadow, text_pos = (0.0, 0.0), pos = (0, 0, 0.66000000000000003))
        self.titleLabel.setBin('gui-fixed', 1)

    
    def _getShowIval(self, time = 0.20000000000000001):
        self.showIval = Sequence(Func(localAvatar.guiMgr.moveLookoutPopup, True), Func(self.show), self.posInterval(time, Point3(-0.55000000000000004, 0, self.destZ), blendType = 'easeOut'), Func(self.slideOpenCallback))
        return self.showIval

    
    def _getHideIval(self, time = 0.20000000000000001):
        self.hideIval = Sequence(Func(self.slideCloseCallback), self.posInterval(time, Point3(-0.55000000000000004, 0, -1.8), blendType = 'easeIn'), Func(self.hide), Func(localAvatar.guiMgr.moveLookoutPopup, False))
        return self.hideIval

    
    def cancelIval(self, type = [
        'show',
        'hide']):
        if self.showIval and self.showIval.isPlaying() and 'show' in type:
            self.showIval.pause()
        
        if self.hideIval and self.hideIval.isPlaying() and 'hide' in type:
            self.hideIval.pause()
        

    
    def setZLoc(self, z):
        self.destZ = z
        if self.showIval:
            self.showIval[2].setEndPos(Point3(-0.55000000000000004, 0, z))
        

    
    def addPage(self, page, index = -1):
        if hasattr(self, 'pages'):
            page.reparentTo(self)
            page.hide()
            if index == -1:
                self.pages.append(page)
            else:
                self.pages.insert(index, page)
                if self.currPageIndex >= index:
                    self.currPageIndex += 1
                
        

    
    def removePage(self, page):
        page.detachNode()
        self.pages.remove(page)

    
    def setPage(self, page):
        pageIndex = self.pages.index(page)
        if self.currPageIndex is not None:
            if self.currPageIndex != pageIndex:
                self.pages[self.currPageIndex].hide()
                self.currPageIndex = pageIndex
                page.show()
            
        else:
            self.currPageIndex = pageIndex
            page.show()

    
    def makeCurPage(self, pageDesired):
        if pageDesired in self.pages:
            pageIndex = self.pages.index(pageDesired)
            self.setCurPage(pageIndex)
        

    
    def setCurPage(self, pageIndex):
        if self.currPageIndex != None:
            self.currPageIndex = pageIndex
        

    
    def getCurPage(self):
        if self.currPageIndex != None:
            return self.pages[self.currPageIndex]
        

    
    def _ChestPanel__pageChange(self, offset):
        if self.currPageIndex is None:
            return None
        
        self.pages[self.currPageIndex].hide()
        self.currPageIndex = self.currPageIndex + offset
        self.currPageIndex = max(self.currPageIndex, 0)
        self.currPageIndex = min(self.currPageIndex, len(self.pages) - 1)
        page = self.pages[self.currPageIndex]
        page.show()

    
    def slideOpen(self):
        if not self.isActive():
            if not self.getCurPage() and localAvatar.guiMgr.getTutorialStatus() >= PiratesGlobals.TUT_GOT_SEACHEST:
                self.setPage(self.pages[0])
            
            self.cancelIval('hide')
            self.setActive(True)
            self.slideOpenPrecall()
            self._getShowIval().start()
        

    
    def slideClose(self):
        if self.isActive():
            (self.cancelIval('show'),)
            self.setActive(False)
            self._getHideIval().start()
        

    
    def slideOpenPrecall(self):
        curPage = self.getCurPage()
        if curPage:
            curPage.slideOpenPrecall()
        

    
    def slideOpenCallback(self):
        curPage = self.getCurPage()
        if curPage:
            curPage.slideOpenCallback()
        

    
    def slideCloseCallback(self):
        curPage = self.getCurPage()
        if curPage:
            curPage.slideCloseCallback()
        

    
    def show(self, *args, **kwargs):
        if not self.beenOpen:
            self.setActive(False)
            localAvatar.guiMgr.showInventoryBagPanel()
            self.setActive(True)
            self.beenOpen = 1
        elif self.getCurPage():
            self.getCurPage().show()
        
        super(self.__class__, self).show(*args, **args)

    
    def hide(self, *args, **kwargs):
        super(self.__class__, self).hide(*args, **args)
        curPage = self.getCurPage()
        if curPage:
            curPage.hide()
        

    
    def setActive(self, active):
        self.active = active

    
    def isActive(self):
        return self.active

    
    def makeTabBar(self, offset = 0):
        return ChestTabBar(parent = self, backParent = self.backTabParent, frontParent = self.frontTabParent, offset = offset)

    
    def setTitleName(self, text):
        self.titleLabel['text'] = text


