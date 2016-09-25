# File: P (Python 2.4)

from otp.friends.FriendInfo import FriendInfo
from pirates.pirate.PAvatarHandle import PAvatarHandle

class PCFriendAvatarInfo(FriendInfo, PAvatarHandle):
    
    def makeFromFriendInfo(cls, info):
        out = cls()
        out.avatarName = info.avatarName
        out.playerName = info.playerName
        out.onlineYesNo = info.onlineYesNo
        out.openChatEnabledYesNo = info.openChatEnabledYesNo
        out.openChatFriendshipYesNo = info.openChatFriendshipYesNo
        out.understandableYesNo = info.understandableYesNo
        out.playerId = info.playerId
        return out

    makeFromFriendInfo = classmethod(makeFromFriendInfo)
    
    def __init__(self, *args, **kw):
        FriendInfo.__init__(self, *args, **args)
        self.bandId = None

    
    def setBandId(self, bandMgrId, bandId):
        if (bandMgrId, bandId) != (0, 0):
            self.bandId = (bandMgrId, bandId)
        else:
            self.bandId = None

    
    def getBandId(self):
        return self.bandId

    
    def sendTeleportQuery(self, sendToId, localBandMgrId, localBandId, localGuildId, localShardId):
        localAvatar.sendTeleportQuery(sendToId, localBandMgrId, localBandId, localGuildId, localShardId)

    sendTeleportQuery = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'teleport')(sendTeleportQuery)
    
    def sendTeleportResponse(self, available, shardId, instanceDoId, areaDoId, sendToId = None):
        localAvatar.sendTeleportResponse(available, shardId, instanceDoId, areaDoId, sendToId)

    sendTeleportResponse = report(types = [
        'deltaStamp',
        'args'], dConfigParam = 'teleport')(sendTeleportResponse)

