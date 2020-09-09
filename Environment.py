import numpy as np
from Genes import Genes
from random import choice
from Organisms import Organism
from Biome import Biome

class World:
    #biomeNames = ['empty', 'grassland', 'forest', 'jungle', 'savanna', 'desert', 'wetland', 'tundra', 'artic', 'reef', 'marine', 'ocean']
    
    def __init__(self, size):
        assert len(size) == 2
        self.size = size
        self.biomes = list()

        self.population = list()

        self.populationMap = list()
        self.visionMap = list()
        
        Genes.size = self.size

        #self.CreateWorld()

    def CreateWorld(self, circle=True):
        from RobertoBiomeGenerator import Roberto
        import random
        
        distribution = list()
        if circle:
            distribution = Roberto.BiomeGeneratorCircle(self.size, len(Biome.biomeNames) - 1, 2, 6)
        else:
            distribution = Roberto.BiomeGeneratorDiamond(self.size, len(Biome.biomeNames) - 1, 3, 20)
        a = b = i = 0
        for r in range(distribution.shape[0]):
            self.biomes.append([])
            for c in range(distribution.shape[1]):
                self.biomes[r].append(Biome(distribution[r][c]))
                i += 1
                b += 1
            a += 1
            b = 0
        for r in range(self.size[0]):
            self.populationMap.append([])
            self.visionMap.append([])
            for c in range(self.size[1]):
                self.populationMap[r].append([])
                self.visionMap[r].append('')

    def CreateCustomWorld(self, indices):
        #assert indices.size == self.size

        a = b = i = 0
        for r in range(self.size[0]):
            self.biomes.append([])
            for c in range(self.size[1]):
                self.biomes[r].append(Biome(indices[r][c]))              
                i += 1
                b += 1
            a += 1
            b = 0

        for r in range(self.size[0]):
            self.populationMap.append([])
            self.visionMap.append([])
            for c in range(self.size[1]):
                self.populationMap[r].append([])            
                self.visionMap[r].append('')

    def SpawnRandom(self, amount=1):
        for _ in range(amount):
            self.AddPopulation()

    def AddPopulation(self, dnaInit='random', pos=(-1, -1)):
        if pos == (-1, -1):
            from random import randint
            pos = (randint(0, self.size[0] - 1), randint(0, self.size[1] - 1))                    
        self.population.append(Organism(pos, dnaInit))
        self.population[len(self.population) - 1].SetBiome(self.biomes[pos[0]][pos[1]])
        print(pos)

    def WritePopulationMap(self):
        for r in range(self.size[0]):
            for c in range(self.size[1]):
                self.populationMap[r][c] = []
        for i in range(len(self.population)):
            pos = self.population[i].position
            self.populationMap[pos[0]][pos[1]].append(i)

    def WriteVisionMap(self):
        self.WritePopulationMap()
        for r in range(self.size[0]):
            for c in range(self.size[1]):
                self.visionMap[r][c] = ''
        for r in range(self.size[0]):
            for c in range(self.size[1]):                
                self.visionMap[r][c] += DecTo2DigitHex(self.biomes[r][c].index)
                for pindex in self.populationMap[r][c]:
                    self.visionMap[r][c] += DecTo2DigitHex(self.population[pindex].foodChainPlace + 12)

    def UpdatePopulationVision(self):
        for p in self.population:
            p.See(self.visionMap)

    def PopulationEat(self):
        for p in self.population:
            p.Eat()

    def PopulationCheck(self):
        deadOrganisms = []
        i = 0
        for p in self.population:
            p.SelfCheck()
            if not p.alive:
                pos = p.position
                self.biomes[pos[0]][pos[1]].organicDebris += p.carbohidrates + p.protein * 2
                deadOrganisms.append(i)
            i += 1
        deadOrganisms.reverse()
        for index in deadOrganisms:
            del self.population[index]
                

    def UpdateOrganismBiomes(self):
        for p in self.population:
            pos = p.position
            p.SetBiome(self.biomes[pos[0]][pos[1]])

    def Move(self):
        for p in self.population:
            p.Move()
            print(p.moveNext)
            if p.moveNext and p.energy > Organism.minMoveEnergy:
                lastPos = p.position
                if p.currDirection == 0 and p.position[0] + 1 < self.size[0]:
                    p.position = (p.position[0] + 1, p.position[1])
                elif p.currDirection == 1 and p.position[1] + 1 < self.size[1]:
                    p.position = (p.position[0], p.position[1] + 1)
                elif p.currDirection == 2 and p.position[0] - 1 >= 0:
                    p.position = (p.position[0] - 1, p.position[1])
                elif p.currDirection == 3 and p.position[1] - 1 >= 0:
                    p.position = (p.position[0], p.position[1] - 1)
                else:
                    p.currDirection = choice([0, 1, 2, 3])

                if lastPos != p.position:
                    p.energy -= Organism.moveCost
                p.SetBiome(self.biomes[p.position[0]][p.position[1]])                
                p.moveNext = False                    
            print(p.position)            
                
    def Loop(self):
        self.WriteVisionMap()
        self.UpdatePopulationVision()
        self.PopulationEat()
        self.Move()
        self.UpdateOrganismBiomes()
        self.PopulationCheck()

# helper functions
def DecTo2DigitHex(dec):
    return format(dec, '02x').upper()
