from random import choice
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

        # internal - static
        self.colour = Genes.GetColour(self)
        self.foodChainPlace = Genes.GetFeedingType(self)
        self.IsAcuatic = Genes.GetIsAcuatic(self)

        # internal - dynamic        
        self.health = 100
        self.protein = 10
        self.carbohidrates = 10
        self.energy = 10

        # external - dynamic
        self.position = pos
        self.currDirection = 0 # 0-up   1-right    2-down   3-left        
        self.visibleTiles = [self.position]
        self.dataInVision = []

        # flags
        self.moveNext = False
        self.targetedMove = False
        self.moveTargets = []

    def SetDNA(self, flag):
        self.dna = Organism.GetDNA(flag)

    def SetPos(self, pos):
        self.position = pos

    def Digest(self):
        if self.foodChainPlace == 0:
            Genes.MakeFotosynthesis(self)
        elif self.foodChainPlace == 1:
            Genes.DigestCarbos(self)
        elif self.foodChainPlace == 2:
            Genes.DigestProteines(self)
        elif self.foodChainPlace == 3:
            Genes.DigestOrganicDebris (self)
        else:
            print('foodChainPlace bad value')
            assert False

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
            if p[0] >= 0 and p[0] < len(data) and p[1] >= 0 and p[1] < len(data[0]):
                if p == self.position:
                    split = SplitEveryNChar(data[p[0]][p[1]], 2)
                    split.remove(DecTo2DigitHex(self.foodChainPlace + 12))
                    string = ''
                    for s in split:
                        string += s
                    self.dataInVision.append([(p[0], p[1]), string])
                else:
                    self.dataInVision.append([(p[0], p[1]), data[p[0]][p[1]]])
                

    def Move(self):
        Genes.Movement(self)
        if self.targetedMove:
            for objective in self.moveTargets:
                targetID = objective[0]
                follow = objective[1]
                isFoundTarget = False    
                foundTargets = []            
                for visible in self.dataInVision:
                    if targetID in visible[1]:
                        isFoundTarget = True
                        print('found target')
                        foundTargets.append(visible[0])

                        target = choice(foundTargets)
                        # get nearest path to target (visible[0])
                        dy = target[0] - self.position[0]
                        dx = target[1] - self.position[0]
                        # ojo q lo de abajo podria estar al reves
                        if abs(dy) > abs(dx):
                            self.moveNext = True
                            if GetSign(dy) > 0:
                                if follow:
                                    self.currDirection = 2
                                else:
                                    self.currDirection = 0
                            else:
                                if follow:
                                    self.currDirection = 0
                                else:
                                    self.currDirection = 2
                        elif abs(dy) < abs(dx):
                            self.moveNext = True
                            if GetSign(dx) > 0:
                                if follow:
                                    self.currDirection = 1
                                else:
                                    self.currDirection = 3
                            else:
                                if follow:
                                    self.currDirection = 3
                                else:
                                    self.currDirection = 1
                        else:
                            self.moveNext = False
                        break
            if not isFoundTarget:
                Genes.Movement(self, True)         
        
# helper functions
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
