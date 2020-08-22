import random
from Genes import Genes
from DNA import DNA

# Vision things ID system 2 hex digit long (for now)
#   00 - 0A --> Biomes in order ['empty', 'grassland', 'forest', 'jungle', 'savanna', 
#                               'desert', 'wetland', 'tundra', 'artic', 'reef', 'marine', 'ocean']
#
#   0C - 0F --> organisms of type ['plant', 'hervibore', 'carnivore', 'decomposer']
#
#   for now anything else represents no target

class Organism:
    @staticmethod
    def GetDNA(flag):
        return DNA.GetDNAFromFlag(flag)
    
    def __init__(self, pos, dna='random'):
        self.dna = Organism.GetDNA(dna)

        self.female = True
        if random.random() < 0.5:
            self.female = False

        # internal - static
        self.colour = Genes.GetColour(self)
        self.foodChainPlace = Genes.GetFeedingType(self)
        self.IsAcuatic = Genes.GetIsAcuatic(self)

        # internal - dynamic
        self.age = 0
        self.health = 100
        self.protein = 10
        self.carbohidrates = 10
        self.energy = 10

        # external - dynamic
        self.position = pos
        self.currDirection = 0 # 0-up   1-right    2-down   3-left        
        self.visibleTiles = [self.position]
        self.dataInVision = []
        self.currBiome

        # flags
        self.moveNext = False
        self.targetedMove = False
        self.moveTargets = []

    def SetDNA(self, flag):
        self.dna = Organism.GetDNA(flag)

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

    def See(self):
        Genes.Vision(self)

    def AdjustVisibleTiles(self, newVisibleTiles):
        self.visibleTiles = newVisibleTiles

    def SetVisionData(self, data):
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
                
    def Move(self):
        Genes.Movement(self)

    def Eat(self):
        if self.foodChainPlace == 0:
            Genes.MaekFotosynthesis(self)
        elif self.foodChainPlace == 1:
            self.EatPlant()
        elif self.foodChainPlace == 2:
            self.EatHervibore()
        elif self.foodChainPlace == 3:
            

    def EatPlant(self):
        for loc in self.dataInVision:
            if loc[0] == self.position and '0C' in loc[1]:
                pass
            # EAT PLANT

    def EatHervibore(self):
        for loc in self.dataInVision:
            if loc[0] == self.position and '0D' in loc[1]:
                pass
            # EAT HERVIBORE
        
    def IsAlive(self):
        if self.age > 100 or health <= 0:
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
