# File: D (Python 2.4)

from direct.distributed import DistributedObject

class DistributedEnemySpawner(DistributedObject.DistributedObject):
    
    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    
    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        print 'created enemy'


