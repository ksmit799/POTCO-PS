# File: I (Python 2.4)

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.makeapirate import JewelryGlobals
from pirates.pirate import HumanDNA
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.inventory import ItemGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import Freebooter
from pirates.inventory import InventoryUIItem
from pirates.inventory import ItemConstants

class InventoryUIJewelryItem(InventoryUIItem.InventoryUIItem):
    
    def __init__(self, manager, itemTuple, imageScaleFactor = 1.0):
        InventoryUIItem.InventoryUIItem.__init__(self, manager, itemTuple, imageScaleFactor = imageScaleFactor)
        self.initialiseoptions(InventoryUIJewelryItem)
        self['relief'] = None
        jewelryGui = loader.loadModel('models/gui/gui_icons_jewelry')
        iconName = ItemGlobals.getIcon(itemTuple[1])
        self['image'] = jewelryGui.find('**/%s' % iconName)
        self['image_scale'] = 0.10000000000000001 * imageScaleFactor
        iconColorIndex = ItemGlobals.getColor(itemTuple[1])
        self.iconColor = ItemConstants.COLOR_VALUES[iconColorIndex]
        self.iconColor = (ItemConstants.COLOR_VALUES[iconColorIndex][0], ItemConstants.COLOR_VALUES[iconColorIndex][1], ItemConstants.COLOR_VALUES[iconColorIndex][2], 1.0)
        self['image_color'] = (self.iconColor[0], self.iconColor[1], self.iconColor[2], self.iconColor[3])
        self.helpFrame = None
        self.cm = CardMaker('itemCard')
        self.cm.setFrame(-0.29999999999999999, 0.29999999999999999, -0.089999999999999997, 0.089999999999999997)
        self.buffer = None
        self.lens = PerspectiveLens()
        self.lens.setNear(0.10000000000000001)
        self.lens.setAspectRatio(0.59999999999999998 / 0.17999999999999999)
        self.realItem = None
        self.itemCard = None
        self.portraitSceneGraph = NodePath('PortraitSceneGraph')
        detailGui = loader.loadModel('models/gui/gui_card_detail')
        self.bg = detailGui.find('**/color')
        self.bg.setScale(4)
        self.bg.setPos(0, 17, -6.2999999999999998)
        self.glow = detailGui.find('**/glow')
        self.glow.setScale(3)
        self.glow.setPos(0, 17, -6.2999999999999998)
        self.glow.setColor(1, 1, 1, 0.80000000000000004)
        self.setBin('gui-fixed', 1)
        self.accept('open_main_window', self.createBuffer)
        self.accept('aspectRatioChanged', self.createBuffer)
        self.accept('close_main_window', self.destroyBuffer)
        self.displayHuman = self.manager.getDisplayHuman()
        self.masterHuman = self.manager.getMasterHuman()

    
    def destroy(self):
        self.displayHuman = None
        self.masterHuman = None
        if self.helpFrame:
            self.helpFrame.destroy()
            self.helpFrame = None
        
        self.destroyBuffer()
        if self.itemCard:
            self.itemCard.removeNode()
        
        if self.realItem:
            self.realItem.removeNode()
        
        InventoryUIItem.InventoryUIItem.destroy(self)

    
    def getName(self):
        return PLocalizer.getItemName(self.itemTuple[1])

    
    def showDetails(self, cell, detailsPos, detailsHeight, event = None):
        self.notify.debug('Item showDetails')
        if self.manager.heldItem and self.manager.locked and cell.isEmpty() or not (self.itemTuple):
            self.notify.debug(' early exit')
            return None
        
        itemId = self.getId()
        self.helpFrame = DirectFrame(parent = self.manager, relief = None, state = DGG.DISABLED, sortOrder = 1)
        self.helpFrame.setBin('gui-popup', -5)
        detailGui = loader.loadModel('models/gui/gui_card_detail')
        topGui = loader.loadModel('models/gui/toplevel_gui')
        coinImage = topGui.find('**/treasure_w_coin*')
        halfWidth = 0.29999999999999999
        halfHeight = 0.20000000000000001
        basePosX = cell.getX(aspect2d)
        basePosZ = cell.getZ(aspect2d)
        cellSizeX = 0.0
        cellSizeZ = 0.0
        if cell:
            cellSizeX = cell.cellSizeX
            cellSizeZ = cell.cellSizeZ
        
        textScale = PiratesGuiGlobals.TextScaleMed
        titleScale = PiratesGuiGlobals.TextScaleTitleSmall
        if len(self.getName()) >= 30:
            titleNameScale = PiratesGuiGlobals.TextScaleLarge
        else:
            titleNameScale = PiratesGuiGlobals.TextScaleExtraLarge
        subtitleScale = PiratesGuiGlobals.TextScaleMed
        iconScalar = 1.5
        borderScaler = 0.25
        splitHeight = 0.01
        vMargin = 0.029999999999999999
        runningVertPosition = 0.29999999999999999
        runningSize = 0.0
        labels = []
        titleColor = PiratesGuiGlobals.TextFG6
        rarity = ItemGlobals.getRarity(itemId)
        rarityText = PLocalizer.getItemRarityName(rarity)
        typeText = PLocalizer.getJewelryTypeName(ItemGlobals.getType(itemId))
        if rarity == ItemGlobals.CRUDE:
            titleColor = PiratesGuiGlobals.TextFG24
        elif rarity == ItemGlobals.COMMON:
            titleColor = PiratesGuiGlobals.TextFG13
        elif rarity == ItemGlobals.RARE:
            titleColor = PiratesGuiGlobals.TextFG4
        elif rarity == ItemGlobals.FAMED:
            titleColor = PiratesGuiGlobals.TextFG5
        
        titleLabel = DirectLabel(parent = self, relief = None, text = self.getName(), text_scale = titleNameScale, text_fg = titleColor, text_shadow = PiratesGuiGlobals.TextShadow, text_align = TextNode.ACenter, pos = (0.0, 0.0, runningVertPosition), text_pos = (0.0, -textScale))
        self.bg.setColor(titleColor)
        tHeight = 0.070000000000000007
        titleLabel.setZ(runningVertPosition)
        runningVertPosition -= tHeight
        runningSize += tHeight
        labels.append(titleLabel)
        subtitleLabel = DirectLabel(parent = self, relief = None, text = '\x1slant\x1%s %s\x2' % (rarityText, typeText), text_scale = subtitleScale, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_align = TextNode.ACenter, pos = (0.0, 0.0, runningVertPosition), text_pos = (0.0, -textScale))
        subtHeight = 0.050000000000000003
        subtitleLabel.setZ(subtHeight * 0.5 + runningVertPosition)
        runningVertPosition -= subtHeight
        runningSize += subtHeight
        labels.append(subtitleLabel)
        gender = localAvatar.style.gender
        dna = HumanDNA.HumanDNA(gender)
        dna.copy(localAvatar.style)
        bodyShape = localAvatar.style.getBodyShape()
        bodyHeight = localAvatar.style.getBodyHeight()
        bodyOffset = 0.5
        browOffset = 0
        earOffset = 0
        noseOffset = 0
        mouthOffset = 0
        handOffset = 0
        if bodyShape == 0:
            bodyOffset = 0.5
            if gender == 'm':
                browOffset = 0.75
                earOffset = 0.65000000000000002
                noseOffset = 0.69999999999999996
                mouthOffset = 0.75
                handOffset = 0.40000000000000002
            elif gender == 'f':
                browOffset = 0.55000000000000004
                earOffset = 0.55000000000000004
                noseOffset = 0.45000000000000001
                mouthOffset = 0.65000000000000002
                handOffset = 0.29999999999999999
            
        elif bodyShape == 1:
            bodyOffset = 0.5
            if gender == 'm':
                browOffset = 0.20000000000000001
                earOffset = 0.20000000000000001
                noseOffset = 0.10000000000000001
                mouthOffset = 0.20000000000000001
                handOffset = 0.20000000000000001
            elif gender == 'f':
                browOffset = 0.5
                earOffset = 0.5
                noseOffset = 0.40000000000000002
                mouthOffset = 0.5
                handOffset = 0.20000000000000001
            
        elif bodyShape == 2:
            bodyOffset = 0.5
            if gender == 'm':
                browOffset = 0.10000000000000001
                earOffset = 0.10000000000000001
                noseOffset = -0.050000000000000003
                mouthOffset = 0.10000000000000001
                handOffset = 0.10000000000000001
            elif gender == 'f':
                browOffset = -0.10000000000000001
                earOffset = -0.10000000000000001
                noseOffset = -0.20000000000000001
                mouthOffset = -0.10000000000000001
                handOffset = -0.10000000000000001
            
        elif bodyShape == 3:
            bodyOffset = 0.5
            if gender == 'm':
                browOffset = 0.20000000000000001
                earOffset = 0.20000000000000001
                noseOffset = 0.050000000000000003
                mouthOffset = 0.20000000000000001
                handOffset = 0.20000000000000001
            elif gender == 'f':
                browOffset = -0.40000000000000002
                earOffset = -0.40000000000000002
                noseOffset = -0.45000000000000001
                mouthOffset = -0.29999999999999999
                handOffset = -0.20000000000000001
            
        elif bodyShape == 4:
            bodyOffset = 0.5
            if gender == 'm':
                browOffset = -0.20000000000000001
                earOffset = -0.20000000000000001
                noseOffset = -0.29999999999999999
                mouthOffset = -0.14999999999999999
                handOffset = -0.050000000000000003
            elif gender == 'f':
                browOffset = 0.10000000000000001
                earOffset = 0.10000000000000001
                noseOffset = 0.0
                mouthOffset = 0.10000000000000001
                handOffset = 0.0
            
        elif bodyShape == 5:
            bodyOffset = 0.5
            if gender == 'm':
                browOffset = 0.10000000000000001
                earOffset = 0.10000000000000001
                noseOffset = -0.050000000000000003
                mouthOffset = 0.10000000000000001
                handOffset = 0.10000000000000001
            elif gender == 'f':
                browOffset = -0.050000000000000003
                earOffset = -0.10000000000000001
                noseOffset = -0.14999999999999999
                mouthOffset = -0.050000000000000003
                handOffset = -0.10000000000000001
            
        elif bodyShape == 6:
            bodyOffset = 0.5
            if gender == 'm':
                browOffset = 0.10000000000000001
                earOffset = 0.10000000000000001
                noseOffset = -0.050000000000000003
                mouthOffset = 0.10000000000000001
                handOffset = 0.10000000000000001
            elif gender == 'f':
                browOffset = 0.40000000000000002
                earOffset = 0.40000000000000002
                noseOffset = 0.25
                mouthOffset = 0.40000000000000002
                handOffset = 0.10000000000000001
            
        elif bodyShape == 7:
            bodyOffset = 0.5
            if gender == 'm':
                browOffset = 0.10000000000000001
                earOffset = 0.10000000000000001
                noseOffset = -0.050000000000000003
                mouthOffset = 0.10000000000000001
                handOffset = 0.10000000000000001
            elif gender == 'f':
                browOffset = 0.0
                earOffset = -0.050000000000000003
                noseOffset = -0.10000000000000001
                mouthOffset = 0.0
                handOffset = -0.050000000000000003
            
        elif bodyShape == 8:
            bodyOffset = 0.5
            if gender == 'm':
                browOffset = -0.10000000000000001
                earOffset = -0.10000000000000001
                noseOffset = -0.20000000000000001
                mouthOffset = -0.050000000000000003
                handOffset = -0.050000000000000003
            elif gender == 'f':
                browOffset = -0.14999999999999999
                earOffset = -0.14999999999999999
                noseOffset = -0.25
                mouthOffset = -0.14999999999999999
                handOffset = -0.10000000000000001
            
        elif bodyShape == 9:
            bodyOffset = 0.5
            if gender == 'm':
                browOffset = -0.20000000000000001
                earOffset = -0.20000000000000001
                noseOffset = -0.29999999999999999
                mouthOffset = -0.10000000000000001
                handOffset = -0.050000000000000003
            elif gender == 'f':
                browOffset = -0.34999999999999998
                earOffset = -0.34999999999999998
                noseOffset = -0.45000000000000001
                mouthOffset = -0.34999999999999998
                handOffset = -0.20000000000000001
            
        
        m = Mat4(Mat4.identMat())
        itemType = ItemGlobals.getType(itemId)
        if itemType == ItemGlobals.BROW:
            jewelType = JewelryGlobals.LBROW
        elif itemType == ItemGlobals.EAR:
            jewelType = JewelryGlobals.LEAR
        elif itemType == ItemGlobals.NOSE:
            jewelType = JewelryGlobals.NOSE
        elif itemType == ItemGlobals.MOUTH:
            jewelType = JewelryGlobals.MOUTH
        elif itemType == ItemGlobals.HAND:
            jewelType = JewelryGlobals.LHAND
        
        primaryColor = ItemGlobals.getPrimaryColor(itemId)
        secondaryColor = ItemGlobals.getSecondaryColor(itemId)
        if localAvatar.style.gender == 'm':
            maleModelId = ItemGlobals.getMaleModelId(itemId)
            if maleModelId:
                jewelId = maleModelId
                dna = HumanDNA.HumanDNA(localAvatar.style.gender)
                dna.copy(localAvatar.style)
                gender = 'm'
            else:
                jewelId = ItemGlobals.getFemaleModelId(itemId)
                dna = HumanDNA.HumanDNA('f')
                gender = 'f'
        else:
            femaleModelId = ItemGlobals.getFemaleModelId(itemId)
            if femaleModelId:
                jewelId = femaleModelId
                dna = HumanDNA.HumanDNA(localAvatar.style.gender)
                dna.copy(localAvatar.style)
                gender = 'f'
            else:
                jewelId = ItemGlobals.getMaleModelId(itemId)
                dna = HumanDNA.HumanDNA('m')
                gender = 'm'
        if jewelType == JewelryGlobals.LBROW:
            dna.setJewelryZone3(jewelId, primaryColor, secondaryColor)
        elif jewelType == JewelryGlobals.LEAR:
            dna.setJewelryZone1(jewelId, primaryColor, secondaryColor)
        elif jewelType == JewelryGlobals.NOSE:
            dna.setJewelryZone5(jewelId, primaryColor, secondaryColor)
        elif jewelType == JewelryGlobals.MOUTH:
            dna.setJewelryZone6(jewelId, primaryColor, secondaryColor)
        elif jewelType == JewelryGlobals.LHAND:
            dna.setJewelryZone7(jewelId, primaryColor, secondaryColor)
        
        dna.setClothesHat(0, 0)
        self.displayHuman.setDNAString(dna)
        self.displayHuman.generateHuman(gender, self.masterHuman)
        self.displayHuman.stopBlink()
        self.displayHuman.pose('idle', 1)
        lodNode = self.displayHuman.find('**/+LODNode').node()
        lodNode.forceSwitch(lodNode.getHighestSwitch())
        if jewelType == JewelryGlobals.LBROW:
            self.displayHuman.getLOD('2000').getChild(0).node().findJoint('trs_right_eyebrow').getNetTransform(m)
            rightEyeHeight = TransformState.makeMat(m).getPos().getZ()
            if gender == 'f':
                offsetX = 0.40000000000000002
                offsetZ = -rightEyeHeight + browOffset - bodyHeight * 1.0
                offsetY = 0.25 + bodyOffset
            else:
                offsetX = 0.29999999999999999
                offsetZ = -rightEyeHeight * 0.98999999999999999 + browOffset - bodyHeight * 1.0
                offsetY = 0.14999999999999999 + bodyOffset
            offsetH = -240
        elif jewelType == JewelryGlobals.LEAR:
            self.displayHuman.getLOD('2000').getChild(0).node().findJoint('def_trs_left_ear').getNetTransform(m)
            leftEarHeight = TransformState.makeMat(m).getPos().getZ()
            if gender == 'f':
                offsetZ = -leftEarHeight + earOffset - bodyHeight * 1.0
                offsetY = 0.40000000000000002 + bodyOffset
                offsetX = 0.14999999999999999
            else:
                offsetZ = -leftEarHeight * 0.98999999999999999 + earOffset - bodyHeight * 1.0
                offsetY = 0.29999999999999999 + bodyOffset
                offsetX = 0.040000000000000001
            offsetH = -250
        elif jewelType == JewelryGlobals.NOSE:
            self.displayHuman.getLOD('2000').getChild(0).node().findJoint('def_trs_mid_nose_bot').getNetTransform(m)
            noseHeight = TransformState.makeMat(m).getPos().getZ()
            if gender == 'f':
                offsetZ = -noseHeight + 0.089999999999999997 + noseOffset - bodyHeight * 0.80000000000000004
                offsetY = 0.45000000000000001 + bodyOffset
            else:
                offsetZ = -noseHeight + 0.10000000000000001 + noseOffset - bodyHeight * 0.80000000000000004
                offsetY = 0.40000000000000002 + bodyOffset
            offsetX = 0.059999999999999998
            offsetH = 180
        elif jewelType == JewelryGlobals.MOUTH:
            self.displayHuman.getLOD('2000').getChild(0).node().findJoint('trs_lips_top').getNetTransform(m)
            mouthHeight = TransformState.makeMat(m).getPos().getZ()
            offsetZ = -mouthHeight + 0.02 + mouthOffset - bodyHeight * 1.1000000000000001
            offsetY = 0.59999999999999998 + bodyOffset
            offsetX = 0.080000000000000002
            offsetH = 180
        elif jewelType == JewelryGlobals.LHAND:
            self.displayHuman.getLOD('2000').getChild(0).node().findJoint('def_left_index01').getNetTransform(m)
            leftIndexHeight = TransformState.makeMat(m).getPos().getZ()
            if gender == 'f':
                offsetZ = -leftIndexHeight + 0.050000000000000003 + handOffset - bodyHeight * 0.5
                offsetX = -0.69999999999999996
                offsetY = 1.25 + bodyOffset
            else:
                offsetZ = -leftIndexHeight + handOffset - bodyHeight * 0.5
                if bodyShape == 4:
                    offsetX = -1.0
                    offsetY = 1.75 + bodyOffset
                elif bodyShape == 3:
                    offsetX = -0.69999999999999996
                    offsetY = 1.25 + bodyOffset
                elif bodyShape == 1:
                    offsetX = -0.69999999999999996
                    offsetY = 1.25 + bodyOffset
                elif bodyShape == 0:
                    offsetX = -0.69999999999999996
                    offsetY = 1.25 + bodyOffset
                else:
                    offsetX = -0.80000000000000004
                    offsetY = 1.25 + bodyOffset
            offsetH = 160
        else:
            offsetZ = 0.0
            offsetY = 0.0
            offsetX = 0.0
            offsetH = 0
        self.displayHuman.setY(offsetY)
        self.displayHuman.setZ(offsetZ)
        self.displayHuman.setX(offsetX)
        self.displayHuman.setH(offsetH)
        self.displayHuman.reparentTo(self.portraitSceneGraph)
        iHeight = 0.17999999999999999
        self.createBuffer()
        self.itemCard.setZ(runningVertPosition - 0.059999999999999998)
        runningVertPosition -= iHeight
        runningSize += iHeight
        labels.append(self.itemCard)
        itemCost = int(ItemGlobals.getGoldCost(itemId))
        if self.cell and self.cell.container:
            itemCost = int(itemCost * self.cell.container.getItemPriceMult())
        
        goldLabel = DirectLabel(parent = self, relief = None, image = coinImage, image_scale = 0.12, image_pos = Vec3(0.025000000000000001, 0, -0.02), text = str(itemCost), text_scale = subtitleScale, text_align = TextNode.ARight, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, pos = (halfWidth - 0.050000000000000003, 0.0, runningVertPosition + 0.080000000000000002), text_pos = (0.0, -textScale))
        labels.append(goldLabel)
        descriptionLabel = DirectLabel(parent = self, relief = None, text = PLocalizer.getItemFlavorText(itemId), text_scale = textScale, text_wordwrap = halfWidth * 2.0 * (0.94999999999999996 / textScale), text_fg = PiratesGuiGlobals.TextFG0, text_align = TextNode.ALeft, pos = (-halfWidth + textScale * 0.5, 0.0, runningVertPosition), text_pos = (0.0, -textScale))
        dHeight = descriptionLabel.getHeight() + 0.02
        runningVertPosition -= dHeight
        runningSize += dHeight
        labels.append(descriptionLabel)
        if not Freebooter.getPaidStatus(localAvatar.getDoId()):
            if rarity != ItemGlobals.CRUDE:
                unlimitedLabel = DirectLabel(parent = self, relief = None, text = PLocalizer.UnlimitedAccessRequirement, text_scale = textScale, text_wordwrap = halfWidth * 2.0 * (1.5 / titleScale), text_fg = PiratesGuiGlobals.TextFG6, text_shadow = PiratesGuiGlobals.TextShadow, text_align = TextNode.ACenter, pos = (0.0, 0.0, runningVertPosition), text_pos = (0.0, -textScale))
                uHeight = unlimitedLabel.getHeight()
                runningVertPosition -= uHeight
                runningSize += uHeight
                labels.append(unlimitedLabel)
            
        
        runningVertPosition -= 0.02
        runningSize += 0.02
        panels = self.helpFrame.attachNewNode('panels')
        topPanel = panels.attachNewNode('middlePanel')
        detailGui.find('**/top_panel').copyTo(topPanel)
        topPanel.setScale(0.080000000000000002)
        topPanel.reparentTo(self.helpFrame)
        middlePanel = panels.attachNewNode('middlePanel')
        detailGui.find('**/middle_panel').copyTo(middlePanel)
        middlePanel.setScale(0.080000000000000002)
        middlePanel.reparentTo(self.helpFrame)
        placement = 0
        i = 0
        heightMax = -0.080000000000000002
        currentHeight = runningVertPosition
        if detailsHeight:
            currentHeight = -detailsHeight
        
        while currentHeight < heightMax:
            middlePanel = panels.attachNewNode('middlePanel%s' % 1)
            detailGui.find('**/middle_panel').copyTo(middlePanel)
            middlePanel.setScale(0.080000000000000002)
            middlePanel.reparentTo(self.helpFrame)
            if currentHeight + 0.20000000000000001 >= heightMax:
                difference = heightMax - currentHeight
                placement += (0.16800000000000001 / 0.20000000000000001) * difference
                currentHeight += difference
            else:
                placement += 0.16800000000000001
                currentHeight += 0.20000000000000001
            middlePanel.setZ(-placement)
            i += 1
        bottomPanel = panels.attachNewNode('bottomPanel')
        detailGui.find('**/bottom_panel').copyTo(bottomPanel)
        bottomPanel.setScale(0.080000000000000002)
        bottomPanel.setZ(-placement)
        bottomPanel.reparentTo(self.helpFrame)
        colorPanel = self.helpFrame.attachNewNode('colorPanel')
        detailGui.find('**/color').copyTo(colorPanel)
        colorPanel.setScale(0.080000000000000002)
        colorPanel.setColor(titleColor)
        colorPanel.reparentTo(self.helpFrame)
        lineBreakTopPanel = panels.attachNewNode('lineBreakTopPanel')
        detailGui.find('**/line_break_top').copyTo(lineBreakTopPanel)
        lineBreakTopPanel.setScale(0.080000000000000002, 0.080000000000000002, 0.070000000000000007)
        lineBreakTopPanel.setZ(0.0080000000000000002)
        lineBreakTopPanel.reparentTo(self.helpFrame)
        panels.flattenStrong()
        self.helpFrame['frameSize'] = (-halfWidth, halfWidth, -(runningSize + vMargin), vMargin)
        totalHeight = self.helpFrame.getHeight() - 0.10000000000000001
        for label in labels:
            label.reparentTo(self.helpFrame)
        
        if basePosX > 0.0:
            newPosX = basePosX - halfWidth + cellSizeX * 0.45000000000000001
        else:
            newPosX = basePosX + halfWidth + cellSizeX * 0.45000000000000001
        if basePosZ > 0.0:
            newPosZ = basePosZ + cellSizeZ * 0.45000000000000001
        else:
            newPosZ = basePosZ + totalHeight - cellSizeZ * 0.75
        if detailsPos:
            (newPosX, newPosZ) = detailsPos
        
        self.helpFrame.setPos(newPosX, 0, newPosZ)

    
    def hideDetails(self, event = None):
        InventoryUIItem.InventoryUIItem.hideDetails(self, event)
        if self.helpFrame:
            self.helpFrame.destroy()
            self.helpFrame = None
        
        self.destroyBuffer()
        if self.realItem:
            self.realItem.removeNode()
        
        if self.displayHuman:
            self.displayHuman.detachNode()
        

    
    def createBuffer(self):
        self.destroyBuffer()
        self.buffer = base.win.makeTextureBuffer('par', 256, 256)
        self.buffer.setOneShot(True)
        self.cam = base.makeCamera(win = self.buffer, scene = self.portraitSceneGraph, clearColor = Vec4(1), lens = self.lens)
        self.cam.node().getDisplayRegion(0).setIncompleteRender(False)
        self.cam.reparentTo(self.portraitSceneGraph)
        self.bg.reparentTo(self.cam)
        self.glow.reparentTo(self.cam)
        if self.itemCard:
            self.itemCard.removeNode()
        
        tex = self.buffer.getTexture()
        self.itemCard = NodePath(self.cm.generate())
        self.itemCard.setTexture(tex, 1)
        if self.helpFrame:
            self.itemCard.reparentTo(self.helpFrame)
        

    
    def destroyBuffer(self):
        if self.buffer:
            base.graphicsEngine.removeWindow(self.buffer)
            self.buffer = None
            self.bg.detachNode()
            self.glow.detachNode()
            self.cam.removeNode()
            self.cam = None
        


