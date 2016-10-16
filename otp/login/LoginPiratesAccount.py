import LoginBase
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *
from direct.directnotify.DirectNotifyGlobal import directNotify

class LoginPiratesAccount(LoginBase.LoginBase):
    notify = directNotify.newCategory('PiratesLogin')

    def __init__(self, cr):
        LoginBase.LoginBase.__init__(self, cr)

    def createAccount(self, loginName, password, data):
        self.notify.warning("Creating account from client is unsupported")
        return

    def sendLoginMsg(self):
        cr = self.cr
        datagram = PyDatagram()
        datagram.addUint16(CLIENT_HELLO)
        datagram.addUint32(cr.hashVal)
        datagram.addString(cr.serverVersion)
        cr.send(datagram)