import math
import random
# numberOfGene:dataRequiredToExpressGene-numberOfSecondGene:DataToExpressSecondGene
# for example:
# 0:FFFFFF-1:A
# this is a gene for an organism of colour white (255, 255, 255) 
# and a fotosynthetic gene with a production rate of 10

class Genes:
    size = (1000, 1000)

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
        # from light and humidity produces carbos
        fotGene = DecodeGene(organism.dna, 3)
        if fotGene == '_':
            return
        prodPercentageGenes = 10
        prodPercentageLight = 10
        prodPercentageHum = 10
        
        lightAvailability = organism.currBiome.light
        humAvailability = organism.currBiome.humidity
        geneProductionRate = GetAvgFromHex(fotGene)
        genesProd = mapVal(geneProductionRate, 0, 15, 0, prodPercentageGenes)
        lightProd = mapVal(lightAvailability, 0, 100, 0, prodPercentageLight)
        humProd = mapVal(humAvailability, 0, 100, 0, prodPercentageHum)
        carbosProduced = genesProd * min(lightProd, humProd)
        organism.carbohidrates += carbosProduced
        organism.Limit()

    #4
    @staticmethod
    def DigestOrganicDebris(organism):
        #similar to fotosynthesis only less efficient and produces energy directly
        debGene = DecodeGene(organism.dna, 4)
        if debGene == '_':
            return
        prodPercentageGenes = 3
        prodPercentageDebris = 1 # one debris represents x energy
        
        digestRate = mapVal(GetAvgFromHex(debGene), 0, 15, 0, prodPercentageGenes)
        totDebris = organism.currOrganicDebris
        takenDebris = 0
        if digestRate <= totDebris:
            organism.currentBiomie.organicDebris = totDebris - digestRate
            takenDebris = digestRate # energy
        else:
            organism.currentBiomie.organicDebris = 0
            takenDebris = totDebris # energy
        organism.energy += takenDebris * prodPercentageDebris
        organism.Limit()

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
        # is 8 digits long for consistency
        visGene = DecodeGene(organism.dna, 8)
        if visGene == '_':
            return
        visionType = round(mapVal(GetAvgFromHex(visGene), 0, 15, 0, 3))
        tiles = GetVisibleCoords(organism.position, visionType, organism.currDirection)
        organism.visibleTiles = []
        for t in tiles:
            if t[0] >= 0 and t[0] < Genes.size[0] and t[1] >= 0 and t[1] < Genes.size[1]:
                organism.visibleTiles.append(t)

    #9, 10, 11
    @staticmethod
    def Movement(organism, forceRandom=False):
        # data is distributed in the following way:
        # 9: average of 4 digits defines move motive
        #   00000000 - 55555555 -> doesn't move
        #   66666666 - AAAAAAAA-> moves at random
        #   BBBBBBBB - FFFFFFFF-> moves if target in vision (X represents the amount of elements of interest (max 10))
        # 10: random average of all digits is taken and 0 = 0% and F = 100%
        # 11: if target in vision:
        #       AABBCCCC DDEEFFFF GGHHIIII ...
        #       target id is [avg(AA) avg(BB)]
        #       bool if follow is avg(CCCC)

        motGene = DecodeGene(organism.dna, 9)
        chaGene = DecodeGene(organism.dna, 10)
        tarGene = DecodeGene(organism.dna, 11)
        motive = GetAvgFromHex(motGene)
        if forceRandom:
            motive = 10
        if motive <= 5: # no movement
            organism.moveNext = False
            organism.targetedMove = False
            return
        elif motive <= 10: # random movement
            organism.currDirection = random.randint(0, 3)
            organism.targetedMove = False
            if random.random() < mapVal(GetAvgFromHex(chaGene), 0, 15, 0, 1):
                organism.moveNext = True
            else:
                organism.moveNext = False
        else: # targeted movement
            organism.targetedMove = True
            targetData = DivideStrAfterChunkSize(tarGene, 8)
            targets = list() # [target id in decimal, follow]
            for target in targetData:
                dec1 = GetAvgFromHex(target[:4], 2)
                hex1 = DecTo2DigitHex(dec1)
                follow = GetBoolFromHex(target[4:])
                targets.append([hex1, follow])
            organism.moveTargets = targets # unused
            targetCoords, follow = GetTarget(targets, organism.dataInVision)
            if targetCoords:
                direction = DirectionFinding(organism.position, targetCoords, follow)
                if direction == -1:
                    organism.moveNext = False
                else:
                    organism.currDirection = direction
                    organism.moveNext = True
            else:
                Genes.Movement(organism, True)

        if not organism.moveNext:
            organism.currDirection = random.choice([0, 1, 2, 3])

# helper functions
def GetTarget(targets, dataInVision):
    foundTargets = list()
    for t in targets:
        foundTargets = []
        for d in dataInVision:
            if t[0] in d[1]:
                print('found target')
                foundTargets.append([d[0], t[1]])
        if foundTargets:
            break
    if not foundTargets:
        return None, True
    target = random.choice(foundTargets)
    return target[0], target[1]

def DirectionFinding(origin, target, follow=True):
    dy = target[0] - origin[0]
    dx = target[1] - origin[1]
    if abs(dy) > abs(dx):
        if (dy > 0 and follow) or (dy < 0 and not follow):
            return 0
        elif (dy < 0 and follow) or (dy > 0 and not follow):
            return 2
        else:
            print('error direction finding (helper function in genes.py')
    if abs(dy) < abs(dx):
        if (dx > 0 and follow) or (dx < 0 and not follow):
            return 1
        elif (dx < 0 and follow) or (dx > 0 and not follow):
            return 3
        else:
            print('error direction finding (helper function in genes.py')
    else:
        if dy == 0 and dx == 0:
            return -1
        if random.random() < 0.5:
            if (dy > 0 and follow) or (dy < 0 and not follow):
                return 0
            elif (dy < 0 and follow) or (dy > 0 and not follow):
                return 2
            else:
                print('error direction finding (helper function in genes.py')                                
        else:
            if (dx > 0 and follow) or (dx < 0 and not follow):
                return 1
            elif (dx < 0 and follow) or (dx > 0 and not follow):
                return 3
            else:
                print('error direction finding (helper function in genes.py')

# maps value with range of iMin - iMax to a range of oMin - oMax
def mapVal(val, iMin, iMax, oMin, oMax):
    return oMin + ((float(val - iMin) / float(iMax - iMin)) * (oMax - oMin))

def HexToRGB(hexCode):
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
    vision = [(v[1], v[0]) for v in vision] # invert components
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

def DecTo2DigitHex(dec):
    return format(dec, '02x').upper()
