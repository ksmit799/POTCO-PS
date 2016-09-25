# File: A (Python 2.4)

from pirates.creature.Creature import Creature

class Animal(Creature):
    
    def __init__(self, animationMixer = None):
        Creature.__init__(self, animationMixer)

    
    def initializeNametag3d(self):
        pass

    initializeNametag3d = report(types = [
        'module',
        'args'], dConfigParam = 'nametag')(initializeNametag3d)
    
    def initializeNametag3dPet(self):
        Creature.initializeNametag3d(self)


