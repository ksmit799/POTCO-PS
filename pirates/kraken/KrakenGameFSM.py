# File: K (Python 2.4)

from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM

class bp:
    kraken = bpdb.bpPreset(cfg = 'krakenfsm', static = 1)
    krakenCall = bpdb.bpPreset(cfg = 'krakenfsm', call = 1, static = 1)


class KrakenGameFSM(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('KrakenGameFSM')
    
    def __init__(self, av):
        FSM.__init__(self, 'KrakenGameFSM')
        self.av = av

    
    def enterRam(self):
        pass

    enterRam = bp.krakenCall()(enterRam)
    
    def exitRam(self):
        pass

    exitRam = bp.krakenCall()(exitRam)
    
    def enterGrab(self):
        self.av.emergeInterval.pause()
        self.av.submergeInterval.start()

    enterGrab = bp.krakenCall()(enterGrab)
    
    def exitGrab(self):
        pass

    exitGrab = bp.krakenCall()(exitGrab)

