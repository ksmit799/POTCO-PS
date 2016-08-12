# File: L (Python 2.4)

from otp.otpbase import OTPGlobals
from otp.otpbase import OTPLauncherGlobals
from otp.otpbase import OTPLocalizer
from direct.gui.DirectGui import *
from pandac.PandaModules import *
import os

class LeaveToPayDialog:
    
    def __init__(self, paidUser, destructorHook = None, doneFunc = None):
        self.destructorHook = destructorHook
        self.dialog = None
        self.okHandler = self._LeaveToPayDialog__handleLeaveToPayOK
        self.cancelHandler = self._LeaveToPayDialog__handleLeaveToPayCancel
        self.paidUser = paidUser
        self.doneFunc = doneFunc

    
    def setOK(self, handler):
        self.okHandler = handler

    
    def setCancel(self, handler):
        self.cancelHandler = handler

    
    def show(self):
        if self.paidUser:
            if base.cr.productName in [
                'DisneyOnline-AP',
                'DisneyOnline-UK',
                'JP',
                'FR']:
                directFrameText = OTPLocalizer.LeaveToEnableChatUK
                directButtonYesText = OTPLocalizer.LeaveToEnableChatUKYes
                directButtonNoText = OTPLocalizer.LeaveToEnableChatUKNo
            else:
                directFrameText = OTPLocalizer.LeaveToSetParentPassword
                directButtonYesText = OTPLocalizer.LeaveToSetParentPasswordYes
                directButtonNoText = OTPLocalizer.LeaveToSetParentPasswordNo
        else:
            directFrameText = OTPLocalizer.LeaveToPay
            directButtonYesText = OTPLocalizer.LeaveToPayYes
            directButtonNoText = OTPLocalizer.LeaveToPayNo
        if self.dialog == None:
            buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
            okButtonImage = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
            cancelButtonImage = (buttons.find('**/CloseBtn_UP'), buttons.find('**/CloseBtn_DN'), buttons.find('**/CloseBtn_Rllvr'))
            self.dialog = DirectFrame(parent = aspect2dp, pos = (0.0, 0.0, 0.0), relief = None, image = DGG.getDefaultDialogGeom(), image_color = OTPGlobals.GlobalDialogColor, image_scale = (0.90000000000000002, 1.0, 0.5), text = directFrameText, text_align = TextNode.ALeft, text_wordwrap = 14, text_scale = OTPLocalizer.LTPDdirectFrameText, text_pos = (-0.40000000000000002, 0.14999999999999999), textMayChange = 0)
            DirectButton(self.dialog, image = okButtonImage, relief = None, text = directButtonYesText, text_scale = OTPLocalizer.LTPDdirectButtonYesText, text_pos = (0.0, -0.10000000000000001), textMayChange = 0, pos = (-0.23000000000000001, 0.0, -0.10000000000000001), command = self.okHandler)
            DirectButton(self.dialog, image = cancelButtonImage, relief = None, text = directButtonNoText, text_scale = OTPLocalizer.LTPDdirectButtonNoText, text_pos = (0.0, -0.10000000000000001), textMayChange = 0, pos = (0.23000000000000001, 0.0, -0.10000000000000001), command = self.cancelHandler)
            buttons.removeNode()
        
        self.dialog.show()

    
    def hide(self):
        self.dialog.hide()

    
    def destroy(self):
        if self.destructorHook:
            self.destructorHook()
        
        if self.dialog:
            self.dialog.hide()
            self.dialog.destroy()
        
        self.dialog = None
        self.okHandler = None
        self.cancelHandler = None

    
    def removed(self):
        if hasattr(self, 'dialog') and self.dialog:
            return self.dialog.removed()
        else:
            return 1

    
    def _LeaveToPayDialog__handleLeaveToPayOK(self):
        self.destroy()
        errorCode = None
        if self.paidUser:
            if base.cr.productName in [
                'DisneyOnline-AP',
                'DisneyOnline-UK',
                'JP',
                'DE',
                'FR']:
                errorCode = OTPLauncherGlobals.ExitEnableChat
            else:
                errorCode = OTPLauncherGlobals.ExitSetParentPassword
        else:
            errorCode = OTPLauncherGlobals.ExitPurchase
        base.setExitErrorCode(errorCode)
        base.cr.loginFSM.request('shutdown', [
            errorCode])

    
    def _LeaveToPayDialog__handleLeaveToPayCancel(self):
        if self.doneFunc:
            self.doneFunc()
        
        self.destroy()


