# File: I (Python 2.4)

from pirates.ship import ShipGlobals
from pirates.pirate import AvatarTypes
from pirates.piratesbase import PiratesGlobals
from pandac.PandaModules import Point3, Vec4
from pirates.quest.QuestConstants import NPCIds
from pirates.ai import HolidayGlobals
from pirates.world.LocationConstants import LocationIds
from pirates.uberdog.UberDogGlobals import InventoryType
JOLLY_ROGER_INVASION_SHIP = ShipGlobals.JOLLY_ROGER
JOLLY_UNIQUE_ID = '1248740229.97robrusso'
JOLLY_DISENGAGE_LIMIT = 1
JOLLY_DISENGAGE_TIME = 5.0
JOLLY_ATTACK_TIME = 2.0
BOSS_WAIT_TIME = 120
INVASION_PORT_ROYAL = HolidayGlobals.INVASIONPORTROYAL
INVASION_TORTUGA = HolidayGlobals.INVASIONTORTUGA
INVASION_DEL_FUEGO = HolidayGlobals.INVASIONDELFUEGO
INVASION_IDS = [
    HolidayGlobals.getHolidayName(INVASION_PORT_ROYAL),
    HolidayGlobals.getHolidayName(INVASION_TORTUGA),
    HolidayGlobals.getHolidayName(INVASION_DEL_FUEGO)]
INVASION_NUMBERS = [
    INVASION_PORT_ROYAL,
    INVASION_TORTUGA,
    INVASION_DEL_FUEGO]
ISLAND_IDS = {
    INVASION_PORT_ROYAL: LocationIds.PORT_ROYAL_ISLAND,
    INVASION_TORTUGA: LocationIds.TORTUGA_ISLAND,
    INVASION_DEL_FUEGO: LocationIds.DEL_FUEGO_ISLAND,
    HolidayGlobals.WRECKEDGOVERNORSMANSION: LocationIds.PORT_ROYAL_ISLAND,
    HolidayGlobals.WRECKEDFAITHFULBRIDE: LocationIds.TORTUGA_ISLAND,
    HolidayGlobals.WRECKEDDELFUEGOTOWN: LocationIds.DEL_FUEGO_ISLAND }

def getIslandId(holiday):
    return ISLAND_IDS[holiday]

REMOVABLE_SPAWN_PTS = {
    INVASION_PORT_ROYAL: [
        '1158366723.53dparis',
        '1158366673.28dparis',
        '1158366574.17dparis',
        '1178667776.0dxschafe0',
        '1178667776.0dxschafe1',
        '1184632064.0dxschafe',
        '1178667904.0dxschafe',
        '1178668288.0dxschafe0',
        '1178667776.0dxschafe'],
    INVASION_TORTUGA: [],
    INVASION_DEL_FUEGO: [] }

def getRemovableSpawnPts(holiday):
    return REMOVABLE_SPAWN_PTS[holiday]

LOSS_HOLIDAYS = {
    INVASION_PORT_ROYAL: HolidayGlobals.WRECKEDGOVERNORSMANSION,
    INVASION_TORTUGA: HolidayGlobals.WRECKEDFAITHFULBRIDE,
    INVASION_DEL_FUEGO: HolidayGlobals.WRECKEDDELFUEGOTOWN }

def getLossHoliday(holiday):
    return LOSS_HOLIDAYS[holiday]

SCREEN_INFO = {
    INVASION_PORT_ROYAL: [
        (0.75, 0, -0.65000000000000002),
        0.00055000000000000003],
    INVASION_TORTUGA: [
        (0.75, 0, -0.65000000000000002),
        0.00080000000000000004],
    INVASION_DEL_FUEGO: [
        (0.75, 0, -0.68000000000000005),
        0.00044999999999999999] }

def getScreenInfo(holiday):
    return SCREEN_INFO[holiday]

LOSS_FIRES = {
    INVASION_PORT_ROYAL: [
        [
            (0.81999999999999995, 0, -0.29199999999999998),
            (-0.45000000000000001, 0.45000000000000001, 0.45000000000000001)],
        [
            (0.83999999999999997, 0, -0.29499999999999998),
            0.59999999999999998],
        [
            (0.86499999999999999, 0, -0.28999999999999998),
            0.45000000000000001]],
    INVASION_TORTUGA: [
        [
            (0.83999999999999997, 0, -0.47999999999999998),
            0.59999999999999998]],
    INVASION_DEL_FUEGO: [
        [
            (0.95999999999999996, 0, -0.69999999999999996),
            0.69999999999999996],
        [
            (0.91000000000000003, 0, -0.68000000000000005),
            (-0.59999999999999998, 0.59999999999999998, 0.59999999999999998)],
        [
            (0.93000000000000005, 0, -0.71999999999999997),
            0.59999999999999998]] }

def getLossFires(holiday):
    return LOSS_FIRES[holiday]

TOWNFOLK_IDS = {
    INVASION_PORT_ROYAL: [
        NPCIds.EDWARD_STORMHAWK,
        NPCIds.SAM_SEABONES,
        NPCIds.FLECTHER_BEAKMAN,
        NPCIds.DARBY_DRYDOCK,
        NPCIds.LUCINDA,
        NPCIds.CASSANDRA,
        NPCIds.EMMA,
        NPCIds.JAMES_MACDOUGAL,
        NPCIds.EDWARD_SHACKLEBY,
        NPCIds.CLAYTON_COLLARD,
        NPCIds.ENSIGN_GRIMM,
        NPCIds.ANGEL_OBONNEY,
        NPCIds.ROSE_SEAFELLOW],
    INVASION_TORTUGA: [
        NPCIds.ORINDA,
        NPCIds.HORATIO_FOWLER,
        NPCIds.O_MALLEY,
        NPCIds.FABIOLA,
        NPCIds.SCARLET,
        NPCIds.HENDRY_CUTTS,
        NPCIds.BUTCHER_BROWN,
        NPCIds.BIG_PHIL],
    INVASION_DEL_FUEGO: [
        NPCIds.ROMANY_BEV,
        NPCIds.SHOCHETT_PRYMME,
        NPCIds.VALENTINA,
        NPCIds.ROLAND_RAGGART,
        NPCIds.OLIVIER,
        NPCIds.HENRY_LOWMAN,
        NPCIds.BALTHASAR,
        NPCIds.PELAGIA,
        NPCIds.HEARTLESS_ROSALINE,
        NPCIds.CLEMENCE_BASILSHOT] }

def getTownfolkIds(holiday):
    return TOWNFOLK_IDS[holiday]

START_MESSAGE_RANGE = {
    INVASION_PORT_ROYAL: 1,
    INVASION_TORTUGA: 1,
    INVASION_DEL_FUEGO: 1 }

def getStartMessageRange(holiday):
    return range(0, START_MESSAGE_RANGE[holiday])

SECOND_WAVE_MESSAGE_RANGE = {
    INVASION_PORT_ROYAL: 1,
    INVASION_TORTUGA: 1,
    INVASION_DEL_FUEGO: 1 }

def getSecondWaveMessageRange(holiday):
    return range(0, SECOND_WAVE_MESSAGE_RANGE[holiday])

LAST_WAVE_MESSAGE_RANGE = {
    INVASION_PORT_ROYAL: 1,
    INVASION_TORTUGA: 1,
    INVASION_DEL_FUEGO: 1 }

def getLastWaveMessageRange(holiday):
    return range(0, LAST_WAVE_MESSAGE_RANGE[holiday])

PHASE_MESSAGE_RANGE = {
    INVASION_PORT_ROYAL: 25,
    INVASION_TORTUGA: 24,
    INVASION_DEL_FUEGO: 23 }

def getPhaseMessageRange(holiday):
    return range(0, PHASE_MESSAGE_RANGE[holiday])

GOOD_BOSS_MESSAGE_RANGE = {
    INVASION_PORT_ROYAL: 4,
    INVASION_TORTUGA: 4,
    INVASION_DEL_FUEGO: 4 }

def getGoodBossMessageRange(holiday):
    return range(0, GOOD_BOSS_MESSAGE_RANGE[holiday])

BAD_BOSS_MESSAGE_RANGE = {
    INVASION_PORT_ROYAL: 1,
    INVASION_TORTUGA: 1,
    INVASION_DEL_FUEGO: 1 }

def getBadBossMessageRange(holiday):
    return range(0, BAD_BOSS_MESSAGE_RANGE[holiday])

LOW_HEALTH_MESSAGE_RANGE = {
    INVASION_PORT_ROYAL: 2,
    INVASION_TORTUGA: 2,
    INVASION_DEL_FUEGO: 2 }

def getLowHealthMessageRange(holiday):
    return range(0, LOW_HEALTH_MESSAGE_RANGE[holiday])

WIN_MESSAGE_RANGE = {
    INVASION_PORT_ROYAL: 1,
    INVASION_TORTUGA: 1,
    INVASION_DEL_FUEGO: 1 }

def getWinMessageRange(holiday):
    return range(0, WIN_MESSAGE_RANGE[holiday])

LOSE_MESSAGE_RANGE = {
    INVASION_PORT_ROYAL: 3,
    INVASION_TORTUGA: 1,
    INVASION_DEL_FUEGO: 3 }

def getLoseMessageRange(holiday):
    return range(0, LOSE_MESSAGE_RANGE[holiday])

TOTAL_SPAWN_ZONE_LIST = {
    INVASION_PORT_ROYAL: 8,
    INVASION_TORTUGA: 7,
    INVASION_DEL_FUEGO: 8 }

def getTotalSpawnZones(holiday):
    return TOTAL_SPAWN_ZONE_LIST[holiday]

SPAWN_ZONE_LIST = {
    INVASION_PORT_ROYAL: ([
        1,
        2,
        3,
        4], [
        1,
        2,
        3,
        4,
        5], [
        1,
        2,
        3,
        5,
        6], [
        1,
        3,
        5,
        6,
        7], [
        1,
        3,
        5,
        6,
        7,
        8]),
    INVASION_TORTUGA: ([
        1,
        2,
        3,
        4], [
        1,
        2,
        3,
        5], [
        1,
        2,
        3,
        5,
        6], [
        1,
        2,
        3,
        5,
        6,
        7]),
    INVASION_DEL_FUEGO: ([
        1,
        2,
        3,
        4], [
        1,
        3,
        4,
        5], [
        1,
        3,
        4,
        5,
        7], [
        1,
        3,
        4,
        5,
        6,
        7], [
        1,
        3,
        5,
        6,
        7,
        8]) }

def getSpawnZones(holiday, numPlayers):
    if holiday == INVASION_PORT_ROYAL or holiday == INVASION_DEL_FUEGO:
        if numPlayers < 41:
            return SPAWN_ZONE_LIST[holiday][0]
        elif numPlayers < 71:
            return SPAWN_ZONE_LIST[holiday][1]
        elif numPlayers < 101:
            return SPAWN_ZONE_LIST[holiday][2]
        elif numPlayers < 131:
            return SPAWN_ZONE_LIST[holiday][3]
        else:
            return SPAWN_ZONE_LIST[holiday][4]
    elif holiday == INVASION_TORTUGA:
        if numPlayers < 21:
            return SPAWN_ZONE_LIST[holiday][0]
        elif numPlayers < 41:
            return SPAWN_ZONE_LIST[holiday][1]
        elif numPlayers < 81:
            return SPAWN_ZONE_LIST[holiday][2]
        else:
            return SPAWN_ZONE_LIST[holiday][3]
    

TOTAL_PHASE_LIST = {
    INVASION_PORT_ROYAL: 7,
    INVASION_TORTUGA: 7,
    INVASION_DEL_FUEGO: 7 }

def getTotalPhases(holiday):
    return TOTAL_PHASE_LIST[holiday]

PHASE_1_ENEMIES = [
    AvatarTypes.Mire,
    AvatarTypes.Mire,
    AvatarTypes.Mire,
    AvatarTypes.Mire,
    AvatarTypes.Mire,
    AvatarTypes.Mire,
    AvatarTypes.Mire,
    AvatarTypes.Muck,
    AvatarTypes.Muck]
PHASE_2_ENEMIES = [
    AvatarTypes.MuckCutlass,
    AvatarTypes.MuckCutlass,
    AvatarTypes.MuckCutlass,
    AvatarTypes.MuckCutlass,
    AvatarTypes.MuckCutlass,
    AvatarTypes.MuckCutlass,
    AvatarTypes.Muck,
    AvatarTypes.Muck,
    AvatarTypes.Muck]
PHASE_3_ENEMIES = [
    AvatarTypes.Muck,
    AvatarTypes.Muck,
    AvatarTypes.Muck,
    AvatarTypes.Muck,
    AvatarTypes.SpanishUndeadA,
    AvatarTypes.SpanishUndeadA,
    AvatarTypes.SpanishUndeadA,
    AvatarTypes.SpanishUndeadB,
    AvatarTypes.SpanishUndeadB]
PHASE_4_ENEMIES = [
    AvatarTypes.FrenchUndeadA,
    AvatarTypes.FrenchUndeadA,
    AvatarTypes.FrenchUndeadB,
    AvatarTypes.FrenchUndeadB,
    AvatarTypes.FrenchUndeadC,
    AvatarTypes.Muck,
    AvatarTypes.Muck,
    AvatarTypes.Muck,
    AvatarTypes.Cadaver]
PHASE_5_ENEMIES = [
    AvatarTypes.Muck,
    AvatarTypes.Muck,
    AvatarTypes.CorpseCutlass,
    AvatarTypes.CorpseCutlass,
    AvatarTypes.CorpseCutlass,
    AvatarTypes.SpanishUndeadC,
    AvatarTypes.SpanishUndeadC,
    AvatarTypes.Cadaver,
    AvatarTypes.Cadaver]
PHASE_6_ENEMIES = [
    AvatarTypes.Cadaver,
    AvatarTypes.Cadaver,
    AvatarTypes.Cadaver,
    AvatarTypes.Muck,
    AvatarTypes.CadaverCutlass,
    AvatarTypes.CadaverCutlass,
    AvatarTypes.CadaverCutlass,
    AvatarTypes.FrenchUndeadD,
    AvatarTypes.SpanishUndeadD]
PHASE_7_ENEMIES = [
    AvatarTypes.CadaverCutlass,
    AvatarTypes.CadaverCutlass,
    AvatarTypes.CaptMudmoss,
    AvatarTypes.CaptMudmoss,
    AvatarTypes.Cadaver,
    AvatarTypes.Cadaver,
    AvatarTypes.Cadaver,
    AvatarTypes.Stump,
    AvatarTypes.Stump]
PHASE_ENEMY_SETS = {
    INVASION_PORT_ROYAL: {
        1: PHASE_1_ENEMIES,
        2: PHASE_2_ENEMIES,
        3: PHASE_3_ENEMIES,
        4: PHASE_4_ENEMIES,
        5: PHASE_5_ENEMIES,
        6: PHASE_6_ENEMIES,
        7: PHASE_7_ENEMIES },
    INVASION_TORTUGA: {
        1: PHASE_1_ENEMIES,
        2: PHASE_2_ENEMIES,
        3: PHASE_3_ENEMIES,
        4: PHASE_4_ENEMIES,
        5: PHASE_5_ENEMIES,
        6: PHASE_6_ENEMIES,
        7: PHASE_7_ENEMIES },
    INVASION_DEL_FUEGO: {
        1: PHASE_1_ENEMIES,
        2: PHASE_2_ENEMIES,
        3: PHASE_3_ENEMIES,
        4: PHASE_4_ENEMIES,
        5: PHASE_5_ENEMIES,
        6: PHASE_6_ENEMIES,
        7: PHASE_7_ENEMIES } }

def getPhaseEnemySets(holiday):
    return PHASE_ENEMY_SETS[holiday]

ENEMY_SPEEDS = {
    INVASION_PORT_ROYAL: 1.0,
    INVASION_TORTUGA: 1.0,
    INVASION_DEL_FUEGO: 1.25 }

def getEnemySpeed(holiday):
    return ENEMY_SPEEDS[holiday]

ENEMY_DURATION_MODIFIER = {
    INVASION_PORT_ROYAL: {
        1: 1.0,
        2: 1.0,
        3: 1.0,
        4: 1.0,
        5: 1.0,
        6: 1.0,
        7: 1.0 },
    INVASION_TORTUGA: {
        1: 1.5,
        2: 1.5,
        3: 1.5,
        4: 1.5,
        5: 1.5,
        6: 1.5,
        7: 1.5 },
    INVASION_DEL_FUEGO: {
        1: 1.0,
        2: 1.0,
        3: 1.0,
        4: 1.0,
        5: 1.0,
        6: 1.0,
        7: 1.0 } }

def getEnemyDurationModifier(holiday, phase):
    return ENEMY_DURATION_MODIFIER[holiday][phase]

BOMBER_ZOMBIE_PROBABILITY = {
    INVASION_PORT_ROYAL: {
        1: 0.0,
        2: 0.59999999999999998,
        3: 0.20000000000000001,
        4: 0.59999999999999998,
        5: 0.20000000000000001,
        6: 0.59999999999999998,
        7: 0.59999999999999998 },
    INVASION_TORTUGA: {
        1: 0.0,
        2: 0.59999999999999998,
        3: 0.59999999999999998,
        4: 0.20000000000000001,
        5: 0.59999999999999998,
        6: 0.20000000000000001,
        7: 0.59999999999999998 },
    INVASION_DEL_FUEGO: {
        1: 0.59999999999999998,
        2: 0.20000000000000001,
        3: 0.59999999999999998,
        4: 0.20000000000000001,
        5: 0.20000000000000001,
        6: 0.59999999999999998,
        7: 0.59999999999999998 } }

def getBomberZombieProbability(holiday, phase):
    return BOMBER_ZOMBIE_PROBABILITY[holiday][phase]

BOMBER_ZOMBIE_PERCENT = {
    INVASION_PORT_ROYAL: {
        1: 0.0,
        2: 0.050000000000000003,
        3: 0.40000000000000002,
        4: 0.050000000000000003,
        5: 0.40000000000000002,
        6: 0.10000000000000001,
        7: 0.10000000000000001 },
    INVASION_TORTUGA: {
        1: 0.0,
        2: 0.050000000000000003,
        3: 0.050000000000000003,
        4: 0.40000000000000002,
        5: 0.10000000000000001,
        6: 0.40000000000000002,
        7: 0.10000000000000001 },
    INVASION_DEL_FUEGO: {
        1: 0.050000000000000003,
        2: 0.40000000000000002,
        3: 0.10000000000000001,
        4: 0.40000000000000002,
        5: 0.40000000000000002,
        6: 0.10000000000000001,
        7: 0.10000000000000001 } }

def getBomberZombiePercent(holiday, phase):
    return BOMBER_ZOMBIE_PERCENT[holiday][phase]

ENEMY_START_PATH_POS_LIST = {
    INVASION_PORT_ROYAL: {
        1: (-61.023200000000003, -192.34299999999999, 11.1546),
        2: (534.14099999999996, -379.63299999999998, 4.2278799999999999),
        3: (339.46499999999997, -461.702, 6.6303700000000001),
        4: (13.4009, -284.65899999999999, 4.0318399999999999),
        5: (226.34299999999999, -315.48500000000001, 13.9557),
        6: None,
        7: None,
        8: None,
        10: (-61.023200000000003, -192.34299999999999, 11.1546),
        11: (339.46499999999997, -461.702, 6.6303700000000001) },
    INVASION_TORTUGA: {
        1: (77.754199999999997, -392.56099999999998, 1.39463),
        2: (107.408, -401.54700000000003, 0.17516100000000001),
        3: (316.505, -256.69400000000002, 0.72986600000000001),
        4: (337.154, -174.624, 0.43289800000000001),
        5: None,
        6: None,
        7: None,
        10: (77.754199999999997, -392.56099999999998, 1.39463),
        11: (316.505, -256.69400000000002, 0.72986600000000001) },
    INVASION_DEL_FUEGO: {
        1: (-1300.7, -493.17099999999999, 0.84996400000000005),
        2: (-1292.3199999999999, -551.34000000000003, 3.20932),
        3: (-1489.03, 362.41699999999997, 5.0126099999999996),
        4: (-1277.6900000000001, 554.61099999999999, 1.5143800000000001),
        5: (-1089.0799999999999, -190.33500000000001, 0.69436799999999999),
        6: None,
        7: (-1177.8499999999999, 18.596599999999999, 0.72250899999999996),
        8: None,
        10: (-1300.7, -493.17099999999999, 0.84996400000000005),
        11: (-1489.03, 362.41699999999997, 5.0126099999999996),
        12: (-1277.6900000000001, 554.61099999999999, 1.5143800000000001) } }

def getEnemyStartPathPos(holiday, zone):
    return ENEMY_START_PATH_POS_LIST[holiday][zone]

TOTAL_CAPTURE_POINT_LIST = {
    INVASION_PORT_ROYAL: 7,
    INVASION_TORTUGA: 7,
    INVASION_DEL_FUEGO: 7,
    HolidayGlobals.getHolidayName(INVASION_PORT_ROYAL): 7,
    HolidayGlobals.getHolidayName(INVASION_TORTUGA): 7,
    HolidayGlobals.getHolidayName(INVASION_DEL_FUEGO): 7 }

def getTotalCapturePoints(holiday):
    return TOTAL_CAPTURE_POINT_LIST[holiday]

CAPTURE_POINT_TARGET_LIST = {
    INVASION_PORT_ROYAL: {
        1: [
            1,
            5,
            7],
        2: [
            2,
            4,
            6,
            7],
        3: [
            2,
            3,
            4,
            6,
            7],
        4: [
            1,
            5,
            7],
        5: [
            3,
            4,
            6,
            7],
        6: [
            6,
            7],
        7: [
            5,
            7],
        8: [
            7],
        10: [
            1,
            5,
            7],
        11: [
            2,
            4,
            6,
            7] },
    INVASION_TORTUGA: {
        1: [
            1,
            3,
            5,
            7],
        2: [
            1,
            3,
            5,
            7],
        3: [
            2,
            4,
            6,
            7],
        4: [
            2,
            4,
            6,
            7],
        5: [
            5,
            7],
        6: [
            6,
            7],
        7: [
            7],
        10: [
            1,
            3,
            5,
            7],
        11: [
            2,
            4,
            6,
            7] },
    INVASION_DEL_FUEGO: {
        1: [
            1,
            4,
            7],
        2: [
            1,
            4,
            7],
        3: [
            2,
            5,
            7],
        4: [
            3,
            6,
            7],
        5: [
            4,
            7],
        6: [
            6,
            7],
        7: [
            5,
            7],
        8: [
            7],
        10: [
            1,
            4,
            7],
        11: [
            2,
            5,
            7],
        12: [
            3,
            6,
            7] } }

def getCapturePointTargetList(holiday):
    return CAPTURE_POINT_TARGET_LIST[holiday]

CAPTURE_POINT_HP_LIST = {
    INVASION_PORT_ROYAL: {
        1: 5000,
        2: 5000,
        3: 5000,
        4: 5000,
        5: 14000,
        6: 14000,
        7: 40000 },
    INVASION_TORTUGA: {
        1: 5000,
        2: 5000,
        3: 5000,
        4: 5000,
        5: 12000,
        6: 12000,
        7: 40000 },
    INVASION_DEL_FUEGO: {
        1: 5000,
        2: 5000,
        3: 5000,
        4: 14000,
        5: 14000,
        6: 14000,
        7: 40000 } }

def getCapturePointHp(holiday, zone):
    return CAPTURE_POINT_HP_LIST[holiday][zone]

CAPTURE_POINT_PATH_POS_LIST = {
    INVASION_PORT_ROYAL: {
        1: Point3(-59.115099999999998, -187.47800000000001, 12.366),
        2: Point3(372.50799999999998, -466.79399999999998, 3.9878200000000001),
        3: Point3(130.95099999999999, -261.16899999999998, 38.2806),
        4: Point3(391.33499999999998, -247.47800000000001, 13.9557),
        5: Point3(-126.583, 64.003299999999996, 35.809800000000003),
        6: Point3(221.399, 80.805599999999998, 35.611699999999999),
        7: Point3(47.390300000000003, 350.27699999999999, 85.597499999999997) },
    INVASION_TORTUGA: {
        1: Point3(57.605499999999999, -346.39600000000002, 5.6463400000000004),
        2: Point3(222.423, -169.90100000000001, 6.7190300000000001),
        3: Point3(43.6479, -120.363, 16.763500000000001),
        4: Point3(281.65899999999999, 1.409, 8.3959399999999995),
        5: Point3(-28.370000000000001, 58.491, 30.5733),
        6: Point3(318.29399999999998, 126.935, 12.182),
        7: None },
    INVASION_DEL_FUEGO: {
        1: Point3(-1244.6900000000001, -547.20000000000005, 11.288),
        2: Point3(-1336.1600000000001, 268.50900000000001, 10.651300000000001),
        3: Point3(-1260.9400000000001, 471.589, 5.9409700000000001),
        4: None,
        5: Point3(-1199.04, 55.629100000000001, 2.19007),
        6: Point3(-918.65999999999997, 400.49799999999999, 15.0496),
        7: None } }

def getCapturePointPathPos(holiday, zone):
    return CAPTURE_POINT_PATH_POS_LIST[holiday][zone]

CAPTURE_POINT_LOW_HP_PERCENT_LIST = {
    INVASION_PORT_ROYAL: 0.25,
    INVASION_TORTUGA: 0.25,
    INVASION_DEL_FUEGO: 0.25 }

def getCapturePointLowHpPercent(holiday):
    return CAPTURE_POINT_LOW_HP_PERCENT_LIST[holiday]

CAPTURE_POINT_TARGETS = {
    INVASION_DEL_FUEGO: {
        4: {
            1: [
                1,
                2],
            2: [
                1,
                2],
            5: [
                0,
                3] } } }

def getCapturePointTargets(holiday, zone, spawnZone):
    if CAPTURE_POINT_TARGETS.get(holiday) and CAPTURE_POINT_TARGETS.get(holiday).get(zone):
        return CAPTURE_POINT_TARGETS.get(holiday).get(zone).get(spawnZone)
    

MAIN_CAPTURE_POINT_TARGETS = {
    INVASION_TORTUGA: {
        1: [
            1,
            2],
        2: [
            1,
            2],
        3: [
            0,
            3],
        4: [
            0,
            3],
        5: [
            1,
            2],
        6: [
            0,
            3],
        7: [
            1,
            2],
        10: [
            1,
            2],
        11: [
            0,
            3] },
    INVASION_DEL_FUEGO: {
        1: [
            0,
            3],
        2: [
            0,
            3],
        3: [
            1,
            4,
            5,
            7,
            8],
        4: [
            2],
        5: [
            0,
            3],
        6: [
            2],
        7: [
            1,
            4,
            5,
            7,
            8],
        8: [
            6,
            9],
        10: [
            1,
            4,
            5,
            7,
            8],
        11: [
            1,
            4,
            5,
            7,
            8],
        12: [
            1,
            4,
            5,
            7,
            8] } }

def getMainCapturePointTargets(holiday, spawnZone):
    if MAIN_CAPTURE_POINT_TARGETS.get(holiday):
        return MAIN_CAPTURE_POINT_TARGETS.get(holiday).get(spawnZone)
    

MAIN_CAPTURE_POINT_HP_POS = {
    HolidayGlobals.getHolidayName(INVASION_PORT_ROYAL): Point3(290, 620, 0),
    HolidayGlobals.getHolidayName(INVASION_TORTUGA): Point3(130, 230, 0),
    HolidayGlobals.getHolidayName(INVASION_DEL_FUEGO): Point3(600, -100, 0) }

def getMainCapturePointHpPos(holiday):
    return MAIN_CAPTURE_POINT_HP_POS[holiday]

BOSS_ENEMY_LIST = {
    INVASION_PORT_ROYAL: AvatarTypes.JollyRoger,
    INVASION_TORTUGA: AvatarTypes.JollyRoger,
    INVASION_DEL_FUEGO: AvatarTypes.JollyRoger }

def getBossEnemy(holiday):
    return BOSS_ENEMY_LIST[holiday]

BOSS_ID_LIST = {
    INVASION_PORT_ROYAL: '1248740229.97robrusso',
    INVASION_TORTUGA: '1248740229.97robrusso',
    INVASION_DEL_FUEGO: '1248740229.97robrusso' }

def getBossId(holiday):
    return BOSS_ID_LIST[holiday]

BOSS_TRIGGER_LIST = {
    INVASION_PORT_ROYAL: [
        (1, 5),
        (2, 4, 6)],
    INVASION_TORTUGA: [
        (1, 3, 5),
        (2, 4, 6)],
    INVASION_DEL_FUEGO: [
        (1, 4),
        (2, 5),
        (3, 6)] }

def getBossTriggers(holiday):
    return BOSS_TRIGGER_LIST[holiday]

BOSS_NPC_LIST = {
    INVASION_PORT_ROYAL: ([
        1.0,
        1.0,
        1.0,
        0.5,
        0.11], [
        1.0,
        1.25,
        2.0,
        0.59999999999999998,
        0.10000000000000001], [
        1.0,
        1.5,
        3.0,
        0.69999999999999996,
        0.089999999999999997], [
        1.0,
        1.75,
        4.0,
        0.80000000000000004,
        0.080000000000000002], [
        1.0,
        2.0,
        5.0,
        0.90000000000000002,
        0.070000000000000007], [
        1.0,
        2.25,
        6.0,
        1.0,
        0.059999999999999998], [
        1.0,
        2.5,
        7.0,
        1.1000000000000001,
        0.050000000000000003], [
        1.0,
        2.75,
        8.0,
        1.2,
        0.040000000000000001], [
        1.0,
        3.0,
        9.0,
        1.3,
        0.029999999999999999], [
        1.0,
        3.25,
        10.0,
        1.3999999999999999,
        0.02], [
        1.0,
        3.5,
        11.0,
        1.5,
        0.01], [
        1.0,
        3.75,
        12.0,
        1.6000000000000001,
        0.0080000000000000002], [
        1.0,
        4.0,
        13.0,
        1.7,
        0.0060000000000000001], [
        1.0,
        4.25,
        14.0,
        1.8,
        0.0040000000000000001], [
        1.0,
        4.5,
        15.0,
        1.8999999999999999,
        0.002], [
        1.0,
        4.75,
        16.0,
        2.0,
        0.001], [
        1.0,
        5.0,
        17.0,
        2.1000000000000001,
        0.001], [
        1.0,
        5.25,
        18.0,
        2.2000000000000002,
        0.001]),
    INVASION_TORTUGA: ([
        1.0,
        1.0,
        1.0,
        0.5,
        0.11], [
        1.0,
        1.25,
        2.0,
        0.59999999999999998,
        0.10000000000000001], [
        1.0,
        1.5,
        3.0,
        0.69999999999999996,
        0.089999999999999997], [
        1.0,
        1.75,
        4.0,
        0.80000000000000004,
        0.080000000000000002], [
        1.0,
        2.0,
        5.0,
        0.90000000000000002,
        0.070000000000000007], [
        1.0,
        2.25,
        6.0,
        1.0,
        0.059999999999999998], [
        1.0,
        2.5,
        7.0,
        1.1000000000000001,
        0.050000000000000003], [
        1.0,
        2.75,
        8.0,
        1.2,
        0.040000000000000001], [
        1.0,
        3.0,
        9.0,
        1.3,
        0.029999999999999999], [
        1.0,
        3.25,
        10.0,
        1.3999999999999999,
        0.02], [
        1.0,
        3.5,
        11.0,
        1.5,
        0.01], [
        1.0,
        3.75,
        12.0,
        1.6000000000000001,
        0.0080000000000000002], [
        1.0,
        4.0,
        13.0,
        1.7,
        0.0060000000000000001], [
        1.0,
        4.25,
        14.0,
        1.8,
        0.0040000000000000001], [
        1.0,
        4.5,
        15.0,
        1.8999999999999999,
        0.002], [
        1.0,
        4.75,
        16.0,
        2.0,
        0.001], [
        1.0,
        5.0,
        17.0,
        2.1000000000000001,
        0.001], [
        1.0,
        5.25,
        18.0,
        2.2000000000000002,
        0.001]),
    INVASION_DEL_FUEGO: ([
        1.0,
        1.0,
        1.0,
        0.5,
        0.11], [
        1.0,
        1.25,
        2.0,
        0.59999999999999998,
        0.10000000000000001], [
        1.0,
        1.5,
        3.0,
        0.69999999999999996,
        0.089999999999999997], [
        1.0,
        1.75,
        4.0,
        0.80000000000000004,
        0.080000000000000002], [
        1.0,
        2.0,
        5.0,
        0.90000000000000002,
        0.070000000000000007], [
        1.0,
        2.25,
        6.0,
        1.0,
        0.059999999999999998], [
        1.0,
        2.5,
        7.0,
        1.1000000000000001,
        0.050000000000000003], [
        1.0,
        2.75,
        8.0,
        1.2,
        0.040000000000000001], [
        1.0,
        3.0,
        9.0,
        1.3,
        0.029999999999999999], [
        1.0,
        3.25,
        10.0,
        1.3999999999999999,
        0.02], [
        1.0,
        3.5,
        11.0,
        1.5,
        0.01], [
        1.0,
        3.75,
        12.0,
        1.6000000000000001,
        0.0080000000000000002], [
        1.0,
        4.0,
        13.0,
        1.7,
        0.0060000000000000001], [
        1.0,
        4.25,
        14.0,
        1.8,
        0.0040000000000000001], [
        1.0,
        4.5,
        15.0,
        1.8999999999999999,
        0.002], [
        1.0,
        4.75,
        16.0,
        2.0,
        0.001], [
        1.0,
        5.0,
        17.0,
        2.1000000000000001,
        0.001], [
        1.0,
        5.25,
        18.0,
        2.2000000000000002,
        0.001]) }

def getBossSkills(holiday, numPlayers):
    if numPlayers < 6:
        return BOSS_NPC_LIST[holiday][0]
    elif numPlayers < 11:
        return BOSS_NPC_LIST[holiday][1]
    elif numPlayers < 16:
        return BOSS_NPC_LIST[holiday][2]
    elif numPlayers < 21:
        return BOSS_NPC_LIST[holiday][3]
    elif numPlayers < 26:
        return BOSS_NPC_LIST[holiday][4]
    elif numPlayers < 31:
        return BOSS_NPC_LIST[holiday][5]
    elif numPlayers < 36:
        return BOSS_NPC_LIST[holiday][6]
    elif numPlayers < 41:
        return BOSS_NPC_LIST[holiday][7]
    elif numPlayers < 46:
        return BOSS_NPC_LIST[holiday][8]
    elif numPlayers < 51:
        return BOSS_NPC_LIST[holiday][9]
    elif numPlayers < 56:
        return BOSS_NPC_LIST[holiday][10]
    elif numPlayers < 61:
        return BOSS_NPC_LIST[holiday][11]
    elif numPlayers < 66:
        return BOSS_NPC_LIST[holiday][12]
    elif numPlayers < 71:
        return BOSS_NPC_LIST[holiday][13]
    elif numPlayers < 76:
        return BOSS_NPC_LIST[holiday][14]
    elif numPlayers < 81:
        return BOSS_NPC_LIST[holiday][15]
    elif numPlayers < 86:
        return BOSS_NPC_LIST[holiday][16]
    else:
        return BOSS_NPC_LIST[holiday][17]

BOSS_SPAWN_LIST = {
    INVASION_PORT_ROYAL: {
        0: 10,
        1: 10,
        2: 11,
        3: 11,
        4: 11,
        5: 10,
        6: 11 },
    INVASION_TORTUGA: {
        0: 10,
        1: 10,
        2: 11,
        3: 10,
        4: 11,
        5: 10,
        6: 11 },
    INVASION_DEL_FUEGO: {
        0: 10,
        1: 10,
        2: 11,
        3: 12,
        4: 10,
        5: 11,
        6: 12 } }

def getBossSpawnZone(holiday, zone):
    return BOSS_SPAWN_LIST[holiday][zone]

WARNING_TIME = {
    INVASION_PORT_ROYAL: 1800,
    INVASION_TORTUGA: 1800,
    INVASION_DEL_FUEGO: 1800 }

def getExtraBossStats(numPlayers):
    if numPlayers < 3:
        return (0.0, 0)
    elif numPlayers < 5:
        return (0.050000000000000003, 1)
    elif numPlayers < 7:
        return (0.10000000000000001, 1)
    elif numPlayers < 9:
        return (0.14999999999999999, 2)
    elif numPlayers < 11:
        return (0.20000000000000001, 2)
    elif numPlayers < 13:
        return (0.25, 2)
    elif numPlayers < 15:
        return (0.29999999999999999, 3)
    elif numPlayers < 17:
        return (0.34999999999999998, 3)
    elif numPlayers < 19:
        return (0.40000000000000002, 4)
    elif numPlayers < 21:
        return (0.45000000000000001, 4)
    elif numPlayers < 25:
        return (0.5, 5)
    elif numPlayers < 29:
        return (0.55000000000000004, 5)
    elif numPlayers < 33:
        return (0.59999999999999998, 5)
    elif numPlayers < 37:
        return (0.65000000000000002, 6)
    elif numPlayers < 41:
        return (0.69999999999999996, 6)
    else:
        return (0.75, 6)


def getEnemyStats(numPlayers):
    if numPlayers < 21:
        return (1.25, 0.80000000000000004)
    elif numPlayers < 26:
        return (1.3, 0.80000000000000004)
    elif numPlayers < 31:
        return (1.3500000000000001, 0.75)
    elif numPlayers < 36:
        return (1.3999999999999999, 0.69999999999999996)
    elif numPlayers < 41:
        return (1.5, 0.65000000000000002)
    elif numPlayers < 46:
        return (1.6000000000000001, 0.59999999999999998)
    elif numPlayers < 51:
        return (1.7, 0.55000000000000004)
    elif numPlayers < 56:
        return (1.8, 0.5)
    elif numPlayers < 61:
        return (1.8999999999999999, 0.45000000000000001)
    elif numPlayers < 66:
        return (2.0, 0.40000000000000002)
    elif numPlayers < 71:
        return (2.1000000000000001, 0.34999999999999998)
    elif numPlayers < 76:
        return (2.2000000000000002, 0.29999999999999999)
    elif numPlayers < 81:
        return (2.25, 0.25)
    elif numPlayers < 86:
        return (2.2999999999999998, 0.20000000000000001)
    elif numPlayers < 91:
        return (2.3500000000000001, 0.14999999999999999)
    elif numPlayers < 96:
        return (2.3999999999999999, 0.10000000000000001)
    elif numPlayers < 101:
        return (2.4500000000000002, 0.10000000000000001)
    elif numPlayers < 106:
        return (2.5, 0.10000000000000001)
    elif numPlayers < 111:
        return (2.5499999999999998, 0.10000000000000001)
    else:
        return (2.6000000000000001, 0.10000000000000001)


def getWarningTime(holiday):
    return WARNING_TIME[holiday]

DELAYED_START_LIST = {
    INVASION_PORT_ROYAL: 28.0,
    INVASION_TORTUGA: 28.0,
    INVASION_DEL_FUEGO: 28.0 }

def getDelayedStart(holiday):
    return DELAYED_START_LIST[holiday]

DELAYED_END_LIST = {
    INVASION_PORT_ROYAL: 16.0,
    INVASION_TORTUGA: 24.0,
    INVASION_DEL_FUEGO: 24.0 }

def getDelayedEnd(holiday):
    return DELAYED_END_LIST[holiday]

SEA_ZONE_LIST = {
    INVASION_PORT_ROYAL: {
        1: 10,
        2: 11,
        3: 11,
        4: 10,
        5: 11,
        6: 11,
        7: 10,
        8: 10 },
    INVASION_TORTUGA: {
        1: 10,
        2: 10,
        3: 11,
        4: 11,
        5: 10,
        6: 11,
        7: 10 },
    INVASION_DEL_FUEGO: {
        1: 10,
        2: 10,
        3: 11,
        4: 12,
        5: 10,
        6: 11,
        7: 12,
        8: 10 } }

def getSeaZone(holiday, zone):
    return SEA_ZONE_LIST[holiday][zone]

SPAWN_STAGGER = 2.0

def getExtraWaveSpawnStagger(numPlayers):
    if numPlayers < 3:
        return 5.0
    elif numPlayers < 5:
        return 4.5
    elif numPlayers < 7:
        return 4.0
    elif numPlayers < 9:
        return 3.5
    elif numPlayers < 11:
        return 3.0
    elif numPlayers < 13:
        return 2.5
    elif numPlayers < 15:
        return 2.0
    elif numPlayers < 17:
        return 1.5
    elif numPlayers < 19:
        return 1.0
    elif numPlayers < 21:
        return 0.5
    else:
        return 0.0

CAPTURE_POINT_UPDATE_WAIT = 1.0
CAPTURE_POINT_HP_SPHERE_SIZES = {
    INVASION_PORT_ROYAL: 70,
    INVASION_TORTUGA: 50,
    INVASION_DEL_FUEGO: 60 }

def getCapturePointHpSphereSize(holiday):
    return CAPTURE_POINT_HP_SPHERE_SIZES[holiday]

FOG_COLORS = {
    INVASION_PORT_ROYAL: Vec4(0.10000000000000001, 0.12, 0.029999999999999999, 1),
    INVASION_TORTUGA: Vec4(0.10000000000000001, 0.12, 0.029999999999999999, 1),
    INVASION_DEL_FUEGO: Vec4(0.10000000000000001, 0.12, 0.029999999999999999, 1) }

def getFogColor(holiday):
    return FOG_COLORS[holiday]

FOG_RANGES = {
    INVASION_PORT_ROYAL: (0.0, 150.0),
    INVASION_TORTUGA: (0.0, 150.0),
    INVASION_DEL_FUEGO: (0.0, 150.0) }

def getFogRange(holiday):
    return FOG_RANGES[holiday]

FAR_FOG_RANGES = {
    INVASION_PORT_ROYAL: (350.0, 2000.0),
    INVASION_TORTUGA: (350.0, 2000.0),
    INVASION_DEL_FUEGO: (350.0, 2000.0) }

def getFarFogRange(holiday):
    return FAR_FOG_RANGES[holiday]

INVASION_LIKELIHOOD = {
    INVASION_PORT_ROYAL: 40,
    INVASION_TORTUGA: 30,
    INVASION_DEL_FUEGO: 30 }

def getInvasionLikelihood(holiday):
    return INVASION_LIKELIHOOD[holiday]

PERCENT_REMAINING_FOR_NEW_WAVE = 0.10000000000000001

def getPercentRemainingForExtraWave(holiday, numPlayers):
    if holiday == INVASION_DEL_FUEGO:
        if numPlayers < 36:
            return 0.5
        elif numPlayers < 41:
            return 0.59999999999999998
        else:
            return 0.69999999999999996
    elif numPlayers < 11:
        return 0.0
    elif numPlayers < 16:
        return 0.10000000000000001
    elif numPlayers < 21:
        return 0.20000000000000001
    elif numPlayers < 26:
        return 0.29999999999999999
    elif numPlayers < 31:
        return 0.40000000000000002
    elif numPlayers < 36:
        return 0.5
    elif numPlayers < 41:
        return 0.59999999999999998
    else:
        return 0.69999999999999996

MAIN_ZONE_BONUS = 0.40000000000000002
ENEMY_BONUS = 0.5
BARRICADE_BONUS = 0.14999999999999999
WAVE_BONUS = 0.20000000000000001
MAX_REP_EARNED = 800
POST_INVASION_DURATION = 3 * 24 * 60 * 60
POST_INVASION_FIRE_DURATION = 3600
JR_PATHS = {
    INVASION_PORT_ROYAL: {
        (0, 1): [
            Point3(-43.8825, -239.52799999999999, 3.0362300000000002),
            Point3(-62.3444, -166.50800000000001, 17.970099999999999)],
        (1, 5): [
            Point3(-89.796700000000001, -82.510199999999998, 34.979199999999999),
            Point3(-125.313, 18.784099999999999, 35.202100000000002),
            Point3(-119.152, 65.964600000000004, 36.496299999999998)],
        (5, 7): [
            Point3(-91.265500000000003, 97.487799999999993, 39.968000000000004),
            Point3(-74.246300000000005, 103.105, 42.418999999999997),
            Point3(-26.6557, 176.26900000000001, 58.543300000000002),
            Point3(-11.169600000000001, 257.12400000000002, 78.270600000000002),
            Point3(-5.1377300000000004, 281.09300000000002, 84.187100000000001),
            Point3(26.746700000000001, 335.12799999999999, 84.278899999999993)],
        (0, 2): [
            Point3(399.47800000000001, -452.45400000000001, 3.10073),
            Point3(336.31999999999999, -460.43900000000002, 6.9645900000000003)],
        (2, 4): [
            Point3(297.142, -401.346, 13.9557),
            Point3(369.16199999999998, -330.92399999999998, 13.9557),
            Point3(401.26600000000002, -253.636, 13.9557)],
        (4, 6): [
            Point3(374.89800000000002, -201.071, 13.9557),
            Point3(358.45800000000003, -119.72499999999999, 14.7235),
            Point3(408.25599999999997, -97.515000000000001, 27.8583),
            Point3(418.75400000000002, -74.839500000000001, 32.156300000000002),
            Point3(413.97500000000002, -52.840600000000002, 32.572600000000001),
            Point3(383.27699999999999, -41.351900000000001, 32.842199999999998),
            Point3(376.512, -16.964700000000001, 40.247900000000001),
            Point3(355.75400000000002, 25.1279, 41.265700000000002),
            Point3(328.94499999999999, 57.771299999999997, 41.265700000000002),
            Point3(283.197, 76.101699999999994, 41.265700000000002),
            Point3(227.30500000000001, 82.058599999999998, 35.673000000000002)],
        (6, 7): [
            Point3(200.214, 109.271, 36.329999999999998),
            Point3(195.35900000000001, 119.363, 37.457299999999996),
            Point3(191.92699999999999, 147.958, 38.716700000000003),
            Point3(177.63200000000001, 201.10300000000001, 45.167999999999999),
            Point3(157.167, 211.012, 52.609200000000001),
            Point3(113.697, 223.26300000000001, 65.705699999999993),
            Point3(97.732100000000003, 255.417, 77.661199999999994),
            Point3(92.333699999999993, 277.83499999999998, 83.734999999999999),
            Point3(72.489500000000007, 334.517, 84.278899999999993)] },
    INVASION_TORTUGA: {
        (0, 1): [
            Point3(67.064099999999996, -386.77999999999997, 1.77451),
            Point3(47.445900000000002, -360.07299999999998, 4.2613300000000001)],
        (1, 3): [
            Point3(20.856400000000001, -302.93799999999999, 6.9682899999999997),
            Point3(2.3101400000000001, -265.45499999999998, 7.9302900000000003),
            Point3(10.706300000000001, -202.721, 9.4061800000000009),
            Point3(54.920699999999997, -127.113, 15.4122)],
        (3, 5): [
            Point3(42.513599999999997, -70.045299999999997, 26.859500000000001),
            Point3(23.017600000000002, -46.174599999999998, 29.184699999999999),
            Point3(19.765000000000001, -40.8399, 29.5809),
            Point3(-4.8402799999999999, -27.9147, 30.6739),
            Point3(-32.996099999999998, 7.5726199999999997, 29.533999999999999),
            Point3(-36.860100000000003, 14.503, 29.498799999999999),
            Point3(-33.686599999999999, 33.085999999999999, 30.104099999999999),
            Point3(-32.002899999999997, 75.296199999999999, 30.3034)],
        (5, 7): [
            Point3(-10.7064, 110.148, 30.739100000000001),
            Point3(11.570399999999999, 113.84, 31.1967),
            Point3(53.3613, 111.254, 31.277200000000001)],
        (0, 2): [
            Point3(293.96899999999999, -245.33099999999999, 2.3120699999999998),
            Point3(258.291, -172.62100000000001, 5.2769700000000004)],
        (2, 4): [
            Point3(223.905, -63.030299999999997, 8.7382600000000004),
            Point3(241.803, -27.976400000000002, 8.9124400000000001),
            Point3(280.38499999999999, -2.2440899999999999, 8.3110999999999997)],
        (4, 6): [
            Point3(295.03300000000002, 6.2694900000000002, 8.0641400000000001),
            Point3(322.14400000000001, 21.6205, 7.78477),
            Point3(341.45299999999997, 55.590699999999998, 7.2417299999999996),
            Point3(321.15699999999998, 127.52500000000001, 11.6012)],
        (6, 7): [
            Point3(280.98399999999998, 151.61799999999999, 24.6632),
            Point3(264.34300000000002, 163.02799999999999, 29.543099999999999),
            Point3(226.52500000000001, 186.12100000000001, 31.015000000000001),
            Point3(168.767, 176.928, 31.223199999999999),
            Point3(121.85299999999999, 118.714, 30.219100000000001),
            Point3(116.232, 112.712, 30.164899999999999),
            Point3(106.008, 84.766900000000007, 29.716899999999999),
            Point3(96.012100000000004, 71.973500000000001, 29.7394)] },
    INVASION_DEL_FUEGO: {
        (0, 1): [
            Point3(-1265.0799999999999, -527.94799999999998, 7.72675)],
        (1, 4): [
            Point3(-1246.6300000000001, -473.303, 4.1024200000000004),
            Point3(-1214.0599999999999, -423.88999999999999, 35.6783),
            Point3(-1167.4100000000001, -345.16899999999998, 35.683500000000002),
            Point3(-1137.54, -294.76100000000002, 2.0154899999999998),
            Point3(-1096.9300000000001, -261.44200000000001, 1.23705)],
        (4, 7): [
            Point3(-1029.5799999999999, -199.25, 1.99986),
            Point3(-998.64599999999996, -154.637, 2.1945999999999999)],
        (0, 2): [
            Point3(-1489.5599999999999, 363.81, 5.0125599999999997),
            Point3(-1362.6900000000001, 254.97200000000001, 9.2648100000000007)],
        (2, 5): [
            Point3(-1324.21, 200.345, 11.9518),
            Point3(-1237.5599999999999, 177.173, 9.8909800000000008),
            Point3(-1201.4200000000001, 58.230499999999999, 2.27976)],
        (5, 7): [
            Point3(-1116.76, 46.308900000000001, 4.9343899999999996),
            Point3(-1060.53, -25.010200000000001, 1.86531),
            Point3(-1006.15, -84.643600000000006, 2.1916199999999999)],
        (0, 3): [
            Point3(-1264.8, 531.995, 2.7367300000000001),
            Point3(-1257.1800000000001, 497.70100000000002, 4.5628099999999998)],
        (3, 6): [
            Point3(-1184.4000000000001, 469.41800000000001, 12.3011),
            Point3(-1141.76, 430.48899999999998, 16.1967),
            Point3(-1100.9300000000001, 420.01499999999999, 19.148900000000001),
            Point3(-983.19100000000003, 443.20800000000003, 16.152899999999999),
            Point3(-924.75800000000004, 407.87099999999998, 15.0837),
            Point3(-912.64400000000001, 339.66300000000001, 16.374099999999999),
            Point3(-920.64499999999998, 312.75, 17.7257)],
        (6, 7): [
            Point3(-971.01800000000003, 213.917, 27.072900000000001),
            Point3(-963.09000000000003, 176.19200000000001, 29.774100000000001),
            Point3(-910.649, 133.697, 27.176100000000002),
            Point3(-910.86599999999999, 56.3491, 13.244899999999999),
            Point3(-991.10199999999998, 11.8028, 3.5243099999999998),
            Point3(-1015.01, -64.591200000000001, 2.1813799999999999),
            Point3(-993.32000000000005, -92.504199999999997, 2.2920099999999999)] } }
JR_POINTS = {
    INVASION_PORT_ROYAL: {
        10: [
            0,
            1,
            5,
            7],
        11: [
            0,
            2,
            4,
            6,
            7] },
    INVASION_TORTUGA: {
        10: [
            0,
            1,
            3,
            5,
            7],
        11: [
            0,
            2,
            4,
            6,
            7] },
    INVASION_DEL_FUEGO: {
        10: [
            0,
            1,
            4,
            7],
        11: [
            0,
            2,
            5,
            7],
        12: [
            0,
            3,
            6,
            7] } }

def getJollyPath(holidayId, startPos, endPos, spawnZone):
    points = JR_POINTS[holidayId][spawnZone]
    startIndex = points.index(startPos)
    endIndex = points.index(endPos)
    path = []
    for i in range(startIndex, endIndex):
        path.extend(JR_PATHS[holidayId][(points[i], points[i + 1])])
    
    return path

