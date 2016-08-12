#from libpandaexpress import ConfigVariableBool
from pandac.PandaModules import *
from direct.showbase.PythonUtil import *
from direct.showbase import AppRunnerGlobal
from pirates.pirate import AvatarTypes
from pirates.battle import EnemyGlobals
from pirates.ship import ShipGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.battle import EnemyGlobals
import DropData
import string
import random
import os

__dropInfo = DropData.dropInfo
__commonDropInfo = DropData.commonDropInfo

__lootDropCache = { }
__lootStoreCache = { }
__lootShipCache = { }
__staticCommonDropList = { }
__typeCommonDropList = { }
__shipMaterialDropList = { }

__columnHeadings = __dropInfo.pop('columnHeadings')

for (heading, value) in __commonDropInfo.items():
    if value == 'x':
        value = 1
    else:
        value = 0
    
    try:
        newHeading = string.replace(heading, '\r', '')
        id = None
        exec 'id = (AvatarTypes.%s.getFaction(), AvatarTypes.%s.getTrack(), AvatarTypes.%s.getId())' % (heading, heading, heading)
        exec '__typeCommonDropList[id] = %s' % value in globals()
    except:
        newHeading = string.replace(heading, '\r', '')
        exec "__staticCommonDropList['%s'] = %s" % (newHeading, value) in globals()

def isLive(item):
    if ConfigVariableBool('force-all-items-live', False):
        return True
    
    isLive = item[__columnHeadings['IS_LIVE']]
    return isLive

__containerDropRate = {
    EnemyGlobals.RED: 45.0,
    EnemyGlobals.YELLOW: 45.0,
    EnemyGlobals.GREEN: 20.0,
    EnemyGlobals.GREY: 8.0 }

def getContainerDropRate(enemyGrade):
    dropRate = __containerDropRate.get(enemyGrade)
    if dropRate:
        return dropRate
    else:
        return 0

__containerTypeRate = {
    1: (100, 0, 0),
    2: (99, 1, 0),
    3: (98, 2, 0),
    4: (97, 3, 0),
    5: (96, 4, 0),
    6: (95, 5, 0),
    7: (94, 6, 0),
    8: (93, 7, 0),
    9: (92, 8, 0),
    10: (91, 8, 1),
    11: (90, 9, 1),
    12: (89, 10, 1),
    13: (88, 11, 1),
    14: (87, 12, 1),
    15: (86, 12, 2),
    16: (85, 13, 2),
    17: (84, 14, 2),
    18: (83, 15, 2),
    19: (82, 16, 2),
    20: (81, 16, 3),
    21: (80, 17, 3),
    22: (79, 18, 3),
    23: (78, 19, 3),
    24: (77, 20, 3),
    25: (76, 20, 4),
    26: (76, 20, 4),
    27: (76, 20, 4),
    28: (76, 20, 4),
    29: (76, 20, 4),
    30: (75, 20, 5),
    31: (75, 20, 5),
    32: (75, 20, 5),
    33: (75, 20, 5),
    34: (75, 20, 5),
    35: (75, 20, 5),
    36: (75, 20, 5),
    37: (75, 20, 5),
    38: (75, 20, 5),
    39: (75, 20, 5),
    40: (75, 20, 5),
    41: (75, 20, 5),
    42: (75, 20, 5),
    43: (75, 20, 5),
    44: (75, 20, 5),
    45: (75, 20, 5),
    46: (75, 20, 5),
    47: (75, 20, 5),
    48: (75, 20, 5),
    49: (75, 20, 5),
    50: (75, 20, 5),
    51: (75, 20, 5),
    52: (75, 20, 5),
    53: (75, 20, 5),
    54: (75, 20, 5),
    55: (75, 20, 5),
    56: (75, 20, 5),
    57: (75, 20, 5),
    58: (75, 20, 5),
    59: (75, 20, 5),
    60: (75, 20, 5),
    61: (75, 20, 5),
    62: (75, 20, 5),
    63: (75, 20, 5),
    64: (75, 20, 5),
    65: (75, 20, 5),
    66: (75, 20, 5),
    67: (75, 20, 5),
    68: (75, 20, 5),
    69: (75, 20, 5),
    70: (75, 20, 5),
    71: (75, 20, 5),
    72: (75, 20, 5),
    73: (75, 20, 5),
    74: (75, 20, 5),
    75: (75, 20, 5),
    76: (75, 20, 5),
    77: (75, 20, 5),
    78: (75, 20, 5),
    79: (75, 20, 5),
    80: (75, 20, 5) }

def getContainerTypeRate(enemyLevel):
    typeRate = __containerTypeRate.get(enemyLevel)
    if typeRate:
        return typeRate
    else:
        return (0, 0, 0)

__numItemsRate = {
    PiratesGlobals.ITEM_SAC: (40, 35, 20, 5, 0, 0),
    PiratesGlobals.TREASURE_CHEST: (0, 25, 40, 25, 10, 0),
    PiratesGlobals.RARE_CHEST: (0, 10, 25, 30, 25, 10) }

def getNumItemsRate(containerType):
    numItemsRate = __numItemsRate.get(containerType)
    if numItemsRate:
        return numItemsRate
    else:
        return (0, 0, 0, 0, 0, 0)

__itemTypeRate = {
    PiratesGlobals.ITEM_SAC: (0.29999999999999999, 0.20000000000000001, 0.14999999999999999, 0.10000000000000001, 0.050000000000000003, 0.080000000000000002, 0.12),
    PiratesGlobals.TREASURE_CHEST: (0.29999999999999999, 0.25, 0.14999999999999999, 0.10000000000000001, 0.10000000000000001, 0.10000000000000001, 0.0),
    PiratesGlobals.RARE_CHEST: (0.29999999999999999, 0.20000000000000001, 0.14999999999999999, 0.10000000000000001, 0.10000000000000001, 0.14999999999999999, 0.0) }

def getItemTypeRate(containerType):
    itemTypeRate = __itemTypeRate.get(containerType)
    if itemTypeRate:
        return itemTypeRate
    else:
        return (1.0, 0, 0, 0, 0, 0, 0)

__itemRarityRate = {
    PiratesGlobals.ITEM_SAC: (0.75490000000000002, 0.20000000000000001, 0.044999999999999998, 0.0001, 0.0),
    PiratesGlobals.TREASURE_CHEST: (0.41979, 0.47999999999999998, 0.10000000000000001, 0.00020000000000000001, 1.0000000000000001e-005),
    PiratesGlobals.RARE_CHEST: (0.0, 0.72414999999999996, 0.25, 0.025000000000000001, 0.00084999999999999995) }

def getItemRarityRate(containerType):
    itemRarityRate = __itemRarityRate.get(containerType)
    if itemRarityRate:
        return itemRarityRate
    else:
        return (1.0, 0, 0, 0, 0, 0, 0)


def getAllItemIds():
    return __dropInfo.keys()

__shipTypeList = {
    ShipGlobals.NAVY_FERRET: __commonDropInfo['NAVY_FERRET'],
    ShipGlobals.NAVY_BULWARK: __commonDropInfo['NAVY_BULWARK'],
    ShipGlobals.NAVY_PANTHER: __commonDropInfo['NAVY_PANTHER'],
    ShipGlobals.NAVY_GREYHOUND: __commonDropInfo['NAVY_GREYHOUND'],
    ShipGlobals.NAVY_VANGUARD: __commonDropInfo['NAVY_VANGUARD'],
    ShipGlobals.NAVY_CENTURION: __commonDropInfo['NAVY_CENTURION'],
    ShipGlobals.NAVY_KINGFISHER: __commonDropInfo['NAVY_KINGFISHER'],
    ShipGlobals.NAVY_MONARCH: __commonDropInfo['NAVY_MONARCH'],
    ShipGlobals.NAVY_MAN_O_WAR: __commonDropInfo['NAVY_MAN_O_WAR'],
    ShipGlobals.NAVY_PREDATOR: __commonDropInfo['NAVY_PREDATOR'],
    ShipGlobals.NAVY_COLOSSUS: __commonDropInfo['NAVY_COLOSSUS'],
    ShipGlobals.NAVY_DREADNOUGHT: __commonDropInfo['NAVY_DREADNOUGHT'],
    ShipGlobals.EITC_SEA_VIPER: __commonDropInfo['EITC_SEA_VIPER'],
    ShipGlobals.EITC_SENTINEL: __commonDropInfo['EITC_SENTINEL'],
    ShipGlobals.EITC_CORVETTE: __commonDropInfo['EITC_CORVETTE'],
    ShipGlobals.EITC_BLOODHOUND: __commonDropInfo['EITC_BLOODHOUND'],
    ShipGlobals.EITC_IRONWALL: __commonDropInfo['EITC_IRONWALL'],
    ShipGlobals.EITC_MARAUDER: __commonDropInfo['EITC_MARAUDER'],
    ShipGlobals.EITC_BARRACUDA: __commonDropInfo['EITC_BARRACUDA'],
    ShipGlobals.EITC_OGRE: __commonDropInfo['EITC_OGRE'],
    ShipGlobals.EITC_WARLORD: __commonDropInfo['EITC_WARLORD'],
    ShipGlobals.EITC_CORSAIR: __commonDropInfo['EITC_CORSAIR'],
    ShipGlobals.EITC_BEHEMOTH: __commonDropInfo['EITC_BEHEMOTH'],
    ShipGlobals.SKEL_PHANTOM: __commonDropInfo['SKEL_PHANTOM'],
    ShipGlobals.SKEL_REVENANT: __commonDropInfo['SKEL_REVENANT'],
    ShipGlobals.SKEL_STORM_REAPER: __commonDropInfo['SKEL_STORM_REAPER'],
    ShipGlobals.SKEL_BLACK_HARBINGER: __commonDropInfo['SKEL_BLACK_HARBINGER'],
    ShipGlobals.SKEL_DEATH_OMEN: __commonDropInfo['SKEL_DEATH_OMEN'],
    ShipGlobals.SKEL_SHADOW_CROW_SP: __commonDropInfo['SKEL_SHADOW_CROW_SP'],
    ShipGlobals.SKEL_HELLHOUND_SP: __commonDropInfo['SKEL_HELLHOUND_SP'],
    ShipGlobals.SKEL_BLOOD_SCOURGE_SP: __commonDropInfo['SKEL_BLOOD_SCOURGE_SP'],
    ShipGlobals.SKEL_SHADOW_CROW_FR: __commonDropInfo['SKEL_SHADOW_CROW_FR'],
    ShipGlobals.SKEL_HELLHOUND_FR: __commonDropInfo['SKEL_HELLHOUND_FR'],
    ShipGlobals.SKEL_BLOOD_SCOURGE_FR: __commonDropInfo['SKEL_BLOOD_SCOURGE_FR'],
    ShipGlobals.GOLIATH: __commonDropInfo['GOLIATH'],
    ShipGlobals.FLYING_DUTCHMAN: __commonDropInfo['FLYING_DUTCHMAN'],
    ShipGlobals.JOLLY_ROGER: __commonDropInfo['JOLLY_ROGER']}

def getShipMaterialDropByClass(shipClass):
    materialDropType = __shipMaterialDropList.get(shipClass, 0)
    return materialDropType

getShipMaterialDropByClass(ShipGlobals.HUNTER_VENGEANCE)

def getShipDropItemsByClass(shipClass):
    dropItems = []
    shipType = __shipTypeList.get(shipClass)
    if __lootShipCache.has_key(shipClass):
        return __lootShipCache[shipClass]
    
    for itemId in __dropInfo:
        item = __dropInfo[itemId]
        if not isLive(item):
            continue
        
        if item[DROPS_FROM_ALL_SHIPS]:
            dropItems.append(itemId)
        
        if shipType and shipType < len(item):
            if item[shipType]:
                dropItems.append(itemId)
            
        item[shipType]
    
    __lootShipCache[shipClass] = dropItems
    return dropItems

__enemyTypeList = {
   AvatarTypes.Cadet: __commonDropInfo['Cadet'],
    AvatarTypes.Guard: __commonDropInfo['Guard'],
    AvatarTypes.Marine: __commonDropInfo['Marine'],
    AvatarTypes.Sergeant: __commonDropInfo['Sergeant'],
    AvatarTypes.Veteran: __commonDropInfo['Veteran'],
    AvatarTypes.Officer: __commonDropInfo['Officer'],
    AvatarTypes.Dragoon: __commonDropInfo['Dragoon'],
    AvatarTypes.Thug: __commonDropInfo['Thug'],
    AvatarTypes.Grunt: __commonDropInfo['Grunt'],
    AvatarTypes.Hiredgun: __commonDropInfo['Hiredgun'],
    AvatarTypes.Mercenary: __commonDropInfo['Mercenary'],
    AvatarTypes.Assassin: __commonDropInfo['Assassin'],
    AvatarTypes.Clod: __commonDropInfo['Clod'],
    AvatarTypes.Sludge: __commonDropInfo['Sludge'],
    AvatarTypes.Mire: __commonDropInfo['Mire'],
    AvatarTypes.MireKnife: __commonDropInfo['MireKnife'],
    AvatarTypes.Muck: __commonDropInfo['Muck'],
    AvatarTypes.MuckCutlass: __commonDropInfo['MuckCutlass'],
    AvatarTypes.Corpse: __commonDropInfo['Corpse'],
    AvatarTypes.CorpseCutlass: __commonDropInfo['CorpseCutlass'],
    AvatarTypes.Carrion: __commonDropInfo['Carrion'],
    AvatarTypes.CarrionKnife: __commonDropInfo['CarrionKnife'],
    AvatarTypes.Cadaver: __commonDropInfo['Cadaver'],
    AvatarTypes.CadaverCutlass: __commonDropInfo['CadaverCutlass'],
    AvatarTypes.Zombie: __commonDropInfo['Zombie'],
    AvatarTypes.CaptMudmoss: __commonDropInfo['CaptMudmoss'],
    AvatarTypes.Revenant: __commonDropInfo['Revenant'],
    AvatarTypes.RageGhost: __commonDropInfo['RageGhost'],
    AvatarTypes.MutineerGhost: __commonDropInfo['MutineerGhost'],
    AvatarTypes.DeviousGhost: __commonDropInfo['DeviousGhost'],
    AvatarTypes.TraitorGhost: __commonDropInfo['TraitorGhost'],
    AvatarTypes.PressGangVoodooZombie: __commonDropInfo['PressGangVoodooZombie'],
    AvatarTypes.CookVoodooZombie: __commonDropInfo['CookVoodooZombie'],
    AvatarTypes.SwabbieVoodooZombie: __commonDropInfo['SwabbieVoodooZombie'],
    AvatarTypes.LookoutVoodooZombie: __commonDropInfo['LookoutVoodooZombie'],
    AvatarTypes.AngryVoodooZombie: __commonDropInfo['AngryVoodooZombie'],
    AvatarTypes.OfficerVoodooZombie: __commonDropInfo['OfficerVoodooZombie'],
    AvatarTypes.SlaveDriverVoodooZombie: __commonDropInfo['SlaveDriverVoodooZombie'],
    AvatarTypes.PettyHunter: __commonDropInfo['PressGangVoodooZombie'],
    AvatarTypes.BailHunter: __commonDropInfo['CookVoodooZombie'],
    AvatarTypes.ScallyWagHunter: __commonDropInfo['SwabbieVoodooZombie'],
    AvatarTypes.BanditHunter: __commonDropInfo['LookoutVoodooZombie'],
    AvatarTypes.PirateHunter: __commonDropInfo['AngryVoodooZombie'],
    AvatarTypes.WitchHunter: __commonDropInfo['OfficerVoodooZombie'],
    AvatarTypes.MasterHunter: __commonDropInfo['SlaveDriverVoodooZombie'],
    AvatarTypes.SpanishUndeadA: __commonDropInfo['SpanishUndeadA'],
    AvatarTypes.SpanishUndeadB: __commonDropInfo['SpanishUndeadB'],
    AvatarTypes.SpanishUndeadC: __commonDropInfo['SpanishUndeadC'],
    AvatarTypes.SpanishUndeadD: __commonDropInfo['SpanishUndeadD'],
    AvatarTypes.SpanishBossA: __commonDropInfo['SpanishUndeadD'],
    AvatarTypes.FrenchUndeadA: __commonDropInfo['FrenchUndeadA'],
    AvatarTypes.FrenchUndeadB: __commonDropInfo['FrenchUndeadB'],
    AvatarTypes.FrenchUndeadC: __commonDropInfo['FrenchUndeadC'],
    AvatarTypes.FrenchUndeadD: __commonDropInfo['FrenchUndeadD'],
    AvatarTypes.FrenchBossA: __commonDropInfo['FrenchUndeadD'],
    AvatarTypes.Drip: __commonDropInfo['Drip'],
    AvatarTypes.Damp: __commonDropInfo['Damp'],
    AvatarTypes.Drizzle: __commonDropInfo['Drizzle'],
    AvatarTypes.Spray: __commonDropInfo['Spray'],
    AvatarTypes.Splatter: __commonDropInfo['Splatter'],
    AvatarTypes.Drool: __commonDropInfo['Drool'],
    AvatarTypes.Drench: __commonDropInfo['Drench'],
    AvatarTypes.Douse: __commonDropInfo['Douse'],
    AvatarTypes.CaptBriney: __commonDropInfo['CaptBriney'],
    AvatarTypes.Crab: __commonDropInfo['Crab'],
    AvatarTypes.StoneCrab: __commonDropInfo['StoneCrab'],
    AvatarTypes.RockCrab: __commonDropInfo['RockCrab'],
    AvatarTypes.GiantCrab: __commonDropInfo['GiantCrab'],
    AvatarTypes.CrusherCrab: __commonDropInfo['CrusherCrab'],
    AvatarTypes.Scorpion: __commonDropInfo['Scorpion'],
    AvatarTypes.DireScorpion: __commonDropInfo['DireScorpion'],
    AvatarTypes.DreadScorpion: __commonDropInfo['DreadScorpion'],
    AvatarTypes.Alligator: __commonDropInfo['Alligator'],
    AvatarTypes.BayouGator: __commonDropInfo['BayouGator'],
    AvatarTypes.BigGator: __commonDropInfo['BigGator'],
    AvatarTypes.HugeGator: __commonDropInfo['HugeGator'],
    AvatarTypes.FlyTrap: __commonDropInfo['Flytrap'],
    AvatarTypes.RancidFlyTrap: __commonDropInfo['RancidFlytrap'],
    AvatarTypes.AncientFlyTrap: __commonDropInfo['AncientFlytrap'],
    AvatarTypes.Stump: __commonDropInfo['Stump'],
    AvatarTypes.TwistedStump: __commonDropInfo['TwistedStump'],
    AvatarTypes.Wasp: __commonDropInfo['Wasp'],
    AvatarTypes.KillerWasp: __commonDropInfo['KillerWasp'],
    AvatarTypes.AngryWasp: __commonDropInfo['AngryWasp'],
    AvatarTypes.SoldierWasp: __commonDropInfo['SoldierWasp'],
    AvatarTypes.Bat: __commonDropInfo['Bat'],
    AvatarTypes.RabidBat: __commonDropInfo['RabidBat'],
    AvatarTypes.VampireBat: __commonDropInfo['VampireBat'],
    AvatarTypes.FireBat: __commonDropInfo['FireBat'],
    AvatarTypes.WillBurybones: __commonDropInfo['WillBurybones'],
    AvatarTypes.FoulCrenshaw: __commonDropInfo['FoulCrenshaw'],
    AvatarTypes.EvanTheDigger: __commonDropInfo['EvanTheDigger'],
    AvatarTypes.ThadIllFortune: __commonDropInfo['ThadIllFortune'],
    AvatarTypes.SimonButcher: __commonDropInfo['SimonButcher'],
    AvatarTypes.ThaddeusWoodworm: __commonDropInfo['ThaddeusWoodworm'],
    AvatarTypes.Bonebreaker: __commonDropInfo['Bonebreaker'],
    AvatarTypes.GideonGrog: __commonDropInfo['GideonGrog'],
    AvatarTypes.WhitWidowmaker: __commonDropInfo['WhitWidowmaker'],
    AvatarTypes.Blackheart: __commonDropInfo['Blackheart'],
    AvatarTypes.FrancisFaust: __commonDropInfo['FrancisFaust'],
    AvatarTypes.JeremyColdhand: __commonDropInfo['JeremyColdhand'],
    AvatarTypes.Stench: __commonDropInfo['Stench'],
    AvatarTypes.GeoffreyPain: __commonDropInfo['GeoffreyPain'],
    AvatarTypes.HughBrandish: __commonDropInfo['HughBrandish'],
    AvatarTypes.NathanielGrimm: __commonDropInfo['NathanielGrimm'],
    AvatarTypes.SidShiver: __commonDropInfo['SidShiver'],
    AvatarTypes.IanRamjaw: __commonDropInfo['IanRamjaw'],
    AvatarTypes.SandStalker: __commonDropInfo['SandStalker'],
    AvatarTypes.ManRipper: __commonDropInfo['ManRipper'],
    AvatarTypes.ClawChief: __commonDropInfo['ClawChief'],
    AvatarTypes.Bowbreaker: __commonDropInfo['Bowbreaker'],
    AvatarTypes.SnapDragon: __commonDropInfo['SnapDragon'],
    AvatarTypes.RipTail: __commonDropInfo['RipTail'],
    AvatarTypes.SilentStinger: __commonDropInfo['SilentStinger'],
    AvatarTypes.Bonecracker: __commonDropInfo['Bonecracker'],
    AvatarTypes.Trapjaw: __commonDropInfo['Trapjaw'],
    AvatarTypes.SwampTerror: __commonDropInfo['SwampTerror'],
    AvatarTypes.Frightfang: __commonDropInfo['Frightfang'],
    AvatarTypes.Bloodleach: __commonDropInfo['Bloodleach'],
    AvatarTypes.Firesting: __commonDropInfo['Firesting'],
    AvatarTypes.Devilwing: __commonDropInfo['Devilwing'],
    AvatarTypes.CarlosCudgel: __commonDropInfo['CarlosCudgel'],
    AvatarTypes.ZachariahSharp: __commonDropInfo['ZachariahSharp'],
    AvatarTypes.HenryFlint: __commonDropInfo['HenryFlint'],
    AvatarTypes.PhineasFowl: __commonDropInfo['PhineasFowl'],
    AvatarTypes.EdwardLohand: __commonDropInfo['EdwardLohand']}
__ignoreEnemyTypeList = [
    AvatarTypes.Pirate,
    AvatarTypes.Flicker,
    AvatarTypes.Spark,
    AvatarTypes.TradingCo,
    AvatarTypes.CaptZephyr,
    AvatarTypes.Fiend,
    AvatarTypes.Scallywag,
    AvatarTypes.Swashbuckler,
    AvatarTypes.Whiff,
    AvatarTypes.Billow,
    AvatarTypes.Shade,
    AvatarTypes.Spout,
    AvatarTypes.Creature,
    AvatarTypes.Phantom,
    AvatarTypes.CaptCinderbones,
    AvatarTypes.Townfolk,
    AvatarTypes.Mossman,
    AvatarTypes.SeaSerpent,
    AvatarTypes.Undead,
    AvatarTypes.Glint,
    AvatarTypes.Smolder,
    AvatarTypes.Warmonger,
    AvatarTypes.Imp,
    AvatarTypes.Brand,
    AvatarTypes.Squall,
    AvatarTypes.Lumen,
    AvatarTypes.Landlubber,
    AvatarTypes.Buccaneer,
    AvatarTypes.Reek,
    AvatarTypes.Navy,
    AvatarTypes.Specter,
    AvatarTypes.Wraith,
    AvatarTypes.Torch,
    AvatarTypes.Seagull,
    AvatarTypes.Raven,
    AvatarTypes.Monkey,
    AvatarTypes.BomberZombie,
    AvatarTypes.JollyRoger,
    AvatarTypes.CrewGhost,
    AvatarTypes.LeaderGhost,
    AvatarTypes.VoodooZombieBoss]
for baseStat in EnemyGlobals.__baseAvatarStats:
    pass


def isValidEnemy(type, uniqueId):
    if not __staticIdTypeList.get(uniqueId):
        pass
    return __enemyTypeList.get(type)


def getEnemyDropItemsByType(type, uniqueId):
    shouldUseCommonDrop = 1
    isStatic = 0
    dropKey = None
    if __staticCommonDropList.has_key(uniqueId):
        shouldUseCommonDrop = __staticCommonDropList[uniqueId]
        isStatic = 1
        dropKey = uniqueId
    else:
        typeKey = (type.getFaction(), type.getTrack(), type.getId())
        if __typeCommonDropList.has_key(typeKey):
            shouldUseCommonDrop = __typeCommonDropList[typeKey]
            dropKey = typeKey
        
    dropItems = []
    enemyType = __staticIdTypeList.get(uniqueId)
    isBoss = 1
    if not enemyType:
        enemyType = __enemyTypeList.get(type)
    
    if dropKey and __lootDropCache.has_key(dropKey):
        return __lootDropCache[dropKey]
    
    for itemId in __dropInfo:
        item = __dropInfo[itemId]
        if not isLive(item):
            continue
        
        if shouldUseCommonDrop and item[DROPS_FROM_ALL_ENEMIES]:
            dropItems.append(itemId)
        
        if enemyType and enemyType < len(item):
            if item[enemyType]:
                dropItems.append(itemId)
            
        item[enemyType]
    
    if dropKey:
        __lootDropCache[dropKey] = dropItems
    
    return dropItems
    if dropKey:
        __lootDropCache[dropKey] = dropItems
    
    return dropItems


def getStoreItems(uniqueId):
    storeItems = []
    shopKeeper = __staticIdTypeList.get(uniqueId)
    if shopKeeper:
        if __lootStoreCache.has_key(uniqueId):
            return __lootStoreCache[uniqueId]
        
        for itemId in __dropInfo:
            item = __dropInfo[itemId]
            if not isLive(item):
                continue
            
            if item[shopKeeper]:
                storeItems.append(itemId)
                continue
        
    
    __lootStoreCache[uniqueId] = storeItems
    return storeItems


def getMakeAPirateClothing():
    mapClothing = []
    for itemId in __dropInfo:
        item = __dropInfo[itemId]
        if not isLive(item):
            continue
        
        if item[MakeAPirate]:
            mapClothing.append(itemId)
            continue
    
    return mapClothing


def getQuestPropItems():
    qpItems = []
    for itemId in __dropInfo:
        item = __dropInfo[itemId]
        if not isLive(item):
            continue
        
        if item[QuestProp]:
            qpItems.append(itemId)
            continue
    
    return qpItems

__fishTables = []
for index in [
    __commonDropInfo['FishSmall'],
    __commonDropInfo['FishMed'],
    __commonDropInfo['FishLarge'],
    __columnHeadings['FishLegendary']]:
    dropTable = []
    for (itemId, item) in __dropInfo.iteritems():
        if not isLive(item):
            continue
        
        if index < len(item):
            if item[index]:
                dropTable.append(itemId)
            
        
    
    __fishTables.append(dropTable)


def getFishDrops(size):
    return __fishTables[size]


def createZippedDist(unsummedDist, outcomes):
    hundredSum = abs(sum(unsummedDist) - 100) < 0.10000000000000001
    if hundredSum:
        return _[1]([ sum(unsummedDist[:x]) for x in range(len(unsummedDist)) ], outcomes)
    
    return None


def rollDistribution(zippedDist):
    roll = random.uniform(0, 100)
    return _[1][-1][1]

