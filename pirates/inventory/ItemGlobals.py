#Had to sacrifice CPickle due to corrupt .pkl - Now using hard coded ItemData.py file
from pandac.PandaModules import *
from direct.showbase.PythonUtil import *
from direct.showbase import AppRunnerGlobal
import string
import os
from ItemConstants import *
from pirates.uberdog.UberDogGlobals import InventoryType, InventoryCategory
from pirates.battle.EnemySkills import *
import ItemData

__itemInfo = ItemData.itemInfo
__columnHeadings = __itemInfo.pop('columnHeadings')
for (heading, value) in __columnHeadings.items():
    heading = string.replace(heading, '\r', '')
    exec '%s = %s' % (heading, value) in globals()

for item in __itemInfo:
    exec '%s = %s' % (__itemInfo[item][CONSTANT_NAME], item) in globals()

del __columnHeadings
GOLD_SALE_MULTIPLIER = 0.050000000000000003
LEVEL_REQ_BUFFER = 0
WEAPON_LEVEL_REQ_BUFFER = 5
ENEMY_LEVEL_REQ_BUFFER = 10
BLOOD_FIRE_MAX = 10
BLOOD_FIRE_TIMER = 30.0
BLOOD_FIRE_BONUS = 0.050000000000000003

def getAllItemIds():
    return __itemInfo.keys()


def getAllWeaponIds(type = None):
    keys = []
    for item in __itemInfo:
        if __itemInfo[item][ITEM_CLASS] == InventoryType.ItemTypeWeapon:
            if type:
                if __itemInfo[item][ITEM_TYPE] != type:
                    continue
                
            
            keys.append(item)
            continue
    
    return keys


def getAllClothingIds(gender = None):
    keys = []
    for item in __itemInfo:
        if __itemInfo[item][ITEM_CLASS] == InventoryType.ItemTypeClothing:
            if gender:
                if (gender == 'm' or __itemInfo[item][MALE_MODEL_ID] == -1 or gender == 'f') and __itemInfo[item][FEMALE_MODEL_ID] == -1:
                    continue
                
            keys.append(item)
            continue
    
    return keys


def getClothingByType(type):
    keys = []
    for item in __itemInfo:
        if __itemInfo[item][ITEM_CLASS] == InventoryType.ItemTypeClothing and __itemInfo[item][ITEM_TYPE] == type:
            keys.append(item)
            continue
    
    return keys


def getAllJewelryIds():
    keys = []
    for item in __itemInfo:
        if __itemInfo[item][ITEM_CLASS] == InventoryType.ItemTypeJewelry:
            keys.append(item)
            continue
    
    return keys


def getJewelryByType(type):
    keys = []
    for item in __itemInfo:
        if __itemInfo[item][ITEM_CLASS] == InventoryType.ItemTypeJewelry and __itemInfo[item][ITEM_TYPE] == type:
            keys.append(item)
            continue
    
    return keys


def getAllTattooIds():
    keys = []
    for item in __itemInfo:
        if __itemInfo[item][ITEM_CLASS] == InventoryType.ItemTypeTattoo:
            keys.append(item)
            continue
    
    return keys


def getTattoosByType(type):
    keys = []
    for item in __itemInfo:
        if __itemInfo[item][ITEM_CLASS] == InventoryType.ItemTypeTattoo and __itemInfo[item][ITEM_TYPE] == type:
            keys.append(item)
            continue
    
    return keys


def getAllCharmIds():
    keys = []
    for item in __itemInfo:
        if __itemInfo[item][ITEM_CLASS] == InventoryType.ItemTypeCharm:
            keys.append(item)
            continue
    
    return keys


def getAllConsumableIds(usableOnly = True):
    keys = []
    for item in __itemInfo:
        if __itemInfo[item][ITEM_CLASS] == InventoryType.ItemTypeConsumable:
            if usableOnly == False or not __itemInfo[item][FROM_QUEST]:
                keys.append(item)
                continue
    
    return keys


def getAllHealthIds():
    keys = []
    for item in __itemInfo:
        if __itemInfo[item][ITEM_CLASS] == InventoryType.ItemTypeConsumable and __itemInfo[item][AUTO_TONIC]:
            keys.append(item)
            continue
    
    return keys


def getHumanWeaponTypes():
    keys = []
    for item in __itemInfo:
        if __itemInfo[item][ITEM_CLASS] == InventoryType.ItemTypeWeapon or __itemInfo[item][ITEM_CLASS] == InventoryType.ItemTypeConsumable:
            keys.append(item)
            continue
    
    return keys


def getVersion(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[VERSION]
    
    return 0


def getGoldCost(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[GOLD_COST]
    
    return 0


def getName(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return str(item[ITEM_NAME])
    
    return ''


def getConstantName(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return str(item[CONSTANT_NAME])
    
    return ''


def getRarity(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[RARITY]
    
    return 0


def getClass(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[ITEM_CLASS]
    
    return 0


def getType(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[ITEM_TYPE]
    
    return 0


def isFromLoot(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[FROM_LOOT]
    
    return 0


def isFromShop(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[FROM_SHOP]
    
    return 0


def isFromQuest(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[FROM_QUEST]
    
    return 0


def isFromPromo(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[FROM_PROMO]
    
    return 0


def isFromPVP(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[FROM_PVP]
    
    return 0


def isFromNPC(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[FROM_NPC]
    
    return 0


def getLegalWeapons(rarity, items, level, weaponLevels, enemyLevel):
    typeItems = []
    for itemId in items:
        item = __itemInfo.get(itemId)
        if item and item[ITEM_CLASS] in (InventoryType.ItemTypeWeapon, InventoryType.ItemTypeCharm) and item[FROM_LOOT] and item[RARITY] == rarity and item[ITEM_NOTORIETY_REQ] <= level + LEVEL_REQ_BUFFER and item[ITEM_NOTORIETY_REQ] <= enemyLevel + ENEMY_LEVEL_REQ_BUFFER:
            itemType = item[ITEM_TYPE]
            itemClass = item[ITEM_CLASS]
            if itemClass == InventoryType.ItemTypeWeapon:
                if item[WEAPON_REQ] <= weaponLevels[itemType - 1] + WEAPON_LEVEL_REQ_BUFFER:
                    typeItems.append(itemId)
                
            else:
                typeItems.append(itemId)
        itemClass == InventoryType.ItemTypeWeapon
    
    return typeItems


def getLegalConsumables(rarity, items, level):
    typeItems = []
    for itemId in items:
        item = __itemInfo.get(itemId)
        if item and item[ITEM_CLASS] == InventoryType.ItemTypeConsumable and item[FROM_LOOT] and item[RARITY] == rarity and item[ITEM_NOTORIETY_REQ] <= level + LEVEL_REQ_BUFFER:
            typeItems.append(itemId)
            continue
    
    return typeItems


def getLegalClothing(rarity, gender, items, level):
    typeItems = []
    for itemId in items:
        item = __itemInfo.get(itemId)
        if item and item[ITEM_CLASS] == InventoryType.ItemTypeClothing and item[FROM_LOOT] and item[RARITY] == rarity and item[ITEM_NOTORIETY_REQ] <= level + LEVEL_REQ_BUFFER:
            if gender == 'm':
                modelId = item[MALE_MODEL_ID]
            else:
                modelId = item[FEMALE_MODEL_ID]
            if modelId != -1:
                typeItems.append(itemId)
            
        modelId != -1
    
    return typeItems


def getLegalStoreItems(items):
    typeItems = []
    for itemId in items:
        item = __itemInfo.get(itemId)
        if item[FROM_SHOP]:
            typeItems.append(itemId)
            continue
    
    return typeItems


def getGenderType(type, gender, items):
    typeItems = []
    for item in items:
        if getType(item) == type:
            if gender == 'm':
                modelId = getMaleModelId(item)
            else:
                modelId = getFemaleModelId(item)
            if modelId != -1:
                typeItems.append(item)
            
        modelId != -1
    
    return typeItems


def getSubtype(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[ITEM_SUBTYPE]
    
    return 0


def getNotorietyRequirement(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[ITEM_NOTORIETY_REQ]
    
    return 0


def getLandInfamyRequirement(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[ITEM_LAND_INFAMY_REQ]
    
    return 0


def getSeaInfamyRequirement(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[ITEM_SEA_INFAMY_REQ]
    
    return 0


def getQuestRequirement(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return str(item[QUEST_REQ])
    
    return ''


def getWeaponRequirement(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[WEAPON_REQ]
    
    return 0


def getPower(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[POWER]
    
    return 0


def getBarrels(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[BARRELS]
    
    return 0


def getSpecialAttackRank(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[SPECIAL_ATTACK_RANK]
    
    return 0


def getSpecialAttack(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[SPECIAL_ATTACK]
    
    return 0


def getAttributeRank1(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[ATTRIBUTE_1_RANK]
    
    return 0


def getAttribute1(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[ATTRIBUTE_1]
    
    return 0


def getAttributeRank2(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[ATTRIBUTE_2_RANK]
    
    return 0


def getAttribute2(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[ATTRIBUTE_2]
    
    return 0


def getAttributeRank3(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[ATTRIBUTE_3_RANK]
    
    return 0


def getAttribute3(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[ATTRIBUTE_3]
    
    return 0


def getWeaponAttributes(itemId, attributeId):
    boostId1 = getAttribute1(itemId)
    if boostId1 == attributeId:
        return getAttributeRank1(itemId)
    
    boostId2 = getAttribute2(itemId)
    if boostId2 == attributeId:
        return getAttributeRank2(itemId)
    
    boostId3 = getAttribute3(itemId)
    if boostId3 == attributeId:
        return getAttributeRank3(itemId)
    
    return 0


def getAttributes(itemId):
    attributes = []
    item = __itemInfo.get(itemId)
    if item:
        attribute1 = getAttribute1(itemId)
        attributeRank1 = getAttributeRank1(itemId)
        if attribute1 and attributeRank1:
            attributes.append((attribute1, attributeRank1))
        
        attribute2 = getAttribute2(itemId)
        attributeRank2 = getAttributeRank2(itemId)
        if attribute2 and attributeRank2:
            attributes.append((attribute2, attributeRank2))
        
        attribute3 = getAttribute3(itemId)
        attributeRank3 = getAttributeRank3(itemId)
        if attribute3 and attributeRank3:
            attributes.append((attribute3, attributeRank3))
        
    
    return attributes


def getSkillBoostRank1(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[SKILLBOOST_1_RANK]
    
    return 0


def getSkillBoost1(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[SKILLBOOST_1]
    
    return 0


def getSkillBoostRank2(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[SKILLBOOST_2_RANK]
    
    return 0


def getSkillBoost2(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[SKILLBOOST_2]
    
    return 0


def getSkillBoostRank3(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[SKILLBOOST_3_RANK]
    
    return 0


def getSkillBoost3(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[SKILLBOOST_3]
    
    return 0


def getWeaponBoosts(itemId, skillId):
    boostId1 = getSkillBoost1(itemId)
    if boostId1 == skillId:
        return getSkillBoostRank1(itemId)
    
    boostId2 = getSkillBoost2(itemId)
    if boostId2 == skillId:
        return getSkillBoostRank2(itemId)
    
    boostId3 = getSkillBoost3(itemId)
    if boostId3 == skillId:
        return getSkillBoostRank3(itemId)
    
    return 0


def getSkillBoosts(itemId):
    skillBoosts = []
    item = __itemInfo.get(itemId)
    if item:
        skillBoost1 = getSkillBoost1(itemId)
        skillBoostRank1 = getSkillBoostRank1(itemId)
        if skillBoost1 and skillBoostRank1:
            skillBoosts.append((skillBoost1, skillBoostRank1))
        
        skillBoost2 = getSkillBoost2(itemId)
        skillBoostRank2 = getSkillBoostRank2(itemId)
        if skillBoost2 and skillBoostRank2:
            skillBoosts.append((skillBoost2, skillBoostRank2))
        
        skillBoost3 = getSkillBoost3(itemId)
        skillBoostRank3 = getSkillBoostRank3(itemId)
        if skillBoost3 and skillBoostRank3:
            skillBoosts.append((skillBoost3, skillBoostRank3))
        
    
    return skillBoosts


def getModel(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return str(item[ITEM_MODEL])
    


def getColor(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[ITEM_COLOR]
    
    return 0


def getIcon(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return str(item[ITEM_ICON])
    


def getVfxType1(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[VFX_TYPE_1]
    
    return 0


def getVfxType2(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[VFX_TYPE_2]
    
    return 0


def getVfxOffset(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[VFX_OFFSET]
    
    return 0


def getFlavorText(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[FLAVOR_TEXT]
    
    return ''

HAS_HOLIDAY_DATA = {
    InventoryType.ItemTypeWeapon: False,
    InventoryType.ItemTypeClothing: True,
    InventoryType.ItemTypeTattoo: True,
    InventoryType.ItemTypeJewelry: True,
    InventoryType.ItemTypeMusic: False,
    InventoryType.ItemTypeCharm: False,
    InventoryType.ItemTypeConsumable: False,
    InventoryType.ItemTypeMoney: False }

def getHoliday(itemId):
    item = __itemInfo.get(itemId)
    itemType = getClass(itemId)
    if item and HAS_HOLIDAY_DATA.get(itemType, False):
        return item[HOLIDAY]
    else:
        return 0


def getStackLimit(itemId):
    item = __itemInfo.get(itemId)
    if item:
        if item[ITEM_CLASS] == InventoryType.ItemTypeConsumable:
            return item[STACK_LIMIT]
        
    
    return 0


def isAutoTonic(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[AUTO_TONIC]
    
    return 0


def getUseSkill(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[USE_SKILL]
    
    return 0


def getMaleModelId(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[MALE_MODEL_ID]
    
    return 0


def getMaleTextureId(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[MALE_TEXTURE_ID]
    
    return 0


def getFemaleModelId(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[FEMALE_MODEL_ID]
    
    return 0


def getFemaleTextureId(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[FEMALE_TEXTURE_ID]
    
    return 0


def canDyeItem(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[CAN_DYE_ITEM]
    
    return 0


def getPrimaryColor(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[PRIMARY_COLOR]
    
    return 0


def getSecondaryColor(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[SECONDARY_COLOR]
    
    return 0


def getMaleOrientation(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[MALE_ORIENTATION]
    
    return 0


def getMaleOrientation2(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[MALE_ORIENTATION_2]
    
    return 0


def getFemaleOrientation(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[FEMALE_ORIENTATION]
    
    return 0


def getFemaleOrientation2(itemId):
    item = __itemInfo.get(itemId)
    if item:
        return item[FEMALE_ORIENTATION_2]
    
    return 0

AttributeIcons = {
    CRITICAL: 'dagger_gouge',
    VENOM: 'dagger_adder',
    POWERFUL: 'dagger_gouge',
    PROTECT_COMBAT: 'dagger_gouge',
    PROTECT_MISSILE: 'dagger_gouge',
    PROTECT_MAGIC: 'dagger_gouge',
    PROTECT_GRENADE: 'dagger_gouge',
    DAMAGE_MANA: 'dagger_gouge',
    SURE_FOOTED: 'dagger_gouge',
    BLOOD_FIRE: 'cutlass_bladestorm',
    INFINITE_VENOM_SHOT: 'venom',
    INFINITE_BANE_SHOT: 'steel',
    INFINITE_HEX_EATER_SHOT: 'gold',
    INFINITE_SILVER_SHOT: 'silver',
    INFINITE_STEEL_SHOT: 'iron',
    INFINITE_ASP: 'dagger_throw',
    INFINITE_ADDER: 'dagger_adder',
    INFINITE_SIDEWINDER: 'dagger_sidewinder',
    INFINITE_VIPER_NEST: 'dagger_vipers_nest',
    INFINITE_CHAIN_SHOT: 'cannon_chain_shot',
    INFINITE_EXPLOSIVE: 'cannon_explosive',
    INFINITE_GRAPE_SHOT: 'cannon_grape_shot',
    INFINITE_FIREBRAND: 'cannon_firebrand',
    INFINITE_THUNDERBOLT: 'cannon_thunderbolt',
    INFINITE_FURY: 'cannon_fury',
    LEECH_HEALTH: 'dagger_gouge',
    LEECH_VOODOO: 'dagger_gouge',
    CRITICAL_ROUND_SHOT: 'cannon_round_shot',
    CRITICAL_CHAIN_SHOT: 'cannon_chain_shot',
    CRITICAL_EXPLOSIVE: 'cannon_explosive',
    CRITICAL_GRAPE_SHOT: 'cannon_grape_shot',
    CRITICAL_FIREBRAND: 'cannon_firebrand',
    CRITICAL_FURY: 'cannon_fury',
    RANGE_ROUND_SHOT: 'cannon_round_shot',
    RANGE_CHAIN_SHOT: 'cannon_chain_shot',
    RANGE_EXPLOSIVE: 'cannon_explosive',
    RANGE_GRAPE_SHOT: 'cannon_grape_shot',
    RANGE_FIREBRAND: 'cannon_firebrand',
    RANGE_FURY: 'cannon_fury',
    IMMUNITY_POISON: 'buff_poison',
    IMMUNITY_ACID: 'buff_acid',
    IMMUNITY_BLIND: 'buff_blind',
    IMMUNITY_FIRE: 'buff_burn',
    IMMUNITY_HOLD: 'buff_hold',
    IMMUNITY_STUN: 'buff_stun',
    IMMUNITY_PAIN: 'buff_stun',
    IMMUNITY_CURSE: 'buff_curse',
    IMMUNITY_WEAKEN: 'buff_weaken',
    IMMUNITY_LIFEDRAIN: 'buff_weaken',
    HALF_DURATION_POISON: 'buff_poison',
    HALF_DURATION_ACID: 'buff_acid',
    HALF_DURATION_BLIND: 'buff_blind',
    HALF_DURATION_FIRE: 'buff_burn',
    HALF_DURATION_HOLD: 'buff_hold',
    HALF_DURATION_STUN: 'buff_stun',
    HALF_DURATION_CURSE: 'buff_curse',
    HALF_DURATION_PAIN: 'buff_stun',
    HALF_DURATION_WOUND: 'buff_wound',
    HALF_DAMAGE_LIFEDRAIN: 'buff_weaken',
    HALF_DAMAGE_SOULTAP: 'buff_weaken',
    NAVIGATION: 'sail_full_sail',
    ANTI_VOODOO_ZOMBIE: 'buff_stun' }

def getAttributeIcon(attributeId):
    return AttributeIcons.get(attributeId)

BoostIcons = {
    InventoryType.PistolLeadShot: 'lead' }

def getBoostIcon(boostId):
    return BoostIcons.get(boostId)

ChargingAnims = {
    PISTOL: 'gun_aim_idle',
    REPEATER: 'gun_aim_idle',
    BLUNDERBUSS: 'rifle_fight_shoot_high_idle',
    MUSKET: 'rifle_fight_shoot_high_idle',
    BAYONET: 'rifle_fight_shoot_high_idle' }

def getChargingAnim(subtypeId):
    return ChargingAnims.get(subtypeId)

ReloadAnims = {
    PISTOL: 'gun_reload',
    REPEATER: 'gun_reload',
    BLUNDERBUSS: 'blunderbuss_reload',
    MUSKET: 'rifle_reload_hip',
    BAYONET: 'rifle_reload_hip' }

def getReloadAnim(subtypeId):
    return ReloadAnims.get(subtypeId)

FireAnims = {
    PISTOL: 'gun_fire',
    REPEATER: 'gun_fire',
    BLUNDERBUSS: 'rifle_fight_shoot_hip',
    MUSKET: 'rifle_fight_shoot_hip',
    BAYONET: 'rifle_fight_shoot_hip' }

def getFireAnim(subtypeId):
    return FireAnims.get(subtypeId)

TakeAimAnims = {
    PISTOL: 'gun_fire',
    REPEATER: 'gun_fire',
    BLUNDERBUSS: 'rifle_fight_shoot_high',
    MUSKET: 'rifle_fight_shoot_high',
    BAYONET: 'rifle_fight_shoot_high' }

def getTakeAimAnim(subtypeId):
    return TakeAimAnims.get(subtypeId)

JumpAnimInfo = {
    BLUNDERBUSS: [
        'bayonet_jump',
        1,
        9,
        32,
        46],
    MUSKET: [
        'bayonet_jump',
        1,
        9,
        32,
        46],
    BAYONET: [
        'bayonet_jump',
        1,
        9,
        32,
        46] }

def getJumpAnimInfo(weaponInfo):
    if weaponInfo[1]:
        subtypeId = getSubtype(weaponInfo[0])
        animInfo = JumpAnimInfo.get(subtypeId)
        if animInfo:
            return animInfo
        
    
    return [
        'jump',
        1,
        7,
        31,
        43]

StopToAimSubtypes = [
    MUSKET,
    BAYONET]

def shouldStopToAim(subtypeId):
    if subtypeId in StopToAimSubtypes:
        return True
    
    return False

LinkedSkills = {
    BROADSWORD: [
        EnemySkills.BROADSWORD_HACK,
        EnemySkills.BROADSWORD_SLASH,
        EnemySkills.BROADSWORD_CLEAVE,
        EnemySkills.BROADSWORD_FLOURISH,
        EnemySkills.BROADSWORD_STAB],
    SABRE: [
        EnemySkills.SABRE_HACK,
        EnemySkills.SABRE_SLASH,
        EnemySkills.SABRE_CLEAVE,
        EnemySkills.SABRE_FLOURISH,
        EnemySkills.SABRE_STAB],
    CURSED_BROADSWORD: [
        EnemySkills.BROADSWORD_HACK,
        EnemySkills.BROADSWORD_SLASH,
        EnemySkills.BROADSWORD_CLEAVE,
        EnemySkills.BROADSWORD_FLOURISH,
        EnemySkills.BROADSWORD_STAB],
    CURSED_SABRE: [
        EnemySkills.SABRE_HACK,
        EnemySkills.SABRE_SLASH,
        EnemySkills.SABRE_CLEAVE,
        EnemySkills.SABRE_FLOURISH,
        EnemySkills.SABRE_STAB],
    BLUNDERBUSS: [
        EnemySkills.PISTOL_SCATTERSHOT,
        EnemySkills.PISTOL_SCATTERSHOT_AIM],
    DIRK: [
        EnemySkills.DAGGER_THROW_COMBO_1,
        EnemySkills.DAGGER_THROW_COMBO_2,
        EnemySkills.DAGGER_THROW_COMBO_3,
        EnemySkills.DAGGER_THROW_COMBO_4] }

def getLinkedSkills(weaponId):
    subtypeId = getSubtype(weaponId)
    return LinkedSkills.get(subtypeId, [])

__weaponId2SkillCategory = {
    InventoryType.MeleeWeaponL1: InventoryCategory.WEAPON_SKILL_MELEE,
    InventoryType.MeleeWeaponL2: InventoryCategory.WEAPON_SKILL_MELEE,
    InventoryType.MeleeWeaponL3: InventoryCategory.WEAPON_SKILL_MELEE,
    InventoryType.MeleeWeaponL4: InventoryCategory.WEAPON_SKILL_MELEE,
    InventoryType.MeleeWeaponL5: InventoryCategory.WEAPON_SKILL_MELEE,
    InventoryType.MeleeWeaponL6: InventoryCategory.WEAPON_SKILL_MELEE,
    SWORD: InventoryCategory.WEAPON_SKILL_CUTLASS,
    PISTOL: InventoryCategory.WEAPON_SKILL_PISTOL,
    REPEATER: InventoryCategory.WEAPON_SKILL_PISTOL,
    BLUNDERBUSS: InventoryCategory.WEAPON_SKILL_PISTOL,
    MUSKET: InventoryCategory.WEAPON_SKILL_MUSKET,
    BAYONET: InventoryCategory.WEAPON_SKILL_MUSKET,
    DAGGER: InventoryCategory.WEAPON_SKILL_DAGGER,
    GRENADE: InventoryCategory.WEAPON_SKILL_GRENADE,
    STAFF: InventoryCategory.WEAPON_SKILL_WAND,
    DOLL: InventoryCategory.WEAPON_SKILL_DOLL,
    InventoryType.KettleWeaponL1: InventoryCategory.WEAPON_SKILL_KETTLE,
    InventoryType.KettleWeaponL2: InventoryCategory.WEAPON_SKILL_KETTLE,
    InventoryType.KettleWeaponL3: InventoryCategory.WEAPON_SKILL_KETTLE }

def getSkillCategory(weaponId):
    type = getType(weaponId)
    if type == GUN:
        return __weaponId2SkillCategory.get(getSubtype(weaponId))
    elif type:
        return __weaponId2SkillCategory.get(type)
    
    return __weaponId2SkillCategory.get(weaponId)

TattooOrientations = {
    MaleChestFullTorso: [
        0.127,
        0.20300000000000001,
        0.155,
        0.0],
    MaleChestUpperChest: [
        0.127,
        0.22500000000000001,
        0.125,
        0.0],
    MaleChestHPeck: [
        0.047,
        0.23499999999999999,
        0.055,
        0.0],
    MaleChestRight: [
        0.091999999999999998,
        0.26500000000000001,
        0.062,
        0.0],
    MaleChestPBrand: [
        0.050000000000000003,
        0.27500000000000002,
        0.028000000000000001,
        346.5],
    MaleChestLScar: [
        0.085000000000000006,
        0.28999999999999998,
        0.044999999999999998,
        75.0],
    MaleChestBulletHoles: [
        0.074999999999999997,
        0.27000000000000002,
        0.055,
        81.0],
    MaleChestLX: [
        0.050000000000000003,
        0.26000000000000001,
        0.057000000000000002,
        262.0],
    MaleChestLY: [
        0.074999999999999997,
        0.28000000000000003,
        0.070000000000000007,
        106.0],
    FemaleChestFullChest: [
        0.55500000000000005,
        0.84199999999999997,
        0.12,
        0.0],
    FemaleChestUpperChest: [
        0.55500000000000005,
        0.87,
        0.080000000000000002,
        0.0],
    FemaleChestLeftBreast: [
        0.57999999999999996,
        0.86199999999999999,
        0.044999999999999998,
        0.0],
    FemaleChestHPeck: [
        0.25700000000000001,
        0.88500000000000001,
        0.044999999999999998,
        0.0],
    FemaleChestBulletHoles: [
        0.29099999999999998,
        0.88,
        0.033000000000000002,
        87.412999999999997],
    FemaleChestPBrand: [
        0.29999999999999999,
        0.871,
        0.024,
        0.0],
    FemaleChestLScar: [
        0.29999999999999999,
        0.88,
        0.042000000000000003,
        78.046999999999997],
    FemaleChestLX: [
        0.25700000000000001,
        0.86199999999999999,
        0.042000000000000003,
        93.745999999999995],
    FemaleChestLY: [
        0.29999999999999999,
        0.871,
        0.042000000000000003,
        99.900000000000006],
    MaleArmLeftUpper: [
        0.105,
        0.56999999999999995,
        0.050000000000000003,
        271.10000000000002],
    MaleArmLeftFlag: [
        0.20000000000000001,
        0.57999999999999996,
        0.070000000000000007,
        270.0],
    MaleArmLeftSleeve: [
        0.11799999999999999,
        0.56200000000000006,
        0.083000000000000004,
        267],
    MaleArmLeftLower: [
        0.105,
        0.56999999999999995,
        0.050000000000000003,
        271.10000000000002],
    MaleArmLeftLowerFlag: [
        0.20000000000000001,
        0.57999999999999996,
        0.070000000000000007,
        270.0],
    MaleArmLeftLowerSleeve: [
        0.11799999999999999,
        0.56200000000000006,
        0.083000000000000004,
        267],
    FemaleArmLeftUpper: [
        0.14999999999999999,
        0.79000000000000004,
        0.050000000000000003,
        271.10000000000002],
    FemaleArmLeftFlag: [
        0.29999999999999999,
        0.79000000000000004,
        0.070000000000000007,
        271.10000000000002],
    FemaleArmLeftSleeve: [
        0.062,
        0.79000000000000004,
        0.066000000000000003,
        267],
    FemaleArmLeftLower: [
        0.14999999999999999,
        0.79000000000000004,
        0.050000000000000003,
        271.10000000000002],
    FemaleArmLeftLowerFlag: [
        0.29999999999999999,
        0.79000000000000004,
        0.070000000000000007,
        271.10000000000002],
    FemaleArmLeftLowerSleeve: [
        0.062,
        0.79000000000000004,
        0.066000000000000003,
        267],
    MaleArmRightUpper: [
        0.11,
        0.83999999999999997,
        0.050000000000000003,
        271.10000000000002],
    MaleArmRightFlag: [
        0.20000000000000001,
        0.83999999999999997,
        0.070000000000000007,
        271.10000000000002],
    MaleArmRightSleeve: [
        0.11600000000000001,
        0.83999999999999997,
        0.070000000000000007,
        271.10000000000002],
    MaleArmRightLower: [
        0.20999999999999999,
        0.83999999999999997,
        0.050000000000000003,
        271.10000000000002],
    MaleArmRightLowerFlag: [
        0.20000000000000001,
        0.83999999999999997,
        0.070000000000000007,
        271.10000000000002],
    MaleArmRightLowerSleeve: [
        0.11600000000000001,
        0.83999999999999997,
        0.070000000000000007,
        271.10000000000002],
    FemaleArmRightUpper: [
        0.14999999999999999,
        0.61399999999999999,
        0.040000000000000001,
        271.10000000000002],
    FemaleArmRightFlag: [
        0.29999999999999999,
        0.61399999999999999,
        0.070000000000000007,
        271.10000000000002],
    FemaleArmRightSleeve: [
        0.10100000000000001,
        0.627,
        0.066000000000000003,
        286.709],
    FemaleArmRightLower: [
        0.14999999999999999,
        0.61399999999999999,
        0.040000000000000001,
        271.10000000000002],
    FemaleArmRightLowerFlag: [
        0.29999999999999999,
        0.61399999999999999,
        0.070000000000000007,
        271.10000000000002],
    FemaleArmRightLowerSleeve: [
        0.10100000000000001,
        0.627,
        0.066000000000000003,
        286.709],
    MaleFace1: [
        0.5,
        0.5,
        1.0,
        0.0],
    MaleFace2: [
        0.75,
        0.45000000000000001,
        0.29999999999999999,
        0.0],
    MaleFace3: [
        0.66500000000000004,
        0.66500000000000004,
        0.23599999999999999,
        15.609],
    MaleFace4: [
        0.69099999999999995,
        0.40500000000000003,
        0.38200000000000001,
        0.0],
    MaleFace5: [
        0.498,
        0.19600000000000001,
        0.33000000000000002,
        0.0],
    MaleFace6: [
        0.498,
        0.56899999999999995,
        0.38300000000000001,
        0.0],
    MaleFace7: [
        0.498,
        0.127,
        0.27200000000000002,
        0.0],
    MaleFace8: [
        0.504,
        0.48299999999999998,
        0.22,
        0.0],
    MaleFace9: [
        0.495,
        0.30099999999999999,
        0.33200000000000002,
        0.0],
    MaleFace10: [
        0.65100000000000002,
        0.59499999999999997,
        0.40000000000000002,
        9.3659999999999997],
    MaleFace11: [
        0.23899999999999999,
        0.39600000000000002,
        0.26200000000000001,
        0.0],
    MaleFace12: [
        0.23899999999999999,
        0.39600000000000002,
        0.219,
        0.0],
    MaleFace13: [
        0.38700000000000001,
        0.308,
        0.099000000000000005,
        0.0],
    MaleFace14: [
        0.11799999999999999,
        0.38700000000000001,
        0.313,
        171.703],
    MaleFace15: [
        0.32700000000000001,
        0.75,
        0.23599999999999999,
        262.238],
    MaleFace16: [
        0.11799999999999999,
        0.43099999999999999,
        0.25600000000000001,
        96.778000000000006],
    FemaleFace1: [
        0.5,
        0.44,
        0.84999999999999998,
        0.0],
    FemaleFace2: [
        0.69999999999999996,
        0.37,
        0.25,
        0.0],
    FemaleFace3: [
        0.63900000000000001,
        0.59499999999999997,
        0.22700000000000001,
        0.0],
    FemaleFace4: [
        0.65600000000000003,
        0.35299999999999998,
        0.27000000000000002,
        0.0],
    FemaleFace5: [
        0.499,
        0.20499999999999999,
        0.245,
        0.0],
    FemaleFace6: [
        0.499,
        0.48299999999999998,
        0.35599999999999998,
        0.0],
    FemaleFace7: [
        0.499,
        0.153,
        0.20999999999999999,
        0.0],
    FemaleFace8: [
        0.499,
        0.42199999999999999,
        0.14099999999999999,
        0.0],
    FemaleFace9: [
        0.499,
        0.27500000000000002,
        0.33900000000000002,
        0.0],
    FemaleFace10: [
        0.65600000000000003,
        0.52400000000000002,
        0.33900000000000002,
        3.1219999999999999],
    FemaleFace11: [
        0.32700000000000001,
        0.33500000000000002,
        0.23599999999999999,
        0.0],
    FemaleFace12: [
        0.32700000000000001,
        0.33500000000000002,
        0.184,
        0.0],
    FemaleFace13: [
        0.33400000000000002,
        0.32700000000000001,
        0.099000000000000005,
        0.0],
    FemaleFace14: [
        0.17000000000000001,
        0.34200000000000003,
        0.14999999999999999,
        109.26600000000001],
    FemaleFace15: [
        0.33500000000000002,
        0.63900000000000001,
        0.184,
        90.534000000000006],
    FemaleFace16: [
        0.153,
        0.36799999999999999,
        0.14999999999999999,
        106.143] }

def getOrientation(orientationNum):
    return TattooOrientations.get(orientationNum, [
        0.0,
        0.0,
        0.0,
        0.0])

_itemTattoosInitialized = 0
ItemTattooImages = { }

def initItemTattooImages():
    global _tattoosInitialized
    tattoos = loader.loadModel('models/misc/tattoos')
    for i in getAllTattooIds():
        image = tattoos.find('**/%s' % getIcon(i)).findAllTextures().getTexture(0)
        scale = float(image.getXSize()) / float(image.getYSize())
        image.setWrapU(Texture.WMBorderColor)
        image.setWrapV(Texture.WMBorderColor)
        image.setBorderColor(Vec4(1, 1, 1, 1))
        ItemTattooImages[i] = (image, scale)
    
    _tattoosInitialized = 1


def getItemTattooImage(tattooNum):
    if _itemTattoosInitialized == 0:
        initItemTattooImages()
    
    return ItemTattooImages.get(tattooNum)


def getItemRepId(itemId):
    itemType = getType(itemId)
    if itemType == SWORD:
        return InventoryType.CutlassRep
    elif itemType == GUN:
        return InventoryType.PistolRep
    elif itemType == DOLL:
        return InventoryType.DollRep
    elif itemType == DAGGER:
        return InventoryType.DaggerRep
    elif itemType == GRENADE:
        return InventoryType.GrenadeRep
    elif itemType == STAFF:
        return InventoryType.WandRep
    elif itemType == CANNON:
        return InventoryType.CannonRep
    elif itemType == SAILING:
        return InventoryType.SailingRep
    

ModelPosHpr = {
    'pir_m_hnd_dol_bane_a': [
        0.0,
        1.5,
        -0.10000000000000001,
        0,
        90,
        180],
    'pir_m_hnd_dol_bane_b': [
        0.0,
        1.8,
        -0.10000000000000001,
        0,
        90,
        180],
    'pir_m_hnd_dol_bane_d': [
        0.0,
        1.5,
        -0.10000000000000001,
        0,
        90,
        180],
    'pir_m_hnd_dol_mojo_b': [
        0.0,
        1.8,
        -0.14999999999999999,
        0,
        90,
        180],
    'pir_m_hnd_dol_mojo_c': [
        0.0,
        1.8999999999999999,
        -0.050000000000000003,
        0,
        90,
        180],
    'pir_m_hnd_dol_mojo_d': [
        0.0,
        1.5,
        -0.10000000000000001,
        0,
        90,
        180],
    'pir_m_hnd_dol_mojo_e': [
        0.0,
        1.8999999999999999,
        -0.050000000000000003,
        0,
        90,
        180],
    'pir_m_hnd_dol_spirit_a': [
        0.0,
        1.8,
        -0.050000000000000003,
        0,
        90,
        180],
    'pir_m_hnd_dol_spirit_b': [
        0.0,
        1.6000000000000001,
        -0.050000000000000003,
        0,
        90,
        180],
    'pir_m_hnd_dol_spirit_c': [
        0.0,
        1.2,
        -0.10000000000000001,
        0,
        90,
        180],
    'pir_m_hnd_dol_spirit_d': [
        0.0,
        1.6000000000000001,
        -0.050000000000000003,
        0,
        90,
        180],
    'pir_m_hnd_dol_spirit_e': [
        0.0,
        1.6000000000000001,
        -0.050000000000000003,
        0,
        90,
        180],
    'pir_m_inv_can_ram_c': [
        -0.80000000000000004,
        1.5,
        -0.29999999999999999,
        70,
        160,
        -90],
    'pir_m_inv_can_ram_d': [
        -0.80000000000000004,
        1.5,
        -0.29999999999999999,
        70,
        160,
        -90],
    'pir_m_inv_can_spyglass_a': [
        0.0,
        1.3,
        0.0,
        90,
        -10,
        -90],
    'pir_m_inv_can_spyglass_b': [
        -0.20000000000000001,
        2.0,
        0.0,
        90,
        -10,
        -90],
    'pir_m_inv_can_spyglass_c': [
        -0.80000000000000004,
        2.0,
        -0.12,
        90,
        -10,
        -90],
    'pir_m_inv_can_spyglass_d': [
        0.0,
        0.20000000000000001,
        0.0,
        90,
        -10,
        -90],
    'pir_m_inv_sal_charts': [
        0.0,
        2.0,
        0.0,
        90,
        80,
        -90],
    'pir_m_inv_sal_globe_a': [
        0.0,
        0.29999999999999999,
        -0.059999999999999998,
        0,
        0,
        0],
    'pir_m_inv_sal_globe_b': [
        0.0,
        13.0,
        1.0,
        0,
        0,
        0],
    'pir_m_inv_pot_porkTonic': [
        0.0,
        2.5,
        -0.40000000000000002,
        45,
        0,
        0] }

def getModelPosHpr(model):
    return ModelPosHpr.get(model, None)


def getDefaultMaleClothing():
    maleShirt = COTTON_SHORT_SLEEVE
    maleShirtDye = 1
    maleShirtColor = 0
    maleVest = 0
    maleVestDye = 0
    maleVestColor = 0
    malePant = COTTON_HIGHWATERS
    malePantDye = 1
    malePantColor = 14
    maleBelt = BASIC_SASH
    maleBeltDye = 1
    maleBeltColor = 0
    maleShoe = COMFY_BOOTS
    maleShoeDye = 0
    maleShoeColor = 0
    defaultMaleClothing = {
        'HAT': [
            0,
            0,
            0],
        'SHIRT': [
            maleShirt,
            maleShirtDye,
            maleShirtColor],
        'VEST': [
            maleVest,
            maleVestDye,
            maleVestColor],
        'COAT': [
            0,
            0,
            0],
        'BELT': [
            maleBelt,
            maleBeltDye,
            maleBeltColor],
        'PANT': [
            malePant,
            malePantDye,
            malePantColor],
        'SHOE': [
            maleShoe,
            maleShoeDye,
            0] }
    return defaultMaleClothing


def getDefaultFemaleClothing():
    femaleShirt = STITCHED_BLOUSE
    femaleShirtDye = 1
    femaleShirtColor = 0
    femaleVest = 0
    femaleVestDye = 0
    femaleVestColor = 0
    femalePant = PATCHWORK_CAPRIS
    femalePantDye = 0
    femalePantColor = 0
    femaleBelt = BUCKLE_SASH
    femaleBeltDye = 1
    femaleBeltColor = 0
    femaleShoe = DECK_SLAPPER_BOOTS
    femaleShoeDye = 0
    femaleShoeColor = 0
    defaultFemaleClothing = {
        'HAT': [
            0,
            0,
            0],
        'SHIRT': [
            femaleShirt,
            femaleShirtDye,
            femaleShirtColor],
        'VEST': [
            femaleVest,
            femaleVestDye,
            femaleVestColor],
        'COAT': [
            0,
            0,
            0],
        'BELT': [
            femaleBelt,
            femaleBeltDye,
            femaleBeltColor],
        'PANT': [
            femalePant,
            femalePantDye,
            femalePantColor],
        'SHOE': [
            femaleShoe,
            femaleShoeDye,
            0] }
    return defaultFemaleClothing

