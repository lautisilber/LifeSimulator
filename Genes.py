from Environment import Biome
from Organisms import Organism
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
    def MakeFotosynthesis(organism):
        # can produce from 0 to 10 energy each time
        # energy production rate: 0 - 10
        fotGene = DecodeGene(organism.dna, 1)
        if FotGene == '_':
            return
        lightAvailability = organism.currentBiomie.light
        humAvailability = organism.currentBiomie.humidity
        energyProductionRate = HexToDec(FotGene)
        produced = energyProductionRate * min(lightAvailability, humAvailability)
        organism.energy += mapVal(produced, 0, 1000, 0, 10)

    #2
    @staticmethod
    def DigestOrganicDebris(organism):
        # rate 0 - 5
        debGene = DecodeGene(organism.dna, 2)
        if debGene == '_':
            return
        totDebris = organism.currentBiomie.organicDebris
        rate = HexToDec(debGene)
        if rate <= totDebris:
            biome.organicDebris = totDebris - rate
            organism.energy += rate # energy
        else:
            biome.organicDebris = 0
            organism.energy += totDebris # energy

    #3
    @staticmethod
    def DigestCarbos(organism):
        # percentage 0 - 100
        # transforms a percentage of carbos from the total to energy and removes that ammount of carbos
        # 2 energy is produced by 1 carbo
        carGene = DecodeGene(organism.dna, 3)
        if carGene == '_':
            return
        conversionRate = 2
        carbosEmployed = organism.carbohidrates * (HexToDec(carGene) / 100)
        organism.energy += carbosEmployed * conversionRate
        organism.carbohidrates -= carbosEmployed

    #4
    @staticmethod
    def DigestProteines(organism):
        # percentage 0 - 100
        # transforms a percentage of prots from the total to energy and removes that ammount of prots
        # 4 energy is produced by 1 prot
        proGene = DecodeGene(organism.dna, 4)
        if carGene == '_':
            return
        conversionRate = 6
        protsEmployed = Organism.protein * (HexToDec(proGene) / 100)
        organism.energy += protsEmployed * conversionRate
        organism.protein -= protsEmployed

    #5
    @staticmethod
    def Heal(organism):
        # for each energy, 1 health is restored
        # return points healed, remaining health
        heaGene = DecodeGene(organism.dna, 4)
        if heaGene == '_':
            return
        healRate = HexToDec(heaGene)
        if organism.energy >= healRate:
            organism.health += healRate
            organism.energy -= healRate
            if organism.health > 100:
                organism.health = 100
        else:
            organism.health += organism.energy
            organism.energy = 0

# EXTERNAL ACTIONS
    #6
    @staticmethod
    def Move(direction, steps, energyMin, totEnergy):
        moveCost = 10


    

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
        s = dna[string.find(key) + len(key):]
        if '-' in s:
            return s[:s.find('-')]
        else:
            return s
    else:
        return '_'