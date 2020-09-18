import random
from Genes import Genes
from DNA import DNA
from Biome import Biome

# Vision things ID system 2 hex digit long (for now)
#   00 - 0A --> Biomes in order ['empty', 'grassland', 'forest', 'jungle', 'savanna', 
#                               'desert', 'wetland', 'tundra', 'artic', 'reef', 'marine', 'ocean']
#
#   0C - 0F --> organisms of type ['plant', 'hervibore', 'carnivore', 'decomposer']
#
#   for now anything else represents no target
# 
# Metabolism cycle:
#   See
#   Eat
#   Digest
#   Move
#   Check life parameters

class Organism:

    # natural energy decay
    energyDecay = 10 # 1 energy loss every x cycles

    # global movement variables
    moveCost = 1
    minMoveEnergy = 10
    foreignBiomeEnergyPenalty = 2
    
    # global mating rules
    matingCooldown = 10

    # organism IDs
    organismIDs = ['0C', '0D', '0E', '0F']

    def __init__(self, pos, dna='random'):
        self.dna = DNA.GetDNAFromFlag(dna)

        self.female = True
        if random.random() < 0.5:
            self.female = False

        # global info
        self.moveCost = Organism.moveCost

        # internal - static
        self.colour = Genes.GetColour(self)
        self.foodChainPlace = Genes.GetFeedingType(self)
        self.isAcuatic = Genes.GetisAcuatic(self)
        self.isFemale = random.choice([True, False])

        # internal - dynamic
        self.age = 0
        self.health = 100
        self.protein = 10
        self.carbohidrates = 10
        self.energy = 100
        self.alive = True
        self.matingCooldown = 0

        # external - dynamic
        self.position = pos
        self.currDirection = 0 # 0-up   1-right    2-down   3-left        
        self.visibleTiles = [self.position]
        self.dataInVision = []
        self.currBiome = Biome(0)

        # flags
        self.moveNext = False
        self.targetedMove = False
        self.moveTargets = []
        self.decayClock = 0

    def SetDNA(self, flag):
        self.dna = DNA.GetDNAFromFlag(flag)

    def SetPos(self, pos):
        self.position = pos

    def SetBiome(self, biome):
        self.currBiome = biome

    def Limit(self):
        if self.health > 100:
            self.health = 100
        if self.energy > 100:
            self.energy = 100
        if self.carbohidrates > 100:
            self.carbohidrates = 100
        if self.protein > 100:
            self.protein = 100

    def Digest(self):
        Genes.DigestCarbos(self)
        Genes.DigestProteines(self)
        Genes.DigestOrganicDebris (self)

    def Heal(self):
        if self.health < 100:
            Genes.Heal(self)

    def See(self, data):
        Genes.Vision(self)
        self.dataInVision = []
        for p in self.visibleTiles:
            vision = p # (p[0] + self.position[0], p[1] + self.position[1])
            if vision[0] >= 0 and vision[0] < len(data) and vision[1] >= 0 and vision[1] < len(data[0]):
                if p == self.position:
                    split = SplitEveryNChar(data[vision[0]][vision[1]], 2)
                    split.remove(DecTo2DigitHex(self.foodChainPlace + 12))
                    string = ''
                    for s in split:
                        string += s
                    self.dataInVision.append([(vision[0], vision[1]), string])
                else:
                    self.dataInVision.append([(vision[0], vision[1]), data[vision[0]][vision[1]]])

    def AdjustVisibleTiles(self, newVisibleTiles):
        self.visibleTiles = newVisibleTiles
                
    def Move(self):
        Genes.Movement(self)

    def Eat(self):
        if self.foodChainPlace == 0:
            Genes.MakeFotosynthesis(self)
        elif self.foodChainPlace == 1:
            self.EatPlant()
        elif self.foodChainPlace == 2:
            self.EatHervibore()
        elif self.foodChainPlace == 3:
            Genes.DigestOrganicDebris(self)

    def EatPlant(self):
        radius = [self.position, (self.position[0], self.position[1] + 1), (self.position[0], self.position[1] - 1),
        (self.position[0] + 1, self.position[1]), (self.position[0] - 1, self.position[1]), (self.position[0] + 1, self.position[1] + 1),
        (self.position[0] + 1, self.position[1] - 1), (self.position[0] - 1, self.position[1] + 1), (self.position[0] - 1, self.position[1] - 1)]
        for loc in self.dataInVision:
            if loc[0] in radius and '0C' in loc[1]:
                return [loc[0], '0C']
            else:
                return []
            # EAT PLANT - return to environment eaten organism diet type and location to environment

    def EatHervibore(self):
        radius = [self.position, (self.position[0], self.position[1] + 1), (self.position[0], self.position[1] - 1),
        (self.position[0] + 1, self.position[1]), (self.position[0] - 1, self.position[1]), (self.position[0] + 1, self.position[1] + 1),
        (self.position[0] + 1, self.position[1] - 1), (self.position[0] - 1, self.position[1] + 1), (self.position[0] - 1, self.position[1] - 1)]
        for loc in self.dataInVision:
            if loc[0] in radius and '0D' in loc[1]:
                return [loc[0], '0D']
            else:
                return []
            # EAT HERVIBORE - same as EatPlant()

    def SelfCheck(self):
        self.decayClock += 1
        if self.decayClock >= Organism.energyDecay:
            self.energy -= 1
            self.decayClock = 0
        if self.energy <= 0:
            self.alive = False
        if (self.isAcuatic and self.currBiome.humidity != 100) or (not self.isAcuatic and self.currBiome.humidity == 100):
            self.energy -= Organism.foreignBiomeEnergyPenalty
        self.Limit()
        
    def IsAlive(self):
        if self.age > 100 or self.health <= 0 or self.energy <= 0:
            return False
        return True

def SplitEveryNChar(string, n):
    return [string[i:i+n] for i in range(0, len(string), n)]

def DecTo2DigitHex(dec):
    return format(dec, '02x').upper()

def GetSign(n):
    if n > 0:
        return 1
    elif n < 0:
        return -1
    else:
        return 0
