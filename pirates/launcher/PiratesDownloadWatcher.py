from otp.launcher import DownloadWatcher
from otp.otpbase import OTPLocalizer
from panda3d.core import Point3, TextNode
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectWaitBar import DirectWaitBar
from direct.gui import DirectGuiGlobals as DGG
from direct.gui.DirectGuiGlobals import NO_FADE_SORT_INDEX

class PiratesDownloadWatcher(DownloadWatcher.DownloadWatcher):
    positions = [
        (Point3(1, 0, 0.90000000000000002), Point3(1, 0, 0.90000000000000002)),
        (Point3(1, 0, 0.90000000000000002), Point3(1, 0, 0.90000000000000002)),
        (Point3(1, 0, 0.90000000000000002), Point3(1, 0, 0.90000000000000002))]
    
    def __init__(self, phaseNames):
        self.phaseNames = phaseNames
        self.model = loader.loadModel('models/gui/pir_m_gui_gen_loadingBar')
        bar = self.model.findTexture('pir_t_gui_gen_loadingBar')
        self.model.find('**/loading_bar').hide()
        self.topFrame = DirectFrame(parent = base.a2dTopRight, pos = (-0.80000000000000004, 0, -0.10000000000000001), sortOrder = NO_FADE_SORT_INDEX + 1)
        self.text = DirectLabel(relief = None, parent = self.topFrame, guiId = 'DownloadWatcherText', pos = (0, 0, 0), text = '                     ', text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1), text_scale = 0.040000000000000001, textMayChange = 1, text_align = TextNode.ARight, text_pos = (0.17000000000000001, 0), sortOrder = 2)
        self.bar = DirectWaitBar(relief = None, parent = self.topFrame, guiId = 'DownloadWatcherBar', pos = (0, 0, 0), frameSize = (-0.40000000000000002, 0.38, -0.044999999999999998, 0.065000000000000002), borderWidth = (0.02, 0.02), range = 100, frameColor = (1, 1, 1, 1), barColor = (0, 0.29999999999999999, 0, 1), barTexture = bar, geom = self.model, geom_scale = 0.089999999999999997, geom_pos = (-0.014, 0, 0.01), text = '0%', text_scale = 0.040000000000000001, text_fg = (1, 1, 1, 1), text_align = TextNode.ALeft, text_pos = (0.19, 0), sortOrder = 1)
        self.bgFrame = DirectFrame(relief = DGG.FLAT, parent = self.topFrame, pos = (0, 0, 0), frameColor = (0.5, 0.27000000000000002, 0.35999999999999999, 0.20000000000000001), frameSize = (-0.44, 0.39000000000000001, -0.035999999999999997, 0.056000000000000001), borderWidth = (0.02, 0.02), scale = 0.90000000000000002, sortOrder = 0)
        self.accept('launcherPercentPhaseComplete', self.update)

    
    def update(self, phase, percent, reqByteRate, actualByteRate):
        phaseName = self.phaseNames[phase]
        self.text['text'] = OTPLocalizer.DownloadWatcherUpdate % phaseName + '  -'
        self.bar['text'] = '%s %%' % percent
        self.bar['value'] = percent

    
    def foreground(self):
        self.topFrame.reparentTo(base.a2dpTopRight)
        self.topFrame.setBin('gui-fixed', 55)
        self.topFrame['sortOrder'] = NO_FADE_SORT_INDEX + 1

    
    def background(self):
        self.topFrame.reparentTo(base.a2dTopRight)
        self.topFrame.setBin('unsorted', 49)
        self.topFrame['sortOrder'] = -1

    
    def cleanup(self):
        self.text.destroy()
        self.bar.destroy()
        self.bgFrame.destroy()
        self.topFrame.destroy()
        self.ignoreAll()


