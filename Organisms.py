import Environment
from Genes import Genes

class Organism:
    def __init__(self, dna, pos):
        self.dna = dna
        self.colour = Genes.GetColour(self)
        self.health = 100
        self.position = pos
        self.protein = 10
        self.carbohidrates = 10
        self.energy = 10
        self.currentBiome = Environment.Biome('empty')

    def SetCurrBiome(self):
        self.currentBiome = Environment.World.GetBiomeFrom2DCoord(self.position)

    def Metabolism(self):
        pass