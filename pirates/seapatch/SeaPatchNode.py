from pandac.PandaModules import NodePath

class SeaPatchNode(NodePath):
    def __init__(self, name, patchRoot):
        NodePath.__init__(self, name)
        self.name = name
        self.patchRoot = patchRoot
        self.wantReflect = False
        self.wantColor = False

    def setWantReflect(self, status):
        self.wantReflect = status

    def getWantReflect(self):
        return self.wantReflect

    def setWantColor(self, status):
        self.wantColor = status

    def getWantColor(self):
        return self.wantColor

    def collectGeometry(self):
        pass