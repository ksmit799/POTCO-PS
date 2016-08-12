import random
from pirates.pirate.AvatarType import AvatarType
from pirates.pirate.AvatarTypeSet import AvatarTypeSet
from pirates.piratesbase import PLocalizer as PL

AnyAvatar = AvatarType()
AnyShip = AvatarType()
BossType = AvatarType(boss = 1)

MovieCasts = [AvatarType() for x in xrange(6)]
JackSparrow, ElizabethSwan, CaptBarbossa, WillTurner, TiaDalma, JoshameeGibbs = MovieCasts

Factions = [AvatarType(faction=x) for x in xrange(9)]
Undead, Navy, Creature, Townfolk, Pirate, TradingCo, Ghost, VoodooZombie, BountyHunter = Factions

CreatureTracks = [AvatarType(base=Creature, track=x) for x in xrange(5)]
LandCreature, SeaCreature, AirCreature, SeaMonster, Animal = CreatureTracks

LandCreatures = [AvatarType(base=LandCreature, id=x) for x in xrange(24)]
Crab, StoneCrab, RockCrab, GiantCrab, CrusherCrab, Chicken, Rooster, Pig, Stump, TwistedStump, FlyTrap, RancidFlyTrap, AncientFlyTrap, Scorpion, DireScorpion, DreadScorpion, Alligator, BayouGator, BigGator, HugeGator, Dog, Seagull, Raven, Monkey = LandCreatures

LandCrab = AvatarTypeSet(PL.LandCrabStrings, Crab, RockCrab, GiantCrab, CrusherCrab)

CrabBosses = [AvatarType(base=Crab, boss=1)]
SandStalker = CrabBosses[0]

RockCrabBosses = [AvatarType(base=RockCrab, boss=1)]
ManRipper = RockCrabBosses[0]

GiantCrabBosses = [AvatarType(base=GiantCrab, boss=1)]
ClawChief = GiantCrabBosses[0]

StumpBosses = [AvatarType(base=Stump, boss=1)]
Bowbreaker = StumpBosses[0]

FlyTrapBosses = [AvatarType(base=FlyTrap, boss=1)]
SnapDragon = FlyTrapBosses[0]

ScorpionBosses = [AvatarType(base=Scorpion, boss=1)]
RipTail = ScorpionBosses[0]

DreadScorpionBosses = [AvatarType(base=DreadScorpion, boss=1)]
SilentStinger = DreadScorpionBosses[0]

AlligatorBosses = [AvatarType(base=Alligator, boss=1)]
Bonecracker = CrabBosses[0]

BigGatorBosses = [AvatarType(base=BigGator, boss=1)]
Trapjaw = BigGatorBosses[0]

HugeGatorBosses = [AvatarType(base=HugeGator, boss=1)]
SwampTerror = HugeGatorBosses[0]

Animals = [AvatarType(base=Animal, id=x) for x in xrange(6)]
Chicken, Rooster, Pig, Dog, Seagull, Raven = Animals

SeaCreatures = [AvatarType(base=SeaCreature, id=x) for x in xrange(1)]
Fish = SeaCreatures[0]

AirCreatures = [AvatarType(base=AirCreature, id=x) for x in xrange(10)]
Seagull, Raven, Bat, RabidBat, VampireBat, FireBat, Wasp, KillerWasp, AngryWasp, SoldierWasp = AirCreatures

BatBosses = [AvatarType(base=Bat, boss=1)]
Frightfang = BatBosses[0]

VampireBatBosses = [AvatarType(base=VampireBat, boss=1)]
Bloodleach = VampireBatBosses[0]

WaspBosses = [AvatarType(base=Wasp, boss=1)]
Firesting = WaspBosses[0]

AngryWaspBosses = [AvatarType(base=AngryWasp, boss=1)]
Devilwing = AngryWaspBosses[0]

SeaMonsters = [AvatarType(base=SeaMonster, id=x) for x in xrange(7)]
SeaKraken, Kraken, KrakenBody, KrakenHead, GrabberTentacle, HolderTentacle, SeaSerpent = SeaMonsters

UndeadTracks = [AvatarType(base=Undead, track=x) for x in xrange(9)]
Earth, Air, Fire, Water, Classic, Boss, French, Spanish, EarthSpecial = UndeadTracks

EarthUndead = [AvatarType(base=Earth, id=x) for x in xrange(15)]
Clod, Sludge, Mire, MireKnife, Muck, MuckCutlass, Corpse, CorpseCutlass, Carrion, CarrionKnife, Cadaver, CadaverCutlass, Zombie, CaptMudmoss, Mossman = EarthUndead

ClodBosses = [AvatarType(base=Clod, boss=x) for x in xrange(4)]
WillBurybones, FoulCrenshaw, EvanTheDigger, ThadIllFortune = ClodBosses

SludgeBosses = [AvatarType(base=Sludge, boss=1)]
SimonButcher = SludgeBosses[0]

MireBosses = [AvatarType(base=Mire, boss=1)]
ThaddeusWoodworm = MireBosses[0]

MuckBosses = [AvatarType(base=Muck, boss=1)]
Bonebreaker = MuckBosses[0]

CorpseBosses = [AvatarType(base=Corpse, boss=1)]
GideonGrog = CorpseBosses[0]

CarrionBosses = [AvatarType(base=Carrion, boss=1)]
WhitWidowmaker = CarrionBosses[0]

CadaverBosses = [AvatarType(base=Cadaver, boss=1)]
Blackheart = CadaverBosses[0]

ZombieBosses = [AvatarType(base=Zombie, boss=1)]
FrancisFaust = ZombieBosses[0]

CaptMudmossBosses = [AvatarType(base=CaptMudmoss, boss=1)]
JeremyColdhand = CaptMudmossBosses[0]

MossmanBosses = [AvatarType(base=Mossman, boss=1)]
Stench = MossmanBosses[0]

AirUndead = [AvatarType(base=Air, id=x) for x in xrange(10)]
Whiff, Reek, Billow, Stench, Shade, Specter, Phantom, Wraith, CaptZephyr, Squall = AirUndead

FireUndead = [AvatarType(base=Fire, id=x) for x in xrange(10)]
Glint, Flicker, Smolder, Spark, Imp, Brand, Lumen, Fiend, CaptCinderbones, Torch = FireUndead

WaterUndead = [AvatarType(base=Water, id=x) for x in xrange(10)]
Drip, Damp, Drizzle, Spray, Splatter, Drool, Drench, Douse, CaptBriney, Spout = WaterUndead

ClassicUndead = list()

BossUndead = [AvatarType(base=Boss, id=x) for x in xrange(1)]
JollyRoger = BossUndead[0]

FrenchUndead = [AvatarType(base=French, id=x) for x in xrange(5)]
FrenchUndeadA, FrenchUndeadB, FrenchUndeadC, FrenchUndeadD, FrenchBoss = FrenchUndead

FrenchBosses = [AvatarType(base=FrenchBoss, boss=1)]
FrenchBossA = FrenchBosses[0]

SpanishUndead = [AvatarType(base=Spanish, id=x) for x in xrange(5)]
SpanishUndeadA, SpanishUndeadB, SpanishUndeadC, SpanishUndeadD, SpanishBoss = SpanishUndead

SpanishBosses = [AvatarType(base=SpanishBoss, boss=1)]
SpanishBossA = SpanishBosses[0]

EarthSpecialUndead = [AvatarType(base=EarthSpecial, id=1)]
BomberZombie = EarthSpecialUndead[0]

UndeadCommon = (EarthUndead[0], EarthUndead[1])
UndeadUncommon = ()
UndeadRare = ()
UndeadUltraRare = ()
AllUndead = []
AllUndead.extend(UndeadCommon)
AllUndead.extend(UndeadUncommon)
AllUndead.extend(UndeadRare)

def pickUndead(minVal, maxVal, undeadType = EarthUndead):
    return undeadType[random.randint(minVal, maxVal)]


def pickEarthUndead(minVal = 0, maxVal = len(EarthUndead) - 1):
    return EarthUndead[random.randint(minVal, maxVal)]


def pickWaterUndead(minVal = 0, maxVal = len(WaterUndead) - 1):
    return WaterUndead[random.randint(minVal, maxVal)]


def pickSpanishUndead(minVal = 0, maxVal = len(SpanishUndead) - 1):
    return SpanishUndead[random.randint(minVal, maxVal)]


def pickFrenchUndead(minVal = 0, maxVal = len(FrenchUndead) - 1):
    return FrenchUndead[random.randint(minVal, maxVal)]


def randomUndead(level):
    retval = level / 3
    rnd = random.randint(0, 14)
    if rnd < 5:
        retval -= 1
    elif rnd > 12:
        retval += 1
    
    if retval < 0:
        retval = 0
    
    if retval > 7:
        retval = 7
    
    return EarthUndead[retval]

NavyTracks = [AvatarType(base=Navy, track=x) for x in xrange(3)]
Soldier, Marksman, Leader = NavyTracks

Soldiers = [AvatarType(base=Soldier, id=x) for x in xrange(5)]
Axeman, Swordsman, RoyalGuard, MasterSwordsman, WeaponsMaster = Soldiers

Marksmen = [AvatarType(base=Marksman, id=x) for x in xrange(7)]
Cadet, Guard, Marine, Sergeant, Veteran, Officer, Dragoon = Marksmen

CadetBosses = [AvatarType(base=Cadet, boss=1)]
GeoffreyPain = CadetBosses[0]

GuardBosses = [AvatarType(base=Guard, boss=1)]
HughBrandish = GuardBosses[0]

SergeantBosses = [AvatarType(base=Sergeant, boss=1)]
NathanielGrimm = SergeantBosses[0]

VeteranBosses = [AvatarType(base=Veteran, boss=1)]
SidShiver = VeteranBosses[0]

OfficerBosses = [AvatarType(base=Officer, boss=1)]
IanRamjaw = OfficerBosses[0]

Leaders = [AvatarType(base=Leader, id=x) for x in xrange(5)]
FirstMate, Captain, Lieutenant, Admiral, Commodore = Leaders

NavyCommon = (Cadet, Guard, Sergeant, Veteran, Officer)

def randomNavy(level):
    retval = level / 4
    rnd = random.randint(0, 14)
    if rnd < 5:
        retval -= 1
    elif rnd > 12:
        retval += 1
    
    if retval < 0:
        retval = 0
    
    if retval > 4:
        retval = 4
    
    return Marksmen[retval]


def pickTrading(tradlow, tradhigh):
    return Mercenaries[random.randint(tradlow, tradhigh)]


def pickNavy(navylow, navyhigh):
    return Marksmen[random.randint(navylow, navyhigh)]

TownfolkTracks = [AvatarType(base=Townfolk, track=x) for x in xrange(3)]
Commoner, StoreOwner, Cast = TownfolkTracks

Commoners = [AvatarType(base=Commoner, id=x) for x in xrange(1)]
Peasant = Commoners

StoreOwners = [AvatarType(base=StoreOwner, id=x) for x in xrange(21)]
Gypsy, Blacksmith, Shipwright, Cannoneer, Merchant, Bartender, Gunsmith, Grenadier, MedicineMan, Tailor, Tattoo, Jeweler, Barber, Musician, Trainer, PvPRewards, Stowaway, Fishmaster, Cannonmaster, CatalogRep, ScrimmageMaster = StoreOwners

CastBosses = [AvatarType(base=Cast, boss=1)]
Kudgel = CastBosses[0]

PirateTracks = [AvatarType(base=Pirate, track=x) for x in xrange(3)]
Player, Brawler, Gunner = PirateTracks

Players = [AvatarType(base=Player, id=x) for x in xrange(2)]
LocalPirateType, NonLocalPirateType = Players

Brawlers = [AvatarType(base=Brawler, id=x) for x in xrange(5)]
Landlubber, Scallywag, Buccaneer, Swashbuckler, Warmonger = Brawlers

Gunners = [AvatarType(base=Gunner, id=x) for x in xrange(5)]
Bandit, Brigand, Sharpshooter, Rifleman, Gunner = Gunners

GhostTracks = [AvatarType(base=Ghost, track=x) for x in xrange(2)]
GhostPirates, KillerGhosts = GhostTracks

GhostPirates = [AvatarType(base=GhostPirates, id=x) for x in xrange(6)]
Revenant, MutineerGhost, DeviousGhost, TraitorGhost, CrewGhost, LeaderGhost = GhostPirates

KillerGhosts = [AvatarType(base=KillerGhosts, id=1)]
RageGhost = KillerGhosts[0]

LeaderGhostBosses = [AvatarType(base=LeaderGhost, boss=1)]
ElPatron = LeaderGhostBosses[0]

VoodooZombieTracks = [AvatarType(base=VoodooZombie, track=1)]
VoodooZombiePirates = VoodooZombieTracks[0]

VoodooZombiePirates = [AvatarType(base=VoodooZombiePirates, id=x) for x in xrange(8)]
PressGangVoodooZombie, CookVoodooZombie, SwabbieVoodooZombie, LookoutVoodooZombie, AngryVoodooZombie, OfficerVoodooZombie, SlaveDriverVoodooZombie, VoodooZombieBoss = VoodooZombiePirates

VoodooZombieBosses = [AvatarType(base=VoodooZombieBoss, boss=1)]
LaSchafe = VoodooZombieBosses[0]

BountyHunterTracks = [AvatarType(base=BountyHunter, track=1)]
BountyHunters = BountyHunterTracks[0]

BountyHunters = [AvatarType(base=BountyHunters, id=x) for x in xrange(7)]
PettyHunter, BailHunter, ScallyWagHunter, BanditHunter, PirateHunter, WitchHunter, MasterHunter = BountyHunters

def pickGhost(minVal = 0, maxVal = len(GhostPirates) - 1):
    return GhostPirates[random.randint(minVal, maxVal)]


def pickVoodooZombie(minVal = 0, maxVal = len(VoodooZombiePirates) - 1):
    return VoodooZombiePirates[random.randint(minVal, maxVal)]


def pickBountyHunter(minVal = 0, maxVal = len(BountyHunters) - 1):
    return BountyHunters[random.randint(minVal, maxVal)]

TradingCoTracks = [AvatarType(base=TradingCo, track=x) for x in xrange(3)]
Mercenary, Assassin, Official = TradingCoTracks

Mercenaries = [AvatarType(base=Mercenary, id=x) for x in xrange(5)]
Thug, Grunt, Hiredgun, Mercenary, Assassin = Mercenaries

ThugBosses = [AvatarType(base=Thug, boss=1)]
CarlosCudgel = ThugBosses[0]

GruntBosses = [AvatarType(base=Grunt, boss=1)]
ZachariahSharp = GruntBosses[0]

HiredgunBosses = [AvatarType(base=Hiredgun, boss=1)]
HenryFlint = HiredgunBosses[0]

MercenaryBosses = [AvatarType(base=Mercenary, boss=1)]
PhineasFowl = MercenaryBosses[0]

AssassinBosses = [AvatarType(base=Assassin, boss=1)]
EdwardLohand = AssassinBosses[0]

Officials = [AvatarType(base=Official, id=x) for x in xrange(5)]
OffA, OffB, OffC, OffD, Viceroy = Officials

Assassins = [AvatarType(base=Assassin, id=x) for x in xrange(5)]
Rogue, Stalker, Cutthroat, Executioner, Professional = Assassins

AVATAR_TYPE_IDX = 0

def typePassthrough(type):
    return type

NPC_SPAWNABLES = {
    'Skeleton': [
        lambda p0 = 0, p1 = 3: pickEarthUndead(p0, p1)],
    'EvilNavy': [
        lambda p0 = 0, p1 = 1: pickNavy(p0, p1)],
    'Skel T0': [
        lambda p0 = 0: pickEarthUndead(p0, p0)],
    'Skel T1': [
        lambda p0 = 1: pickEarthUndead(p0, p0)],
    'Skel T2': [
        lambda p0 = 2, p1 = 3: pickEarthUndead(p0, p1)],
    'Skel T3': [
        lambda p0 = 4, p1 = 5: pickEarthUndead(p0, p1)],
    'Skel T4': [
        lambda p0 = 6: pickEarthUndead(p0, p0)],
    'Skel T5': [
        lambda p0 = 7: pickEarthUndead(p0, p0)],
    'Skel T6': [
        lambda p0 = 8, p1 = 9: pickEarthUndead(p0, p1)],
    'Skel T7': [
        lambda p0 = 10, p1 = 11: pickEarthUndead(p0, p1)],
    'Skel T8': [
        lambda p0 = 12: pickEarthUndead(p0, p0)],
    'Crab T0': [
        lambda p0 = Crab: typePassthrough(p0)],
    'Crab T1': [
        lambda p0 = StoneCrab: typePassthrough(p0)],
    'Crab T3': [
        lambda p0 = RockCrab: typePassthrough(p0)],
    'Crab T5': [
        lambda p0 = GiantCrab: typePassthrough(p0)],
    'Crab T6': [
        lambda p0 = CrusherCrab: typePassthrough(p0)],
    'Scorp T1': [
        lambda p0 = Scorpion: typePassthrough(p0)],
    'Scorp T3': [
        lambda p0 = DireScorpion: typePassthrough(p0)],
    'Scorp T5': [
        lambda p0 = DreadScorpion: typePassthrough(p0)],
    'Gator T1': [
        lambda p0 = Alligator: typePassthrough(p0)],
    'Gator T2': [
        lambda p0 = BayouGator: typePassthrough(p0)],
    'Gator T4': [
        lambda p0 = BigGator: typePassthrough(p0)],
    'Gator T5': [
        lambda p0 = HugeGator: typePassthrough(p0)],
    'Bat T1': [
        lambda p0 = Bat: typePassthrough(p0)],
    'Bat T2': [
        lambda p0 = RabidBat: typePassthrough(p0)],
    'Bat T4': [
        lambda p0 = VampireBat: typePassthrough(p0)],
    'Bat T8': [
        lambda p0 = FireBat: typePassthrough(p0)],
    'Wasp T3': [
        lambda p0 = Wasp: typePassthrough(p0)],
    'Wasp T4': [
        lambda p0 = KillerWasp: typePassthrough(p0)],
    'Wasp T5': [
        lambda p0 = AngryWasp: typePassthrough(p0)],
    'Wasp T6': [
        lambda p0 = SoldierWasp: typePassthrough(p0)],
    'FlyTrap T4': [
        lambda p0 = FlyTrap: typePassthrough(p0)],
    'FlyTrap T5': [
        lambda p0 = RancidFlyTrap: typePassthrough(p0)],
    'FlyTrap T8': [
        lambda p0 = AncientFlyTrap: typePassthrough(p0)],
    'Stump T8': [
        lambda p0 = Stump: typePassthrough(p0)],
    'Stump T9': [
        lambda p0 = TwistedStump: typePassthrough(p0)],
    'Navy T1': [
        lambda p0 = Cadet: typePassthrough(p0)],
    'Navy T2': [
        lambda p0 = Guard: typePassthrough(p0)],
    'Navy T3': [
        lambda p0 = Marine: typePassthrough(p0)],
    'Navy T4': [
        lambda p0 = Sergeant: typePassthrough(p0)],
    'Navy T5': [
        lambda p0 = Veteran: typePassthrough(p0)],
    'Navy T6': [
        lambda p0 = Officer: typePassthrough(p0)],
    'Navy T7': [
        lambda p0 = Dragoon: typePassthrough(p0)],
    'EITC T4': [
        lambda p0 = Thug: typePassthrough(p0)],
    'EITC T5': [
        lambda p0 = Grunt: typePassthrough(p0)],
    'EITC T6': [
        lambda p0 = Hiredgun: typePassthrough(p0)],
    'EITC T7': [
        lambda p0 = Mercenary: typePassthrough(p0)],
    'EITC T8': [
        lambda p0 = Assassin: typePassthrough(p0)],
    'DJCREW T7': [
        lambda p0 = 0: pickWaterUndead(p0, p0)],
    'DJCREW T8': [
        lambda p0 = 1, p1 = 2: pickWaterUndead(p0, p1)],
    'DJCREW T9': [
        lambda p0 = 3, p1 = 4: pickWaterUndead(p0, p1)],
    'DJCREW T10': [
        lambda p0 = 5, p1 = 6: pickWaterUndead(p0, p1)],
    'DJCREW T11': [
        lambda p0 = 7, p1 = 8: pickWaterUndead(p0, p1)],
    'Ghost T7': [
        lambda p0 = Revenant: typePassthrough(p0)],
    'Ghost T9': [
        lambda p0 = 1, p1 = 2: pickGhost(p0, p1)],
    'GhostTest': [
        lambda p0 = 1, p1 = 2: pickGhost(p0, p1)],
    'Ghost T10': [
        lambda p0 = TraitorGhost: typePassthrough(p0)],
    'KillerGhost T11': [
        lambda p0 = RageGhost: typePassthrough(p0)],
    'Mutineer Ghost': [
        lambda p0 = MutineerGhost: typePassthrough(p0)],
    'Devious Ghost': [
        lambda p0 = DeviousGhost: typePassthrough(p0)],
    'VoodooZombie T4': [
        lambda p0 = 0, p1 = 0: pickVoodooZombie(p0, p1)],
    'VoodooZombie T5': [
        lambda p0 = 1, p1 = 1: pickVoodooZombie(p0, p1)],
    'VoodooZombie T6': [
        lambda p0 = 2, p1 = 2: pickVoodooZombie(p0, p1)],
    'VoodooZombie T7': [
        lambda p0 = 3, p1 = 3: pickVoodooZombie(p0, p1)],
    'VoodooZombie T8': [
        lambda p0 = 4, p1 = 4: pickVoodooZombie(p0, p1)],
    'VoodooZombie T9': [
        lambda p0 = 5, p1 = 5: pickVoodooZombie(p0, p1)],
    'VoodooZombie T10': [
        lambda p0 = 6, p1 = 6: pickVoodooZombie(p0, p1)],
    'VoodooZombie Boss': [
        lambda p0 = LaSchafe: typePassthrough(p0)],
    'BountyHunter T5': [
        lambda p0 = PettyHunter: typePassthrough(p0)],
    'BountyHunter T6': [
        lambda p0 = BailHunter: typePassthrough(p0)],
    'BountyHunter T7': [
        lambda p0 = ScallyWagHunter: typePassthrough(p0)],
    'BountyHunter T8': [
        lambda p0 = BanditHunter: typePassthrough(p0)],
    'BountyHunter T9': [
        lambda p0 = PirateHunter: typePassthrough(p0)],
    'BountyHunter T10': [
        lambda p0 = WitchHunter: typePassthrough(p0)],
    'BountyHunter T11': [
        lambda p0 = MasterHunter: typePassthrough(p0)],
    'Noob Skeleton': [
        lambda p0 = 0: pickEarthUndead(p0, p0)],
    'Low Skeleton': [
        lambda p0 = 0, p1 = 1: pickEarthUndead(p0, p1)],
    'Early Skeleton': [
        lambda p0 = 1, p1 = 3: pickEarthUndead(p0, p1)],
    'Mid Skeleton': [
        lambda p0 = 3, p1 = 5: pickEarthUndead(p0, p1)],
    'Mean Skeleton': [
        lambda p0 = 5, p1 = 7: pickEarthUndead(p0, p1)],
    'High Skeleton': [
        lambda p0 = 7, p1 = 9: pickEarthUndead(p0, p1)],
    'Fierce Skeleton': [
        lambda p0 = 9, p1 = 11: pickEarthUndead(p0, p1)],
    'Elite Skeleton': [
        lambda p0 = 10, p1 = 12: pickEarthUndead(p0, p1)],
    'Low EITC': [
        lambda p0 = 1: pickTrading(p0, p0)],
    'Mid EITC': [
        lambda p0 = 1, p1 = 3: pickTrading(p0, p1)],
    'High EITC': [
        lambda p0 = 3, p1 = 4: pickTrading(p0, p1)],
    'Crab': [
        lambda p0 = Crab: typePassthrough(p0)],
    'Rock Crab': [
        lambda p0 = RockCrab: typePassthrough(p0)],
    'Giant Crab': [
        lambda p0 = GiantCrab: typePassthrough(p0)],
    'Devourer Crab': [
        lambda p0 = CrusherCrab: typePassthrough(p0)],
    'Scorpion': [
        lambda p0 = Scorpion: typePassthrough(p0)],
    'Dread Scorpion': [
        lambda p0 = DreadScorpion: typePassthrough(p0)],
    'Alligator': [
        lambda p0 = Alligator: typePassthrough(p0)],
    'Bayou Gator': [
        lambda p0 = BayouGator: typePassthrough(p0)],
    'Big Gator': [
        lambda p0 = BigGator: typePassthrough(p0)],
    'Huge Gator': [
        lambda p0 = HugeGator: typePassthrough(p0)],
    'Bat': [
        lambda p0 = Bat: typePassthrough(p0)],
    'Rabid Bat': [
        lambda p0 = RabidBat: typePassthrough(p0)],
    'Vampire Bat': [
        lambda p0 = VampireBat: typePassthrough(p0)],
    'Wasp': [
        lambda p0 = Wasp: typePassthrough(p0)],
    'Angry Wasp': [
        lambda p0 = AngryWasp: typePassthrough(p0)],
    'Soldier Wasp': [
        lambda p0 = SoldierWasp: typePassthrough(p0)],
    'FlyTrap': [
        lambda p0 = FlyTrap: typePassthrough(p0)],
    'Stump': [
        lambda p0 = Stump: typePassthrough(p0)],
    'Twisted Stump': [
        lambda p0 = TwistedStump: typePassthrough(p0)],
    'Noob Navy': [
        lambda p0 = 0: pickNavy(p0, p0)],
    'Low Navy': [
        lambda p0 = 0, p1 = 1: pickNavy(p0, p1)],
    'Mid Navy': [
        lambda p0 = 2, p1 = 3: pickNavy(p0, p1)],
    'High Navy': [
        lambda p0 = 4, p1 = 5: pickNavy(p0, p1)],
    'Low DJCrew': [
        lambda p0 = 0, p1 = 1: pickWaterUndead(p0, p1)],
    'Early DJCrew': [
        lambda p0 = 1, p1 = 2: pickWaterUndead(p0, p1)],
    'Mid DJCrew': [
        lambda p0 = 2, p1 = 3: pickWaterUndead(p0, p1)],
    'Mean DJCrew': [
        lambda p0 = 3, p1 = 4: pickWaterUndead(p0, p1)],
    'High DJCrew': [
        lambda p0 = 4, p1 = 5: pickWaterUndead(p0, p1)],
    'Fierce DJCrew': [
        lambda p0 = 5, p1 = 6: pickWaterUndead(p0, p1)],
    'Elite DJCrew': [
        lambda p0 = 6, p1 = 7: pickWaterUndead(p0, p1)],
    'Area': [
        lambda p0 = 0, p1 = 3: pickEarthUndead(p0, p1)],
    'French Undead': [
        lambda p0 = 0, p1 = 3: pickFrenchUndead(p0, p1)],
    'French Undead Low': [
        lambda p0 = 0, p1 = 1: pickFrenchUndead(p0, p1)],
    'French Undead Mid': [
        lambda p0 = 1, p1 = 2: pickFrenchUndead(p0, p1)],
    'French Undead High': [
        lambda p0 = 2, p1 = 3: pickFrenchUndead(p0, p1)],
    'French Undead Maitre': [
        lambda p0 = FrenchUndeadA: typePassthrough(p0)],
    'French Undead Quarter Master': [
        lambda p0 = FrenchUndeadB: typePassthrough(p0)],
    'French Undead Lieutenant': [
        lambda p0 = FrenchUndeadC: typePassthrough(p0)],
    'French Undead Capitaine': [
        lambda p0 = FrenchUndeadD: typePassthrough(p0)],
    'French Undead Boss': [
        lambda p0 = FrenchBossA: typePassthrough(p0)],
    'Spanish Undead': [
        lambda p0 = 0, p1 = 3: pickSpanishUndead(p0, p1)],
    'Spanish Undead Low': [
        lambda p0 = 0, p1 = 1: pickSpanishUndead(p0, p1)],
    'Spanish Undead Mid': [
        lambda p0 = 1, p1 = 2: pickSpanishUndead(p0, p1)],
    'Spanish Undead High': [
        lambda p0 = 2, p1 = 3: pickSpanishUndead(p0, p1)],
    'Spanish Undead Conquistador': [
        lambda p0 = SpanishUndeadA: typePassthrough(p0)],
    'Spanish Undead Bandido': [
        lambda p0 = SpanishUndeadB: typePassthrough(p0)],
    'Spanish Undead Pirata': [
        lambda p0 = SpanishUndeadC: typePassthrough(p0)],
    'Spanish Undead Captain': [
        lambda p0 = SpanishUndeadD: typePassthrough(p0)],
    'Spanish Undead Boss': [
        lambda p0 = SpanishBossA: typePassthrough(p0)] }
NPC_SPAWNABLES_KEYS = [
    'Skel T0',
    'Skel T1',
    'Skel T2',
    'Skel T3',
    'Skel T4',
    'Skel T5',
    'Skel T6',
    'Skel T7',
    'Skel T8',
    'Crab T0',
    'Crab T1',
    'Crab T3',
    'Crab T5',
    'Crab T6',
    'Scorp T1',
    'Scorp T3',
    'Scorp T5',
    'Gator T1',
    'Gator T2',
    'Gator T4',
    'Gator T5',
    'Bat T1',
    'Bat T2',
    'Bat T4',
    'Bat T8',
    'Wasp T3',
    'Wasp T4',
    'Wasp T5',
    'Wasp T6',
    'FlyTrap T4',
    'FlyTrap T5',
    'FlyTrap T8',
    'Stump T8',
    'Stump T9',
    'Navy T1',
    'Navy T2',
    'Navy T3',
    'Navy T4',
    'Navy T5',
    'Navy T6',
    'Navy T7',
    'EITC T4',
    'EITC T5',
    'EITC T6',
    'EITC T7',
    'EITC T8',
    'DJCREW T7',
    'DJCREW T8',
    'DJCREW T9',
    'DJCREW T10',
    'DJCREW T11',
    'Ghost T7',
    'Ghost T9',
    'Ghost T10',
    'KillerGhost T11',
    'Mutineer Ghost',
    'Devious Ghost',
    'VoodooZombie T4',
    'VoodooZombie T5',
    'VoodooZombie T6',
    'VoodooZombie T7',
    'VoodooZombie T8',
    'VoodooZombie T9',
    'VoodooZombie T10',
    'VoodooZombie Boss',
    'BountyHunter T5',
    'BountyHunter T6',
    'BountyHunter T7',
    'BountyHunter T8',
    'BountyHunter T9',
    'BountyHunter T10',
    'BountyHunter T11',
    'Noob Skeleton',
    'Low Skeleton',
    'Early Skeleton',
    'Mid Skeleton',
    'Mean Skeleton',
    'High Skeleton',
    'Fierce Skeleton',
    'Elite Skeleton',
    'Low EITC',
    'Mid EITC',
    'High EITC',
    'Crab',
    'Rock Crab',
    'Giant Crab',
    'Scorpion',
    'Dread Scorpion',
    'Alligator',
    'Bayou Gator',
    'Big Gator',
    'Huge Gator',
    'Bat',
    'Rabid Bat',
    'Vampire Bat',
    'Wasp',
    'Angry Wasp',
    'Soldier Wasp',
    'FlyTrap',
    'Stump',
    'Twisted Stump',
    'Noob Navy',
    'Low Navy',
    'Mid Navy',
    'High Navy',
    'Low DJCrew',
    'Early DJCrew',
    'Mid DJCrew',
    'Mean DJCrew',
    'High DJCrew',
    'Fierce DJCrew',
    'Elite DJCrew',
    'Area',
    'French Undead',
    'French Undead Low',
    'French Undead Mid',
    'French Undead High',
    'French Undead Maitre',
    'French Undead Quarter Master',
    'French Undead Lieutenant',
    'French Undead Capitaine',
    'Spanish Undead',
    'Spanish Undead Low',
    'Spanish Undead Mid',
    'Spanish Undead High',
    'Spanish Undead Conquistador',
    'Spanish Undead Bandido',
    'Spanish Undead Pirata',
    'Spanish Undead Captain']

def buildEditorSpawnableTypes():
    category = [
        [
            [
                'Cadet',
                'Guard',
                'Marine',
                'Sergeant',
                'Veteran',
                'Officer',
                'Dragoon'],
            'Navy - '],
        [
            [
                'Thug',
                'Grunt',
                'Hiredgun',
                'Mercenary',
                'Assassin'],
            'EITC - '],
        [
            [
                'Clod',
                'Sludge',
                'Mire',
                'MireKnife',
                'Muck',
                'MuckCutlass',
                'Corpse',
                'CorpseCutlass',
                'Carrion',
                'CarrionKnife',
                'Cadaver',
                'CadaverCutlass',
                'Zombie',
                'CaptMudmoss',
                'Mossman',
                'Drip',
                'Damp',
                'Drizzle',
                'Spray',
                'Splatter',
                'Drool',
                'Drench',
                'Douse',
                'CaptBriney',
                'Spout'],
            'Undead - ']]
    for currCategory in category:
        for currType in currCategory[0]:
            name = currCategory[1] + currType
            NPC_SPAWNABLES[name] = [
                lambda p0 = eval(currType): typePassthrough(p0)]
            NPC_SPAWNABLES_KEYS.append(name)
        
    

buildEditorSpawnableTypes()

def pickPokerUndead(possibles = None):
    if not possibles:
        possibles = [
            EarthUndead[1],
            EarthUndead[6],
            EarthUndead[7],
            EarthUndead[8],
            EarthUndead[10],
            EarthUndead[14],
            FrenchUndeadA,
            FrenchUndeadC,
            FrenchUndeadD,
            SpanishUndeadA,
            SpanishUndeadB,
            SpanishUndeadC,
            SpanishUndeadD]
    
    return (random.choice(possibles), possibles)

