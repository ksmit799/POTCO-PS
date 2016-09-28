# File: B (Python 2.4)

from pandac.PandaModules import *
from direct.showbase import PythonUtil
TARGET_POS = {
    4: Vec3(0.84999999999999998, 0, 0.0),
    3: Vec3(0.59999999999999998, 0, 0.41999999999999998),
    2: Vec3(0.27000000000000002, 0, 0.59999999999999998),
    1: Vec3(-0.080000000000000002, 0, 0.63),
    0: Vec3(-0.58999999999999997, 0, 0.28999999999999998) }
FACES = PythonUtil.Enum('DEALER,ONE,TWO,THREE,FOUR,FIVE,SIX,SEVEN')
FACE_SPOT_POS = {
    FACES.DEALER: (-1.0, 0, 0.59999999999999998),
    FACES.ONE: (-1.1499999999999999, 0, -0.29999999999999999),
    FACES.TWO: (-0.95999999999999996, 0, -0.60999999999999999),
    FACES.THREE: (-0.65000000000000002, 0, -0.80000000000000004),
    FACES.FOUR: (0.65000000000000002, 0, -0.80000000000000004),
    FACES.FIVE: (0.95999999999999996, 0, -0.60999999999999999),
    FACES.SIX: (1.1499999999999999, 0, -0.29999999999999999) }
FINGER_RANGES = [
    [
        -26,
        -16],
    [
        -3,
        8],
    [
        23,
        32],
    [
        52,
        60]]
PLAYER_ACTIONS = PythonUtil.Enum('JoinGame,UnjoinGame,RejoinGame,Resign,Leave,Continue,Progress')
GAME_ACTIONS = PythonUtil.Enum('AskForContinue,NotifyOfWin,NotifyOfLoss')
CONTINUE_OPTIONS = PythonUtil.Enum('Resign,Continue,Rejoin,Leave')
GameTimeDelay = 5
RoundTimeDelay = 5
RoundTimeLimit = 90
RoundContinueWait = 10
