from Nametag3d import *

class NametagFloat2d(Nametag3d):
    WANT_DYNAMIC_SCALING = False
    SCALING_FACTOR = 1.0
    SHOULD_BILLBOARD = False

    def setActive(self, active):
        pass # TODO

    def upcastToPandaNode(self):
        return 'Nametag2D-%s' % id(self) # TODO