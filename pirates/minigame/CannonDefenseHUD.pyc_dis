# File: C (Python 2.4)

from pirates.piratesgui.CannonDefenseGoldRemaingUI import *
from pirates.piratesgui.CannonDefenseTimeRemainingUI import *

class CannonDefenseHUD:
    
    def __init__(self):
        self.goldRemainingUI = None
        self.timeRemainingUI = None

    
    def create(self):
        self.goldRemainingUI = CannonDefenseGoldRemaingUI()
        self.timeRemainingUI = CannonDefenseTimeRemainingUI()
        self.timeRemainingUI.setWaveNumber(1)
        self.goldRemainingUI.mineCounter.setPos(0.025000000000000001, 0, -0.035000000000000003)
        self.timeRemainingUI.timeRemaining.setPos(-0.01, 0, 0)

    
    def destroy(self):
        if self.goldRemainingUI:
            self.goldRemainingUI.destroy()
            self.goldRemainingUI = None
        
        if self.timeRemainingUI:
            self.timeRemainingUI.destroy()
            self.timeRemainingUI = None
        


