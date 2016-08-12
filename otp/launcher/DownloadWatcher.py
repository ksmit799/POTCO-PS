# File: D (Python 2.4)

from direct.task import Task
from otp.otpbase import OTPLocalizer
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject

class DownloadWatcher(DirectObject):
    
    def __init__(self, phaseNames):
        self.phaseNames = phaseNames
        self.text = DirectLabel(relief = None, guiId = 'DownloadWatcherText', pos = (-0.95999999999999996, 0, -0.91000000000000003), text = OTPLocalizer.DownloadWatcherInitializing, text_fg = (1, 1, 1, 1), text_scale = 0.050000000000000003, textMayChange = 1, text_align = TextNode.ALeft, sortOrder = 50)
        self.bar = DirectWaitBar(guiId = 'DownloadWatcherBar', pos = (-0.81000000000000005, 0, -0.95999999999999996), relief = DGG.SUNKEN, frameSize = (-0.59999999999999998, 0.59999999999999998, -0.10000000000000001, 0.10000000000000001), borderWidth = (0.02, 0.02), scale = 0.25, range = 100, sortOrder = 50, frameColor = (0.5, 0.5, 0.5, 0.5), barColor = (0.20000000000000001, 0.69999999999999996, 0.20000000000000001, 0.5), text = '0%', text_scale = 0.16, text_fg = (1, 1, 1, 1), text_align = TextNode.ACenter, text_pos = (0, -0.050000000000000003))
        self.accept('launcherPercentPhaseComplete', self.update)

    
    def update(self, phase, percent, reqByteRate, actualByteRate):
        phaseName = self.phaseNames[phase]
        self.text['text'] = OTPLocalizer.DownloadWatcherUpdate % phaseName
        self.bar['text'] = '%s %%' % percent
        self.bar['value'] = percent

    
    def cleanup(self):
        self.text.destroy()
        self.bar.destroy()
        self.ignoreAll()


