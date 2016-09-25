# File: P (Python 2.4)

from otp.avatar.AvatarHandle import AvatarHandle

class PAvatarHandle(AvatarHandle):
    dclassName = 'PAvatarHandle'
    
    def getBandId(self):
        if __dev__:
            pass
        1
        return (0, 0)

    
    def sendTeleportQuery(self, sendToId, localBandMgrId, localBandId, localGuildId, localShardId):
        if __dev__:
            pass
        1

    sendTeleportQuery = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'teleport')(sendTeleportQuery)
    
    def sendTeleportResponse(self, available, shardId, instanceDoId, areaDoId, sendToId = None):
        if __dev__:
            pass
        1

    sendTeleportResponse = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'teleport')(sendTeleportResponse)

