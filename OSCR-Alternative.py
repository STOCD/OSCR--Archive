import datetime
import tempfile
import time as timer

#first draft

path = "Combatlog2.Log" #input path to combatlog here. 2 combatlogs in the file are a ISE run by Spencer, previously provided by Gaus' version and a personal ISA run
counter = 0
globalcombatlog = []          #unspliced combatlog
combatlogDict = {"date": 0, "character": 1, "ID": 2, "pet": 3, "petID": 4, "target": 5, "targetID": 6,
                 "source": 7, "sourceID": 8, "dmageType": 9, "flags": 10, "mag1": 11, "mag2": 12}   #dictonary of spliced combatlog
playerdict = {}         #dictionary all entities, gives ID and returns position of that ID in tableArray
playerList = []         #list of all players
NPCs = []               #list of all NPCs
newCombatLog = []       #combatlog with spliced lines
tableArray = []         #array with all the player class'
otherslist = []         #all pet damage abilities
mainlist = []           #all non pet damage abiliites
templist = []
excludeAttacks = ["Shield Scraping II", "Tachyon Charges"]
excludeDamage = ["Warp Core Breach"]
exculdedHealTicks = []
otherCombats = []


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
            self.finalresist = self.resist/self.hullAttacks
        if not self.totalTime == 0:
            self.DPS = self.totaldamage/self.totalTime
        if self.temptotalAttacks >= 1 and self.totalAttacks >= 1 and self.totalCrits >= 1 and self.flanks >= 1:
            self.crtH = self.totalCrits/self.temptotalAttacks * 100
            self.flankRate = self.flanks/self.temptotalAttacks * 100
            self.acc = self.temptotalAttacks/self.totalAttacks * 100
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
                if  col[self.dmgoutindex["hullAttacks"]] ==  0:
                    print(col[self.dmgoutindex["hullAttacks"]], col[self.dmgoutindex["resist"]])
                else:
                    col[self.dmgoutindex["finalResist"]] = col[self.dmgoutindex["resist"]]/col[self.dmgoutindex["hullAttacks"]]

                col[self.dmgoutindex["DPS"]] = self.tmpDamage/self.combatTime
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
                    #update pet type stats
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
                            #update pet instance stats
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
                                #update pet weapon and target stats
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
                            #update pet instance stats
                            self.tmpHealsOut = cols2[self.healOutIndex["healtotal"]]
                            self.tmpCrits = cols2[self.healOutIndex["Crits"]]
                            self.tmpTicks = cols2[self.healOutIndex["healticks"]]
                            cols2[self.healOutIndex["HPS"]] = self.tmpHealsOut / self.combatTime
                            if self.tmpCrits > 0:
                                cols2[self.healOutIndex["CrtH"]] = self.tmpCrits / self.tmpTicks
                        else:
                            for cols3 in cols2:
                                #update pet weapon and target stats
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


counter2 = 0
def createTableInstance(line):      #creates a new class instance and appends to list
    global counter2
    if line[combatlogDict["ID"]][0] == "P":
        player = True
    else:
        player = False
    ID = line[combatlogDict["ID"]]
    if player:
        tableArray.append(players(ID, True, timeToTimeAndDate(line[combatlogDict["date"]])))
        playerdict.update({ID: counter2})
        counter2 += 1
    else:
        tableArray.append(players(ID, False, timeToTimeAndDate(line[combatlogDict["date"]])))
        playerdict.update({ID: counter2})
        counter2 += 1

def timeToTimeAndDate(timeSplice):  #turns combatlog time string into TimeDate object
    timeSplice = timeSplice.split(":")
    seconds = timeSplice.pop()
    seconds = seconds.split(".")
    timeSplice.append(seconds[0])
    timeSplice.append(seconds[1])
    timeSplice[0] = int(timeSplice[0])+2000

    time = datetime.datetime(timeSplice[0], int(timeSplice[1]), int(timeSplice[2]), int(timeSplice[3]), int(timeSplice[4]), int(timeSplice[5]), int(timeSplice[6])*100000)

    return time

def generateHandle(IDSplyce):       #returns player handle, can further splice this for only @xxxx or character name.
    IDSplyce = IDSplyce.split(" ")
    IDSplyce = IDSplyce[1]
    IDSplyce = IDSplyce[:-1]
    return IDSplyce

def generateID(IDSplyce):           #returns player ID (not necessary if necessary, might be removed down the road if unnecessary
    OGSplyce = IDSplyce
    IDSplyce = IDSplyce.split(" ")
    IDSplyce = IDSplyce[0]
    IDSplyce = IDSplyce.split("[")
    if IDSplyce[0] == "C":
        name = "unkownNPC"
        for y in NPCs:
            if y[1] == OGSplyce:
                name = y[0]
        returner = name + " " + IDSplyce[1]
        return returner
    else:
        return IDSplyce[1]


def createFrontPageTable():     #generates the front page table with a quick summary of combat stats
    endTable = [["player", "combatTime", "DPS", "Total Damage", "CritH", "MaxOneHit", "%debuff", "%damage", "%damage taken", "%atks-in", "total heals", "% healed" , "deaths"]]
    totalDamage = 0
    totalTaken = 0
    totalAtks = 0
    totalHeals = 0
    for player in tableArray:
        if player.isPlayer:
            totalDamage += player.totaldamage
            totalTaken += player.totalDamageTaken
            totalAtks += player.totalAttacksTaken
            totalHeals += player.totalHeals

    for player in tableArray:
        if player.isPlayer:
            percentageDamage = player.totaldamage/totalDamage * 100
            percentageATS = player.totalAttacksTaken/totalAtks * 100
            percentageTaken = player.totalDamageTaken/totalTaken * 100
            percentageHeals = player.totalHeals/totalHeals * 100
            handle = generateHandle(player.name)
            temp = [handle, player.totalTime, player.DPS, player.totaldamage, player.crtH, player.maxOneHit, player.finalresist, percentageDamage, percentageTaken, percentageATS, player.totalHeals, percentageHeals, player.deaths]
            endTable.append(temp)

    return endTable

def getFlags(flagUpdater):      #returns flags combat lines
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

#main driver to read combats
def combatLogAnalysis():
    for x in globalcombatlog:
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
        if not x[combatlogDict["ID"]] in playerList:
            if x[combatlogDict["ID"]][0] == "P":
                playerList.append(x[combatlogDict["ID"]])
                createTableInstance(x)
            elif not [x[combatlogDict["character"]], x[combatlogDict["ID"]]] in NPCs:
                NPCs.append(x[combatlogDict["ID"]])
                createTableInstance(x)

        newCombatLog.append(x)
        # if not x[combatlogDict["targetID"]] in templist and x[combatlogDict["sourceID"]] == "P[12231228@5044720 CasualSAB@spencerb96]":
        #     templist.append(x[combatlogDict["targetID"]])
        #     print("adsfaf", x[combatlogDict["targetID"]])

        attacker = tableArray[playerdict[x[combatlogDict["ID"]]]]

        # flag updater
        isCrit, isMiss, isFlank, isKill = getFlags(x[combatlogDict["flags"]])
        if isMiss:
            attacker.misses += 1
        if isCrit:
            attacker.totalCrits += 1
        if isFlank:
            attacker.flanks = attacker.flanks + 1
        if isKill:
            attacker.kills += 1
            if x[combatlogDict["targetID"]] in playerdict:
                tableArray[playerdict[x[combatlogDict["targetID"]]]].deaths += 1

        # attacker = players("name", True, None)
        damage1 = float(x[combatlogDict["mag1"]])
        damage2 = float(x[combatlogDict["mag2"]])
        damagetype = x[combatlogDict["dmageType"]]

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
            source = x[combatlogDict["source"]]
            target = x[combatlogDict["targetID"]]
            if x[combatlogDict["targetID"]] in playerList:
                damaged = tableArray[playerdict[x[combatlogDict["targetID"]]]]
            else:
                damaged = players("name", False, None)

            #non pet heals
            if x[combatlogDict["pet"]] == "*" or x[combatlogDict["targetID"]] == "*":
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
                            if not source in exculdedHealTicks:
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
                        if not source in excludeAttacks:
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
                dmgOutSource = x[combatlogDict["ID"]]
                if dmgOutSource in damaged.healsInTable:
                    newTargeted = True
                    for col in damaged.healsInTable[damaged.healsInDict[dmgOutSource]]:
                        if col[damaged.healOutIndex["target"]] == source:
                            newTargeted = False
                            damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][attacker.healOutIndex["healtotal"]] += damage1
                            damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][attacker.healOutIndex["hullheal"]] += hullHeal
                            damaged.healsInTable[damaged.healsInDict[dmgOutSource]][0][attacker.healOutIndex["shieldheal"]] += shieldHeal
                            if not source in exculdedHealTicks:
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
                        if not source in excludeAttacks:
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
                source = x[combatlogDict["pet"]]
                sourceID = x[combatlogDict["petID"]]
                ability = x[combatlogDict["source"]]
                target = x[combatlogDict["targetID"]]
                dmgOutSource = x[combatlogDict["ID"]]
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
                            if not source in exculdedHealTicks:
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
                        if not source in excludeAttacks:
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

                if sourceID in attacker.petHealsIDDict:
                    #updateing stats of pet instance
                    attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][0][
                        attacker.healOutIndex["healtotal"]] += damage1
                    attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][0][
                        attacker.healOutIndex["hullheal"]] += hullHeal
                    attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][0][
                        attacker.healOutIndex["shieldheal"]] += shieldHeal
                    if not ability in exculdedHealTicks:
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
                            if not ability in exculdedHealTicks:
                                attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][attacker.petAbilityDict[abilityID]][0][attacker.healOutIndex["healticks"]] += 1
                            if damage1 > attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][attacker.petAbilityDict[abilityID]][0][attacker.healOutIndex["maxHeal"]]:
                                attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][attacker.petAbilityDict[abilityID]][0][attacker.healOutIndex["maxHeal"]] = damage1
                            if isCrit:
                                attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][attacker.petAbilityDict[abilityID]][0][attacker.healOutIndex["Crits"]] += 1

                            if targetID in attacker.petHealTargetDict:
                                attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][attacker.petAbilityDict[abilityID]][attacker.petHealTargetDict[targetID]][attacker.healOutIndex["healtotal"]] += damage1
                                attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][attacker.petAbilityDict[abilityID]][attacker.petHealTargetDict[targetID]][attacker.healOutIndex["hullheal"]] += hullHeal
                                attacker.petHealsTable[attacker.petHealSourceDict[source]][attacker.petHealsIDDict[sourceID]][attacker.petAbilityDict[abilityID]][attacker.petHealTargetDict[targetID]][attacker.healOutIndex["shieldheal"]] += shieldHeal
                                if not ability in exculdedHealTicks:
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





        #Non pets


        elif (x[combatlogDict["pet"]] == "*" or x[combatlogDict["targetID"]] == "*") and damagetype != "HitPoints":
            if not x[combatlogDict["source"]] in excludeDamage:
                if not ((x[combatlogDict["targetID"]] in playerList) and (x[combatlogDict["ID"]] in playerList)):
                    if damage1 < 0:
                        damage1 *= -1
                    # update general stats of attacker
                    source = x[combatlogDict["source"]]
                    target = x[combatlogDict["targetID"]]
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


                    if x[combatlogDict["targetID"]] in playerList:
                        damaged = tableArray[playerdict[x[combatlogDict["targetID"]]]]
                        damaged.totalDamageTaken += damage1
                        if not source in excludeAttacks:
                            damaged.totalAttacksTaken += 1

                    else:
                        damaged = players("name", False, None)

                    #update stats
                    time = timeToTimeAndDate(x[combatlogDict["date"]])
                    attacker.updateStats(time)
                    #keeps log of all damageing abilities DEBUG ONLY FOR NOW
                    if not x[combatlogDict["source"]] in mainlist:
                        mainlist.append(x[combatlogDict["source"]])


                    #dmg Hanlder        ADD HULL AND SHIELD DAMAGE ROWS

                    hulldamage = 0
                    shielddamage = 0

                    if not source in excludeAttacks:
                        attacker.totalAttacks += 1

                    if damagetype == "Shield":
                        shielddamage = damage1
                    else:
                        hulldamage = damage1
                    #DMGout updater
                    dmgOutSource = x[combatlogDict["ID"]]
                    if dmgOutSource in damaged.dmginTable:
                        newTargeted = True
                        for col in damaged.dmginTable[damaged.dmgInDict[dmgOutSource]]:
                            if col[damaged.dmgoutindex["target"]] == source:
                                newTargeted = False
                                damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][attacker.dmgoutindex["damage"]] += damage1
                                damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][attacker.dmgoutindex["hulldamage"]] += hulldamage
                                damaged.dmginTable[damaged.dmgInDict[dmgOutSource]][0][attacker.dmgoutindex["shielddamage"]] += shielddamage
                                if not source in excludeAttacks:
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
                            if not source in excludeAttacks:
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
                                if not source in excludeAttacks:
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
                            if not source in excludeAttacks:
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
            if not x[combatlogDict["source"]] in excludeDamage:
                if not ((x[combatlogDict["targetID"]] in playerList) and (x[combatlogDict["ID"]] in playerList)):
                    if damage1 < 0:
                        damage1 *= -1
                    player = x[combatlogDict["ID"]]
                    source = x[combatlogDict["pet"]]
                    sourceID = x[combatlogDict["petID"]]
                    weapon = x[combatlogDict["source"]]
                    target = x[combatlogDict["targetID"]]
                    weaponID = player + source + sourceID + weapon
                    targetID = player + source + sourceID + weapon + target
                    # update general stats of attacker
                    if not source in excludeAttacks:
                        attacker.totalAttacks += 1

                    attacker.totaldamage += damage1
                    if damage1 > attacker.maxOneHit:
                        attacker.maxOneHit = damage1

                    if x[combatlogDict["targetID"]] in playerList:
                        damaged = tableArray[playerdict[x[combatlogDict["targetID"]]]]
                        damaged.totalDamageTaken += damage1
                        if not source in excludeAttacks:
                            damaged.totalAttacksTaken += 1
                    else:
                        damaged = players("name", False, None)

                    # update stats
                    time = timeToTimeAndDate(x[combatlogDict["date"]])
                    attacker.updateStats(time)
                    # keeps log of all damageing abilities DEBUG ONLY FOR NOW
                    if not x[combatlogDict["source"]] in mainlist:
                        mainlist.append(x[combatlogDict["source"]])

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

                    dmgOutSource = x[combatlogDict["ID"]]
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
                                if not dmgOutSource in excludeAttacks:
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
                            if not dmgOutSource in excludeAttacks:
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
                        if not weapon in excludeAttacks:
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
                            if not weapon in excludeAttacks:
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
                                if not weapon in excludeAttacks:
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
                                    if not weapon in excludeAttacks:
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



    for table in tableArray:
        table.updateTables()

# read combat loop
def readCombat(inmediatlyReadFirstCombat=True):
    # time between combats
    combatDelta = datetime.timedelta(seconds = 100)
    # first combat to read
    combatlog = []
    # next Combat to save
    #combat ID
    combatID = 1
    #tracks amount of parsed lines, to prevent single lines to go through, as this will casue issues
    parsedLines = 0
    #read files loop
    newCombat = True
    firstCombat = True
    with open(path, "r") as file:
        start = timer.time()
        for line in file:
            initialLineSplice = line.split("::")
            timeCheck = initialLineSplice[0]
            time = timeToTimeAndDate(timeCheck)
            parsedLines += 1
            if firstCombat:
                lastTime = time
                firstCombat = False
            if newCombat:
                print("new Combat")
                newfile = tempfile.NamedTemporaryFile(mode="w+", delete=True)
                otherCombats.append((combatID, newfile))
                newfile.write(line)
                newCombat = False
            else:
                newfile = otherCombats[combatID - 2]
                newfile = newfile[1]
                newfile.write(line)
            betweencombatDetla = time - lastTime
            lastTime = time
            if betweencombatDetla > combatDelta:
                if parsedLines < 2:
                    otherCombats.pop()
                else:
                    newCombat = True
    combat = otherCombats[combatID-2]
    file = combat[1]
    file.seek(0)
    lines = file.readlines()
    for line in lines:
        print(line)
        globalcombatlog.append(line)
    combatLogAnalysis()


    lastTime = timer.time()
    run = lastTime - start
    print(run)


def changePath(newPath):
    path = newPath

def readPreviousCombat(combatID):
    combat = otherCombats[combatID-2]
    file = combat[1]
    file.seek(0)
    lines = file.readlines()
    for line in lines:
        globalcombatlog.append(line)
    combatLogAnalysis()

def main():
    global path, combatlogDict, combatlog, newCombatLog, tableArray, playerdict, NPCs, excludeDamage, excludeAttacks, exculdedHealTicks
    readCombat()
    print(tableArray)
    prontpageTable = createFrontPageTable()
    for player in prontpageTable:
        print(player)



if __name__ == '__main__':
    main()
