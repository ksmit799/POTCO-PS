from pandac.PandaModules import *
import time
 
accountServerEndpoint = 'https://www.toontowninfinite.com/api/associate/accesslevel/'
 
http = HTTPClient()
http.setVerifySsl(0)
 
def executeHttpRequest(url, message):
    channel = http.makeChannel(True)
    spec = DocumentSpec(accountServerEndpoint + url)
    rf = Ramfile()
    channel.sendExtraHeader('User-Agent', 'TTI-CSM-Bot')
    channel.sendExtraHeader('X-Game-Server-Signature', 'dev')
    if channel.getDocument(spec) and channel.downloadToRam(rf):
        return rf.getData()
 
print executeHttpRequest('associate/accesslevel/', '')
