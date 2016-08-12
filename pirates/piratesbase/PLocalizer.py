#Rewritten from orignal File
#TODO: Get language from cfg file
language = "English"
'''
try:
    #language = getConfigExpress().GetString('language', 'english')
    #checkLanguage = getConfigExpress().GetBool('check-language', 1)
except:
    #language = simbase.config.GetString('language', 'english')
    #checkLanguage = simbase.config.GetBool('check-language', 1)
	#Why would it except????? .-.
	print("Error setting language")
'''

def getLanguage():
    return language

_PLocalizer = 'pirates.piratesbase.PLocalizer' + language
_PQuestStrings = 'pirates.piratesbase.PQuestStrings' + language
_PDialogStrings = 'pirates.piratesbase.PDialogStrings' + language
_PGreetingStrings = 'pirates.piratesbase.PGreetingStrings' + language

try:
	exec 'from ' + _PLocalizer + ' import *'
	exec 'from ' + _PQuestStrings + ' import *'
	exec 'from ' + _PDialogStrings + ' import *'
	exec 'from ' + _PGreetingStrings + ' import *'
	print 'PLocalizer: Running in language: %s' % language
except:
	print("PLocalizer: Error, Language not found!")
	print("PLocalizer: Setting language to default (English)")
	from pirates.piratesbase.PLocalizerEnglish import *
	from pirates.piratesbase.PQuestStringsEnglish import *
	from pirates.piratesbase.PDialogStringsEnglish import *
	from pirates.piratesbase.PGreetingStringsEnglish import *