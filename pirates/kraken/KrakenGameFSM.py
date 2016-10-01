from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM
from pirates.util.BpDb import *

class bp:
    bpdb = BpDb()
    kraken = bpdb.bpPreset(cfg = 'krakenfsm', static = 1)
    krakenCall = bpdb.bpPreset(cfg = 'krakenfsm', call = 1, static = 1)


class KrakenGameFSM(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('KrakenGameFSM')
    
    def __init__(self, av):
        FSM.__init__(self, 'KrakenGameFSM')
        self.av = av

    
    def enterRam(self):
        pass

    enterRam = None
    #enterRam = bp.krakenCall()(enterRam)
    
    def exitRam(self):
        pass

    exitRam = None
    #exitRam = bp.krakenCall()(exitRam)
    
    def enterGrab(self):
        self.av.emergeInterval.pause()
        self.av.submergeInterval.start()

    enterGarb = None
    #enterGrab = bp.krakenCall()(enterGrab)
    
    def exitGrab(self):
        pass

    exitGrab = None
    #exitGrab = bp.krakenCall()(exitGrab)
