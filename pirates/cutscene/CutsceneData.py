# File: C (Python 2.4)

from direct.showbase.PythonUtil import POD
from pirates.cutscene.CutsceneActor import *
from pirates.pirate.AvatarTypes import *
from pirates.ship import ShipGlobals
from pirates.piratesbase import PLocalizer
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfxString
Cutscene1_1_1 = '1.1.1: Jail Break'
Cutscene1_1_2 = '1.1.2: Jail Break (continued)'
Cutscene1_1_5_a = '1.1.5.a: Doggerel Dan and Nell Intro'
Cutscene1_1_5_b = '1.1.5.b: Doggerel Dan and Nell Rush'
Cutscene1_1_5_c = '1.1.5.c: Doggerel Dan and Nell Bye'
Cutscene1_2 = "1.2: Beck's Boat"
Cutscene1_3 = '1.3: Jolly Roger'
Cutscene2_1 = '2.1: Will Turner Sword'
Cutscene2_1_b = '2.1.b: Sword Tut end'
Cutscene2_2 = '2.2: Tia Dalma Compass'
Cutscene2_3 = '2.3: Elizabeth Swan '
Cutscene2_4 = '2.4: Capt Barbossa Intro'
Cutscene2_4_b = '2.4.b: Capt Barbossa Pistol Finish'
Cutscene2_5 = '2.5: Jack Sparrow in Bar'
Cutscene3_1 = '3.1: Sneaking to BlackPearl'
Cutscene3_2 = '3.2: Jack and Joshamee'
Cutscene6_1 = '6.1: Tia Showing Voodoo Doll'
CutsceneNames = [
    Cutscene1_1_1,
    Cutscene1_1_2,
    Cutscene1_1_5_a,
    Cutscene1_1_5_b,
    Cutscene1_1_5_c,
    Cutscene1_2,
    Cutscene1_3,
    Cutscene2_1,
    Cutscene2_1_b,
    Cutscene2_2,
    Cutscene2_3,
    Cutscene2_4,
    Cutscene2_4_b,
    Cutscene2_5,
    Cutscene3_1,
    Cutscene3_2,
    Cutscene6_1]
CutsceneFilenames = {
    Cutscene1_1_1: 'tut_act_1_1_1_jail',
    Cutscene1_1_2: 'tut_act_1_1_2_jail',
    Cutscene1_1_5_a: 'tut_act_1_1_5_a_dan',
    Cutscene1_1_5_b: 'tut_act_1_1_5_b_dan',
    Cutscene1_1_5_c: 'tut_act_1_1_5_c_dan',
    Cutscene1_2: 'tut_act_1_2',
    Cutscene1_3: 'tut_act_1_3_jr',
    Cutscene2_1: 'tut_act_2_1_wt',
    Cutscene2_1_b: 'tut_act_2_1_b_wt',
    Cutscene2_2: 'tut_act_2_2_td',
    Cutscene2_3: 'tut_act_2_3_es',
    Cutscene2_4: 'tut_act_2_4_cb',
    Cutscene2_4_b: 'tut_act_2_4_cb',
    Cutscene2_5: 'tut_act_2_5_js',
    Cutscene3_1: 'tut_act_3_1_bp',
    Cutscene3_2: 'tut_act_3_2_js',
    Cutscene6_1: 'tut_act_6_1_td' }
CutsceneSubtitles = {
    Cutscene1_1_1: [
        {
            'beginTime': 4,
            'text': PLocalizer.CutSubtitle1_1_1__1 }],
    Cutscene1_1_2: [
        {
            'beginTime': 0.5,
            'text': PLocalizer.CutSubtitle1_1_2__1 },
        {
            'beginTime': 2.5,
            'text': PLocalizer.CutSubtitle1_1_2__2 },
        {
            'beginTime': 12.5,
            'text': PLocalizer.CutSubtitle1_1_2__3 },
        {
            'beginTime': 14.300000000000001,
            'text': PLocalizer.CutSubtitle1_1_2__4,
            'endTime': 20.0 }],
    Cutscene1_1_5_a: [
        {
            'beginTime': 1.3999999999999999,
            'text': PLocalizer.CutSubtitle1_1_5_a__1 },
        {
            'beginTime': 4.7999999999999998,
            'text': PLocalizer.CutSubtitle1_1_5_a__2 },
        {
            'beginTime': 10.9,
            'text': PLocalizer.CutSubtitle1_1_5_a__3 },
        {
            'beginTime': 13.199999999999999,
            'text': PLocalizer.CutSubtitle1_1_5_a__4,
            'endTime': 17.780000000000001 },
        {
            'beginTime': 20.0,
            'text': PLocalizer.CutSubtitle1_1_5_a__5 },
        {
            'beginTime': 21.0,
            'text': PLocalizer.CutSubtitle1_1_5_a__6 },
        {
            'beginTime': 25.710000000000001,
            'text': PLocalizer.CutSubtitle1_1_5_a__7 }],
    Cutscene1_1_5_b: [
        {
            'beginTime': 0.5,
            'text': PLocalizer.CutSubtitle1_1_5_b__1 }],
    Cutscene1_1_5_c: [
        {
            'beginTime': 0.40000000000000002,
            'text': PLocalizer.CutSubtitle1_1_5_c__1 },
        {
            'beginTime': 2.9300000000000002,
            'text': PLocalizer.CutSubtitle1_1_5_c__2 },
        {
            'beginTime': 5.7000000000000002,
            'text': PLocalizer.CutSubtitle1_1_5_c__3 },
        {
            'beginTime': 10.199999999999999,
            'text': PLocalizer.CutSubtitle1_1_5_c__4 },
        {
            'beginTime': 13.699999999999999,
            'text': PLocalizer.CutSubtitle1_1_5_c__5 },
        {
            'beginTime': 17.899999999999999,
            'text': PLocalizer.CutSubtitle1_1_5_c__6 },
        {
            'beginTime': 24.359999999999999,
            'text': PLocalizer.CutSubtitle1_1_5_c__7 },
        {
            'beginTime': 26.800000000000001,
            'text': PLocalizer.CutSubtitle1_1_5_c__8 },
        {
            'beginTime': 32.200000000000003,
            'text': PLocalizer.CutSubtitle1_1_5_c__9 },
        {
            'beginTime': 34.609999999999999,
            'text': PLocalizer.CutSubtitle1_1_5_c__10 }],
    Cutscene1_2: [
        {
            'beginTime': 1.55,
            'text': PLocalizer.CutSubtitle1_2_a__1 },
        {
            'beginTime': 3.6499999999999999,
            'text': PLocalizer.CutSubtitle1_2_a__2 },
        {
            'beginTime': 6.4699999999999998,
            'text': PLocalizer.CutSubtitle1_2_a__3 },
        {
            'beginTime': 10.300000000000001,
            'text': PLocalizer.CutSubtitle1_2_b__1 },
        {
            'beginTime': 13.49,
            'text': PLocalizer.CutSubtitle1_2_b__2 },
        {
            'beginTime': 18.359999999999999,
            'text': PLocalizer.CutSubtitle1_2_b__3 }],
    Cutscene1_3: [
        {
            'beginTime': 0.29999999999999999,
            'text': PLocalizer.CutSubtitle1_3_a__1 },
        {
            'beginTime': 5.8600000000000003,
            'text': PLocalizer.CutSubtitle1_3_a__2 },
        {
            'beginTime': 11.449999999999999,
            'text': PLocalizer.CutSubtitle1_3_a__3,
            'endTime': 14.220000000000001 },
        {
            'beginTime': 16.5,
            'text': PLocalizer.CutSubtitle1_3_a__4 },
        {
            'beginTime': 24.129999999999999,
            'text': PLocalizer.CutSubtitle1_3_a__5 },
        {
            'beginTime': 27.699999999999999,
            'text': PLocalizer.CutSubtitle1_3_a__6 },
        {
            'beginTime': 31.699999999999999,
            'text': PLocalizer.CutSubtitle1_3_a__7,
            'endTime': 35.0 },
        {
            'beginTime': 38.210000000000001,
            'text': PLocalizer.CutSubtitle1_3_a__8 },
        {
            'beginTime': 42.600000000000001,
            'text': PLocalizer.CutSubtitle1_3_a__9,
            'endTime': 47.649999999999999 },
        {
            'beginTime': 51.700000000000003,
            'text': PLocalizer.CutSubtitle1_3_a__10 },
        {
            'beginTime': 59.140000000000001,
            'text': PLocalizer.CutSubtitle1_3_a__11 },
        {
            'beginTime': 65.599999999999994,
            'text': PLocalizer.CutSubtitle1_3_a__12 },
        {
            'beginTime': 75.299999999999997,
            'text': PLocalizer.CutSubtitle1_3_a__13 }],
    Cutscene2_1: [
        {
            'beginTime': 3.0,
            'text': PLocalizer.CutSubtitle2_1_a__1 },
        {
            'beginTime': 6.1799999999999997,
            'text': PLocalizer.CutSubtitle2_1_a__2 },
        {
            'beginTime': 11.789999999999999,
            'text': PLocalizer.CutSubtitle2_1_a__3 },
        {
            'beginTime': 13.02,
            'text': PLocalizer.CutSubtitle2_1_a__5 },
        {
            'beginTime': 16.41,
            'text': PLocalizer.CutSubtitle2_1_a__6 },
        {
            'beginTime': 21.0,
            'text': PLocalizer.CutSubtitle2_1_a__7 },
        {
            'beginTime': 28.449999999999999,
            'text': PLocalizer.CutSubtitle2_1_a__8 },
        {
            'beginTime': 30.399999999999999,
            'text': PLocalizer.CutSubtitle2_1_a__9 }],
    Cutscene2_1_b: [
        {
            'beginTime': 1.2,
            'text': PLocalizer.CutSubtitle2_1_b__1 },
        {
            'beginTime': 3.52,
            'text': PLocalizer.CutSubtitle2_1_b__2,
            'endTime': 9.0800000000000001 },
        {
            'beginTime': 11.1,
            'text': PLocalizer.CutSubtitle2_1_b__4 },
        {
            'beginTime': 13.75,
            'text': PLocalizer.CutSubtitle2_1_b__6 }],
    Cutscene2_2: [
        {
            'beginTime': 1.8999999999999999,
            'text': PLocalizer.CutSubtitle2_2__1 },
        {
            'beginTime': 7.3700000000000001,
            'text': PLocalizer.CutSubtitle2_2__2 },
        {
            'beginTime': 13.699999999999999,
            'text': PLocalizer.CutSubtitle2_2__3 },
        {
            'beginTime': 22.82,
            'text': PLocalizer.CutSubtitle2_2__4 },
        {
            'beginTime': 32.659999999999997,
            'text': PLocalizer.CutSubtitle2_2__5 },
        {
            'beginTime': 38.640000000000001,
            'text': PLocalizer.CutSubtitle2_2__6 },
        {
            'beginTime': 45.100000000000001,
            'text': PLocalizer.CutSubtitle2_2__7 },
        {
            'beginTime': 53.520000000000003,
            'text': PLocalizer.CutSubtitle2_2__8 },
        {
            'beginTime': 62.700000000000003,
            'text': PLocalizer.CutSubtitle2_2__9 },
        {
            'beginTime': 70.109999999999999,
            'text': PLocalizer.CutSubtitle2_2__10 },
        {
            'beginTime': 77.670000000000002,
            'text': PLocalizer.CutSubtitle2_2__11 },
        {
            'beginTime': 84.920000000000002,
            'text': PLocalizer.CutSubtitle2_2__12 }],
    Cutscene2_3: [
        {
            'beginTime': 2.1000000000000001,
            'text': PLocalizer.CutSubtitle2_3__1 },
        {
            'beginTime': 6.2599999999999998,
            'text': PLocalizer.CutSubtitle2_3__2 },
        {
            'beginTime': 10.130000000000001,
            'text': PLocalizer.CutSubtitle2_3__3 },
        {
            'beginTime': 15.4,
            'text': PLocalizer.CutSubtitle2_3__4 },
        {
            'beginTime': 21.260000000000002,
            'text': PLocalizer.CutSubtitle2_3__5 },
        {
            'beginTime': 24.68,
            'text': PLocalizer.CutSubtitle2_3__6 },
        {
            'beginTime': 27.75,
            'text': PLocalizer.CutSubtitle2_3__7,
            'endTime': 31.34 },
        {
            'beginTime': 33.100000000000001,
            'text': PLocalizer.CutSubtitle2_3__8 },
        {
            'beginTime': 38.149999999999999,
            'text': PLocalizer.CutSubtitle2_3__9 },
        {
            'beginTime': 40.640000000000001,
            'text': PLocalizer.CutSubtitle2_3__10 },
        {
            'beginTime': 43.479999999999997,
            'text': PLocalizer.CutSubtitle2_3__11 },
        {
            'beginTime': 45.5,
            'text': PLocalizer.CutSubtitle2_3__12 },
        {
            'beginTime': 51.109999999999999,
            'text': PLocalizer.CutSubtitle2_3__13 }],
    Cutscene2_4: [
        {
            'beginTime': 1.6000000000000001,
            'text': PLocalizer.CutSubtitle2_4_a__1 },
        {
            'beginTime': 3.9199999999999999,
            'text': PLocalizer.CutSubtitle2_4_a__2 },
        {
            'beginTime': 8.9199999999999999,
            'text': PLocalizer.CutSubtitle2_4_a__3 },
        {
            'beginTime': 16.91,
            'text': PLocalizer.CutSubtitle2_4_a__4 }],
    Cutscene2_4_b: [
        {
            'beginTime': 1.8,
            'text': PLocalizer.CutSubtitle2_4_b__1 },
        {
            'beginTime': 8.3200000000000003,
            'text': PLocalizer.CutSubtitle2_4_b__2 },
        {
            'beginTime': 14.82,
            'text': PLocalizer.CutSubtitle2_4_b__3 },
        {
            'beginTime': 21.170000000000002,
            'text': PLocalizer.CutSubtitle2_4_b__4 },
        {
            'beginTime': 29.0,
            'text': PLocalizer.CutSubtitle2_4_b__5 },
        {
            'beginTime': 35.030000000000001,
            'text': PLocalizer.CutSubtitle2_4_b__6 }],
    Cutscene2_5: [
        {
            'beginTime': 0,
            'text': PLocalizer.CutSubtitle2_5__1 },
        {
            'beginTime': 2.02,
            'text': PLocalizer.CutSubtitle2_5__2 },
        {
            'beginTime': 6.1100000000000003,
            'text': PLocalizer.CutSubtitle2_5__3 },
        {
            'beginTime': 10.0,
            'text': PLocalizer.CutSubtitle2_5__4 },
        {
            'beginTime': 13.050000000000001,
            'text': PLocalizer.CutSubtitle2_5__5 },
        {
            'beginTime': 18.32,
            'text': PLocalizer.CutSubtitle2_5__6 },
        {
            'beginTime': 24.210000000000001,
            'text': PLocalizer.CutSubtitle2_5__7 },
        {
            'beginTime': 29.100000000000001,
            'text': PLocalizer.CutSubtitle2_5__8 },
        {
            'beginTime': 32.890000000000001,
            'text': PLocalizer.CutSubtitle2_5__9 },
        {
            'beginTime': 38.299999999999997,
            'text': PLocalizer.CutSubtitle2_5__10 },
        {
            'beginTime': 43.049999999999997,
            'text': PLocalizer.CutSubtitle2_5__11,
            'endTime': 46.68 },
        {
            'beginTime': 50.0,
            'text': PLocalizer.CutSubtitle2_5__12 },
        {
            'beginTime': 53.009999999999998,
            'text': PLocalizer.CutSubtitle2_5__13 },
        {
            'beginTime': 56.829999999999998,
            'text': PLocalizer.CutSubtitle2_5__14 }],
    Cutscene3_1: [
        {
            'beginTime': 1.8999999999999999,
            'text': PLocalizer.CutSubtitle3_1__1 },
        {
            'beginTime': 3.9500000000000002,
            'text': PLocalizer.CutSubtitle3_1__2 },
        {
            'beginTime': 7.4500000000000002,
            'text': PLocalizer.CutSubtitle3_1__3 },
        {
            'beginTime': 10.1,
            'text': PLocalizer.CutSubtitle3_1__4 },
        {
            'beginTime': 13.58,
            'text': PLocalizer.CutSubtitle3_1__5 },
        {
            'beginTime': 17.260000000000002,
            'text': PLocalizer.CutSubtitle3_1__6 },
        {
            'beginTime': 18.510000000000002,
            'text': PLocalizer.CutSubtitle3_1__7 },
        {
            'beginTime': 23.420000000000002,
            'text': PLocalizer.CutSubtitle3_1__8 },
        {
            'beginTime': 29.670000000000002,
            'text': PLocalizer.CutSubtitle3_1__9 },
        {
            'beginTime': 34.68,
            'text': PLocalizer.CutSubtitle3_1__10 },
        {
            'beginTime': 38.479999999999997,
            'text': PLocalizer.CutSubtitle3_1__11 },
        {
            'beginTime': 41.299999999999997,
            'text': PLocalizer.CutSubtitle3_1__12 },
        {
            'beginTime': 46.399999999999999,
            'text': PLocalizer.CutSubtitle3_1__13 },
        {
            'beginTime': 52.530000000000001,
            'text': PLocalizer.CutSubtitle3_1__14 },
        {
            'beginTime': 59.399999999999999,
            'text': PLocalizer.CutSubtitle3_1__15 },
        {
            'beginTime': 65.519999999999996,
            'text': PLocalizer.CutSubtitle3_1__16 },
        {
            'beginTime': 69.5,
            'text': PLocalizer.CutSubtitle3_1__17 }],
    Cutscene3_2: [
        {
            'beginTime': 0,
            'text': PLocalizer.CutSubtitle3_2__1 },
        {
            'beginTime': 4.4100000000000001,
            'text': PLocalizer.CutSubtitle3_2__2 },
        {
            'beginTime': 8.2200000000000006,
            'text': PLocalizer.CutSubtitle3_2__3 },
        {
            'beginTime': 14.960000000000001,
            'text': PLocalizer.CutSubtitle3_2__4 },
        {
            'beginTime': 20.859999999999999,
            'text': PLocalizer.CutSubtitle3_2__5 },
        {
            'beginTime': 26.550000000000001,
            'text': PLocalizer.CutSubtitle3_2__6 },
        {
            'beginTime': 29.460000000000001,
            'text': PLocalizer.CutSubtitle3_2__7 },
        {
            'beginTime': 31.059999999999999,
            'text': PLocalizer.CutSubtitle3_2__8 },
        {
            'beginTime': 35.990000000000002,
            'text': PLocalizer.CutSubtitle3_2__9 },
        {
            'beginTime': 38.0,
            'text': PLocalizer.CutSubtitle3_2__10,
            'endTime': 41.600000000000001 },
        {
            'beginTime': 43.0,
            'text': PLocalizer.CutSubtitle3_2__11 },
        {
            'beginTime': 45.159999999999997,
            'text': PLocalizer.CutSubtitle3_2__12 },
        {
            'beginTime': 51.600000000000001,
            'text': PLocalizer.CutSubtitle3_2__13 },
        {
            'beginTime': 54.68,
            'text': PLocalizer.CutSubtitle3_2__14 },
        {
            'beginTime': 59.469999999999999,
            'text': PLocalizer.CutSubtitle3_2__15 },
        {
            'beginTime': 64.680000000000007,
            'text': PLocalizer.CutSubtitle3_2__16 },
        {
            'beginTime': 69.200000000000003,
            'text': PLocalizer.CutSubtitle3_2__17,
            'endTime': 74.599999999999994 },
        {
            'beginTime': 79,
            'text': PLocalizer.CutSubtitle3_2__18 },
        {
            'beginTime': 85.109999999999999,
            'text': PLocalizer.CutSubtitle3_2__19 },
        {
            'beginTime': 88.920000000000002,
            'text': PLocalizer.CutSubtitle3_2__20 },
        {
            'beginTime': 90.260000000000005,
            'text': PLocalizer.CutSubtitle3_2__21 },
        {
            'beginTime': 94.730000000000004,
            'text': PLocalizer.CutSubtitle3_2__22 },
        {
            'beginTime': 96.579999999999998,
            'text': PLocalizer.CutSubtitle3_2__23 },
        {
            'beginTime': 100.45999999999999,
            'text': PLocalizer.CutSubtitle3_2__24 }],
    Cutscene6_1: [
        {
            'beginTime': 0,
            'text': PLocalizer.CutSubtitle6_1__1 },
        {
            'beginTime': 3.5,
            'text': PLocalizer.CutSubtitle6_1__2 },
        {
            'beginTime': 6.0,
            'text': PLocalizer.CutSubtitle6_1__3 },
        {
            'beginTime': 9.9000000000000004,
            'text': PLocalizer.CutSubtitle6_1__4 },
        {
            'beginTime': 12.25,
            'text': PLocalizer.CutSubtitle6_1__5 },
        {
            'beginTime': 14.6,
            'text': PLocalizer.CutSubtitle6_1__6 },
        {
            'beginTime': 18.559999999999999,
            'text': PLocalizer.CutSubtitle6_1__7 },
        {
            'beginTime': 21.300000000000001,
            'text': PLocalizer.CutSubtitle6_1__8 }] }
CutsceneIds = CutsceneFilenames.keys()
CutsceneIds.sort()
PRELOADED_CUTSCENE_STAGE1 = [
    Cutscene1_1_2]
PRELOADED_CUTSCENE_STAGE2 = [
    Cutscene1_1_5_a,
    Cutscene1_1_5_c]
PRELOADED_CUTSCENE_STAGE3 = [
    Cutscene1_2,
    Cutscene1_3]
PRELOADED_CUTSCENE_STAGE4 = [
    Cutscene2_1_b]
PRELOADED_CUTSCENE_STAGE5 = [
    Cutscene2_4_b]

class CutsceneDesc(POD):
    DataSet = {
        'id': None,
        'components': tuple(''),
        'actorFunctors': None,
        'soundFile': None,
        'filmSizeHorizontal': 42.667000000000002,
        'focalLength': 30 }
    
    def __init__(self, *args, **kwArgs):
        POD.__init__(self, *args, **args)
        self.filename = CutsceneFilenames[self.id]


CutsceneData = {
    Cutscene1_1_1: CutsceneDesc(id = Cutscene1_1_1, components = [
        ''], actorFunctors = [
        CutJackSparrow,
        Functor(CutLocalPirate, False)], soundFile = loadSfxString(SoundGlobals.CS_1_1_A_JS), filmSizeHorizontal = 42.667000000000002, focalLength = 50),
    Cutscene1_1_2: CutsceneDesc(id = Cutscene1_1_2, components = [
        ''], actorFunctors = [
        CutJackSparrow,
        Functor(CutLocalPirate, False)], soundFile = loadSfxString(SoundGlobals.CS_1_1_B_JS), filmSizeHorizontal = 42.667000000000002, focalLength = 50),
    Cutscene1_1_5_a: CutsceneDesc(id = Cutscene1_1_5_a, components = [
        ''], actorFunctors = [
        Functor(CutLocalPirate, False),
        Functor(CutBartenderMmsDoggerel, 1),
        Functor(CutBartenderFmiNell, 1)], soundFile = loadSfxString(SoundGlobals.CS_1_1_5_A_DAN), filmSizeHorizontal = 42.667000000000002, focalLength = 50),
    Cutscene1_1_5_b: CutsceneDesc(id = Cutscene1_1_5_b, components = [
        ''], actorFunctors = [
        Functor(CutLocalPirate, False),
        Functor(CutBartenderMmsDoggerel, 1),
        Functor(CutBartenderFmiNell, 1)], soundFile = loadSfxString(SoundGlobals.CS_1_1_5_B_DAN), filmSizeHorizontal = 42.667000000000002, focalLength = 50),
    Cutscene1_1_5_c: CutsceneDesc(id = Cutscene1_1_5_c, components = [
        ''], actorFunctors = [
        Functor(CutLocalPirate, False),
        Functor(CutBartenderMmsDoggerel, 1),
        Functor(CutBartenderFmiNell, 1)], soundFile = loadSfxString(SoundGlobals.CS_1_1_5_C_DAN), filmSizeHorizontal = 42.667000000000002, focalLength = 50),
    Cutscene1_2: CutsceneDesc(id = Cutscene1_2, components = [
        '_dock',
        '_b_dock'], actorFunctors = [
        Functor(CutLocalPirate, False),
        Functor(CutCaptainBeckShort, 1),
        Functor(CutGenericActor, 'wheel', 'wheel_zero', 'models/props/'),
        Functor(CutShip, ShipGlobals.STUMPY_SHIP, ShipGlobals.Styles.Player)], soundFile = loadSfxString(SoundGlobals.CS_1_2_DOCK), filmSizeHorizontal = 42.667000000000002, focalLength = 50),
    Cutscene1_3: CutsceneDesc(id = Cutscene1_3, components = [
        '_a',
        '_b'], actorFunctors = [
        CutJollyRoger,
        Functor(CutLocalPirate, False),
        Functor(CutGenericActor, 'wheel', 'wheel_zero', 'models/props/'),
        Functor(CutGenericActor, 'plank', 'plank_zero', 'models/props/'),
        Functor(CutCaptainBeckShort, 1),
        Functor(CutSkeleton, EarthUndead[0], 1),
        Functor(CutSkeleton, EarthUndead[4], 2),
        Functor(CutSkeleton, EarthUndead[2], 3),
        Functor(CutShip, ShipGlobals.STUMPY_SHIP, ShipGlobals.Styles.Player),
        Functor(CutShip, ShipGlobals.SKEL_DEATH_OMEN, ShipGlobals.Styles.Undead)], soundFile = loadSfxString(SoundGlobals.CS_1_3_JR), filmSizeHorizontal = 42.667000000000002, focalLength = 50),
    Cutscene2_1: CutsceneDesc(id = Cutscene2_1, components = [
        ''], actorFunctors = [
        Functor(CutWillTurner, '1152830677.95jubutler'),
        Functor(CutLocalPirate, False)], soundFile = loadSfxString(SoundGlobals.CS_2_1_A_WT), filmSizeHorizontal = 42.667000000000002, focalLength = 72),
    Cutscene2_1_b: CutsceneDesc(id = Cutscene2_1_b, components = [
        ''], actorFunctors = [
        Functor(CutWillTurner, '1152830677.95jubutler'),
        Functor(CutLocalPirate, False),
        Functor(CutSkeleton, EarthUndead[2], 2),
        Functor(CutSkeleton, EarthUndead[1], 3)], soundFile = loadSfxString(SoundGlobals.CS_2_1_B_WT), filmSizeHorizontal = 42.667000000000002, focalLength = 35),
    Cutscene2_2: CutsceneDesc(id = Cutscene2_2, components = [
        ''], actorFunctors = [
        Functor(CutTiaDalma, '1154497344.0jubutlerPR'),
        Functor(CutLocalPirate, False),
        Functor(CutBlackGuard1, 1),
        Functor(CutBlackGuard2, 2),
        Functor(CutBlackGuard3, 3),
        CutJollyRoger,
        Functor(CutSkeleton, EarthUndead[4], 4),
        Functor(CutSkeleton, EarthUndead[2], 5),
        Functor(CutGenericActor, 'lantern', 'lantern_zero', 'models/props/'),
        Functor(CutGenericActor, 'crablegs', 'crablegs_zero', 'models/props/')], soundFile = loadSfxString(SoundGlobals.CS_2_2_TD), filmSizeHorizontal = 42.667000000000002, focalLength = 72),
    Cutscene2_3: CutsceneDesc(id = Cutscene2_3, components = [
        ''], actorFunctors = [
        Functor(CutElizabethSwan, '1171325040.86MAsaduzz'),
        Functor(CutLocalPirate, False),
        Functor(CutGenericActor, 'paper', 'paper_zero', 'models/props/')], soundFile = loadSfxString(SoundGlobals.CS_2_3_ES), filmSizeHorizontal = 42.667000000000002, focalLength = 32),
    Cutscene2_4: CutsceneDesc(id = Cutscene2_4, components = [
        '_a'], actorFunctors = [
        Functor(CutCaptBarbossa, '1172618710.78sdnaik'),
        Functor(CutLocalPirate, False),
        Functor(CutGenericActor, 'monkey', 'monkey_hi', 'models/char/')], soundFile = loadSfxString(SoundGlobals.CS_2_4_A_CB), filmSizeHorizontal = 42.667000000000002, focalLength = 50),
    Cutscene2_4_b: CutsceneDesc(id = Cutscene2_4_b, components = [
        '_b',
        '_c'], actorFunctors = [
        Functor(CutCaptBarbossa, '1172618710.78sdnaik'),
        Functor(CutLocalPirate, True),
        Functor(CutGenericActor, 'monkey', 'monkey_hi', 'models/char/')], soundFile = loadSfxString(SoundGlobals.CS_2_4_B_CB), filmSizeHorizontal = 42.667000000000002, focalLength = 50),
    Cutscene2_5: CutsceneDesc(id = Cutscene2_5, components = [
        ''], actorFunctors = [
        CutJackSparrow,
        Functor(CutLocalPirate, False),
        Functor(CutGenericActor, 'mug', 'mug_zero', 'models/props/'),
        Functor(CutBartenderPear, 1)], soundFile = loadSfxString(SoundGlobals.CS_2_5_JS), filmSizeHorizontal = 42.667000000000002, focalLength = 30),
    Cutscene3_1: CutsceneDesc(id = Cutscene3_1, components = [
        ''], actorFunctors = [
        Functor(CutLocalPirate, False),
        Functor(CutGenericActor, 'open_paper', 'open_paper_zero', 'models/props/'),
        Functor(CutNavyMtpPeter, 1),
        Functor(CutNavyMtpJeff, 2),
        Functor(CutCaptainBeckShort, 3),
        Functor(CutBartenderMmsDoggerel, 4),
        Functor(CutShip, ShipGlobals.GOLIATH, ShipGlobals.Styles.Navy),
        Functor(CutShip, ShipGlobals.BLACK_PEARL, ShipGlobals.Styles.BP)], soundFile = loadSfxString(SoundGlobals.CS_3_1_BP), filmSizeHorizontal = 42.667000000000002, focalLength = 50),
    Cutscene3_2: CutsceneDesc(id = Cutscene3_2, components = [
        ''], actorFunctors = [
        CutJackSparrow,
        Functor(CutLocalPirate, False),
        Functor(CutJoshGibbs, '1168022298.47Shochet')], soundFile = loadSfxString(SoundGlobals.CS_3_2_JS), filmSizeHorizontal = 42.667000000000002, focalLength = 50),
    Cutscene6_1: CutsceneDesc(id = Cutscene6_1, components = [
        ''], actorFunctors = [
        Functor(CutTiaDalma, '1154497344.0jubutlerPR'),
        Functor(CutLocalPirate, False)], soundFile = loadSfxString(SoundGlobals.CS_6_1_TD), filmSizeHorizontal = 42.667000000000002, focalLength = 50) }
