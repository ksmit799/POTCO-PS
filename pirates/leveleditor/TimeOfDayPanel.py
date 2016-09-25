# File: T (Python 2.4)

import pprint
from direct.showbase.TkGlobal import *
from direct.tkwidgets.AppShell import *
from direct.tkwidgets import Dial
from direct.tkwidgets import Floater
from direct.tkwidgets import Slider
from direct.tkwidgets import VectorWidgets
from direct.tkwidgets import Valuator
import tkColorChooser
from direct.directtools.DirectUtil import getTkColorString
import Pmw
from direct.gui import DirectGuiGlobals as DGG
from pirates.piratesbase import PLocalizer as PL
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import TODGlobals
from pandac.PandaModules import *
from Tkinter import *

class TimeOfDayPanel(AppShell):
    appname = 'Time Of Day Panel'
    appversion = '1.1'
    copyright = 'Copyright 2006 Walt Disney Interactive Media Group.' + ' All Rights Reserved'
    contactname = 'Pirates Team - DIMG'
    contactphone = ''
    contactemail = ''
    frameWidth = 690
    frameHeight = 800
    usecommandarea = 0
    usestatusarea = 0
    
    def __init__(self, todMgr, parent = None, **kw):
        self.todMgr = todMgr
        self.editor = None
        self.selectedCycleDuration = -1
        self.uncommitedColor = Vec4(255.0, 0.0, 0.0, 255.0)
        self.changedColor = Vec4(0.0, 255.0, 255.0, 255.0)
        self.defaultColor = Vec4(255.0, 255.0, 255.0, 255.0)
        self.changesEnabled = 0
        self.holdFogColor = None
        self.holdFogExp = None
        self.holdLinearRanges = None
        self.holdAmbientColor = None
        self.holdDirectionColor = None
        self.holdBackColor = None
        self.holdSunDirection = None
        self.accept('timeOfDayChange', self.updateTod)
        self.accept('environmentChanged', self.updateEnv)
        self.accept('TOD_Setting_Change', self.checkButtonsForChange)
        self.accept('TOD_CYCLE_CHANGE', self.updateCycleType)
        DGG.INITOPT = Pmw.INITOPT
        optiondefs = (('title', self.appname, None),)
        self.defineoptions(kw, optiondefs)
        AppShell.__init__(self, parent)
        self.initialiseoptions(TimeOfDayPanel)

    
    def setEditor(self, editor):
        self.editor = editor
        self.checkButtonsForChange()

    
    def onDestroy(self, event):
        if self.editor:
            self.editor.TODPanel = None
            self.editor.TODPanelLoaded = False
        
        self.ignoreAll()
        AppShell.onDestroy(self, event)

    
    def getTkColorFromVec4(self, v, mult = 255):
        return getTkColorString([
            int(v[0] * mult),
            int(v[1] * mult),
            int(v[2] * mult)])

    
    def createInterface(self):
        interior = self.interior()
        todFrame = Frame(interior, borderwidth = 4, relief = 'raised')
        todButtonFrame = Frame(todFrame, borderwidth = 2, relief = 'sunken')
        printButton = Button(todButtonFrame, text = 'PRINT', command = self.printSettings)
        texToggle = Button(todButtonFrame, text = 'Toggle Textures', command = base.toggleTexture)
        saveChanges = Button(todButtonFrame, text = 'Insert Change', command = self.saveChanges)
        self.saveChanges = saveChanges
        self.saveChanges['state'] = 'disabled'
        removeChanges = Button(todButtonFrame, text = 'Clear to Environment Setting', command = self.clearChanges)
        self.removeChanges = removeChanges
        self.removeChanges['state'] = 'disabled'
        undoChanges = Button(todButtonFrame, text = 'Undo Change', command = self.undoChanges)
        self.undoChanges = undoChanges
        self.environmetVar = IntVar()
        self.environmetVar.set(self.todMgr.environment)
        environmentFrame = Frame(todFrame, borderwidth = 2, relief = 'sunken')
        for environmentId in TODGlobals.ENVIRONMENT_NAMES:
            name = TODGlobals.ENVIRONMENT_NAMES[environmentId]
            button = Radiobutton(environmentFrame, text = name, variable = self.environmetVar, value = environmentId, command = self.changeEnvironment)
            button.pack(side = LEFT, fill = X, expand = 0)
        
        todCycleTypeFrame = Frame(todFrame, borderwidth = 2, relief = 'sunken')
        self.cycleTypeVar = IntVar()
        self.cycleTypeVar.set(self.todMgr.cycleType)
        self.cycleTypeDict = { }
        for idKey in TODGlobals.CYCLE_NAMES:
            name = TODGlobals.CYCLE_NAMES[idKey]
            self.cycleTypeDict[idKey] = Radiobutton(todCycleTypeFrame, text = name, variable = self.cycleTypeVar, value = idKey, command = self.commandChangeTodCycle)
        
        for buttonKey in self.cycleTypeDict:
            button = self.cycleTypeDict[buttonKey]
            button.pack(side = LEFT, fill = X, expand = 0)
        
        self.todStateFrame = Frame(todFrame, borderwidth = 2, relief = 'sunken')
        self.todVar = IntVar()
        self.todVar.set(self.todMgr.currentState)
        todCycleId = self.todMgr.cycleType
        todCycleList = TODGlobals.CycleStateTimeList[todCycleId]
        self.todButtonDict = { }
        self.makeTODButtons()
        for buttonKey in self.todButtonDict:
            button = self.todButtonDict[buttonKey]
            button.pack(side = LEFT, fill = X, expand = 0)
        
        todCycleFrame = Frame(todFrame, borderwidth = 2, relief = 'sunken')
        self.cycleDurationVar = IntVar()
        todCycle0 = Radiobutton(todCycleFrame, text = 'Off(edit)', variable = self.cycleDurationVar, value = 0, command = self.commandChangeTodSpeed)
        todCycle1 = Radiobutton(todCycleFrame, text = '30 sec', variable = self.cycleDurationVar, value = 120, command = self.commandChangeTodSpeed)
        todCycle2 = Radiobutton(todCycleFrame, text = '2 min', variable = self.cycleDurationVar, value = 30, command = self.commandChangeTodSpeed)
        todCycle3 = Radiobutton(todCycleFrame, text = '10 min', variable = self.cycleDurationVar, value = 6, command = self.commandChangeTodSpeed)
        todCycle4 = Radiobutton(todCycleFrame, text = '1 hour', variable = self.cycleDurationVar, value = 1, command = self.commandChangeTodSpeed)
        self.cycleDurationVar.set(int(self.todMgr.cycleSpeed))
        envInfo = Label(todFrame, text = 'Environment- -DataOnly- is the working set', borderwidth = 2, anchor = W, font = ('MS Sans Serif', 9))
        todInfo = Label(todFrame, text = 'TOD- White is Default, Blue is Saved, Red is changed but not saved', borderwidth = 2, anchor = W, font = ('MS Sans Serif', 9))
        cycleInfo = Label(todFrame, text = 'Cycle', borderwidth = 2, anchor = W, font = ('MS Sans Serif', 9))
        durationInfo = Label(todFrame, text = 'Duration- Select Off to Edit', borderwidth = 2, anchor = W, font = ('MS Sans Serif', 9))
        todCycle0.pack(side = LEFT, fill = X, expand = 0)
        todCycle1.pack(side = LEFT, fill = X, expand = 0)
        todCycle2.pack(side = LEFT, fill = X, expand = 0)
        todCycle3.pack(side = LEFT, fill = X, expand = 0)
        todCycle4.pack(side = LEFT, fill = X, expand = 0)
        todButtonFrame.pack(side = TOP, fill = X, expand = 0)
        printButton.pack(fill = X, expand = 0)
        texToggle.pack(fill = X, expand = 0)
        saveChanges.pack(fill = X, expand = 0)
        undoChanges.pack(fill = X, expand = 0)
        removeChanges.pack(fill = X, expand = 0)
        envInfo.pack(fill = X, expand = 0)
        environmentFrame.pack(fill = X, expand = 0)
        cycleInfo.pack(fill = X, expand = 0)
        todCycleTypeFrame.pack(fill = X, expand = 0)
        todInfo.pack(side = TOP, fill = X, expand = 0)
        self.todStateFrame.pack(fill = X, expand = 0)
        durationInfo.pack(side = TOP, fill = X, expand = 0)
        todCycleFrame.pack(fill = X, expand = 0)
        todFrame.pack(fill = X, expand = 0, pady = 4)
        initialFogColor = self.todMgr.fog.getColor()
        controlFrame = Frame(interior, borderwidth = 2, relief = 'raised')
        otherFrame = Frame(controlFrame, borderwidth = 2, relief = 'raised')
        skyFrame = Frame(interior, borderwidth = 2, relief = 'raised')
        skyLabel = Label(skyFrame, text = 'Select Sky', font = ('MS Sans Serif', 11))
        self.todSkyTypeVar = IntVar()
        self.todSkyTypeVar.set(int(self.todMgr.skyGroup.lastSky))
        skyListFrame = Frame(interior, borderwidth = 2, relief = 'raised')
        for key in TODGlobals.SKY_NAMES:
            name = TODGlobals.SKY_NAMES[key]
            skyTypeButton = Radiobutton(skyListFrame, text = name, variable = self.todSkyTypeVar, value = key, command = self.changeSky)
            skyTypeButton.pack(side = LEFT, fill = X, expand = 0)
        
        otherFrame.pack(side = RIGHT, fill = NONE, expand = 0, pady = 4)
        fogFrame = Frame(otherFrame, borderwidth = 2, relief = 'raised')
        fogLabelFrame = Frame(fogFrame, borderwidth = 2, relief = 'sunken')
        fogControlFrame = Frame(fogFrame, borderwidth = 2, relief = 'sunken')
        self.fogTopLabel = Label(fogLabelFrame, text = 'FOG ', font = ('MS Sans Serif', 11))
        fogTypeFrame = Frame(fogControlFrame, borderwidth = 2, relief = 'raised')
        self.fogTypeVar = IntVar()
        self.fogTypeVar.set(self.todMgr.fogType)
        self.fogOff = Radiobutton(fogTypeFrame, text = 'Off', variable = self.fogTypeVar, value = TODGlobals.FOG_OFF, command = self.setFogType)
        self.fogExp = Radiobutton(fogTypeFrame, text = 'Exponent', variable = self.fogTypeVar, value = TODGlobals.FOG_EXP, command = self.setFogType)
        self.fogLinear = Radiobutton(fogTypeFrame, text = 'Linear', variable = self.fogTypeVar, value = TODGlobals.FOG_LINEAR, command = self.setFogType)
        self.fogLabel = Label(fogLabelFrame, text = '\n ', font = ('MS Sans Serif', 11))
        self.fogLabel['bg'] = self.getTkColorFromVec4(initialFogColor)
        self.fogColor = Valuator.ValuatorGroup(parent = fogControlFrame, dim = 3, labels = [
            'R',
            'G',
            'B'], value = [
            int(initialFogColor[0] * 1.0),
            int(initialFogColor[1] * 1.0),
            int(initialFogColor[2] * 1.0)], type = 'slider', valuator_style = 'mini', valuator_min = 0, valuator_max = 1.0, valuator_resolution = 0.01)
        self.fogColor['command'] = self.setFogColorVec
        
        def popupFogColorPicker():
            baseColor = self.todMgr.getFogColor()
            initColor = self.clipLightValue(baseColor * 255.0, 255.0)
            color = tkColorChooser.askcolor(parent = interior, initialcolor = (initColor[0], initColor[1], initColor[2]))
            if color[0] is not None:
                self.fogColor.set((round(color[0][0] / 255.0, 2), round(color[0][1] / 255.0, 2), round(color[0][2] / 255.0, 2)))
            

        pButton = Button(fogLabelFrame, text = 'Popup Color Picker', command = popupFogColorPicker)
        initialRange = self.todMgr.fog.getExpDensity()
        self.fogRangeFrame = Frame(fogControlFrame)
        self.fogRange = Valuator.ValuatorGroup(parent = self.fogRangeFrame, dim = 1, labels = [
            'Range'], value = [
            initialRange], type = 'slider', valuator_style = 'mini', min = 0.0, max = 0.01, numDigits = 6, resolution = 9.9999999999999995e-007)
        self.fogRange['command'] = self.setFogRangeVec
        initialOnSet = self.todMgr.linearFog.getLinearOnsetPoint()
        initialPeak = self.todMgr.linearFog.getLinearOpaquePoint()
        self.fogLinearRange = Valuator.ValuatorGroup(parent = self.fogRangeFrame, dim = 2, labels = [
            'OnSet',
            'Peak'], value = [
            initialOnSet[1],
            initialPeak[1]], type = 'slider', valuator_style = 'mini', min = 0.0, max = 1000.0, numDigits = 0, resolution = 1.0)
        self.fogLinearRange['command'] = self.setFogLinearRange
        initialSunDirection = self.todMgr.skyGroup.getSunTrueAngle()
        sunFrame = Frame(otherFrame, borderwidth = 2, relief = 'raised')
        self.sunDirectionLabel = Label(sunFrame, text = 'Sun Direction', font = ('MS Sans Serif', 11))
        self.sunDirection = Valuator.ValuatorGroup(parent = sunFrame, dim = 3, labels = [
            'Heading (Sunrise Direction)',
            'Pitch (Tilt)',
            'Roll (Rise and Set)'], value = [
            int(initialSunDirection[0] * 360),
            int(initialSunDirection[1] * 360),
            int(initialSunDirection[2] * 360)], type = 'slider', valuator_style = 'mini', valuator_min = 0, valuator_max = 360, valuator_resolution = 1)
        self.sunDirection['command'] = self.setSunDirection
        
        def pointSunDown():
            self.sunDirection.set((0, 0, 270))

        
        def pointSunUp():
            self.sunDirection.set((0, 0, 90))

        sunDown = Button(sunFrame, text = 'Sun at Top', command = pointSunDown)
        sunUp = Button(sunFrame, text = 'Sun at Bottom', command = pointSunUp)
        self.sunDirectionLabel.pack(side = TOP, fill = X, expand = 0, pady = 4)
        self.sunDirection.pack(side = TOP, fill = X, expand = 0, pady = 4)
        sunDown.pack(side = TOP, fill = X, expand = 0, pady = 4)
        sunUp.pack(side = TOP, fill = X, expand = 0, pady = 4)
        controlFrame.pack(side = TOP, fill = X, expand = 0, pady = 4)
        skyFrame.pack(side = TOP, fill = X, expand = 0, pady = 4)
        skyLabel.pack(side = TOP, fill = X, expand = 0)
        skyListFrame.pack(side = TOP, fill = X, expand = 0)
        fogLabelFrame.pack(side = LEFT, fill = X, expand = 0)
        fogControlFrame.pack(side = RIGHT, fill = X, expand = 1)
        self.fogTopLabel.pack(side = TOP, fill = X, expand = 1)
        fogTypeFrame.pack(side = TOP, fill = X, expand = 1)
        self.fogOff.pack(side = RIGHT, fill = X, expand = 1)
        self.fogExp.pack(side = RIGHT, fill = X, expand = 1)
        self.fogLinear.pack(side = RIGHT, fill = X, expand = 1)
        self.fogLabel.pack(side = TOP, fill = X, expand = 1)
        pButton.pack(side = BOTTOM, fill = X, expand = 0)
        self.fogColor.pack(fill = X, expand = 0)
        self.fogRangeFrame.pack(fill = X, expand = 0)
        self.fogRange.pack(fill = X, expand = 0)
        fogFrame.pack(side = TOP, fill = X, expand = 0, pady = 4)
        sunFrame.pack(side = TOP, fill = X, expand = 0, pady = 4)
        initialAmbientColor = self.todMgr.alight.node().getColor()
        lightingFrame = Frame(controlFrame, borderwidth = 2, relief = 'raised')
        ambientFrame = Frame(lightingFrame, borderwidth = 2, relief = 'raised')
        ambientControlFrame = Frame(ambientFrame, borderwidth = 2, relief = 'sunken')
        ambientLabelFrame = Frame(ambientFrame, borderwidth = 2, relief = 'sunken')
        self.ambientLabel = Label(ambientLabelFrame, text = '\n ', font = ('MS Sans Serif', 11))
        self.ambientLabel['bg'] = self.getTkColorFromVec4(self.clipLightValue(initialAmbientColor * 1.0, 1.0))
        self.ambientSwitchVar = IntVar()
        self.ambientSwitch = Checkbutton(ambientLabelFrame, text = 'Fill Light', variable = self.ambientSwitchVar, command = self.switchAmbient)
        self.ambientColor = Valuator.ValuatorGroup(parent = ambientControlFrame, dim = 3, labels = [
            'R',
            'G',
            'B'], value = [
            int(initialAmbientColor[0] * 1.0),
            int(initialAmbientColor[1] * 1.0),
            int(initialAmbientColor[2] * 1.0)], type = 'slider', valuator_style = 'mini', valuator_min = 0, valuator_max = 1.0, valuator_resolution = 0.01)
        self.ambientColor['command'] = self.setAmbientColorVec
        
        def popupAmbientColorPicker():
            baseColor = self.todMgr.getFillLightColor()
            initColor = self.clipLightValue(baseColor * 255.0, 255.0)
            color = tkColorChooser.askcolor(parent = interior, initialcolor = (initColor[0], initColor[1], initColor[2]))
            if color[0] is not None:
                self.ambientColor.set((round(color[0][0] / 255.0, 2), round(color[0][1] / 255.0, 2), round(color[0][2] / 255.0, 2)))
            

        pButton = Button(ambientLabelFrame, text = 'Popup Color Picker', command = popupAmbientColorPicker)
        ambientLabelFrame.pack(side = LEFT, fill = X, expand = 0)
        ambientControlFrame.pack(side = RIGHT, fill = X, expand = 1)
        self.ambientSwitch.pack(side = TOP, fill = X, expand = 1)
        self.ambientLabel.pack(side = TOP, fill = X, expand = 1)
        pButton.pack(side = BOTTOM, fill = X, expand = 0)
        self.ambientColor.pack(fill = X, expand = 0)
        lightingFrame.pack(side = LEFT, fill = NONE, expand = 0, pady = 4)
        if self.todMgr.dlight:
            initialDirectionalColor = self.todMgr.getFrontLightColor()
        else:
            initialDirectionalColor = Vec4(0, 0, 0, 1)
        directionalFrame = Frame(lightingFrame, borderwidth = 2, relief = 'raised')
        directionalControlFrame = Frame(directionalFrame, borderwidth = 2, relief = 'sunken')
        directionalLabelFrame = Frame(directionalFrame, borderwidth = 2, relief = 'sunken')
        self.directionalLabel = Label(directionalLabelFrame, text = 'FRONT LIGHT\n ', font = ('MS Sans Serif', 11))
        self.directionalLabel['bg'] = self.getTkColorFromVec4(self.clipLightValue(initialDirectionalColor * 0.5, 1.0))
        self.frontSwitchVar = IntVar()
        self.frontSwitch = Checkbutton(directionalLabelFrame, text = 'Front Light', variable = self.frontSwitchVar, command = self.switchFront)
        self.directionalColor = Valuator.ValuatorGroup(parent = directionalControlFrame, dim = 3, labels = [
            'R',
            'G',
            'B'], value = [
            int(initialDirectionalColor[0] * 1.0),
            int(initialDirectionalColor[1] * 1.0),
            int(initialDirectionalColor[2] * 1.0)], type = 'slider', valuator_style = 'mini', valuator_min = 0, valuator_max = 2.0, valuator_resolution = 0.01)
        self.directionalColor['command'] = self.setDirectionalColorVec
        
        def popupDirectionalColorPicker():
            baseColor = self.todMgr.getFrontLightColor()
            initColor = self.clipLightValue(baseColor * 127.5, 255.0)
            color = tkColorChooser.askcolor(parent = interior, initialcolor = (initColor[0], initColor[1], initColor[2]))
            if color[0] is not None:
                self.directionalColor.set((round(color[0][0] / 127.5, 2), round(color[0][1] / 127.5, 2), round(color[0][2] / 127.5, 2)))
            

        pButton = Button(directionalLabelFrame, text = 'Popup Color Picker', command = popupDirectionalColorPicker)
        directionalLabelFrame.pack(side = LEFT, fill = X, expand = 0)
        directionalControlFrame.pack(side = RIGHT, fill = X, expand = 1)
        self.frontSwitch.pack(side = TOP, fill = X, expand = 1)
        self.directionalLabel.pack(side = TOP, fill = X, expand = 1)
        pButton.pack(side = BOTTOM, fill = X, expand = 0)
        self.directionalColor.pack(fill = X, expand = 0)
        if self.todMgr.shadowLight:
            initialBackLightColor = self.todMgr.getBackLightColor()
        else:
            initialBackLightColor = Vec4(0, 0, 0, 1)
        backLightFrame = Frame(lightingFrame, borderwidth = 2, relief = 'raised')
        backLightControlFrame = Frame(backLightFrame, borderwidth = 2, relief = 'sunken')
        backLightLabelFrame = Frame(backLightFrame, borderwidth = 2, relief = 'sunken')
        self.backLightLabel = Label(backLightLabelFrame, text = 'BACK LIGHT\n ', font = ('MS Sans Serif', 11))
        self.backLightLabel['bg'] = self.getTkColorFromVec4(self.clipLightValue(initialBackLightColor * 0.5, 1.0))
        self.backSwitchVar = IntVar()
        self.backSwitch = Checkbutton(backLightLabelFrame, text = 'Back Light', variable = self.backSwitchVar, command = self.switchBack)
        self.backLightColor = Valuator.ValuatorGroup(parent = backLightControlFrame, dim = 3, labels = [
            'R',
            'G',
            'B'], value = [
            int(initialBackLightColor[0] * 1.0),
            int(initialBackLightColor[1] * 1.0),
            int(initialBackLightColor[2] * 1.0)], type = 'slider', valuator_style = 'mini', valuator_min = 0, valuator_max = 2.0, valuator_resolution = 0.01)
        self.backLightColor['command'] = self.setBackColorVec
        
        def popupBackColorPicker():
            baseColor = self.todMgr.getBackLightColor()
            initColor = self.clipLightValue(baseColor * 127.5, 255.0)
            color = tkColorChooser.askcolor(parent = interior, initialcolor = (initColor[0], initColor[1], initColor[2]))
            if color[0] is not None:
                self.backLightColor.set((round(color[0][0] / 127.5, 2), round(color[0][1] / 127.5, 2), round(color[0][2] / 127.5, 2)))
            

        pButton = Button(backLightLabelFrame, text = 'Popup Color Picker', command = popupBackColorPicker)
        backLightLabelFrame.pack(side = LEFT, fill = X, expand = 0)
        backLightControlFrame.pack(side = RIGHT, fill = X, expand = 1)
        self.backSwitch.pack(side = TOP, fill = X, expand = 1)
        self.backLightLabel.pack(side = TOP, fill = X, expand = 1)
        pButton.pack(side = BOTTOM, fill = X, expand = 0)
        self.backLightColor.pack(fill = X, expand = 0)
        directionalFrame.pack(side = TOP, fill = X, expand = 0, pady = 4)
        ambientFrame.pack(side = TOP, fill = X, expand = 0, pady = 4)
        backLightFrame.pack(side = TOP, fill = X, expand = 0, pady = 4)
        self.postCreateInterface()

    
    def postCreateInterface(self):
        self.cycleDurationVar.set(int(self.todMgr.cycleSpeed))
        self.selectedCycleDuration = self.todMgr.cycleSpeed
        if self.todMgr.cycleDuration == 0:
            self.holdData()
        
        self.setEnableDisable()
        self.checkButtonsForChange()

    
    def makeTODButtons(self):
        for buttonKey in self.todButtonDict:
            button = self.todButtonDict[buttonKey]
            button.pack_forget()
        
        self.todButtonDict = { }
        todCycleId = self.todMgr.cycleType
        todCycleList = TODGlobals.CycleStateTimeList[todCycleId]
        for todCycleState in todCycleList:
            timeId = todCycleState[0]
            timeName = TODGlobals.StateDict[timeId]
            newButton = Radiobutton(self.todStateFrame, text = timeName, variable = self.todVar, value = timeId, command = self.commandChangeTod)
            self.todButtonDict[timeId] = newButton
            newButton.pack(side = LEFT, fill = X, expand = 0)
        

    
    def setEnableDisable(self):
        cycleDuration = self.todMgr.cycleSpeed
        if cycleDuration > 0.0 or self.todMgr.currentState != self.todVar.get():
            self.ambientLabel['text'] = 'DISABLED\n '
            self.directionalLabel['text'] = 'DISABLED\n '
            self.backLightLabel['text'] = 'DISABLED\n '
            self.fogLabel['text'] = 'DISABLED\n '
            self.saveChanges['state'] = 'disabled'
            self.changesEnabled = 0
            self.holdFogColor = None
            self.holdFogExp = None
            self.holdLinearRanges = None
            self.holdAmbientColor = None
            self.holdDirectionColor = None
            self.holdBackColor = None
        elif cycleDuration == -1.0:
            self.ambientLabel['text'] = '\n '
            self.directionalLabel['text'] = '\n '
            self.backLightLabel['text'] = '\n '
            self.fogLabel['text'] = 'DISABLED\n '
            self.saveChanges['state'] = 'disabled'
            self.changesEnabled = 0
            self.holdFogColor = None
            self.holdFogExp = None
            self.holdLinearRanges = None
            self.holdAmbientColor = None
            self.holdDirectionColor = None
            self.holdBackColor = None
        else:
            self.ambientLabel['text'] = '\n '
            self.directionalLabel['text'] = '\n '
            self.backLightLabel['text'] = '\n '
            self.fogLabel['text'] = '\n '
            self.changesEnabled = 1
        if self.selectedCycleDuration != 0 or self.holdFogColor == None:
            self.changesEnabled = 0
            self.saveChanges['state'] = 'disabled'
        
        if self.changesEnabled:
            self.frontSwitch['state'] = 'normal'
            self.ambientSwitch['state'] = 'normal'
            self.backSwitch['state'] = 'normal'
        else:
            self.frontSwitch['state'] = 'disabled'
            self.ambientSwitch['state'] = 'disabled'
            self.backSwitch['state'] = 'disabled'
        if self.todMgr.fogMask:
            self.fogTopLabel['text'] = 'FOG -hidden-'
        else:
            self.fogTopLabel['text'] = 'FOG'

    
    def checkButtonsForChange(self):
        changedColor = Vec4(0.0, 255.0, 255.0, 255.0)
        defaultColor = Vec4(255.0, 255.0, 255.0, 255.0)
        if self.editor:
            alteredTODs = self.todMgr.listAlteredTODs(TODGlobals.ENV_DATAFILE)
        else:
            alteredTODs = self.todMgr.listAlteredTODs(self.todMgr.environment)
        for key in self.todButtonDict:
            button = self.todButtonDict[key]
            text = TODGlobals.StateDict.get(key)
            if text:
                if text in alteredTODs:
                    button['bg'] = getTkColorString(self.changedColor)
                else:
                    button['bg'] = getTkColorString(self.defaultColor)
            text in alteredTODs
        
        frontSwitch = self.todMgr.lightSwitch[0]
        ambientSwitch = self.todMgr.lightSwitch[1]
        backSwitch = self.todMgr.lightSwitch[2]
        self.frontSwitchVar.set(frontSwitch)
        self.ambientSwitchVar.set(ambientSwitch)
        self.backSwitchVar.set(backSwitch)
        self.fogTypeVar.set(self.todMgr.fogType)
        self.todSkyTypeVar.set(int(self.todMgr.skyGroup.lastSky))
        alteredTODs = self.todMgr.listAlteredTODs(self.todMgr.environment)
        alteredTime = 0
        stateId = self.todMgr.currentState
        for entry in alteredTODs:
            if entry == stateId:
                alteredTime = 1
                continue
        
        if alteredTime or self.selectedCycleDuration == 0 or 1:
            self.removeChanges['state'] = 'normal'
        else:
            self.removeChanges['state'] = 'disabled'

    
    def updateTod(self, stateId, stateDuration, elapsedTime, transitionTime):
        self.todVar.set(stateId)
        self.holdData()
        self.setEnableDisable()
        self.checkButtonsForChange()
        self.repackFog()

    
    def holdData(self):
        holdChanges = self.changesEnabled
        self.changesEnabled = 1
        stateId = self.todMgr.currentState
        fogColor = TODGlobals.getTodEnvSetting(stateId, self.todMgr.environment, 'FogColor')
        fogRange = TODGlobals.getTodEnvSetting(stateId, self.todMgr.environment, 'FogExp')
        linearFogOnSet = self.todMgr.linearFog.getLinearOnsetPoint()
        linearFogPeak = self.todMgr.linearFog.getLinearOpaquePoint()
        ambientColor = TODGlobals.getTodEnvSetting(stateId, self.todMgr.environment, 'AmbientColor')
        self.fogColor.set((fogColor[0], fogColor[1], fogColor[2]))
        self.fogRange.set((fogRange,))
        self.ambientColor.set((ambientColor[0], ambientColor[1], ambientColor[2]))
        self.fogLinearRange.set((linearFogOnSet[1], linearFogPeak[1]))
        sunDirection = self.todMgr.skyGroup.boundSunAngle(TODGlobals.getTodEnvSetting(stateId, self.todMgr.environment, 'Direction'))
        self.sunDirection.set((sunDirection[0], sunDirection[1], sunDirection[2]))
        directionalColor = None
        if self.todMgr.dlight:
            directionalColor = TODGlobals.getTodEnvSetting(stateId, self.todMgr.environment, 'FrontColor')
            self.holdDirectionColor = directionalColor
            self.directionalColor.set((directionalColor[0], directionalColor[1], directionalColor[2]))
        
        backLightColor = None
        if self.todMgr.shadowLight:
            backLightColor = TODGlobals.getTodEnvSetting(stateId, self.todMgr.environment, 'BackColor')
            self.holdBackColor = backLightColor
            self.backLightColor.set((backLightColor[0], backLightColor[1], backLightColor[2]))
        
        if self.selectedCycleDuration == 0:
            pass
        1
        self.holdFogColor = fogColor
        self.holdFogExp = fogRange
        self.holdLinearRanges = (linearFogOnSet[1], linearFogPeak[1])
        self.holdAmbientColor = ambientColor
        self.holdDirectionColor = directionalColor
        self.holdBackColor = backLightColor
        self.holdSunDirection = sunDirection
        self.changesEnabled = holdChanges

    
    def updateEnv(self):
        self.environmetVar.set(self.todMgr.environment)

    
    def changeEnvironment(self):
        environmentId = self.environmetVar.get()
 