from direct.directnotify.DirectNotifyGlobal import directNotify
from panda3d.core import ConfigVariableString

notify = directNotify.newCategory('OTPLocalizer')

language = ConfigVariableString('language', 'English').getValue()
_languageModule = 'otp.otpbase.OTPLocalizer' + language

try:
	exec 'from ' + _languageModule + ' import *'
	notify.info("Running in language: %s" % language)
except:
	notify.warning("Language '%s' not found! Setting as default (English)" % language)
	from otp.otpbase.OTPLocalizerEnglish import *
    
def getLanguage():
    return language