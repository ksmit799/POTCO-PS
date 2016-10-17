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
        datagram.addUint32(0xe7a9a07e)
        datagram.addString(cr.serverVersion)
        cr.send(datagram)

    def supportsRelogin(self):
        return False

    def authorize(self, loginName, password):
        self.loginName = loginName
        self.password = password
        self.createFlag = 0
        self.cr.freeTimeExpiresAt = -1
        self.cr.setIsPaid(1)