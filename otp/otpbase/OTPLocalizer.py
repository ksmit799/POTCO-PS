#Rewritten from orignal File
#TODO: Get language from cfg file
language = "English"
'''
try:
    language = getConfigExpress().GetString('language', 'english')
    checkLanguage = getConfigExpress().GetBool('check-language', 0)
except:
    language = simbase.config.GetString('language', 'english')
    checkLanguage = simbase.config.GetBool('check-language', 0)
'''

def getLanguage():
    return language

_languageModule = 'otp.otpbase.OTPLocalizer' + language

try:
	exec 'from ' + _languageModule + ' import *'
	print 'OTPLocalizer: Running in language: %s' % language
except:
	print("OPT Localizer: Error, Language not found!")
	print("OPT Localizer: Setting language to default (English)")
	from otp.otpbase.OTPLocalizerEnglish import *
    

