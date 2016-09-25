# File: F (Python 2.4)

from direct.showbase.PythonUtil import *
from pandac.PandaModules import *
import math
Shapes = Enum('Default,Square,Cut,TwoCut,                LongTaper,LongTaperCut,ShortTaper,ShortTaperCut')
ShapeCount = len(Shapes)
Layouts = Enum('Square,Circle,Hex')
(SQRT2, SQRT3) = (math.sqrt(2), math.sqrt(3))
ISQRT2 = 1 / SQRT2 / 2
LayoutOffsets = [
    [
        [
            0,
            1],
        [
            0.5,
            1],
        [
            1,
            1],
        [
            0,
            0.5],
        [
            0.5,
            0.5],
        [
            1,
            0.5],
        [
            0,
            0],
        [
            0.5,
            0],
        [
            1,
            0]],
    [
        [
            0.5 - ISQRT2,
            0.5 + ISQRT2],
        [
            0.5,
            1],
        [
            0.5 + ISQRT2,
            0.5 + ISQRT2],
        [
            0,
            0.5],
        [
            0.5,
            0.5],
        [
            1,
            0.5],
        [
            0.5 - ISQRT2,
            0.5 - ISQRT2],
        [
            0.5,
            0],
        [
            0.5 + ISQRT2,
            0.5 - ISQRT2]],
    [
        [
            0.25,
            0.25 * (2 + SQRT3)],
        [
            0.75,
            0.25 * (2 + SQRT3)],
        [
            0,
            0.5],
        [
            0.5,
            0.5],
        [
            1,
            0.5],
        [
            0.25,
            0.25 * (2 - SQRT3)],
        [
            0.75,
            0.25 * (2 - SQRT3)]]]
LayoutCount = len(Layouts)
Backgrounds = Enum('Default,VHalf,HHalf,Corners,VThird,HThird,                     DiagHalf,Sides,Serrated,CenterCross,OffsetCross,                     Texas,HNarrowBand,HWideBand,VNarrowBand,VBand,                     VWideBand,Slash,XCross')
BackgroundCount = len(Backgrounds)
Emblems = Enum('Circle,Cross1,Cross2,Cross3,Crescent,Star1,Knife1,Knife2,Skull1,Skull2,Scimitar')
EmblemCount = len(Emblems)
MaxEmblemCount = 3
Colors = [
    Vec4(0.10000000000000001, 0.10000000000000001, 0.10000000000000001, 1),
    Vec4(1),
    Vec4(0.40000000000000002, 0.40000000000000002, 0.40000000000000002, 1),
    Vec4(0.25, 0.25, 0.25, 1),
    Vec4(0.25, 0, 0.070000000000000007, 1),
    Vec4(0.39000000000000001, 0, 0.10000000000000001, 1),
    Vec4(0.5, 0.0, 0.0, 1),
    Vec4(0.64000000000000001, 0, 0, 1),
    Vec4(0.75, 0, 0, 1)]
ColorCount = len(Colors)
RotationCount = 24
XPosLowCount = 0
XPosHiCount = 256
YPosLowCount = 56
YPosHiCount = 200
LayoutScaleMin = 0.125
LayoutScaleMax = 1.0
LayoutScaleResolutionFactor = 16
continue
LayoutScales = [ LayoutScaleMin + (float(x) / (LayoutScaleResolutionFactor - 1)) * (LayoutScaleMax - LayoutScaleMin) for x in range(LayoutScaleResolutionFactor) ]
LayoutScaleCount = len(LayoutScales)
EmblemScales = LayoutScales
EmblemScaleCount = len(EmblemScales)
EmblemNearProximity = 0.074999999999999997
EmblemFarProximity = 0.10000000000000001
BgNearProximity = 0.14999999999999999
BgFarProximity = 0.14999999999999999
