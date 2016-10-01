from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal

class HolidayManager(DistributedObject.DistributedObject):
	notify = DirectNotifyGlobal.directNotify.newCategory('HolidayManager')
	neverDisable = 1
	
	def __init__(self):
		pass