try:
  from panda3dCoreModules import *
except ImportError, err:
  if "DLL loader cannot find" not in str(err):
    raise

try:
  from panda3dPhysicsModules import *
except ImportError, err:
  if "DLL loader cannot find" not in str(err):
    raise

try:
  from panda3dFxModules import *
except ImportError, err:
  if "DLL loader cannot find" not in str(err):
    raise

try:
  from panda3dDirectModules import *
except ImportError, err:
  if "DLL loader cannot find" not in str(err):
    raise

try:
  from panda3dVisionModules import *
except ImportError, err:
  if "DLL loader cannot find" not in str(err):
    raise

try:
  from panda3dSkelModules import *
except ImportError, err:
  if "DLL loader cannot find" not in str(err):
    raise

try:
  from panda3dEggModules import *
except ImportError, err:
  if "DLL loader cannot find" not in str(err):
    raise

try:
  from panda3dOdeModules import *
except ImportError, err:
  if "DLL loader cannot find" not in str(err):
    raise

try:
  from panda3dVrpnModules import *
except ImportError, err:
  if "DLL loader cannot find" not in str(err):
    raise

