import random, gc, sys, os, time, __builtin__
import PiratesPreloader
from pirates.launcher.PiratesLauncher import PiratesLauncher
print ':PiratesStart: Starting the game.'

class game:
    name = 'pirates'
    process = 'client'

__builtin__.game = game()
__builtin__.launcher = PiratesLauncher()

gc.disable()

from direct.gui import DirectGuiGlobals
import PiratesGlobals
DirectGuiGlobals.setDefaultFontFunc(PiratesGlobals.getInterfaceFont)
launcher.setPandaErrorCode(7)

from panda3d.core import *
loadPrcFile("config/config_dev.prc")
for dtool in ('children', 'parent', 'name'):
    del NodePath.DtoolClassDict[dtool]

import PiratesBase
PiratesBase.PiratesBase()

from direct.showbase.ShowBaseGlobal import *
if base.config.GetBool('want-preloader', False):
    base.preloader = PiratesPreloader.PiratesPreloader()

if base.win == None:
    print ':PiratesStart: Unable to open window; aborting.'
    sys.exit()

launcher.setPandaErrorCode(0)
launcher.setPandaWindowOpen()
base.sfxPlayer.setCutoffDistance(500.0)

from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
rolloverSound = loadSfx(SoundGlobals.SFX_GUI_ROLLOVER_01)
rolloverSound.setVolume(0.5)
DirectGuiGlobals.setDefaultRolloverSound(rolloverSound)
clickSound = loadSfx(SoundGlobals.SFX_GUI_CLICK_01)
DirectGuiGlobals.setDefaultClickSound(clickSound)
clearColor = Vec4(0.0, 0.0, 0.0, 1.0)
base.win.setClearColor(clearColor)

from pirates.shader.Hdr import *
hdr = Hdr()

from pirates.seapatch.Reflection import Reflection
Reflection.initialize(render)

serverVersion = base.config.GetString('server-version', 'no_version_set')
print ':PiratesStart: serverVersion: ', serverVersion

from pirates.distributed import PiratesClientRepository
cr = PiratesClientRepository.PiratesClientRepository(serverVersion, launcher)
base.initNametagGlobals()
base.startShow(cr)

from otp.distributed import OtpDoGlobals
from pirates.piratesbase import UserFunnel
UserFunnel.logSubmit(1, 'CLIENT_OPENS')
UserFunnel.logSubmit(0, 'CLIENT_OPENS')

if base.config.GetBool('want-portal-cull', False):
    base.cam.node().setCullCenter(base.camera)
    base.graphicsEngine.setPortalCull(1)

if base.options:
    base.options.options_to_config()
    base.options.setRuntimeOptions()
    if launcher.isDummy() and not Thread.isTrueThreads():
        run()
    elif __name__ == '__main__':
        run()