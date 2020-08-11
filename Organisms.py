import Environment
from Genes import Genes

# Vision things ID system 2 hex digit long (for now)
#   
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

class Organism:
    def __init__(self, dna, pos):
        self.dna = dna
        self.worldDimensions = list()        
        self.colour = Genes.GetColour(self)
        self.foodChainPlace = Genes.GetFeedingType(self)
        self.IsAcuatic = Genes.GetIsAcuatic(self)
        self.health = 100
        self.position = pos
        self.protein = 10
        self.carbohidrates = 10
        self.energy = 10
        self.currDirection = 0 # 0-up   1-right    2-down   3-left
        self.currentBiome = Environment.Biome('empty')
        self.moveNext = False
        self.visibleTiles = self.position

    def SetWorldDimensions(self, dim):
        assert len(dim) == 2
        self.worldDimensions = dim

    def Metabolism(self):
        pass