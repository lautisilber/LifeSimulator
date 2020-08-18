import math
import random
# Shape of a gene
# numberOfGene:dataRequiredToExpressGene-numberOfSecondGene:DataToExpressSecondGene
# for example:
# 0:FFFFFF-1:A
# this is a gene for an organism of colour white (255, 255, 255) 
# and a fotosynthetic gene with a production rate of 10

class Genes:
# INTERNAL ACTIONS
    #0
    @staticmethod
    def GetColour(organism):
        colourCode = DecodeGene(organism.dna, 0)
        return HexToRGB(colourCode)

    #1
    @staticmethod
    def GetIsAcuatic(organism):
        acuGene = DecodeGene(organism.dna, 1)
        return GetBoolFromHex(acuGene)

    #2
    @staticmethod
    def GetFeedingType(organism):
        # it's 8 hex digits whose average indicate the organism's food chain place
        # 0 is Plant, 1 is Hervibore, 2 is Carnivore, 3 is Decomposer        
        aliGene = DecodeGene(organism.dna, 2)
        val = GetAvgFromHex(aliGene)
        return round(mapVal(val, 0, 15, 0, 4))

    #3
    @staticmethod
    def MakeFotosynthesis(organism):
        # can produce from 0 to 10 energy each time
        # energy production rate: 0 - 10 (0 - 9 is rate, A - F is 0)
        fotGene = DecodeGene(organism.dna, 3)
        if fotGene == '_':
            return
        lightAvailability = organism.currentBiomie.light
        humAvailability = organism.currentBiomie.humidity
        energyProductionRate = GetAvgFromHex(fotGene)
        if energyProductionRate > 9:
            energyProductionRate = 0
        produced = energyProductionRate * min(lightAvailability, humAvailability)
        organism.energy += mapVal(produced, 0, 1000, 0, 10)

    #4
    @staticmethod
    def DigestOrganicDebris(organism):
        # rate 0 - 5
        # A - F is 0 production
        # 0 - 9 is rate floor(/ 2)
        debGene = DecodeGene(organism.dna, 4)
        if debGene == '_':
            return
        totDebris = organism.currentBiomie.organicDebris
        digestRate = GetAvgFromHex(debGene)
        if digestRate > 9:
            digestRate = 0
        digestRate = math.floor(digestRate / 2)
        if digestRate <= totDebris:
            organism.currentBiomie.organicDebris = totDebris - digestRate
            organism.energy += digestRate # energy
        else:
            organism.currentBiomie.organicDebris = 0
            organism.energy += totDebris # energy

    #5
    @staticmethod
    def DigestCarbos(organism):
        # percentage 0 - 100
        # transforms a percentage of carbos from the total to energy and removes that ammount of carbos
        # 2 energy is produced by 1 carbo
        carGene = DecodeGene(organism.dna, 5)
        if carGene == '_':
            return
        conversionRate = 2
        carbosEmployed = organism.carbohidrates * (GetAvgFromHex(carGene) / 100)
        organism.energy += carbosEmployed * conversionRate
        organism.carbohidrates -= carbosEmployed

    #6
    @staticmethod
    def DigestProteines(organism):
        # percentage 0 - 100
        # transforms a percentage of prots from the total to energy and removes that ammount of prots
        # 4 energy is produced by 1 prot
        proGene = DecodeGene(organism.dna, 6)
        if proGene == '_':
            return
        conversionRate = 6
        protsEmployed = organism.protein * (GetAvgFromHex(proGene) / 100)
        organism.energy += protsEmployed * conversionRate
        organism.protein -= protsEmployed

    #7
    @staticmethod
    def Heal(organism):
        # for each energy, 1 health is restored
        # return points healed, remaining health
        heaGene = DecodeGene(organism.dna, 7)
        if heaGene == '_':
            return
        healRate = GetAvgFromHex(heaGene)
        if organism.energy >= healRate:
            organism.health += healRate
            organism.energy -= healRate
            if organism.health > 100:
                organism.health = 100
        else:
            organism.health += organism.energy
            organism.energy = 0

# SENSING ACTIONS
    #8
    @staticmethod
    def Vision(organism):
        # is 4 digits long for consistency
        visGene = DecodeGene(organism.dna, 8)
        if visGene == '_':
            return
        visionType = round(GetAvgFromHex(visGene) / 4)
        organism.visibleTiles = GetVisibleCoords(organism.position, visionType, organism.currDirection)

    #9 and 10
    @staticmethod
    def Movement(organism):
        # data is distributed in the following way:
        # 9: average of 4 digits defines move motive
        #   0000XXXX - 5555XXXX -> doesn't move
        #   6666XXXX - AAAAXXXX-> moves at random
        #   BBBBXXXX - FFFFXXXX-> moves if target in vision (X represents the amount of elements of interest (max 10))
        # 10: nothing if not moving
        #   if random average of all digits is taken and 0 = 0% and F = 100%
        #   if target in vision:
        #       AABBCCCC DDEEFFFF GGHHIIII ...
        #       target id is [avg(AA) avg(BB)]
        #       bool if follow is avg(CCCC)

        motGene = DecodeGene(organism.dna, 9)
        minGene = DecodeGene(organism.dna, 10)
        motive = GetAvgFromHex(motGene[:4])
        if motive <= 5:
            organism.moveNext = False
            return
        elif motive <= 10:
            organism.currDirection = random.randint(0, 3)
            percentage = mapVal(GetAvgFromHex(minGene), 0, 15, 0, 1)
            if random.random() < percentage:
                organism.moveNext = True
            else:
                organism.moveNext = False
        else:
            targetNumber = GetAvgFromHex(motGene[4:])
            targetData = DivideStrAfterChunkSize(minGene[:targetNumber * 8], 8)
            targets = list() # [target id in decimal, follow]
            for target in targetData:
                hex1 = GetAvgFromHex(target[:2])
                hex2 = GetAvgFromHex(target[2:4])
                follow = GetBoolFromHex(target[4:])
                targets.append([hex1 + hex2, follow])

        @staticmethod
        def Eat(organism, otherHealth):
            pass


# maps value with range of iMin - iMax to a range of oMin - oMax
def mapVal(val, iMin, iMax, oMin, oMax):
    return oMin + ((float(val - iMin) / float(iMax - iMin)) * (oMax - oMin))

def HexToRGB(hexCode):
    print(hexCode)
    assert isinstance(hexCode, str)
    hexCode = hexCode.lstrip('#')
    return tuple(int(hexCode[i:i+2], 16) for i in (0, 2, 4))

def HexToDec(hexCode):
    assert isinstance(hexCode, str)
    return int(hexCode, 16)

def DecodeGene(dna, geneNr):
    key = str(geneNr) + ':'
    if key in dna:
        s = dna[dna.find(key) + len(key):]
        if '-' in s:
            return s[:s.find('-')]
        else:
            return s
    else:
        return '#'

def GetVisibleCoords(origin, visionType, direction):
    # VisionType
    #
    #   0
    #               O
    #   1
    #                     .
    #                   . .
    #               O . . .
    #                   . .
    #                     .
    #   2
    #               .
    #             . . .
    #           . . O . .
    #             . . .
    #               .
    #   3
    #               . .
    #               . . .
    #               O . .
    #               . . .
    #               . .
    #
    # Direction
    #
    #   0 -> up
    #   1 -> right
    #   2 -> down
    #   3 -> left

    if visionType == 0:
        return [origin]

    
    vision = []
    ox = origin[0]
    oy = origin[1]
    if visionType == 1:
        vision = [
            (0, 0),
            (1, 0), (2, 0), (3, 0),
            (2, 1), (3, 1),
            (2, -1), (3, -1),
            (3, 2),
            (3, -2)
        ]
    elif visionType == 2:
        vision = [
            (0, 0),
            (-2, 0), (-1, 0), (1, 0), (2, 0),
            (-1,1), (0, 1), (1, 1),
            (-1, -1), (0, -1), (1, -1),
            (0, 2),
            (0, -2)
        ]
    elif visionType == 3:
        vision = [
            (0, 0),
            (1, 0), (2, 0),
            (0, 1), (1, 1), (2, 1),
            (0, -1), (1, -1), (2, -1),
            (0, 2),  (1, 2),
            (0, -2), (1, -2)
        ]

    r = 1
    if direction == 2 or direction == 3:
        r = -1
    if direction == 1 or direction == 3:
        return [(c[0] * r + ox, c[1] * r + oy) for c in vision]
    if direction == 0 or direction == 2:
        return [(c[1] * r + ox, c[0] * r + oy) for c in vision]

def DivideStrAfterChunkSize(string, size):
    return [string[i:i+size] for i in range(0, len(string), size)]

def GetAvgFromHex(hexString, digitLength=1):
    s = DivideStrAfterChunkSize(hexString, digitLength)
    avg = 0
    for d in s:
        avg += HexToDec(d)
    avg /= len(s)
    return round(avg)

def GetBoolFromHex(hexCode):
    val = round(mapVal(GetAvgFromHex(hexCode), 0, 15, 0, 1))
    if val == 1:
        return True
    elif val == 0:
        return False
    else:
        assert False
