from pandac.PandaModules import *
import time
import hmac
import hashlib

SECRET = 'secret-dev'  # Definitely going to be changed lmfao

accountServerEndpoint = 'https://www.toontowninfinite.com/api/'

http = HTTPClient()
http.setVerifySsl(0)

def executeHttpRequest(url, message):
    channel = http.makeChannel(True)
    spec = DocumentSpec(accountServerEndpoint + url)
    rf = Ramfile()
    channel.sendExtraHeader('User-Agent', 'TTI-CSM-Bot')
    timestamp = str(int(time.mktime(time.gmtime())))
    channel.sendExtraHeader('X-Game-Server-Request-Timestamp', timestamp)
    digest = hmac.new(SECRET, timestamp + message, hashlib.sha256)
    channel.sendExtraHeader('X-Game-Server-Signature', digest.hexdigest())
    if channel.getDocument(spec) and channel.downloadToRam(rf):
        return rf.getData()

userId = 3
accessLevel = 500

print executeHttpRequest('associate/accesslevel/?userid={0}&accesslevel={1}'.format(userId, accessLevel), str(userId) + str(accessLevel))