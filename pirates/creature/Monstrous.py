# File: M (Python 2.4)


class Monstrous:
    
    def initializeMonstrousTags(self, rootNodePath):
        PiratesGlobals = PiratesGlobals
        import pirates.piratesbase
        rootNodePath.setPythonTag('MonstrousObject', self)
        self.setPythonTag('MonstrousObject', self)
        rootNodePath.setTag('objType', str(PiratesGlobals.COLL_MONSTROUS))
        self.setTag('objType', str(PiratesGlobals.COLL_MONSTROUS))

    
    def cleanupMontstrousTags(self, rootNodePath):
        rootNodePath.clearPythonTag('MonstrousObject')
        self.clearPythonTag('MonstrousObject')

    
    def initializeBattleCollisions(self):
        pass


