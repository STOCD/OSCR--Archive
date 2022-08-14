import datetime
import tempfile
from decimal import Decimal
import time as timer

class players:          #main container class, used for saving stats on all entities
    def __init__(self, name, isPlayer, time):
        self.isPlayer = isPlayer
        self.combatOver = False
        self.name = name
        self.dmgoutindex = {"name": 0, "target": 1, "damage": 2, "DPS": 3, "maxHit": 4, "crits": 5, "flanks": 6, "attacks": 7, "misses": 8, "CrtH": 9, "acc": 10, "flankrate": 11, "kills": 12, "hulldamage": 13, "shielddamage": 14, "resist": 15, "hullAttacks": 16, "finalResist": 17}
        self.healOutIndex = {"name": 0, "target": 1, "healtotal": 2, "HPS": 3, "hullheal": 4, "shieldheal": 5, "maxHeal": 6, "Crits": 7, "healticks": 8, "CrtH": 9 }
        self.dmgoutTable = []
        self.dmgoutDict = {}
        self.petDMGTable = []
        self.petSourceDict = {}
        self.petSourceIDDict = {}
        self.petWeaponDict = {}
        self.petTargetDict = {}
        self.healsInDict = {}
        self.healsOutDict = {}
        self.petHealSourceDict = {}
        self.petHealsIDDict = {}
        self.petAbilityDict = {}
        self.petHealTargetDict = {}
        self.dmginTable = []    #to be added
        self.dmgInDict = {}     #to be added
        self.healsOutTable = [] #to be added
        self.healsInTable = []  #to be added
        self.petHealsTable = []
        self.totaldamage = 0
        self.totalAttacks = 0
        self.totalCrits = 0
        self.totalHeals = 0
        self.totalDamageTaken = 0
        self.totalAttacksTaken = 0
        self.deaths = 0
        self.maxOneHit = 0
        self.DPS = 0
        self.crtH = 0
        self.startTime = time
        self.totalTime = 0
        self.flanks = 0
        self.misses = 0
        self.kills = 0
        self.runtime = 0
        self.endTime = 0
        self.finishTime = 0
        self.acc = 0
        self.resist = 0
        self.hullAttacks = 0
        self.finalresist = 0

    def updateStats(self, time2):
        self.temptotalAttacks = self.totalAttacks - self.misses
        self.totalTime = (time2 - self.startTime).total_seconds()
        self.runtime = self.totalTime
        self.endTime = time2
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

    def updateTables(self):
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


class parser:
    def __init__(self):
        self.path = ""
        self.combatlog = []
        self.playerdict = {}
        self.playerList = []
        self.NPCs = []
        self.tableArray = []
        self.otherCombats = {}
        self.graphDelta = datetime.timedelta(milliseconds=200)
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
        self.DPSChart = {}

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

        self.checkSpaceMaps = ["Infected_Space", "Azure_Nebula", "Battle_At_The_Binary_Stars", "Borg_Disconnected", "Counterpoint", "Crystalline_Entity",
                               "Gateway_To_Grethor", "Herald_Sphere", "Operation_Riposte", "Cure_Found", "Days_Of_Doom", "Dranuur_Gauntlet", "Khitomer_space",
                               "Storming_The_Spire", "Swarm", "To_Hell_With_Honor", "Gravity_Kills", "Hive_Space", "Best_Served_Cold"]

        self.isSpace = True

        self.endTable = []


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
    def setPath(self, path):
        self.path = path
    def createTableInstance(self, line):  # creates a new class instance and appends to list
        if line[self.combatlogDict["ID"]][0] == "P":
            player = True
        else:
            player = False
        ID = line[self.combatlogDict["ID"]]
        if player:
            self.tableArray.append(players(ID, True, self.timeToTimeAndDate(line[self.combatlogDict["date"]])))
            self.playerdict.update({ID: self.counter2})
            self.counter2 += 1
        else:
            self.tableArray.append(players(ID, False, self.timeToTimeAndDate(line[self.combatlogDict["date"]])))
            self.playerdict.update({ID: self.counter2})
            self.counter2 += 1

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

    def generateHandle(self, IDSplyce):  # returns player handle, can further splice this for only @xxxx or character name.
        IDSplyce = IDSplyce.split(" ", 1)
        IDSplyce = IDSplyce[1]
        IDSplyce = IDSplyce[:-1]
        return IDSplyce

    def generateID(self, IDSplyce):  # returns player ID (not necessary if necessary, might be removed down the road if unnecessary
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

    def combatLogAnalysis(self):
        for x in self.combatlog:
            final = []
            splicer1 = x.split("::")
            final.append(splicer1[0])
            splicer11 = splicer1[1]
            splicer2 = splicer11.split(",")
            for y in splicer2:
                if y == "":
                    y="*"
                final.append(y)
            x = final
            if not x[self.combatlogDict["ID"]] in self.playerList:
                if x[self.combatlogDict["ID"]][0] == "P":
                    self.playerList.append(x[self.combatlogDict["ID"]])
                    self.createTableInstance(x)
                elif not [x[self.combatlogDict["character"]], x[self.combatlogDict["ID"]]] in self.NPCs:
                    self.NPCs.append(x[self.combatlogDict["ID"]])
                    self.createTableInstance(x)

            self.splicedCombatlog.append(x)
            # if not x[combatlogDict["targetID"]] in templist and x[combatlogDict["sourceID"]] == "P[12231228@5044720 CasualSAB@spencerb96]":
            #     templist.append(x[combatlogDict["targetID"]])
            #     print("adsfaf", x[combatlogDict["targetID"]])

            attacker = self.tableArray[self.playerdict[x[self.combatlogDict["ID"]]]]

            # flag updater
            isCrit, isMiss, isFlank, isKill = self.getFlags(x[self.combatlogDict["flags"]])
            if isMiss:
                attacker.misses += 1
            if isCrit:
                attacker.totalCrits += 1
            if isFlank:
                attacker.flanks = attacker.flanks + 1
            if isKill:
                attacker.kills += 1
                if x[self.combatlogDict["targetID"]] in self.playerdict:
                    self.tableArray[self.playerdict[x[self.combatlogDict["targetID"]]]].deaths += 1

            # attacker = players("name", True, None)
            damage1 = float(x[self.combatlogDict["mag1"]])
            damage2 = float(x[self.combatlogDict["mag2"]])
            damagetype = x[self.combatlogDict["dmageType"]]

            #Heals
            if (damagetype == "Shield" and damage1 < 0 and damage2 >= 0) or damagetype == "HitPoints":
                if damage1 < 0:
                    damage1 *= -1
                attacker.totalHeals += damage1
                if damagetype == "Hitpoints":
                    shieldHeal = 0
                    hullHeal = damage1
                else:
                    shieldHeal = damage1
                    hullHeal = 0
                source = x[self.combatlogDict["source"]]
                target = x[self.combatlogDict["targetID"]]
                if x[self.combatlogDict["targetID"]] in self.playerList:
                    damaged = self.tableArray[self.playerdict[x[self.combatlogDict["targetID"]]]]
                else:
                    damaged = players("name", False, None)

                #non pet heals
                if x[self.combatlogDict["pet"]] == "*" or x[self.combatlogDict["targetID"]] == "*":
                    if source in attacker.healsOutDict:
                        newTarget = True
                        for col in attacker.healsOutTable[attacker.healsOutDict[source]]:
                            if col[attacker.healOutIndex["target"]] == target:
                                newTarget = False
                                attacker.healsOutTable[attacker.healsOutDict[source]][0][
                                    attacker.healOutIndex["healtotal"]] += damage1
                                attacker.healsOutTable[attacker.healsOutDict[source]][0][
                                    attacker.healOutIndex["hullheal"]] += hullHeal
                                attacker.healsOutTable[attacker.healsOutDict[source]][0][
                                    attacker.healOutIndex["shieldheal"]] += shieldHeal
                                if not source in self.exculdedHealTicks:
                                    attacker.healsOutTable[attacker.healsOutDict[source]][0][
                                        attacker.healOutIndex["healticks"]] += 1
                                    col[attacker.healOutIndex["healticks"]] += 1
                                col[attacker.healOutIndex["healtotal"]] += damage1
                                col[attacker.healOutIndex["hullheal"]] += hullHeal
                                col[attacker.healOutIndex["shieldheal"]] += shieldHeal
                                if damage1 > attacker.healsOutTable[attacker.healsOutDict[source]][0][
                                    attacker.healOutIndex["maxHeal"]]:
                                    attacker.healsOutTable[attacker.healsOutDict[source]][0][
                                        attacker.healOutIndex["maxHeal"]] = damage1
                                if damage1 > col[attacker.healOutIndex["maxHeal"]]:
                                    col[attacker.healOutIndex["maxHeal"]] = damage1
                                if isCrit:
                                    attacker.healsOutTable[attacker.healsOutDict[source]][0][attacker.healOutIndex["Crits"]] += 1
                                    col[attacker.healOutIndex["Crits"]] += 1
                        if newTarget:
                            attacker.healsOutTable[attacker.healsOutDict[source]].append(
                                [source, target, damage1, 0, hullHeal, shieldHeal, damage1, (1 if isCrit else 0), 1, 0])
                            attacker.healsOutTable[attacker.healsOutDict[source]][0][attacker.healOutIndex["healtotal"]] += damage1
                            attacker.healsOutTable[attacker.healsOutDict[source]][0][
                                attacker.healOutIndex["hullheal"]] += hullHeal
                            attacker.healsOutTable[attacker.healsOutDict[source]][0][
                                attacker.healOutIndex["shieldheal"]] += shieldHeal
                            if not source in self.exculdedHealTicks:
                                attacker.healsOutTable[attacker.healsOutDict[source]][0][attacker.healOutIndex["healticks"]] += 1
                            if damage1 > attacker.healsOutTable[attacker.healsOutDict[source]][0][
                                attacker.healOutIndex["maxHeal"]]:
                                attacker.healsOutTable[attacker.healsOutDict[source]][0][
                                    attacker.healOutIndex["maxHeal"]] = damage1
                            if isCrit:
                                attacker.healsOutTable[attacker.healsOutDict[source]][0][attacker.healOutIndex["Crits"]] += 1
                    else:
                        attacker.healsOutTable.append([
                            [source, target, damage1, 0, hullHeal, shieldHeal, damage1, (1 if isCrit else 0), 1, 0],
                            [source, target, damage1, 0, hullHeal, shieldHeal, damage1, (1 if isCrit else 0), 1, 0]])
                        attacker.healsOutDict.update({source: len(attacker.healsOutTable) - 1})

                    #heals out
                    dmgOutSource = x[self.combatlogDict["ID"]]
                    if dmgOutSource in damaged.healsInTable:
                        newTargeted = True
                        for col in damaged.healsInTable[damaged.healsInDict[dmgOutSource]]:
                            if col[damaged.healOutIndex["target"]] == source:
                                newTargeted = False
                                damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][attacker.healOutIndex["healtotal"]] += damage1
                                damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][attacker.healOutIndex["hullheal"]] += hullHeal
                                damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][attacker.healOutIndex["shieldheal"]] += shieldHeal
                                if not source in self.exculdedHealTicks:
                                    damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][attacker.healsInDict["healticks"]] += 1
                                    col[attacker.healsInDict["healticks"]] += 1
                                col[attacker.healOutIndex["healtotal"]] += damage1
                                col[attacker.healOutIndex["hullheal"]] += hullHeal
                                col[attacker.healOutIndex["shieldheal"]] += shieldHeal

                                if damage1 > damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][attacker.healOutIndex["maxHeal"]]:
                                    damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][attacker.healOutIndex["maxHeal"]] = damage1
                                if damage1 > col[attacker.healOutIndex["maxHeal"]]:
                                    col[attacker.healOutIndex["maxHeal"]] = damage1
                                if isCrit:
                                    damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][attacker.healOutIndex["Crits"]] += 1
                                    col[attacker.healOutIndex["Crits"]] += 1
                        if newTargeted:
                            damaged.healsInTable[damaged.healsInDict[dmgOutSource]].append(
                                [source, target, damage1, 0, hullHeal, shieldHeal, damage1, (1 if isCrit else 0), 1, 0])
                            damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][attacker.healOutIndex["healtotal"]] += damage1
                            damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][attacker.healOutIndex["hullheal"]] += hullHeal
                            damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][attacker.healOutIndex["shieldheal"]] += shieldHeal
                            if not source in self.exculdedHealTicks:
                                damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][attacker.healOutIndex["healticks"]] += 1
                            if damage1 > damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][attacker.healOutIndex["maxHeal"]]:
                                damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][attacker.healOutIndex["maxHeal"]] = damage1
                            if isCrit:
                                damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][attacker.healOutIndex["Crits"]] += 1
                    else:
                        damaged.healsInTable.append([
                            [source, target, damage1, 0, hullHeal, shieldHeal, damage1, (1 if isCrit else 0), 1, 0],
                            [source, target, damage1, 0, hullHeal, shieldHeal, damage1, (1 if isCrit else 0), 1, 0]])
                        damaged.dmgInDict.update({dmgOutSource: len(attacker.dmgoutTable) - 1})






                #pet heals
                else:
                    source = x[self.combatlogDict["pet"]]
                    sourceIDtmp = x[self.combatlogDict["petID"]]
                    ability = x[self.combatlogDict["source"]]
                    target = x[self.combatlogDict["targetID"]]
                    dmgOutSource = x[self.combatlogDict["ID"]]
                    sourceID = source + sourceIDtmp
                    abilityID = sourceID + ability
                    targetID = sourceID + ability + target


                    if dmgOutSource in damaged.healsInTable:
                        newTargeted = True
                        for col in damaged.healsInTable[damaged.healsInDict[dmgOutSource]]:
                            if col[damaged.healOutIndex["target"]] == source:
                                newTargeted = False
                                damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][
                                    attacker.healOutIndex["healtotal"]] += damage1
                                damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][
                                    attacker.healOutIndex["hullheal"]] += hullHeal
                                damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][
                                    attacker.healOutIndex["shieldheal"]] += shieldHeal
                                if not source in self.exculdedHealTicks:
                                    damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][
                                        attacker.healsInDict["healticks"]] += 1
                                    col[attacker.healsInDict["healticks"]] += 1
                                col[attacker.healOutIndex["healtotal"]] += damage1
                                col[attacker.healOutIndex["hullheal"]] += hullHeal
                                col[attacker.healOutIndex["shieldheal"]] += shieldHeal

                                if damage1 > damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][
                                    attacker.healOutIndex["maxHeal"]]:
                                    damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][
                                        attacker.healOutIndex["maxHeal"]] = damage1
                                if damage1 > col[attacker.healOutIndex["maxHeal"]]:
                                    col[attacker.healOutIndex["maxHeal"]] = damage1
                                if isCrit:
                                    damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][
                                        attacker.healOutIndex["Crits"]] += 1
                                    col[attacker.healOutIndex["Crits"]] += 1
                        if newTargeted:
                            damaged.healsInTable[damaged.healsInDict[dmgOutSource]].append(
                                [source, target, damage1, 0, hullHeal, shieldHeal, damage1, (1 if isCrit else 0), 1, 0])
                            damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][
                                attacker.healOutIndex["healtotal"]] += damage1
                            damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][
                                attacker.healOutIndex["hullheal"]] += hullHeal
                            damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][
                                attacker.healOutIndex["shieldheal"]] += shieldHeal
                            if not source in self.exculdedHealTicks:
                                damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][
                                    attacker.healOutIndex["healticks"]] += 1
                            if damage1 > damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][
                                attacker.healOutIndex["maxHeal"]]:
                                damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][
                                    attacker.healOutIndex["maxHeal"]] = damage1
                            if isCrit:
                                damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][
                                    attacker.healOutIndex["Crits"]] += 1
                    else:
                        damaged.healsInTable.append([
                            [source, target, damage1, 0, hullHeal, shieldHeal, damage1, (1 if isCrit else 0), 1, 0],
                            [source, target, damage1, 0, hullHeal, shieldHeal, damage1, (1 if isCrit else 0), 1, 0]])
                        damaged.dmgInDict.update({dmgOutSource: len(attacker.dmgoutTable) - 1})

                    attacker = players(" ", " ", " ")
                    if source in attacker.petHealSourceDict:
                        attacker.petHealsTable[attacker.petHealSourceDict[source]][0][
                            attacker.healOutIndex["healtotal"]] += damage1
                        attacker.petHealsTable[attacker.petHealSourceDict[source]][0][
                            attacker.healOutIndex["hullheal"]] += hullHeal
                        attacker.petHealsTable[attacker.petHealSourceDict[source]][0][
                            attacker.healOutIndex["shieldheal"]] += shieldHeal
                        if not ability in self.exculdedHealTicks:
                            attacker.petHealsTable[attacker.petHealSourceDict[source]][0][
                                attacker.healOutIndex["healticks"]] += 1
                        if damage1 > attacker.petHealsTable[attacker.petHealSourceDict[source]][0][
                            attacker.healOutIndex["maxHeal"]]:
                            attacker.petHealsTable[attacker.petHealSourceDict[source]][0][
                                attacker.healOutIndex["maxHeal"]] = damage1
                        if isCrit:
                            attacker.petHealsTable[attacker.petHealSourceDict[source]][0][
                                attacker.healOutIndex["Crits"]] += 1


                        if sourceID in attacker.petHealsIDDict:
                            #updateing stats of pet instance
                            attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][0][
                                attacker.healOutIndex["healtotal"]] += damage1
                            attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][0][
                                attacker.healOutIndex["hullheal"]] += hullHeal
                            attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][0][
                                attacker.healOutIndex["shieldheal"]] += shieldHeal
                            if not ability in self.exculdedHealTicks:
                                attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][0][
                                    attacker.healOutIndex["healticks"]] += 1
                            if damage1 > attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][0][
                                attacker.healOutIndex["maxHeal"]]:
                                attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][0][
                                    attacker.healOutIndex["maxHeal"]] = damage1
                            if isCrit:
                                attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][0][
                                    attacker.healOutIndex["Crits"]] += 1

                                #check if weapon for pet exists
                            if abilityID in attacker.petAbilityDict:
                                #update stats
                                attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][attacker.petAbilityDict[abilityID]][0][attacker.healOutIndex["healtotal"]] += damage1
                                attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][attacker.petAbilityDict[abilityID]][0][attacker.healOutIndex["hullheal"]] += hullHeal
                                attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][attacker.petAbilityDict[abilityID]][0][attacker.healOutIndex["shieldheal"]] += shieldHeal
                                if not ability in self.exculdedHealTicks:
                                    attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][attacker.petAbilityDict[abilityID]][0][attacker.healOutIndex["healticks"]] += 1
                                if damage1 > attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][attacker.petAbilityDict[abilityID]][0][attacker.healOutIndex["maxHeal"]]:
                                    attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][attacker.petAbilityDict[abilityID]][0][attacker.healOutIndex["maxHeal"]] = damage1
                                if isCrit:
                                    attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][attacker.petAbilityDict[abilityID]][0][attacker.healOutIndex["Crits"]] += 1

                                if targetID in attacker.petHealTargetDict:
                                    attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][attacker.petAbilityDict[abilityID]][attacker.petHealTargetDict[targetID]][attacker.healOutIndex["healtotal"]] += damage1
                                    attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][attacker.petAbilityDict[abilityID]][attacker.petHealTargetDict[targetID]][attacker.healOutIndex["hullheal"]] += hullHeal
                                    attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][attacker.petAbilityDict[abilityID]][attacker.petHealTargetDict[targetID]][attacker.healOutIndex["shieldheal"]] += shieldHeal
                                    if not ability in self.exculdedHealTicks:
                                        attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][attacker.petAbilityDict[abilityID]][attacker.petHealTargetDict[targetID]][attacker.healOutIndex["healticks"]] += 1
                                    if damage1 > attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][attacker.petAbilityDict[abilityID]][attacker.petHealTargetDict[targetID]][attacker.healOutIndex["maxHeal"]]:
                                        attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][attacker.petAbilityDict[abilityID]][attacker.petHealTargetDict[targetID]][attacker.healOutIndex["maxHeal"]] = damage1
                                    if isCrit:
                                        attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][attacker.petAbilityDict[abilityID]][attacker.petHealTargetDict[targetID]][attacker.healOutIndex["Crits"]] += 1

                                else: #adding a new target that's healed
                                    attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][attacker.petAbilityDict[abilityID]].append(
                                        [target, "global", damage1, 0, hullHeal, shieldHeal, damage1, (1 if isCrit else 0), 1, 0])
                                    attacker.petHealTargetDict.update({targetID: len(attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][attacker.petAbilityDict[abilityID]])-1})

                            else:
                                #adding new heal ability instance
                                attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]].append([[ability, "global", damage1, 0, hullHeal, shieldHeal, damage1, (1 if isCrit else 0), 1, 0], [target, "global", damage1, 0, hullHeal, shieldHeal, damage1, (1 if isCrit else 0), 1, 0]])
                                attacker.petAbilityDict.update({abilityID: len(attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]])-1})
                                attacker.petHealTargetDict.update({targetID: len(attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][attacker.petAbilityDict[abilityID]])-1})


                        else:
                            #adding a new unique pet to a type of pet
                            attacker.petHealsTable[attacker.petHealSourceDict[source]].append([[sourceID, "global", damage1, 0, hullHeal, shieldHeal, damage1, (1 if isCrit else 0), 1, 0], [[ability, "global", damage1, 0, hullHeal, shieldHeal, damage1, (1 if isCrit else 0), 1, 0], [target, "global", damage1, 0, hullHeal, shieldHeal, damage1, (1 if isCrit else 0), 1, 0]]])
                            attacker.petHealsIDDict.update({sourceID: len(attacker.petHealsTable[attacker.petHealSourceDict[source]])-1})
                            attacker.petAbilityDict.update({abilityID: len(attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]])-1})
                            attacker.petHealTargetDict.update({targetID: len(attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][attacker.petAbilityDict[abilityID]])-1})

                    else:
                        #adding a new pet type
                        attacker.petHealsTable.append([[source, "global", damage1, 0, hullHeal, shieldHeal, damage1, (1 if isCrit else 0), 1, 0], [[sourceID, "global", damage1, 0, hullHeal, shieldHeal, damage1, (1 if isCrit else 0), 1, 0], [[ability, "global", damage1, 0, hullHeal, shieldHeal, damage1, (1 if isCrit else 0), 1, 0], [target, "global", damage1, 0, hullHeal, shieldHeal, damage1, (1 if isCrit else 0), 1, 0]]]])
                        attacker.petHealSourceDict.update({source: len(attacker.petHealsTable)-1})
                        attacker.petHealsIDDict.update({sourceID: len(attacker.petHealsTable[attacker.petHealSourceDict[source]])-1})
                        attacker.petAbilityDict.update({abilityID: len(attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]])-1})
                        attacker.petHealTargetDict.update({targetID: len(attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][attacker.petAbilityDict[abilityID]])-1})



            elif x[self.combatlogDict["source"]] == "Warp Core Breach":
                if self.warpCoreBreach == None:
                    self.warpCoreBreach = players("WarpCoreBreach", False, self.timeToTimeAndDate(x[self.combatlogDict["date"]]))
                #Do something for WCB damage tracking
                pass

            #Non pets
            elif (x[self.combatlogDict["pet"]] == "*" or x[self.combatlogDict["targetID"]] == "*") and damagetype != "HitPoints":
                if not x[self.combatlogDict["source"]] in self.excludeDamage:
                    if not ((x[self.combatlogDict["targetID"]] in self.playerList) and (x[self.combatlogDict["ID"]] in self.playerList)):
                        if damage1 < 0:
                            damage1 *= -1
                        # update general stats of attacker
                        source = x[self.combatlogDict["source"]]
                        target = x[self.combatlogDict["targetID"]]
                        attacker.totaldamage += damage1
                        if damage1 > attacker.maxOneHit:
                            attacker.maxOneHit = damage1

                        resist = 0
                        if not damagetype == "Shield" and not isMiss:
                            if damage2 == 0:
                                resist = 0
                            else:
                                resist = damage1/damage2*100
                                if not resist == 0:
                                    attacker.resist += resist
                                    attacker.hullAttacks += 1


                        if x[self.combatlogDict["targetID"]] in self.playerList:
                            damaged = self.tableArray[self.playerdict[x[self.combatlogDict["targetID"]]]]
                            damaged.totalDamageTaken += damage1
                            if not source in self.excludeAttacks:
                                damaged.totalAttacksTaken += 1

                        else:
                            damaged = players("name", False, None)

                        #update stats
                        time = self.timeToTimeAndDate(x[self.combatlogDict["date"]])
                        attacker.updateStats(time)
                        #dmg Hanlder        ADD HULL AND SHIELD DAMAGE ROWS

                        hulldamage = 0
                        shielddamage = 0

                        if not source in self.excludeAttacks:
                            attacker.totalAttacks += 1

                        if damagetype == "Shield":
                            shielddamage = damage1
                        else:
                            hulldamage = damage1
                        #DMGout updater
                        dmgOutSource = x[self.combatlogDict["ID"]]
                        if dmgOutSource in damaged.dmginTable:
                            newTargeted = True
                            for col in damaged.dmginTable[damaged.dmgInDict[dmgOutSource]]:
                                if col[damaged.dmgoutindex["target"]] == source:
                                    newTargeted = False
                                    damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][attacker.dmgoutindex["damage"]] += damage1
                                    damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][attacker.dmgoutindex["hulldamage"]] += hulldamage
                                    damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][attacker.dmgoutindex["shielddamage"]] += shielddamage
                                    if not source in self.excludeAttacks:
                                        damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][attacker.dmgoutindex["attacks"]] += 1
                                        col[attacker.dmgoutindex["attacks"]] += 1
                                    col[attacker.dmgoutindex["damage"]] += damage1
                                    col[attacker.dmgoutindex["hulldamage"]] += hulldamage
                                    col[attacker.dmgoutindex["shielddamage"]] += shielddamage
                                    if not damagetype == "Shield" and not isMiss and not resist == 0:
                                        damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][attacker.dmgoutindex["hullAttacks"]] += 1
                                        damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][attacker.dmgoutindex["resist"]] += resist
                                        col[attacker.dmgoutindex["resist"]] += resist
                                    if damage1 > damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][attacker.dmgoutindex["maxHit"]]:
                                        damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][attacker.dmgoutindex["maxHit"]] = damage1
                                    if damage1 > col[attacker.dmgoutindex["maxHit"]]:
                                        col[attacker.dmgoutindex["maxHit"]] = damage1

                                    if isMiss:
                                        damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][attacker.dmgoutindex["misses"]] += 1
                                        col[attacker.dmgoutindex["misses"]] += 1
                                    if isCrit:
                                        damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][attacker.dmgoutindex["crits"]] += 1
                                        col[attacker.dmgoutindex["crits"]] += 1
                                    if isFlank:
                                        damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][attacker.dmgoutindex["flanks"]] += 1
                                        col[attacker.dmgoutindex["flanks"]] += 1
                                    if isKill:
                                        damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][attacker.dmgoutindex["kills"]] += 1
                                        col[attacker.dmgoutindex["kills"]] += 1


                            if newTargeted:
                                damaged.dmginTable[damaged.dmgInDict[dmgOutSource]].append(
                                    [dmgOutSource, source, damage1, 0, damage1, (1 if isCrit else 0),(1 if isFlank else 0), 1, (1 if isMiss else 0), 0, 0, 0, (1 if isKill else 0), hulldamage, shielddamage, (0 if damagetype == "Shield" else resist), 1, 0])
                                damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][attacker.dmgoutindex["damage"]] += damage1
                                damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][attacker.dmgoutindex["hulldamage"]] += hulldamage
                                damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][attacker.dmgoutindex["shielddamage"]] += shielddamage
                                if not damagetype == "Shield" and not isMiss and not resist == 0:
                                    damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][
                                        attacker.dmgoutindex["hullAttacks"]] += 1
                                    damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][
                                        attacker.dmgoutindex["resist"]] += resist
                                if not source in self.excludeAttacks:
                                    damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][attacker.dmgoutindex["attacks"]] += 1
                                if damage1 > damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][attacker.dmgoutindex["maxHit"]]:
                                    damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][attacker.dmgoutindex["maxHit"]] = damage1
                                if isMiss:
                                    damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][attacker.dmgoutindex["misses"]] += 1
                                if isCrit:
                                    damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][attacker.dmgoutindex["crits"]] += 1
                                if isFlank:
                                    damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][attacker.dmgoutindex["flanks"]] += 1
                                if isKill:
                                    damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][attacker.dmgoutindex["kills"]] += 1

                        else:
                            damaged.dmginTable.append([
                                [source, "global", damage1, 0, damage1, (1 if isCrit else 0), (1 if isFlank else 0), 1,
                                 (1 if isMiss else 0), 0, 0, 0, (1 if isKill else 0), hulldamage, shielddamage, (0 if damagetype == "Shield" else resist), 1, 0],
                                [source, target, damage1, 0, damage1, (1 if isCrit else 0),
                                 (1 if isFlank else 0), 1, (1 if isMiss else 0), 0, 0, 0, (1 if isKill else 0), hulldamage, shielddamage, (0 if damagetype == "Shield" else resist), 1, 0]])
                            damaged.dmgInDict.update({dmgOutSource: len(attacker.dmgoutTable) - 1})


                        if source in attacker.dmgoutDict:
                            newTarget = True
                            for col in attacker.dmgoutTable[attacker.dmgoutDict[source]]:
                                if col[attacker.dmgoutindex["target"]] == target:
                                    newTarget = False
                                    attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["damage"]] += damage1
                                    attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["hulldamage"]] += hulldamage
                                    attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["shielddamage"]] += shielddamage
                                    if not source in self.excludeAttacks:
                                        attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["attacks"]] += 1
                                        col[attacker.dmgoutindex["attacks"]] += 1
                                    col[attacker.dmgoutindex["damage"]] += damage1
                                    col[attacker.dmgoutindex["hulldamage"]] += hulldamage
                                    col[attacker.dmgoutindex["shielddamage"]] += shielddamage
                                    if not damagetype == "Shield" and not isMiss and not resist == 0:
                                        attacker.dmgoutTable[attacker.dmgoutDict[source]][0][
                                            attacker.dmgoutindex["hullAttacks"]] += 1
                                        attacker.dmgoutTable[attacker.dmgoutDict[source]][0][
                                            attacker.dmgoutindex["resist"]] += resist
                                        col[attacker.dmgoutindex["resist"]] += resist
                                    if damage1 > attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["maxHit"]]:
                                        attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["maxHit"]] = damage1
                                    if damage1 > col[attacker.dmgoutindex["maxHit"]]:
                                        col[attacker.dmgoutindex["maxHit"]] = damage1
                                    if isMiss:
                                        attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["misses"]] += 1
                                        col[attacker.dmgoutindex["misses"]] += 1
                                    if isCrit:
                                        attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["crits"]] += 1
                                        col[attacker.dmgoutindex["crits"]] += 1
                                    if isFlank:
                                        attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["flanks"]] += 1
                                        col[attacker.dmgoutindex["flanks"]] += 1
                                    if isKill:
                                        attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["kills"]] += 1
                                        col[attacker.dmgoutindex["kills"]] += 1
                            if newTarget:
                                attacker.dmgoutTable[attacker.dmgoutDict[source]].append(
                                    [source, target, damage1, 0, damage1, (1 if isCrit else 0),(1 if isFlank else 0), 1, (1 if isMiss else 0), 0, 0, 0, (1 if isKill else 0), hulldamage, shielddamage, (0 if damagetype == "Shield" else resist), 1, 0])
                                attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["damage"]] += damage1
                                attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["hulldamage"]] += hulldamage
                                attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["shielddamage"]] += shielddamage
                                if not damagetype == "Shield" and not isMiss and not resist == 0:
                                    attacker.dmgoutTable[attacker.dmgoutDict[source]][0][
                                        attacker.dmgoutindex["hullAttacks"]] += 1
                                    attacker.dmgoutTable[attacker.dmgoutDict[source]][0][
                                        attacker.dmgoutindex["resist"]] += resist
                                if not source in self.excludeAttacks:
                                    attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["attacks"]] += 1
                                if damage1 > attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["maxHit"]]:
                                    attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["maxHit"]] = damage1
                                if isMiss:
                                    attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["misses"]] += 1
                                if isCrit:
                                    attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["crits"]] += 1
                                if isFlank:
                                    attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["flanks"]] += 1
                                if isKill:
                                    attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["kills"]] += 1
                        else:
                            attacker.dmgoutTable.append([
                                [source, "global", damage1, 0, damage1, (1 if isCrit else 0), (1 if isFlank else 0), 1,
                                 (1 if isMiss else 0), 0, 0, 0, (1 if isKill else 0), hulldamage, shielddamage, (0 if damagetype == "Shield" else resist), 1, 0],
                                [source, target, damage1, 0, damage1, (1 if isCrit else 0),
                                 (1 if isFlank else 0), 1, (1 if isMiss else 0), 0, 0, 0, (1 if isKill else 0), hulldamage, shielddamage, (0 if damagetype == "Shield" else resist), 1, 0]])
                            attacker.dmgoutDict.update({source: len(attacker.dmgoutTable) - 1})


            #Pets
            else:
                if not x[self.combatlogDict["source"]] in self.excludeDamage:
                    if not ((x[self.combatlogDict["targetID"]] in self.playerList) and (x[self.combatlogDict["ID"]] in self.playerList)):
                        if damage1 < 0:
                            damage1 *= -1
                        player = x[self.combatlogDict["ID"]]
                        sourceID = x[self.combatlogDict["petID"]]
                        weapon = x[self.combatlogDict["source"]]
                        target = x[self.combatlogDict["targetID"]]
                        source = "Pets (sum)"
                        # update general stats of attacker

                        attacker.totaldamage += damage1
                        if damage1 > attacker.maxOneHit:
                            attacker.maxOneHit = damage1

                        if x[self.combatlogDict["targetID"]] in self.playerList:
                            damaged = self.tableArray[self.playerdict[x[self.combatlogDict["targetID"]]]]
                            damaged.totalDamageTaken += damage1
                            if not source in self.excludeAttacks:
                                damaged.totalAttacksTaken += 1
                        else:
                            damaged = players("name", False, None)

                        # update stats
                        time = self.timeToTimeAndDate(x[self.combatlogDict["date"]])
                        attacker.updateStats(time)

                        # specific attacks handler

                        resist = 0
                        if not damagetype == "Shield" and not isMiss:
                            if damage2 == 0:
                                resist = 0
                            else:
                                resist = damage1/damage2*100
                                if not resist == 0:
                                    attacker.resist += resist
                                    attacker.hullAttacks += 1

                        hulldamage = 0
                        shielddamage = 0

                        if damagetype == "Shield":
                            shielddamage = damage1
                        else:
                            hulldamage = damage1



                        if source in attacker.dmgoutDict:
                            newTarget = True
                            for col in attacker.dmgoutTable[attacker.dmgoutDict[source]]:
                                if col[attacker.dmgoutindex["target"]] == target:
                                    newTarget = False
                                    attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["damage"]] += damage1
                                    attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["hulldamage"]] += hulldamage
                                    attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["shielddamage"]] += shielddamage
                                    if not source in self.excludeAttacks:
                                        attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["attacks"]] += 1
                                        col[attacker.dmgoutindex["attacks"]] += 1
                                    col[attacker.dmgoutindex["damage"]] += damage1
                                    col[attacker.dmgoutindex["hulldamage"]] += hulldamage
                                    col[attacker.dmgoutindex["shielddamage"]] += shielddamage
                                    if not damagetype == "Shield" and not isMiss and not resist == 0:
                                        attacker.dmgoutTable[attacker.dmgoutDict[source]][0][
                                            attacker.dmgoutindex["hullAttacks"]] += 1
                                        attacker.dmgoutTable[attacker.dmgoutDict[source]][0][
                                            attacker.dmgoutindex["resist"]] += resist
                                        col[attacker.dmgoutindex["resist"]] += resist
                                    if damage1 > attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["maxHit"]]:
                                        attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["maxHit"]] = damage1
                                    if damage1 > col[attacker.dmgoutindex["maxHit"]]:
                                        col[attacker.dmgoutindex["maxHit"]] = damage1
                                    if isMiss:
                                        attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["misses"]] += 1
                                        col[attacker.dmgoutindex["misses"]] += 1
                                    if isCrit:
                                        attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["crits"]] += 1
                                        col[attacker.dmgoutindex["crits"]] += 1
                                    if isFlank:
                                        attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["flanks"]] += 1
                                        col[attacker.dmgoutindex["flanks"]] += 1
                                    if isKill:
                                        attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["kills"]] += 1
                                        col[attacker.dmgoutindex["kills"]] += 1
                            if newTarget:
                                attacker.dmgoutTable[attacker.dmgoutDict[source]].append(
                                    [source, target, damage1, 0, damage1, (1 if isCrit else 0),(1 if isFlank else 0), 1, (1 if isMiss else 0), 0, 0, 0, (1 if isKill else 0), hulldamage, shielddamage, (0 if damagetype == "Shield" else resist), 1, 0])
                                attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["damage"]] += damage1
                                attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["hulldamage"]] += hulldamage
                                attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["shielddamage"]] += shielddamage
                                if not damagetype == "Shield" and not isMiss and not resist == 0:
                                    attacker.dmgoutTable[attacker.dmgoutDict[source]][0][
                                        attacker.dmgoutindex["hullAttacks"]] += 1
                                    attacker.dmgoutTable[attacker.dmgoutDict[source]][0][
                                        attacker.dmgoutindex["resist"]] += resist
                                if not source in self.excludeAttacks:
                                    attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["attacks"]] += 1
                                if damage1 > attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["maxHit"]]:
                                    attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["maxHit"]] = damage1
                                if isMiss:
                                    attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["misses"]] += 1
                                if isCrit:
                                    attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["crits"]] += 1
                                if isFlank:
                                    attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["flanks"]] += 1
                                if isKill:
                                    attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["kills"]] += 1
                        else:
                            attacker.dmgoutTable.append([
                                [source, "global", damage1, 0, damage1, (1 if isCrit else 0), (1 if isFlank else 0), 1,
                                 (1 if isMiss else 0), 0, 0, 0, (1 if isKill else 0), hulldamage, shielddamage, (0 if damagetype == "Shield" else resist), 1, 0],
                                [source, target, damage1, 0, damage1, (1 if isCrit else 0),
                                 (1 if isFlank else 0), 1, (1 if isMiss else 0), 0, 0, 0, (1 if isKill else 0), hulldamage, shielddamage, (0 if damagetype == "Shield" else resist), 1, 0]])
                            attacker.dmgoutDict.update({source: len(attacker.dmgoutTable) - 1})

                        source = x[self.combatlogDict["pet"]]
                        weaponID = player + source + sourceID + weapon
                        targetID = player + source + sourceID + weapon + target
                        if not source in self.excludeAttacks:
                            attacker.totalAttacks += 1


                        dmgOutSource = x[self.combatlogDict["ID"]]
                        if dmgOutSource in damaged.dmginTable:
                            newTargeted = True
                            for col in damaged.dmginTable[damaged.dmgInDict[dmgOutSource]]:
                                if col[damaged.dmgoutindex["target"]] == source:
                                    newTargeted = False
                                    damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][
                                        attacker.dmgoutindex["damage"]] += damage1
                                    damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][
                                        attacker.dmgoutindex["hulldamage"]] += hulldamage
                                    damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][
                                        attacker.dmgoutindex["shielddamage"]] += shielddamage
                                    if not dmgOutSource in self.excludeAttacks:
                                        damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][
                                            attacker.dmgoutindex["attacks"]] += 1
                                        col[attacker.dmgoutindex["attacks"]] += 1
                                    col[attacker.dmgoutindex["damage"]] += damage1
                                    col[attacker.dmgoutindex["hulldamage"]] += hulldamage
                                    col[attacker.dmgoutindex["shielddamage"]] += shielddamage
                                    if not damagetype == "Shield" and not isMiss and not resist == 0:
                                        damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][
                                            attacker.dmgoutindex["hullAttacks"]] += 1
                                        damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][
                                            attacker.dmgoutindex["resist"]] += resist
                                        col[attacker.dmgoutindex["resist"]] += resist
                                    if damage1 > damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][
                                        attacker.dmgoutindex["maxHit"]]:
                                        damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][
                                            attacker.dmgoutindex["maxHit"]] = damage1
                                    if damage1 > col[attacker.dmgoutindex["maxHit"]]:
                                        col[attacker.dmgoutindex["maxHit"]] = damage1

                                    if isMiss:
                                        damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][
                                            attacker.dmgoutindex["misses"]] += 1
                                        col[attacker.dmgoutindex["misses"]] += 1
                                    if isCrit:
                                        damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][
                                            attacker.dmgoutindex["crits"]] += 1
                                        col[attacker.dmgoutindex["crits"]] += 1
                                    if isFlank:
                                        damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][
                                            attacker.dmgoutindex["flanks"]] += 1
                                        col[attacker.dmgoutindex["flanks"]] += 1
                                    if isKill:
                                        damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][
                                            attacker.dmgoutindex["kills"]] += 1
                                        col[attacker.dmgoutindex["kills"]] += 1
                            if newTargeted:
                                damaged.dmginTable[damaged.dmgInDict[dmgOutSource]].append(
                                    [dmgOutSource, source, damage1, 0, damage1, (1 if isCrit else 0), (1 if isFlank else 0),
                                     1, (1 if isMiss else 0), 0, 0, 0, (1 if isKill else 0), hulldamage, shielddamage, (0 if damagetype == "Shield" else resist), 1, 0])
                                damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][
                                    attacker.dmgoutindex["damage"]] += damage1
                                damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][
                                    attacker.dmgoutindex["hulldamage"]] += hulldamage
                                damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][
                                    attacker.dmgoutindex["shielddamage"]] += shielddamage
                                if not damagetype == "Shield" and not isMiss and not resist == 0:
                                    damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][
                                        attacker.dmgoutindex["hullAttacks"]] += 1
                                    damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][
                                        attacker.dmgoutindex["resist"]] += resist
                                if not dmgOutSource in self.excludeAttacks:
                                    damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][attacker.dmgoutindex["attacks"]] += 1
                                if damage1 > damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][
                                    attacker.dmgoutindex["maxHit"]]:
                                    damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][
                                        attacker.dmgoutindex["maxHit"]] = damage1
                                if isMiss:
                                    damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][
                                        attacker.dmgoutindex["misses"]] += 1
                                if isCrit:
                                    damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][
                                        attacker.dmgoutindex["crits"]] += 1
                                if isFlank:
                                    damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][
                                        attacker.dmgoutindex["flanks"]] += 1
                                if isKill:
                                    damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][
                                        attacker.dmgoutindex["kills"]] += 1

                        else:
                            damaged.dmginTable.append([
                                [source, "global", damage1, 0, damage1, (1 if isCrit else 0), (1 if isFlank else 0), 1,
                                 (1 if isMiss else 0), 0, 0, 0, (1 if isKill else 0), hulldamage, shielddamage, (0 if damagetype == "Shield" else resist), 1, 0],
                                [source, target, damage1, 0, damage1, (1 if isCrit else 0),
                                 (1 if isFlank else 0), 1, (1 if isMiss else 0), 0, 0, 0, (1 if isKill else 0), hulldamage,
                                 shielddamage, (0 if damagetype == "Shield" else resist), 1, 0]])
                            damaged.dmgInDict.update({dmgOutSource: len(attacker.dmgoutTable) - 1})






                        #check if pet type already exists
                        if source in attacker.petSourceDict:
                            #update damage of existing pet type
                            attacker.petDMGTable[attacker.petSourceDict[source]][0][attacker.dmgoutindex["damage"]] += damage1
                            attacker.petDMGTable[attacker.petSourceDict[source]][0][
                                attacker.dmgoutindex["hulldamage"]] += hulldamage
                            attacker.petDMGTable[attacker.petSourceDict[source]][0][
                                attacker.dmgoutindex["shielddamage"]] += shielddamage
                            if not damagetype == "Shield" and not isMiss and not resist == 0:
                                attacker.petDMGTable[attacker.petSourceDict[source]][0][
                                    attacker.dmgoutindex["hullAttacks"]] += 1
                                attacker.petDMGTable[attacker.petSourceDict[source]][0][
                                    attacker.dmgoutindex["resist"]] += resist
                            if not weapon in self.excludeAttacks:
                                attacker.petDMGTable[attacker.petSourceDict[source]][0][attacker.dmgoutindex["attacks"]] += 1
                            if damage1 > attacker.petDMGTable[attacker.petSourceDict[source]][0][attacker.dmgoutindex["maxHit"]]:
                                attacker.petDMGTable[attacker.petSourceDict[source]][0][attacker.dmgoutindex["maxHit"]] = damage1
                            if isMiss:
                                attacker.petDMGTable[attacker.petSourceDict[source]][0][attacker.dmgoutindex["misses"]] += 1
                            if isCrit:
                                attacker.petDMGTable[attacker.petSourceDict[source]][0][attacker.dmgoutindex["crits"]] += 1
                            if isFlank:
                                attacker.petDMGTable[attacker.petSourceDict[source]][0][attacker.dmgoutindex["flanks"]] += 1
                            if isKill:
                                attacker.petDMGTable[attacker.petSourceDict[source]][0][attacker.dmgoutindex["kills"]] += 1

                            #check if pet instance exists
                            if sourceID in attacker.petSourceIDDict:
                                #updateing stats of pet instance
                                attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][0][
                                    attacker.dmgoutindex["damage"]] += damage1
                                attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][0][
                                    attacker.dmgoutindex["hulldamage"]] += hulldamage
                                attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][0][
                                    attacker.dmgoutindex["shielddamage"]] += shielddamage
                                if not damagetype == "Shield" and not isMiss and not resist == 0:
                                    attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][0][
                                        attacker.dmgoutindex["hullAttacks"]] += 1
                                    attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][0][
                                        attacker.dmgoutindex["resist"]] += resist
                                if not weapon in self.excludeAttacks:
                                    attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][0][
                                        attacker.dmgoutindex["attacks"]] += 1
                                if damage1 > attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][0][
                                    attacker.dmgoutindex["maxHit"]]:
                                    attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][0][
                                        attacker.dmgoutindex["maxHit"]] = damage1
                                if isMiss:
                                    attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][0][
                                        attacker.dmgoutindex["misses"]] += 1
                                if isCrit:
                                    attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][0][
                                        attacker.dmgoutindex["crits"]] += 1
                                if isFlank:
                                    attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][0][
                                        attacker.dmgoutindex["flanks"]] += 1
                                if isKill:
                                    attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][0][
                                        attacker.dmgoutindex["kills"]] += 1
                                #check if weapon for pet exists
                                if weaponID in attacker.petWeaponDict:
                                    #update stats
                                    attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]][0][attacker.dmgoutindex["damage"]] += damage1
                                    attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]][0][attacker.dmgoutindex["hulldamage"]] += hulldamage
                                    attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]][0][attacker.dmgoutindex["shielddamage"]] += shielddamage
                                    if not damagetype == "Shield" and not isMiss and not resist == 0:
                                        attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]][0][
                                            attacker.dmgoutindex["hullAttacks"]] += 1
                                        attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]][0][
                                            attacker.dmgoutindex["resist"]] += resist
                                    if not weapon in self.excludeAttacks:
                                        attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]][0][attacker.dmgoutindex["attacks"]] += 1
                                    if damage1 > attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]][0][attacker.dmgoutindex["maxHit"]]:
                                        attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]][0][attacker.dmgoutindex["maxHit"]] = damage1
                                    if isMiss:
                                        attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]][0][attacker.dmgoutindex["misses"]] += 1
                                    if isCrit:
                                        attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]][0][attacker.dmgoutindex["crits"]] += 1
                                    if isFlank:
                                        attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]][0][attacker.dmgoutindex["flanks"]] += 1
                                    if isKill:
                                        attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]][0][attacker.dmgoutindex["kills"]] += 1

                                    if targetID in attacker.petTargetDict:
                                        attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]][attacker.petTargetDict[targetID]][attacker.dmgoutindex["hulldamage"]] += hulldamage
                                        attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]][attacker.petTargetDict[targetID]][attacker.dmgoutindex["damage"]] += damage1
                                        attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]][attacker.petTargetDict[targetID]][attacker.dmgoutindex["shielddamage"]] += shielddamage
                                        if not damagetype == "Shield" and not isMiss and not resist == 0:
                                            attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]][attacker.petTargetDict[targetID]][attacker.dmgoutindex["hullAttacks"]] += 1
                                            attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]][attacker.petTargetDict[targetID]][attacker.dmgoutindex["resist"]] += resist
                                        if not weapon in self.excludeAttacks:
                                            attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]][attacker.petTargetDict[targetID]][attacker.dmgoutindex["attacks"]] += 1
                                        if damage1 > attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]][attacker.petTargetDict[targetID]][attacker.dmgoutindex["maxHit"]]:
                                            attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]][attacker.petTargetDict[targetID]][attacker.dmgoutindex["maxHit"]] = damage1
                                        if isMiss:
                                            attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]][attacker.petTargetDict[targetID]][attacker.dmgoutindex["misses"]] += 1
                                        if isCrit:
                                            attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]][attacker.petTargetDict[targetID]][attacker.dmgoutindex["crits"]] += 1
                                        if isFlank:
                                            attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]][attacker.petTargetDict[targetID]][attacker.dmgoutindex["flanks"]] += 1
                                        if isKill:
                                            attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]][attacker.petTargetDict[targetID]][attacker.dmgoutindex["kills"]] += 1

                                    else:
                                        attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]].append(
                                            [target, "global4", damage1, 0, damage1, (1 if isCrit else 0), (1 if isFlank else 0), 1,
                                             (1 if isMiss else 0), 0, 0, 0, (1 if isKill else 0), hulldamage, shielddamage, (0 if damagetype == "Shield" else resist), 1, 0])
                                        attacker.petTargetDict.update({targetID: len(attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]])-1})

                                else:
                                    #adding new weapon instance
                                    attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]].append([[weapon, "global", damage1, 0, damage1, (1 if isCrit else 0), (1 if isFlank else 0), 1,
                                                                                                                                      (1 if isMiss else 0), 0, 0, 0, (1 if isKill else 0), hulldamage, shielddamage, (0 if damagetype == "Shield" else resist), 1, 0], [target, "global3", damage1, 0, damage1, (1 if isCrit else 0), (1 if isFlank else 0), 1,
                                                                                                                                                                                                                                                                        (1 if isMiss else 0), 0, 0, 0, (1 if isKill else 0), hulldamage, shielddamage, (0 if damagetype == "Shield" else resist), 1, 0]])
                                    attacker.petWeaponDict.update({weaponID: len(attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]])-1})
                                    attacker.petTargetDict.update({targetID: len(attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]])-1})


                            else:
                                #adding a new unique pet to a type of pet
                                attacker.petDMGTable[attacker.petSourceDict[source]].append([[sourceID, "global2", damage1, 0, damage1, (1 if isCrit else 0), (1 if isFlank else 0), 1,
                                                                                              (1 if isMiss else 0), 0, 0, 0, (1 if isKill else 0), hulldamage, shielddamage, (0 if damagetype == "Shield" else resist), 1, 0], [[weapon, "global", damage1, 0, damage1, (1 if isCrit else 0), (1 if isFlank else 0), 1,
                                                                                                                                                                                                                                 (1 if isMiss else 0), 0, 0, 0, (1 if isKill else 0), hulldamage, shielddamage, (0 if damagetype == "Shield" else resist), 1, 0], [target, "global2", damage1, 0, damage1, (1 if isCrit else 0), (1 if isFlank else 0), 1,
                                                                                                                                                                                                                                                                                                                                                                   (1 if isMiss else 0), 0, 0, 0, (1 if isKill else 0), hulldamage, shielddamage, (0 if damagetype == "Shield" else resist), 1, 0]]])
                                attacker.petSourceIDDict.update({sourceID: len(attacker.petDMGTable[attacker.petSourceDict[source]])-1})
                                attacker.petWeaponDict.update({weaponID: len(attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]])-1})
                                attacker.petTargetDict.update({targetID: len(attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]])-1})

                        else:
                            #adding a new pet type
                            attacker.petDMGTable.append([[source, "global", damage1, 0, damage1, (1 if isCrit else 0), (1 if isFlank else 0), 1,
                                                          (1 if isMiss else 0), 0, 0, 0, (1 if isKill else 0), hulldamage, shielddamage, (0 if damagetype == "Shield" else resist), 1, 0], [[sourceID, "global1", damage1, 0, damage1, (1 if isCrit else 0), (1 if isFlank else 0), 1,
                                                                                                                                                                                             (1 if isMiss else 0), 0, 0, 0, (1 if isKill else 0), hulldamage, shielddamage, (0 if damagetype == "Shield" else resist), 1, 0], [[weapon, "global", damage1, 0, damage1, (1 if isCrit else 0), (1 if isFlank else 0), 1,
                                                                                                                                                                                                                                                                                                                                (1 if isMiss else 0), 0, 0, 0, (1 if isKill else 0), hulldamage, shielddamage, (0 if damagetype == "Shield" else resist), 1, 0], [target, "global1", damage1, 0, damage1, (1 if isCrit else 0), (1 if isFlank else 0), 1,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                  (1 if isMiss else 0), 0, 0, 0, (1 if isKill else 0), hulldamage, shielddamage, (0 if damagetype == "Shield" else resist), 1, 0]]]])
                            attacker.petSourceDict.update({source: len(attacker.petDMGTable)-1})
                            attacker.petSourceIDDict.update({sourceID: len(attacker.petDMGTable[attacker.petSourceDict[source]])-1})
                            attacker.petWeaponDict.update({weaponID: len(attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]])-1})
                            attacker.petTargetDict.update({targetID: len(attacker.petDMGTable[attacker.petSourceDict[source]][attacker.petSourceIDDict[sourceID]][attacker.petWeaponDict[weaponID]])-1})

            time = self.timeToTimeAndDate(x[self.combatlogDict["date"]])
            if self.lastGraphTime == None:
                self.lastGraphTime = time
            if (time - self.lastGraphTime) >= self.graphDelta:
                pass
                # do something with graph stuff

            self.lastGraphTime = time

        for table in self.tableArray:
            table.updateTables()







    def detectCombat(self, IDString):
        if IDString in self.mapIdentifiers:
            map = self.mapIdentifiers[IDString]

            if map == "Infected_Space_Elite": #add exceptions for all other maps that have unique entities to identify map difficulty
                self.map = "Infected_Space"
                self.difficulty = "Elite"
            else: #set map
                self.map = map
            if self.map in self.checkSpaceMaps:
                self.isSpace = True
            else:
                self.isSpace = False
        else: #entity not curcial to map identification
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
                    IDcheck = IDcheck[self.combatlogDict["targetID"]-1]
                    wrapperUpdated = False
                    if not IDcheck == "*":
                        targetID = IDcheck.split(" ")
                        targetID = targetID[1].split("]")[0]
                        self.detectCombat(targetID)
                elif not wrapperUpdated:
                    combatInformationWrapper = str( self.removeUnderscore(self.map)) + " " + str(time.day) + "/" + str(
                        time.month) + "/" + str(time.year) + " " + str(time.hour) + ":" + str(
                        time.minute) + ":" + str(time.second)
                    self.otherCombats.update({combatID: (newFile, combatInformationWrapper)})
                    print(combatInformationWrapper)
                    wrapperUpdated = True
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
                if newCombat:
                    combatInformationWrapper = str(self.map) + " " + str(time.day) + "/" + str(time.month) + "/" + str(time.year) + " " + str(time.hour) + ":" + str(time.minute) + ":" + str(time.second)

                    newFile = tempfile.NamedTemporaryFile(mode="w+", delete=True)
                    self.otherCombats.update({combatID: (newFile, combatInformationWrapper)})
                    newFile.write(line)
                    newCombat = False
                else:
                    tmpFile = self.otherCombats[combatID][0]
                    tmpFile.write(line)
                parsedLines += 1
        file = self.otherCombats[len(self.otherCombats)-1][0]
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

    def generatedUItables(self):
        for entity in self.tableArray:
            input = [entity.isPlayer, entity.dmgoutTable, entity.petDMGTable, entity.dmginTable, entity.healsOutTable,
                     entity.petHealsTable, entity.healsInTable]
            self.uiDictionary.update({entity.name: input})

    def readCombatwithUITables(self, path):
        self.setPath(path)
        self.readCombat()
        self.generatedUItables()
        return self.uiDictionary, self.dmgTableIndex, self.healTableIndex, self.uiInputDictionary #, self.otherCombats, self.map, self.difficulty, self.damageChart, self.DPSChart
    def readPreviousCombatwithUITables(self, combatID):
        self.readPreviousCombat(combatID)
        self.generatedUItables()
        return self.uiDictionary, self.dmgTableIndex, self.healTableIndex, self.uiInputDictionary #, self.otherCombats, self.map, self.difficulty, self.damageChart, self.DPSChart
    def generateFrontPageTable(self):  # generates the front page table with a quick summary of combat stats
        self.endTable.append(
            ["player", "combatTime", "DPS", "Total Damage", "CritH", "MaxOneHit", "%debuff", "%damage", "%damage taken",
             "%atks-in", "total heals", "% healed", "deaths"])
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
                        player.finalresist, percentageDamage, percentageTaken, percentageATS, player.totalHeals,
                        percentageHeals, player.deaths]
                temptable.append(temp)
        temptable.sort(key=lambda x:x[2], reverse=True)
        for row in temptable:
            self.endTable.append(row)


    def generateIndividualGraphs(self):
        pass


    def createFrontPageTable(self):
        self.generateFrontPageTable()
        return self.endTable



    def generalStatsCopy(self):
        playerArray = []
        returnString = "OSCR - "
        if self.endTable == []:
            self.generateFrontPageTable()
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
                handle =  self.generateHandle(player.name)
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
                    dps = str(dps[0])+ "," + str(dps[1])[0:1] + "K"
                elif len(dps) == 3:
                    dps = str(dps[0])+ "," + str(dps[1])[0:1] + "M"
                elif len(dps) > 3:
                    dps = str(dps[0])+ "," + str(dps[1])[0:1] + "B"



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
            map = map + "[" + str(minutes) +":" + str(seconds) + "." + str(temp.seconds)[0] + "] DMG(DPS) - "
        else:
            map = map + "[0:" + str(temp.seconds) + "." + str(temp.seconds)[0] + "] DMG(DPS) - "
        playerArray.sort(key=lambda row: row[2], reverse=True)
        mapCopy = map
        for playerinstance in playerArray:
            map = map + playerinstance[0] + ": " + str(playerinstance[1]) + "(" + str(playerinstance[2]) + ") "
            if len(map) > 1000:
                map = mapCopy + playerinstance[0][0:6] + ": " + str(playerinstance[1]) + "(" + str(playerinstance[2]) + ") "


        returnString = returnString + map
        print(returnString)
        print(playerArray)



def main():
    path = "Infected [LR] (S) - 06-06-2020 14.11.45.log"
    parserInstance = parser()
    parserInstance.setPath(path)
    parserInstance.readCombat()
    parserInstance.generalStatsCopy()
    table = parserInstance.createFrontPageTable()
    return table

if __name__ == '__main__':
    main()
