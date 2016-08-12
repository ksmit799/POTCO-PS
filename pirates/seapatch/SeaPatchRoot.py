class SeaPatchRoot:
    WTZ = None
    WTV = None
    WTU = None
    WFSin = None
    WFNoise = None

    def addFlatWell(self, string1, nodePath1, float1, float2, float3, float4):
        pass

    def allocateWave(self, int1):
        pass

    def animateHeight(self, bool1):
        pass

    def animateUv(self, bool1):
        pass

    def appendWavesFrom(self, seaPatchRoot1):
        pass

    def assignEnvironmentFrom(self, seaPatchRoot1):
        pass

    def assignPropertiesFrom(self, seaPatchRoot1):
        pass

    def calcColor(self, vec41, float1, float2, float3):
        pass

    def calcFilteredHeight(self, float1, float2, float3, float4):
        pass

    def calcFlatWellScale(self, float1, float2):
        pass

    def calcHeight(self, float1, float2, float3):
        pass

    def calcHeightForMass(self, float1, float2, float3, float4, float5, float6):
        pass

    def calcNormal(self, float1, float2, float3, float4):
        pass

    def calcNormalForMass(self, float1, float2, float3, float4, float5, float6):
        pass

    def calcUv(self, point21, float1, float2, float3):
        pass

    def clampColor(self, vec41):
        pass

    def clearFlatWells(self):
        pass

    def clearWaves(self):
        pass

    def computeAmplitudeScale(self):
        pass

    def disable(self):
        pass

    def disableWave(self, int1):
        pass

    def enable(self):
        pass

    def enableWave(self, int1):
        pass

    def getAnchor(self):
        pass

    def getAnimateHeight(self):
        pass

    def getCenter(self):
        pass

    def getChoppyK(self, int1):
        pass

    def getHeightDamper(self):
        pass

    def getHighColor(self):
        pass

    def getLowColor(self):
        pass

    def getMidColor(self):
        pass

    def getNormalDamper(self):
        pass

    def getNumWaves(self):
        pass

    def getOverallSpeed(self):
        pass

    def getRadius(self):
        pass

    def getRootT(self):
        pass

    def getSeaLevel(self):
        pass

    def getThreshold(self):
        pass

    def getType(self):
        pass

    def getUvOffset(self):
        pass

    def getUvScale(self):
        pass

    def getUvSpeed(self):
        pass

    def getWaveAmplitude(self, int):
        pass

    def getWaveDirection(self, int):
        pass

    def getWaveFunc(self, int):
        pass

    def getWaveLength(self, int):
        pass

    def getWaveSpeed(self, int):
        pass

    def getWaveTarget(self, int):
        pass

    def hasFlatWell(self, string):
        pass

    def isEnabled(self):
        pass

    def isWaveEnabled(self, int):
        pass

    def output(self, string):
        pass

    def printFlatWells(self):
        pass

    def removeFlatWell(self, string):
        pass

    def removeWave(self, int):
        pass

    def resetEnvironment(self):
        pass

    def resetProperties(self):
        pass

    def setAnchor(self, nodePath):
        pass

    def setCenter(self, nodePath):
        pass

    def setChoppyK(self, int, int2):
        pass

    def setHeightDamper(self, float):
        pass

    def setHighColor(self, vec4):
        pass

    def setLowColor(self, vec4):
        pass

    def setNormalDamper(self, float):
        pass

    def setOverallSpeed(self, float):
        pass

    def setRadius(self, float):
        pass

    def setSeaLevel(self, float):
        pass

    def setThreshold(self, float):
        pass

    def setUvScale(self, vec2):
        pass

    def setUvSpeed(self, vec2):
        pass

    def setWaveAmplitude(self, int, float):
        pass

    def setWaveDirection(self, int, vec2):
        pass

    def setWaveFunc(self, int, WaveFunc):
        pass

    def setWaveLength(self, int, float):
        pass

    def setWaveSpeed(self, int, float):
        pass

    def setWaveTarget(self, int, WaveTarget):
        pass

    def write(self, string, uint):
        pass