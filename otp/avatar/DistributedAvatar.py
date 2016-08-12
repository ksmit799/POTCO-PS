# File: D (Python 2.4)

import time
import string
from pandac.PandaModules import *
from direct.distributed import DistributedNode
from direct.actor.DistributedActor import DistributedActor
from direct.task import Task
from direct.showbase import PythonUtil
from otp.nametag import Nametag
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPLocalizer
from otp.speedchat import SCDecoders
from otp.chat import ChatGarbler
from otp.chat import ChatManager
import random
from Avatar import Avatar
import AvatarDNA

class DistributedAvatar(DistributedActor, Avatar):
    HpTextGenerator = TextNode('HpTextGenerator')
    HpTextEnabled = 1
    ManagesNametagAmbientLightChanged = True
    
    def __init__(self, cr):
        
        try:
            return None
        except:
            self.DistributedAvatar_initialized = 1

        Avatar.__init__(self)
        DistributedActor.__init__(self, cr)
        self.hpText = None
        self.hp = None
        self.maxHp = None

    
    def disable(self):
        
        try:
            del self.DistributedAvatar_announced
        except:
            return None

        self.reparentTo(hidden)
        self.removeActive()
        self.disableBodyCollisions()
        self.hideHpText()
        self.hp = None
        self.ignore('nameTagShowAvId')
        self.ignore('nameTagShowName')
        DistributedActor.disable(self)

    
    def delete(self):
        
        try:
            pass
        except:
            self.DistributedAvatar_deleted = 1
            Avatar.delete(self)
            DistributedActor.delete(self)


    
    def generate(self):
        DistributedActor.generate(self)
        if not self.isLocal():
            self.addActive()
            self.considerUnderstandable()
        
        self.setParent(OTPGlobals.SPHidden)
        self.setTag('avatarDoId', str(self.doId))
        self.accept('nameTagShowAvId', self._DistributedAvatar__nameTagShowAvId)
        self.accept('nameTagShowName', self._DistributedAvatar__nameTagShowName)

    
    def announceGenerate(self):
        
        try:
            return None
        except:
            self.DistributedAvatar_announced = 1

        if not self.isLocal():
            self.initializeBodyCollisions('distAvatarCollNode-' + str(self.doId))
        
        DistributedActor.announceGenerate(self)

    
    def _DistributedAvatar__setTags(self, extra = None):
        if hasattr(base, 'idTags'):
            if base.idTags:
                self._DistributedAvatar__nameTagShowAvId()
            else:
                self._DistributedAvatar__nameTagShowName()
        

    
    def do_setParent(self, parentToken):
        if not self.isDisabled():
            if parentToken == OTPGlobals.SPHidden:
                self.nametag2dDist &= ~(Nametag.CName)
            else:
                self.nametag2dDist |= Nametag.CName
            self.nametag.getNametag2d().setContents(self.nametag2dContents & self.nametag2dDist)
            DistributedActor.do_setParent(self, parentToken)
            self._DistributedAvatar__setTags()
        

    
    def toonUp(self, hpGained):
        if self.hp == None or hpGained < 0:
            return None
        
        oldHp = self.hp
        if self.hp + hpGained <= 0:
            self.hp += hpGained
        else:
            self.hp = min(max(self.hp, 0) + hpGained, self.maxHp)
        hpGained = self.hp - max(oldHp, 0)
        if hpGained > 0:
            self.showHpText(hpGained)
            self.hpChange(quietly = 0)
        

    
    def takeDamage(self, hpLost, bonus = 0):
        if self.hp == None or hpLost < 0:
            return None
        
        oldHp = self.hp
        self.hp = max(self.hp - hpLost, 0)
        hpLost = oldHp - self.hp
        if hpLost > 0:
            self.showHpText(-hpLost, bonus)
            self.hpChange(quietly = 0)
            if self.hp <= 0 and oldHp > 0:
                self.died()
            
        

    
    def setHp(self, hitPoints):
        if hitPoints is not None and self.hp is not None and self.hp - hitPoints > 0:
            pass
        justRanOutOfHp = hitPoints <= 0
        self.hp = hitPoints
        self.hpChange(quietly = 1)
        if justRanOutOfHp:
            self.died()
        

    
    def hpChange(self, quietly = 0):
        if hasattr(self, 'doId'):
            if self.hp != None and self.maxHp != None:
                messenger.send(self.uniqueName('hpChange'), [
                    self.hp,
                    self.maxHp,
                    quietly])
            
            if self.hp != None and self.hp > 0:
                messenger.send(self.uniqueName('positiveHP'))
            
        

    
    def died(self):
        pass

    
    def getHp(self):
        return self.hp

    
    def setMaxHp(self, hitPoints):
        self.maxHp = hitPoints
        self.hpChange()

    
    def getMaxHp(self):
        return self.maxHp

    
    def getName(self):
        return Avatar.getName(self)

    
    def setName(self, name):
        
        try:
            self.node().setName('%s-%d' % (name, self.doId))
            self.gotName = 1
        except:
            pass

        return Avatar.setName(self, name)

    
    def showHpText(self, number, bonus = 0, scale = 1):
        if self.HpTextEnabled and not (self.ghostMode):
            if number != 0:
                if self.hpText:
                    self.hideHpText()
                
                self.HpTextGenerator.setFont(OTPGlobals.getSignFont())
                if number < 0:
                    self.HpTextGenerator.setText(str(number))
                else:
                    self.HpTextGenerator.setText('+' + str(number))
                self.HpTextGenerator.clearShadow()
                self.HpTextGenerator.setAlign(TextNode.ACenter)
                if bonus == 1:
                    r = 1.0
                    g = 1.0
                    b = 0
                    a = 1
                elif bonus == 2:
                    r = 1.0
                    g = 0.5
                    b = 0
                    a = 1
                elif number < 0:
                    r = 0.90000000000000002
                    g = 0
                    b = 0
                    a = 1
                else:
                    r = 0
                    g = 0.90000000000000002
                    b = 0
                    a = 1
                self.HpTextGenerator.setTextColor(r, g, b, a)
                self.hpTextNode = self.HpTextGenerator.generate()
                self.hpText = self.attachNewNode(self.hpTextNode)
                self.hpText.setScale(scale)
                self.hpText.setBillboardPointEye()
                self.hpText.setBin('fixed', 100)
                self.hpText.setPos(0, 0, self.height / 2)
                seq = Task.sequence(self.hpText.lerpPos(Point3(0, 0, self.height + 1.5), 1.0, blendType = 'easeOut'), Task.pause(0.84999999999999998), self.hpText.lerpColor(Vec4(r, g, b, a), Vec4(r, g, b, 0), 0.10000000000000001), Task.Task(self.hideHpTextTask))
                taskMgr.add(seq, self.uniqueName('hpText'))
            
        

    
    def showHpString(self, text, duration = 0.84999999999999998, scale = 0.69999999999999996):
        if self.HpTextEnabled and not (self.ghostMode):
            if text != '':
                if self.hpText:
                    self.hideHpText()
                
                self.HpTextGenerator.setFont(OTPGlobals.getSignFont())
                self.HpTextGenerator.setText(text)
                self.HpTextGenerator.clearShadow()
                self.HpTextGenerator.setAlign(TextNode.ACenter)
                r = 1.0
                a = 1.0
                g = 0.0
                b = 0.0
                self.HpTextGenerator.setTextColor(r, g, b, a)
                self.hpTextNode = self.HpTextGenerator.generate()
                self.hpText = self.attachNewNode(self.hpTextNode)
                self.hpText.setScale(scale)
                self.hpText.setBillboardAxis()
                self.hpText.setPos(0, 0, self.height / 2)
                seq = Task.sequence(self.hpText.lerpPos(Point3(0, 0, self.height + 1.5), 1.0, blendType = 'easeOut'), Task.pause(duration), self.hpText.lerpColor(Vec4(r, g, b, a), Vec4(r, g, b, 0), 0.10000000000000001), Task.Task(self.hideHpTextTask))
                taskMgr.add(seq, self.uniqueName('hpText'))
            
        

    
    def hideHpTextTask(self, task):
        self.hideHpText()
        return Task.done

    
    def hideHpText(self):
        if self.hpText:
            taskMgr.remove(self.uniqueName('hpText'))
            self.hpText.removeNode()
            self.hpText = None
        

    
    def getStareAtNodeAndOffset(self):
        return (self, Point3(0, 0, self.height))

    
    def getAvIdName(self):
        return '%s\n%s' % (self.getName(), self.doId)

    
    def _DistributedAvatar__nameTagShowAvId(self, extra = None):
        self.setDisplayName(self.getAvIdName())

    
    def _DistributedAvatar__nameTagShowName(self, extra = None):
        self.setDisplayName(self.getName())

    
    def askAvOnShard(self, avId):
        if base.cr.doId2do.get(avId):
            messenger.send('AvOnShard%s' % avId, [
                True])
        else:
            self.sendUpdate('checkAvOnShard', [
                avId])

    
    def confirmAvOnShard(self, avId, onShard = True):
        messenger.send('AvOnShard%s' % avId, [
            onShard])

    
    def getDialogueArray(self):
        pass


