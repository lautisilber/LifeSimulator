import numpy as np
from random import choice
from Organisms import Organism

class World:

    biomeNames = ['empty', 'grassland', 'forest', 'jungle', 'savanna', 'desert', 'wetland', 'tundra', 'artic', 'reef', 'marine', 'ocean']
    
    def __init__(self, size):
        assert len(size) == 2
        self.size = size
        self.biomeMap = np.zeros(size, dtype=int)
        self.biomes = list()        
        self.populationMap = list()
        self.population = list()
        self.visionMap = list()

        #self.CreateWorld()

    def CreateWorld(self, circle=True):
        from RobertoBiomeGenerator import Roberto
        import random
        
        distribution = list()
        if circle:
            distribution = Roberto.BiomeGeneratorCircle(self.size, len(World.biomeNames) - 1, 2, 6)
        else:
            distribution = Roberto.BiomeGeneratorDiamond(self.size, len(World.biomeNames) - 1, 3, 20)
        a = b = i = 0
        for r in distribution:
            for c in r:
                self.biomes.append(Biome(c))
                self.biomeMap[a][b] = i
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
        for r in indices:
            for c in r:
                self.biomes.append(Biome(c))
                self.biomeMap[a][b] = i
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

    def AddPopulation(self, dnaInit='random', randPos=True, pos=(0, 0)):
        position = pos
        if randPos:
            from random import randint
            position = (randint(0, self.biomeMap.shape[0] - 1), randint(0, self.biomeMap.shape[1] - 1))            
        self.population.append(Organism(position, dnaInit))
        print(position)

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
                self.visionMap[r][c] += DecTo2DigitHex(self.biomes[self.biomeMap[r][c]].index)
                for pindex in self.populationMap[r][c]:
                    self.visionMap[r][c] += DecTo2DigitHex(self.population[pindex].foodChainPlace + 12)

    def UpdatePopulationVision(self):
        for p in self.population:
            p.See(self.visionMap)

    def PopulationEat(self):
        for p in self.population:
            p.Eat()

    def Move(self):
        for p in self.population:
            p.Move()
            print(p.moveNext)
            if p.moveNext:
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
                p.moveNext = False                        
            print(p.position)
                
    def Loop(self):
        self.WriteVisionMap()
        self.UpdatePopulationVision()
        self.PopulationEat()
        self.Move()

class Biome:
    def __init__(self, index):
        self.index = index
        self.name = World.biomeNames[self.index]
        self.colour = Biome.GetColourFromName(self.name)
        self.light = Biome.GetLightFromName(self.name)
        self.temperature = Biome.GetTempFromName(self.name)
        self.humidity = Biome.GetHumFromName(self.name)
        self.organicDebris = 0

    @staticmethod
    def GetColourFromName(name):
        colDict = {
            'empty' : (192, 192, 192),
            'grassland' : (0, 255, 0),
            'forest' : (0, 135, 0),
            'jungle' : (153, 255, 102),
            'savanna' : (255, 153, 0),
            'desert' : (255, 255, 0),
            'wetland' : (0, 153, 153),
            'tundra' : (204, 255, 255),
            'artic' : (255, 255, 255),
            'reef' : (153, 255, 255),
            'marine' : (0, 255, 255),
            'ocean' : (0, 102, 204)
        }
        return colDict[name]

    @staticmethod 
    def GetLightFromName(name):
        # Light level is 0 - 100
        lightDict = {
            'empty' : 0,
            'grassland' : 70,
            'forest' : 60,
            'jungle' : 80,
            'savanna' : 90,
            'desert' : 100,
            'wetland' : 50,
            'tundra' : 40,
            'artic' : 20,
            'reef' : 80,
            'marine' : 50,
            'ocean' : 10
        }
        return lightDict[name]

    @staticmethod 
    def GetTempFromName(name):
        # Temperature level is 0 - 100
        tempDict = {
            'empty' : 0,
            'grassland' : 40,
            'forest' : 50,
            'jungle' : 80,
            'savanna' : 90,
            'desert' : 100,
            'wetland' : 50,
            'tundra' : 10,
            'artic' : 5,
            'reef' : 70,
            'marine' : 30,
            'ocean' : 15
        }
        return tempDict[name]

    @staticmethod 
    def GetHumFromName(name):
        # Humidity level is 0 - 100
        tempDict = {
            'empty' : 0,
            'grassland' : 50,
            'forest' : 60,
            'jungle' : 95,
            'savanna' : 35,
            'desert' : 5,
            'wetland' : 85,
            'tundra' : 25,
            'artic' : 5,
            'reef' : 100,
            'marine' : 100,
            'ocean' : 100
        }
        return tempDict[name]

# helper functions
def DecTo2DigitHex(dec):
    return format(dec, '02x').upper()
