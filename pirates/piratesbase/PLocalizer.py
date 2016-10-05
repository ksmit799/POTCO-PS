from direct.directnotify.DirectNotifyGlobal import directNotify
from panda3d.core import ConfigVariableString

notify = directNotify.newCategory('PLocalizer')

language = ConfigVariableString('language', 'English').getValue()
_PLocalizer = 'pirates.piratesbase.PLocalizer' + language
_PQuestStrings = 'pirates.piratesbase.PQuestStrings' + language
_PDialogStrings = 'pirates.piratesbase.PDialogStrings' + language
_PGreetingStrings = 'pirates.piratesbase.PGreetingStrings' + language

try:
	exec 'from ' + _PLocalizer + ' import *'
	exec 'from ' + _PQuestStrings + ' import *'
	exec 'from ' + _PDialogStrings + ' import *'
	exec 'from ' + _PGreetingStrings + ' import *'
	notify.info("Running in language: %s" % language)
except:
	notify.warning("Language '%s' not found! Setting as default (English)" % language)
	from pirates.piratesbase.PLocalizerEnglish import *
	from pirates.piratesbase.PQuestStringsEnglish import *
	from pirates.piratesbase.PDialogStringsEnglish import *
	from pirates.piratesbase.PGreetingStringsEnglish import *

def getLanguage():
    return language