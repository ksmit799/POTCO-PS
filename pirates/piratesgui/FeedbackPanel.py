# File: F (Python 2.4)

import sys
import os
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
from pirates.piratesgui.CheckBox import CheckBox
from direct.gui.DirectCheckBox import DirectCheckBox
from pirates.piratesgui import PNameTumbler
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.distributed import InteractGlobals

try:
    import embedded
    hasEmbedded = 1
except ImportError:
    hasEmbedded = 0


class FeedbackConfirmButton(RequestButton):
    
    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(FeedbackConfirmButton)



class FeedbackCancelButton(RequestButton):
    
    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(FeedbackCancelButton)



class FeedbackAccountButton(RequestButton):
    
    def __init__(self, text, command):
        RequestButton.__init__(self, text, command, 1.8500000000000001)
        self.initialiseoptions(FeedbackAccountButton)



class FeedbackInput(GuiPanel.GuiPanel):
    
    def __init__(self, commandToExe):
        currentInteraction = base.cr.interactionMgr.getCurrent()
        if not hasattr(currentInteraction, 'storeType'):
            GuiPanel.GuiPanel.__init__(self, '', 0.73499999999999999, 0.46999999999999997, 0, '', pos = (0.42999999999999999, 0, -0.71999999999999997))
        elif currentInteraction.storeType in [
            InteractGlobals.ACCESSORIES_STORE,
            InteractGlobals.CATALOG_STORE,
            InteractGlobals.TATTOO_STORE,
            InteractGlobals.JEWELRY_STORE,
            InteractGlobals.BARBER_STORE]:
            GuiPanel.GuiPanel.__init__(self, '', 0.73499999999999999, 0.46999999999999997, 0, '', pos = (-1.22, 0, -0.71999999999999997))
        else:
            GuiPanel.GuiPanel.__init__(self, '', 0.73499999999999999, 0.46999999999999997, 0, '', pos = (0.42999999999999999, 0, -0.71999999999999997))
        self.commandToExe = commandToExe
        self.accept('clientLogout', self.destroy)
        self.accept('destroyFeedbackPanel', self.destroy)

    
    def destroy(self):
        if hasattr(self, 'destroyed'):
            return None
        
        self.destroyed = 1
        self.ignore('Esc')
        GuiPanel.GuiPanel.destroy(self)

    
    def generateFeedbackPanel(self, commandToExe):
        self.feedbackInput = DirectEntry(parent = self, relief = DGG.GROOVE, scale = 0.050999999999999997, pos = (0.0070000000000000001, 0, 0.41999999999999998), borderWidth = PiratesGuiGlobals.BorderWidth, frameColor = (0, 0.0, 0.0, 0.5), text_align = TextNode.ALeft, width = 14, numLines = 9, focus = 1, cursorKeys = 1, text_fg = (1, 1, 1, 1), command = self.commandToExe, suppressKeys = 1, suppressMouse = 1, autoCapitalize = 0)
        return self.feedbackInput



class FeedbackPanel(GuiPanel.GuiPanel):
    notify = DirectNotifyGlobal.directNotify.newCategory('FeedbackPanel')
    
    def __init__(self):
        if hasattr(base, 'localAvatar'):
            if base.localAvatar.guiMgr.feedbackFormActive:
                return None
            else:
                base.localAvatar.guiMgr.feedbackFormActive = True
        
        title = PLocalizer.FeedbackFormTitle
        self.hasEmbedded = hasEmbedded
        currentInteraction = base.cr.interactionMgr.getCurrent()
        if not hasattr(currentInteraction, 'storeType'):
            GuiPanel.GuiPanel.__init__(self, title, 0.79000000000000004, 1.1499999999999999, 0, 1.5, pos = (0.40000000000000002, 0, -0.82999999999999996))
        elif currentInteraction.storeType in [
            InteractGlobals.ACCESSORIES_STORE,
            InteractGlobals.CATALOG_STORE,
            InteractGlobals.TATTOO_STORE,
            InteractGlobals.JEWELRY_STORE,
            InteractGlobals.BARBER_STORE]:
            GuiPanel.GuiPanel.__init__(self, title, 0.79000000000000004, 1.1499999999999999, 0, 1.5, pos = (-1.25, 0, -0.82999999999999996))
        else:
            GuiPanel.GuiPanel.__init__(self, title, 0.79000000000000004, 1.1499999999999999, 0, 1.5, pos = (0.40000000000000002, 0, -0.82999999999999996))
        self.initialiseoptions(FeedbackPanel)
        self.charGui = loader.loadModel('models/gui/char_gui')
        message = PLocalizer.FeedbackFormMessage
        self.message = DirectLabel(parent = self, relief = None, text = message, text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 10, pos = (0.2225, 0, 0.93000000000000005), textMayChange = 1)
        self.categoryItems = PLocalizer.FeedbackFormCatItems
        self.categoryItems.sort()
        self.tumbler = PNameTumbler.PNameTumbler(self.categoryItems, '')
        self.tumbler.reparentTo(self)
        self.tumbler.setPos(0.57799999999999996, 0, 0.90000000000000002)
        self.tumbler.setScale(0.75)
        self.feedbackObj = FeedbackInput(self._typedAComment)
        self.feedbackInput = self.feedbackObj.generateFeedbackPanel(self._typedAComment)
        self.feedbackInput.reparentTo(self.feedbackObj)
        self.feedbackObj.setBin('gui-popup', 0)
        self.bOk = FeedbackConfirmButton(text = PLocalizer.FeedbackFormSend, command = self._FeedbackPanel__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.074999999999999997, 0, 0.025000000000000001)
        self.bCancel = FeedbackCancelButton(text = PLocalizer.GenericConfirmCancel, command = self._FeedbackPanel__handleCancel)
        self.bCancel.reparentTo(self)
        self.bCancel.setPos(0.26800000000000002, 0, 0.025000000000000001)
        self.bManageAccount = FeedbackAccountButton(text = PLocalizer.FeedbackManageButton, command = self._FeedbackPanel__handleAccountWeb)
        self.bManageAccount.reparentTo(self)
        self.bManageAccount.setPos(0.54000000000000004, 0, 0.025000000000000001)
        self.accept('clientLogout', self.destroy)
        self.accept('destroyFeedbackPanel', self.destroy)

    
    def destroy(self):
        if hasattr(base, 'localAvatar'):
            base.localAvatar.guiMgr.feedbackFormActive = False
        
        if hasattr(self, 'destroyed'):
            return None
        
        self.destroyed = 1
        self.ignore('Esc')
        GuiPanel.GuiPanel.destroy(self)

    
    def _FeedbackPanel__handleOk(self):
        base.cr.centralLogger.writeClientEvent('GUEST_FEEDBACK|%s|%s' % (self.tumbler.getName(), self.feedbackInput.get()))
        self.destroy()
        self.feedbackObj.destroy()

    
    def _FeedbackPanel__handleCancel(self):
        self.feedbackObj.destroy()
        self.destroy()

    
    def _FeedbackPanel__handleCancelFromAbove(self):
        self.feedbackObj.destroy()
        self.destroy()

    
    def _FeedbackPanel__handleAccountWeb(self):
        base.popupBrowser(launcher.getValue('GAME_INGAME_MANAGE_ACCT'))
        self.feedbackObj.destroy()
        self.destroy()

    
    def _typedAComment(self, *args):
        self.feedbackInput['focus'] = 0
        name = self.feedbackInput.get()
        name = TextEncoder().decodeText(name)
        name = name.strip()
        name = TextEncoder().encodeWtext(name)
        self.feedbackInput.enterText(name)

    
    def _catSelect(self, item):
        print 'Item Selected is %s' % item


