class LoginBase:
    freeTimeExpires = -1
    
    def __init__(self, cr):
        self.cr = cr

    
    def sendLoginMsg(self, loginName, password, createFlag):
        pass

    
    def getErrorCode(self):
        return

    
    def needToSetParentPassword(self):
        return