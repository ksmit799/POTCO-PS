# File: S (Python 2.4)

import os
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectButton import DirectButton
from pirates.piratesgui.PDialog import PDialog
from pirates.piratesgui import PiratesGuiGlobals
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PLocalizer
from direct.directnotify import DirectNotifyGlobal

class ScreenshotViewer:
    notify = DirectNotifyGlobal.directNotify.newCategory('ScreenshotViewer')
    
    def __init__(self):
        self.resetImages()
        imageFrame = PDialog(parent = aspect2dp, pos = (0, 0, 0.10000000000000001), image_scale = (1.3 * 4 / 3.0, 1, 1.3), fadeScreen = 0.84999999999999998, scale = 1.1000000000000001)
        imageFrame.hide()
        imX = 0.84999999999999998
        imY = imX * 3 / 4.0
        self.imageObj = OnscreenImage(parent = imageFrame, image = self.screens[0], scale = (imX, 1, imY), pos = (0, 0, -0.025000000000000001))
        self.imageLabel = DirectLabel(parent = imageFrame, relief = None, state = DGG.DISABLED, pos = (0, 0, -0.75), textMayChange = 1, text_fg = (0.59999999999999998, 0.59999999999999998, 0.59999999999999998, 1), text_scale = 0.040000000000000001)
        self.imageLabel.hide()
        topGui = loader.loadModel('models/gui/toplevel_gui')
        arrow = topGui.find('**/generic_arrow')
        buttons = loader.loadModel('models/gui/lookout_gui')
        closeButton = (buttons.find('**/lookout_close_window'), buttons.find('**/lookout_close_window_down'), buttons.find('**/lookout_close_window_over'))
        xs = 1.2
        self.nextButton = DirectButton(parent = imageFrame, relief = None, command = self.next, pos = (0.69999999999999996, 0, 0), image = arrow, image_scale = (-xs, xs, xs), sortOrder = -5)
        self.prevButton = DirectButton(parent = imageFrame, relief = None, command = self.prev, pos = (-0.69999999999999996, 0, 0), image = arrow, image_scale = xs, sortOrder = -5)
        self.closeButton = DirectButton(parent = imageFrame, relief = None, command = self.close, pos = (0.78000000000000003, 0, -0.5), image = closeButton, image_scale = 0.29999999999999999, text = PLocalizer.lClose, text_fg = PiratesGuiGlobals.TextFG1, text_scale = 0.050000000000000003, text_pos = (0, -0.10000000000000001), sortOrder = -5)
        self.showIval = Sequence(Func(imageFrame.show), Wait(1), Parallel(LerpPosInterval(self.closeButton, 0.20000000000000001, Vec3(0.78000000000000003, 0, -0.80000000000000004), Vec3(0.78000000000000003, 0, -0.5)), LerpPosInterval(self.nextButton, 0.20000000000000001, Vec3(1, 0, 0), Vec3(0.69999999999999996, 0, 0)), LerpPosInterval(self.prevButton, 0.20000000000000001, Vec3(-1, 0, 0), Vec3(-0.69999999999999996, 0, 0))), Func(self.imageLabel.show))
        self.imageFrame = imageFrame
        base.transitions.fadeScreen(0.84999999999999998)

    
    def destroy(self):
        self.imageFrame.destroy()

    
    def resetImages(self):
        filenames = os.listdir(os.curdir + '/' + PLocalizer.ScreenshotDir)
        self.screens = _[1]
        self.currentIndex = 0

    
    def resetButtons(self):
        self.closeButton.setPos(Vec3(0.78000000000000003, 0, -0.5))
        self.nextButton.setPos(Vec3(0.69999999999999996, 0, 0))
        self.prevButton.setPos(Vec3(-0.69999999999999996, 0, 0))

    
    def showImage(self, index):
        if index >= 0 and index < len(self.screens):
            self.imageFrame.show()
            self.imageObj.setImage(self.screens[index])
            pandafile = Filename(str(ExecutionEnvironment.getCwd()))
            winfile = pandafile.toOsSpecific()
            self.imageLabel['text'] = '%s:\n%s\n%s\n[%s/%s]' % (PLocalizer.ScreenshotLocation, winfile, self.screens[index], index + 1, len(self.screens))
            self.imageLabel['text_fg'] = (0.59999999999999998, 0.59999999999999998, 0.59999999999999998, 1)
            self.imageLabel['text_scale'] = 0.040000000000000001
        
        if len(self.screens) == 1:
            self.prevButton['state'] = DGG.DISABLED
            self.nextButton['state'] = DGG.DISABLED
        else:
            self.prevButton['state'] = DGG.NORMAL
            self.nextButton['state'] = DGG.NORMAL

    
    def next(self):
        self.currentIndex = (self.currentIndex + 1) % len(self.screens)
        
        try:
            self.showImage(self.currentIndex)
        except:
            self.notify.error('Bad image')


    
    def prev(self):
        self.currentIndex = (self.currentIndex - 1) % len(self.screens)
        
        try:
            self.showImage(self.currentIndex)
        except:
            self.notify.error('Bad Image')


    
    def close(self):
        self.imageFrame.hide()

    
    def show(self):
        self.resetImages()
        self.resetButtons()
        self.showImage(0)
        self.showIval.start()

    
    def toggleShow(self):
        if self.imageFrame.isHidden():
            self.show()
        else:
            self.close()


