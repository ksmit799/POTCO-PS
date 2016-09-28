# File: M (Python 2.4)

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.band import BandConstance
from pirates.piratesgui.RequestButton import RequestButton

class MainMenuConfirmButton(RequestButton):
    
    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(MainMenuConfirmButton)



class MainMenuConfirm(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('MainMenuConfirm')
    
    def __init__(self, type):
        guiMain = loader.loadModel('models/gui/gui_main')
        DirectFrame.__init__(self, relief = None, image = loader.loadModel('models/misc/fade'), image_scale = (5, 2, 2), image_color = (0, 0, 0, 0.80000000000000004), image_pos = (0.5, 0, 0.80000000000000004), state = DGG.NORMAL, pos = (-0.80000000000000004, 0.0, -0.80000000000000004), sortOrder = 20)
        self.confirmBox = DirectFrame(parent = self, relief = None, pos = (0.55000000000000004, 0, 0.65000000000000002), image = guiMain.find('**/general_frame_e'), image_pos = (0.25, 0, 0.27500000000000002), image_scale = 0.25)
        self.initialiseoptions(MainMenuConfirm)
        titleText = ''
        messageText = ''
        self.type = type
        if self.type == 'logout':
            titleText = PLocalizer.MainMenuLogout
            messageText = PLocalizer.MainMenuLogoutConfirm
        elif self.type == 'quit':
            titleText = PLocalizer.MainMenuQuit
            messageText = PLocalizer.MainMenuQuitConfirm
        
        self.title = DirectLabel(parent = self.confirmBox, relief = None, text = titleText, text_scale = PiratesGuiGlobals.TextScaleExtraLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_font = PiratesGlobals.getPirateOutlineFont(), pos = (0.25, 0, 0.41999999999999998))
        self.message = DirectLabel(parent = self.confirmBox, relief = None, text = messageText, text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 11, pos = (0.25, 0, 0.32500000000000001), textMayChange = 1)
        self.bOk = MainMenuConfirmButton(text = PLocalizer.TeleportConfirmOK, command = self._MainMenuConfirm__handleOk)
        self.bOk.reparentTo(self.confirmBox)
        self.bOk.setPos(0.10000000000000001, 0, 0.050000000000000003)
        self.bNo = MainMenuConfirmButton(text = PLocalizer.TeleportConfirmNo, command = self._MainMenuConfirm__handleNo)
        self.bNo.reparentTo(self.confirmBox)
        self.bNo.setPos(0.29999999999999999, 0, 0.050000000000000003)

    
    def destroy(self):
        if hasattr(self, 'destroyed'):
            return None
        
        self.destroyed = 1
        self.ignore('Esc')
        DirectFrame.destroy(self)

    
    def _MainMenuConfirm__handleOk(self):
        if self.type == 'logout':
            if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr and base.localAvatar.guiMgr.mainMenu:
                base.localAvatar.guiMgr.mainMenu.logout_dialog_command(1)
            
        elif self.type == 'quit':
            base.userExit()
        
        self.destroy()

    
    def _MainMenuConfirm__handleNo(self):
        self.destroy()


