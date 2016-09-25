# File: F (Python 2.4)

from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from pirates.creature.Creature import Creature
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class FlyTrap(Creature):
    ModelInfo = ('models/char/flytrap_hi', 'models/char/flytrap_')
    SfxNames = dict(Creature.SfxNames)
    SfxNames.update({
        'death': SoundGlobals.SFX_MONSTER_FLYTRAP_DEATH,
        'pain': SoundGlobals.SFX_MONSTER_FLYTRAP_PAIN,
        'spawn': SoundGlobals.SFX_MONSTER_FLYTRAP_SPAWN })
    sfx = { }
    AnimList = (('idle', 'idle'), ('attack_a', 'attack_a'), ('attack_jab', 'attack_jab'), ('attack_left_fake', 'attack_left_fake'), ('attack_right_fake', 'attack_right_fake'), ('intro', 'rise_from_ground'), ('shoot', 'spit'), ('pain', 'hit'), ('death', 'death'))
    
    class AnimationMixer(Creature.AnimationMixer):
        notify = DirectNotifyGlobal.directNotify.newCategory('FlyTrapAnimationMixer')
        LOOP = Creature.AnimationMixer.LOOP
        ACTION = Creature.AnimationMixer.ACTION
        AnimRankings = {
            'idle': (LOOP['LOOP'],),
            'attack_a': (ACTION['ACTION'],),
            'attack_jab': (ACTION['ACTION'],),
            'attack_left_fake': (ACTION['ACTION'],),
            'attack_right_fake': (ACTION['ACTION'],),
            'intro': (ACTION['ACTION'],),
            'shoot': (ACTION['ACTION'],),
            'pain': (ACTION['ACTION'],),
            'death': (ACTION['MOVIE'],) }

    
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', -1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', -1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0)))

    setupAnimInfo = classmethod(setupAnimInfo)
    
    def __init__(self):
        Creature.__init__(self)
        if not FlyTrap.sfx:
            for name in FlyTrap.SfxNames:
                FlyTrap.sfx[name] = loadSfx(FlyTrap.SfxNames[name])
            
        
        self.nametagOffset = 23
        self.generateCreature()
        self.headNode = self.find('**/def_stem10')

    
    def generateCreature(self):
        Creature.generateCreature(self)
        self.getGeomNode().setH(180)
        self.setAvatarScale(0.69999999999999996)

    
    def shouldNotice(self):
        return 0


