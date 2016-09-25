# File: M (Python 2.4)


class Mappable:
    
    def __init__(self):
        pass

    
    def getMapNode(self):
        pass



class MappableArea(Mappable):
    
    def getMapName(self):
        return ''

    
    def getZoomLevels(self):
        return ((100, 200, 300), 1)

    
    def getFootprintNode(self):
        pass

    
    def getShopNodes(self):
        return ()

    
    def getCapturePointNodes(self, holidayId):
        return ()



class MappableGrid(MappableArea):
    
    def getGridParamters(self):
        return ()


