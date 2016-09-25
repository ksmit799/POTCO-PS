# File: G (Python 2.4)

from direct.interval.IntervalGlobal import *
from pirates.pirate.BattleAvatarGameFSM import BattleAvatarGameFSM
import random

class bp:
    off = bpdb.bpPreset(cfg = 'krakengrabberfsm', grp = 'off', static = 1)
    offCall = bpdb.bpPreset(cfg = 'krakengrabberfsm', grp = 'off', call = 1, static = 1)
    idle = bpdb.bpPreset(cfg = 'krakengrabberfsm', grp = 'idle', static = 1)
    idleCall = bpdb.bpPreset(cfg = 'krakengrabberfsm', grp = 'idle', call = 1, static = 1)
    submerged = bpdb.bpPreset(cfg = 'krakengrabberfsm', grp = 'submerged', static = 1)
    submergedCall = bpdb.bpPreset(cfg = 'krakengrabberfsm', grp = 'submerged', call = 1, static = 1)


class GrabberGameFSM(BattleAvatarGameFSM):
    
    def __init__(self, av):
        BattleAvatarGameFSM.__init__(self, av)
        self.submergeIval = None
        self.emergeIval = None

    
    def delete(self):
        BattleAvatarGameFSM.delete(self)
        self.av.creature = None
        if self.submergeIval:
            self.submergeIval.finish()
            self.submergeIval = None
        
        if self.emergeIval:
            self.emergeIval.finish()
            self.emergeIval = None
        

    
    def exitOff(self, *args):
        self.submergeIval = self.av.actorInterval('emerge', playRate = -1, blendOutT = 0)
        self.submergeIval.start()
        self.submergeIval.finish()
        self.submergeIval = None

    exitOff = bp.offCall()(exitOff)
    
    def fromOffToSubmerged(self, *args):
        self.submergeIval = self.av.actorInterval('emerge', playRate = -1, blendOutT = 0)
        self.submergeIval.start()
        self.submergeIval.finish()
        self.submergeIval = None

    fromOffToSubmerged = bp.submergedCall()(fromOffToSubmerged)
    
    def enterSubmerged(self, *args):
        self.submergeIval = Sequence(Wait(random.random()), self.av.actorInterval('emerge', playRate = -1, blendOutT = 0), Func(self.av.creature.hide), Func(self.av.creature.stopUpdateTask), Func(self.av.creature.removeEffects))
        self.submergeIval.start()

    enterSubmerged = bp.submergedCall()(enterSubmerged)
    
    def exitSubmerged(self):
        if self.submergeIval:
            self.submergeIval.finish()
            self.submergeIval = None
        
        self.av.creature.startUpdateTask()

    exitSubmerged = bp.submergedCall()(exitSubmerged)
    
    def fromOffToIdle(self, *args):
        self.emergeIval = Sequence(Func(self.fromOffToSubmerged), Func(self.fromSubmergedToIdle))
        self.emergeIval.start()

    fromOffToIdle = bp.idleCall()(fromOffToIdle)
    
    def fromSubmergedToIdle(self, *args):
        self.emergeIval = Sequence(Func(self.exitSubmerged), Wait(random.random()), Func(self.av.creature.show), self.av.actorInterval('emerge', playRate = 0.75, blendOutT = 0), Func(self.enterIdle))
        self.emergeIval.start()

    fromSubmergedToIdle = bp.idleCall()(fromSubmergedToIdle)
    
    def enterIdle(self, *args):
        self.av.creature.startIdleTask()

    enterIdle = bp.idleCall()(enterIdle)
    
    def exitIdle(self):
        if self.emergeIval:
            self.emergeIval.finish()
            self.emergeIval = None
        
        self.av.creature.stopIdleTask()

    exitIdle = bp.idleCall()(exitIdle)

