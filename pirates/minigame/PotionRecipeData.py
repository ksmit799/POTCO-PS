from pirates.battle.WeaponConstants import *
from pirates.piratesbase import PLocalizer
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.battle import WeaponGlobals
from pirates.inventory import ItemGlobals
from pirates.minigame import PotionGlobals

def safeSubstitute(text, dict):
    for key in dict.keys():
        text = text.replace('$'+key, str(dict[key]))
    return text

PotionColorSets = [
    [
        0,
        1,
        2],
    [
        0,
        1,
        2,
        3],
    [
        0,
        1,
        2,
        4],
    [
        0,
        1,
        2,
        5]]
PotionRecipeList = [
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.Burp],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.Burp], {
            'pot': 0,
            'dur': 0,
            'unit': 0 }),
        'potionID': C_BURP,
        'ingredients': [
            {
                'color': 0,
                'level': 3 },
            {
                'color': 1,
                'level': 3 },
            {
                'color': 2,
                'level': 3 },
            {
                'color': 4,
                'level': 3 }],
        'level': 3,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.Fart],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.Fart], {
            'pot': 0,
            'dur': 0,
            'unit': 0 }),
        'potionID': C_FART,
        'ingredients': [
            {
                'color': 0,
                'level': 3 },
            {
                'color': 1,
                'level': 3 },
            {
                'color': 2,
                'level': 3 },
            {
                'color': 5,
                'level': 4 }],
        'level': 4,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.Vomit],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.Vomit], {
            'pot': 0,
            'dur': 0,
            'unit': 0 }),
        'disabled': True,
        'potionID': C_VOMIT,
        'ingredients': [
            {
                'color': 0,
                'level': 3 },
            {
                'color': 1,
                'level': 3 },
            {
                'color': 2,
                'level': 3 },
            {
                'color': 3,
                'level': 3 }],
        'level': 9,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.FaceColor],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.FaceColor], {
            'pot': 0,
            'dur': 0,
            'unit': 0 }),
        'potionID': C_CRAZY_SKIN_COLOR,
        'ingredients': [
            {
                'color': 0,
                'level': 3 },
            {
                'color': 1,
                'level': 3 },
            {
                'color': 2,
                'level': 3 },
            {
                'color': 5,
                'level': 3 }],
        'level': 5,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.SizeReduce],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.SizeReduce], {
            'pot': 0,
            'dur': 0,
            'unit': 0 }),
        'potionID': C_SIZE_REDUCE,
        'ingredients': [
            {
                'color': 0,
                'level': 3 },
            {
                'color': 1,
                'level': 3 },
            {
                'color': 2,
                'level': 3 },
            {
                'color': 3,
                'level': 5 }],
        'level': 10,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.SizeIncrease],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.SizeIncrease], {
            'pot': 0,
            'dur': 0,
            'unit': 0 }),
        'potionID': C_SIZE_INCREASE,
        'ingredients': [
            {
                'color': 0,
                'level': 3 },
            {
                'color': 1,
                'level': 3 },
            {
                'color': 2,
                'level': 3 },
            {
                'color': 5,
                'level': 5 }],
        'level': 16,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.HeadFire],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.HeadFire], {
            'pot': 0,
            'dur': 0,
            'unit': 0 }),
        'potionID': C_HEAD_FIRE,
        'ingredients': [
            {
                'color': 0,
                'level': 3 },
            {
                'color': 1,
                'level': 3 },
            {
                'color': 2,
                'level': 3 },
            {
                'color': 4,
                'level': 5 },
            {
                'color': 4,
                'level': 5 }],
        'level': 17,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.ScorpionTransform],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.ScorpionTransform], {
            'pot': 0,
            'dur': 0,
            'unit': 0 }),
        'disabled': True,
        'potionID': C_SCORPION_TRANSFORM,
        'ingredients': [
            {
                'color': 0,
                'level': 6 }],
        'level': 20,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.AlligatorTransform],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.AlligatorTransform], {
            'pot': 0,
            'dur': 0,
            'unit': 0 }),
        'disabled': True,
        'potionID': C_ALLIGATOR_TRANSFORM,
        'ingredients': [
            {
                'color': 2,
                'level': 6 }],
        'level': 20,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.CrabTransform],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.CrabTransform], {
            'pot': 0,
            'dur': 0,
            'unit': 0 }),
        'disabled': True,
        'potionID': C_CRAB_TRANSFORM,
        'ingredients': [
            {
                'color': 1,
                'level': 6 }],
        'level': 20,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.CannonDamageLvl1],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.CannonDamageLvl1], {
            'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.CannonDamageLvl1)) * 100),
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.CannonDamageLvl1))),
            'unit': 'seconds' }),
        'potionID': C_CANNON_DAMAGE_LVL1,
        'ingredients': [
            {
                'color': 0,
                'level': 3 },
            {
                'color': 1,
                'level': 3 },
            {
                'color': 2,
                'level': 3 }],
        'level': 2,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.PistolDamageLvl1],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.PistolDamageLvl1], {
            'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.PistolDamageLvl1)) * 100),
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.PistolDamageLvl1))),
            'unit': 'seconds' }),
        'potionID': C_PISTOL_DAMAGE_LVL1,
        'ingredients': [
            {
                'color': 0,
                'level': 3 },
            {
                'color': 0,
                'level': 3 },
            {
                'color': 1,
                'level': 3 }],
        'level': 1,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.CutlassDamageLvl1],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.CutlassDamageLvl1], {
            'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.CutlassDamageLvl1)) * 100),
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.CutlassDamageLvl1))),
            'unit': 'seconds' }),
        'potionID': C_CUTLASS_DAMAGE_LVL1,
        'ingredients': [
            {
                'color': 0,
                'level': 3 },
            {
                'color': 2,
                'level': 3 },
            {
                'color': 2,
                'level': 3 }],
        'level': 1,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.DollDamageLvl1],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.DollDamageLvl1], {
            'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.DollDamageLvl1)) * 100),
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.DollDamageLvl1))),
            'unit': 'seconds' }),
        'potionID': C_DOLL_DAMAGE_LVL1,
        'ingredients': [
            {
                'color': 1,
                'level': 3 },
            {
                'color': 1,
                'level': 3 },
            {
                'color': 2,
                'level': 3 }],
        'level': 2,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.CannonDamageLvl2],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.CannonDamageLvl2], {
            'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.CannonDamageLvl2)) * 100),
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.CannonDamageLvl2))),
            'unit': 'seconds' }),
        'potionID': C_CANNON_DAMAGE_LVL2,
        'ingredients': [
            {
                'color': 0,
                'level': 4 },
            {
                'color': 1,
                'level': 4 },
            {
                'color': 2,
                'level': 4 }],
        'level': 7,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.PistolDamageLvl2],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.PistolDamageLvl2], {
            'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.PistolDamageLvl2)) * 100),
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.PistolDamageLvl2))),
            'unit': 'seconds' }),
        'potionID': C_PISTOL_DAMAGE_LVL2,
        'ingredients': [
            {
                'color': 0,
                'level': 4 },
            {
                'color': 0,
                'level': 4 },
            {
                'color': 1,
                'level': 4 }],
        'level': 6,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.CutlassDamageLvl2],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.CutlassDamageLvl2], {
            'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.CutlassDamageLvl2)) * 100),
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.CutlassDamageLvl2))),
            'unit': 'seconds' }),
        'potionID': C_CUTLASS_DAMAGE_LVL2,
        'ingredients': [
            {
                'color': 0,
                'level': 4 },
            {
                'color': 2,
                'level': 4 },
            {
                'color': 2,
                'level': 4 }],
        'level': 6,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.DollDamageLvl2],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.DollDamageLvl2], {
            'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.DollDamageLvl2)) * 100),
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.DollDamageLvl2))),
            'unit': 'seconds' }),
        'potionID': C_DOLL_DAMAGE_LVL2,
        'ingredients': [
            {
                'color': 1,
                'level': 4 },
            {
                'color': 1,
                'level': 4 },
            {
                'color': 2,
                'level': 4 }],
        'level': 7,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.CannonDamageLvl3],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.CannonDamageLvl3], {
            'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.CannonDamageLvl3)) * 100),
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.CannonDamageLvl3))),
            'unit': 'seconds' }),
        'potionID': C_CANNON_DAMAGE_LVL3,
        'ingredients': [
            {
                'color': 0,
                'level': 5 },
            {
                'color': 1,
                'level': 5 },
            {
                'color': 2,
                'level': 5 }],
        'level': 12,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.PistolDamageLvl3],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.PistolDamageLvl3], {
            'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.PistolDamageLvl3)) * 100),
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.PistolDamageLvl3))),
            'unit': 'seconds' }),
        'potionID': C_PISTOL_DAMAGE_LVL3,
        'ingredients': [
            {
                'color': 0,
                'level': 5 },
            {
                'color': 0,
                'level': 5 },
            {
                'color': 1,
                'level': 5 }],
        'level': 11,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.CutlassDamageLvl3],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.CutlassDamageLvl3], {
            'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.CutlassDamageLvl3)) * 100),
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.CutlassDamageLvl3))),
            'unit': 'seconds' }),
        'potionID': C_CUTLASS_DAMAGE_LVL3,
        'ingredients': [
            {
                'color': 0,
                'level': 5 },
            {
                'color': 2,
                'level': 5 },
            {
                'color': 2,
                'level': 5 }],
        'level': 11,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.DollDamageLvl3],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.DollDamageLvl3], {
            'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.DollDamageLvl3)) * 100),
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.DollDamageLvl3))),
            'unit': 'seconds' }),
        'potionID': C_DOLL_DAMAGE_LVL3,
        'ingredients': [
            {
                'color': 1,
                'level': 5 },
            {
                'color': 1,
                'level': 5 },
            {
                'color': 2,
                'level': 5 }],
        'level': 12,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.HastenLvl1],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.HastenLvl1], {
            'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.HastenLvl1)) * 100),
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.HastenLvl1))),
            'unit': 'seconds' }),
        'potionID': C_HASTEN_LVL1,
        'ingredients': [
            {
                'color': 0,
                'level': 3 },
            {
                'color': 0,
                'level': 3 },
            {
                'color': 1,
                'level': 3 },
            {
                'color': 2,
                'level': 3 }],
        'level': 3,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.HastenLvl2],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.HastenLvl2], {
            'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.HastenLvl2)) * 100),
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.HastenLvl2))),
            'unit': 'seconds' }),
        'potionID': C_HASTEN_LVL2,
        'ingredients': [
            {
                'color': 0,
                'level': 3 },
            {
                'color': 0,
                'level': 3 },
            {
                'color': 1,
                'level': 3 },
            {
                'color': 1,
                'level': 3 },
            {
                'color': 2,
                'level': 3 }],
        'level': 8,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.HastenLvl3],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.HastenLvl3], {
            'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.HastenLvl3)) * 100),
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.HastenLvl3))),
            'unit': 'seconds' }),
        'potionID': C_HASTEN_LVL3,
        'ingredients': [
            {
                'color': 0,
                'level': 3 },
            {
                'color': 0,
                'level': 3 },
            {
                'color': 1,
                'level': 3 },
            {
                'color': 1,
                'level': 3 },
            {
                'color': 2,
                'level': 3 },
            {
                'color': 2,
                'level': 3 }],
        'level': 13,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.RepBonusLvl1],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.RepBonusLvl1], {
            'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.RepBonusLvl1)) * 100),
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.RepBonusLvl1))),
            'unit': 'seconds' }),
        'potionID': C_REP_BONUS_LVL1,
        'ingredients': [
            {
                'color': 3,
                'level': 3 },
            {
                'color': 3,
                'level': 3 },
            {
                'color': 3,
                'level': 3 },
            {
                'color': 3,
                'level': 3 },
            {
                'color': 3,
                'level': 3 },
            {
                'color': 3,
                'level': 3 }],
        'level': 15,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.RepBonusLvl2],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.RepBonusLvl2], {
            'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.RepBonusLvl2)) * 100),
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.RepBonusLvl2))),
            'unit': 'seconds' }),
        'potionID': C_REP_BONUS_LVL2,
        'ingredients': [
            {
                'color': 3,
                'level': 4 },
            {
                'color': 3,
                'level': 4 },
            {
                'color': 3,
                'level': 4 },
            {
                'color': 3,
                'level': 4 }],
        'level': 19,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.GoldBonusLvl1],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.GoldBonusLvl1], {
            'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.GoldBonusLvl1)) * 100),
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.GoldBonusLvl1))),
            'unit': 'seconds' }),
        'potionID': C_GOLD_BONUS_LVL1,
        'ingredients': [
            {
                'color': 4,
                'level': 3 },
            {
                'color': 4,
                'level': 3 },
            {
                'color': 4,
                'level': 3 },
            {
                'color': 4,
                'level': 3 },
            {
                'color': 4,
                'level': 3 },
            {
                'color': 4,
                'level': 3 }],
        'level': 14,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.GoldBonusLvl2],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.GoldBonusLvl2], {
            'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.GoldBonusLvl2)) * 100),
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.GoldBonusLvl2))),
            'unit': 'seconds' }),
        'potionID': C_GOLD_BONUS_LVL2,
        'ingredients': [
            {
                'color': 4,
                'level': 4 },
            {
                'color': 4,
                'level': 4 },
            {
                'color': 4,
                'level': 4 },
            {
                'color': 4,
                'level': 4 }],
        'level': 19,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.InvisibilityLvl1],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.InvisibilityLvl1], {
            'pot': 0,
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.InvisibilityLvl1))),
            'unit': 'seconds' }),
        'potionID': C_INVISIBILITY_LVL1,
        'ingredients': [
            {
                'color': 5,
                'level': 3 },
            {
                'color': 5,
                'level': 3 },
            {
                'color': 5,
                'level': 3 },
            {
                'color': 5,
                'level': 3 },
            {
                'color': 5,
                'level': 3 },
            {
                'color': 5,
                'level': 3 }],
        'level': 13,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.InvisibilityLvl2],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.InvisibilityLvl2], {
            'pot': 0,
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.InvisibilityLvl2))),
            'unit': 'seconds' }),
        'potionID': C_INVISIBILITY_LVL2,
        'ingredients': [
            {
                'color': 5,
                'level': 4 },
            {
                'color': 5,
                'level': 4 },
            {
                'color': 5,
                'level': 4 },
            {
                'color': 5,
                'level': 4 }],
        'level': 18,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.AccuracyBonusLvl1],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.AccuracyBonusLvl1], {
            'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.AccuracyBonusLvl1)) * 100),
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.AccuracyBonusLvl1))),
            'unit': 'seconds' }),
        'potionID': C_ACCURACY_BONUS_LVL1,
        'ingredients': [
            {
                'color': 5,
                'level': 2 },
            {
                'color': 5,
                'level': 3 },
            {
                'color': 5,
                'level': 3 }],
        'level': 4,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.AccuracyBonusLvl2],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.AccuracyBonusLvl2], {
            'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.AccuracyBonusLvl2)) * 100),
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.AccuracyBonusLvl2))),
            'unit': 'seconds' }),
        'potionID': C_ACCURACY_BONUS_LVL2,
        'ingredients': [
            {
                'color': 5,
                'level': 2 },
            {
                'color': 5,
                'level': 3 },
            {
                'color': 5,
                'level': 3 },
            {
                'color': 5,
                'level': 4 }],
        'level': 9,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.AccuracyBonusLvl3],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.AccuracyBonusLvl3], {
            'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.AccuracyBonusLvl3)) * 100),
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.AccuracyBonusLvl3))),
            'unit': 'seconds' }),
        'potionID': C_ACCURACY_BONUS_LVL3,
        'ingredients': [
            {
                'color': 5,
                'level': 3 },
            {
                'color': 5,
                'level': 3 },
            {
                'color': 5,
                'level': 3 },
            {
                'color': 5,
                'level': 4 },
            {
                'color': 5,
                'level': 4 },
            {
                'color': 5,
                'level': 4 }],
        'level': 14,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.RemoveGroggy],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.RemoveGroggy], {
            'pot': 0,
            'dur': 0,
            'unit': 0 }),
        'potionID': C_REMOVE_GROGGY,
        'ingredients': [
            {
                'color': 0,
                'level': 4 },
            {
                'color': 0,
                'level': 4 },
            {
                'color': 1,
                'level': 4 },
            {
                'color': 1,
                'level': 4 },
            {
                'color': 2,
                'level': 4 },
            {
                'color': 2,
                'level': 4 }],
        'level': 16,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.RegenLvl1],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.RegenLvl1], {
            'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.RegenLvl1)) * 100),
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.RegenLvl1))),
            'unit': 'seconds' }),
        'potionID': C_REGEN_LVL1,
        'ingredients': [
            {
                'color': 1,
                'level': 4 },
            {
                'color': 1,
                'level': 4 }],
        'level': 5,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.RegenLvl2],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.RegenLvl2], {
            'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.RegenLvl2)) * 100),
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.RegenLvl2))),
            'unit': 'seconds' }),
        'potionID': C_REGEN_LVL2,
        'ingredients': [
            {
                'color': 1,
                'level': 4 },
            {
                'color': 1,
                'level': 4 },
            {
                'color': 1,
                'level': 4 }],
        'level': 10,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.RegenLvl3],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.RegenLvl3], {
            'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.RegenLvl3)) * 100),
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.RegenLvl3))),
            'unit': 'seconds' }),
        'potionID': C_REGEN_LVL3,
        'ingredients': [
            {
                'color': 1,
                'level': 4 },
            {
                'color': 1,
                'level': 4 },
            {
                'color': 1,
                'level': 4 },
            {
                'color': 1,
                'level': 4 }],
        'level': 15,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.RegenLvl4],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.RegenLvl4], {
            'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.RegenLvl4)) * 100),
            'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.RegenLvl4))),
            'unit': 'seconds' }),
        'potionID': C_REGEN_LVL4,
        'ingredients': [
            {
                'color': 1,
                'level': 4 },
            {
                'color': 1,
                'level': 4 },
            {
                'color': 1,
                'level': 4 },
            {
                'color': 1,
                'level': 4 },
            {
                'color': 1,
                'level': 4 }],
        'level': 17,
        'discovered': False },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.StaffEnchant1],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.StaffEnchant1], {
            'pot': 0,
            'dur': 0,
            'unit': 0 }),
        'potionID': C_STAFF_ENCHANT_LVL1,
        'ingredients': [
            {
                'color': 0,
                'level': 3 },
            {
                'color': 1,
                'level': 3 },
            {
                'color': 1,
                'level': 3 },
            {
                'color': 2,
                'level': 3 },
            {
                'color': 2,
                'level': 3 }],
        'level': 8,
        'discovered': False,
        'questOnly': True },
    {
        'name': PLocalizer.InventoryTypeNames[InventoryType.StaffEnchant2],
        'desc': safeSubstitute(PLocalizer.PotionDescs[InventoryType.StaffEnchant2], {
            'pot': 0,
            'dur': 0,
            'unit': 0 }),
        'potionID': C_STAFF_ENCHANT_LVL2,
        'ingredients': [
            {
                'color': 2,
                'level': 6 }],
        'level': 20,
        'discovered': False,
        'questOnly': True }]

def getFreeStatus(potionID):
    for potion in PotionRecipeList:
        if potion['potionID'] == potionID:
            return potion['free']
            continue
    
    return False


def getNumIngredients(potionID):
    for potion in PotionRecipeList:
        if potion['potionID'] == potionID:
            return len(potion['ingredients'])
            continue
    
    return 0


def getDisabled(potionID):
    for potion in PotionRecipeList:
        if potion['potionID'] == potionID:
            return potion.get('disabled', False)
            continue
    
    return 0

