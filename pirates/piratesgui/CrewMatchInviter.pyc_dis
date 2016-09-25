# File: C (Python 2.4)

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.reputation import ReputationGlobals
from pirates.piratesbase import PLocalizer
from pirates.band import BandConstance
from pirates.piratesgui.RequestButton import RequestButton

class CrewMatchInviterButton(RequestButton):
    
    def __init__(self, text, command):
        if text == PLocalizer.CrewMatchAdvancedOptionsButton or text == PLocalizer.CrewMatchSimpleOptionsButton:
            RequestButton.__init__(self, text, command, 2.1000000000000001)
        else:
            RequestButton.__init__(self, text, command)
        self.initialiseoptions(CrewMatchInviterButton)



class CrewMatchInviter(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('CrewMatchInviter')
    
    def __init__(self, currentRepLevel, advancedOptions = False):
        guiMain = loader.loadModel('models/gui/gui_main')
        DirectFrame.__init__(self, relief = None, pos = (0.65000000000000002, 0, 0.25), image = guiMain.find('**/general_frame_e'), image_pos = (0.25, 0, 0.27500000000000002), image_scale = 0.40000000000000002)
        self.initialiseoptions(CrewMatchInviter)
        self.setBin('gui-fixed', 0)
        self.currentRepLevel = currentRepLevel
        self.charGui = loader.loadModel('models/gui/char_gui')
        self.sliderOutputValue = '0'
        self.sliderOutputValueNoto = '0'
        self.sliderOutputValueSail = '0'
        self.sliderOutputValueCannon = '0'
        self.title = DirectLabel(parent = self, relief = None, text = PLocalizer.CrewMatchCrewLookout, text_scale = PiratesGuiGlobals.TextScaleTitleMed, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_font = PiratesGlobals.getPirateOutlineFont(), pos = (0.25, 0, 0.5), image = None, image_scale = 0.25)
        text = PLocalizer.CrewMatchInviterText
        self.advancedOptions = advancedOptions
        if not advancedOptions:
            self.message = DirectLabel(parent = self, relief = None, text = text, text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 15, pos = (0.25, 0, 0.34999999999999998), textMayChange = 1)
            self.rangeSlider = DirectSlider(parent = self, relief = None, range = (0, ReputationGlobals.GlobalLevelCap), value = base.localAvatar.guiMgr.crewHUD.getNotorietyMatchRange(), pageSize = 2, scale = (0.19, 0.23999999999999999, 0.23999999999999999), text = self.sliderOutputValue, text_scale = (0.20999999999999999, 0.17999999999999999, 0.17999999999999999), text_pos = (0, 0.074999999999999997), text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG1, textMayChange = 1, frameColor = (0.5, 0.5, 0.5, 0.29999999999999999), image = self.charGui.find('**/chargui_slider_small'), thumb_relief = None, image_scale = (2.1499999999999999, 2.1499999999999999, 1.5), thumb_image = (self.charGui.find('**/chargui_slider_node'), self.charGui.find('**/chargui_slider_node_down'), self.charGui.find('**/chargui_slider_node_over')), command = self._CrewMatchInviter__showSliderValue)
            self.rangeSlider.reparentTo(self)
            self.rangeSlider.setPos(0.25, 0, 0.19)
            self.bOk = CrewMatchInviterButton(text = PLocalizer.CrewInviterOK, command = self._CrewMatchInviter__handleOk)
            self.bOk.reparentTo(self)
            self.bOk.setPos(0.10000000000000001, 0, 0)
            self.bNo = CrewMatchInviterButton(text = PLocalizer.CrewMatchCancelButton, command = self._CrewMatchInviter__handleNo)
            self.bNo.reparentTo(self)
            self.bNo.setPos(0.29999999999999999, 0, 0)
            self.bAdvanced = CrewMatchInviterButton(text = PLocalizer.CrewMatchAdvancedOptionsButton, command = self._CrewMatchInviter__handleAdvanced)
            self.bAdvanced.reparentTo(self)
            self.bAdvanced.setPos(0.20000000000000001, 0, -0.074999999999999997)
        else:
            self.messageNoto = DirectLabel(parent = self, relief = None, text = PLocalizer.CrewMatchAdvancedNotorietyRange, text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 11, pos = (0.25, 0, 0.37), textMayChange = 1)
            self.messageSail = DirectLabel(parent = self, relief = None, text = PLocalizer.CrewMatchAdvancedMinSailSkillLevel, text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 8, pos = (0.050000000000000003, 0, 0.22), textMayChange = 1)
            self.messageCannon = DirectLabel(parent = self, relief = None, text = PLocalizer.CrewMatchAdvancedMinCannonSkillLevel, text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 8, pos = (0.45000000000000001, 0, 0.22), textMayChange = 1)
            self.rangeSliderNoto = DirectSlider(parent = self, relief = None, range = (0, ReputationGlobals.GlobalLevelCap), value = base.localAvatar.guiMgr.crewHUD.getNotorietyMatchRange(), pageSize = 2, scale = (0.19, 0.23999999999999999, 0.23999999999999999), text = self.sliderOutputValue, text_scale = (0.20999999999999999, 0.17999999999999999, 0.17999999999999999), text_pos = (0, 0.074999999999999997), text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG1, textMayChange = 1, frameColor = (0.5, 0.5, 0.5, 0.29999999999999999), image = self.charGui.find('**/chargui_slider_small'), thumb_relief = None, image_scale = (2.1499999999999999, 2.1499999999999999, 1.5), thumb_image = (self.charGui.find('**/chargui_slider_node'), self.charGui.find('**/chargui_slider_node_down'), self.charGui.find('**/chargui_slider_node_over')), command = self._CrewMatchInviter__showSliderValueNoto)
            self.rangeSliderSail = DirectSlider(parent = self, relief = None, range = (1, ReputationGlobals.LevelCap), value = base.localAvatar.guiMgr.crewHUD.getSailingMatchRange(), pageSize = 2, scale = (0.14999999999999999, 0.23999999999999999, 0.23999999999999999), text = self.sliderOutputValue, text_scale = (0.27000000000000002, 0.17999999999999999, 0.17999999999999999), text_pos = (0, 0.074999999999999997), text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG1, textMayChange = 1, frameColor = (0.5, 0.5, 0.5, 0.29999999999999999), image = self.charGui.find('**/chargui_slider_small'), thumb_relief = None, image_scale = (2.1499999999999999, 2.1499999999999999, 1.5), thumb_image = (self.charGui.find('**/chargui_slider_node'), self.charGui.find('**/chargui_slider_node_down'), self.charGui.find('**/chargui_slider_node_over')), command = self._CrewMatchInviter__showSliderValueSail)
            self.rangeSliderCannon = DirectSlider(parent = self, relief = None, range = (1, ReputationGlobals.LevelCap), value = base.localAvatar.guiMgr.crewHUD.getCannonMatchRange(), pageSize = 2, scale = (0.14999999999999999, 0.23999999999999999, 0.23999999999999999), text = self.sliderOutputValue, text_scale = (0.27000000000000002, 0.17999999999999999, 0.17999999999999999), text_pos = (0, 0.074999999999999997), text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG1, textMayChange = 1, frameColor = (0.5, 0.5, 0.5, 0.29999999999999999), image = self.charGui.find('**/chargui_slider_small'), thumb_relief = None, image_scale = (2.1499999999999999, 2.1499999999999999, 1.5), thumb_image = (self.charGui.find('**/chargui_slider_node'), self.charGui.find('**/chargui_slider_node_down'), self.charGui.find('**/chargui_slider_node_over')), command = self._CrewMatchInviter__showSliderValueCannon)
            self.rangeSliderNoto.reparentTo(self)
            self.rangeSliderNoto.setPos(0.25, 0, 0.31)
            self.rangeSliderSail.reparentTo(self)
            self.rangeSliderSail.setPos(0.050000000000000003, 0, 0.12)
            self.rangeSliderCannon.reparentTo(self)
            self.rangeSliderCannon.setPos(0.45000000000000001, 0, 0.12)
            self.bOk = CrewMatchInviterButton(text = PLocalizer.CrewInviterOK, command = self._CrewMatchInviter__handleOk)
            self.bOk.reparentTo(self)
            self.bOk.setPos(0.10000000000000001, 0, 0)
            self.bNo = CrewMatchInviterButton(text = PLocalizer.CrewMatchCancelButton, command = self._CrewMatchInviter__handleNo)
            self.bNo.reparentTo(self)
            self.bNo.setPos(0.29999999999999999, 0, 0)
            self.bAdvanced = CrewMatchInviterButton(text = PLocalizer.CrewMatchSimpleOptionsButton, command = self._CrewMatchInviter__handleAdvanced)
            self.bAdvanced.reparentTo(self)
            self.bAdvanced.setPos(0.20000000000000001, 0, -0.074999999999999997)
        self.accept('clientLogout', self.destroy)

    
    def destroy(self):
        if hasattr(self, 'destroyed'):
            return None
        
        self.destroyed = 1
        self.ignore('Esc')
        DirectFrame.destroy(self)

    
    def _CrewMatchInviter__handleOk(self):
        if not self.advancedOptions:
            base.localAvatar.guiMgr.crewHUD.setNotorietyMatchRange(int(self.sliderOutputValue))
            base.localAvatar.guiMgr.crewHUD.setAdvancedMatching(False)
            base.cr.crewMatchManager.changeCrewLookoutOptions(int(self.sliderOutputValue), 0, 0)
        else:
            base.localAvatar.guiMgr.crewHUD.setNotorietyMatchRange(int(self.sliderOutputValueNoto))
            base.localAvatar.guiMgr.crewHUD.setSailingMatchRange(int(self.sliderOutputValueSail))
            base.localAvatar.guiMgr.crewHUD.setCannonMatchRange(int(self.sliderOutputValueCannon))
            base.localAvatar.guiMgr.crewHUD.setAdvancedMatching(True)
            base.cr.crewMatchManager.changeCrewLookoutOptions(int(self.sliderOutputValueNoto), int(self.sliderOutputValueSail), int(self.sliderOutputValueCannon))
        self.destroy()

    
    def _CrewMatchInviter__handleNo(self):
        self.destroy()

    
    def _CrewMatchInviter__handleCancelFromAbove(self):
        self.destroy()

    
    def _CrewMatchInviter__showSliderValue(self):
        self.sliderOutputValue = str(int(self.rangeSlider['value']))
        self.rangeSlider['text'] = PLocalizer.CrewMatchRangeIndicator % str(int(self.rangeSlider['value']))

    
    def _CrewMatchInviter__showSliderValueNoto(self):
        self.sliderOutputValueNoto = str(int(self.rangeSliderNoto['value']))
        self.rangeSliderNoto['text'] = PLocalizer.CrewMatchRangeIndicator % str(int(self.rangeSliderNoto['value']))

    
    def _CrewMatchInviter__showSliderValueSail(self):
        self.sliderOutputValueSail = str(int(self.rangeSliderSail['value']))
        self.rangeSliderSail['text'] = PLocalizer.CrewMatchLevelIndicator % str(int(self.rangeSliderSail['value']))

    
    def _CrewMatchInviter__showSliderValueCannon(self):
        self.sliderOutputValueCannon = str(int(self.rangeSliderCannon['value']))
        self.rangeSliderCannon['text'] = PLocalizer.CrewMatchLevelIndicator % str(int(self.rangeSliderCannon['value']))

    
    def _CrewMatchInviter__handleAdvanced(self):
        if self.advancedOptions:
            CrewMatchInviter(self.currentRepLevel, False)
        else:
            CrewMatchInviter(self.currentRepLevel, True)
        self.destroy()


