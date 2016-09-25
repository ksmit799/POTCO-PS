# File: C (Python 2.4)

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase import DirectObject
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals

class ComboMeter(DirectObject.DirectObject):
    COMBO_METER_RESET = 2.0
    COMBO_NUM_SCALE = 0.14000000000000001
    BACKSTAB_SCALE = 0.089999999999999997
    TEXT_COLOR = PiratesGuiGlobals.TextFG1
    TEAM_COMBO_TEXT_COLOR = PiratesGuiGlobals.TextFG4
    SUB_TEXT_COLOR = PiratesGuiGlobals.TextFG2
    NUMBER_COLOR = PiratesGuiGlobals.TextFG1
    BACKSTAB_COLOR = Vec4(0.80000000000000004, 0.40000000000000002, 0.20000000000000001, 1)
    
    def __init__(self):
        DirectObject.DirectObject.__init__(self)
        self.combo = 0
        self.totalDamage = 0
        self.text = DirectLabel(parent = base.a2dTopLeft, relief = None, text = PLocalizer.HitCombo, text_align = TextNode.ALeft, text_scale = PiratesGuiGlobals.TextScaleTitleLarge, text_fg = self.TEXT_COLOR, text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 1, pos = (0.5, 0, -0.5), text_font = PiratesGlobals.getPirateOutlineFont())
        self.text.setTransparency(1)
        self.subText = DirectLabel(parent = self.text, relief = None, text = PLocalizer.Damage, text_align = TextNode.ALeft, text_scale = PiratesGuiGlobals.TextScaleTitleSmall, text_fg = self.SUB_TEXT_COLOR, text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 1, pos = (0.089999999999999997, 0, -0.070000000000000007), text_font = PiratesGlobals.getPirateOutlineFont())
        self.comboCounter = DirectLabel(parent = self.text, relief = None, text = '', text_align = TextNode.ARight, text_scale = self.COMBO_NUM_SCALE, text_fg = self.NUMBER_COLOR, text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 1, pos = (-0.025999999999999999, 0, -0.01), text_font = PiratesGlobals.getPirateOutlineFont())
        self.backstabText = DirectLabel(parent = base.a2dTopLeft, relief = None, text = 'Backstab!', text_align = TextNode.ALeft, text_scale = self.BACKSTAB_SCALE, text_fg = self.BACKSTAB_COLOR, text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 1, pos = (1.165, 0, -0.96999999999999997), text_font = PiratesGlobals.getPirateOutlineFont())
        self.text.hide()
        self.backstabText.hide()
        self.faderIn = None
        self.faderOut = None
        self.animIval = None
        self.backstabFaderIn = None
        self.backstabFaderOut = None
        self.backstabAnimIval = None
        self.accept('trackCombo', self.newHit)

    
    def destroy(self):
        if self.animIval:
            self.animIval.pause()
            self.animIval = None
        
        if self.faderIn:
            self.faderIn.pause()
            self.faderIn = None
        
        if self.faderOut:
            self.faderOut.pause()
            self.faderOut = None
        
        if self.backstabAnimIval:
            self.backstabAnimIval.pause()
            self.backstabAnimIval = None
        
        if self.backstabFaderIn:
            self.backstabFaderIn.pause()
            self.backstabFaderIn = None
        
        if self.backstabFaderOut:
            self.backstabFaderOut.pause()
            self.backstabFaderOut = None
        
        if self.text:
            self.text.destroy()
            self.text = None
        
        if self.backstabText:
            self.backstabText.destroy()
            self.backstabText = None
        
        self.ignoreAll()
        taskMgr.remove(self._ComboMeter__getResetComboMeter())

    
    def newHit(self, value, numAttackers, totalDamage):
        if value == 0 and numAttackers == 0 and totalDamage == 0:
            self.resetMeter()
        
        if value <= 1:
            return None
        
        self._ComboMeter__showMeter()
        if self.combo < value:
            self.combo = value
            self.comboCounter['text'] = str(self.combo)
            color = Vec4(0.59999999999999998 + value * 0.10000000000000001, 1.0 - value * 0.10000000000000001, 0, 1)
            self.comboCounter['text_fg'] = color
            if self.animIval:
                self.animIval.finish()
                self.animIval = None
            
            scaleIval = self.comboCounter.scaleInterval(0.20000000000000001, 1.0, startScale = 2.0, blendType = 'easeIn')
            self.animIval = Parallel(scaleIval)
            self.animIval.start()
        
        if numAttackers > 1:
            self.text['text'] = PLocalizer.TeamCombo
            self.text['text_fg'] = self.TEAM_COMBO_TEXT_COLOR
        
        if abs(self.totalDamage) < abs(totalDamage):
            self.totalDamage = totalDamage
            self.subText['text'] = str(abs(self.totalDamage)) + ' ' + PLocalizer.Damage
        
        taskMgr.remove(self._ComboMeter__getResetComboMeter())
        taskMgr.doMethodLater(self.COMBO_METER_RESET, self.resetMeter, self._ComboMeter__getResetComboMeter())

    
    def newBackstab(self):
        self._ComboMeter__showBackstab()
        if self.backstabAnimIval:
            self.backstabAnimIval.finish()
            self.backstabAnimIval = None
        
        scaleIval = self.backstabText.scaleInterval(0.20000000000000001, 1.0, startScale = 2.0, blendType = 'easeIn')
        self.backstabAnimIval = Parallel(scaleIval)
        self.backstabAnimIval.start()
        taskMgr.remove(self._ComboMeter__getResetBackstab())
        taskMgr.doMethodLater(self.COMBO_METER_RESET, self.resetBackstab, self._ComboMeter__getResetBackstab())

    
    def resetMeter(self, args = None):
        self._ComboMeter__fadeOutMeter()
        self.combo = 0
        self.totalDamage = 0

    
    def resetBackstab(self, args = None):
        self._ComboMeter__fadeOutBackstab()

    
    def _ComboMeter__getResetComboMeter(self):
        return 'resetComboMeter'

    
    def _ComboMeter__getResetBackstab(self):
        return 'resetBackstab'

    
    def _ComboMeter__hideMeter(self):
        if self.faderIn:
            self.faderIn.pause()
            self.faderIn = None
        
        if self.faderOut:
            self.faderOut.pause()
            self.faderOut = None
        
        self.text.hide()
        self.backstabText.hide()

    
    def _ComboMeter__showMeter(self):
        if self.faderIn:
            self.faderIn.pause()
            self.faderIn = None
        
        if self.faderOut:
            self.faderOut.pause()
            self.faderOut = None
        
        self.text.show()
        self.text.setAlphaScale(1.0)
        self.text['text_fg'] = self.TEXT_COLOR

    
    def _ComboMeter__showBackstab(self):
        if self.backstabFaderIn:
            self.backstabFaderIn.pause()
            self.backstabFaderIn = None
        
        if self.backstabFaderOut:
            self.backstabFaderOut.pause()
            self.backstabFaderOut = None
        
        self.backstabText.show()
        self.backstabText.setAlphaScale(1.0)

    
    def _ComboMeter__fadeInMeter(self):
        self.text.show()
        if self.faderOut:
            self.faderOut.pause()
            self.faderOut = None
        
        if self.faderIn:
            return None
        
        self.faderIn = LerpFunctionInterval(self.text.setAlphaScale, fromData = 0, toData = 1, duration = 1.0)
        self.faderIn.start()

    
    def _ComboMeter__fadeOutMeter(self):
        if self.faderIn:
            self.faderIn.pause()
            self.faderIn = None
        
        if self.faderOut:
            return None
        
        
        def restoreColor():
            self.text['text_fg'] = self.TEXT_COLOR
            self.text['text'] = PLocalizer.HitCombo
            self.subText['text'] = str(0) + ' ' + PLocalizer.Damage
            self.comboCounter['text'] = str(0)

        self.text.setAlphaScale(1.0)
        fadeOut = LerpFunctionInterval(self.text.setAlphaScale, fromData = 1, toData = 0, duration = 1.0)
        self.faderOut = Sequence(fadeOut, Func(self.text.hide), Func(restoreColor))
        self.faderOut.start()

    
    def _ComboMeter__fadeOutBackstab(self):
        if self.backstabFaderIn:
            self.backstabFaderIn.pause()
            self.backstabFaderIn = None
        
        if self.backstabFaderOut:
            return None
        
        self.backstabText.setAlphaScale(1.0)
        fadeOut = LerpFunctionInterval(self.backstabText.setAlphaScale, fromData = 1, toData = 0, duration = 1.0)
        self.backstabFaderOut = Sequence(fadeOut, Func(self.backstabText.hide))
        self.backstabFaderOut.start()


