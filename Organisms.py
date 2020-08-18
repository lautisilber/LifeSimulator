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
    
    def __init__(self, pos, dna=''):
        self.dna = dna

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
        self.visibleTiles = self.position
        self.dataInVision = []

        # flags
        self.moveNext = False

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
            vision = (p[0] + self.position[0], p[1] + self.position[1])
            if vision[0] >= 0 and vision[0] < len(data) and vision[1] >= 0 and vision[1] < len(data[0]):
                if p == (0, 0):
                    split = SplitEveryNChar(data[vision[0]][vision[1]], 2)
                    split.remove(DecTo2DigitHex(self.foodChainPlace))
                    string = ''
                    for s in split:
                        string += s
                    self.dataInVision.append(string)
                else:
                    self.dataInVision.append([vision[0]][vision[1]])
                

    def Move(self):
        Genes.Movement(self)
        
# helper functions
def SplitEveryNChar(string, n):
    return [string[i:i+n] for i in range(0, len(string), n)]

def DecTo2DigitHex(dec):
    return format(dec, '02x').upper()
        
