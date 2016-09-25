# File: O (Python 2.4)

from pandac.PandaModules import Vec4
from direct.gui.DirectGui import DirectFrame, DGG
from direct.task import Task
from direct.showbase.PythonUtil import bound
from otp.otpbase import OTPGlobals

class OTPTimer(DirectFrame):
    ClockImage = None
    TimerId = 0
    
    def __init__(self, useImage = True, highlightNearEnd = True):
        if useImage:
            image = self.getImage()
        else:
            image = None
        DirectFrame.__init__(self, state = DGG.DISABLED, relief = None, scale = 0.45000000000000001, image = image, image_pos = (0, 0, 0), text = '0', text_fg = (0, 0, 0, 1), text_font = OTPGlobals.getInterfaceFont(), text_pos = (-0.01, -0.14999999999999999), text_scale = 0.34999999999999998)
        self.initialiseoptions(OTPTimer)
        self.timerId = OTPTimer.TimerId
        OTPTimer.TimerId += 1
        self.highlightNearEnd = highlightNearEnd
        self.countdownTask = None
        self.currentTime = 0
        self.taskTime = 0.0
        self.setFontColor(Vec4(0, 0, 0, 1))

    
    def setFontColor(self, vColor):
        self.vFontColor = vColor

    
    def getImage(self):
        if OTPTimer.ClockImage == None:
            model = loader.loadModel('phase_3.5/models/gui/clock_gui')
            OTPTimer.ClockImage = model.find('**/alarm_clock')
            model.removeNode()
        
        return OTPTimer.ClockImage

    
    def posInTopRightCorner(self):
        self.setPos(1.1599999999999999, 0, 0.82999999999999996)

    
    def posBelowTopRightCorner(self):
        self.setPos(1.1599999999999999, 0, 0.57999999999999996)

    
    def posAboveShtikerBook(self):
        self.setPos(1.1599999999999999, 0, -0.63)

    
    def setTime(self, time):
        time = bound(time, 0, 999)
        if time == self.currentTime:
            return None
        
        self.currentTime = time
        timeStr = str(time)
        timeStrLen = len(timeStr)
        if timeStrLen == 1:
            if time <= 5 and self.highlightNearEnd:
                self.setTimeStr(timeStr, 0.34000000000000002, (-0.025000000000000001, -0.125), Vec4(1, 0, 0, 1))
            else:
                self.setTimeStr(timeStr, 0.34000000000000002, (-0.025000000000000001, -0.125))
        elif timeStrLen == 2:
            self.setTimeStr(timeStr, 0.27000000000000002, (-0.025000000000000001, -0.10000000000000001))
        elif timeStrLen == 3:
            self.setTimeStr(timeStr, 0.20000000000000001, (-0.01, -0.080000000000000002))
        

    
    def setTimeStr(self, timeStr, scale = 0.20000000000000001, pos = (-0.01, -0.080000000000000002), fg = None):
        self['text'] = ''
        if not fg:
            pass
        self['text_fg'] = self.vFontColor
        self['text_scale'] = scale
        self['text_pos'] = pos
        self['text'] = timeStr

    
    def getElapsedTime(self):
        return self.taskTime

    
    def _timerTask(self, task):
        countdownTime = int(task.duration - task.time)
        self.setTime(countdownTime)
        self.taskTime = task.time
        if task.time >= task.duration:
            self.timerExpired()
            if task.callback:
                task.callback()
            
            return Task.done
        else:
            return Task.cont

    
    def countdown(self, duration, callback = None):
        self.countdownTask = Task.Task(self._timerTask)
        self.countdownTask.duration = duration
        self.countdownTask.callback = callback
        taskMgr.remove('timerTask%s' % self.timerId)
        return taskMgr.add(self.countdownTask, 'timerTask%s' % self.timerId)

    
    def timerExpired(self):
        pass

    
    def stop(self):
        if self.countdownTask:
            taskMgr.remove(self.countdownTask)
        

    
    def reset(self):
        self.stop()
        self.setTime(0)
        taskMgr.remove('timerTask%s' % self.timerId)
        self.taskTime = 0.0

    
    def destroy(self):
        self.reset()
        self.countdownTask = None
        DirectFrame.destroy(self)

    
    def cleanup(self):
        self.destroy()
        self.notify.warning('Call destroy, not cleanup')


