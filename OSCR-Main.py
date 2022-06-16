import datetime

#first draft

path = "combatlog.log" #input path to combatlog here
counter = 0
combatlog = []          #unspliced combatlog
combatlogDict = {"date": 0, "character": 1, "ID": 2, "pet": 3, "petID": 4, "target": 5, "targetID": 6,
                 "source": 7, "sourceID": 8, "dmageType": 9, "flags": 10, "mag1": 11, "mag2": 12}   #dictonary of spliced combatlog
playerdict = {}         #dictionary all entities, gives ID and returns position of that ID in tableArray
playerList = []         #list of all players
NPCs = []               #list of all NPCs
newCombatLog = []       #combatlog with spliced lines
tableArray = []         #array with all the player class'
otherslist = []         #all pet damage abilities
mainlist = []           #all non pet damage abiliites

class players:          #main container class, used for saving stats on all entities
    def __init__(self, name, isPlayer, time):
        self.isPlayer = isPlayer
        self.combatOver = False
        self.name = name
        self.dmgoutindex = {"name": 0, "target": 1, "damage": 2, "DPS": 3, "maxHit": 4, "crits": 5, "flanks": 6, "attacks": 7, "misses": 8, "CrtH": 9, "acc": 10, "flankrate": 11, "kills": 12, "hulldamage": 13, "shielddamage": 14}
        self.dmgoutTable = []
        self.dmgoutDict = {}
        self.dmginTable = []    #to be added
        self.dmgInDict = {}     #to be added
        self.healsOutTable = [] #to be added
        self.healsInTable = []  #to be added
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
    def updateStats(self, time2):
        self.temptotalAttacks = self.totalAttacks - self.misses
        self.totalTime = (time2 - self.startTime).total_seconds()
        self.runtime = self.totalTime
        self.endTime = time2
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
        for cols in self.dmgoutTable:
            for row in cols:
                self.tmpDamage = row[self.dmgoutindex["damage"]]
                self.tmpCrits = row[self.dmgoutindex["crits"]]
                self.tmpAttacks = row[self.dmgoutindex["attacks"]]
                self.tmpMisses = row[self.dmgoutindex["misses"]]
                self.tmpFlanks = row[self.dmgoutindex["flanks"]]
                row[self.dmgoutindex["DPS"]] = self.tmpDamage/self.combatTime
                self.temporalAttacks = self.tmpAttacks - self.tmpMisses
                if self.temporalAttacks >= 1 and self.tmpAttacks >= 1 and self.tmpCrits >= 1 and self.tmpFlanks >= 1:
                    row[self.dmgoutindex["CrtH"]] = self.tmpCrits / self.temporalAttacks * 100
                    row[self.dmgoutindex["flankrate"]] = self.tmpFlanks / self.temporalAttacks * 100
                    row[self.dmgoutindex["acc"]] = self.temporalAttacks / self.tmpAttacks * 100
                elif self.temporalAttacks >= 1 and self.tmpAttacks >= 1 and self.tmpCrits >= 1:
                    row[self.dmgoutindex["CrtH"]] = self.tmpCrits / self.temporalAttacks * 100
                    row[self.dmgoutindex["acc"]] = self.temporalAttacks / self.tmpAttacks * 100
                    row[self.dmgoutindex["flankrate"]] = 0
                elif self.temporalAttacks >= 1 and self.tmpAttacks >= 1:
                    row[self.dmgoutindex["CrtH"]] = 0
                    row[self.dmgoutindex["acc"]] = self.temporalAttacks / self.tmpAttacks * 100
                    row[self.dmgoutindex["flankrate"]] = 0
    def updatePetsDMGOutTable(self):
        pass    #to be added
    def updateDMGInTable(self):
        pass    #to be added
    def updateHealsTable(self):
        pass    #to be added
    def updatePetHealsTable(self):
        pass    #to be added
    def updateHealingInTable(self):
        pass    #to be added

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
    endTable = [["player", "combatTime", "DPS", "Total Damage", "CritH", "MaxOneHit", "%damage", "%damage taken", "%atks-in", "total heals", "% healed" , "deaths"]]
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
            temp = [handle, player.totalTime, player.DPS, player.totaldamage, player.crtH, player.maxOneHit, percentageDamage, percentageTaken, percentageATS, player.totalHeals, percentageHeals, player.deaths]
            endTable.append(temp)
            #re add heals
    #some order function, might be better in the visual driver for allowing the user to filter by stats

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

def main():     #for now the functinos for reading the .log file into arrays, slicing arrays and generating all the data tables are together in 1 function, eventually will be split up
    global path, combatlogDict, combatlog, newCombatLog, tableArray, playerdict, NPCs
    with open(path, "r") as file:
        for line in file:
           combatlog.append(line)
    for x in combatlog:
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


        attacker = tableArray[playerdict[x[combatlogDict["ID"]]]]
        # attacker = players("name", True, None)
        damage1 = float(x[combatlogDict["mag1"]])
        damage2 = float(x[combatlogDict["mag2"]])
        damagetype = x[combatlogDict["dmageType"]]
        #first handle heals
        if damagetype == "HitPoints":
            if damage1 < 0:
                damage1 *= -1
            attacker.totalHeals += damage1
        #Shieldheals
        elif damagetype == "Shield" and damage1 < 0 and damage2 >= 0:
            if damage1 < 0:
                damage1 *= -1
            attacker.totalHeals += damage1
        #pets
        elif x[combatlogDict["pet"]] == "*" or x[combatlogDict["targetID"]] == "*":
            if not damagetype == "Warp Core Breach":
                if damage1 < 0:
                    damage1 *= -1
                # update general stats of attacker
                attacker.totalAttacks += 1
                attacker.totaldamage += damage1
                if damage1 > attacker.maxOneHit:
                    attacker.maxOneHit = damage1

                if x[combatlogDict["targetID"]] in playerList:
                    damaged = tableArray[playerdict[x[combatlogDict["targetID"]]]]
                    damaged.totalAttacksTaken += 1
                    damaged.totalDamageTaken += damage1

                #update stats
                time = timeToTimeAndDate(x[combatlogDict["date"]])
                attacker.updateStats(time)
                #keeps log of all damageing abilities DEBUG ONLY FOR NOW
                if not x[combatlogDict["source"]] in mainlist:
                    mainlist.append(x[combatlogDict["source"]])
               #flag updater
                isCrit, isMiss, isFlank, isKill = getFlags(x[combatlogDict["flags"]])
                if isMiss:
                    attacker.misses += 1
                if isCrit:
                    attacker.totalCrits += 1
                if isFlank:
                    attacker.flanks = attacker.flanks + 1
                if isKill:
                    attacker.kills += 1
                #dmg Hanlder        ADD HULL AND SHIELD DAMAGE ROWS
                source = x[combatlogDict["source"]]
                target = x[combatlogDict["targetID"]]
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
                            attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["attacks"]] += 1
                            col[attacker.dmgoutindex["damage"]] += damage1
                            col[attacker.dmgoutindex["hulldamage"]] += hulldamage
                            col[attacker.dmgoutindex["shielddamage"]] += shielddamage
                            col[attacker.dmgoutindex["attacks"]] += 1
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
                            [source, target, damage1, 0, damage1, (1 if isCrit else 0),(1 if isFlank else 0), 1, (1 if isMiss else 0), 0, 0, 0, (1 if isKill else 0), hulldamage, shielddamage])
                        attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["damage"]] += damage1
                        attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["hulldamage"]] += hulldamage
                        attacker.dmgoutTable[attacker.dmgoutDict[source]][0][attacker.dmgoutindex["shielddamage"]] += shielddamage

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
                         (1 if isMiss else 0), 0, 0, 0, (1 if isKill else 0), hulldamage, shielddamage],
                        [source, target, damage1, 0, damage1, (1 if isCrit else 0),
                         (1 if isFlank else 0), 1, (1 if isMiss else 0), 0, 0, 0, (1 if isKill else 0), hulldamage, shielddamage]])
                    attacker.dmgoutDict.update({source: len(attacker.dmgoutTable) - 1})



        else:
            if not damagetype == "Warp Core Breach":
                if not damagetype == "Warp Core Breach":
                    if damage1 < 0:
                        damage1 *= -1
                    # update general stats of attacker
                    attacker.totalAttacks += 1
                    attacker.totaldamage += damage1
                    if damage1 > attacker.maxOneHit:
                        attacker.maxOneHit = damage1

                    if x[combatlogDict["targetID"]] in playerList:
                        damaged = tableArray[playerdict[x[combatlogDict["targetID"]]]]
                        damaged.totalAttacksTaken += 1
                        damaged.totalDamageTaken += damage1

                    # update stats
                    time = timeToTimeAndDate(x[combatlogDict["date"]])
                    attacker.updateStats(time)
                    # keeps log of all damageing abilities DEBUG ONLY FOR NOW
                    if not x[combatlogDict["source"]] in mainlist:
                        mainlist.append(x[combatlogDict["source"]])

                    isCrit, isMiss, isFlank, isKill = getFlags(x[combatlogDict["flags"]])
                    if isMiss:
                        attacker.misses += 1
                    if isCrit:
                        attacker.totalCrits += 1
                    if isFlank:
                        attacker.flanks = attacker.flanks + 1
                    if isKill:
                        attacker.kills += 1

                    # specific attacks handler



    for table in tableArray:
        if table.isPlayer:      #comment/uncomment all the data that you want printed.
            table.updateTables()
            print("                 ", table.name)
            # print("damage: ", table.totaldamage)
            # print("DPS: ", table.DPS)
            # print("maxOneHit: ", table.maxOneHit)
            # print("CrtH: ", table.crtH)
            # print("acc: ", table.acc)
            # print("flanks: ", table.flankRate)
            # print("runtime: ", table.runtime)
            # print("tank stats: ", table.totalDamageTaken, table.totalAttacksTaken)
            for col in table.dmgoutTable:
                print(col)
        # if not table.isPlayer:                printing stats on NPCs
        #     table.updateTables()
        #     print("                 ", table.name)
        #     # print("damage: ", table.totaldamage)
        #     # print("DPS: ", table.DPS)
        #     # print("maxOneHit: ", table.maxOneHit)
        #     # print("CrtH: ", table.crtH)
        #     # print("acc: ", table.acc)
        #     # print("flanks: ", table.flankRate)
        #     # print("runtime: ", table.runtime)
        #     # print("tank stats: ", table.totalDamageTaken, table.totalAttacksTaken)
        #     for col in table.dmgoutTable:
        #         print(col)

    frontpageTable = createFrontPageTable()
    for player in frontpageTable:
        print(player)


if __name__ == "__main__":
    main()