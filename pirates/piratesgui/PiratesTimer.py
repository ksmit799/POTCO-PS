# File: P (Python 2.4)

from otp.otpbase import OTPTimer
from direct.showbase.ShowBaseGlobal import *
from direct.task import Task
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import GuiButton
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
import time

class PiratesTimer(OTPTimer.OTPTimer):
    BGImage = None
    
    def __init__(self, showMinutes = 0, mode = None, titleText = '', titleFg = None, infoText = '', cancelText = '', cancelCallback = None, alarmTime = 0):
        self.showMinutes = showMinutes
        self.mode = mode
        OTPTimer.OTPTimer.__init__(self)
        self['text_pos'] = (0, 0)
        self['text_font'] = PiratesGlobals.getPirateOutlineFont()
        self['text'] = ''
        self.setFontColor(PiratesGuiGlobals.TextFG8)
        self.initialiseoptions(PiratesTimer)
        self.loadDials()
        self.setScale(1)
        self.alarmTime = alarmTime
        self.dialInterval = None
        self.alarmInterval = None
        self.alarmStarted = None
        if self.alarmTime > 0:
            self.alarmSfx = loadSfx(SoundGlobals.SFX_GUI_ALARM)
            self.outOfTimeSfx = loadSfx(SoundGlobals.SFX_GUI_OUT_OF_TIME)
        
        if titleText or infoText:
            self.createTimerText(titleText, titleFg, infoText)
        
        if cancelCallback:
            self.createCancelButton(cancelCallback, cancelText)
        
        self.slide = False
        self.end = False

    
    def destroy(self):
        self.stopAlarm()
        self.stopDial()
        OTPTimer.OTPTimer.destroy(self)

    
    def getImage(self):
        pass

    
    def loadDials(self):
        model = loader.loadModel('models/gui/gui_timer')
        model.setScale(0.20000000000000001)
        model.flattenLight()
        PiratesTimer.ClockImage = model.find('**/timer_front')
        PiratesTimer.BGImage = model.find('**/timer_back')
        model.removeNode()
        self.bgDial = DirectFrame(parent = self, state = DGG.DISABLED, relief = None, image = self.BGImage)
        self.fgLabel = DirectLabel(parent = self, state = DGG.DISABLED, relief = None, image = self.ClockImage, image_pos = (-0.01, 0, 0.035000000000000003), image_scale = (1.1000000000000001, 1, 0.80000000000000004), text_scale = 0.070000000000000007, text_align = TextNode.ACenter, text_font = PiratesGlobals.getPirateOutlineFont())

    
    def setTime(self, currTime):
        if currTime < 0:
            currTime = 0
        
        if self.slide:
            elapsedTime = self.getElapsedTime()
            if elapsedTime <= self.startTime:
                self.setPos(self.startPosition)
            
            if elapsedTime > self.startTime and elapsedTime < self.endTime:
                duration = self.endTime - self.startTime
                delta_time = self.getElapsedTime() - self.startTime
                t = delta_time / duration
                delta = self.endPosition - self.startPosition
                self.setPos(self.startPosition + delta * t)
            
            if elapsedTime >= self.endTime:
                self.setPos(self.endPosition)
            
        
        if currTime == self.currentTime:
            return None
        
        self.currentTime = currTime
        if currTime >= 60 and self.showMinutes:
            t = time.gmtime(currTime)
            timeStr = '%s:%s' % (t[4], str(t[5]).zfill(2))
        else:
            timeStr = str(currTime)
            self.fgLabel['text_scale'] = 0.070000000000000007
        timeStrLen = len(timeStr)
        if 0 >= currTime:
            pass
        currTime < self.alarmTime
        if 1:
            fgColor = Vec4(0.90000000000000002, 0.10000000000000001, 0.10000000000000001, 1)
            if not self.alarmStarted:
                self.startAlarm()
            
        else:
            fgColor = self.vFontColor
        if timeStrLen == 1:
            self.setTimeStr(timeStr, 0.089999999999999997, (0, -0.02), fgColor)
        elif timeStrLen == 2:
            self.setTimeStr(timeStr, 0.080000000000000002, (0, -0.014999999999999999))
        elif timeStrLen == 3:
            self.setTimeStr(timeStr, 0.080000000000000002, (0, -0.014999999999999999))
        else:
            self.setTimeStr(timeStr, 0.070000000000000007, (0, -0.012))

    
    def setTimeStr(self, timeStr, scale = 0.080000000000000002, pos = (0, -0.014999999999999999), fg = None):
        self.fgLabel['text'] = ''
        if not fg:
            pass
        self.fgLabel['text_fg'] = self.vFontColor
        self.fgLabel['text_scale'] = scale
        self.fgLabel['text_pos'] = pos
        self.fgLabel['text'] = timeStr

    
    def countdown(self, duration, callback = None):
        OTPTimer.OTPTimer.countdown(self, duration, callback)
        self.fgLabel['text_font'] = PiratesGlobals.getInterfaceFont()
        self.fgLabel['text_scale'] = 0.070000000000000007
        self.startDial()

    
    def timerExpired(self):
        self.stop()
        self.stopDial()
        if self.alarmTime > 0:
            base.playSfx(self.outOfTimeSfx)
        
        self.stopAlarm()

    
    def createTimerText(self, titleText, titleFg, infoText):
        self.titleText = DirectFrame(parent = self, state = DGG.DISABLED, relief = None, text = titleText, text_align = TextNode.ACenter, text_scale = 0.050000000000000003, text_fg = titleFg, text_shadow = PiratesGuiGlobals.TextShadow, text_font = PiratesGlobals.getPirateOutlineFont(), textMayChange = 1, text_wordwrap = 6, pos = (0, 0, 0.69999999999999996))
        self.infoText = DirectFrame(parent = self, state = DGG.DISABLED, relief = None, text = infoText, text_align = TextNode.ACenter, text_scale = 0.14000000000000001, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_font = PiratesGlobals.getPirateOutlineFont(), textMayChange = 1, text_wordwrap = 6, pos = (0, 0, -0.75))

    
    def createCancelButton(self, cancelCallback, cancelText):
        if self.mode != PiratesGlobals.HIGHSEAS_ADV_WAIT:
            return None
        
        if not base.localAvatar.isCrewCaptain():
            return None
        
        self.cancelButton = GuiButton.GuiButton(parent = self, helpText = cancelText, command = cancelCallback, borderWidth = PiratesGuiGlobals.BorderWidth, text = PLocalizer.Cancel, frameColor = PiratesGuiGlobals.ButtonColor3, text_fg = PiratesGuiGlobals.TextFG2, text_pos = (0, 0.014999999999999999), frameSize = (-0.089999999999999997, 0.089999999999999997, -0.014999999999999999, 0.065000000000000002), text_scale = PiratesGuiGlobals.TextScaleLarge, pad = (0.01, 0.01), pos = (0, 0, -1.55), scale = 2.2999999999999998)

    
    def startDial(self, t = 6):
        if self.dialInterval:
            self.dialInterval.pause()
            self.dialInterval = None
        
        self.dialInterval = LerpHprInterval(self.bgDial, t, Vec3(0, 0, 360), Vec3(0, 0, 0))
        self.dialInterval.loop()

    
    def stopDial(self):
        if self.dialInterval:
            self.dialInterval.pause()
            self.dialInterval = None
        

    
    def startAlarm(self):
        if self.end == False:
            self.alarmStarted = 1
            origScale = self.getScale()
            scale = origScale * 1.2
            t = 0.5
            self.alarmInterval = Sequence(Parallel(SoundInterval(self.alarmSfx), LerpScaleInterval(self, t, scale, origScale, blendType = 'noBlend')), Parallel(SoundInterval(self.alarmSfx), LerpScaleInterval(self, t, origScale, scale, blendType = 'noBlend')))
            self.alarmInterval.loop()
            self.startDial(t = 2)
        

    
    def stopAlarm(self):
        self.alarmStarted = 0
        if self.alarmInterval:
            self.alarmInterval.pause()
            self.alarmInterval = None
        
        self.end = True

    
    def setSlide(self, startTime, endTime, startPosition, endPosition):
        self.slide = True
        self.startTime = startTime
        self.endTime = endTime
        self.startPosition = startPosition
        self.endPosition = endPosition


