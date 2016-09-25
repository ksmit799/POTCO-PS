# File: C (Python 2.4)

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals
from pirates.piratesgui import PDialog
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.band import BandConstance
from pirates.piratesgui.RequestButton import RequestButton
CREW_ICON_BAM = 'models/gui/gui_main'
CREW_ICONS = {
    1: 'crew_member/crew_member',
    2: 'crew_member/crew_member' }

class CrewIconSelectorConfirmButton(RequestButton):
    
    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(CrewIconSelectorConfirmButton)



class CrewIconSelectorCancelButton(RequestButton):
    
    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(CrewIconSelectorCancelButton)



class CrewIconSelector(GuiPanel.GuiPanel):
    notify = DirectNotifyGlobal.directNotify.newCategory('CrewIconSelector')
    
    def __init__(self, title, selectedIconKey = 0):
        GuiPanel.GuiPanel.__init__(self, title, 0.80000000000000004, 0.77000000000000002, 0, '', pos = (0.52000000000000002, 0, -0.81999999999999995))
        self.initialiseoptions(CrewIconSelector)
        self.setPics = { }
        self.selectedIconKey = selectedIconKey
        self.currentIconKey = base.localAvatar.getCrewIcon()
        self.localHeight = PiratesGuiGlobals.InventoryPanelHeight - 0.20000000000000001
        gui = loader.loadModel('models/gui/toplevel_gui')
        spotPic = gui.find('**/treasure_w_a_slot')
        self.card = loader.loadModel(CREW_ICON_BAM)
        crewIconParent = NodePath('crewIconParent')
        for colSpot in range(4):
            for rowSpot in range(4):
                if colSpot > 0:
                    blip = spotPic.copyTo(crewIconParent)
                    blip.setScale(0.45000000000000001)
                    blip.setPos(0.23999999999999999 + 0.17999999999999999 * rowSpot, 0, self.localHeight - 0.40000000000000002 - 0.17999999999999999 * colSpot)
                    continue
            
        
        crewIconParent.flattenStrong()
        self.iconFrame = DirectFrame(parent = self, relief = None, geom = crewIconParent)
        self.iconFrame.setPos(-0.10000000000000001, 0, -0.12)
        self.bOk = CrewIconSelectorConfirmButton(text = PLocalizer.GenericConfirmOK, command = self._CrewIconSelector__handleOK)
        self.bCancel = CrewIconSelectorCancelButton(text = PLocalizer.DialogCancel, command = self._CrewIconSelector__handleCancel)
        self.bOk.reparentTo(self)
        self.bCancel.reparentTo(self)
        self.bOk.setPos(0.25, 0, 0.050000000000000003)
        self.bCancel.setPos(0.45000000000000001, 0, 0.050000000000000003)
        self.loadIconList()

    
    def destroy(self):
        if hasattr(self, 'destroyed'):
            return None
        
        self.destroyed = 1
        self.ignore('Esc')
        GuiPanel.GuiPanel.destroy(self)

    
    def _CrewIconSelector__handleOK(self):
        if type(self.selectedIconKey) != int:
            self.selectedIconKey = 0
        
        base.cr.PirateBandManager.d_requestCrewIconUpdate(self.selectedIconKey)
        self.destroy()

    
    def _CrewIconSelector__handleCancel(self):
        base.localAvatar.setCrewIcon(self.currentIconKey)
        self.destroy()

    
    def loadIconList(self):
        setCount = len(CREW_ICONS)
        rowSpot = 0
        colSpot = 0
        counter = 0
        for (loopItr, iconFile) in CREW_ICONS.iteritems():
            setKey = loopItr
            pic_name = iconFile
            tex = self.card.find('**/%s' % pic_name)
            self.setPics[setKey] = DirectButton(parent = self.iconFrame, relief = None, image = tex, image_scale = 0.34000000000000002, image2_scale = 0.35999999999999999, image_pos = (0, 0, 0), pos = (0.23999999999999999 + 0.17999999999999999 * rowSpot, 0, self.localHeight - 0.40000000000000002 - 0.17999999999999999 * colSpot - 0.17999999999999999), command = self._CrewIconSelector__setIconKey, extraArgs = [
                setKey], pressEffect = 1)
            self.setPics[setKey].setTransparency(1)
            counter += 1
            rowSpot = counter % 4
            colSpot = counter / 4
        

    
    def _CrewIconSelector__setIconKey(self, setValue):
        self.selectedIconKey = setValue
        base.localAvatar.setCrewIcon(setValue)


