import datetime
import tempfile
from decimal import Decimal
import time as timer
import numpy as np


class players:  # main container class, used for saving stats on all entities
    def __init__(self, name, isPlayer, time):
        self.isPlayer = isPlayer
        self.combatOver = False
        self.name = name
        self.dmgoutindex = {"name": 0, "target": 1, "damage": 2, "DPS": 3, "maxHit": 4, "crits": 5, "flanks": 6,
                            "attacks": 7, "misses": 8, "CrtH": 9, "acc": 10, "flankrate": 11, "kills": 12,
                            "hulldamage": 13, "shielddamage": 14, "resist": 15, "hullAttacks": 16, "finalResist": 17}
        self.healOutIndex = {"name": 0, "target": 1, "healtotal": 2, "HPS": 3, "hullheal": 4, "shieldheal": 5,
                             "maxHeal": 6, "Crits": 7, "healticks": 8, "CrtH": 9}

        self.dmgoutTable = []
        self.dmgoutDict = {}
        self.petDMGTable = []
        self.petSourceDict = {}
        self.petSourceidDict = {}
        self.petWeaponDict = {}
        self.petTargetDict = {}
        self.healsInDict = {}
        self.healsOutDict = {}
        self.petHealsourceDict = {}
        self.petHealsIDDict = {}
        self.petAbilityDict = {}
        self.petHealTargetDict = {}
        self.dmginTable = []  # to be added
        self.dmgInDict = {}  # to be added
        self.healsOutTable = []  # to be added
        self.healsInTable = []  # to be added
        self.petHealsTable = []
        self.totaldamage = 0
        self.totalAttacks = 0
        self.hulllDamage = 0
        self.shieldDamage = 0
        self.totalHealInstances = 0
        self.totalCrits = 0
        self.totalHealCrits = 0
        self.totalHeals = 0
        self.totalDamageTaken = 0
        self.totalAttacksTaken = 0
        self.deaths = 0
        self.maxOneHit = 0
        self.maxOneHitWeapon = ""
        self.maxOneHeal = 0
        self.maxOneHealWeapon = ""
        self.DPS = 0
        self.crtH = 0
        self.healCrtH = 0
        self.startTime = time
        self.totalTime = 0
        self.flanks = 0
        self.misses = 0
        self.kills = 0
        self.runtime = 0
        self.endTime = 0
        self.acc = 0
        self.resist = 0
        self.hullAttacks = 0
        self.finalresist = 0
        self.ATKSinPercentage = 0
        self.dmgPercentage = 0
        self.percentageTaken = 0
        self.percentageHealed = 0
        self.ATKSpMin = 0
        self.HPS = 0
        self.globalFinishTime = None
        self.globalStartTime = None
        self.globalRunTime = None
        self.timeKilled = None
        self.killedByLast = None


    def updateStats(self, time2, midParseUpdate=True):
        self.temptotalAttacks = self.totalAttacks - self.misses
        self.totalTime = (time2 - self.startTime).total_seconds()
        self.runtime = self.totalTime
        self.endTime = time2
        if self.totalTime > 0 and self.totalHeals > 0:
            self.HPS = self.totalHeals / self.totalTime
        if not self.hullAttacks == 0:
            self.finalresist = self.resist / self.hullAttacks
        if not self.totalTime == 0:
            self.DPS = self.totaldamage / self.totalTime
        if self.temptotalAttacks >= 1 and self.totalAttacks >= 1 and self.totalCrits >= 1 and self.flanks >= 1:
            self.crtH = self.totalCrits / self.temptotalAttacks * 100
            self.flankRate = self.flanks / self.temptotalAttacks * 100
            self.acc = self.temptotalAttacks / self.totalAttacks * 100
        elif self.temptotalAttacks >= 1 and self.totalAttacks >= 1 and self.totalCrits >= 1:
            self.acc = self.temptotalAttacks / self.totalAttacks * 100
            self.crtH = self.totalCrits / self.temptotalAttacks * 100
            self.flankRate = 0
        elif self.totalCrits == 0:
            self.crtH = 0
        elif self.flanks == 0:
            self.flankRate = 0
        if self.totalHealInstances > 0:
            self.healCrtH = self.totalHealCrits / self.totalHealInstances * 100

    def updateTables(self):
        self.updateStats(self.endTime, False)
        self.updateDMGOutTable()
        self.updatePetsDMGOutTable()
        self.updateDMGInTable()
        self.updateHealsTable()
        self.updatePetHealsTable()
        self.updateHealingInTable()

    def updateDMGOutTable(self):
        self.combatTime = self.runtime
        if self.combatTime < 1:
            self.combatTime = 1
            self.runtime = 1
        for rows in self.dmgoutTable:
            for col in rows:
                self.tmpDamage = col[self.dmgoutindex["damage"]]
                self.tmpCrits = col[self.dmgoutindex["crits"]]
                self.tmpAttacks = col[self.dmgoutindex["attacks"]]
                self.tmpMisses = col[self.dmgoutindex["misses"]]
                self.tmpFlanks = col[self.dmgoutindex["flanks"]]
                if col[self.dmgoutindex["hullAttacks"]] == 0:
                    pass
                else:
                    col[self.dmgoutindex["finalResist"]] = col[self.dmgoutindex["resist"]] / col[
                        self.dmgoutindex["hullAttacks"]]

                col[self.dmgoutindex["DPS"]] = self.tmpDamage / self.combatTime
                self.temporalAttacks = self.tmpAttacks - self.tmpMisses
                if self.temporalAttacks >= 1 and self.tmpAttacks >= 1 and self.tmpCrits >= 1 and self.tmpFlanks >= 1:
                    col[self.dmgoutindex["CrtH"]] = self.tmpCrits / self.temporalAttacks * 100
                    col[self.dmgoutindex["flankrate"]] = self.tmpFlanks / self.temporalAttacks * 100
                    col[self.dmgoutindex["acc"]] = self.temporalAttacks / self.tmpAttacks * 100
                elif self.temporalAttacks >= 1 and self.tmpAttacks >= 1 and self.tmpCrits >= 1:
                    col[self.dmgoutindex["CrtH"]] = self.tmpCrits / self.temporalAttacks * 100
                    col[self.dmgoutindex["acc"]] = self.temporalAttacks / self.tmpAttacks * 100
                    col[self.dmgoutindex["flankrate"]] = 0
                elif self.temporalAttacks >= 1 and self.tmpAttacks >= 1:
                    col[self.dmgoutindex["CrtH"]] = 0
                    col[self.dmgoutindex["acc"]] = self.temporalAttacks / self.tmpAttacks * 100
                    col[self.dmgoutindex["flankrate"]] = 0

    def updatePetsDMGOutTable(self):
        self.combatTime = self.runtime
        if self.combatTime < 1:
            self.combatTime = 1
        for rows in self.petDMGTable:
            for col in rows:
                if col == rows[0]:
                    # update pet type stats
                    self.tmpDamage = col[self.dmgoutindex["damage"]]
                    self.tmpCrits = col[self.dmgoutindex["crits"]]
                    self.tmpAttacks = col[self.dmgoutindex["attacks"]]
                    self.tmpMisses = col[self.dmgoutindex["misses"]]
                    self.tmpFlanks = col[self.dmgoutindex["flanks"]]
                    col[self.dmgoutindex["DPS"]] = self.tmpDamage / self.combatTime
                    self.temporalAttacks = self.tmpAttacks - self.tmpMisses
                    col[self.dmgoutindex["finalResist"]] = col[self.dmgoutindex["resist"]] / col[
                        self.dmgoutindex["hullAttacks"]]
                    if self.temporalAttacks >= 1 and self.tmpAttacks >= 1 and self.tmpCrits >= 1 and self.tmpFlanks >= 1:
                        col[self.dmgoutindex["CrtH"]] = self.tmpCrits / self.temporalAttacks * 100
                        col[self.dmgoutindex["flankrate"]] = self.tmpFlanks / self.temporalAttacks * 100
                        col[self.dmgoutindex["acc"]] = self.temporalAttacks / self.tmpAttacks * 100
                    elif self.temporalAttacks >= 1 and self.tmpAttacks >= 1 and self.tmpCrits >= 1:
                        col[self.dmgoutindex["CrtH"]] = self.tmpCrits / self.temporalAttacks * 100
                        col[self.dmgoutindex["acc"]] = self.temporalAttacks / self.tmpAttacks * 100
                        col[self.dmgoutindex["flankrate"]] = 0
                    elif self.temporalAttacks >= 1 and self.tmpAttacks >= 1:
                        col[self.dmgoutindex["CrtH"]] = 0
                        col[self.dmgoutindex["acc"]] = self.temporalAttacks / self.tmpAttacks * 100
                        col[self.dmgoutindex["flankrate"]] = 0
                else:
                    for cols2 in col:
                        if cols2 == col[0]:
                            # update pet instance stats
                            self.tmpDamage = cols2[self.dmgoutindex["damage"]]
                            self.tmpCrits = cols2[self.dmgoutindex["crits"]]
                            self.tmpAttacks = cols2[self.dmgoutindex["attacks"]]
                            self.tmpMisses = cols2[self.dmgoutindex["misses"]]
                            self.tmpFlanks = cols2[self.dmgoutindex["flanks"]]
                            cols2[self.dmgoutindex["finalResist"]] = cols2[self.dmgoutindex["resist"]] / cols2[
                                self.dmgoutindex["hullAttacks"]]
                            cols2[self.dmgoutindex["DPS"]] = self.tmpDamage / self.combatTime
                            self.temporalAttacks = self.tmpAttacks - self.tmpMisses
                            if self.temporalAttacks >= 1 and self.tmpAttacks >= 1 and self.tmpCrits >= 1 and self.tmpFlanks >= 1:
                                cols2[self.dmgoutindex["CrtH"]] = self.tmpCrits / self.temporalAttacks * 100
                                cols2[self.dmgoutindex["flankrate"]] = self.tmpFlanks / self.temporalAttacks * 100
                                cols2[self.dmgoutindex["acc"]] = self.temporalAttacks / self.tmpAttacks * 100
                            elif self.temporalAttacks >= 1 and self.tmpAttacks >= 1 and self.tmpCrits >= 1:
                                cols2[self.dmgoutindex["CrtH"]] = self.tmpCrits / self.temporalAttacks * 100
                                cols2[self.dmgoutindex["acc"]] = self.temporalAttacks / self.tmpAttacks * 100
                                cols2[self.dmgoutindex["flankrate"]] = 0
                            elif self.temporalAttacks >= 1 and self.tmpAttacks >= 1:
                                cols2[self.dmgoutindex["CrtH"]] = 0
                                cols2[self.dmgoutindex["acc"]] = self.temporalAttacks / self.tmpAttacks * 100
                                cols2[self.dmgoutindex["flankrate"]] = 0
                        else:
                            for cols3 in cols2:
                                # update pet weapon and target stats
                                self.tmpDamage = cols3[self.dmgoutindex["damage"]]
                                self.tmpCrits = cols3[self.dmgoutindex["crits"]]
                                self.tmpAttacks = cols3[self.dmgoutindex["attacks"]]
                                self.tmpMisses = cols3[self.dmgoutindex["misses"]]
                                self.tmpFlanks = cols3[self.dmgoutindex["flanks"]]
                                cols3[self.dmgoutindex["DPS"]] = self.tmpDamage / self.combatTime
                                self.temporalAttacks = self.tmpAttacks - self.tmpMisses
                                cols3[self.dmgoutindex["finalResist"]] = cols3[self.dmgoutindex["resist"]] / cols3[
                                    self.dmgoutindex["hullAttacks"]]
                                if self.temporalAttacks >= 1 and self.tmpAttacks >= 1 and self.tmpCrits >= 1 and self.tmpFlanks >= 1:
                                    cols3[self.dmgoutindex["CrtH"]] = self.tmpCrits / self.temporalAttacks * 100
                                    cols3[self.dmgoutindex["flankrate"]] = self.tmpFlanks / self.temporalAttacks * 100
                                    cols3[self.dmgoutindex["acc"]] = self.temporalAttacks / self.tmpAttacks * 100
                                elif self.temporalAttacks >= 1 and self.tmpAttacks >= 1 and self.tmpCrits >= 1:
                                    cols3[self.dmgoutindex["CrtH"]] = self.tmpCrits / self.temporalAttacks * 100
                                    cols3[self.dmgoutindex["acc"]] = self.temporalAttacks / self.tmpAttacks * 100
                                    cols3[self.dmgoutindex["flankrate"]] = 0
                                elif self.temporalAttacks >= 1 and self.tmpAttacks >= 1:
                                    cols3[self.dmgoutindex["CrtH"]] = 0
                                    cols3[self.dmgoutindex["acc"]] = self.temporalAttacks / self.tmpAttacks * 100
                                    cols3[self.dmgoutindex["flankrate"]] = 0

    def updateDMGInTable(self):
        self.combatTime = self.runtime
        for rows in self.dmginTable:
            for col in rows:
                self.tmpDamage = col[self.dmgoutindex["damage"]]
                self.tmpCrits = col[self.dmgoutindex["crits"]]
                self.tmpAttacks = col[self.dmgoutindex["attacks"]]
                self.tmpMisses = col[self.dmgoutindex["misses"]]
                self.tmpFlanks = col[self.dmgoutindex["flanks"]]
                col[self.dmgoutindex["DPS"]] = self.tmpDamage / self.combatTime
                self.temporalAttacks = self.tmpAttacks - self.tmpMisses
                col[self.dmgoutindex["finalResist"]] = col[self.dmgoutindex["resist"]] / col[
                    self.dmgoutindex["hullAttacks"]]
                if self.temporalAttacks >= 1 and self.tmpAttacks >= 1 and self.tmpCrits >= 1 and self.tmpFlanks >= 1:
                    col[self.dmgoutindex["CrtH"]] = self.tmpCrits / self.temporalAttacks * 100
                    col[self.dmgoutindex["flankrate"]] = self.tmpFlanks / self.temporalAttacks * 100
                    col[self.dmgoutindex["acc"]] = self.temporalAttacks / self.tmpAttacks * 100
                elif self.temporalAttacks >= 1 and self.tmpAttacks >= 1 and self.tmpCrits >= 1:
                    col[self.dmgoutindex["CrtH"]] = self.tmpCrits / self.temporalAttacks * 100
                    col[self.dmgoutindex["acc"]] = self.temporalAttacks / self.tmpAttacks * 100
                    col[self.dmgoutindex["flankrate"]] = 0
                elif self.temporalAttacks >= 1 and self.tmpAttacks >= 1:
                    col[self.dmgoutindex["CrtH"]] = 0
                    col[self.dmgoutindex["acc"]] = self.temporalAttacks / self.tmpAttacks * 100
                    col[self.dmgoutindex["flankrate"]] = 0

    def updateHealsTable(self):
        self.combatTime = self.runtime
        if self.combatTime < 1:
            self.combatTime = 1
        for rows in self.healsOutTable:
            for col in rows:
                self.tmpHealsOut = col[self.healOutIndex["healtotal"]]
                self.tmpCrits = col[self.healOutIndex["Crits"]]
                self.tmpTicks = col[self.healOutIndex["healticks"]]
                col[self.healOutIndex["HPS"]] = self.tmpHealsOut / self.combatTime
                if self.tmpCrits > 0:
                    col[self.healOutIndex["CrtH"]] = self.tmpCrits / self.tmpTicks

    def updatePetHealsTable(self):
        self.combatTime = self.runtime
        if self.combatTime < 1:
            self.combatTime = 1
        for rows in self.petHealsTable:
            for col in rows:
                if col == rows[0]:
                    self.tmpHealsOut = col[self.healOutIndex["healtotal"]]
                    self.tmpCrits = col[self.healOutIndex["Crits"]]
                    self.tmpTicks = col[self.healOutIndex["healticks"]]
                    col[self.healOutIndex["HPS"]] = self.tmpHealsOut / self.combatTime
                    if self.tmpCrits > 0:
                        col[self.healOutIndex["CrtH"]] = self.tmpCrits / self.tmpTicks
                else:
                    for cols2 in col:
                        if cols2 == col[0]:
                            # update pet instance stats
                            self.tmpHealsOut = cols2[self.healOutIndex["healtotal"]]
                            self.tmpCrits = cols2[self.healOutIndex["Crits"]]
                            self.tmpTicks = cols2[self.healOutIndex["healticks"]]
                            cols2[self.healOutIndex["HPS"]] = self.tmpHealsOut / self.combatTime
                            if self.tmpCrits > 0:
                                cols2[self.healOutIndex["CrtH"]] = self.tmpCrits / self.tmpTicks
                        else:
                            for cols3 in cols2:
                                # update pet weapon and target stats
                                self.tmpHealsOut = cols3[self.healOutIndex["healtotal"]]
                                self.tmpCrits = cols3[self.healOutIndex["Crits"]]
                                self.tmpTicks = cols3[self.healOutIndex["healticks"]]
                                cols3[self.healOutIndex["HPS"]] = self.tmpHealsOut / self.combatTime
                                if self.tmpCrits > 0:
                                    cols3[self.healOutIndex["CrtH"]] = self.tmpCrits / self.tmpTicks

    def updateHealingInTable(self):
        self.combatTime = self.runtime
        if self.combatTime < 1:
            self.combatTime = 1
        for rows in self.healsInTable:
            for col in rows:
                self.tmpHealsOut = col[self.healOutIndex["healtotal"]]
                self.tmpCrits = col[self.healOutIndex["Crits"]]
                self.tmpTicks = col[self.healOutIndex["healticks"]]
                col[self.healOutIndex["HPS"]] = self.tmpHealsOut / self.combatTime
                if self.tmpCrits > 0:
                    col[self.healOutIndex["CrtH"]] = self.tmpCrits / self.tmpTicks

    def rounder(self, entry):
        if isinstance(entry, int):
            return f'{entry:,}'
        elif isinstance(entry, float):
            a = Decimal(entry).quantize(Decimal('1.00'))
            return f'{a:,}'
        else:
            return str(entry)

    def setCombatTime(self, combatTimeRule):
        if self.endTime == 0:
            self.endTime = self.globalFinishTime
        if combatTimeRule == "personal":
            self.runtime = (self.endTime - self.startTime).total_seconds()
        elif combatTimeRule == "personalStartGlobalEnd":
            self.runtime = (self.globalFinishTime - self.startTime).total_seconds()
        elif combatTimeRule == "Global":
            self.runtime = self.globalRunTime
        elif combatTimeRule == "globalStartPersonalEnd":
            self.runtime = (self.endTime - self.globalStartTime)


class parser:
    def __init__(self):
        self.path = ""
        self.combatlog = []
        self.playerdict = {}
        self.playerList = []
        self.preventIterative = True
        self.NPCs = []
        self.tableArray = []
        self.otherCombats = {}
        self.deltaValue = 200
        self.graphDelta = datetime.timedelta(milliseconds=self.deltaValue)
        self.lastGraphTime = None
        self.splicedCombatlog = []
        self.uiDictionary = {}
        self.tempInstance = players("temp", False, None)
        self.dmgTableIndex = self.tempInstance.dmgoutindex
        self.healTableIndex = self.tempInstance.healOutIndex
        self.uiInputDictionary = {"isPlayer": 0, "damageOut": 1, "petDamageOut": 2, "damageIn": 3, "healsOut": 4,
                                  "petHealsOut": 5, "healsIn": 6}
        self.excludeAttacks = ["Shield Scraping II", "Tachyon Charges"]
        self.excludeDamage = ["Warp Core Breach"]
        self.exculdedHealTicks = []
        self.combatlogDict = {"date": 0, "character": 1, "ID": 2, "pet": 3, "petID": 4, "target": 5, "targetID": 6,
                              "source": 7, "sourceID": 8, "dmageType": 9, "flags": 10, "mag1": 11,
                              "mag2": 12}
        self.counter2 = 0
        self.map = None
        self.difficulty = None
        self.warpCoreBreach = None
        self.damageChart = {}
        self.NPCDamageChart = {}
        self.DPSChart = {}
        self.NPCDPSChart = {}
        self.bufferedDamage = {}
        self.globalCombatTime = None
        self.globalCombatStart = None
        self.globalCombatEnd = None

        self.difficultyToAbreviation = {"Elite": "E", "Advanced": "A", "Normal": "N"}
        self.AbreviationToDifficulty = {"N": "Normal", "Advanced": "A", "E": "Elite"}

        self.queueToAbreviation = {"Infected_Space": "IS",
                                   "Azure_Nebula": "AN",
                                   "Battle_At_The_Binary_Stars": "BBS",
                                   "Battle_At_Procyon_V": "BPV",
                                   "Borg_Disconnected": "BD",
                                   "Counterpoint": "CP",
                                   "Crystalline_Entity": "CC",
                                   "Gateway_To_Grethor": "GG",
                                   "Herald_Sphere": "HSP",
                                   "Operation_Riposte": "OR",
                                   "Cure_Found": "CS",
                                   "Days_Of_Doom": "DOD",
                                   "Dranuur Gauntlet": "DG",
                                   "Khitomer_Space": "KS",
                                   "Storming_The_Spire": "STS",
                                   "Swarm": "SW",
                                   "To_Hell_With_Honor": "THWH",
                                   "Gravity_Kills": "GK",
                                   "Hive_Space": "HS",
                                   "Best_Served_Cold": "BSC",
                                   "Operation_Wolf": "OF"
                                   }

        self.AbreviationToQueue = {}

        self.mapIdentifiers = {"Space_Borg_Battleship_Raidisode_Sibrian_Elite_Initial": "Infected_Space_Elite",
                               "Space_Borg_Dreadnought_Raidisode_Sibrian_Final_Boss": "Infected_Space",
                               "Mission_Space_Romulan_Colony_Flagship_Lleiset": "Azure_Nebula",
                               "Space_Klingon_Dreadnought_Dsc_Sarcophagus": "Battle_At_The_Binary_Stars",
                               "Event_Procyon_5_Queue_Krenim_Dreadnaught_Annorax": "Battle_At_Procyon_V",
                               "Mission_Space_Borg_Queen_Diamond_Brg_Queue_Liberation": "Borg_Disconnected",
                               "Mission_Starbase_Mirror_Ds9_Mu_Queue": "Counterpoint",
                               "Space_Crystalline_Entity_2018": "Crystalline_Entity",
                               "Event_Ico_Qonos_Space_Herald_Dreadnaught": "Gateway_To_Grethor",
                               "Mission_Space_Federation_Science_Herald_Sphere": "Herald_Sphere",
                               "Msn_Dsc_Priors_System_Tfo_Orbital_Platform_1_Fed_Dsc": "Operation_Riposte",
                               "Space_Borg_Dreadnought_R02": "Cure_Found",
                               "Space_Klingon_Tos_X3_Battlecruiser": "Days_Of_Doom",
                               "Msn_Luk_Colony_Dranuur_Queue_System_Upgradeable_Satellite": "Dranuur_Gauntlet",
                               "Space_Borg_Dreadnought_Raidisode_Khitomer_Intro_Boss": "Khitomer_Space",
                               "Mission_Spire_Space_Voth_Frigate": "Storming_The_Spire",
                               "Space_Drantzuli_Alpha_Battleship": "Swarm",
                               "Mission_Beta_Lankal_Destructible_Reactor": "To_Hell_With_Honor",
                               "Space_Federation_Dreadnought_Jupiter_Class_Carrier": "Gravity_Kills",
                               "Msn_Luk_Hypermass_Queue_System_Tzk_Protomatter_Facility": "Gravity_Kills",
                               "Space_Borg_Dreadnought_Hive_Intro": "Hive_Space",
                               "Mission_Space_Borg_Battleship_Queen_1_0f_2": "Hive_Space",
                               "Msn_Kcw_Rura_Penthe_System_Tfo_Dilithium_Hauler": "Best_Served_Cold",
                               "Ground_Federation_Capt_Mirror_Runabout_Tfo": "Operation_Wolf"
                               }

        self.checkSpaceMaps = ["Infected_Space", "Azure_Nebula", "Battle_At_The_Binary_Stars", "Borg_Disconnected",
                               "Counterpoint", "Crystalline_Entity",
                               "Gateway_To_Grethor", "Herald_Sphere", "Operation_Riposte", "Cure_Found", "Days_Of_Doom",
                               "Dranuur_Gauntlet", "Khitomer_space",
                               "Storming_The_Spire", "Swarm", "To_Hell_With_Honor", "Gravity_Kills", "Hive_Space",
                               "Best_Served_Cold"]

        self.isSpace = True

        self.difficultyDetectionDict = {}

        self.endTable = []

        self.combatTimeRule = "personal"
        self.WCBrule = "Global" #Global, Personal, Killer
        self.depthAnalysis = True

    def resetParser(self):
        self.warpCoreBreach = None
        self.combatlog = []
        self.playerdict = {}
        self.playerList = []
        self.NPCs = []
        self.tableArray = []
        self.otherCombats = {}
        self.splicedCombatlog = []
        self.uiDictionary = {}
        self.counter2 = 0
        self.map = None
        self.difficulty = None
        self.endTable = []
        self.damageChart = {}
        self.NPCDamageChart = {}
        self.DPSChart = {}
        self.NPCDPSChart = {}
        self.bufferedDamage = {}
        self.globalCombatTime = None
        self.globalCombatStart = None
        self.globalCombatEnd = None
        self.depthAnalysis = False

    def softResetParser(self):
        self.warpCoreBreach = None
        self.combatlog = []
        self.playerdict = {}
        self.playerList = []
        self.NPCs = []
        self.splicedCombatlog = []
        self.uiDictionary = {}
        self.counter2 = 0
        self.tableArray = []
        self.map = None
        self.difficulty = None
        self.endTable = []
        self.damageChart = {}
        self.NPCDamageChart = {}
        self.DPSChart = {}
        self.NPCDPSChart = {}
        self.bufferedDamage = {}
        self.globalCombatTime = None
        self.globalCombatStart = None
        self.globalCombatEnd = None
        self.depthAnalysis = False

    def setPath(self, path):
        self.path = path

    def createTableInstanceAlternate(self, isPlayer):
        self.tableArray.append(players(self.targetID, isPlayer, self.timeToTimeAndDate(self.date)))
        self.playerdict.update({self.targetID: self.counter2})
        self.counter2 += 1

    def createTableInstance(self):  # creates a new class instance and appends to list
        if self.isPlayer:
            self.tableArray.append(players(self.ID, True, self.timeToTimeAndDate(self.date)))
            self.playerdict.update({self.ID: self.counter2})
            self.counter2 += 1
        else:
            self.tableArray.append(players(self.ID, False, self.timeToTimeAndDate(self.date)))
            self.playerdict.update({self.ID: self.counter2})
            self.counter2 += 1

    def getGlobalTime(self):
        self.globalCombatTime = (self.globalCombatEnd - self.globalCombatStart).total_seconds()

    def timeToTimeAndDate(self, timeSplice):  # turns combatlog time string into TimeDate object
        timeSplice = timeSplice.split(":")
        seconds = timeSplice.pop()
        seconds = seconds.split(".")
        timeSplice.append(seconds[0])
        timeSplice.append(seconds[1])
        timeSplice[0] = int(timeSplice[0]) + 2000

        time = datetime.datetime(timeSplice[0], int(timeSplice[1]), int(timeSplice[2]), int(timeSplice[3]),
                                 int(timeSplice[4]), int(timeSplice[5]), int(timeSplice[6]) * 100000)

        return time

    def generateHandle(self,IDSplyce):  # returns player handle, can further splice this for only @xxxx or character name.
        IDSplyce = IDSplyce.split(" ", 1)
        IDSplyce = IDSplyce[1]
        IDSplyce = IDSplyce[:-1]
        return IDSplyce

    def generateID(self,IDSplyce):  # returns player ID (not necessary if necessary, might be removed down the road if unnecessary
        OGSplyce = IDSplyce
        IDSplyce = IDSplyce.split(" ")
        IDSplyce = IDSplyce[0]
        IDSplyce = IDSplyce.split("[")
        if IDSplyce[0] == "C":
            name = "unkownNPC"
            for y in self.NPCs:
                if y[1] == OGSplyce:
                    name = y[0]
            returner = name + " " + IDSplyce[1]
            return returner
        else:
            return IDSplyce[1]

    def rounder(self, entry):
        if isinstance(entry, int):
            return f'{entry:,}'
        elif isinstance(entry, float):
            a = Decimal(entry).quantize(Decimal('1.00'))
            return f'{a:,}'
        else:
            return str(entry)

    def removeUnderscore(self, stringer):
        string = stringer
        string = string.replace("_", " ")
        return string

    def arrayExtend(self, arr1, arr2):
        for i in arr2:
            arr1.append(i)
        return arr1


    def getFlags(self, flagUpdater):  # returns flags combat lines
        crit = False
        miss = False
        flank = False
        kill = False
        if not flagUpdater == "*":
            flagUpdater = flagUpdater.split("|")
            for flag in flagUpdater:
                if flag == "Miss":
                    miss = True
                if flag == "Critical":
                    crit = True
                if flag == "Flank":
                    flank = True
                if flag == "Kill":
                    kill = True
        return crit, miss, flank, kill

    def quickScan(self):
        if self.targetID == "*" or not self.targetID in self.playerdict:
            self.damaged = players("name", False, None)

        if (self.damagetype == "Shield" and self.damage1 < 0 and self.damage2 >= 0) or self.damagetype == "HitPoints":
            self.attacker.totalHeals += self.damage1
            if self.damage1 > self.attacker.maxOneHeal:
                self.attacker.maxOneHeal = self.damage1
        else:
            if self.damage1 < 0:
                self.damage1 *= -1
            self.damaged.totalDamageTaken += self.damage1
            self.damaged.totalAttacksTaken += 1
            self.attacker.totalAttacks += 1
            self.attacker.totaldamage += self.damage1
            if self.damage1 > self.attacker.maxOneHit:
                self.attacker.maxOneHit = self.damage1
            if not self.damagetype == "Shield" and not self.isMiss:
                if self.damage2 == 0:
                    pass
                else:
                    self.resist = 0
                    self.resist = self.damage1 / self.damage2 * 100
                    if not self.resist == 0:
                        self.attacker.resist += self.resist
                        self.attacker.hullAttacks += 1

    def generateHealStatLine(self):
        return [self.source, self.target, self.damage1, 0, self.hullHeal, self.shieldHeal, self.damage1, (1 if self.isCrit else 0), 1, 0]

    def generateHealStatLineOpen(self):
        return [self.damage1, 0, self.hullHeal, self.shieldHeal, self.damage1, (1 if self.isCrit else 0), 1, 0]


    def generateHealsOutTable(self):
        self.dmgOutSource = self.ID
        if self.dmgOutSource in self.damaged.healsInTable:
            newTargeted = True
            for col in self.damaged.healsInTable[self.damaged.healsInDict[self.dmgOutSource]]:
                if col[self.damaged.healOutIndex["target"]] == self.source:
                    newTargeted = False
                    self.damaged.healsInTable[self.damaged.healsInDict[self.dmgOutSource]][0][
                        self.attacker.healOutIndex["healtotal"]] += self.damage1
                    self.damaged.healsInTable[self.damaged.healsInDict[self.dmgOutSource]][0][
                        self.attacker.healOutIndex["hullheal"]] += self.hullHeal
                    self.damaged.healsInTable[self.damaged.healsInDict[self.dmgOutSource]][0][
                        self.attacker.healOutIndex["shieldheal"]] += self.shieldHeal
                    if not self.source in self.exculdedHealTicks:
                        self.damaged.healsInTable[self.damaged.healsInDict[self.dmgOutSource]][0][
                            self.attacker.healsInDict["healticks"]] += 1
                        col[self.attacker.healsInDict["healticks"]] += 1
                    col[self.attacker.healOutIndex["healtotal"]] += self.damage1
                    col[self.attacker.healOutIndex["hullheal"]] += self.hullHeal
                    col[self.attacker.healOutIndex["shieldheal"]] += self.shieldHeal

                    if self.damage1 > self.damaged.healsInTable[self.damaged.healsInDict[self.dmgOutSource]][0][
                        self.attacker.healOutIndex["maxHeal"]]:
                        self.damaged.healsInTable[self.damaged.healsInDict[self.dmgOutSource]][0][
                            self.attacker.healOutIndex["maxHeal"]] = self.damage1
                    if self.damage1 > col[self.attacker.healOutIndex["maxHeal"]]:
                        col[self.attacker.healOutIndex["maxHeal"]] = self.damage1
                    if self.isCrit:
                        self.damaged.healsInTable[self.damaged.healsInDict[self.dmgOutSource]][0][
                            self.attacker.healOutIndex["Crits"]] += 1
                        col[self.attacker.healOutIndex["Crits"]] += 1
            if newTargeted:
                self.damaged.healsInTable[self.damaged.healsInDict[self.dmgOutSource]].append(
                    self.arrayExtend([self.source, self.target], self.generateHealStatLineOpen()))
                self.damaged.healsInTable[self.damaged.healsInDict[self.dmgOutSource]][0][
                    self.attacker.healOutIndex["healtotal"]] += self.damage1
                self.damaged.healsInTable[self.damaged.healsInDict[self.dmgOutSource]][0][
                    self.attacker.healOutIndex["hullheal"]] += self.hullHeal
                self.damaged.healsInTable[self.damaged.healsInDict[self.dmgOutSource]][0][
                    self.attacker.healOutIndex["shieldheal"]] += self.shieldHeal
                if not self.source in self.exculdedHealTicks:
                    self.damaged.healsInTable[self.damaged.healsInDict[self.dmgOutSource]][0][
                        self.attacker.healOutIndex["healticks"]] += 1
                if self.damage1 > self.damaged.healsInTable[self.damaged.healsInDict[self.dmgOutSource]][0][
                    self.attacker.healOutIndex["maxHeal"]]:
                    self.damaged.healsInTable[self.damaged.healsInDict[self.dmgOutSource]][0][
                        self.attacker.healOutIndex["maxHeal"]] = self.damage1
                if self.isCrit:
                    self.damaged.healsInTable[self.damaged.healsInDict[self.dmgOutSource]][0][
                        self.attacker.healOutIndex["Crits"]] += 1
        else:
            self.damaged.healsInTable.append([
                self.arrayExtend([self.source, "global"], self.generateHealStatLineOpen()),
                self.arrayExtend([self.source, self.target], self.generateHealStatLineOpen())])
            self.damaged.dmgInDict.update({self.dmgOutSource: len(self.attacker.dmgoutTable) - 1})

    def generateHealsInTable(self):
        if self.source in self.attacker.healsOutDict:
            newTarget = True
            for col in self.attacker.healsOutTable[self.attacker.healsOutDict[self.source]]:
                if col[self.attacker.healOutIndex["target"]] == self.target:
                    newTarget = False
                    self.attacker.healsOutTable[self.attacker.healsOutDict[self.source]][0][
                        self.attacker.healOutIndex["healtotal"]] += self.damage1
                    self.attacker.healsOutTable[self.attacker.healsOutDict[self.source]][0][
                        self.attacker.healOutIndex["hullheal"]] += self.hullHeal
                    self.attacker.healsOutTable[self.attacker.healsOutDict[self.source]][0][
                        self.attacker.healOutIndex["shieldheal"]] += self.shieldHeal
                    if not self.source in self.exculdedHealTicks:
                        self.attacker.healsOutTable[self.attacker.healsOutDict[self.source]][0][
                            self.attacker.healOutIndex["healticks"]] += 1
                        col[self.attacker.healOutIndex["healticks"]] += 1
                    col[self.attacker.healOutIndex["healtotal"]] += self.damage1
                    col[self.attacker.healOutIndex["hullheal"]] += self.hullHeal
                    col[self.attacker.healOutIndex["shieldheal"]] += self.shieldHeal
                    if self.damage1 > self.attacker.healsOutTable[self.attacker.healsOutDict[self.source]][0][
                        self.attacker.healOutIndex["maxHeal"]]:
                        self.attacker.healsOutTable[self.attacker.healsOutDict[self.source]][0][
                            self.attacker.healOutIndex["maxHeal"]] = self.damage1
                    if self.damage1 > col[self.attacker.healOutIndex["maxHeal"]]:
                        col[self.attacker.healOutIndex["maxHeal"]] = self.damage1
                    if self.isCrit:
                        self.attacker.healsOutTable[self.attacker.healsOutDict[self.source]][0][
                            self.attacker.healOutIndex["Crits"]] += 1
                        col[self.attacker.healOutIndex["Crits"]] += 1
            if newTarget:
                self.attacker.healsOutTable[self.attacker.healsOutDict[self.source]].append(
                    self.arrayExtend([self.source, self.target], self.generateHealStatLineOpen()))
                self.attacker.healsOutTable[self.attacker.healsOutDict[self.source]][0][
                    self.attacker.healOutIndex["healtotal"]] += self.damage1
                self.attacker.healsOutTable[self.attacker.healsOutDict[self.source]][0][
                    self.attacker.healOutIndex["hullheal"]] += self.hullHeal
                self.attacker.healsOutTable[self.attacker.healsOutDict[self.source]][0][
                    self.attacker.healOutIndex["shieldheal"]] += self.shieldHeal
                if not self.source in self.exculdedHealTicks:
                    self.attacker.healsOutTable[self.attacker.healsOutDict[self.source]][0][
                        self.attacker.healOutIndex["healticks"]] += 1
                if self.damage1 > self.attacker.healsOutTable[self.attacker.healsOutDict[self.source]][0][
                    self.attacker.healOutIndex["maxHeal"]]:
                    self.attacker.healsOutTable[self.attacker.healsOutDict[self.source]][0][
                        self.attacker.healOutIndex["maxHeal"]] = self.damage1
                if self.isCrit:
                    self.attacker.healsOutTable[self.attacker.healsOutDict[self.source]][0][
                        self.attacker.healOutIndex["Crits"]] += 1
        else:
            self.attacker.healsOutTable.append([
                self.arrayExtend([self.source, "global"], self.generateHealStatLineOpen()),
                self.arrayExtend([self.source, self.target], self.generateHealStatLineOpen())])
            self.attacker.healsOutDict.update({self.source: len(self.attacker.healsOutTable) - 1})

    def petHeals(self):
        if self.source in self.attacker.petHealsourceDict:
            self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][0][
                self.attacker.healOutIndex["healtotal"]] += self.damage1
            self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][0][
                self.attacker.healOutIndex["hullheal"]] += self.hullHeal
            self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][0][
                self.attacker.healOutIndex["shieldheal"]] += self.shieldHeal
            if not self.ability in self.exculdedHealTicks:
                self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][0][
                    self.attacker.healOutIndex["healticks"]] += 1
            if self.damage1 > self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][0][
                self.attacker.healOutIndex["maxHeal"]]:
                self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][0][
                    self.attacker.healOutIndex["maxHeal"]] = self.damage1
            if self.isCrit:
                self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][0][
                    self.attacker.healOutIndex["Crits"]] += 1

            if self.sourceID in self.attacker.petHealsIDDict:
                # updateing stats of pet instance
                self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                    self.attacker.petHealsIDDict[self.sourceID]][0][
                    self.attacker.healOutIndex["healtotal"]] += self.damage1
                self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                    self.attacker.petHealsIDDict[self.sourceID]][0][
                    self.attacker.healOutIndex["hullheal"]] += self.hullHeal
                self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                    self.attacker.petHealsIDDict[self.sourceID]][0][
                    self.attacker.healOutIndex["shieldheal"]] += self.shieldHeal
                if not self.ability in self.exculdedHealTicks:
                    self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                        self.attacker.petHealsIDDict[self.sourceID]][0][
                        self.attacker.healOutIndex["healticks"]] += 1
                if self.damage1 > self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                    self.attacker.petHealsIDDict[self.sourceID]][0][
                    self.attacker.healOutIndex["maxHeal"]]:
                    self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                        self.attacker.petHealsIDDict[self.sourceID]][0][
                        self.attacker.healOutIndex["maxHeal"]] = self.damage1
                if self.isCrit:
                    self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                        self.attacker.petHealsIDDict[self.sourceID]][0][
                        self.attacker.healOutIndex["Crits"]] += 1

                    # check if weapon for pet exists
                if self.abilityID in self.attacker.petAbilityDict:
                    # update stats
                    self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                        self.attacker.petHealsIDDict[self.sourceID]][self.attacker.petAbilityDict[self.abilityID]][0][
                        self.attacker.healOutIndex["healtotal"]] += self.damage1
                    self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                        self.attacker.petHealsIDDict[self.sourceID]][self.attacker.petAbilityDict[self.abilityID]][0][
                        self.attacker.healOutIndex["hullheal"]] += self.hullHeal
                    self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                        self.attacker.petHealsIDDict[self.sourceID]][self.attacker.petAbilityDict[self.abilityID]][0][
                        self.attacker.healOutIndex["shieldheal"]] += self.shieldHeal
                    if not self.ability in self.exculdedHealTicks:
                        self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                            self.attacker.petHealsIDDict[self.sourceID]][self.attacker.petAbilityDict[self.abilityID]][0][
                            self.attacker.healOutIndex["healticks"]] += 1
                    if self.damage1 > self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                        self.attacker.petHealsIDDict[self.sourceID]][self.attacker.petAbilityDict[self.abilityID]][0][
                        self.attacker.healOutIndex["maxHeal"]]:
                        self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                            self.attacker.petHealsIDDict[self.sourceID]][self.attacker.petAbilityDict[self.abilityID]][0][
                            self.attacker.healOutIndex["maxHeal"]] = self.damage1
                    if self.isCrit:
                        self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                            self.attacker.petHealsIDDict[self.sourceID]][self.attacker.petAbilityDict[self.abilityID]][0][
                            self.attacker.healOutIndex["Crits"]] += 1

                    if self.targetID in self.attacker.petHealTargetDict:
                        self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                            self.attacker.petHealsIDDict[self.sourceID]][self.attacker.petAbilityDict[self.abilityID]][
                            self.attacker.petHealTargetDict[self.targetID]][
                            self.attacker.healOutIndex["healtotal"]] += self.damage1
                        self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                            self.attacker.petHealsIDDict[self.sourceID]][self.attacker.petAbilityDict[self.abilityID]][
                            self.attacker.petHealTargetDict[self.targetID]][
                            self.attacker.healOutIndex["hullheal"]] += self.hullHeal
                        self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                            self.attacker.petHealsIDDict[self.sourceID]][self.attacker.petAbilityDict[self.abilityID]][
                            self.attacker.petHealTargetDict[self.targetID]][
                            self.attacker.healOutIndex["shieldheal"]] += self.shieldHeal
                        if not self.ability in self.exculdedHealTicks:
                            self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                                self.attacker.petHealsIDDict[self.sourceID]][self.attacker.petAbilityDict[self.abilityID]][
                                self.attacker.petHealTargetDict[self.targetID]][
                                self.attacker.healOutIndex["healticks"]] += 1
                        if self.damage1 > \
                                self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                                    self.attacker.petHealsIDDict[self.sourceID]][
                                    self.attacker.petAbilityDict[self.abilityID]][
                                    self.attacker.petHealTargetDict[self.targetID]][self.attacker.healOutIndex["maxHeal"]]:
                            self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                                self.attacker.petHealsIDDict[self.sourceID]][self.attacker.petAbilityDict[self.abilityID]][
                                self.attacker.petHealTargetDict[self.targetID]][
                                self.attacker.healOutIndex["maxHeal"]] = self.damage1
                        if self.isCrit:
                            self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                                self.attacker.petHealsIDDict[self.sourceID]][self.attacker.petAbilityDict[self.abilityID]][
                                self.attacker.petHealTargetDict[self.targetID]][self.attacker.healOutIndex["Crits"]] += 1

                    else:  # adding a new target that's healed
                        self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                            self.attacker.petHealsIDDict[self.sourceID]][
                            self.attacker.petAbilityDict[self.abilityID]].append(
                            self.arrayExtend([self.target, self.displayTarget], self.generateHealStatLineOpen()))
                        self.attacker.petHealTargetDict.update({self.targetID: len(
                            self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                                self.attacker.petHealsIDDict[self.sourceID]][
                                self.attacker.petAbilityDict[self.abilityID]]) - 1})

                else:
                    # adding new heal ability instance
                    self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                        self.attacker.petHealsIDDict[self.sourceID]].append(
                        [self.arrayExtend([self.ability, self.ability], self.generateHealStatLineOpen()),
                         self.arrayExtend([self.target, self.displayTarget], self.generateHealStatLineOpen())])
                    self.attacker.petAbilityDict.update({self.abilityID: len(
                        self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                            self.attacker.petHealsIDDict[self.sourceID]]) - 1})
                    self.attacker.petHealTargetDict.update({self.targetID: len(
                        self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                            self.attacker.petHealsIDDict[self.sourceID]][self.attacker.petAbilityDict[self.abilityID]]) - 1})


            else:
                # adding a new unique pet to a type of pet
                self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]].append([self.arrayExtend([self.sourceID, self.displaysourceID], self.generateHealStatLineOpen()), [self.arrayExtend([self.ability, self.ability], self.generateHealStatLineOpen()),
                                                                                                             self.arrayExtend([self.target, self.displayTarget], self.generateHealStatLineOpen())]])
                self.attacker.petHealsIDDict.update(
                    {self.sourceID: len(
                        self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]]) - 1})
                self.attacker.petAbilityDict.update({self.abilityID: len(
                    self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                        self.attacker.petHealsIDDict[self.sourceID]]) - 1})
                self.attacker.petHealTargetDict.update({self.targetID: len(
                    self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                        self.attacker.petHealsIDDict[self.sourceID]][self.attacker.petAbilityDict[self.abilityID]]) - 1})

        else:
            # adding a new pet type
            self.attacker.petHealsTable.append(
                [self.arrayExtend([self.source, self.source], self.generateHealStatLineOpen()), [
                     self.arrayExtend([self.sourceID, self.displaysourceID], self.generateHealStatLineOpen()), [
                        self.arrayExtend([self.ability, self.abilityID], self.generateHealStatLineOpen()), self.arrayExtend([self.target, self.displayTarget], self.generateHealStatLineOpen())]]])
            self.attacker.petHealsourceDict.update({self.source: len(self.attacker.petHealsTable) - 1})
            self.attacker.petHealsIDDict.update(
                {self.sourceID: len(
                    self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]]) - 1})
            self.attacker.petAbilityDict.update({self.abilityID: len(
                self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                    self.attacker.petHealsIDDict[self.sourceID]]) - 1})
            self.attacker.petHealTargetDict.update({self.targetID: len(
                self.attacker.petHealsTable[self.attacker.petHealsourceDict[self.source]][
                    self.attacker.petHealsIDDict[self.sourceID]][self.attacker.petAbilityDict[self.abilityID]]) - 1})

    def addHeals(self):
        self.attacker.totalHealInstances += 1
        if self.damage1 < 0:
            self.damage1 *= -1
        self.attacker.totalHeals += self.damage1
        if self.damagetype == "Hitpoints":
            self.shieldHeal = 0
            self.hullHeal = self.damage1
        else:
            self.shieldHeal = self.damage1
            self.hullHeal = 0
        if not (self.targetID in self.playerList):
            self.damaged = players("name", False, None)
        if self.damage1 > self.attacker.maxOneHeal:
            self.attacker.maxOneHeal = self.damage1
            self.attacker.maxOneHealWeapon = self.source

        # non pet heals
        if self.pet == "*" or self.targetID == "*":
            self.generateHealsOutTable()
            self.generateHealsInTable()

        # pet heals
        else:
            self.ability = self.sourceID
            self.source = self.pet
            self.sourceIDtmp = self.petID
            self.target = self.targetID
            self.sourceID = self.source + self.sourceIDtmp
            self.abilityID = self.sourceID + self.ability
            self.targetID = self.sourceID + self.ability + self.target
            self.tempTargetID = self.target.split("[")[1]
            self.tempTargetID = self.tempTargetID.split(" ")[0]
            self.displayTarget = self.line[self.combatlogDict["target"]] + " " + self.tempTargetID
            self.tempdisplaysourceID = self.sourceIDtmp.split("[")[1]
            self.tempdisplaysourceID = self.tempdisplaysourceID.split(" ")[0]
            self.displaysourceID = self.source + " " + self.tempdisplaysourceID
            self.generateHealsInTable()
            self.generateHealsOutTable()
            self.attacker = players(" ", " ", " ")
            self.petHeals()

    def generateDMGStatLine(self):
        return [self.dmgOutSource, self.source, self.damage1, 0, self.damage1, (1 if self.isCrit else 0),
                (1 if self.isFlank else 0), 1, (1 if self.isMiss else 0), 0, 0, 0, (1 if self.isKill else 0),
                self.hulldamage, self.shielddamage, (0 if self.damagetype == "Shield" else self.resist), 1, 0]

    def generateDMGStatLineOpen(self):
        return [float(self.damage1), 0, float(self.damage1), (1 if self.isCrit else 0),
               (1 if self.isFlank else 0), 1, (1 if self.isMiss else 0), 0, 0, 0, (1 if self.isKill else 0),
               float(self.hulldamage), float(self.shielddamage), (0 if self.damagetype == "Shield" else float(self.resist)), 1, 0]

    def damageInUpdater(self):
        self.dmgOutSource = self.ID
        if self.dmgOutSource in self.damaged.dmginTable:
            newTargeted = True
            for col in self.damaged.dmginTable[self.damaged.dmgInDict[self.dmgOutSource]]:
                if col[self.damaged.dmgoutindex["target"]] == self.source:
                    newTargeted = False
                    self.damaged.dmginTable[self.damaged.dmgInDict[self.dmgOutSource]][0][
                        self.attacker.dmgoutindex["damage"]] += self.damage1
                    self.damaged.dmginTable[self.damaged.dmgInDict[self.dmgOutSource]][0][
                        self.attacker.dmgoutindex["hulldamage"]] += self.hulldamage
                    self.damaged.dmginTable[self.damaged.dmgInDict[self.dmgOutSource]][0][
                        self.attacker.dmgoutindex["shielddamage"]] += self.shielddamage
                    if not self.source in self.excludeAttacks:
                        self.damaged.dmginTable[self.damaged.dmgInDict[self.dmgOutSource]][0][
                            self.attacker.dmgoutindex["attacks"]] += 1
                        col[self.attacker.dmgoutindex["attacks"]] += 1
                    col[self.attacker.dmgoutindex["damage"]] += self.damage1
                    col[self.attacker.dmgoutindex["hulldamage"]] += self.hulldamage
                    col[self.attacker.dmgoutindex["shielddamage"]] += self.shielddamage
                    if not self.damagetype == "Shield" and not self.isMiss and not self.resist == 0:
                        self.damaged.dmginTable[self.damaged.dmgInDict[self.dmgOutSource]][0][
                            self.attacker.dmgoutindex["hullAttacks"]] += 1
                        self.damaged.dmginTable[self.damaged.dmgInDict[self.dmgOutSource]][0][
                            self.attacker.dmgoutindex["resist"]] += self.resist
                        col[self.attacker.dmgoutindex["resist"]] += self.resist
                    if self.damage1 > self.damaged.dmginTable[self.damaged.dmgInDict[self.dmgOutSource]][0][
                        self.attacker.dmgoutindex["maxHit"]]:
                        self.damaged.dmginTable[self.damaged.dmgInDict[self.dmgOutSource]][0][
                            self.attacker.dmgoutindex["maxHit"]] = self.damage1
                    if self.damage1 > col[self.attacker.dmgoutindex["maxHit"]]:
                        col[self.attacker.dmgoutindex["maxHit"]] = self.damage1

                    if self.isMiss:
                        self.damaged.dmginTable[self.damaged.dmgInDict[self.dmgOutSource]][0][
                            self.attacker.dmgoutindex["misses"]] += 1
                        col[self.attacker.dmgoutindex["misses"]] += 1
                    if self.isCrit:
                        self.damaged.dmginTable[self.damaged.dmgInDict[self.dmgOutSource]][0][
                            self.attacker.dmgoutindex["crits"]] += 1
                        col[self.attacker.dmgoutindex["crits"]] += 1
                    if self.isFlank:
                        self.damaged.dmginTable[self.damaged.dmgInDict[self.dmgOutSource]][0][
                            self.attacker.dmgoutindex["flanks"]] += 1
                        col[self.attacker.dmgoutindex["flanks"]] += 1
                    if self.isKill:
                        self.damaged.dmginTable[self.damaged.dmgInDict[self.dmgOutSource]][0][
                            self.attacker.dmgoutindex["kills"]] += 1
                        col[self.attacker.dmgoutindex["kills"]] += 1

            if newTargeted:
                self.damaged.dmginTable[self.damaged.dmgInDict[self.dmgOutSource]].append(
                   self.arrayExtend([self.dmgOutSource, self.source], self.generateDMGStatLineOpen()))
                self.damaged.dmginTable[self.damaged.dmgInDict[self.dmgOutSource]][0][
                    self.attacker.dmgoutindex["damage"]] += self.damage1
                self.damaged.dmginTable[self.damaged.dmgInDict[self.dmgOutSource]][0][
                    self.attacker.dmgoutindex["hulldamage"]] += self.hulldamage
                self.damaged.dmginTable[self.damaged.dmgInDict[self.dmgOutSource]][0][
                    self.attacker.dmgoutindex["shielddamage"]] += self.shielddamage
                if not self.damagetype == "Shield" and not self.isMiss and not self.resist == 0:
                    self.damaged.dmginTable[self.damaged.dmgInDict[self.dmgOutSource]][0][
                        self.attacker.dmgoutindex["hullAttacks"]] += 1
                    self.damaged.dmginTable[self.damaged.dmgInDict[self.dmgOutSource]][0][
                        self.attacker.dmgoutindex["resist"]] += self.resist
                if not self.source in self.excludeAttacks:
                    self.damaged.dmginTable[self.damaged.dmgInDict[self.dmgOutSource]][0][
                        self.attacker.dmgoutindex["attacks"]] += 1
                if self.damage1 > self.damaged.dmginTable[self.damaged.dmgInDict[self.dmgOutSource]][0][
                    self.attacker.dmgoutindex["maxHit"]]:
                    self.damaged.dmginTable[self.damaged.dmgInDict[self.dmgOutSource]][0][
                        self.attacker.dmgoutindex["maxHit"]] = self.damage1
                if self.isMiss:
                    self.damaged.dmginTable[self.damaged.dmgInDict[self.dmgOutSource]][0][
                        self.attacker.dmgoutindex["misses"]] += 1
                if self.isCrit:
                    self.damaged.dmginTable[self.damaged.dmgInDict[self.dmgOutSource]][0][
                        self.attacker.dmgoutindex["crits"]] += 1
                if self.isFlank:
                    self.damaged.dmginTable[self.damaged.dmgInDict[self.dmgOutSource]][0][
                        self.attacker.dmgoutindex["flanks"]] += 1
                if self.isKill:
                    self.damaged.dmginTable[self.damaged.dmgInDict[self.dmgOutSource]][0][
                        self.attacker.dmgoutindex["kills"]] += 1

        else:
            self.damaged.dmginTable.append([
                self.arrayExtend([self.source, "global"],self.generateDMGStatLineOpen()),
                self.arrayExtend([self.source, self.target],self.generateDMGStatLineOpen())])
            self.damaged.dmgInDict.update({self.dmgOutSource: len(self.attacker.dmgoutTable) - 1})

    def damageOutUpdater(self):
        if self.source in self.attacker.dmgoutDict:
            newTarget = True
            for col in self.attacker.dmgoutTable[self.attacker.dmgoutDict[self.source]]:
                if col[self.attacker.dmgoutindex["target"]] == self.target:
                    newTarget = False
                    self.attacker.dmgoutTable[self.attacker.dmgoutDict[self.source]][0][
                        self.attacker.dmgoutindex["damage"]] += float(self.damage1)
                    self.attacker.dmgoutTable[self.attacker.dmgoutDict[self.source]][0][
                        self.attacker.dmgoutindex["hulldamage"]] += self.hulldamage
                    self.attacker.dmgoutTable[self.attacker.dmgoutDict[self.source]][0][
                        self.attacker.dmgoutindex["shielddamage"]] += self.shielddamage
                    if not self.source in self.excludeAttacks:
                        self.attacker.dmgoutTable[self.attacker.dmgoutDict[self.source]][0][
                            self.attacker.dmgoutindex["attacks"]] += 1
                        col[self.attacker.dmgoutindex["attacks"]] += 1
                    col[self.attacker.dmgoutindex["damage"]] += self.damage1
                    col[self.attacker.dmgoutindex["hulldamage"]] += self.hulldamage
                    col[self.attacker.dmgoutindex["shielddamage"]] += self.shielddamage
                    if not self.damagetype == "Shield" and not self.isMiss and not self.resist == 0:
                        self.attacker.dmgoutTable[self.attacker.dmgoutDict[self.source]][0][
                            self.attacker.dmgoutindex["hullAttacks"]] += 1
                        self.attacker.dmgoutTable[self.attacker.dmgoutDict[self.source]][0][
                            self.attacker.dmgoutindex["resist"]] += self.resist
                        col[self.attacker.dmgoutindex["resist"]] += self.resist
                    if self.damage1 > self.attacker.dmgoutTable[self.attacker.dmgoutDict[self.source]][0][
                        self.attacker.dmgoutindex["maxHit"]]:
                        self.attacker.dmgoutTable[self.attacker.dmgoutDict[self.source]][0][
                            self.attacker.dmgoutindex["maxHit"]] = self.damage1
                    if self.damage1 > col[self.attacker.dmgoutindex["maxHit"]]:
                        col[self.attacker.dmgoutindex["maxHit"]] = self.damage1
                    if self.isMiss:
                        self.attacker.dmgoutTable[self.attacker.dmgoutDict[self.source]][0][
                            self.attacker.dmgoutindex["misses"]] += 1
                        col[self.attacker.dmgoutindex["misses"]] += 1
                    if self.isCrit:
                        self.attacker.dmgoutTable[self.attacker.dmgoutDict[self.source]][0][
                            self.attacker.dmgoutindex["crits"]] += 1
                        col[self.attacker.dmgoutindex["crits"]] += 1
                    if self.isFlank:
                        self.attacker.dmgoutTable[self.attacker.dmgoutDict[self.source]][0][
                            self.attacker.dmgoutindex["flanks"]] += 1
                        col[self.attacker.dmgoutindex["flanks"]] += 1
                    if self.isKill:
                        self.attacker.dmgoutTable[self.attacker.dmgoutDict[self.source]][0][
                            self.attacker.dmgoutindex["kills"]] += 1
                        col[self.attacker.dmgoutindex["kills"]] += 1
            if newTarget:
                self.attacker.dmgoutTable[self.attacker.dmgoutDict[self.source]].append(
                    self.arrayExtend([self.source, self.target],(self.generateDMGStatLineOpen())))
                self.attacker.dmgoutTable[self.attacker.dmgoutDict[self.source]][0][
                    self.attacker.dmgoutindex["damage"]] += self.damage1
                self.attacker.dmgoutTable[self.attacker.dmgoutDict[self.source]][0][
                    self.attacker.dmgoutindex["hulldamage"]] += self.hulldamage
                self.attacker.dmgoutTable[self.attacker.dmgoutDict[self.source]][0][
                    self.attacker.dmgoutindex["shielddamage"]] += self.shielddamage
                if not self.damagetype == "Shield" and not self.isMiss and not self.resist == 0:
                    self.attacker.dmgoutTable[self.attacker.dmgoutDict[self.source]][0][
                        self.attacker.dmgoutindex["hullAttacks"]] += 1
                    self.attacker.dmgoutTable[self.attacker.dmgoutDict[self.source]][0][
                        self.attacker.dmgoutindex["resist"]] += self.resist
                if not self.source in self.excludeAttacks:
                    self.attacker.dmgoutTable[self.attacker.dmgoutDict[self.source]][0][
                        self.attacker.dmgoutindex["attacks"]] += 1
                if self.damage1 > self.attacker.dmgoutTable[self.attacker.dmgoutDict[self.source]][0][
                    self.attacker.dmgoutindex["maxHit"]]:
                    self.attacker.dmgoutTable[self.attacker.dmgoutDict[self.source]][0][
                        self.attacker.dmgoutindex["maxHit"]] = self.damage1
                if self.isMiss:
                    self.attacker.dmgoutTable[self.attacker.dmgoutDict[self.source]][0][
                        self.attacker.dmgoutindex["misses"]] += 1
                if self.isCrit:
                    self.attacker.dmgoutTable[self.attacker.dmgoutDict[self.source]][0][
                        self.attacker.dmgoutindex["crits"]] += 1
                if self.isFlank:
                    self.attacker.dmgoutTable[self.attacker.dmgoutDict[self.source]][0][
                        self.attacker.dmgoutindex["flanks"]] += 1
                if self.isKill:
                    self.attacker.dmgoutTable[self.attacker.dmgoutDict[self.source]][0][
                        self.attacker.dmgoutindex["kills"]] += 1
        else:
            self.attacker.dmgoutTable.append([
                self.arrayExtend([self.source, "global"],self.generateDMGStatLineOpen()),
                self.arrayExtend([self.source, self.target],self.generateDMGStatLineOpen())])
            self.attacker.dmgoutDict.update({self.source: len(self.attacker.dmgoutTable) - 1})


    def addDamageStats(self):
        if not self.source in self.excludeDamage:
            if not ((self.targetID in self.playerList) and (
                    self.ID in self.playerList)):
                if self.damage1 < 0:
                    self.damage1 *= -1
                # update general stats of self.attacker
                self.attacker.totaldamage += self.damage1
                if self.damage1 > self.attacker.maxOneHit:
                    self.attacker.maxOneHit = self.damage1
                    self.attacker.maxOneHitWeapon = self.source
                self.resist = 0
                if not self.damagetype == "Shield" and not self.isMiss:
                    if self.damage2 == 0:
                        self.resist = 0
                    else:
                        self.resist = self.damage1 / self.damage2 * 100
                        if not self.resist == 0:
                            self.attacker.resist += self.resist
                            self.attacker.hullAttacks += 1

                if self.targetID in self.playerList:
                    self.damaged.totalDamageTaken += self.damage1
                    if not self.source in self.excludeAttacks:
                        self.damaged.totalAttacksTaken += 1
                else:
                    self.damaged = players("name", False, None)

                # update stats
                self.attacker.updateStats(self.time)
                # dmg Hanlder        ADD HULL AND SHIELD DAMAGE ROWS

                self.hulldamage = 0
                self.shielddamage = 0
                if not self.source in self.excludeAttacks:
                    self.attacker.totalAttacks += 1
                if self.damagetype == "Shield":
                    self.shielddamage = self.damage1
                else:
                    self.hulldamage = self.damage1
                self.attacker.hulllDamage += self.hulldamage
                self.attacker.shieldDamage += self.shielddamage

                # DMGout updater
                self.damageOutUpdater()
                self.damageInUpdater()

    def petTableUpdater(self):
        # check if pet type already exists
        if self.source in self.attacker.petSourceDict:
            # update damage of existing pet type
            self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][0][
                self.attacker.dmgoutindex["damage"]] += self.damage1
            self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][0][
                self.attacker.dmgoutindex["hulldamage"]] += self.hulldamage
            self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][0][
                self.attacker.dmgoutindex["shielddamage"]] += self.shielddamage
            if not self.damagetype == "Shield" and not self.isMiss and not self.resist == 0:
                self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][0][
                    self.attacker.dmgoutindex["hullAttacks"]] += 1
                self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][0][
                    self.attacker.dmgoutindex["resist"]] += self.resist
            if not self.weapon in self.excludeAttacks:
                self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][0][
                    self.attacker.dmgoutindex["attacks"]] += 1
            if self.damage1 > self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][0][
                self.attacker.dmgoutindex["maxHit"]]:
                self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][0][
                    self.attacker.dmgoutindex["maxHit"]] = self.damage1
            if self.isMiss:
                self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][0][
                    self.attacker.dmgoutindex["misses"]] += 1
            if self.isCrit:
                self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][0][
                    self.attacker.dmgoutindex["crits"]] += 1
            if self.isFlank:
                self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][0][
                    self.attacker.dmgoutindex["flanks"]] += 1
            if self.isKill:
                self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][0][
                    self.attacker.dmgoutindex["kills"]] += 1

            # check if pet instance exists
            if self.sourceID in self.attacker.petSourceidDict:
                # updateing stats of pet instance
                self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                    self.attacker.petSourceidDict[self.sourceID]][0][
                    self.attacker.dmgoutindex["damage"]] += self.damage1
                self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                    self.attacker.petSourceidDict[self.sourceID]][0][
                    self.attacker.dmgoutindex["hulldamage"]] += self.hulldamage
                self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                    self.attacker.petSourceidDict[self.sourceID]][0][
                    self.attacker.dmgoutindex["shielddamage"]] += self.shielddamage
                if not self.damagetype == "Shield" and not self.isMiss and not self.resist == 0:
                    self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                        self.attacker.petSourceidDict[self.sourceID]][0][
                        self.attacker.dmgoutindex["hullAttacks"]] += 1
                    self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                        self.attacker.petSourceidDict[self.sourceID]][0][
                        self.attacker.dmgoutindex["resist"]] += self.resist
                if not self.weapon in self.excludeAttacks:
                    self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                        self.attacker.petSourceidDict[self.sourceID]][0][
                        self.attacker.dmgoutindex["attacks"]] += 1
                if self.damage1 > self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                    self.attacker.petSourceidDict[self.sourceID]][0][
                    self.attacker.dmgoutindex["maxHit"]]:
                    self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                        self.attacker.petSourceidDict[self.sourceID]][0][
                        self.attacker.dmgoutindex["maxHit"]] = self.damage1
                if self.isMiss:
                    self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                        self.attacker.petSourceidDict[self.sourceID]][0][
                        self.attacker.dmgoutindex["misses"]] += 1
                if self.isCrit:
                    self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                        self.attacker.petSourceidDict[self.sourceID]][0][
                        self.attacker.dmgoutindex["crits"]] += 1
                if self.isFlank:
                    self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                        self.attacker.petSourceidDict[self.sourceID]][0][
                        self.attacker.dmgoutindex["flanks"]] += 1
                if self.isKill:
                    self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                        self.attacker.petSourceidDict[self.sourceID]][0][
                        self.attacker.dmgoutindex["kills"]] += 1
                # check if weapon for pet exists
                if self.weaponID in self.attacker.petWeaponDict:
                    # update stats
                    self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                        self.attacker.petSourceidDict[self.sourceID]][
                        self.attacker.petWeaponDict[self.weaponID]][0][
                        self.attacker.dmgoutindex["damage"]] += self.damage1
                    self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                        self.attacker.petSourceidDict[self.sourceID]][
                        self.attacker.petWeaponDict[self.weaponID]][0][
                        self.attacker.dmgoutindex["hulldamage"]] += self.hulldamage
                    self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                        self.attacker.petSourceidDict[self.sourceID]][
                        self.attacker.petWeaponDict[self.weaponID]][0][
                        self.attacker.dmgoutindex["shielddamage"]] += self.shielddamage
                    if not self.damagetype == "Shield" and not self.isMiss and not self.resist == 0:
                        self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                            self.attacker.petSourceidDict[self.sourceID]][
                            self.attacker.petWeaponDict[self.weaponID]][0][
                            self.attacker.dmgoutindex["hullAttacks"]] += 1
                        self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                            self.attacker.petSourceidDict[self.sourceID]][
                            self.attacker.petWeaponDict[self.weaponID]][0][
                            self.attacker.dmgoutindex["resist"]] += self.resist
                    if not self.weapon in self.excludeAttacks:
                        self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                            self.attacker.petSourceidDict[self.sourceID]][
                            self.attacker.petWeaponDict[self.weaponID]][0][
                            self.attacker.dmgoutindex["attacks"]] += 1
                    if self.damage1 > self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                        self.attacker.petSourceidDict[self.sourceID]][
                        self.attacker.petWeaponDict[self.weaponID]][0][
                        self.attacker.dmgoutindex["maxHit"]]:
                        self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                            self.attacker.petSourceidDict[self.sourceID]][
                            self.attacker.petWeaponDict[self.weaponID]][0][
                            self.attacker.dmgoutindex["maxHit"]] = self.damage1
                    if self.isMiss:
                        self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                            self.attacker.petSourceidDict[self.sourceID]][
                            self.attacker.petWeaponDict[self.weaponID]][0][
                            self.attacker.dmgoutindex["misses"]] += 1
                    if self.isCrit:
                        self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                            self.attacker.petSourceidDict[self.sourceID]][
                            self.attacker.petWeaponDict[self.weaponID]][0][
                            self.attacker.dmgoutindex["crits"]] += 1
                    if self.isFlank:
                        self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                            self.attacker.petSourceidDict[self.sourceID]][
                            self.attacker.petWeaponDict[self.weaponID]][0][
                            self.attacker.dmgoutindex["flanks"]] += 1
                    if self.isKill:
                        self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                            self.attacker.petSourceidDict[self.sourceID]][
                            self.attacker.petWeaponDict[self.weaponID]][0][
                            self.attacker.dmgoutindex["kills"]] += 1

                    if self.targetID in self.attacker.petTargetDict:
                        self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                            self.attacker.petSourceidDict[self.sourceID]][
                            self.attacker.petWeaponDict[self.weaponID]][
                            self.attacker.petTargetDict[self.targetID]][
                            self.attacker.dmgoutindex["hulldamage"]] += self.hulldamage
                        self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                            self.attacker.petSourceidDict[self.sourceID]][
                            self.attacker.petWeaponDict[self.weaponID]][
                            self.attacker.petTargetDict[self.targetID]][
                            self.attacker.dmgoutindex["damage"]] += self.damage1
                        self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                            self.attacker.petSourceidDict[self.sourceID]][
                            self.attacker.petWeaponDict[self.weaponID]][
                            self.attacker.petTargetDict[self.targetID]][
                            self.attacker.dmgoutindex["shielddamage"]] += self.shielddamage
                        if not self.damagetype == "Shield" and not self.isMiss and not self.resist == 0:
                            self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                                self.attacker.petSourceidDict[self.sourceID]][
                                self.attacker.petWeaponDict[self.weaponID]][
                                self.attacker.petTargetDict[self.targetID]][
                                self.attacker.dmgoutindex["hullAttacks"]] += 1
                            self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                                self.attacker.petSourceidDict[self.sourceID]][
                                self.attacker.petWeaponDict[self.weaponID]][
                                self.attacker.petTargetDict[self.targetID]][
                                self.attacker.dmgoutindex["resist"]] += self.resist
                        if not self.weapon in self.excludeAttacks:
                            self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                                self.attacker.petSourceidDict[self.sourceID]][
                                self.attacker.petWeaponDict[self.weaponID]][
                                self.attacker.petTargetDict[self.targetID]][
                                self.attacker.dmgoutindex["attacks"]] += 1
                        if self.damage1 > \
                                self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                                    self.attacker.petSourceidDict[self.sourceID]][
                                    self.attacker.petWeaponDict[self.weaponID]][
                                    self.attacker.petTargetDict[self.targetID]][self.attacker.dmgoutindex["maxHit"]]:
                            self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                                self.attacker.petSourceidDict[self.sourceID]][
                                self.attacker.petWeaponDict[self.weaponID]][
                                self.attacker.petTargetDict[self.targetID]][
                                self.attacker.dmgoutindex["maxHit"]] = self.damage1
                        if self.isMiss:
                            self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                                self.attacker.petSourceidDict[self.sourceID]][
                                self.attacker.petWeaponDict[self.weaponID]][
                                self.attacker.petTargetDict[self.targetID]][self.attacker.dmgoutindex["misses"]] += 1
                        if self.isCrit:
                            self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                                self.attacker.petSourceidDict[self.sourceID]][
                                self.attacker.petWeaponDict[self.weaponID]][
                                self.attacker.petTargetDict[self.targetID]][self.attacker.dmgoutindex["crits"]] += 1
                        if self.isFlank:
                            self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                                self.attacker.petSourceidDict[self.sourceID]][
                                self.attacker.petWeaponDict[self.weaponID]][
                                self.attacker.petTargetDict[self.targetID]][self.attacker.dmgoutindex["flanks"]] += 1
                        if self.isKill:
                            self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                                self.attacker.petSourceidDict[self.sourceID]][
                                self.attacker.petWeaponDict[self.weaponID]][
                                self.attacker.petTargetDict[self.targetID]][self.attacker.dmgoutindex["kills"]] += 1

                    else:
                        self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                            self.attacker.petSourceidDict[self.sourceID]][
                            self.attacker.petWeaponDict[self.weaponID]].append(
                            self.arrayExtend([self.target, self.displayTarget],self.generateDMGStatLineOpen()))
                        self.attacker.petTargetDict.update({self.targetID: len(
                            self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                                self.attacker.petSourceidDict[self.sourceID]][
                                self.attacker.petWeaponDict[self.weaponID]]) - 1})

                else:
                    # adding new weapon instance
                    self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                        self.attacker.petSourceidDict[self.sourceID]].append(
                        [self.arrayExtend([self.weapon, self.weapon],self.generateDMGStatLineOpen()),
                         self.arrayExtend([self.target, self.displayTarget],self.generateDMGStatLineOpen())])
                    self.attacker.petWeaponDict.update({self.weaponID: len(
                        self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                            self.attacker.petSourceidDict[self.sourceID]]) - 1})
                    self.attacker.petTargetDict.update({self.targetID: len(
                        self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                            self.attacker.petSourceidDict[self.sourceID]][
                            self.attacker.petWeaponDict[self.weaponID]]) - 1})


            else:
                # adding a new unique pet to a type of pet
                self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]].append(
                    [self.arrayExtend([self.sourceID, self.displaysourceID],self.generateDMGStatLineOpen()), [self.arrayExtend([self.weapon, self.weapon],self.generateDMGStatLineOpen()), self.arrayExtend([self.target,
                                       self.displayTarget],self.generateDMGStatLineOpen())]])
                self.attacker.petSourceidDict.update(
                    {self.sourceID: len(
                        self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]]) - 1})
                self.attacker.petWeaponDict.update({self.weaponID: len(
                    self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                        self.attacker.petSourceidDict[self.sourceID]]) - 1})
                self.attacker.petTargetDict.update({self.targetID: len(
                    self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                        self.attacker.petSourceidDict[self.sourceID]][
                        self.attacker.petWeaponDict[self.weaponID]]) - 1})

        else:
            # adding a new pet type
            self.attacker.petDMGTable.append(
                [self.arrayExtend([self.source, self.source],self.generateDMGStatLineOpen()), [
                     self.arrayExtend([self.sourceID, self.displaysourceID],self.generateDMGStatLineOpen()), [
                        self.arrayExtend([self.weapon, self.weapon],self.generateDMGStatLineOpen()),
                        self.arrayExtend([self.target, self.displayTarget],self.generateDMGStatLineOpen())]]])
            self.attacker.petSourceDict.update({self.source: len(self.attacker.petDMGTable) - 1})
            self.attacker.petSourceidDict.update(
                {self.sourceID: len(
                    self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]]) - 1})
            self.attacker.petWeaponDict.update({self.weaponID: len(
                self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                    self.attacker.petSourceidDict[self.sourceID]]) - 1})
            self.attacker.petTargetDict.update({self.targetID: len(
                self.attacker.petDMGTable[self.attacker.petSourceDict[self.source]][
                    self.attacker.petSourceidDict[self.sourceID]][
                    self.attacker.petWeaponDict[self.weaponID]]) - 1})



    def petDamageUpdater(self):
        if not self.source in self.excludeDamage:
            if not ((self.targetID in self.playerList) and (
                    self.ID in self.playerList)):
                if self.damage1 < 0:
                    self.damage1 *= -1
                self.sourceID = self.petID
                self.weapon = self.source
                self.target = self.targetID

                self.source = "Pets (sum)"
                # update general stats of self.attacker

                self.attacker.totaldamage += self.damage1
                if self.damage1 > self.attacker.maxOneHit:
                    self.attacker.maxOneHit = self.damage1
                    self.attacker.maxOneHitWeapon = self.line[self.combatlogDict["pet"]]

                if self.targetID in self.playerList:
                    self.damaged.totalDamageTaken += self.damage1
                    if not self.source in self.excludeAttacks:
                        self.damaged.totalAttacksTaken += 1
                # update stats
                self.attacker.updateStats(self.time)

                # specific attacks handler

                self.resist = 0
                if not self.damagetype == "Shield" and not self.isMiss:
                    if self.damage2 == 0:
                        self.resist = 0
                    else:
                        self.resist = self.damage1 / self.damage2 * 100
                        if not self.resist == 0:
                            self.attacker.resist += self.resist
                            self.attacker.hullAttacks += 1

                hulldamage = 0
                shielddamage = 0

                if self.damagetype == "Shield":
                    shielddamage = self.damage1
                else:
                    hulldamage = self.damage1
                self.attacker.hulllDamage += hulldamage
                self.attacker.shieldDamage += shielddamage

                self.damageOutUpdater()


                self.source = self.line[self.combatlogDict["pet"]]
                self.weaponID = self.player + self.source + self.sourceID + self.weapon
                self.targetID = self.player + self.source + self.sourceID + self.weapon + self.target
                if not self.source in self.excludeAttacks:
                    self.attacker.totalAttacks += 1
                self.damageInUpdater()
                self.tempTargetID = self.target.split("[")[1]
                self.tempTargetID = self.tempTargetID.split(" ")[0]
                self.displayTarget = self.line[self.combatlogDict["target"]] + " " + self.tempTargetID
                self.tempdisplaysourceID = self.sourceID.split("[")[1]
                self.tempdisplaysourceID = self.tempdisplaysourceID.split(" ")[0]
                self.displaysourceID = self.source + " " + self.tempdisplaysourceID

                self.petTableUpdater()

    def WCBHandler(self):

        if self.WCBrule == "Global":
            if not "WarpCoreBreach" in self.playerdict:
                self.tableArray.append(
                    players("WarpCoreBreach", False, self.timeToTimeAndDate(self.date)))
                self.playerdict.update({"WarpCoreBreach": self.counter2})
                self.counter2 += 1
            self.attacker = self.tableArray[self.playerdict["WarpCoreBreach"]]
        elif self.WCBrule == "Personal":
            self.attacker = self.tableArray[self.playerdict[self.ID]]
        elif self.WCBrule == "Killer":
            self.attacker = self.tableArray[self.playerdict[self.ID.killedByLast]]
        if self.damage1 < 0:
            self.damage1 *= -1
        self.sourceID = self.ID + "_WCB"
        self.weapon = "Warp Core Breach"
        self.target = self.targetID
        self.source = "Pets (sum)"
        # update general stats of self.attacker
        self.attacker.totaldamage += self.damage1
        if self.damage1 > self.attacker.maxOneHit:
            self.attacker.maxOneHit = self.damage1
            self.attacker.maxOneHitWeapon = "Warp Core Breach"
        if self.targetID in self.playerList:
            self.damaged.totalDamageTaken += self.damage1
            if not self.source in self.excludeAttacks:
                self.damaged.totalAttacksTaken += 1
        else:
            self.damaged = players("name", False, None)
        # update stats
        self.attacker.updateStats(self.time)

        # specific attacks handler

        self.resist = 0
        if not self.damagetype == "Shield" and not self.isMiss:
            if self.damage2 == 0:
                self.resist = 0
            else:
                self.resist = self.damage1 / self.damage2 * 100
                if not self.resist == 0:
                    self.attacker.resist += self.resist
                    self.attacker.hullAttacks += 1

        self.hulldamage = 0
        self.shielddamage = 0

        if self.damagetype == "Shield":
            self.shielddamage = self.damage1
        else:
            self.hulldamage = self.damage1
        self.attacker.hulllDamage += self.hulldamage
        self.attacker.shieldDamage += self.shielddamage

        self.damageOutUpdater()

        self.source = "Warp Core Breach"
        self.weaponID = self.player + self.source + self.sourceID + self.weapon
        self.targetID = self.player + self.source + self.sourceID + self.weapon + self.target
        if not self.source in self.excludeAttacks:
            self.attacker.totalAttacks += 1

        self.damageInUpdater()

        self.tempTargetID = self.target.split("[")[1]
        self.tempTargetID = self.tempTargetID.split(" ")[0]
        self.displayTarget = self.line[self.combatlogDict["target"]] + " " + self.tempTargetID
        self.tempdisplaysourceID = self.sourceID.split("[")[1]
        self.tempdisplaysourceID = self.tempdisplaysourceID.split(" ")[0]
        self.displaysourceID = self.source + " " + self.tempdisplaysourceID

        self.petTableUpdater()


    def combatLogAnalysis(self):
        firstLine = True
        for x in self.combatlog:
            final = []
            splicer1 = x.split("::")
            final.append(splicer1[0])
            splicer11 = splicer1[1]
            splicer2 = splicer11.split(",")
            for y in splicer2:
                if y == "":
                    y = "*"
                final.append(y)
            x = final
            self.line = x
            self.date = x[self.combatlogDict["date"]]
            self.character = x[self.combatlogDict["character"]]
            self.ID = x[self.combatlogDict["ID"]]
            self.dmgOutSource = self.ID
            self.pet = x[self.combatlogDict["pet"]]
            self.petID = x[self.combatlogDict["petID"]]
            self.target = x[self.combatlogDict["target"]]
            self.targetID = x[self.combatlogDict["targetID"]]
            self.source = x[self.combatlogDict["source"]]
            self.sourceID = x[self.combatlogDict["sourceID"]]
            self.resist = 0
            self.hullAttacks = 0
            self.isPlayer = (True if self.ID[0] == "P" else False)
            self.targetIsPlayer = (True if self.targetID[0] == "P" else False)

            if self.ID not in self.playerList and self.ID not in self.NPCs:
                if self.isPlayer:

                    self.playerList.append(self.ID)
                    self.createTableInstance()
                elif not self.ID in self.NPCs:
                    self.NPCs.append(self.ID)
                    self.createTableInstance()
            if self.targetID not in self.NPCs and self.targetID not in self.playerList:
                if not self.targetID == "*" and not self.targetID == None:
                    if self.targetID not in self.playerList and self.targetIsPlayer:
                        self.playerList.append(self.targetID)
                        self.createTableInstanceAlternate(True)
                    elif self.targetID not in self.NPCs:
                        self.NPCs.append(self.targetID)
                        self.createTableInstanceAlternate(False)
            if self.targetID in self.playerList or self.targetID in self.NPCs:
                self.damaged = self.tableArray[self.playerdict[self.targetID]]
            else:
                self.damaged = players("name", False, None)
            self.attacker = self.tableArray[self.playerdict[self.ID]]
            self.player = self.attacker.name
            self.damage1 = float(x[self.combatlogDict["mag1"]])
            self.damage2 = float(x[self.combatlogDict["mag2"]])
            self.damagetype = x[self.combatlogDict["dmageType"]]
            self.time = self.timeToTimeAndDate(self.date)

            self.splicedCombatlog.append(x)
            # if not x[combatlogDict["targetID"]] in templist and x[combatlogDict["sourceID"]] == "P[12231228@5044720 CasualSAB@spencerb96]":
            #     templist.append(x[combatlogDict["targetID"]])
            #     print("adsfaf", x[combatlogDict["targetID"]])
            if firstLine:
                self.globalCombatStart = self.timeToTimeAndDate(x[self.combatlogDict["date"]])
                firstLine = False


            # flag updater
            self.isCrit, self.isMiss, self.isFlank, self.isKill = self.getFlags(x[self.combatlogDict["flags"]])
            if self.isMiss:
                self.attacker.misses += 1
            if self.isCrit:
                if (self.damagetype == "Shield" and self.damage1 < 0 and self.damage2 >= 0) or self.damagetype == "HitPoints":
                    self.attacker.totalHealCrits += 1
                else:
                    self.attacker.totalCrits += 1
            if self.isFlank:
                self.attacker.flanks = self.attacker.flanks + 1
            if self.isKill:
                self.attacker.kills += 1
                if x[self.combatlogDict["targetID"]] in self.playerdict:
                    self.tableArray[self.playerdict[x[self.combatlogDict["targetID"]]]].deaths += 1
                    self.tableArray[self.playerdict[x[self.combatlogDict["targetID"]]]].killedByLast = x[self.combatlogDict["ID"]]
                    self.tableArray[self.playerdict[x[self.combatlogDict["targetID"]]]].timeKilled = self.timeToTimeAndDate(x[self.combatlogDict["date"]])


            # self.attacker = players("name", True, None)


            if not self.depthAnalysis: #quick scan
                self.quickScan()


            else:
                # Heals
                if (self.damagetype == "Shield" and self.damage1 < 0 and self.damage2 >= 0) or self.damagetype == "HitPoints":
                    self.addHeals()


                elif x[self.combatlogDict["source"]] == "Warp Core Breach":
                    self.WCBHandler()


                # Non pets
                elif (x[self.combatlogDict["pet"]] == "*" or x[
                    self.combatlogDict["targetID"]] == "*") and self.damagetype != "HitPoints":
                    self.addDamageStats()


                # Pets
                else:
                    self.petDamageUpdater()



            timer = self.timeToTimeAndDate(self.date)
            if self.lastGraphTime == None:
                self.lastGraphTime = timer
            if not (self.damagetype == "Shield" and self.damage1 < 0 and self.damage2 >= 0) or not self.damagetype == "HitPoints":

                if self.attacker.name in self.bufferedDamage:
                    if self.damage1 < 0:
                        self.damage1 *= -1
                    previousDamage = self.bufferedDamage[self.attacker.name]
                    damage = previousDamage + self.damage1
                    self.bufferedDamage.update({self.attacker.name: damage})
                else:
                    self.bufferedDamage.update({self.attacker.name: self.damage1})
            if (timer - self.lastGraphTime) >= self.graphDelta:
                for updatedPlayer in self.tableArray:
                    killedTime = updatedPlayer.timeKilled
                    if killedTime == None:
                        killedTime = timer
                    temptime = self.deltaValue*250
                    if (timer - killedTime < datetime.timedelta(milliseconds=temptime)):
                        updatedPlayer.updateStats(timer)
                        if updatedPlayer.name in self.bufferedDamage:
                            bufferDamage = self.bufferedDamage[updatedPlayer.name]
                        else:
                            bufferDamage = 0
                        if updatedPlayer.name in (self.DPSChart if updatedPlayer.isPlayer else self.NPCDPSChart):
                            DPScharts = (self.DPSChart[updatedPlayer.name] if updatedPlayer.isPlayer else self.NPCDPSChart[updatedPlayer.name])
                            damageChart = (self.damageChart[updatedPlayer.name] if updatedPlayer.isPlayer else self.NPCDamageChart[updatedPlayer.name])
                            DPScharts[0].append(DPScharts[0][-1] + self.deltaValue)
                            DPScharts[1].append(updatedPlayer.DPS)
                            damageChart[0].append(DPScharts[0][-1] + self.deltaValue)
                            damageChart[1].append(bufferDamage)
                        else:
                            if updatedPlayer.isPlayer:
                                self.DPSChart.update({updatedPlayer.name: [[self.deltaValue], [updatedPlayer.DPS]]})
                                self.damageChart.update({updatedPlayer.name: [[self.deltaValue], [bufferDamage]]})
                            else:
                                self.NPCDPSChart.update({updatedPlayer.name: [[self.deltaValue], [updatedPlayer.DPS]]})
                                self.NPCDamageChart.update({updatedPlayer.name: [[self.deltaValue], [bufferDamage]]})

                self.bufferedDamage = {}
            self.lastGraphTime = timer
            self.globalCombatEnd = self.timeToTimeAndDate(x[self.combatlogDict["date"]])



        self.getGlobalTime()
        for table in self.tableArray:
            table.globalStartTime, table.globalFinishTime, table.globalRunTime = self.globalCombatStart, self.globalCombatEnd, self.globalCombatTime
            table.setCombatTime(self.combatTimeRule)
            table.updateTables()
        if self.difficulty == None:
            self.detectDifficulty()
        print(len(self.tableArray), len(self.playerList), len(self.NPCs), len(self.playerdict))
    def detectDifficulty(self):
        for entity in self.tableArray:
            if entity.name in self.difficultyDetectionDict:
                difficultyDetectHolder = self.difficultyDetectionDict[entity.name]
                damageTaken = entity.totalDamageTaken
                if len(difficultyDetectHolder) == 1:  # Entity is used to set 1 difficulty
                    if damageTaken >= difficultyDetectHolder[0][0]:
                        self.difficulty = difficultyDetectHolder[0][1]
                    else:
                        pass  # invalid combat
                elif len(difficultyDetectHolder) == 2:  # enttity is used to set 2 diffuclties
                    if damageTaken >= difficultyDetectHolder[1][0]:
                        self.difficulty = difficultyDetectHolder[1][1]
                    elif damageTaken >= difficultyDetectHolder[0][0]:
                        self.difficulty = difficultyDetectHolder[0][1]
                    else:
                        pass  # invalid combat
                elif len(difficultyDetectHolder) == 3:
                    if damageTaken >= difficultyDetectHolder[2][0]:
                        self.difficulty = difficultyDetectHolder[2][1]
                    elif damageTaken >= difficultyDetectHolder[1][0]:
                        self.difficulty = difficultyDetectHolder[1][1]
                    elif damageTaken >= difficultyDetectHolder[0][0]:
                        self.difficulty = difficultyDetectHolder[0][1]
                    else:
                        pass  # invalid combat

    def detectCombat(self, IDString):
        if IDString in self.mapIdentifiers:
            map = self.mapIdentifiers[IDString]

            if map == "Infected_Space_Elite":  # add exceptions for all other maps that have unique entities to identify map difficulty
                self.map = "Infected_Space"
                self.difficulty = "Elite"
            else:  # set map
                self.map = map
            if self.map in self.checkSpaceMaps:
                self.isSpace = True
            else:
                self.isSpace = False
        else:  # entity not curcial to map identification
            pass

    def readCombat(self):
        combatID = 0
        newCombat = True
        combatDelta = datetime.timedelta(seconds=100)
        lastTime = None
        firstLine = True
        parsedLines = 0
        with open(self.path, "r") as file:
            start = timer.time()
            for line in file:
                splycedLine = line.split("::")
                if self.map == None:
                    IDcheck = splycedLine[1].split(",")
                    IDcheck = IDcheck[self.combatlogDict["targetID"] - 1]
                    wrapperUpdated = False
                    if not IDcheck == "*":
                        targetID = IDcheck.split(" ")
                        targetID = targetID[1].split("]")[0]
                        self.detectCombat(targetID)
                elif not wrapperUpdated:
                    timeHelper = [time.day, time.month, time.year, time.hour, time.minute, time.second]
                    tracker = 0
                    for timeHelp in timeHelper:
                        if timeHelp < 10:
                            timeHelper[tracker] = "0" + str(timeHelp)
                        tracker += 1
                    day, month, year, hour, minute, second = timeHelper
                    combatInformationWrapper = str(self.removeUnderscore(self.map)) + " " + str(day) + "/" + str(
                        month) + "/" + str(year) + " " + str(hour) + ":" + str(
                        minute) + ":" + str(second)
                    self.otherCombats.update({combatID: (newFile, combatInformationWrapper)})
                    wrapperUpdated = True
                    print(combatInformationWrapper)
                timeCheck = splycedLine[0]
                time = self.timeToTimeAndDate(timeCheck)
                if firstLine:
                    firstLine = False
                    lastTime = time
                combatLineDelta = time - lastTime
                lastTime = time
                if combatLineDelta > combatDelta:
                    if parsedLines < 2:
                        self.otherCombats.pop(combatID)
                        newCombat = True
                    else:
                        newCombat = True
                        combatID += 1
                    parsedLines = 0
                    wrapperUpdated = False
                if newCombat:
                    combatInformationWrapper = str(self.map) + " " + str(time.day) + "/" + str(time.month) + "/" + str(
                        time.year) + " " + str(time.hour) + ":" + str(time.minute) + ":" + str(time.second)

                    newFile = tempfile.NamedTemporaryFile(mode="w+", delete=True)
                    self.otherCombats.update({combatID: (newFile, combatInformationWrapper)})
                    newFile.write(line)
                    newCombat = False
                else:
                    tmpFile = self.otherCombats[combatID][0]
                    tmpFile.write(line)
                parsedLines += 1
        file = self.otherCombats[len(self.otherCombats) - 1][0]
        file.seek(0)
        lines = file.readlines()
        for line in lines:
            self.combatlog.append(line)
        self.combatLogAnalysis()
        lastTime = timer.time()
        run = lastTime - start
        print(run)

    def readPreviousCombat(self, combatID):
        self.softResetParser()
        file = self.otherCombats[combatID][0]
        file.seek(0)
        lines = file.readlines()
        for line in lines:
            self.combatlog.append(line)
        self.combatLogAnalysis()

    def readCombatFromTempfile(self, otherCombat):
        self.softResetParser()
        file = otherCombat[0]
        file.seek(0)
        lines = file.readlines()
        for line in lines:
            self.combatlog.append(line)
        self.combatLogAnalysis()

    def generatedUItables(self):
        for entity in self.tableArray:
            input = [entity.isPlayer, entity.dmgoutTable, entity.petDMGTable, entity.dmginTable, entity.healsOutTable,
                     entity.petHealsTable, entity.healsInTable]
            self.uiDictionary.update({entity.name: input})

    def returnUItables(self):
        self.generatedUItables()
        return self.uiDictionary, self.dmgTableIndex, self.healTableIndex, self.uiInputDictionary, self.otherCombats, self.map, self.difficulty, self.damageChart, self.DPSChart, self.NPCDamageChart, self.NPCDPSChart

    def readCombatwithUITables(self, path):
        self.setPath(path)
        self.readCombat()
        self.generatedUItables()
        return self.uiDictionary, self.dmgTableIndex, self.healTableIndex, self.uiInputDictionary, self.otherCombats, self.map, self.difficulty, self.damageChart, self.DPSChart, self.NPCDamageChart, self.NPCDPSChart

    def readPreviousCombatwithUITables(self, combatID):
        self.readPreviousCombat(combatID)
        self.generatedUItables()
        return self.uiDictionary, self.dmgTableIndex, self.healTableIndex, self.uiInputDictionary, self.otherCombats, self.map, self.difficulty, self.damageChart, self.DPSChart, self.NPCDamageChart, self.NPCDPSChart

    def readTempFileCombatwithUITables(self, otherCombat):
        self.readCombatFromTempfile(otherCombat)
        self.generatedUItables()
        return self.uiDictionary, self.dmgTableIndex, self.healTableIndex, self.uiInputDictionary, self.otherCombats, self.map, self.difficulty, self.damageChart, self.DPSChart, self.NPCDamageChart, self.NPCDPSChart


    def readCombatFull(self, path):
        self.resetParser()
        self.depthAnalysis = True
        self.setPath(path)
        self.readCombat()
        self.generatedUItables()
        return self.uiDictionary, self.dmgTableIndex, self.healTableIndex, self.uiInputDictionary, self.otherCombats, self.map, self.difficulty, self.damageChart, self.DPSChart, self.NPCDamageChart, self.NPCDPSChart

    def readCombatShallow(self, path):
        self.resetParser()
        self.depthAnalysis = False
        self.setPath(path)
        self.readCombat()
        return self.otherCombats, self.map, self.difficulty, self.damageChart, self.DPSChart, self.NPCDamageChart, self.NPCDPSChart

    def readPreviousCombatFull(self, combatID):
        self.resetParser()
        self.depthAnalysis = True
        self.readPreviousCombat(combatID)
        self.generatedUItables()
        return self.uiDictionary, self.dmgTableIndex, self.healTableIndex, self.uiInputDictionary, self.otherCombats, self.map, self.difficulty, self.damageChart, self.DPSChart, self.NPCDamageChart, self.NPCDPSChart


    def readPreviousCombatShallow(self, combatID):
        self.resetParser()
        self.depthAnalysis = False
        self.readPreviousCombat(combatID)
        return self.otherCombats, self.map, self.difficulty, self.damageChart, self.DPSChart, self.NPCDamageChart, self.NPCDPSChart


    def readTempFileCombatFull(self, otherCombat):
        self.resetParser()
        self.depthAnalysis = True
        self.readCombatFromTempfile(otherCombat)
        self.generatedUItables()
        return self.uiDictionary, self.dmgTableIndex, self.healTableIndex, self.uiInputDictionary, self.otherCombats, self.map, self.difficulty, self.damageChart, self.DPSChart, self.NPCDamageChart, self.NPCDPSChart


    def readTempFileCombatShallow(self, otherCombat):
        self.resetParser()
        self.depthAnalysis = False
        self.readCombatFromTempfile(otherCombat)
        return  self.otherCombats, self.map, self.difficulty, self.damageChart, self.DPSChart, self.NPCDamageChart, self.NPCDPSChart


    def reReadCombatFull(self):
        self.resetParser()
        self.depthAnalysis = True
        self.combatLogAnalysis()
        self.generatedUItables()
        return self.uiDictionary, self.dmgTableIndex, self.healTableIndex, self.uiInputDictionary, self.otherCombats, self.map, self.difficulty, self.damageChart, self.DPSChart, self.NPCDamageChart, self.NPCDPSChart

    def realTimeParser(self):
        startline = None
        tempLine = 0
        playerDict = {}
        startTime = None
        # lineOffset = []
        # offset = 0
        print("realtime Parser")
        running = True
        while running:
            if startline == None:
                with open(self.path, "r") as file:
                    for line in file:
                        # lineOffset.append(offset)
                        # offset += len(line)
                        splycedLine = line.split("::")
                        time = self.timeToTimeAndDate(splycedLine[0])
                        now = datetime.datetime.now()
                        delta = datetime.timedelta(seconds=1)
                        if now - time < delta:
                            startline = line
                            startTime = time
                            print("test")
                            print(startline)
                            break
            else:
                # print("running")
                foundStart = False
                with open(self.path, "r") as file:
                    for line in file:
                        if line == startline:
                            foundStart = True
                        if foundStart:
                            final = []
                            splicer1 = line.split("::")
                            final.append(splicer1[0])
                            splicer11 = splicer1[1]
                            splicer2 = splicer11.split(",")
                            for y in splicer2:
                                if y == "":
                                    y = "*"
                                final.append(y)
                            line = final
                            time = self.timeToTimeAndDate(line[self.combatlogDict["date"]])
                            mag1 = float(line[self.combatlogDict["mag1"]])
                            mag2 = float(line[self.combatlogDict["mag2"]])
                            if (line[self.combatlogDict["dmageType"]] == "Shield" and mag1 < 0 and mag2 >= 0) or line[
                                self.combatlogDict["dmageType"]] == "HitPoints":
                                pass
                            else:
                                if mag1 < 0:
                                    mag1 *= -1
                                if line[self.combatlogDict["ID"]] in playerDict:
                                    playerDict[line[self.combatlogDict["ID"]]][0] += mag1

                                else:
                                    if line[self.combatlogDict["ID"]][0] == "P":
                                        playerDict.update({line[self.combatlogDict["ID"]]: [mag1, 0]})
                                    else:
                                        pass
                                combatTime = (time - startTime).total_seconds()
                                if combatTime == 0:
                                    combatTime = 1
                                for player in playerDict:
                                    playerDict[player][1] = playerDict[player][0] / combatTime
                                    print(player, playerDict[player][1])
                            timer.sleep(0.5)

    def generateFrontPageTable(self):  # generates the front page table with a quick summary of combat stats
        self.endTable.append(
            ["player", "combatTime", "DPS", "Total Damage", "CritH", "MaxOneHit", "%debuff", "%damage", "%damage taken",
             "%atks-in", "total heals", "healCrtH" ,"% healed", "deaths"])
        temptable = []
        totalDamage = 0
        totalTaken = 0
        totalAtks = 0
        totalHeals = 0
        for player in self.tableArray:
            if player.isPlayer:
                totalDamage += player.totaldamage
                totalTaken += player.totalDamageTaken
                totalAtks += player.totalAttacksTaken
                totalHeals += player.totalHeals
                if totalDamage == 0:
                    totalDamage += 1
                if totalTaken == 0:
                    totalTaken += 1
                if totalAtks == 0:
                    totalAtks += 1
                if totalHeals == 0:
                    totalHeals += 1

        for player in self.tableArray:
            if player.isPlayer:
                percentageDamage = player.totaldamage / totalDamage * 100
                percentageATS = player.totalAttacksTaken / totalAtks * 100
                percentageTaken = player.totalDamageTaken / totalTaken * 100
                percentageHeals = player.totalHeals / totalHeals * 100
                handle = self.generateHandle(player.name)
                temp = [handle, player.totalTime, player.DPS, player.totaldamage, player.crtH, player.maxOneHit,
                        player.finalresist, percentageDamage, percentageTaken, percentageATS, player.totalHeals, player.healCrtH,
                        percentageHeals, player.deaths]
                temptable.append(temp)
                player.dmgPercentage = percentageDamage
                player.ATKSpMin = round(player.totalAttacksTaken / player.runtime, 2)
                player.ATKSinPercentage = percentageATS
                player.percentageTaken = percentageTaken
                player.percentageHealed = percentageHeals

        temptable.sort(key=lambda x: x[2], reverse=True)
        for row in temptable:
            self.endTable.append(row)

    def createFrontPageTable(self):
        self.generateFrontPageTable()
        return self.endTable

    def generalStatsCopy(self):
        playerArray = []
        returnString = "OSCR - "
        if self.map == None:
            map = "UNKWN"
        else:
            map = self.queueToAbreviation[self.map]
        if self.difficulty == None:
            map = map + "X"
        else:
            map = map + self.difficultyToAbreviation[self.difficulty]
        if self.isSpace:
            map = map + "(S) - "
        else:
            map = map + "(G) - "
        combatTime = 0
        for player in self.tableArray:
            if player.isPlayer:
                handle = self.generateHandle(player.name)
                handle = handle.split("@")
                handle = "@" + handle[1]
                dmg = self.rounder(player.totaldamage)
                dps = self.rounder(player.DPS)
                dmg = dmg.split(",")
                dps = dps.split(",")
                if len(dmg) == 2:
                    dmg = str(dmg[0]) + "," + str(dmg[1])[0:1] + "K"
                elif len(dmg) == 3:
                    dmg = str(dmg[0]) + "," + str(dmg[1])[0:1] + "M"
                elif len(dmg) > 3:
                    dmg = str(dmg[0]) + "," + str(dmg[1])[0:1] + "B"

                if len(dps) == 2:
                    dps = str(dps[0]) + "," + str(dps[1])[0:1] + "K"
                elif len(dps) == 3:
                    dps = str(dps[0]) + "," + str(dps[1])[0:1] + "M"
                elif len(dps) > 3:
                    dps = str(dps[0]) + "," + str(dps[1])[0:1] + "B"
                if handle == int and dmg == int and dps == int:
                    playerArray.append([handle, dmg, dps])
                if player.runtime > combatTime:
                    combatTime = player.runtime
        temp = datetime.timedelta(seconds=combatTime)
        if temp > datetime.timedelta(minutes=1):
            seconds = temp.seconds
            minutes = seconds // 60
            seconds = seconds - (60 * minutes)
            if seconds < 10:
                seconds = "0" + str(seconds)
            if minutes < 10:
                minutes = "0" + str(minutes)
            map = map + "[" + str(minutes) + ":" + str(seconds) + "." + str(temp.seconds)[0] + "] DMG(DPS) - "
        else:
            map = map + "[0:" + str(temp.seconds) + "." + str(temp.seconds)[0] + "] DMG(DPS) - "
        print(playerArray)
        playerArray.sort(key=lambda row: row[2], reverse=True)
        mapCopy = map
        for playerinstance in playerArray:
            map = map + playerinstance[0] + ": " + str(playerinstance[1]) + "(" + str(playerinstance[2]) + ") "
            if len(map) > 200:
                map = mapCopy + playerinstance[0][0:8] + ": " + str(playerinstance[1]) + "(" + str(
                    playerinstance[2]) + ") "
                if len(map) > 200:
                    map = mapCopy + playerinstance[0][0:6] + ": " + str(playerinstance[1]) + "(" + str(
                        playerinstance[2]) + ") "
                    if len(map) > 200:
                        map = mapCopy + playerinstance[0][0:4] + ": " + str(playerinstance[1]) + "(" + str(
                            playerinstance[2]) + ") "

        returnString = returnString + map
        return returnString

    def getStatsCopy(self, wantedStat, playerID):
        handle = self.generateHandle(playerID)
        player = self.tableArray[self.playerdict[playerID]]
        returnString = "OSCR - "
        if self.map == None:
            map = "UNKWN"
        else:
            map = self.queueToAbreviation[self.map]
        if self.difficulty == None:
            map = map + "X"
        else:
            map = map + self.difficultyToAbreviation[self.difficulty]
        if self.isSpace:
            map = map + "(S) - "
        else:
            map = map + "(G) - "
        returnString = returnString + map
        returnString = returnString + handle + " - "
        if wantedStat == "MaxOneHit":
            returnString = returnString + "Max One-Hit: " + str(player.maxOneHit) + " (" + str(
                player.maxOneHitWeapon) + ")"
        elif wantedStat == "dmgOut":
            returnString = returnString + "DMG out: " + str(self.rounder(player.totaldamage)) + " DPS: " + str(
                self.rounder(player.DPS)) + " (" + str(round(player.dmgPercentage, 1)) + "% of team)"
        elif wantedStat == "ATKS-in":
            returnString = returnString + "ATKS-in: " + str(player.totalAttacksTaken) + " ATPS " + str(
                self.rounder(player.ATKSpMin)) + " (" + str(round(player.ATKSinPercentage, 1)) + "% of team)"
        elif wantedStat == "Heal-Out":
            returnString = returnString + "Heal out: " + str(self.rounder(player.totalHeals)) + " HPS: " + str(
                self.rounder(player.HPS)) + " (" + str(round(player.percentageHealed, 1)) + "% of team)"
        elif wantedStat == "MaxOneHeal":
            returnString = returnString + "Max One-Heal: " + str(player.maxOneHeal) + " (" + str(
                player.maxOneHealWeapon) + ")"
        else:
            return "keyError"
        return returnString

    def getSpecificGraph(self, playerID, targetCatagory, Target, isDamageGraph):
        # keys: pet, petID, targetID, self.source, petSum
        # IF USING IT FOR A GRAPH ON TARGETID, SUPPLY A TUPLE/ARRAY WITH [self.source/weapon, targetID]!!!!
        # isDamageGraph = True means damage dealt or healing done in interval, isDamageGraph = False = DPS/HPS
        lastTime = None
        firstTime = None
        returnArray = [[], []]
        firstLine = True
        damagePlaceHolder = 0
        bufferDamage = 0

        if targetCatagory == "pet" or targetCatagory == "petID" or targetCatagory[
            1] == "targetID" or targetCatagory == "source" or targetCatagory == "petSum":
            for line in self.splicedCombatlog:
                time = line[self.combatlogDict["date"]]
                time = self.timeToTimeAndDate(time)
                damage = float(line[self.combatlogDict["mag1"]])
                if damage < 0:
                    damage *= -1
                if firstLine:
                    firstTime = time
                    firstLine = False
                if lastTime == None:
                    lastTime = time
                if line[self.combatlogDict["ID"]] == playerID:
                    if (line[self.combatlogDict[targetCatagory]] == Target and (
                            targetCatagory == "pet" or targetCatagory == "petID" or targetCatagory == "source")) or (
                            line[self.combatlogDict["petID"]] != "*" and targetCatagory == "petSum") or (
                            line[self.combatlogDict["source"]] == Target[0] and line[
                        self.combatlogDict["targetID"]] == Target[1]):
                        if isDamageGraph:
                            bufferDamage += damage
                        else:
                            damagePlaceHolder += damage
                if time - lastTime >= self.graphDelta:
                    if isDamageGraph:
                        if len(returnArray[0]) == 0:
                            returnArray[0].append(self.deltaValue)
                            returnArray[1].append(bufferDamage)
                            bufferDamage = 0
                        else:
                            returnArray[0].append(self.deltaValue + returnArray[0][-1])
                            returnArray[1].append(bufferDamage)
                            bufferDamage = 0
                    else:
                        if len(returnArray[0]) == 0:
                            returnArray[0].append(self.deltaValue)
                            returnArray[1].append(damagePlaceHolder)
                        else:
                            timer = (time - firstTime).total_seconds()
                            DPS = damagePlaceHolder / timer
                            returnArray[0].append(self.deltaValue + returnArray[0][-1])
                            returnArray[1].append(DPS)
                    lastTime = time

            return returnArray
        else:
            return "keyError"







def main():
    path = "multiplelogtest.txt"
    parserInstance = parser()
    parserInstance.setPath(path)
    # parserInstance.realTimeParser()
    results = parserInstance.readCombatShallow(path)
    table = parserInstance.createFrontPageTable()
    print(table)

    for player in parserInstance.tableArray:
        if player.isPlayer:
            graph = parserInstance.getStatsCopy("ATKS-in", player.name)
            print(graph)
    for row in table:
        print(row)




if __name__ == '__main__':
    main()
